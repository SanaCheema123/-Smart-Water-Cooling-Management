# Smart Water and Cooling Management Platform — Backend (FIXED)
[Aivonex.webm](https://github.com/user-attachments/assets/29e0ab74-2636-483e-8894-8ad777650081)

A prototype backend for cooling-water monitoring, cooling-water demand prediction, leak/anomaly detection, WUE, recommendations, WebSockets, PostgreSQL and Grafana.

## Important Windows fix
This package uses `psycopg[binary]` instead of the old `psycopg2-binary==2.9.10`, avoiding the `pg_config executable not found` build error seen with Python 3.14.

The API no longer crashes during import when PostgreSQL is temporarily unavailable. Swagger can open, while database endpoints become usable after PostgreSQL is running.

## Run without venv
```powershell
Copy-Item .env.example .env -Force
python -m pip install -r requirements.txt
docker compose up -d postgres grafana
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Swagger: http://127.0.0.1:8000/docs
Health: http://127.0.0.1:8000/api/health
Grafana: http://127.0.0.1:3000
WebSocket: ws://127.0.0.1:8000/ws/sensors

## API
- POST /api/readings
- GET /api/readings
- GET /api/readings/latest
- GET /api/dashboard
- GET /api/predictions/demand
- GET /api/prediction
- GET /api/leak
- GET /api/anomaly
- GET /api/wue
- GET /api/recommendations
- GET /api/alerts
- PATCH /api/alerts/{alert_id}/acknowledge
- GET /api/reports/sustainability

## Simulation
After the API and PostgreSQL are running:
```powershell
python scripts/simulate_sensors.py
```
The simulator generates normal readings and deliberate abnormal events for testing.

## Troubleshooting
If `docker compose up` reports `dockerDesktopLinuxEngine` not found, start Docker Desktop first, then run the compose command again. This is a Docker daemon/desktop state issue, not a Python package error.

If `/api/health` says database `error`, PostgreSQL is not reachable on localhost:5432.

## Python 3.14 compatibility fix

This release pins scikit-learn to 1.9.1 and SciPy to 1.16.3, which provide CPython 3.14 Windows wheels. This avoids the source-build/Windows Long Path failure seen with older scikit-learn releases. The project remains designed to run without a virtual environment.
