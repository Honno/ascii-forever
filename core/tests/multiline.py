from itertools import zip_longest

__all__ = ["multiline", "multiline_assert"]


class multiline(str):
    def __new__(cls, string):
        start = 0 if string[0] != "\n" else 1
        end = None if string[-1] != "\n" else -1
        string = string[start:end]

        return super().__new__(cls, string)


def multiline_assert(str1, str2):
    x = 0
    y = 0
    for char1, char2 in zip_longest(str1, str2):
        if char1 != char2:
            f_char1 = repr(char1)
            f_char2 = repr(char2)

            f_line1 = repr(str1.splitlines()[y])
            f_line2 = repr(str2.splitlines()[y])

            raise AssertionError(
                f"L{y} C{x}: {f_char1} != {f_char2}\n"
                f"i.e. {f_line1} !=\n"
                f"     {f_line2}"
            )

        if char1 == char2 != "\n":
            x += 1
        else:
            x = 0
            y += 1
