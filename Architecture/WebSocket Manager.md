# WebSocket Manager

> `backend/websocket_manager.py`

The real-time nervous system of SmartCCTV. Fans out AI-detected events from background worker threads to every connected browser client simultaneously.

## Key Functions

| Function | Purpose |
|----------|---------|
| `manager.connect(ws)` | Accept and register a new browser WebSocket |
| `manager.broadcast(message)` | Async fan-out to all connected clients |
| `publish_from_worker(message)` | **Thread-safety bridge** — lets synchronous camera/AI threads safely push events into the async FastAPI event loop via `asyncio.run_coroutine_threadsafe()` |
| `set_event_loop(loop)` | Registers the app event loop at startup |

## Event Types

| Type | Published By | Consumed By |
|------|-------------|-------------|
| `attendance` | [[Face Recognition]] | [[Frontend]] Dashboard, AttendanceLog |
| `alert` | [[Weapon Detection]], [[Trespasser Detection]] | [[Frontend]] AlertsFeed, Alerts page |
| `voice` | [[Voice Engine]] | [[Frontend]] AppContext → SpeechSynthesis |
| `connection_ack` | `main.py` on connect | [[Frontend]] useRealtime |

## Why It's a Hub

Every AI detection event flows through here before reaching the browser. It decouples the synchronous Python AI threads from the async FastAPI/WebSocket layer.

## Connected To

- Receives from: [[Face Recognition]], [[Weapon Detection]], [[Trespasser Detection]], [[Compliance Checker]], [[Voice Engine]]
- Sends to: [[Frontend]]

## Part of

- [[SmartCCTV Overview]]
