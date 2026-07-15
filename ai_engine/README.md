# Astravon Live Arena AI Engine

## Overview

The **Astravon Live Arena AI Engine** is the computer vision component of the Astravon Live Arena platform. It processes live camera feeds and recorded videos to detect, track, and analyze crowds in real time. The engine communicates with the FastAPI backend, which powers the dashboard, reporting system, and emergency response modules.

The AI Engine is designed to be modular, making it easy to replace or improve individual components without affecting the rest of the system.

---

# Objectives

The AI Engine is responsible for:

* Detecting people using a pretrained YOLO model.
* Tracking individuals across video frames.
* Counting people accurately.
* Estimating crowd density.
* Calculating venue occupancy.
* Monitoring crowd movement.
* Simulating environmental conditions.
* Estimating crowd risk levels.
* Sending real-time data to the backend.
* Supporting multiple camera feeds.

---

# Features

* Multi-camera support
* Real-time person detection
* Crowd counting
* Crowd density estimation
* Occupancy monitoring
* Crowd movement analysis
* Congestion detection
* Heat simulation
* Risk scoring
* Alert generation
* Report generation
* WebSocket communication
* REST API integration
* Modular architecture

---

# Project Structure

```text
ai_engine/

├── README.md
├── requirements.txt
├── main.py
├── config.py
├── constants.py

├── models/
│   ├── yolov_model/
│   └── cache/

├── vision/
│   ├── camera.py
│   ├── camera_manager.py
│   ├── stream.py
│   ├── detector.py
│   ├── tracker.py
│   ├── pipeline.py
│   ├── preprocessing.py
│   ├── calibration.py
│   ├── drawing.py
│   └── zones.py

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

# Technology Stack

## Computer Vision

* Ultralytics YOLOv8 / YOLO11
* OpenCV

## Tracking

* ByteTrack

## Programming Language

* Python 3.11+

## Communication

* FastAPI
* REST API
* WebSocket

## Configuration

* YAML
* Environment Variables

---

# AI Pipeline

```text
Phone Camera / Video

        │

        ▼

OpenCV Video Stream

        │

        ▼

YOLO Detection

        │

        ▼

ByteTrack Tracking

        │

        ▼

Crowd Analysis

        │

        ▼

Risk Analysis

        │

        ▼

Backend API

        │

        ▼

Live Dashboard
```

---

# Detection Classes

The MVP primarily focuses on the following object classes:

* Person
* Backpack
* Handbag
* Car
* Bus
* Truck
* Motorcycle
* Bicycle

The **Person** class is the primary input for crowd analytics.

---

# Multi-Camera Support

The engine is designed to process multiple camera feeds simultaneously.

Supported sources include:

* USB webcams
* Laptop cameras
* Mobile phone IP cameras
* Recorded videos
* RTSP streams (future)
* CCTV systems (future)

Each camera is processed independently before results are aggregated.

---

# Crowd Analytics

The engine calculates:

* Total people
* Crowd density
* Occupancy percentage
* Crowd movement
* Congestion level
* Crowd trends
* Average flow rate

---

# Heat Simulation

The MVP includes environmental simulation such as:

* Temperature
* Humidity
* Heat Index

These values are combined with crowd statistics to estimate overall event conditions.

---

# Risk Analysis

Risk analysis combines multiple indicators, including:

* Crowd size
* Crowd density
* Heat index
* Occupancy
* Congestion
* Movement

The engine classifies risk into:

* Low
* Medium
* High
* Critical

---

# Backend Integration

The AI Engine communicates with the Astravon Live Arena backend using HTTP requests and WebSocket messages.

Example output:

```json
{
  "camera_id": 1,
  "location": "North Entrance",
  "people_count": 84,
  "density": "High",
  "occupancy": 72,
  "temperature": 31.4,
  "risk_score": 76
}
```

---

# Configuration

Configuration files are stored in the `configs/` directory.

Examples:

* `ai.yaml`
* `camera.yaml`
* `risk.yaml`

These files define:

* Model settings
* Camera settings
* Detection thresholds
* Risk thresholds

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
```

Navigate into the AI engine:

