"""Utility Functions."""

def format_time(t: float) -> str:
    """Format a time in seconds to MM:SS"""
    seconds: float = 0 if t < 0 else t
    minutes: int = 0
    while seconds > 60:
        minutes += 1
        seconds -= 60
    return f"{minutes:02d}:{seconds:02.0f}"

def hz_to_mhz(x: int) -> float:
    """Function to convert a frequency in Hz in MHz"""
    return x / 1000000

def mhz_to_hz(x: int) -> int:
    """Function to convert a frequency in MHz to Hz"""
    return x * 1000000
