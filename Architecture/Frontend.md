# Frontend

> `frontend/src/` — React 18 + Vite single-page application

The teacher-facing UI for monitoring attendance, managing students, reviewing security alerts, and configuring the system.

## Pages

| Page | Route | Purpose |
|------|-------|---------|
| [[Landing Page]] | `/` (unauthenticated) | Cyberpunk login/register portal |
| [[Dashboard Page]] | `/` (authenticated) | Live camera, stats, attendance log, alerts |
| [[Students Page]] | `/students` | Student CRUD + face enrollment |
| [[Reports Page]] | `/reports` | Analytics, trend charts, CSV/PDF export |
| [[Alerts Page]] | `/alerts` | Security alert review and resolution |
| [[Settings Page]] | `/settings` | System configuration |
| [[Credits Page]] | `/credits` | Team and project credits |

## State Management

- [[Auth Context]] — User authentication, JWT token, 3-second cyberpunk loading screen
- [[App Context]] — Global system status, WebSocket events, notification queue

## Services

| Service | Purpose |
|---------|---------|
| `services/api.js` | Axios HTTP client for all [[REST API]] calls |
| `services/websocket.js` | `WSClient` singleton with auto-reconnect for [[WebSocket Manager]] events |
| `services/supabase.js` | Direct Supabase auth + Realtime subscriptions |

## Custom Hooks

| Hook | Wraps |
|------|-------|
| `useAttendance.js` | Attendance API + today's records |
| `useStudents.js` | Student list with sections |
| `useRealtime.js` | WebSocket event subscriptions |

## Connected To

- [[REST API]] — All HTTP data operations
- [[WebSocket Manager]] — Real-time push events
- [[Supabase]] — Direct auth and Realtime
- [[Config]] — Via `VITE_API_BASE_URL` env var

## Part of

- [[SmartCCTV Overview]]