```bash
cd ai_engine
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the AI Engine

Start the engine with:

```bash
python main.py
```

---

# Outputs

Processed data can be saved to:

* `outputs/processed_frames/`
* `outputs/reports/`
* `outputs/recordings/`

---

# Testing

Run the test suite:

```bash
pytest tests -v
```

---

# Future Enhancements

* Custom model fine-tuning
* Automatic camera discovery
* Face anonymization
* Emergency exit monitoring
* Vehicle flow analysis
* Predictive crowd behavior
* Drone camera integration
* Thermal camera support
* Cloud deployment
* Distributed edge processing

---

# License

Copyright © House of Astravon.

All rights reserved.

---

# Author

**House of Astravon**

Astravon Live Arena — AI-powered crowd monitoring and event safety platform.


Yes, and this is actually a very good time to tighten the architecture. Right now your dashboard is mixing **live values** with **connection status**, which is why you're seeing contradictions like:

* ✅ Live Camera
* ✅ People = 1
* ✅ FPS = 2.61
* ❌ Backend: Offline
* ❌ AI Engine: Offline
* ❌ WebSocket: Disconnected

Those cannot all be true simultaneously.

---

## Think of Live Arena as a telemetry system

Every number on the dashboard should come from the backend, not be guessed by the frontend.

For example, your AI pipeline already knows:

```python
statistics = {

    "people_count": people_count,

    "occupancy": occupancy,

    "density": density,

    "temperature": temperature,

    "humidity": humidity,

    "heat_index": heat_index,

    "risk_score": risk["risk_score"],

    "risk_level": risk["risk_level"],

    "detected_objects": len(objects),

    "confidence": confidence,

    "processing_time": processing_time,

    "fps": self.metrics.average_fps()

}
```

That is your source of truth.

---

# Backend health

The backend should periodically broadcast

```json
{
    "type": "system",
    "data": {

        "backend": true,

        "ai_engine": true,

        "websocket": true,

        "timestamp": 1754567890

    }
}
```

The frontend should **never** assume the backend is offline.

---

## WebSocket status

The frontend already knows this.

```javascript
socket.onopen
```

means

```
WebSocket Connected
```

and

```javascript
socket.onclose
```

means

```
Disconnected
```

No fake values.

---

## AI Engine status

The backend knows whether the AI Engine is connected.

Example

```python
class LiveState:

    ai_connected = False
```

When the AI connects

```python
LiveState.ai_connected = True
```

When it disconnects

```python
LiveState.ai_connected = False
```

Broadcast

```python
await manager.broadcast({

    "type": "system",

    "data": {

        "ai_engine": LiveState.ai_connected,

        "backend": True

    }

})
```

---

## Camera

Instead of only

```
Resolution

FPS

Frames
```

I'd make it

```
Resolution : 1280 × 720
Camera FPS : 2.61
Frames Received : 137
Latency : 21 ms
Last Frame : 17:58:02
```

That immediately tells you whether you're actually receiving a live stream.

---

## Analytics

Processing

```
0.3 ms
```

is almost certainly misleading.

YOLO inference alone usually takes tens of milliseconds on a CPU.

You probably want

```
Capture

Inference

Tracking

Drawing

Encoding

Total

FPS
```

Example

```
Capture       6 ms
Inference    81 ms
Tracking      2 ms
Drawing       3 ms
Encoding      7 ms
---------------------
Total        99 ms

FPS = 10.1
```

Now you immediately know where the bottleneck is.

---

## Integrity panel

Since Astravon Live Arena is intended as a monitoring platform, I'd even add a small "System Integrity" card.

```
System Integrity

✔ Backend Online

✔ AI Connected

✔ Camera Active

✔ WebSocket Connected

✔ Statistics Updating

✔ Frames Streaming

✔ Alerts Active

Last Update:
17:58:04.221
```

If any component fails, it turns red immediately.

---

I think this would make the dashboard feel much more like a professional operations center. Instead of simply showing data, it would continuously verify that every subsystem (camera, AI, backend, WebSocket, analytics, and alerts) is healthy and synchronized, making it much easier to trust the integrity of the live information during demonstrations and testing.


Given the stage Astravon Live Arena is in, I would approach it like a software engineer validating a safety-critical system rather than just a developer fixing bugs.

Instead of asking *"Does the dashboard work?"*, ask:

> **"Can I prove that every value on the screen is correct?"**

That mindset changes how you test the application.

---

# Phase 1 — Validate the Data Source

First, ensure every subsystem produces correct data independently.

### Camera

Verify that:

* Camera ID remains constant.
* Resolution matches the configured value.
* FPS is measured correctly.
* Frame counter increases continuously.
* Reconnection works after disconnecting the camera.

Example checklist:

```
✓ Camera connected
✓ Width = 1280
✓ Height = 720
✓ FPS > 0
✓ Frames increasing
✓ Timestamp updating
```

---

### Weather

Compare your backend values with the weather API.

For example:

```
Weather API

