# Weapon Detection

> `backend/ai_engine/security/weapon_detection.py`

Scans video frames for weapons and hazardous objects using the YOLOv8n model.

## How It Works

- Runs at ~3 scans/second (`SCAN_INTERVAL = 0.33s`)
- Detected threats persist on-screen for 1.8s to prevent flickering
- Per-class alert cooldown of 20 seconds prevents repeated notifications
- Draws red corner-bracket bounding boxes with confidence labels on the MJPEG stream

## Detectable Threats

| Class | Min Confidence |
|-------|---------------|
| knife / bladed weapon | 0.35–0.40 |
| gun / firearm | 0.32 |
| weapon (generic) | 0.38 |
| explosive | 0.30 |

## Model

- **YOLOv8n** — `yolov8n.pt` (loaded from path in [[Config]])

## Pipeline

```
Frame from [[Camera Ingestion]]
  → scan_threats() (YOLOv8n inference)
  → draw_threat_boxes() (annotates MJPEG stream)
  → [[Database]] (write security alert)
  → [[WebSocket Manager]] (push "alert" event to [[Frontend]])
```

## Related

- [[Compliance Checker]] — uniform compliance in the same security module
- [[Trespasser Detection]]
- [[AI Engine]]
