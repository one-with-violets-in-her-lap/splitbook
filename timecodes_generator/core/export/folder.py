import os

from timecodes_generator.core.types import Timecode
from timecodes_generator.core.utils.audio import save_audio_file_part
from timecodes_generator.core.utils.sanitize_filename import sanitize_filename


def export_timecodes_as_folder(
    source_file_path: str, timecodes: list[Timecode], is_verbose=True
):
    file_path_without_extension, extension = os.path.splitext(source_file_path)
    folder_path = file_path_without_extension + " (split in chapters)"

    os.makedirs(folder_path, exist_ok=True)

    for index, timecode in enumerate(timecodes):
        end_time_seconds = (
            timecodes[index + 1].start_seconds if index + 1 < len(timecodes) else None
        )

        filename = sanitize_filename(f"{timecode.title} ({timecode.id}){extension}")

        save_audio_file_part(
            source_file_path,
            os.path.join(folder_path, filename),
            timecode.start_seconds,
            end_time_seconds,
            is_verbose=is_verbose,
        )

    return folder_path