Temperature = 19.1°C
Humidity = 61%
Wind = 9.2 km/h
Weather Code = 3

↓

Dashboard

Temperature = 19.1°C ✓
Humidity = 61% ✓
Wind = 9.2 km/h ✓
Weather Code = 3 ✓
```

If every field matches, that module passes.

---

### AI Detection

Create known test cases.

#### Empty room

Expected:

```
People = 0

Objects = 0

Risk = Low
```

---

#### One person

```
People = 1

Objects = Person

Occupancy > 0%

Risk still Low
```

---

#### Five people

```
People = 5

Occupancy increases

Density changes

Risk updates
```

Don't move on until these behave consistently.

---

# Phase 2 — Validate Every Calculation

This is where many systems fail.

Every derived value should have a formula.

Example:

```
Occupancy

=

People

÷

Maximum Capacity

×

100
```

Verify manually.

Example:

```
Capacity = 500

People = 125

Expected occupancy = 25%
```

Does the dashboard show 25%?

If not,

there's a bug.

---

Do the same for

```
Density

Heat Index

Risk Score

Risk Level
```

---

# Phase 3 — Validate Data Flow

The data passes through several stages:

```
Camera

↓

AI Engine

↓

Backend

↓

WebSocket

↓

Frontend

↓

Dashboard
```

At every stage,

log the values.

Example:

```
Camera

People = 23

↓

AI

People = 23

↓

Backend

People = 23

↓

WebSocket

People = 23

↓

Dashboard

People = 23
```

If any stage differs,

that's where the bug is.

---

# Phase 4 — Stress Testing

A real event isn't static.

Test rapid changes.

Examples:

```
0 people

↓

100 people

↓

20 people

↓

350 people

↓

0 people
```

The dashboard should update smoothly.

No freezes.

No negative values.

No lag.

---

# Phase 5 — Edge Cases

These reveal hidden bugs.

Test things like:

### Camera disconnected

Expected:

```
Camera Offline

No crash

Reconnect button works
```

---

### Weather API unavailable

Expected:

```
Unknown

—not—

Application crash
```

---

### AI timeout

Expected:

```
No detection

Previous statistics retained

Warning logged
```

---

### WebSocket disconnected

Expected:

```
Status = Disconnected

Reconnect automatically

Dashboard resumes
```

---

### Invalid values

Test:

```
People = -5

Temperature = 500°C

Humidity = 150%
```

Your validators should reject them.

---

# Phase 6 — Performance

Measure:

```
Frame Capture

↓

Inference

↓

Statistics

↓

WebSocket

↓

Rendering
```

For example:

```
Frame Capture

12 ms

↓

YOLO

32 ms

↓

Statistics

2 ms

↓

WebSocket

4 ms

↓

Dashboard

7 ms

Total

57 ms
```

This lets you know exactly where bottlenecks are.

---

# Phase 7 — User Experience

Ask questions like:

Can someone understand the dashboard in five seconds?

For example:

```
Camera

Online

Crowd

245

Risk

Medium

Temperature

31°C

Alerts

2
```

Should be instantly understandable.

---

# Phase 8 — Logging

Every important action should leave a trail.

Example:

```
19:15:01

Camera Connected

19:15:04

People = 43

19:15:05

Risk = Medium

19:15:07

Alert Created

Heat Warning

19:15:09

Emergency Vehicle Dispatched
```

Good logs make debugging and demonstrations much easier.

---

# Phase 9 — Demonstration Scenario

Since Astravon Live Arena is intended as a smart event safety platform, build a scripted scenario that exercises the whole system.

For example:

1. Camera starts.
2. Weather loads.
3. Crowd grows from 0 to 300 people.
4. Occupancy reaches 70%.
5. Density changes from Low → High.
6. Heat index rises.
7. Risk becomes High.
8. Alert is generated.
9. Emergency response appears on the map.
10. Reports update automatically.

If the application can handle that sequence reliably, you've demonstrated that all the major components work together.

---

## A practical order of work

1. ✅ Validate all backend calculations (occupancy, density, heat index, risk).
2. ✅ Validate REST API responses with tools like Swagger or Postman.
3. ✅ Validate WebSocket payloads against the REST responses.
4. ✅ Validate frontend rendering against the incoming data.
5. ✅ Run stress and edge-case tests.
6. ✅ Optimize performance where needed.
7. ✅ Polish the UI and prepare a complete demonstration scenario.

Following that order lets you catch problems at the source instead of chasing symptoms in the dashboard. It also builds confidence that every number the system displays is accurate before you add more advanced capabilities.
