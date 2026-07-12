# Astravon Live Arena
# AI Engine Documentation

**Version:** 1.0.0

**AI Engine Version:** 1.0

**Project Lead:** Johnpaul Kiwinga

---

# 1. Overview

The AI Engine is the intelligence layer of Astravon Live Arena.

Its responsibility is to transform live video into meaningful operational information for event monitoring.

Unlike traditional surveillance systems that simply display video feeds, the AI Engine continuously analyzes scenes to estimate crowd activity, assess potential safety risks, and provide actionable insights.

The AI Engine performs real-time processing and communicates with the backend through REST APIs or WebSockets.

---

# 2. Objectives

The AI Engine is responsible for:

- Capturing live video
- Detecting people
- Tracking movement
- Counting individuals
- Estimating crowd density
- Calculating occupancy
- Simulating environmental conditions
- Estimating risk
- Sending structured data to the backend

---

# 3. AI Engine Architecture

```
                 Camera
                    │
                    ▼
            Frame Capture
                    │
                    ▼
            Image Processing
                    │
                    ▼
            YOLO Detection
                    │
                    ▼
              Object Tracker
                    │
                    ▼
            Crowd Analytics
                    │
                    ▼
            Heat Simulation
                    │
                    ▼
              Risk Engine
                    │
                    ▼
              JSON Output
                    │
                    ▼
               FastAPI API
```

---

# 4. Processing Pipeline

Every frame follows the same pipeline.

```
Capture Frame

↓

Preprocess Frame

↓

Run YOLO

↓

Detect People

↓

Track Objects

↓

Count People

↓

Calculate Density

↓

Estimate Occupancy

↓

Simulate Temperature

↓

Calculate Risk Score

↓

Return JSON
```

---

# 5. Folder Structure

```
ai_engine/

├── main.py
├── config.py
├── constants.py
│
├── models/
├── vision/
├── crowd/
├── heat/
├── risk/
├── simulation/
├── api/
├── analytics/
├── utils/
├── configs/
├── assets/
├── outputs/
├── logs/
└── tests/
```

---

# 6. Module Responsibilities

## Vision

Responsible for

- Camera access
- Frame capture
- Preprocessing
- Object detection
- Tracking
- Drawing overlays

Files

```
camera.py

stream.py

detector.py

tracker.py

drawing.py

zones.py
```

---

## Models

Stores AI models.

Contains

```
YOLO Weights

Labels

Model Loader
```

Example

```
best.pt

labels.txt

loader.py
```

---

## Crowd Module

Responsible for

- Crowd counting
- Density estimation
- Occupancy
- Congestion
- Crowd movement

Output

```
People Count

Density

Occupancy
```

---

## Heat Module

Since the MVP does not include IoT sensors,

temperature is simulated.

Responsibilities

- Temperature
- Humidity
- Heat Index

Future

Real sensor integration.

---

## Risk Module

Combines all measurements.

Input

- Crowd Density
- Occupancy
- Temperature

Output

```
Risk Score

Risk Level

Recommendation
```

---

## Simulation

Provides realistic demonstrations.

Supports

- Football
- Concert
- Graduation
- Conference

Simulation also generates

- Crowd growth
- Heat increase
- Random incidents

---

## API Module

Communicates with backend.

Responsible for

- JSON formatting
- HTTP requests
- WebSocket communication

---

## Analytics

Responsible for

- Metrics
- Performance
- Reports
- Logging

---

## Utilities

Contains reusable helper functions.

Examples

```
Logger

Validators

Image Helpers

Math Utilities
```

---

# 7. AI Workflow

```
Camera

↓

Frame

↓

YOLO Detection

↓

Person Detection

↓

Tracking

↓

Crowd Count

↓

Density

↓

Heat

↓

Risk

↓

Backend
```

---

# 8. Detection Workflow

```
Input Frame

↓

Resize

↓

Normalize

↓

YOLO

↓

Bounding Boxes

↓

Confidence Filter

↓

Output Detections
```

---

# 9. Tracking Workflow

```
Detected Objects

↓

Assign IDs

↓

Track Movement

↓

Update Positions

↓

Remove Lost Objects
```

Each detected person receives a temporary tracking ID.

Example

```
Person #1

Person #2

Person #3
```

---

# 10. Crowd Counting

