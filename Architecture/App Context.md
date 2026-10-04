# App Context

> `frontend/src/context/AppContext.jsx`

Global application state for the teacher dashboard in the [[Frontend]].

## Responsibilities

- Tracks the live system status and connection state
- Stores notification messages and toast queue items
- Receives real-time events from the [[WebSocket Manager]]
- Controls shared dashboard behavior for alerts, attendance, and voice messages
- Exposes app-wide state to the authenticated UI

## Data Flow

```
[[WebSocket Manager]]
  → AppContext event handlers
  → UI updates in [[Dashboard Page]], [[Alerts Page]], and [[Settings Page]]
```

## Connected To

- [[Frontend]]
- [[WebSocket Manager]]
- [[REST API]]
- [[Voice Engine]]

## Part of

- [[Frontend]]
