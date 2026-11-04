"""Utility Functions."""

import sys
from enum import Enum

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

class Colour(Enum):
    """Enum to define colours"""
    GREEN = 1
    RED = 2

def print_coloured(colour: Colour, text: str) -> None:
    """Function to colour text to stdout"""
    if sys.platform.startswith("win"):
        sys.stdout.write(text)
        return

    prefix: str = ""
    if colour == Colour.GREEN:
        prefix = "\033[1;32m"
    elif colour == Colour.RED:
        prefix = "\033[1;31m"
    sys.stdout.write(f"{prefix}{text}\033[0;0m")
