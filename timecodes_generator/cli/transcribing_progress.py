import logging
import shutil
import time

import click

from timecodes_generator.cli.utils.formatting.formatting import format_text_in_columns
from timecodes_generator.cli.waveform_animation import CliWaveformAnimation

CLEAR_LINE_CODE = "\033[A                             \033[A"

STATUS_TEXT = "Transcribing ...."
STATUS_TEXT_COLUMN_WIDTH = 64

WAVEFORM_COLUMN_WIDTH = 20

TYPING_ANIMATION_DURATION_SECONDS = 2.4

TRANSCRIPTION_PREVIEW_UPDATE_RATE_SECONDS = 0.3
TRANSCRIPTION_PREVIEW_COLUMN_WIDTH = 64
TRANSCRIPTION_CAROUSEL_SPEED = 2
TRANSCRIPTION_CAROUSEL_WIDTH = 50

_logger = logging.getLogger(__name__)

terminal_width = shutil.get_terminal_size()[0]


class CliTranscribingProgress:
    def __init__(self):
        self.transcription_text: str | None = None
        self.seconds_transcribed: float | None = None
        self.total_seconds_duration: float | None = None

        self.waveform_animation = CliWaveformAnimation()

        self._is_typing_animation_stopped = False
        self._transcription_preview_animation = {
            "is_stopped": True,
            "carousel_width": min(TRANSCRIPTION_CAROUSEL_WIDTH, terminal_width),
            "carousel_offset": 0,
        }

    def _build_status_text(self):
        status_text = STATUS_TEXT

        if (
            self.seconds_transcribed is not None
            and self.total_seconds_duration is not None
        ):
            status_text += f"     ({self.seconds_transcribed:.0f}/{self.total_seconds_duration:.0f})"

        return status_text

    def _clear_lines(self):
        for _ in range(self.waveform_animation.line_count):
            click.echo(CLEAR_LINE_CODE)

    def _play_typing_animation(self):
        current_text = ""
        typing_rate = TYPING_ANIMATION_DURATION_SECONDS / len(STATUS_TEXT)

        for character_index, character in enumerate(STATUS_TEXT):
            if character_index > 0:
                self._clear_lines()

            if self._is_typing_animation_stopped:
                current_text = STATUS_TEXT
            else:
                current_text += character

            click.echo(
                format_text_in_columns(
                    {"width": STATUS_TEXT_COLUMN_WIDTH, "text": "\n\n" + current_text},
                    {
                        "width": WAVEFORM_COLUMN_WIDTH,
                        "text": self.waveform_animation.get_current_frame_and_update(),
                    },
                )
            )

            if self._is_typing_animation_stopped:
                break
            else:
                time.sleep(typing_rate)

        self._is_typing_animation_stopped = True

        click.echo()

    def _update_transcription_preview_animation(self):
        if (
            self.transcription_text is None
            or self._transcription_preview_animation["is_stopped"]
        ):
            return

        self._clear_lines()

        text_end = (
            self._transcription_preview_animation["carousel_offset"]
            + self._transcription_preview_animation["carousel_width"]
        )

        transcription_preview = click.style(
            "   "
            + self.transcription_text[
                self._transcription_preview_animation["carousel_offset"] : text_end
            ],
            dim=True,
        )

        click.echo(
            format_text_in_columns(
                {
                    "width": TRANSCRIPTION_PREVIEW_COLUMN_WIDTH,
                    "text": "\n" + self._build_status_text() + "\n" + transcription_preview,
                },
                {
                    "width": WAVEFORM_COLUMN_WIDTH,
                    "text": self.waveform_animation.get_current_frame_and_update(),
                },
            )
        )

        # If more text is available, moves the carousel
        if len(self.transcription_text) > text_end:
            self._transcription_preview_animation["carousel_offset"] += (
                TRANSCRIPTION_CAROUSEL_SPEED
            )

    def _play_transcription_preview_animation(self):
        self._transcription_preview_animation["is_stopped"] = False

        while not self._transcription_preview_animation["is_stopped"]:
            self._update_transcription_preview_animation()
            time.sleep(TRANSCRIPTION_PREVIEW_UPDATE_RATE_SECONDS)

    def start_animations(self):
        self._play_typing_animation()
        self._play_transcription_preview_animation()

    def update_progress(
        self,
        append_transcription: str,
        seconds_transcribed: float,
        total_seconds_duration: float,
    ):
        if self.transcription_text is None:
            self.transcription_text = append_transcription
        else:
            self.transcription_text += append_transcription

        self.seconds_transcribed = seconds_transcribed
        self.total_seconds_duration = total_seconds_duration

        self._update_transcription_preview_animation()

    def stop_animations(self):
        self._is_typing_animation_stopped = True
        self._transcription_preview_animation["is_stopped"] = True
