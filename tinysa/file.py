"""Module to deal with file operations."""

import os
from datetime import date

import util

type Data = list[tuple[int, float | None]]

class File:
    """Class to deal with file operations."""

    BASE_DIRECTORY: str = "scans"

    def __init__(self, filename: str):
        today = date.today()
        self._filename: str = f"{filename}.csv" if os.path.splitext(filename)[1] == "" else filename
        self._directory: str = f"{self.BASE_DIRECTORY}-{today.strftime("%Y%m%d")}"
        self._path: str = os.path.join(self._directory, self._filename)

        if not os.path.exists(self._directory):
            os.mkdir(self._directory)

        if os.path.splitext(self._filename)[1] == ".csv":
            with open(self._path, "w", encoding="utf-8"):
                pass

    def append(self, data: Data) -> None:
        """Method to append to a scan csv file"""
        with open(self._path, "a", encoding="utf-8") as fp:
            for _, (freq, level) in enumerate(data):
                print(f"{util.hz_to_mhz(freq):.3f};{level:2.2f}", file=fp)

    def write(self, data: Data) -> None:
        """Method to write a scan csv file"""
        with open(self._path, "w", encoding="utf-8") as fp:
            for _, (freq, level) in enumerate(data):
                print(f"{util.hz_to_mhz(freq):.3f};{level:2.2f}", file=fp)

    def image_dump(self, img) -> None:
        """Method to dump an image file"""
        img.save(self._path)

    def filename(self) -> str:
        """Method to return the filename"""
        return self._filename
