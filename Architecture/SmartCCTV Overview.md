# SmartCCTV — System Overview

AI-powered attendance and campus security system for Bestlink College of the Philippines.

## Architecture Layers

- [[Camera Ingestion]] — Captures live frames from OBS Virtual Camera via OpenCV
- [[AI Engine]] — Face recognition, threat detection, gesture and compliance checking
- [[REST API]] — FastAPI HTTP endpoints consumed by the frontend
- [[WebSocket Manager]] — Real-time event bridge between backend workers and browser
- [[Database]] — Supabase PostgreSQL persistence layer
- [[Frontend]] — React + Vite single-page application
- [[Config]] — Central environment-driven configuration

## Entry Points

- Backend starts at `backend/main.py`
- Frontend starts at `frontend/src/main.jsx`
- All settings loaded from [[Config]]

## Real-Time Data Flow

[[Camera Ingestion]] → [[AI Engine]] → [[WebSocket Manager]] → [[Frontend]]

## Persistence Flow

[[AI Engine]] → [[Database]] → Supabase Cloud
[[REST API]] → [[Database]] → Supabase Cloud

## External Services

- [[Supabase]] — Cloud database, auth, and file storage
- OBS Studio — Virtual camera bridge between Yi IoT CCTV and OpenCV
