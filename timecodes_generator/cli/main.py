import logging
import re
from threading import Thread

import click
from dumb_whisper import Segment

from timecodes_generator.cli.transcribing_progress import CliTranscribingProgress
from timecodes_generator.core.export import EXPORTERS, ExportFormat
from timecodes_generator.core.generate_timecodes import generate_timecodes
from timecodes_generator.core.load import ModelName, load_whisper_model
from timecodes_generator.core.utils.datetime_formatting import (
    format_timestamp_from_seconds,
)
from timecodes_generator.core.utils.logging import configure_logging
from timecodes_generator.core.utils.regex import join_and_compile_regex_patterns

log_level_names_mapping = logging.getLevelNamesMapping()

export_format_click_type = click.Choice(
    [model_name_type.value for model_name_type in ExportFormat]
)


@click.command()
@click.argument("file-path", required=True)
@click.option(
    "--search",
    "-s",
    "search_patterns",
    required=True,
    multiple=True,
    help="Pattern in regular expression format to match word markers. "
    + "Example: Unit \\d (matches Unit {number}). "
    + "You can provide multiple patterns by using "
    + "this option multiple times (-s Pattern -s Pattern ...)",
)
@click.option("--log-level", type=click.Choice(log_level_names_mapping), default="INFO")
@click.option("--log-file-path", "--log", "-l", default=None, required=False)
@click.option(
    "--model",
    "-m",
    "model_name",
    type=click.Choice([model_name_type.value for model_name_type in ModelName]),
    default="small",
)
@click.option(
    "--export",
    "export_format",
    default=None,
    required=False,
    type=export_format_click_type,
    help="Export timecodes in one of the following formats:\n"
    + "- id3: Encode timecodes in a new MP3 file with chapters\n"
    + "- folder: Split original file in multiple files based on the timecodes",
)
@click.option("--verbose", "-v", "is_verbose", default=False)
def start_cli(
    file_path: str,
    search_patterns: list[str],
    log_level: str,
    log_file_path: str | None,
    model_name: str,
    export_format: str | None,
    is_verbose: bool,
):
    configure_logging(log_file_path, log_level_names_mapping[log_level])

    click.echo(
        click.style("\n- Loading a model - ", dim=True)
        + click.style(f"Whisper {model_name}\n", italic=True)
    )
    model = load_whisper_model(ModelName(model_name))

    progress = CliTranscribingProgress()
    cli_progress_showing_thread = Thread(target=progress.start_animations)
    cli_progress_showing_thread.start()

    def handle_progress_update(
        seconds_transcribed: float,
        total_seconds_duration: float,
        new_segment: Segment | None,
    ):
        progress.update_progress(
            new_segment.text if new_segment is not None else "",
            seconds_transcribed,
            total_seconds_duration,
        )

    timecodes = generate_timecodes(
        model,
        file_path,
        join_and_compile_regex_patterns(search_patterns, flags=re.IGNORECASE),
        is_verbose=None,  # Silences default Whisper output
        on_progress_update=handle_progress_update,
    )

    progress.stop_animations()

    click.secho("\n★ Timecodes:", bold=True)

    for timecode in timecodes:
        click.echo(
            click.style(format_timestamp_from_seconds(timecode.start_seconds))
            + " - "
            + timecode.title
        )

    if export_format is None:
        is_export_allowed = click.confirm(
            click.style("\n(?) ", dim=True) + "Would you like to save the timecodes?",
        )

        if is_export_allowed:
            export_format = click.prompt(
                click.style("\t(?) ", dim=True)
                + "In what format would you like to export?",
                type=export_format_click_type,
                show_choices=True,
            )

    if export_format is not None:
        exporter = EXPORTERS[ExportFormat(export_format)]
        export_result_path = exporter(file_path, timecodes, is_verbose)

        click.secho(f"\n✓ Saved at {export_result_path}", fg="green")


if __name__ == "__main__":
    start_cli()
