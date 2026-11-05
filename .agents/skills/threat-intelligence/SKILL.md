---
name: threat-intelligence
description: IOC enrichment, threat research and defensive threat hunting.
---

# Threat Intelligence Skill

## Workflow
1. Normalize indicators (IP, domain, URL, hash, email) and record source.
2. Check reputable vendor advisories and trusted feeds.
3. Assess freshness, confidence, context and possible false positives.
4. Correlate indicators with local telemetry supplied by the user.
5. Recommend defensive detections and containment.

## Boundaries
Do not interact with malicious infrastructure beyond safe, passive lookups. Do not download or execute payloads. Do not treat a single feed hit as proof of compromise.

## Output
IOC, source, first/last seen if known, confidence, context, false-positive notes and defensive action.
