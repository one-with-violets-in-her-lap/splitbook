from dataclasses import dataclass
from typing import TypedDict, cast

from whisper import Whisper

from timecodes_generator.core.utils.datetime_formatting import (
    format_timestamp_from_seconds,
)


class Segment(TypedDict):
    id: int
    start: int
    end: int
    text: str


@dataclass
class Timecode:
    id: int
    start_seconds: int
    title: str

    def __str__(self):
        return f"{format_timestamp_from_seconds(self.start_seconds)} - {self.title}"


def generate_timecodes(whisper_model: Whisper, file_path: str) -> list[Timecode]:
    transcription_result = whisper_model.transcribe(file_path)
    segments = cast(list[Segment], transcription_result["segments"])

    return [
        Timecode(
            id=segment["id"],
            start_seconds=segment["start"],
            title=segment["text"],
        )
        for segment in segments
        if "Unit" in segment["text"]
    ]
