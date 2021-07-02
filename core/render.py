from dataclasses import dataclass
from functools import cached_property
from functools import lru_cache
from typing import Iterable
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Tuple
from typing import Union

from django.utils.html import escape
from django.utils.safestring import SafeString
from django.utils.safestring import mark_safe
from rich.ansi import AnsiDecoder
from rich.console import Console
from rich.segment import Segment
from rich.style import Style
from rich.text import Text

__all__ = ["Span", "SpanRow"]


COLOR_CLASSES = [
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "bright-black",
    "bright-red",
    "bright-green",
    "bright-yellow",
    "bright-blue",
    "bright-magenta",
    "bright-cyan",
    "bright-white",
]


class Inline(NamedTuple):
    property_: str
    value: str

    @cached_property
    def markup(self) -> SafeString:
        return escape(f"{self.property_}: {self.value}")


@dataclass(frozen=True)
class Span:
    text: str
    classes: Optional[Tuple[str]] = None
    inlines: Optional[Tuple[Inline]] = None

    @classmethod
    @lru_cache
    def from_style(cls, text: str, style: Style):
        classes = []
        inlines = []

        color = style.color
        bgcolor = style.bgcolor

        if style.reverse:
            color, bgcolor = bgcolor, color

        color_class = True
        color_hex = None

        if not color:
            if not style.reverse:
                classes.append("fgcolor")
            else:
                classes.append("bgcolor")
        else:
            if color.is_system_defined:
                classes.append(COLOR_CLASSES[color.number])
            else:
                color_class = False
                color_hex = color.get_truecolor().hex
                inlines.append(f"text-color: {color_hex}")
                inlines.append(f"text-decoration-color: {color_hex}")
                inlines.append(f"border-color: {color_hex}")

        if style.bold:
            if color_class:
                classes.append("-bold")
            else:
                inlines.append(
                    f"text-shadow: -0.25px 0 {color_hex}, -0.25px 0 {color_hex}"
                )
        if style.dim:
            # TODO figure out dim style that is:
            #      - theme agnostic
            #      - wont break column spacing
            #      - doesnt affect bgcolor
            #      possibly just create a parent span for bgcolor then use opacity
            pass
        if style.italic:
            inlines.append("font-style: italic")
        if style.underline:
            inlines.append("font-style: underline")
        if style.strike:
            inlines.append("font-style: line-through")
        if style.overline:
            inlines.append("font-style: overline")

        if not bgcolor:
            if style.reverse:
                classes.append("bg-fgcolor")
        else:
            if bgcolor.is_system_defined:
                classes.append(f"bg-{COLOR_CLASSES[bgcolor.number]}")
            else:
                inlines.append(f"background-color: {bgcolor.get_truecolor().hex}")

        return cls(
            text,
            tuple(classes) if classes else None,
            tuple(inlines) if inlines else None,
        )

    def __len__(self):
        return len(self.text)

    def __getitem__(self, key: Union[int, slice]):
        return Span(
            self.text[key],
            self.classes,
            self.inlines,
        )

    @cached_property
    def markup(self) -> SafeString:
        safe_text = escape(self.text)

        if not self.classes and not self.inlines:
            return safe_text
        else:
            span = "<span"
            if self.classes:
                f_classes = " ".join(escape(class_) for class_ in self.classes)
                span += f' class="{f_classes}"'
            if self.inlines:
                f_styles = "; ".join(style.markup for style in self.inlines)
                span += f' style="{f_styles}"'
            span += ">"

            return mark_safe(f"{span}{safe_text}</span>")


@dataclass(frozen=True)
class SpanRow:
    spans: Tuple[Span]

    @classmethod
    @lru_cache
    def from_segments(cls, segments: Tuple[Segment]):
        spans = []
        for text, style, _ in segments:
            if style is None:
                spans.append(Span(text))
            else:
                spans.append(Span.from_style(text, style))

        return cls(tuple(spans))

    def __len__(self):
        return sum(len(span) for span in self.spans)

    def __getitem__(self, key: Union[int, slice]):
        if isinstance(key, int) or key.step:
            raise NotImplementedError()

        spans = []
        range_ = range(len(self))[key]
        span_start = 0
        for span in self.spans:
            span_end = span_start + len(span)
            if span_end > range_.start:
                local_start = (
                    0 if span_start >= range_.start else range_.start - span_start
                )
                local_stop = (
                    None if span_end <= range_.stop else len(range_) - local_start
                )
                if local_start is None and local_stop is None:
                    spans.append(span)
                else:
                    spans.append(span[local_start:local_stop])

            span_start = span_end
            if span_start > range_.stop:
                break

        return SpanRow(tuple(spans))

    @cached_property
    def markup(self) -> SafeString:
        return mark_safe("".join(span.markup for span in self.spans))
