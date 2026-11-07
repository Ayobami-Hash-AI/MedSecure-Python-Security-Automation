import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"


def generate_incident_report(alerts, output_dir=REPORT_DIR):
    """
    Convert security alerts into structured JSON incident reports.

    Returns the paths of generated report files.
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    generated_reports = []

    for alert in alerts:

        incident_id = f"MED-{uuid4().hex[:12].upper()}"

        report = {
            "incident_id": incident_id,
            "incident_type": "Possible SSH Brute-Force Attack",
            "source_ip": alert["source_ip"],
            "failed_attempts": alert["failed_attempts"],
            "severity": alert["severity"],
            "first_seen": alert["first_seen"],
            "last_seen": alert["last_seen"],
            "status": "Requires Investigation",
            "detected_at": datetime.now(
                timezone.utc
            ).isoformat()
        }

        report_file = output_dir / f"{incident_id}.json"

        with open(report_file, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

        generated_reports.append(report_file)

    return generated_reports