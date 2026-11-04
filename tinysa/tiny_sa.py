"""Module to represent a TinySA connection."""

import struct
import logging
from serial.tools import list_ports
import serial
import numpy as np
from PIL import Image

class TinySA:
    """Class to represent a TinySA connection."""
    VID: int = 0x0483 #1155
    PID: int = 0x5740 #22336

    def __init__(self, dev = None):
        self.dev = dev or self.getport()
        self.serial: serial.Serial | None = None
        logging.info("Got connection %s", self.dev)

    def getport(self) -> str:
        """Gets the TinySA port automatically."""
        device_list = list_ports.comports()
        for device in device_list:
            if device.vid == self.VID and device.pid == self.PID:
                return device.device
        raise OSError("device not found")

    def open(self) -> None:
        """Opens a connection to the device."""
        if self.serial is None:
            self.serial = serial.Serial(self.dev)
            logging.info("Opened serial connection %s", self.serial)

    def close(self) -> None:
        """Closes the connection to the device."""
        if self.serial:
            self.serial.close()
            logging.info("Closed serial connection")
        self.serial = None

    def send_command(self, cmd: str) -> None:
        """Sends a command to the device."""
        self.open()
        if self.serial:
            self.serial.write(cmd.encode())
            self.serial.readline()
            logging.info("Command sent to TinySA: %s", cmd.encode())

    def resume(self) -> None:
        """Resumes the device."""
        self.send_command("resume\r")
        logging.info("Device resumed")

    def pause(self) -> None:
        """Pauses the device."""
        self.send_command("pause\r")
        logging.info("Device paused")

    def rbw(self, data = 0) -> None:
        """Sends a command to the device to set the RBW."""
        if data == 0:
            self.send_command("rbw auto\r")
        else:
            self.send_command(f"rbw {data}\r")

    def send_scan(self, start: int, stop: int, points: int | None = None) -> None:
        """Sends a scan command to the device."""
        if points:
            self.send_command(f"scan {start} {stop} {points}\r")
        else:
            self.send_command(f"scan {start} {stop}\r")

    def scan(self, f1: int, f2: int, points: int) -> list[str]:
        """Starts a scan and returns data."""
        self.send_scan(f1, f2, points)
        return self.data()

    def fetch_data(self) -> str:
        """Fetches raw data from the device."""
        logging.info("Fetching data")
        result: str = ""
        line: str = ""
        i: int = 1
        raw_data: str = ""
        while self.serial:
            c = self.serial.read().decode("utf-8")
            raw_data += c
            if c != chr(13):
                line += c
                if c == chr(10):
                    result += line
                    line = ""
                elif line.endswith("ch>"):
                    break
            i += 1
        logging.info("Data fetched (%d characters, %d lines): '%s'", \
                     i, len(result.split("\n")), raw_data.replace("\n", "\\n").replace("\r", "\\r"))
        return result

    def data(self, array: int = 2) -> list[str]:
        """Fetches data from the device."""
        self.send_command(f"data {array}\r")
        data = self.fetch_data()
        return list(filter(lambda x : x != "", data.split('\n')))

    def fetch_frequencies(self) -> list[int]:
        """Fetches frequencies from the device."""
        frequencies = []
        self.send_command("frequencies\r")
        data = self.fetch_data()
        for line in data.split('\n'):
            if line:
                frequencies.append(float(line))
        return frequencies

    def capture(self):
        """Captures a screenshot of the device."""
        self.send_command("capture\r")
        if self.serial:
            b = self.serial.read(480 * 320 * 2)
            x = struct.unpack(">153600H", b)
            arr = np.array(x, dtype=np.uint32)
            arr = 0xFF000000 + ((arr & 0xF800) >> 8) + \
                  ((arr & 0x07E0) << 5) + ((arr & 0x001F) << 19)
            return Image.frombuffer('RGBA', (480, 320), arr, 'raw', 'RGBA', 0, 1)
        return None
