INVALID_CHARS = '/<>:"/\\|?*'


def sanitize_filename(filename: str):
    return "".join(char if char not in INVALID_CHARS else "_" for char in filename)
