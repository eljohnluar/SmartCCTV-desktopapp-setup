# Voice Engine

> `backend/ai_engine/voice/`

Generates and plays spoken announcements for attendance check-ins and security alerts.

## Files

| File | Role |
|------|------|
| `announcer.py` | Builds announcement text (e.g., "Welcome, John. Marked Present.") |
| `speaker.py` | Plays audio via gTTS (Google Text-to-Speech). Also publishes `voice` WebSocket events for browser fallback. |

## Dual-Mode Audio

1. **Server audio** — gTTS generates and plays audio through the server machine's speakers (e.g., the classroom PC connected to the CCTV system).
2. **Browser fallback** — If server audio is unavailable, a `voice` event is sent via [[WebSocket Manager]] and the [[Frontend]]'s `AppContext` uses the Web SpeechSynthesis API in the browser.

## Triggered By

- [[Face Recognition]] — on successful student identification
- [[Weapon Detection]] — on threat detection alert

## Settings (from [[Config]])

| Setting | Default |
|---------|---------|
| Voice enabled | `true` |
| Language | `en` |
| Volume | Configurable via Settings page |

## Part of

- [[AI Engine]]
