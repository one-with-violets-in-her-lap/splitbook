import logging
import subprocess

_logger = logging.getLogger(__name__)


def get_base_ffmpeg_flags(is_verbose: bool) -> list[str]:
    flags = ["-y"]

    if not is_verbose:
        flags.extend(["-hide_banner", "-nostats", "-loglevel", "error"])

    return flags


def save_audio_file_part(
    input_path: str,
    output_path: str,
    start_seconds: float,
    end_seconds: float | None = None,
    is_verbose=True,
):
    ffmpeg_command = [
        "ffmpeg",
        *get_base_ffmpeg_flags(is_verbose),
        "-ss",
        str(start_seconds),
        "-i",
        input_path,
    ]

    if end_seconds is not None:
        part_duration = end_seconds - start_seconds

        ffmpeg_command.extend(
            [
                "-t",
                str(part_duration),
            ]
        )

    ffmpeg_command.extend(
        [
            "-acodec",
            "copy",
            output_path,
        ]
    )

    _logger.debug("Running %s", " ".join(ffmpeg_command))

    completed_process = subprocess.run(ffmpeg_command, check=True)
    completed_process.check_returncode()


def convert_audio_file(input_path: str, output_path: str, is_verbose=True):
    ffmpeg_command = [
        "ffmpeg",
        *get_base_ffmpeg_flags(is_verbose),
        "-i",
        input_path,
        output_path,
    ]

    completed_process = subprocess.run(ffmpeg_command)
    completed_process.check_returncode()
