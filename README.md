# CyberPulse

**CyberPulse** is a CLI tool to ingest vulnerability scanner exports (JSON, CSV, XML), apply risk-based prioritization, enrich findings with CVE data, and generate actionable remediation steps.

## Features

- Parse JSON, CSV, and XML scanner outputs  
- Apply CVSS-based prioritization, public-facing host checks, known-exploited CVE flags  
- Enrich findings from a local NVD database  
- One-line remediation summaries via on-device Llama-2 or GPT-4 (Pro)  
- Output grouped to-do lists (Critical, High, Medium) in Markdown, plain text, or Slack  

## Installation

```bash
pip install cyberpulse
```

## Quick Start

```bash
# Free mode (on-device Llama-2)
cyberpulse --input scan.json --output fixes.md

# Pro mode (GPT-4 via CyberPulse Cloud)
cyberpulse login
cyberpulse --input scan.json --cloud --slack
```

## Development

```bash
# From project root
source venv/bin/activate
pip install -r requirements-dev.txt
pytest --cov=src/cyberpulse
flake8 src/cyberpulse
black --check src/cyberpulse
```

## Project Structure

```text
cyberpulse/
├── src/
│   └── cyberpulse/
├── tests/
├── docs/
├── requirements.txt
├── requirements-dev.txt
├── README.md
└── .gitignore
```

## License

[MIT](LICENSE)
