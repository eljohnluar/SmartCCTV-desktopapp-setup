# Config

> `backend/utils/config.py`

Single source of truth for all environment-driven configuration. Uses Pydantic `BaseSettings` to load from a `.env` file.

## Configuration Groups

### Supabase
| Key | Purpose |
|-----|---------|
| `SUPABASE_URL` | Cloud DB URL |
| `SUPABASE_SERVICE_KEY` | Admin key for backend |
| `SUPABASE_ANON_KEY` | Public key fallback |

### Camera
| Key | Default |
|-----|---------|
| `CAMERA_INDEX` | `1` (OBS Virtual Cam) |
| `CAMERA_FPS` | `15` |
| `CAMERA_FRAME_WIDTH` | `1280` |
| `CAMERA_FRAME_HEIGHT` | `720` |

### Face Recognition
| Key | Default |
|-----|---------|
| `RECOGNITION_THRESHOLD` | `0.45` |
| `FACE_DETECTION_CONFIDENCE` | `0.75` |
| `FACE_DETECTION_FPS` | `6.0` |
| `FACE_DETECTION_MODEL_PATH` | YuNet ONNX path |
| `FACE_RECOGNITION_MODEL_PATH` | SFace ONNX path |

### Security / YOLO
| Key | Default |
|-----|---------|
| `WEAPON_DETECTION_ENABLED` | `true` |
| `YOLO_MODEL_PATH` | `yolov8n.pt` |
| `WEAPON_CONFIDENCE_THRESHOLD` | `0.35` |

### Voice
| Key | Default |
|-----|---------|
| `VOICE_ENABLED` | `true` |
| `VOICE_LANGUAGE` | `en` |

## Read By

Every backend module reads from the `settings` singleton:
- [[Camera Ingestion]]
- [[Face Recognition]]
- [[Weapon Detection]]
- [[Voice Engine]]
- [[Database]]
- [[REST API]]

## Part of

- [[SmartCCTV Overview]]
