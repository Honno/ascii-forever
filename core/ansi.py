from functools import lru_cache
from html import escape

from django.utils.safestring import SafeString
from django.utils.safestring import mark_safe
from rich.ansi import AnsiDecoder
from rich.console import Console
from rich.segment import Segment
from rich.style import Style
from rich.text import Text

__all__ = ["ansi2html"]


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


decoder = AnsiDecoder()
mock_console = Console(
    color_system="truecolor",
    force_terminal=True,
    width=float("inf"),
    tab_size=8,
)


@lru_cache()
def style2span(style: Style):
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
            inlines.append(f"text-shadow: -0.25px 0 {color_hex}, -0.25px 0 {color_hex}")
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

    span = "<span"
    if classes:
        f_classes = " ".join(classes)
        span += f' class="{f_classes}"'
    if inlines:
        f_inlines = "; ".join(inlines)
        span += ' style="{f_inlines}"'
    span += ">"

    return span


def ansi2html(art: str) -> SafeString:
    html_lines = []
    text_lines = decoder.decode(art)
    for text_line in text_lines:
        html_line = ""
        for text, style, _ in text_line.render(mock_console):
            html_segment = escape(text)
            if style:
                span = style2span(style)
                html_segment = f"{span}{html_segment}</span>"

            html_line += html_segment

        html_lines.append(html_line)

    html = "\n".join(html_lines)

    return mark_safe(html)
