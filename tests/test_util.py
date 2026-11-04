"""Util testing"""

import unittest
from typing import TypedDict

import util

class TestOutput(unittest.TestCase):
    """Util testing"""

    def test_format_time(self):
        """format_time test cases."""

        test_case = TypedDict('test_case', {'input': float, 'expected_output': str})

        tests: list[test_case] = [{
            "input": 34.624,
            "expected_output": "00:35",
        }, {
            "input": 0.51,
            "expected_output": "00:01",
        }, {
            "input": 0.49999,
            "expected_output": "00:00",
        }, {
            "input": 945.0,
            "expected_output": "15:45",
        }, {
            "input": 3608.2347,
            "expected_output": "60:08",
        }, {
            "input": 3699,
            "expected_output": "61:39",
        }, {
            "input": -178,
            "expected_output": "00:00",
        }, {
            "input": 0,
            "expected_output": "00:00",
        }]

        for test in tests:
            output = util.format_time(test["input"])
            self.assertEqual(test["expected_output"], output)

    def test_mhz_to_hz(self):
        """mhz_to_hz test cases."""

        test_case = TypedDict('test_case', {'input': float, 'expected_output': int})

        tests: list[test_case] = [{
            "input": 606.253,
            "expected_output": 606253000
        }, {
            "input": 23,
            "expected_output": 23000000
        }, {
            "input": 2450,
            "expected_output": 2450000000
        }, {
            "input": 0.000001,
            "expected_output": 1
        }]

        for test in tests:
            output = util.mhz_to_hz(test["input"])
            self.assertEqual(test["expected_output"], output)

    def test_hz_to_mhz(self):
        """mhz_to_hz test cases."""

        test_case = TypedDict('test_case', {'input': int, 'expected_output': float})

        tests: list[test_case] = [{
            "input": 855025000,
            "expected_output": 855.025
        }, {
            "input": 4,
            "expected_output": 0.000004
        }, {
            "input": 2480000000,
            "expected_output": 2480
        }, {
            "input": 253738293,
            "expected_output": 253.738293
        }]

        for test in tests:
            output = util.hz_to_mhz(test["input"])
            self.assertEqual(test["expected_output"], output)
