from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
import ipaddress
import re

# Detection configuration
THRESHOLD = 5
TIME_WINDOW = 60

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "sample_logs" / "authentication.log"

LOG_PATTERN = re.compile(
    r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"(Failed|Accepted) password for \S+ from "
    r"(\d{1,3}(?:\.\d{1,3}){3})$"
)


def detect_brute_force(logs, threshold=5, window_seconds=60):
    """
    Analyze authentication events and identify suspicious IP addresses.

    Returns a list of alerts.
    """

    if threshold < 1 or window_seconds < 0:
        raise ValueError("Threshold must be positive and window nonnegative")

    failed_attempts = defaultdict(list)

    for log in logs:
        match = LOG_PATTERN.search(log.strip())

        if not match:
            continue

        timestamp_text, status, ip_address = match.groups()

        # Validate the IP address
        try:
            ipaddress.IPv4Address(ip_address)
        except ipaddress.AddressValueError:
            continue

        # Ignore successful authentication events
        if status != "Failed":
            continue

        timestamp = datetime.strptime(
            timestamp_text,
            "%Y-%m-%d %H:%M:%S"
        )

        failed_attempts[ip_address].append(timestamp)

    alerts = []
    time_window = timedelta(seconds=window_seconds)

    for ip, timestamps in failed_attempts.items():
        timestamps.sort()

        left = 0

        for right, current_time in enumerate(timestamps):

            while current_time - timestamps[left] > time_window:
                left += 1

            count = right - left + 1

            if count >= threshold:
                alerts.append({
                    "source_ip": ip,
                    "failed_attempts": count,
                    "severity": "HIGH",
                    "first_seen": timestamps[left].isoformat(),
                    "last_seen": current_time.isoformat()
                })
                break

    return alerts


def main():
    print("\n===== MEDSECURE SECURITY MONITOR =====")

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        logs = file.readlines()

    alerts = detect_brute_force(
        logs,
        threshold=THRESHOLD,
        window_seconds=TIME_WINDOW
    )

    if not alerts:
        print("\nNo suspicious authentication activity detected.")

    for alert in alerts:
        print("\n[ALERT] Possible SSH Brute-Force Attack")
        print(f"Source IP: {alert['source_ip']}")
        print(f"Failed Attempts: {alert['failed_attempts']}")
        print(f"First Seen: {alert['first_seen']}")
        print(f"Last Seen: {alert['last_seen']}")
        print(f"Severity: {alert['severity']}")

    print("\n===== ANALYSIS COMPLETED =====")


if __name__ == "__main__":
    main()