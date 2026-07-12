# Astravon Live Arena
# API Documentation

**Version:** 1.0.0

**Base URL**

```
http://localhost:8000
```

---

# 1. Overview

The Astravon Live Arena API provides communication between:

- AI Engine
- Backend
- Frontend Dashboard

The API is REST-based with WebSocket support for real-time updates.

---

# 2. Architecture

```
Camera

↓

AI Engine

↓

REST API

↓

FastAPI Backend

↓

Database

↓

Dashboard
```

---

# 3. API Standards

Content Type

```
application/json
```

Encoding

```
UTF-8
```

Authentication

Current Version

```
None
```

Future

```
JWT Authentication
```

---

# 4. Response Format

Every endpoint returns

```json
{
    "success": true,
    "message": "Operation successful",
    "data": {}
}
```

Errors return

```json
{
    "success": false,
    "message": "Error description"
}
```

---

# 5. Health Check

## GET /

Purpose

Checks whether the backend is running.

Response

```json
{
    "message":"Astravon Live Arena API"
}
```

---

## GET /status

Purpose

Check server health.

Response

```json
{
    "status":"online",
    "version":"1.0.0"
}
```

---

# 6. AI Endpoints

## POST /api/ai/detection

Purpose

Receives processed AI data from the AI Engine.

Request

```json
{
    "camera_id":"CAM-01",
    "people_count":53,
    "density":"Medium",
    "temperature":28,
    "risk_score":34
}
```

Response

```json
{
    "success":true,
    "message":"Detection received."
}
```

---

## GET /api/ai/latest

Purpose

Returns the latest AI detection.

Response

```json
{
    "camera_id":"CAM-01",
    "people_count":53,
    "density":"Medium",
    "temperature":28,
    "risk_score":34,
    "timestamp":"2026-07-12T12:00:00"
}
```

---

# 7. Crowd Endpoints

## GET /api/crowd/statistics

Returns

```json
{
    "people_count":105,
    "density":"High",
    "occupancy":82
}
```

---

## GET /api/crowd/history

Returns historical crowd statistics.

Example

```json
[
    {
        "time":"12:00",
        "people":80
    },
    {
        "time":"12:01",
        "people":83
    }
]
```

---

# 8. Temperature Endpoints

## GET /api/temperature

Response

```json
{
    "temperature":29,
    "humidity":61,
    "heat_index":31
}
```

---

# 9. Risk Endpoints

## GET /api/risk

Response

```json
{
    "risk_score":44,
    "risk_level":"Moderate",
    "recommendation":"Continue Monitoring"
}
```

---

## GET /api/risk/history

Returns

```json
[
    {
        "time":"12:00",
        "risk":22
    },
    {
        "time":"12:01",
        "risk":27
    }
]
```

---

# 10. Alert Endpoints

## GET /api/alerts

Returns active alerts.

Example

```json
[
    {
        "id":1,
        "severity":"Warning",
        "message":"High Crowd Density"
    }
]
```

---

## POST /api/alerts

Creates an alert.

Request

```json
{
    "severity":"Critical",
    "message":"Emergency Evacuation Required"
}
```

---

## DELETE /api/alerts/{id}

Deletes an alert.

Response

```json
{
    "success":true
}
```

---

# 11. Event Endpoints

## GET /api/events

Returns all monitored events.

Example

```json
[
    {
        "id":1,
        "name":"Football Match"
    }
]
```

---

## POST /api/events

Create a new event.

Request

```json
{
    "name":"Concert",
    "venue":"Arena A",
    "capacity":3000
}
```

---

## GET /api/events/{id}

Returns event details.

---

## PUT /api/events/{id}

Updates event information.

---

## DELETE /api/events/{id}

Deletes an event.

---

# 12. Report Endpoints

## GET /api/reports

Returns available reports.

---

## GET /api/reports/{id}

Returns report details.

---

## POST /api/reports/generate

Generates a report.

Response

```json
{
    "status":"Generating"
}
```

---

# 13. Dashboard Endpoints

## GET /api/dashboard

Returns everything required for dashboard initialization.

Example

```json
{
    "people":95,
    "density":"Medium",
    "temperature":27,
    "risk":41,
    "alerts":[]
}
```

---

# 14. Camera Endpoints

## GET /api/cameras

Returns available cameras.

Example

```json
[
    {
        "id":"CAM-01",
        "status":"Online"
    }
]
```

---

# 15. Simulation Endpoints

## POST /api/simulation/start

Starts simulation.

---

## POST /api/simulation/stop

Stops simulation.

---

## POST /api/simulation/reset

Resets simulation.

---

## POST /api/simulation/event

Changes event mode.

Request

```json
{
    "event":"Football"
}
```

Supported

- Football
- Concert
- Graduation
- Conference

---

# 16. WebSocket API

Endpoint

```
ws://localhost:8000/ws
```

Purpose

Provides real-time updates.

Messages

```json
{
    "type":"crowd",
    "people":92
}
```

```json
{
    "type":"risk",
    "score":65
}
```

```json
{
    "type":"temperature",
    "value":31
}
```

```json
{
    "type":"alert",
    "severity":"Warning"
}
```

---

# 17. HTTP Status Codes

| Code | Meaning |
|-------|----------|
|200|Success|
|201|Created|
|400|Bad Request|
|401|Unauthorized|
|403|Forbidden|
|404|Not Found|
|409|Conflict|
|422|Validation Error|
|500|Internal Server Error|

---

# 18. Error Response

Example

```json
{
    "success":false,
    "message":"Camera not found."
}
```

---

# 19. API Flow

```
AI Engine

↓

POST Detection

↓

Backend

↓

Store Database

↓

Broadcast WebSocket

↓

Dashboard Update
```

---

# 20. AI Data Contract

The AI Engine **must** send the following structure.

```json
{
    "camera_id":"CAM-01",
    "timestamp":"2026-07-12T12:00:00",
    "people_count":84,
    "density":"High",
    "occupancy":78,
    "temperature":30,
    "humidity":55,
    "heat_index":33,
    "risk_score":61,
    "risk_level":"High"
}
```

This contract should remain stable so the frontend and backend can evolve independently.

---

# 21. Future API Expansion

Future endpoints may include:

- Authentication
- User management
- Multiple cameras
- Cloud synchronization
- IoT sensors
- Drone integration
- Mobile notifications
- Historical analytics
- AI model management

---

# 22. API Versioning

Current Version

```
v1
```

Future versions

```
/api/v2/
/api/v3/
```

Breaking changes should only be introduced in a new API version.

---

# 23. Testing the API

After starting the backend:

```
uvicorn main:app --reload
```

Open:

```
http://localhost:8000/docs
```

FastAPI automatically generates interactive Swagger documentation where every endpoint can be tested directly from the browser.

---

# 24. Summary

The Astravon Live Arena API is the communication backbone of the platform.

It enables:

- AI Engine → Backend communication
- Backend → Database persistence
- Backend → Frontend updates
- Real-time monitoring through WebSockets
- Modular expansion for future features

By maintaining a consistent API contract, each subsystem can be developed, tested, and improved independently while ensuring reliable integration across the entire platform.