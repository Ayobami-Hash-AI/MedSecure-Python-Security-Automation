import unittest
import sys
from pathlib import Path

# Allow tests to import our application
sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src")
)

from monitor import detect_brute_force


class TestBruteForceDetection(unittest.TestCase):

    def test_five_failures_within_60_seconds(self):

        logs = [
            f"2026-11-06 10:00:{i:02d} Failed password for admin from 192.168.1.10"
            for i in range(5)
        ]

        alerts = detect_brute_force(logs)

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["source_ip"], "192.168.1.10")

    def test_five_failures_over_ten_minutes(self):

        logs = [
            f"2026-11-06 10:{i:02d}:00 Failed password for admin from 192.168.1.10"
            for i in [0, 2, 4, 6, 10]
        ]

        alerts = detect_brute_force(logs)

        self.assertEqual(len(alerts), 0)

    def test_three_failures_within_60_seconds(self):

        logs = [
            f"2026-11-06 10:00:{i:02d} Failed password for admin from 192.168.1.10"
            for i in range(3)
        ]

        alerts = detect_brute_force(logs)

        self.assertEqual(len(alerts), 0)

    def test_successful_logins(self):

        logs = [
            f"2026-11-06 10:00:{i:02d} Accepted password for admin from 192.168.1.10"
            for i in range(5)
        ]

        alerts = detect_brute_force(logs)

        self.assertEqual(len(alerts), 0)

    def test_different_source_ips(self):

        logs = [
            f"2026-11-06 10:00:{i:02d} Failed password for admin from 192.168.1.{i + 10}"
            for i in range(5)
        ]

        alerts = detect_brute_force(logs)

        self.assertEqual(len(alerts), 0)


if __name__ == "__main__":
    unittest.main()