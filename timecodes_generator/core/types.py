from dataclasses import dataclass

from timecodes_generator.core.utils.datetime_formatting.datetime_formatting import (
    format_timestamp_from_seconds,
)


@dataclass
class Timecode:
    id: int
    start_seconds: float
    end_seconds: float
    title: str

    def __str__(self):
        return f"{format_timestamp_from_seconds(self.start_seconds)} - {self.title}"
