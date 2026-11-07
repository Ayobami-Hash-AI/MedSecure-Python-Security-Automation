import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src")
)

from reporter import generate_incident_report


class TestIncidentReporting(unittest.TestCase):

    def setUp(self):
        self.alert = {
            "source_ip": "192.168.1.10",
            "failed_attempts": 5,
            "severity": "HIGH",
            "first_seen": "2026-11-06T10:01:12",
            "last_seen": "2026-11-06T10:01:20"
        }

        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

    def test_report_file_created(self):
        reports = generate_incident_report(
            [self.alert],
            output_dir=self.temp_dir.name
        )

        self.assertEqual(len(reports), 1)
        self.assertTrue(reports[0].exists())

    def test_report_contains_correct_information(self):
        reports = generate_incident_report(
            [self.alert],
            output_dir=self.temp_dir.name
        )

        with open(reports[0], encoding="utf-8") as file:
            report = json.load(file)

        self.assertEqual(report["source_ip"], "192.168.1.10")
        self.assertEqual(report["failed_attempts"], 5)
        self.assertEqual(report["severity"], "HIGH")
        self.assertEqual(report["status"], "Requires Investigation")
        self.assertIn("incident_id", report)
        self.assertIn("detected_at", report)

    def test_no_alerts_no_reports(self):
        reports = generate_incident_report(
            [],
            output_dir=self.temp_dir.name
        )

        self.assertEqual(len(reports), 0)
        self.assertEqual(
            list(Path(self.temp_dir.name).glob("*.json")),
            []
        )

    def test_multiple_alerts_generate_multiple_reports(self):
        second_alert = {
            **self.alert,
            "source_ip": "192.168.1.20"
        }

        reports = generate_incident_report(
            [self.alert, second_alert],
            output_dir=self.temp_dir.name
        )

        self.assertEqual(len(reports), 2)
        self.assertNotEqual(reports[0], reports[1])


if __name__ == "__main__":
    unittest.main()