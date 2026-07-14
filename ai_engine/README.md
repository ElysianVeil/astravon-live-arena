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
