def format_timestamp_from_seconds(seconds: int):
    hours = seconds // 3600
    minutes_remainder = seconds % 3600
    seconds_remainder = minutes_remainder % 60

    return f"{hours:02.0f}:{minutes_remainder:02.0f}:{seconds_remainder:02.0f}"
