# Antigravity Cybersecurity Multi-Agent Assistant

A modular, local-first cybersecurity assistant scaffold for Google Antigravity on Kali Linux + Python.

## What is included
- Master orchestration instructions in `AGENTS.md`
- Reusable Antigravity skills in `.agents/skills/`
- Python CLI for safe local workflows
- Explicit target scope enforcement for Nmap
- PCAP metadata analysis using `tshark` (when installed)
- SHA-256 evidence hashing
- Markdown report generation
- Tool availability checks

## Safety model
This project is intended for systems, networks, files, and lab environments that you own or are explicitly authorized to assess.
- Network scans are disabled until you configure `config/scope.json`.
- Nmap targets must be inside an explicitly approved CIDR.
- The CLI uses argument arrays (not shell strings).
- No exploit execution, password attacks, stealth, persistence, destructive actions, or data exfiltration are implemented.
- Review commands and scope before running them. Do not add public targets unless you have written authorization.

## 1. Install on Kali Linux

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nmap tshark yara git
# Optional tools, install only when needed:
sudo apt install -y whois dnsutils
```

Some packages may be unavailable or named differently on your Kali release. Check with `apt-cache policy <package>`.

```bash
git clone <your-repository-url>
cd antigravity-cybersecurity-agent
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp config/scope.example.json config/scope.json
```

Edit `config/scope.json` and add only authorized lab CIDRs, for example `192.168.56.0/24` for a host-only virtual lab. Do not assume that example subnet matches your network.

## 2. Open in Antigravity
1. Open this project folder in Antigravity.
2. Ensure `.agents/skills/` is present.
3. Start a new agent conversation if the skills do not appear immediately.
4. Ask for a task in natural language, e.g. "Use the network-security skill to review this lab PCAP."
5. For network scanning, explicitly identify the authorized target and ensure it is covered by `config/scope.json`.

Skills are instruction packages. They do not automatically install tools, grant privileges, or create independent LLM agents.

## 3. CLI examples

```bash
python cybersec.py doctor
python cybersec.py hash evidence/sample.bin
python cybersec.py pcap evidence/lab-capture.pcap
python cybersec.py scan 192.168.56.10
python cybersec.py report --title "Lab network review" --finding "Unnecessary service exposed" --severity Medium
```

`scan` is restricted to configured CIDRs. Nmap service/version detection can still generate traffic; use only on authorized lab systems.

## 4. Recommended workflow
1. Define objective, ownership/authorization, target, time window, and exclusions.
2. Select one specialist skill.
3. Collect evidence using the least intrusive method.
4. Preserve originals; hash evidence before analysis.
5. Validate findings and record confidence/limitations.
6. Generate a report with evidence and remediation.
7. Obtain human review before any intrusive follow-up.

## 5. Add optional tools
Use the package manager or official vendor instructions. Verify each binary with `command -v <tool>`.
- Network: `nmap`, `tshark`
- Web testing: OWASP ZAP (prefer passive/baseline checks in a lab)
- Forensics: Autopsy, Sleuth Kit, Volatility 3
- Malware triage: YARA, Ghidra (analyze samples in an isolated VM)
- Threat research: local IOC lists and reputable vendor advisories

Do not run unknown samples on your host machine. Use an isolated, disposable VM with snapshots and no shared folders/network unless specifically required.

## 6. Project layout

```text
.
├── AGENTS.md
├── cybersec.py
├── requirements.txt
├── config/
│   ├── scope.example.json
│   └── scope.json                 # local-only; do not commit
├── scripts/
│   └── security_core.py
├── evidence/
├── reports/
└── .agents/skills/
    ├── orchestrator/
    ├── recon-osint/
    ├── network-security/
    ├── web-api-security/
    ├── vulnerability-assessment/
    ├── digital-forensics/
    ├── malware-triage/
    ├── ctf-analysis/
    ├── threat-intelligence/
    ├── incident-response/
    └── security-reporting/
```

## 7. Limitations
This is a safe starter framework, not an autonomous penetration-testing platform. It does not prove exploitability, guarantee vulnerability coverage, or replace expert review. Tool outputs can be incomplete or misleading.


## Upstream knowledge and payload-reference integration

`config/repository-integrations.json` records a curated integration with:
- `mukul975/Anthropic-Cybersecurity-Skills` (Apache-2.0): reference patterns include focused skill procedures, compact discovery metadata, and supporting references/scripts. The inspected default branch listed 818 skill directories.
- `Pratibh-kumari/PayloadsAllTheThings` (MIT): topic-level web-security references, including SQLi, XSS, SSRF, command injection, traversal, XXE, IDOR and CSRF.

This project links to upstream payload documentation rather than copying the corpus or auto-firing payloads. Use only local intentionally vulnerable labs or explicitly authorized staging assets. The `payload-reference-testing` skill requires exact scope and approval, favors harmless canaries and synthetic records, and prohibits credential capture, exfiltration, destructive tests and denial of service.

```bash
python scripts/payload_catalog.py
python scripts/payload_catalog.py sqli
```

The catalogue is offline and reference-only. Refresh by reviewing upstream changes, confirming current commits and license files, then updating the manifest. Do not auto-sync executable payload files into the runtime.
