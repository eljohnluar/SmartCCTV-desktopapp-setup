# AI Engine

> `backend/ai_engine/`

The intelligence core of SmartCCTV. Processes video frames and drives all automated decisions.

## Sub-Components

- [[Face Recognition]] — Detects and identifies enrolled students in real time
- [[Weapon Detection]] — Scans frames for threats using YOLOv8
- [[Gesture Detection]] — Detects open-palm confirmation gestures
- [[Compliance Checker]] — Validates student uniform policy against detected clothing
- [[Voice Engine]] — Generates and plays attendance/alert announcements

## Data Flow

```
[[Camera Ingestion]] supplies frames
         ↓
  ┌──────┴──────────────────────────┐
  │                                 │
[[Face Recognition]]       [[Weapon Detection]]
  │                                 │
  ↓                                 ↓
[[Database]] (attendance)   [[Database]] (alerts)
  │                                 │
  └──────────┬──────────────────────┘
             ↓
     [[WebSocket Manager]]
             ↓
         [[Frontend]]
```

## Reads From

- [[Config]] — Model paths, confidence thresholds, enabled flags
- [[Database]] — Enrolled student face embeddings

## Writes To

- [[Database]] — Attendance records, security alerts
- [[WebSocket Manager]] — Real-time events for frontend
