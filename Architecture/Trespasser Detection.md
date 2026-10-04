# Trespasser Detection

> `backend/ai_engine/security/trespasser.py`

Detects individuals on camera who are not enrolled in the student database.

## How It Works

- Runs alongside [[Face Recognition]]
- If a face is detected but does not match any enrolled student, it is flagged as an unrecognized individual
- Triggers a security alert stored in [[Database]]
- Pushes an `alert` event via [[WebSocket Manager]] to [[Frontend]]

## Part of

- [[AI Engine]]
- [[Weapon Detection]] (same `security/` module folder)
