# Database

> `backend/database/`

Abstraction layer over Supabase PostgreSQL. All persistence reads and writes in the system flow through here.

## Files

| File | Role |
|------|------|
| `supabase_client.py` | Lazily initializes `supabase_client` from env vars. Raises `DatabaseUnavailableError` if unconfigured, surfaced as HTTP 503. |
| `queries.py` | All CRUD: students, attendance records, alerts, settings. |
| `storage.py` | Supabase Storage operations for the `face-enrollments` bucket (face image upload/download). |
| `schema.sql` | PostgreSQL table definitions (students, attendance, alerts, sections). |
| `users_schema.sql` | User table schema for teacher accounts. |

## Tables (Supabase PostgreSQL)

| Table | Used By |
|-------|---------|
| `students` | [[REST API]], [[Face Recognition]] |
| `attendance_records` | [[Face Recognition]], [[REST API]] |
| `alerts` | [[Weapon Detection]], [[Trespasser Detection]], [[REST API]] |
| `users` | [[REST API]] auth routes |

## Storage Buckets (Supabase)

| Bucket | Used By |
|--------|---------|
| `face-enrollments` | [[Face Recognition]] (stores enrolled face images) |

## Error Handling

`DatabaseUnavailableError` propagates cleanly as HTTP 503 when Supabase is not configured, so the app degrades gracefully.

## Connected To

- [[Supabase]] — Cloud host
- [[REST API]] — Reads/writes via routes
- [[Face Recognition]] — Attendance writes
- [[Weapon Detection]] — Alert writes
- [[Config]] — Connection credentials

## Part of

- [[SmartCCTV Overview]]
