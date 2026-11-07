from collections import Counter
import re

# Simulated hospital server authentication logs
logs = [
    "Failed password for admin from 192.168.1.10",
    "Failed password for root from 192.168.1.10",
    "Failed password for admin from 192.168.1.10",
    "Accepted password for john from 192.168.1.20",
    "Failed password for root from 192.168.1.10",
    "Failed password for admin from 192.168.1.10",
]

failed_ips = []

# Analyze each authentication event
for log in logs:
    if "Failed password" in log:
        match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", log)

        if match:
            failed_ips.append(match.group(1))

# Count failed login attempts
attempts = Counter(failed_ips)

print("\n===== MEDSECURE SECURITY MONITOR =====")

for ip, count in attempts.items():
    print(f"\nSource IP: {ip}")
    print(f"Failed Login Attempts: {count}")

    if count >= 5:
        print("ALERT: Possible SSH Brute-Force Attack!")
        print("Severity: HIGH")
    else:
        print("Status: Monitoring")

print("\n===== ANALYSIS COMPLETED =====")