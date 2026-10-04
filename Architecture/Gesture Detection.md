# Gesture Detection

> `backend/ai_engine/gesture_detection.py`

Detects an open-palm hand gesture from video frames as a secondary confirmation before recording attendance.

## Purpose

When a student is enrolled with gesture confirmation enabled, they must show an open palm to the camera before their attendance is recorded. Students enrolled without it check in normally via [[Face Recognition]] only.

## Integration

- Receives frames from [[Camera Ingestion]]
- Works alongside [[Face Recognition]] in the recognition loop
- Enrolled gesture status is stored in [[Database]] (per-student flag)
- Controlled via the Settings page in [[Frontend]]

## Part of

- [[AI Engine]]
