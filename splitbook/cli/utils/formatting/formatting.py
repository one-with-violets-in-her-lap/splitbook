import logging
from typing import TypedDict

import click


class CliPrintColumn(TypedDict):
    width: int
    text: str


_logger = logging.getLogger(__name__)


def format_text_in_columns(*columns: CliPrintColumn):
    result = ""

    if len(columns) == 0:
        return result

    column_line_counts = [column["text"].count("\n") + 1 for column in columns]

    max_line_count = max(column_line_counts)

    for line_index in range(max_line_count):
        line = ""

        for column_index, column in enumerate(columns):
            column_width = column["width"]

            if line_index >= column_line_counts[column_index]:
                line += " " * column_width
                continue

            column_line = column["text"].splitlines()[line_index]

            line += pad_string_left(
                column_line, column_width, ignore_control_characters=True
            )

        result += line

        if line_index + 1 < max_line_count:
            result += "\n"

    return result


def pad_string_left(
    string: str, new_length: int, ignore_control_characters=False, pad_character=" "
):
    string_length = (
        len(click.unstyle(string)) if ignore_control_characters else len(string)
    )

    pad_amount = new_length - string_length

    if pad_amount <= 0:
        return string

    return string + pad_character * pad_amount
