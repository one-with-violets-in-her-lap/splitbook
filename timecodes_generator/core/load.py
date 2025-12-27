from enum import Enum

import whisperx
import whisperx.asr


class ModelName(Enum):
    TINY = "tiny"
    TINY_EN = "tiny.en"
    BASE = "base"
    BASE_EN = "base.en"
    SMALL = "small"
    SMALL_EN = "small.en"
    MEDIUM = "medium"
    MEDIUM_EN = "medium.en"
    LARGE = "large"
    TURBO = "turbo"


def load_whisper_model(model_name: ModelName) -> whisperx.asr.FasterWhisperPipeline:
    return whisperx.load_model(model_name.value, compute_type="float16", device="cuda")
