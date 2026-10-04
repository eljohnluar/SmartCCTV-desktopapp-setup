# Compliance Checker

> `backend/ai_engine/security/compliance.py`

Validates whether detected individuals are wearing uniforms that match the school's approved color policy.

## How It Works

- Reads the active uniform color policy from `utils/uniform_policy.py`
- The policy is configured via the Settings page and persisted in [[Database]]
- Approved colors: Navy Blue, Royal Blue, Maroon, Bright Red, White, Gray, Green
- Non-compliant students trigger a status of `late` or flag for manual review

## Integration

- Receives frames from [[Camera Ingestion]]
- Reads policy from [[Config]] / `uniform_policy.py`
- Compliance result flows into [[Database]] (attendance status field)
- Can push compliance alerts through [[WebSocket Manager]] to [[Frontend]]

## Part of

- [[AI Engine]]
- [[Weapon Detection]] (same `security/` module folder)
