"""Safe, bounded helpers for local defensive analysis."""
import hashlib
import ipaddress
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

def doctor():
    tools = ["python3", "nmap", "tshark", "yara", "whois", "dig", "zaproxy", "vol"]
    return {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "tools": {name: shutil.which(name) or "not installed" for name in tools}
    }

def _existing_file(path):
    p = Path(path).expanduser().resolve()
    if not p.is_file():
        raise FileNotFoundError(f"File not found: {p}")
    return p

def sha256_file(path):
    p = _existing_file(path)
    digest = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return {"file": str(p), "size_bytes": p.stat().st_size, "sha256": digest.hexdigest()}

def analyze_pcap(path):
    p = _existing_file(path)
    tshark = shutil.which("tshark")
    if not tshark:
        raise RuntimeError("tshark is not installed. Install Wireshark/tshark first.")
    # Read-only summary; no packet payload export.
    cmd = [tshark, "-r", str(p), "-q", "-z", "io,phs"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "tshark failed")
    return {
        "file": str(p),
        "sha256": sha256_file(p)["sha256"],
        "analysis": "Protocol hierarchy summary (read-only)",
        "summary": result.stdout[-12000:]
    }

def _load_scope(scope_path):
    p = Path(scope_path)
    if not p.exists():
        raise RuntimeError(
            "Scope is not configured. Copy config/scope.example.json to config/scope.json "
            "and enter only authorized lab CIDRs."
        )
    try:
        data = json.loads(p.read_text())
        cidrs = [ipaddress.ip_network(x, strict=False) for x in data.get("authorized_cidrs", [])]
    except (ValueError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Invalid scope configuration: {exc}")
    if not cidrs:
        raise RuntimeError("No authorized_cidrs configured; refusing to scan.")
    return data, cidrs

def authorized_nmap_scan(target, scope_path):
    try:
        ip = ipaddress.ip_address(target)
    except ValueError:
        raise ValueError("This starter scanner accepts one literal IP address only.")
    config, networks = _load_scope(scope_path)
    if config.get("require_private_address", True) and not ip.is_private:
        raise RuntimeError("Refusing non-private target because require_private_address is enabled.")
    if not any(ip in net for net in networks):
        raise RuntimeError(f"Target {ip} is outside all configured authorized CIDRs.")
    nmap = shutil.which("nmap")
    if not nmap:
        raise RuntimeError("nmap is not installed.")
    cmd = [nmap, "-sV", "-T3", "--top-ports", "100", "--reason", str(ip)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, check=False)
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr.strip() or "nmap failed")
    return {
        "target": str(ip),
        "scope_cidrs": [str(n) for n in networks],
        "command": cmd,
        "return_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "note": "Service/version scan; run only with explicit authorization."
    }

def write_report(report_dir, title, findings, severity):
    report_dir = Path(report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    safe_title = "".join(c if c.isalnum() or c in "-_" else "_" for c in title).strip("_")[:70]
    if not safe_title:
        safe_title = "security_report"
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = report_dir / f"{stamp}-{safe_title}.md"
    lines = [
        f"# {title}", "",
        f"- Generated: {datetime.now(timezone.utc).isoformat()}",
        "- Assessment type: Defensive / authorized analysis",
        "- Status: Draft — requires human review", "",
        "## Executive summary", "",
        f"Number of supplied findings: {len(findings)}", "",
        "## Findings", ""
    ]
    if not findings:
        lines.append("No findings were supplied. This does not mean the target is secure.")
    for i, finding in enumerate(findings, 1):
        lines += [
            f"### {i}. {finding}", "",
            f"- Severity: {severity}",
            "- Confidence: Not assessed",
            "- Evidence: Add exact evidence and timestamps before distribution.",
            "- Remediation: Add a specific, validated remediation.",
            ""
        ]
    lines += [
        "## Scope and methodology", "",
        "Document authorized assets, exclusions, tools and versions, time window, and methods here.", "",
        "## Limitations", "",
        "This report is a template. Findings and severity require analyst validation.", ""
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
