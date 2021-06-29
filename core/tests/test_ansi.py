from pytest import mark

from core.ansi import ansi2html

from .multiline import multiline_assert

examples = {
    "plain": ("hello", "hello"),
    "red": ("\u001b[31mred", '<span class="red">red</span>'),
    "reverse_bold": (
        "\u001b[0m\u001b[1;7mreverse-bold",
        '<span class="bgcolor -bold bg-fgcolor">reverse-bold</span>',
    ),
}


@mark.parametrize("ansi, html", examples.values(), ids=examples.keys())
def test_render(ansi, html):
    assert ansi2html(ansi) == html
