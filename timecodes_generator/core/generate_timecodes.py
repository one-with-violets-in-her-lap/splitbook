import logging
import re
from dataclasses import dataclass
from re import Pattern
from typing import TypedDict, cast

from whisper import Whisper

from timecodes_generator.core.utils.datetime_formatting import (
    format_timestamp_from_seconds,
)

_logger = logging.getLogger(__name__)


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


SEGMENT_GROUP_SIZE = 3


def find_segment_by_string_position(segment_group: list[Segment], position: int):
    text_end = 0

    for segment in segment_group:
        text_start = text_end - 1
        text_end = text_end + len(segment["text"])

        if position > text_start and position < text_end:
            print("\n")
            return segment


def extract_timecodes(segments: list[Segment], search_patterns: list[Pattern]):
    timecodes: list[Timecode] = []

    segment_start_index = 0

    while segment_start_index < len(segments):
        starting_segment = segments[segment_start_index]

        segment_group = segments[
            segment_start_index : segment_start_index + SEGMENT_GROUP_SIZE
        ]

        text = "".join([segment["text"] for segment in segment_group])

        _logger.debug("Merged segments: %s", text)

        any_pattern_match: re.Match | None = None

        for pattern in search_patterns:
            current_pattern_match = pattern.search(text)
            if current_pattern_match is not None and any_pattern_match is None:
                any_pattern_match = current_pattern_match

            if current_pattern_match is not None:
                _logger.info("Match: %s", current_pattern_match.group())

                segment_with_occurrence = find_segment_by_string_position(
                    segment_group, current_pattern_match.start()
                )

                if segment_with_occurrence is None:
                    _logger.warning(
                        "Failed to find segment by string position. Falling back to a starting segment"
                    )
                    segment_with_occurrence = starting_segment

                timecodes.append(
                    Timecode(
                        id=segment_with_occurrence["id"],
                        start_seconds=segment_with_occurrence["start"],
                        title=current_pattern_match.group(),
                    )
                )

        if any_pattern_match is not None:
            segment_start_index = segment_start_index + SEGMENT_GROUP_SIZE
        else:
            segment_start_index = segment_start_index + 1

    return timecodes


def generate_timecodes(
    whisper_model: Whisper, file_path: str, search_patterns: list[Pattern]
) -> list[Timecode]:
    transcription_result = whisper_model.transcribe(file_path)
    segments = cast(list[Segment], transcription_result["segments"])

    _logger.debug("Segments: %s", segments)

    return extract_timecodes(segments, search_patterns)
