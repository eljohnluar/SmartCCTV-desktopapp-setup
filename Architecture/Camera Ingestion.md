# Camera Ingestion

> `backend/ai_engine/camera/`

Captures live video frames from an OBS Virtual Camera using OpenCV's `VideoCapture`.

## Files

- `rtsp_client.py` — `CameraCapture` singleton (`camera_stream`). Runs a daemon thread that continuously reads frames at the configured FPS, stores `latest_frame`, and fires an optional per-frame callback.
- `frame_processor.py` — Stateless frame utilities: resize, grayscale convert, ROI crop.

## Connections

- Reads settings from [[Config]] (camera index, FPS, resolution)
- Provides frames to [[AI Engine]]
- Exposes `get_latest_frame()` to [[REST API]] for MJPEG streaming to [[Frontend]]
- Started and stopped by `main.py` (see [[REST API]])

## Hardware Chain

```
Yi IoT CCTV Camera
  → OBS Studio (window capture → Virtual Camera)
    → OpenCV VideoCapture(index)
      → camera_stream.latest_frame
```

## Key Properties

| Property | Default |
|----------|---------|
| Camera Index | `1` (OBS Virtual Cam) |
| Target FPS | `15` |
| Resolution | `1280 × 720` |
| Thread Model | Background daemon thread |
