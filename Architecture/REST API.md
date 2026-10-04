# REST API

> `backend/api/` + `backend/main.py`

FastAPI application that exposes all HTTP endpoints consumed by the [[Frontend]]. Registered with `/api` prefix.

## Routes

| Route File | Endpoints | Purpose |
|-----------|-----------|---------|
| `auth.py` | `/auth/login`, `/auth/register` | Teacher authentication |
| `students.py` | CRUD + `/students/face-enroll` | Student management + face enrollment |
| `attendance.py` | `/attendance/today`, `/date/:d`, `/manual`, `/reset` | Attendance records |
| `reports.py` | `/reports/summary`, `/trend`, `/export/csv`, `/export/pdf` | Analytics & exports |
| `alerts.py` | `/alerts` CRUD, `/alerts/reset` | Security alert management |
| `camera.py` | `/camera/stream` (MJPEG), `/attendance-recording`, `/test-voice` | Live feed + controls |
| `settings.py` | `/settings/uniform-policy`, `/voice`, `/gesture-attendance`, `/runtime-controls`, `/schedule` | System configuration |

## Special Endpoints

- `GET /api/system/status` — System health: camera active, AI active, student count, unresolved alerts
- `WS /ws` — WebSocket endpoint (see [[WebSocket Manager]])

## Middleware

- `cors.py` — Allows frontend origin
- `auth.py` — JWT Bearer token validation on protected routes

## Connections

- Reads/writes to [[Database]]
- Reads frames from [[Camera Ingestion]] (MJPEG stream)
- All settings read from [[Config]]
- Consumed by [[Frontend]] via `services/api.js`

## Part of

- [[SmartCCTV Overview]]
