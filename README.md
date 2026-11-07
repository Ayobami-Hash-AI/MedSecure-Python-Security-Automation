# MedSecure — Python Security Automation

A lightweight, reproducible Python project for detecting suspicious SSH authentication patterns in **synthetic** security logs. Built as a practical exercise in Python automation, security detection engineering, Linux development, testing, and Git version control.

[![MedSecure CI](https://github.com/Ayobami-Hash-AI/MedSecure-Python-Security-Automation/actions/workflows/ci.yml/badge.svg)](https://github.com/Ayobami-Hash-AI/MedSecure-Python-Security-Automation/actions/workflows/ci.yml)

> **Status:** Milestones 1–5 complete (Docker and CI included). This is a learning prototype, not a production SIEM or real-time intrusion detection system.

## What it does

- Reads timestamped authentication events from `sample_logs/authentication.log`.
- Parses the event timestamp, outcome, and source IPv4 address.
- Validates extracted IPv4 addresses and ignores successful logins.
- Groups failed logins by source IP.
- Uses a sliding 60-second window to flag **five or more failed attempts** from the same IP.
- Prints a structured high-severity *possible SSH brute-force* alert with first/last observed timestamps.
- Exposes detection logic as `detect_brute_force()` for reuse and testing.
- Creates structured JSON incident reports with identifiers, timestamps, severity and investigation status.
- Runs inside a non-root Docker container and validates changes with GitHub Actions.

A threshold alert is **not proof of an attack**. A human analyst must investigate the context.

## Repository layout

```text
MedSecure-Python-Security-Automation/
├── src/
│   ├── monitor.py               # Log parsing, detection, and reporting integration
│   └── reporter.py              # JSON incident report generation
├── sample_logs/
│   └── authentication.log       # Synthetic events for reproduction
├── tests/
│   ├── test_monitor.py          # Five detection tests
│   └── test_reporter.py         # Four incident-report tests
├── reports/
│   └── .gitkeep                 # Generated JSON reports are ignored
├── .github/workflows/ci.yml      # Automated tests, Docker build, container smoke test
├── Dockerfile                   # Non-root Python container image
├── .dockerignore                # Excluded Docker build context files
├── .gitignore
├── LICENSE
└── README.md
```

## Requirements

- Python 3 (developed and tested with Python 3.14.4 on Ubuntu under WSL2)
- Git (optional, for cloning)
- Docker Desktop or Docker Engine (optional, for container execution)

The application uses only Python's standard library; no third-party Python packages are required.

## Run locally

```bash
git clone https://github.com/Ayobami-Hash-AI/MedSecure-Python-Security-Automation.git
cd MedSecure-Python-Security-Automation
python3 src/monitor.py
```

When an alert is found, MedSecure also writes a JSON incident report under `reports/`. Generated `reports/*.json` files are excluded from version control; rerunning the monitor creates another report for the same sample activity.

## Run with Docker

From the repository root:

```bash
docker build -t medsecure-monitor:1.0 .
docker run --rm medsecure-monitor:1.0
```

To **retain generated JSON reports** after the container exits, use a bind mount:

```bash
mkdir -p reports
docker run --rm \\
  --mount type=bind,source="$(pwd)/reports",target=/app/reports \\
  medsecure-monitor:1.0
ls reports/
```

The bind-mount example uses Bash (Linux, macOS or WSL2). The container runs as UID 10001, so the host directory must be writable by that user. Generated reports are ignored by Git; do not commit sensitive incident data. Without a mount, reports disappear when the `--rm` container exits.

Expected detection for the committed synthetic sample:

```text
===== MEDSECURE SECURITY MONITOR =====

[ALERT] Possible SSH Brute-Force Attack
Source IP: 192.168.1.10
Failed Attempts: 5
First Seen: 2026-11-06T10:01:12
Last Seen: 2026-11-06T10:01:20
Severity: HIGH

===== ANALYSIS COMPLETED =====
```

## Run automated tests

```bash
python3 -m unittest discover -s tests -v
```

Nine tests currently cover detection and incident reporting:

| Scenario | Expected outcome |
| --- | --- |
| Five failures from one IP within 60 seconds | Alert |
| Five failures spread across ten minutes | No alert |
| Three failures within 60 seconds | No alert |
| Successful logins only | No alert |
| Failures from five distinct IPs | No alert |

The four reporting tests verify file creation, expected JSON fields, zero reports for zero alerts, and separate files for multiple alerts.

**Observed milestone-4 result:** 9 tests passed in 0.014 seconds on the development machine. Runtime will vary.

## Continuous integration

The workflow at `.github/workflows/ci.yml` runs on pushes and pull requests targeting `main`. It checks out the code, sets up Python 3.14, runs all nine `unittest` cases, builds the Docker image, and performs a container execution smoke test. A green workflow result indicates those configured checks passed; it is not a security audit or proof of production readiness.

## Detection approach

1. Read log lines from the sample file.
2. Match the supported synthetic authentication-log format using a regular expression.
3. Validate IPv4 addresses and retain failed attempts.
4. Sort timestamps for each source IP.
5. Slide a two-pointer window forward, counting failures within 60 seconds.
6. Emit at most one alert per source IP once the threshold is reached.

The current parser expects records like:

```text
2026-11-06 10:01:12 Failed password for admin from 192.168.1.10
```

It is **not** yet a parser for all native Linux `auth.log` / journald formats. The program runs on demand, not continuously. It does not block IPs or send notifications. JSON incident reports are written locally, but the application does not yet deduplicate repeat detections.

## Development milestones

| Milestone | Outcome | Status |
| --- | --- | --- |
| 1 — Initial detector | Count simulated failed logins and print an alert | Complete |
| 2 — Time-based analysis | Read external log file; correlate failures within 60 seconds | Complete |
| 3 — Testable detection engine | Reusable function, IPv4 validation, sliding window, five unit tests | Complete |
| 4 — Incident reporting | Save structured JSON incident reports; four reporting unit tests | Complete |
| 5 — Packaging and CI | Docker image, persistent report bind mount, and GitHub Actions validation | Complete |

## Skills demonstrated

**Python:** collections, functions, dictionaries, regular expressions, file I/O, JSON serialization, UTC timestamps, UUID-based identifiers, IP validation, and sliding-window algorithms.

**Security:** SSH authentication analysis, event correlation, detection thresholds, alert triage, and false-positive considerations.

**Engineering:** Linux/WSL2 execution, Git/GitHub workflows, reusable modules, temporary-directory test isolation, Docker images and bind mounts, non-root execution, GitHub Actions CI, repeatable test fixtures, and regression tests.

## Responsible use

All committed authentication events are synthetic and intended for defensive education and reproducible testing. No real healthcare or patient data is used.

## Next steps

- Continuous monitoring of appended authentication events.
- Deduplication and alert suppression to reduce repeated incident reports.
- Better parsing, configuration, logging and error handling.
- Additional security tests and container hardening.
