import os

from pydub import AudioSegment

from timecodes_generator.core.generate_timecodes import Timecode
from timecodes_generator.core.utils.errors import AudioProcessingError
from timecodes_generator.core.utils.sanitize_filename import sanitize_filename


def export_timecodes_as_folder(source_file_path: str, timecodes: list[Timecode]):
    file_path_without_extension, extension = os.path.splitext(source_file_path)
    folder_path = file_path_without_extension + " (split in chapters)"

    os.makedirs(folder_path, exist_ok=True)

    audio_segment: AudioSegment = AudioSegment.from_file(source_file_path)

    for index, timecode in enumerate(timecodes):
        end_time_milliseconds = (
            timecodes[index + 1].start_seconds * 1000
            if index + 1 < len(timecodes)
            else len(audio_segment)
        )

        audio_part_segment = audio_segment[
            timecode.start_seconds * 1000 : end_time_milliseconds
        ]

        if not isinstance(audio_part_segment, AudioSegment):
            raise AudioProcessingError(
                "Failed to split audio file. Segment slicing result is not an instance of AudioSegment"
            )

        filename = sanitize_filename(f"{timecode.title} ({timecode.id}){extension}")

        audio_part_segment.export(
            os.path.join(folder_path, filename),
            format=extension.lstrip("."),
        )

    return folder_path
