from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
import re

# Security detection configuration
THRESHOLD = 5
TIME_WINDOW = timedelta(seconds=60)

# Locate the authentication log
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "sample_logs" / "authentication.log"

# Store failed authentication attempts by IP
failed_attempts = defaultdict(list)

# Define the expected log format
pattern = re.compile(
    r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"Failed password for \S+ from "
    r"(\d{1,3}(?:\.\d{1,3}){3})$"
)

print("\n===== MEDSECURE SECURITY MONITOR =====")

# Read and process authentication logs
with open(LOG_FILE, "r", encoding="utf-8") as file:
    for line in file:

        match = pattern.search(line.strip())

        if match:
            timestamp = datetime.strptime(
                match.group(1),
                "%Y-%m-%d %H:%M:%S"
            )

            ip_address = match.group(2)

            failed_attempts[ip_address].append(timestamp)

# Analyze failed attempts within a time window
for ip, timestamps in failed_attempts.items():

    timestamps.sort()

    for index, start_time in enumerate(timestamps):

        attempts_in_window = [
            timestamp
            for timestamp in timestamps[index:]
            if timestamp - start_time <= TIME_WINDOW
        ]

        if len(attempts_in_window) >= THRESHOLD:

            print("\n[ALERT] Possible SSH Brute-Force Attack")
            print(f"Source IP: {ip}")
            print(f"Failed Attempts: {len(attempts_in_window)}")
            print(f"Time Window: {TIME_WINDOW.total_seconds()} seconds")
            print("Severity: HIGH")

            break

print("\n===== ANALYSIS COMPLETED =====")