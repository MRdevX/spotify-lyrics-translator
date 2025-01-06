"""Time conversion utilities."""

def ms_to_min_sec(ms: int) -> str:
    """Convert milliseconds to MM:SS format."""
    try:
        # Ensure ms is an integer
        ms = int(ms) if isinstance(ms, str) else ms
        minutes = ms // 60000
        seconds = (ms % 60000) // 1000
        return f"{minutes}:{seconds:02d}"
    except (ValueError, TypeError):
        return "0:00"

def time_str_to_ms(time_str: str) -> int:
    """Convert MM:SS format to milliseconds."""
    try:
        minutes, seconds = map(int, time_str.split(":"))
        return minutes * 60000 + seconds * 1000
    except (ValueError, TypeError):
        return 0 