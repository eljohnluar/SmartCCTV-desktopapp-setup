# Face Recognition

> `backend/ai_engine/face_recognition/`

Identifies enrolled students from live camera frames using two ONNX models.

## Files

| File | Role |
|------|------|
| `detector.py` | Detects face bounding boxes — **YuNet** ONNX model |
| `recognizer.py` | Matches face crops to stored embeddings — **SFace** ONNX model |
| `live_matcher.py` | Orchestrates the real-time loop: detect → recognize → record → announce |
| `liveness.py` | Anti-spoofing: rejects photos and printed faces |

## ONNX Models

- `ai_engine/models/face_detection_yunet_2023mar.onnx`
- `ai_engine/models/face_recognition_sface_2021dec.onnx`

## Pipeline

```
Frame from [[Camera Ingestion]]
  → detector.py  (YuNet — find face boxes)
  → recognizer.py (SFace — match embeddings)
  → [[Database]] (write attendance record)
  → [[Voice Engine]] (announce result)
  → [[WebSocket Manager]] (push "attendance" event to [[Frontend]])
```

## Key Settings (from [[Config]])

| Setting | Default |
|---------|---------|
| Recognition threshold | `0.45` |
| Detection confidence | `0.75` |
| Detection FPS | `6.0` |
| Min face size | `28 px` |

## Part of

- [[AI Engine]]
- [[SmartCCTV Overview]]
