"""Script to automatically collect RF scan data."""

from argparse import ArgumentParser
from datetime import date
import signal
import sys
import logging

from tiny_sa import TinySA
import scan
import util

if __name__ == "__main__":
    def _signal_handler(_sig, _frame):
        """SIGINT Handler"""
        logging.info("Ctrl-C!")
        if tsa is not None:
            tsa.abort()
        sys.exit(0)

    signal.signal(signal.SIGINT, _signal_handler)

    today = date.today()
    logging.basicConfig(filename=f"log-{today.strftime("%Y%m%d")}.log", \
                        format="%(asctime)s %(levelname)s:%(message)s", \
                        datefmt="%Y-%m-%d %H:%M:%S", \
                        level=logging.INFO)
    logging.info("Script started")

    parser = ArgumentParser(prog="tinysa", description="Automated RF Scanning")
    parser.add_argument("-i", "--inside", action="store_true")
    parser.add_argument("-o", "--outside", action="store_true")
    parser.add_argument("-y", action="store_false")
    parser.add_argument("-p", "--prompt", action="store_false")
    args = parser.parse_args()

    file_prefix: str = "IN_" if args.inside else ("OUT_" if args.outside else "")
    prompt: bool = args.prompt

    running_time: float = 0

    tsa: TinySA | None = None
    QUIT: str = ""
    while tsa is None and QUIT.upper() != "X":
        try:
            tsa = TinySA()
        except OSError:
            QUIT = input("TinySA not plugged in. Press enter to retry or x to quit: ")
        if QUIT.upper() == "X":
            sys.exit(0)

    assert tsa is not None
    tsa.resume()

    if file_prefix == "":
        inside: str = "start"
        while len(inside) == 0 or (inside.strip()[0] != "1" and inside.strip()[0] != "2"):
            inside = input("1: Inside\n2: Outside\nIs this scan inside or outside? ")
            print()
        file_prefix = "IN_" if inside == "1" else "OUT_"
    print(f"FILE PREFIX: \"{file_prefix}\"")
    logging.info("File Prefix Set: %s", file_prefix)

    if args.y:
        input("Extend the antenna to maximum. Press enter to continue.\a")
    print("Scanning")

    running_time += scan.detailed(f"{file_prefix}14", 470, 890, tsa)
    running_time += scan.coarse(f"{file_prefix}02", 54, 88, tsa)
    running_time += scan.coarse(f"{file_prefix}07", 174, 216, tsa)
    running_time += scan.coarse(f"{file_prefix}FM", 80, 120, tsa)

    if args.y:
        input("Shorten the antenna to half. Press enter to continue.\a")
    running_time += scan.coarse(f"{file_prefix}900", 902, 928, tsa)
    running_time += scan.coarse(f"{file_prefix}X1", 944, 952, tsa)

    if args.y:
        input("Shorten the antenna to minimum. Press enter to continue.\a")
    running_time += scan.coarse(f"{file_prefix}DEUR", 1880, 1900, tsa)

    WIFI: str = ""
    while WIFI.upper() not in ("Y", "N"):
        WIFI = input("Would you like to capture a WiFi Scan (y/n): \a")
    if WIFI.upper() == "Y":
        running_time += scan.wifi("2400MHz", 2400, 2500, tsa)

    print("Scan Complete")
    print(f"Complete in {util.format_time(running_time)}")
    logging.info("Scan complete in %s", util.format_time(running_time))
