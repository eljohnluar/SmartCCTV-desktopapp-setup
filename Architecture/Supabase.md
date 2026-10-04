# Supabase

> Cloud backend-as-a-service powering the SmartCCTV persistence layer.

## Services Used

| Service        | Purpose                                                                       |
| -------------- | ----------------------------------------------------------------------------- |
| **PostgreSQL** | Primary database for students, attendance, alerts, users                      |
| **Auth**       | JWT-based teacher authentication (login/register)                             |
| **Storage**    | `face-enrollments` bucket for storing enrolled face images                    |
| **Realtime**   | Used by [[Frontend]] for live database subscriptions (via Supabase JS client) |

## Tables

- `students` — enrolled student profiles and face embedding metadata
- `attendance_records` — daily check-in records with status and confidence
- `alerts` — security incidents (weapons, trespassers, compliance violations)
- `users` — teacher accounts

## Connected To

- [[Database]] — All SQL queries via Python `supabase-py` client
- [[Frontend]] — Direct auth + Realtime subscriptions via `supabase-js`
- [[Config]] — Credentials (`SUPABASE_URL`, `SUPABASE_SERVICE_KEY`)

## Part of

- [[SmartCCTV Overview]]
