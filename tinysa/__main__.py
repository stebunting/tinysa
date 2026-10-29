#!/opt/homebrew/share/man/man1/python3.1
"""Script to automatically collect RF scan data."""

from argparse import ArgumentParser
import scan
from tiny_sa import TinySA
from util import format_time

if __name__ == "__main__":
    parser = ArgumentParser(prog="tinysa", description="Automated RF Scanning")
    parser.add_argument("-i", "--inside", action="store_true")
    parser.add_argument("-o", "--outside", action="store_true")
    parser.add_argument("-y", action="store_false")
    args = parser.parse_args()

    file_prefix: str = "IN_" if args.inside else ("OUT_" if args.outside else "")

    running_time: float = 0

    tsa: TinySA = TinySA()

    if file_prefix == "":
        inside: str = "start"
        while inside.strip()[0] != "1" and inside.strip()[0] != "2":
            inside = input("1: Inside\n2: Outside\nIs this scan inside or outside? ")
            print("")
        file_prefix = "IN_" if inside == "1" else "OUT_"
    print(f"FILE PREFIX: \"{file_prefix}\"")

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

    running_time += scan.wifi("2400MHz", 2400, 2500, tsa)

    print("Scan Complete")
    print(f"Complete in {format_time(running_time)}")
