"""Module for scanning functions"""

import time
from file_util import File
from tiny_sa import TinySA
from util import format_time, hz_to_mhz, mhz_to_hz

type Data = list[tuple[int, float | None]]

def _section(f1: int, f2: int, points: int, averages: int, device: TinySA) -> Data:
    """Function to perform multiple scans and average data."""
    func_start_time: float = time.time()

    device.rbw(30)
    device.send_command("calc off\r")
    device.resume()

    print(f"{hz_to_mhz(f1):.3f}MHz - {hz_to_mhz(f2):.3f}MHz", end="", flush=True)

    raw_data: list[list[float]] = [[] for _ in range(points)]
    for _ in range(averages):
        lines = device.scan(f1, f2, points)
        for i in range(points):
            try:
                raw_data[i].append(float(lines[i]))
            except ValueError:
                # Level data is not valid float
                pass
        print(".", end="", flush=True)

    frequencies: list[int] = device.fetch_frequencies()
    levels: list[float] = [sum(raw_data[i]) / len(raw_data[i]) for i in range(len(raw_data))]

    print(f"OK ({format_time(time.time() - func_start_time)})")
    return [(frequencies[i], levels[i]) for i in range(points)]

def detailed(filename: str, f1_mhz: int, f2_mhz: int, device: TinySA) -> float:
    """Function to divide a scan into multiple scans and combine them into a file"""
    func_start_time: float = time.time()

    fp: File = File(filename)

    f1: int = mhz_to_hz(f1_mhz)
    f2: int = mhz_to_hz(f2_mhz)

    step: int = 25000
    max_points: int = 450

    i: int = 0
    end: int = 0
    while end < f2:
        start: int = f1 + i * (step * max_points)
        end = f2 if (start + (step * (max_points - 1))) > f2 else start + (step * (max_points - 1))
        points: int = int((end - start) / step) + 1
        fp.append(_section(start, end, points, 6, device))
        i += 1

    t: float = time.time() - func_start_time
    print(f"{fp.filename()} written. Complete in {format_time(t)}")
    return t

def coarse(filename: str, f1_mhz: int, f2_mhz: int, device: TinySA) -> float:
    """Method to take a single scan between 2 frequencies"""
    func_start_time: float = time.time()

    f1: int = mhz_to_hz(f1_mhz)
    f2: int = mhz_to_hz(f2_mhz)

    fp = File(filename)
    fp.write(_section(f1, f2, 450, 6, device))

    t: float = time.time() - func_start_time
    print(f"{fp.filename()} written. Complete in {format_time(t)}")
    return t

def wifi(filename: str, f1_mhz: int, f2_mhz: int, device: TinySA) -> float:
    """Method to take a WiFi scan and capture to an image file"""
    func_start_time: float = time.time()

    f1: int = mhz_to_hz(f1_mhz)
    f2: int = mhz_to_hz(f2_mhz)
    averages: int  = 4

    print(f"{hz_to_mhz(f1):.3f}MHz - {hz_to_mhz(f2):.3f}MHz", end="", flush=True)

    device.send_command(f"sweep start {f1}\r")
    device.send_command(f"sweep stop {f2}\r")
    device.send_command("calc maxh\r")
    device.resume()

    for _ in range(averages):
        time.sleep(21.5)
        print(".", end="", flush=True)

    img = device.capture()
    if img is not None:
        jpg = img.convert('RGB')
        jpg.save(f"{filename}.jpg")

    t: float = time.time() - func_start_time
    print(f"OK ({format_time(t)})")
    print(f"{filename}.jpg written. Complete in {format_time(t)}")
    return t
