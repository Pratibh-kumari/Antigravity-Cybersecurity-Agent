---
name: network-security
description: Authorized network inventory, Nmap output interpretation and read-only PCAP analysis.
---

# Network Security Skill

## Supported workflows
- Review existing Nmap XML/text output.
- Use `python cybersec.py scan <single-private-IP>` only after configuring approved CIDRs.
- Analyze user-supplied PCAP files with `python cybersec.py pcap <file>`.
- Hash evidence with `python cybersec.py hash <file>`.

## Analysis
Identify services, unexpected exposure, protocol anomalies, suspicious DNS/HTTP patterns and unusual communication. Correlate timestamps and avoid asserting maliciousness from a single indicator.

## Safety
No stealth scans, evasion, exploitation, flooding, credential capture or scanning outside configured authorized scope. Ask before any scan that may affect production systems.

## Report
Include asset, ports/services, evidence, confidence, business impact, remediation and limitations.
