#!/usr/bin/env python3
"""Local-first defensive cybersecurity helper CLI."""
import argparse
import json
import sys
from pathlib import Path
from scripts.security_core import (
    doctor, sha256_file, analyze_pcap, authorized_nmap_scan, write_report
)

ROOT = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser(description="Antigravity Cybersecurity Assistant CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="Check availability of optional security tools")

    p_hash = sub.add_parser("hash", help="Calculate SHA-256 for an evidence file")
    p_hash.add_argument("file")

    p_pcap = sub.add_parser("pcap", help="Summarize a PCAP using tshark")
    p_pcap.add_argument("file")

    p_scan = sub.add_parser("scan", help="Run a scoped Nmap service/version scan")
    p_scan.add_argument("target", help="Single IP address inside configured authorized CIDRs")

    p_report = sub.add_parser("report", help="Create a basic Markdown report")
    p_report.add_argument("--title", required=True)
    p_report.add_argument("--finding", action="append", default=[])
    p_report.add_argument("--severity", default="Informational",
                          choices=["Critical", "High", "Medium", "Low", "Informational"])

    args = parser.parse_args()
    try:
        if args.command == "doctor":
            print(json.dumps(doctor(), indent=2))
        elif args.command == "hash":
            print(json.dumps(sha256_file(args.file), indent=2))
        elif args.command == "pcap":
            print(json.dumps(analyze_pcap(args.file), indent=2))
        elif args.command == "scan":
            print(json.dumps(authorized_nmap_scan(args.target, ROOT / "config/scope.json"), indent=2))
        elif args.command == "report":
            path = write_report(ROOT / "reports", args.title, args.finding, args.severity)
            print(f"Report created: {path}")
    except (ValueError, RuntimeError, FileNotFoundError, PermissionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
