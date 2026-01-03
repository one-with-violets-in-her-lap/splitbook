import click
from splitbook.cli.utils.formatting.formatting import format_text_in_columns


def test_format_text_in_columns():
    assert (
        format_text_in_columns({"width": 10, "text": "hello\nworld"})
        == """
hello     
world     
""".strip("\n")
    )

    assert (
        format_text_in_columns(
            {"width": 14, "text": "col1_line1\ncol1_line2"},
            {"width": 15, "text": "col2_line1\ncol2_line2"},
        )
        == """
col1_line1    col2_line1     
col1_line2    col2_line2     
""".strip("\n")
    ), (
        "Spacing must be 14 characters for first column and 15 characters for second column"
    )

    assert (
        format_text_in_columns(
            {"width": 12, "text": "col1_line1\ncol1_line2\ncol1_line3"},
            {"width": 12, "text": "col2_line1"},
        )
        == """
col1_line1  col2_line1  
col1_line2              
col1_line3              
""".strip("\n")
    ), "Must align columns with less amount of lines to the top"

    assert format_text_in_columns() == "", (
        "Must return an empty string if no columns are passed"
    )

    assert (
        format_text_in_columns(
            {"width": 12, "text": "col1_line1\ncol1_line2\ncol1_line3"},
            {"width": 12, "text": "\ncol2_line1"},
        )
        == """
col1_line1              
col1_line2  col2_line1  
col1_line3              
""".strip("\n")
    ), "Must allow empty lines for custom column alignment"