Count all detected people.

Example

```
Detected

↓

95 People
```

Output

```json
{
    "people_count":95
}
```

---

# 11. Crowd Density

Density is estimated using

```
People Count

+

Camera Coverage Area
```

Example

```
0–30

Low

31–80

Medium

81+

High
```

Thresholds are configurable.

---

# 12. Occupancy

Occupancy compares

```
Current Attendance

÷

Venue Capacity
```

Example

```
People

180

Capacity

250

Occupancy

72%
```

---

# 13. Heat Simulation

The MVP simulates weather.

Example

```
Time

↓

Temperature

↓

Humidity

↓

Heat Index
```

Output

```json
{
    "temperature":30,
    "humidity":55,
    "heat_index":33
}
```

Future versions can replace this with live sensor data.

---

# 14. Risk Engine

The Risk Engine combines multiple indicators.

```
Crowd Density

+

Occupancy

+

Heat

↓

Risk Calculator
```

Output

```json
{
    "risk_score":68,
    "risk_level":"High"
}
```

---

# 15. Alert Logic

Example

```
IF

Density > Threshold

AND

Temperature > Threshold

↓

Generate Alert
```

Possible alerts

- High Crowd Density
- Over Capacity
- Heat Warning
- Critical Risk

---

# 16. AI Output Format

The AI Engine always returns the same structure.

```json
{
    "camera_id":"CAM-01",
    "timestamp":"2026-07-12T15:30:00",

    "people_count":82,

    "density":"Medium",

    "occupancy":68,

    "temperature":29,

    "humidity":54,

    "heat_index":31,

    "risk_score":45,

    "risk_level":"Moderate"
}
```

This serves as the contract with the backend.

---

# 17. Performance Goals

Prototype Targets

| Metric | Target |
|----------|----------|
| Detection Speed | 15–30 FPS |
| Response Time | <100 ms per frame |
| API Response | <50 ms |
| CPU Usage | Minimize where practical |
| Memory Usage | <2 GB (typical development machine) |

These targets are appropriate for an academic prototype and will vary depending on hardware.

---

# 18. Error Handling

The AI Engine should detect and recover from common issues.

Examples

```
Camera unavailable

↓

Retry Connection

↓

Notify Backend
```

```
YOLO Model Missing

↓

Stop Processing

↓

Log Error
```

```
Invalid Frame

↓

Discard Frame

↓

Continue Processing
```

---

# 19. Logging

Log

- Startup
- Camera connection
- Detection count
- Errors
- Warnings
- Performance

Example

```
[15:00]

Camera Connected

[15:01]

People Detected: 84

[15:02]

Risk Score: 61
```

---

# 20. Testing

Each module should have dedicated tests.

Examples

```
Camera Test

Detector Test

Tracker Test

Counter Test

Risk Test

API Test
```

Run

```
pytest
```

---

# 21. Future Improvements

Possible future features include:

- Multi-camera support
- Object classification beyond people
- Crowd flow prediction
- Abandoned object detection
- Queue length estimation
- Behavioral anomaly detection
- Real weather sensor integration
- Drone video support
- GPU acceleration
- Edge AI deployment
- Cloud inference
- AI model switching

---

# 22. Ethical Considerations

The AI Engine is designed with privacy in mind.

The prototype:

- Detects people without identifying them
- Does not perform facial recognition
- Does not store biometric information
- Uses aggregate crowd statistics
- Demonstrates responsible AI principles

---

# 23. AI Development Roadmap

## Week 1

- Camera
- YOLO
- Person Detection
- Crowd Counter

---

## Week 2

- Tracking
- Density
- Occupancy
- Heat Simulation

---

## Week 3

- Risk Engine
- Alerts
- Analytics
- Event Modes

---

## Week 4

- Optimization
- Testing
- Documentation
- Final Demonstration

---

# 24. Summary

The AI Engine is the analytical core of Astravon Live Arena.

It transforms live video into structured information by detecting people, estimating crowd conditions, simulating environmental factors, and calculating risk levels. The engine is modular by design, allowing new algorithms and capabilities to be added without changing the overall architecture.

By separating perception (vision), analysis (crowd, heat, risk), and communication (API), the AI Engine remains maintainable, extensible, and well suited for both this academic prototype and future real-world enhancements.