import re

import whisperx.asr

from timecodes_generator.core.generate_timecodes import extract_timecodes
from timecodes_generator.core.utils.regex import join_and_compile_regex_patterns

TEST_TIMECODE_SEARCH_PATTERN = join_and_compile_regex_patterns(
    [
        r"(?:Unit \d+.?)? Activity [a-zA-Z].+?(?=\.|$)",  # Unit {number}. Activity {letter}. {...remaining sentence}
        r"(?:Unit \d+.?)? Practice \d.+?(?=\.|$)",  # Unit {number}. Practice {number}. {...remaining sentence}
        r"Unit \d+.? (?![^.]*\bActivity|Practice\b)[^.]*(\.|$)",  # Unit {number}. {...remaining sentence}
    ],
    flags=re.IGNORECASE,
)

TEST_TRANSCRIPTION_SEGMENTS: list[whisperx.asr.SingleSegment] = [
    {
        "start": 0,
        "end": 5,
        "text": ' Welcome to the "Learn English" book. The book contains grammar info,',
    },
    {
        "start": 6,
        "end": 12,
        "text": " exercises and optional audition practice. Unit 1. Basic words.",
    },
    {
        "start": 14,
        "end": 20,
        "text": " Placeholder text. Placeholder text, placeholder text, placeholder text.",
    },
    {
        "start": 21,
        "end": 26,
        "text": " Unit 1. Activity A. Greetings. Placeholder text, placeholder text, placeholder text, placeholder text.",
    },
    {
        "start": 28,
        "end": 36,
        "text": " Unit 1, practice 1. Responding. Placeholder text, placeholder text,",
    },
    {
        "start": 36,
        "end": 47,
        "text": " placeholder text. Unit 2, Verbs. Placeholder text, placeholder text. Placeholder text.",
    },
]


def test_generate_timecodes():
    timecodes = extract_timecodes(
        TEST_TRANSCRIPTION_SEGMENTS, TEST_TIMECODE_SEARCH_PATTERN
    )

    assert timecodes[0].start_seconds == 6
    assert timecodes[0].title == "Unit 1. Basic words."

    assert timecodes[1].start_seconds == 21
    assert timecodes[1].title == "Unit 1. Activity A. Greetings"

    assert timecodes[2].start_seconds == 28
    assert timecodes[2].title == "Unit 1, practice 1. Responding"

    assert timecodes[3].start_seconds == 36
    assert timecodes[3].title == "Unit 2, Verbs."
