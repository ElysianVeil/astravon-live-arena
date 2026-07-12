# Astravon Live Arena
## System Architecture

**Version:** 1.0.0

**Project Lead:** Johnpaul Kiwinga

---

# 1. Overview

Astravon Live Arena is an AI-powered event monitoring and safety management platform designed to demonstrate how Artificial Intelligence, Information Systems, Computer Vision, Networking, and Web Technologies work together in a real-world application.

The platform monitors a simulated football match, concert, graduation, or public event using computer vision to estimate crowd statistics, assess potential safety risks, and present information through an interactive dashboard.

The project is educational and uses simulated data where real hardware (such as temperature sensors) is unavailable.

---

# 2. High-Level Architecture

```
                        Webcam / Video
                              │
                              ▼
                   AI Engine (OpenCV + YOLO)
                              │
                              ▼
                Crowd & Risk Analysis Engine
                              │
                              ▼
                  FastAPI Backend Services
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
          PostgreSQL Database       WebSocket API
                 │                         │
                 └────────────┬────────────┘
                              ▼
                  Frontend Dashboard
                              │
                              ▼
                         End User
```

---

# 3. System Layers

The application consists of five major layers.

## Layer 1 — Input Layer

Responsible for collecting all incoming data.

Sources include:

- Webcam
- Video file
- Simulated temperature
- Simulated event data

Output:

```
Raw Frames
```

---

## Layer 2 — AI Engine

Processes incoming frames using Computer Vision.

Responsibilities

- Detect people
- Count people
- Track movement
- Estimate density
- Calculate occupancy
- Simulate environmental factors
- Produce AI statistics

Output Example

```json
{
    "people_count": 83,
    "density": "High",
    "temperature": 31,
    "risk_score": 78
}
```

---

## Layer 3 — Backend

The backend is responsible for managing application logic.

Responsibilities

- Receive AI data
- Store event statistics
- Manage alerts
- Generate reports
- Serve API endpoints
- Broadcast WebSocket updates

Framework

FastAPI

---

## Layer 4 — Database

Stores application information.

Main entities

- Events
- Alerts
- Crowd Statistics
- Reports

Database

PostgreSQL

---

## Layer 5 — Dashboard

Provides a visual interface for users.

Displays

- Live camera
- Crowd count
- Density
- Temperature
- Risk score
- Charts
- Event timeline
- Reports
- Alerts

Technologies

- HTML
- CSS
- JavaScript

---

# 4. Module Architecture

```
Astravon Live Arena

├── Frontend
│
├── Backend
│
├── AI Engine
│
├── Database
│
└── Documentation
```

---

## AI Engine

```
AI Engine

Camera

↓

Detection

↓

Tracking

↓

Crowd Analysis

↓

Heat Simulation

↓

Risk Analysis

↓

JSON Output
```

---

## Backend

```
Request

↓

API

↓

Business Logic

↓

Database

↓

Response
```

---

## Frontend

```
Browser

↓

Dashboard

↓

Charts

↓

Live Updates

↓

User Interaction
```

---

# 5. Data Flow

```
Camera

↓

Frame Capture

↓

YOLO Detection

↓

Crowd Counter

↓

Risk Calculator

↓

Backend API

↓

Database

↓

Dashboard

↓

User
```

---

# 6. Communication Flow

The AI Engine communicates only with the backend.

```
AI Engine

↓

HTTP/WebSocket

↓

Backend

↓

HTTP/WebSocket

↓

Frontend
```

The frontend never communicates directly with the AI Engine.

---

# 7. Folder Responsibilities

## Frontend

Responsible for

- User Interface
- Charts
- Map
- Alerts
- Reports

---

## Backend

Responsible for

- APIs
- Business Logic
- Database
- Authentication (future)
- Event Processing

---

## AI Engine

Responsible for

- Camera
- Detection
- Tracking
- Crowd Analytics
- Risk Analysis

---

## Database

Responsible for

- Persistent Storage

---

## Documentation

Responsible for

- Technical Documentation
- Architecture
- Setup Guide
- API Guide

---

# 8. External Libraries

## AI

- OpenCV
- Ultralytics YOLO
- NumPy

---

## Backend

- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic

---

## Database

- PostgreSQL

---

## Frontend

- HTML5
- CSS3
- JavaScript
- Chart.js
- Leaflet.js

---

# 9. Event Workflow

```
Start Event

↓

Open Camera

↓

Detect People

↓

Count Crowd

↓

Calculate Density

↓

Estimate Risk

↓

Store Statistics

↓

Update Dashboard

↓

Generate Alerts

↓

Generate Report

↓

End Event
```

---

# 10. Safety Score Formula (Prototype)

The prototype combines multiple indicators into a single score.

Example

```
Safety Score

=

40% Crowd Density

+

30% Occupancy

+

30% Temperature
```

The exact weighting can be adjusted during testing.

---

# 11. Event Modes

Different event types use different thresholds.

### Football

High crowd tolerance

Large occupancy

High movement

---

### Concert

Very high movement

High excitement

Lower congestion threshold

---

### Graduation

Moderate density

Lower movement

Family attendance

---

### Conference

Low density

Minimal movement

Quiet environment

---

# 12. Scalability

The architecture supports future enhancements without redesign.

Possible extensions

- Multiple cameras
- Real IoT sensors
- Facial recognition (subject to ethics and legal approval)
- Drone surveillance
- Mobile application
- Cloud deployment
- Historical analytics
- Predictive crowd modelling

---

# 13. Security Considerations

The system follows basic security principles.

- Validate all API inputs.
- Restrict API access.
- Secure database credentials.
- Store configuration in environment variables.
- Log system events.
- Prevent unauthorized access.

---

# 14. Ethical Considerations

Astravon Live Arena is designed for educational purposes.

The prototype:

- Does not identify individuals.
- Does not perform facial recognition.
- Uses crowd-level analytics instead of personal identification.
- Demonstrates responsible AI principles.

---

# 15. Development Roadmap

## Week 1

- Repository setup
- Backend
- Webcam
- Person detection
- Dashboard

---

## Week 2

- Crowd density
- Occupancy
- Heat simulation
- Risk score
- Charts

---

## Week 3

- Alerts
- Event modes
- Reports
- Database
- Map

---

## Week 4

- Testing
- Optimization
- Documentation
- Presentation
- Final demonstration

---

# 16. Future Vision

Astravon Live Arena is intended as a modular platform that can evolve into a real-time event operations system capable of supporting stadiums, concerts, conferences, and public gatherings through AI-assisted monitoring and decision support.