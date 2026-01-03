from enum import Enum
from typing import Callable

from splitbook.core.export.folder import export_timecodes_as_folder
from splitbook.core.export.id3_tagged_file import export_tagged_audio_file
from splitbook.core.types import Timecode


class ExportFormat(Enum):
    ID3_TAGGED_FILE = "id3"
    FOLDER = "folder"


EXPORTERS: dict[ExportFormat, Callable[[str, list[Timecode], bool], str]] = {
    ExportFormat.ID3_TAGGED_FILE: export_tagged_audio_file,
    ExportFormat.FOLDER: export_timecodes_as_folder,
}
