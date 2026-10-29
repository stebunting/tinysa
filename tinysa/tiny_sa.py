"""Module to represent a TinySA connection."""

import struct
from serial.tools import list_ports
import serial
import numpy as np
from PIL import Image

class TinySA:
    """Class to represent a TinySA connection."""
    VID = 0x0483 #1155
    PID = 0x5740 #22336

    def __init__(self, dev = None):
        self.dev = dev or self.getport()
        self.serial: serial.Serial | None = None

    def getport(self) -> str:
        """Gets the TinySA port automatically."""
        device_list = list_ports.comports()
        for device in device_list:
            if device.vid == self.VID and device.pid == self.PID:
                return device.device
        raise OSError("device not found")

    def open(self):
        """Opens a connection to the device."""
        if self.serial is None:
            self.serial = serial.Serial(self.dev)

    def close(self):
        """Closes the connection to the device."""
        if self.serial:
            self.serial.close()
        self.serial = None

    def send_command(self, cmd: str):
        """Sends a command to the device."""
        self.open()
        if self.serial:
            self.serial.write(cmd.encode())
            self.serial.readline()

    def cmd(self, text: str):
        """Sends a command to the device and returns data."""
        self.open()
        if self.serial:
            self.serial.write((text + "\r").encode())
            self.serial.readline()
            data = self.fetch_data()
            return data
        return None

    def rbw(self, data = 0):
        """Sends a command to the device to set the RBW."""
        if data == 0:
            self.send_command("rbw auto\r")
        else:
            self.send_command(f"rbw {data}\r")

    def fetch_data(self):
        """Fetches raw data from the device."""
        result = ""
        line = ""
        while self.serial:
            c = self.serial.read().decode("utf-8")
            if c != chr(13):
                line += c
                if c == chr(10):
                    result += line
                    line = ""
                elif line.endswith("ch>"):
                    break
        return result

    def resume(self):
        """Resumes the device."""
        self.send_command("resume\r")

    def pause(self):
        """Pauses the device."""
        self.send_command("pause\r")

    def data(self, array: int = 2):
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

    def send_scan(self, start: int, stop: int, points: int | None = None):
        """Sends a scan command to the device."""
        if points:
            self.send_command(f"scan {start} {stop} {points}\r")
        else:
            self.send_command(f"scan {start} {stop}\r")

    def scan(self, f1: int, f2: int, points: int):
        """Starts a scan and returns data."""
        self.send_scan(f1, f2, points)
        return self.data()

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
