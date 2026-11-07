# Security Policy

## Project status

MedSecure is an educational security automation prototype, not a production SIEM or medical system. The supported development branch is `main`.

## Reporting a vulnerability

Please **do not** post active credentials, tokens, private keys, personal information, or sensitive exploit details in a public GitHub issue or pull request.

Use GitHub's **Report a vulnerability** option under the repository's Security tab if private vulnerability reporting is enabled. Otherwise, request a private communication channel through the maintainer's GitHub profile **before** sharing sensitive details. Do not assume public issue comments are confidential.

## Data and secrets

- Use synthetic, non-identifiable log samples in this public repository.
- Do not commit `.env` variants, API keys, private keys, credentials, or real patient/security logs.
- Keep credentials outside source control. GitHub Actions secrets should be managed in GitHub settings, not in workflow YAML.
- If a secret is ever committed, **revoke or rotate it immediately**; deleting the file does not remove it from Git history.

## Automated protections

- MedSecure CI executes Python unit tests, a Docker build, and a container smoke test.
- CodeQL scans Python on pushes, pull requests, and a weekly schedule.
- Dependabot checks GitHub Actions and Docker image references weekly.

GitHub account protections, branch rules, secret-scanning alert settings, and collaborators are controlled in GitHub's Settings/Security interfaces. This document does not mean those settings are enabled.
