# Auth Context

> `frontend/src/context/AuthContext.jsx`

Manages all authentication state in the [[Frontend]].

## Responsibilities

- Stores the logged-in teacher's `user` object and JWT `access_token` in `localStorage`
- Exposes `login()`, `register()`, `logout()` functions to all components
- Validates the hardcoded clearance code `TEACHER2026` on the client before sending to server
- Shows a 3-second cyberpunk **AuthLoadingScreen** on login, register, and logout transitions
- Bootstraps from `localStorage` on page reload (no re-login required within the 24-hour window)

## Auth Flow

```
User submits credentials on [[Landing Page]]
  → AuthContext.login()
  → POST /api/auth/login (via [[REST API]])
  → Store user + token in localStorage
  → Show AuthLoadingScreen (3s)
  → Render authenticated app
```

## Exposed Values

| Value | Type | Purpose |
|-------|------|---------|
| `user` | Object | Logged-in teacher profile |
| `loading` | Boolean | True during initial session restore |
| `authTransition` | Object | Drives loading screen (type + message) |
| `login()` | Function | Authenticate with username/password |
| `register()` | Function | Register with username/password/code |
| `logout()` | Function | Clear session |

## Connected To

- [[Landing Page]] — Login and register forms
- [[REST API]] — `/auth/login`, `/auth/register`
- [[Supabase]] — `supabase.auth.signOut()` on logout
- [[App Context]] — Wraps inside AuthProvider in `App.jsx`

## Part of

- [[Frontend]]
