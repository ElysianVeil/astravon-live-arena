astravon-live-arena/
│
├── README.md
├── LICENSE
├── .gitignore
├── CONTRIBUTING.md
├── PROJECT_PLAN.md
├── CHANGELOG.md
│
├── frontend/                 # Member 1
│   │
│   ├── index.html
│   ├── css/
│   │   ├── style.css
│   │   └── dashboard.css
│   │
│   ├── js/
│   │   ├── app.js
│   │   ├── dashboard.js
│   │   ├── charts.js
│   │   ├── map.js
│   │   └── websocket.js
│   │
│   ├── assets/
│   │   ├── images/
│   │   └── icons/
│   │
│   └── README.md
│
│
├── backend/                 # Member 3
│   │
│   ├── app/
│   │   │
│   │   ├── main.py
│   │   ├── config.py
│   │   │
│   │   ├── api/
│   │   │   ├── routes.py
│   │   │   ├── alerts.py
│   │   │   └── statistics.py
│   │   │
│   │   ├── database/
│   │   │   ├── database.py
│   │   │   ├── models.py
│   │   │   └── schemas.py
│   │   │
│   │   ├── websocket/
│   │   │   └── manager.py
│   │   │
│   │   └── services/
│   │       ├── risk_service.py
│   │       └── routing_service.py
│   │
│   ├── requirements.txt
│   └── README.md
│
│
├── ai_engine/               # Member 2
│   │
│   ├── vision/
│   │   ├── camera.py
│   │   ├── detector.py
│   │   └── tracker.py
│   │
│   ├── models/
│   │   └── yolov_model/
│   │
│   ├── crowd/
│   │   ├── counter.py
│   │   └── density.py
│   │
│   ├── heat/
│   │   └── simulator.py
│   │
│   ├── risk/
│   │   └── analyzer.py
│   │
│   ├── requirements.txt
│   └── README.md
│
│
├── database/
│   │
│   ├── schema.sql
│   └── seed.sql
│
│
├── docs/
│   │
│   ├── architecture.md
│   ├── diagrams/
│   ├── screenshots/
│   └── presentation/
│
│
├── tests/
│
└── docker-compose.yml

Since you're taking ownership of the **AI Engine** and serving as the **Project Lead**, I recommend designing it as if it were a standalone AI service. This keeps it modular, testable, and easy for the backend team to integrate. The layout below preserves your current structure while expanding it into a professional architecture.

```text
ai_engine/
│
├── README.md
├── requirements.txt
├── main.py                     # Starts the AI Engine
├── config.py                   # Configuration settings
├── constants.py                # Global constants
├── __init__.py
│
├── models/                     # AI models
│   │
│   ├── README.md
│   ├── __init__.py
│   │
│   ├── yolov_model/
│   │   ├── best.pt
│   │   ├── yolov8n.pt
│   │   ├── labels.txt
│   │   └── model_loader.py
│   │
│   ├── classifiers/
│   │   └── __init__.py
│   │
│   └── cache/
│
├── vision/                     # Camera and image processing
│   │
│   ├── __init__.py
│   ├── camera.py
│   ├── detector.py
│   ├── tracker.py
│   ├── stream.py
│   ├── frame_reader.py
│   ├── frame_processor.py
│   ├── preprocessing.py
│   ├── drawing.py
│   ├── calibration.py
│   └── zones.py
│
├── crowd/                      # Crowd analytics
│   │
│   ├── __init__.py
│   ├── counter.py
│   ├── density.py
│   ├── occupancy.py
│   ├── movement.py
│   ├── congestion.py
│   ├── flow.py
│   ├── statistics.py
│   └── trends.py
│
├── heat/                       # Environmental simulation
│   │
│   ├── __init__.py
│   ├── simulator.py
│   ├── temperature.py
│   ├── humidity.py
│   ├── heat_index.py
│   ├── weather_adapter.py
│   └── alerts.py
│
├── risk/                       # Risk intelligence
│   │
│   ├── __init__.py
│   ├── analyzer.py
│   ├── scoring.py
│   ├── severity.py
│   ├── thresholds.py
│   ├── incidents.py
│   ├── recommendations.py
│   └── predictor.py
│
├── simulation/                 # Demo and testing utilities
│   │
│   ├── __init__.py
│   ├── crowd_generator.py
│   ├── event_simulator.py
│   ├── incident_generator.py
│   ├── fake_temperature.py
│   └── random_events.py
│
├── api/                        # Communication with backend
│   │
│   ├── __init__.py
│   ├── output.py
│   ├── schemas.py
│   ├── serializers.py
│   ├── websocket_client.py
│   └── http_client.py
│
├── analytics/                  # AI statistics
│   │
│   ├── __init__.py
│   ├── metrics.py
│   ├── logger.py
│   ├── reports.py
│   └── exporter.py
│
├── storage/                    # Temporary AI data
│   │
│   ├── __init__.py
│   ├── cache.py
│   ├── session.py
│   └── history.py
│
├── utils/                      # Shared helper functions
│   │
│   ├── __init__.py
│   ├── logger.py
│   ├── timer.py
│   ├── helpers.py
│   ├── validators.py
│   ├── file_manager.py
│   ├── image_utils.py
│   └── math_utils.py
│
├── configs/                    # Configuration files
│   │
│   ├── ai.yaml
│   ├── camera.yaml
│   ├── risk.yaml
│   ├── thresholds.yaml
│   └── logging.yaml
│
├── assets/                     # AI resources
│   │
│   ├── icons/
│   ├── sample_images/
│   ├── sample_videos/
│   └── demo_data/
│
├── logs/
│   ├── engine.log
│   ├── detections.log
│   └── errors.log
│
├── outputs/                    # Generated results
│   ├── screenshots/
│   ├── processed_frames/
│   ├── recordings/
│   └── reports/
│
├── tests/
│   │
│   ├── __init__.py
│   ├── test_camera.py
│   ├── test_detector.py
│   ├── test_tracker.py
│   ├── test_counter.py
│   ├── test_density.py
│   ├── test_risk.py
│   ├── test_heat.py
│   └── test_api.py
│
└── docs/
    ├── architecture.md
    ├── api.md
    ├── workflow.md
    ├── setup.md
    └── algorithms.md
```

## Module Responsibilities

| Module         | Purpose                                                                                           |
| -------------- | ------------------------------------------------------------------------------------------------- |
| **vision**     | Captures video, preprocesses frames, performs object detection and tracking.                      |
| **models**     | Stores YOLO weights and model-loading logic.                                                      |
| **crowd**      | Counts people, estimates density, tracks movement, and computes occupancy.                        |
| **heat**       | Simulates environmental conditions such as temperature and heat index for the prototype.          |
| **risk**       | Combines crowd and environmental data into safety scores, risk levels, and recommendations.       |
| **simulation** | Generates synthetic scenarios for demonstrations (e.g., concerts, football matches, emergencies). |
| **api**        | Formats AI results and sends them to the backend through HTTP or WebSockets.                      |
| **analytics**  | Produces reports and performance metrics about detections and system operation.                   |
| **storage**    | Manages temporary session data and caches without relying on the backend database.                |
| **utils**      | Shared helper functions used throughout the AI engine.                                            |
| **configs**    | Centralizes configuration values so code doesn't need hard-coded settings.                        |
| **assets**     | Stores videos, images, and other resources for testing and demonstrations.                        |
| **logs**       | Records detections, warnings, and errors for debugging.                                           |
| **outputs**    | Saves generated reports, processed frames, and recordings.                                        |
| **tests**      | Unit and integration tests for the AI engine.                                                     |
| **docs**       | Technical documentation describing the architecture, APIs, setup, and algorithms.                 |

### AI Engine Workflow

```text
Camera / Video
      │
      ▼
Frame Capture
      │
      ▼
Preprocessing
      │
      ▼
YOLO Detection
      │
      ▼
Object Tracking
      │
      ▼
Crowd Analytics
      │
      ▼
Heat Simulation
      │
      ▼
Risk Analysis
      │
      ▼
JSON Output API
      │
      ▼
FastAPI Backend
      │
      ▼
Dashboard
```

This structure is intentionally **modular**. Even though your current MVP only needs webcam input, person detection, crowd counting, heat simulation, and risk analysis, the architecture leaves room for future enhancements—such as multi-camera support, real environmental sensors, or additional analytics—without requiring a major redesign.


If you're preparing to do **Astravon Live Arena** by yourself, then the project needs to be planned differently. Instead of building three separate systems and hoping they'll fit together, you'll build **one coherent system in layers**. Every week should produce something you can demonstrate, even if it's not feature-complete.

The guiding principle is:

> **Always have a working application. Never spend a week building something that can't be demonstrated.**

---

# Overall Project Timeline (4 Weeks)

```text
Week 1 → Working Prototype
Week 2 → AI Intelligence
Week 3 → Operations Dashboard
Week 4 → Polish, Testing & Presentation
```

Each week ends with a demonstration.

---

# Final System Architecture

```text
Astravon Live Arena

├── Frontend Dashboard
│
├── FastAPI Backend
│
├── AI Engine
│
├── PostgreSQL Database
│
├── Event Simulation Engine
│
└── Documentation
```

---

# WEEK 1 — Build the Foundation

## Goal

By the end of Week 1, you should be able to show:

* A dashboard in the browser
* A live webcam feed
* AI detecting people
* The current people count displayed
* Backend API running
* Repository with documentation

Even if it only detects people, that's already a working AI application.

---

## Day 1 — Project Initialization

Create the repository structure.

Set up:

* Python virtual environment
* GitHub repository
* Project board
* Documentation

Install:

```bash
pip install fastapi
pip install uvicorn
pip install ultralytics
pip install opencv-python
pip install numpy
pip install python-multipart
```

Deliverable:

```
Repository initialized
```

---

## Day 2 — Backend

Create:

```
backend/

main.py
```

Run:

```
localhost:8000
```

Endpoints:

```
GET /

GET /status
```

Output:

```json
{
  "status":"online"
}
```

Deliverable:

```
Backend running
```

---

## Day 3 — AI Camera

Open webcam.

Display live video.

No AI yet.

Deliverable:

```
Camera opens successfully.
```

---

## Day 4 — YOLO

Install YOLO.

Detect people.

Draw boxes.

Deliverable:

```
People detected.
```

---

## Day 5 — Crowd Counter

Count:

```
People: 7
```

Display on video.

Deliverable:

```
Live people counter.
```

---

## Day 6

Connect AI →

Backend.

Backend receives:

```json
{
 "people":7
}
```

---

## Day 7

Create simple dashboard.

Display:

```
Camera

People: 7
```

---

### Week 1 Demo

Show:

```
Camera

↓

YOLO

↓

People Count

↓

Dashboard
```

This alone demonstrates computer vision, backend communication, and a user interface.

---

# WEEK 2 — Build Intelligence

Now the system starts making decisions.

---

## Crowd Density

Instead of:

```
People: 52
```

Display:

```
Density

LOW

MEDIUM

HIGH
```

---

## Occupancy

Example:

```
Capacity

200

Current

164

Occupancy

82%
```

---

## Heat Simulation

Since you won't have real sensors,

simulate:

```
28°C

30°C

31°C

33°C
```

---

## Safety Score

Combine:

* crowd
* occupancy
* heat

Output:

```
Safety Score

92%
```

---

## Charts

Create:

* Crowd history
* Temperature history

---

## Alerts

Example

```
WARNING

High Crowd Density
```

---

### Week 2 Demo

```
Camera

↓

People Count

↓

Density

↓

Safety Score

↓

Charts
```

Now it looks like a real control room.

---

# WEEK 3 — Operations Platform

This is where the project becomes more than an AI demo.

---

## Venue Map

Draw simple stadium.

Example

```
Entrance A

Entrance B

Stage

Medical Tent

Parking
```

---

## Emergency Route

When:

```
High Crowd Density
```

show

```
Vehicle Route
```

---

## Incident Timeline

```
12:01

Crowd High

12:04

Heat Alert

12:08

Risk Normal
```

---

## Event Modes

Create:

```
Football

Concert

Graduation

Conference
```

Each has different thresholds.

---

## Reports

Generate

```
Event Summary

Average Crowd

Maximum Crowd

Highest Temperature

Alerts Generated
```

---

### Week 3 Demo

The lecturer should feel like they're looking at an operations center rather than just a webcam.

---

# WEEK 4 — Polish

Now everything already works.

Spend the last week improving quality.

---

## Better UI

Animations.

Icons.

Better colours.

Professional layout.

---

## Better AI

Improve:

* detection confidence
* tracking

---

## Testing

Test:

* Camera
* AI
* Backend
* Dashboard

---

## Documentation

Finish:

* README
* User Manual
* Technical Report

---

## Presentation

Create:

* slides
* screenshots
* architecture diagram

---

## Practice

Practice the demonstration.

---

# Final Demonstration Flow

Imagine presenting it like this:

---

"I'll begin by opening Astravon Live Arena."

Dashboard appears.

---

"Now I'll activate the live camera."

Camera opens.

---

"The AI is detecting people."

Bounding boxes appear.

---

"As more people enter the frame, the attendance count increases."

Count changes live.

---

"The dashboard calculates crowd density."

Indicator changes from Low to Medium.

---

"Next, I'll simulate rising temperatures."

Temperature changes.

Safety score decreases.

---

"When both density and temperature exceed thresholds, the system generates a warning."

Alert appears.

---

"Finally, I'll switch to the venue map."

Map displays.

---

"The platform recommends a simulated emergency response route."

Route is highlighted.

---

"After the event, I can review the statistics and generated report."

Report appears.

---

# Daily Schedule

If you work consistently, a simple schedule could be:

* **Morning (1–2 hours):** Build one new feature.
* **Afternoon (30–60 minutes):** Test the feature and fix bugs.
* **Evening (30 minutes):** Commit to GitHub, update the project board, and note tomorrow's goal.

This gives you visible progress every day rather than large bursts of work.

---

# How This Fits Your Coursework

One advantage of Astravon Live Arena is that it naturally incorporates the subjects you're studying:

| Course                          | Where it appears in the project                                                   |
| ------------------------------- | --------------------------------------------------------------------------------- |
| Computers in Perspective        | Overall system architecture and real-world application                            |
| IT Hardware                     | Webcam as the input device and discussion of camera hardware                      |
| IT Software                     | Python, FastAPI, HTML/CSS/JavaScript, OpenCV, YOLO                                |
| Number Systems & Character Sets | Representation of image data, RGB pixel values, data encoding, JSON               |
| Computer Networks               | Communication between frontend, backend, and AI using HTTP/WebSockets             |
| Storage & I/O                   | Reading camera frames, storing event statistics in PostgreSQL                     |
| Ethics in Computing             | Privacy, avoiding facial recognition, human oversight of AI decisions             |
| Introduction to the Internet    | Browser-based dashboard, REST APIs, local or cloud deployment                     |
| Information Systems             | Integrating people, processes, data, and technology into one operational platform |

---

## Why this roadmap reduces risk

The most important design choice is that **every week ends with a complete, demonstrable increment**:

* **Week 1:** A working AI-powered people counter.
* **Week 2:** A decision-support dashboard with analytics.
* **Week 3:** An event operations platform with maps and alerts.
* **Week 4:** A polished, documented prototype ready for presentation.

If unexpected problems arise, you still have a working project from the previous week. That makes it much less likely you'll reach the final week with an unfinished system.


astravon-live-arena/
│
├── README.md                          # Project overview
├── LICENSE                            # License
├── CONTRIBUTING.md                    # Contribution guidelines
├── PROJECT_PLAN.md                    # Project roadmap
├── CHANGELOG.md                       # Version history
├── .gitignore
├── .env.example                       # Example environment variables
├── docker-compose.yml                 # Optional deployment
│
├── docs/                              # Documentation
│   │
│   ├── architecture.md
│   ├── workflow.md
│   ├── setup.md
│   ├── api.md
│   ├── database.md
│   ├── ai_engine.md
│   ├── presentation.md
│   ├── testing.md
│   └── screenshots/
│
├── frontend/                          # Dashboard
│   │
│   ├── index.html
│   ├── package.json                   # (optional if using npm)
│   │
│   ├── assets/
│   │   ├── images/
│   │   ├── icons/
│   │   ├── fonts/
│   │   └── videos/
│   │
│   ├── css/
│   │   ├── variables.css
│   │   ├── layout.css
│   │   ├── dashboard.css
│   │   ├── components.css
│   │   └── responsive.css
│   │
│   ├── js/
│   │   ├── app.js
│   │   ├── api.js
│   │   ├── websocket.js
│   │   ├── dashboard.js
│   │   ├── charts.js
│   │   ├── map.js
│   │   ├── alerts.js
│   │   ├── event_modes.js
│   │   └── utils.js
│   │
│   ├── components/
│   │   ├── navbar.js
│   │   ├── sidebar.js
│   │   ├── statistics.js
│   │   ├── camera_panel.js
│   │   ├── alert_panel.js
│   │   └── footer.js
│   │
│   └── pages/
│       ├── dashboard.html
│       ├── reports.html
│       ├── settings.html
│       └── about.html
│
├── backend/
│   │
│   ├── requirements.txt
│   ├── main.py
│   ├── config.py
│   │
│   ├── api/
│   │   ├── routes.py
│   │   ├── websocket.py
│   │   ├── alerts.py
│   │   ├── statistics.py
│   │   ├── routes/
│   │   │   └──routes.py
│   │   └── reports.py
│   │
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── event_service.py
│   │   ├── route_service.py
│   │   └── report_service.py
│   │
│   ├── models/
│   │   ├── event.py
│   │   ├── statistics.py
│   │   ├── alert.py
│   │   └── report.py
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── logging.py
│   │   ├── exception_handler.py
│   │   └── cors.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── common.py
│   │   ├── detection.py
│   │   ├── event.py
│   │   ├── statistics.py
│   │   ├── alert.py
│   │   ├── report.py
│   │   └── route.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   └── session.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   ├── responses.py
│   │   ├── validators.py
│   │   ├── helpers.py
│   │   └── logger.py
│   │
│   └── tests/
│       ├── __init__.py
│       ├── test_routes.py
│       ├── test_ai_service.py
│       ├── test_event_service.py
│       ├── test_report_service.py
│       └── test_statistics.py
│
├── ai_engine/
│   │
│   ├── README.md
│   ├── requirements.txt
│   ├── main.py
│   ├── config.py
│   ├── constants.py
│   │
│   ├── models/
│   │   │
│   │   ├── yolov_model/
│   │   │   ├── best.pt # YOLO model
│   │   │   ├── labels.txt # COCO class labels
│   │   │   └── loader.py
│   │   │
│   │   └── cache/
│   │
│   ├── vision/
│   │   ├── camera.py # Represents one camera
│   │   ├── camera_manager.py # Handles multiple cameras
│   │   ├── stream.py # Reads frames continuously
│   │   ├── detector.py # YOLO detection
│   │   ├── tracker.py # ByteTrack tracking
│   │   ├── pipeline.py # connects camera -> YOLO -> tracking
│   │   ├── preprocessing.py
│   │   ├── calibration.py
│   │   ├── drawing.py
│   │   └── zones.py
│   │
│   ├── crowd/
│   │   ├── counter.py
│   │   ├── density.py
│   │   ├── occupancy.py
│   │   ├── movement.py
│   │   ├── congestion.py
│   │   ├── statistics.py
│   │   └── trends.py
│   │
│   ├── heat/
│   │   ├── simulator.py
│   │   ├── temperature.py
│   │   ├── humidity.py
│   │   ├── heat_index.py
│   │   └── alerts.py
│   │
│   ├── risk/
│   │   ├── analyzer.py
│   │   ├── scoring.py
│   │   ├── thresholds.py
│   │   ├── predictor.py
│   │   ├── severity.py
│   │   └── recommendations.py
│   │
│   ├── simulation/
│   │   ├── event_simulator.py
│   │   ├── fake_temperature.py
│   │   ├── crowd_generator.py
│   │   └── incident_generator.py
│   │
│   ├── api/
│   │   ├── output.py
│   │   ├── schemas.py
│   │   ├── websocket_client.py
│   │   └── http_client.py
│   │
│   ├── analytics/
│   │   ├── metrics.py
│   │   ├── logger.py
│   │   └── reports.py
│   │
│   ├── utils/
│   │   ├── helpers.py
│   │   ├── validators.py
│   │   ├── logger.py
│   │   └── math_utils.py
│   │
│   ├── configs/
│   │   ├── ai.yaml
│   │   ├── camera.yaml
│   │   └── risk.yaml
│   │
│   ├── assets/
│   │   ├── sample_images/
│   │   ├── sample_videos/
│   │   └── demo_data/
│   │
│   ├── outputs/
│   │   ├── processed_frames/
│   │   ├── reports/
│   │   └── recordings/
│   │
│   ├── logs/
│   │
│   └── tests/
│
├── database/
│   │
│   ├── schema.sql
│   ├── seed.sql
│   ├── migrations/
│   ├── backups/
│   └── diagrams/
│
├── shared/                           # Shared code
│   │
│   ├── constants.py
│   ├── enums.py
│   ├── dto.py
│   └── validators.py
│
├── scripts/                          # Automation
│   │
│   ├── setup.py
│   ├── start_backend.py
│   ├── start_ai.py
│   ├── start_frontend.py
│   └── reset_database.py
│
├── tests/
│   │
│   ├── integration/
│   ├── system/
│   └── performance/
│
└── presentations/
    │
    ├── proposal/
    ├── mid_demo/
    ├── final_demo/
    └── assets/

1. Documentation
        │
        ▼
2. Backend Foundation
        │
        ▼
3. AI Engine Foundation
        │
        ▼
4. Frontend Dashboard
        │
        ▼
5. AI → Backend Integration
        │
        ▼
6. Backend → Frontend Integration
        │
        ▼
7. Crowd Analytics
        │
        ▼
8. Heat & Risk Analysis
        │
        ▼
9. Reports & Database
        │
        ▼
10. Testing
        │
        ▼
11. Final Presentation

Four-Week Build Order
Week 1 — Minimum Viable Product (MVP)
docs/
backend/
ai_engine/
frontend/

Deliverable:

Live webcam
Person detection
Crowd count
Dashboard displaying the count
Week 2 — Intelligence Layer
crowd/
heat/
risk/
database/

Deliverable:

Crowd density
Occupancy
Heat simulation
Safety score
Database storage
Week 3 — Operations Layer
simulation/
analytics/
reports/
map/
alerts/

Deliverable:

Event modes
Alerts
Reports
Venue map
Emergency routing (simulated)
Week 4 — Production Readiness
tests/
docs/
presentations/

Deliverable:

Fully integrated system
Documentation
Testing
Final presentation
Demo-ready application

"Astravon Live Arena supports distributed camera monitoring. Multiple camera feeds are processed independently, and crowd intelligence is aggregated into a central safety dashboard"

Multi-camera AI processing

You don't want:

Camera 1
   |
 YOLO
   |
 Camera 2
   |
 YOLO

inside one huge loop.

Instead:

Camera 1
 |
Thread 1
 |
YOLO


Camera 2
 |
Thread 2
 |
YOLO


Camera 3
 |
Thread 3
 |
YOLO

Each camera gets its own processing pipeline.

Your AI engine folder is already designed like a production system. For a 4-week MVP, do **not** start by creating every file. Start from the **core pipeline**:

```
Camera → OpenCV → YOLO → ByteTrack → Crowd Analysis → Backend
```

Everything else can connect later.

The correct development order is:

---

# Phase 1 — Create the AI Engine foundation

First create the package structure:

```
ai_engine/
│
├── main.py
├── config.py
├── constants.py
├── requirements.txt
│
├── models/
│   └── yolov_model/
│       └── loader.py
│
├── vision/
│   ├── camera.py
│   ├── stream.py
│   ├── detector.py
│   ├── tracker.py
│   └── pipeline.py
│
├── crowd/
│   ├── counter.py
│   └── density.py
│
├── api/
│   ├── http_client.py
│   └── schemas.py
│
└── tests/
```

Ignore the other folders initially.

---

# Step 1 — Setup requirements.txt

Start with:

```txt
ultralytics
opencv-python
numpy
requests
pydantic
pyyaml
python-dotenv
```

Later add:

```txt
lapx
supervision
```

for tracking.

Install:

```bash
pip install -r requirements.txt
```

---

# Step 2 — Test YOLO first

Create:

```
models/yolov_model/loader.py
```

Purpose:

Load your AI model once.

```python
from ultralytics import YOLO


class YOLOLoader:

    def __init__(self):

        self.model = YOLO(
            "yolov8n.pt"
        )


    def get_model(self):

        return self.model
```

Test:

```python
from models.yolov_model.loader import YOLOLoader


model = YOLOLoader().get_model()

print(model)
```

If this works, your AI foundation is alive.

---

# Step 3 — Create camera input

`vision/camera.py`

Purpose:

Represent one camera.

```python
class Camera:

    def __init__(
        self,
        camera_id,
        source,
        location
    ):

        self.camera_id = camera_id
        self.source = source
        self.location = location
```

Example:

```python
camera = Camera(
    1,
    "video.mp4",
    "Main Entrance"
)
```

---

# Step 4 — Create video stream reader

`vision/stream.py`

This talks to OpenCV.

```python
import cv2


class VideoStream:


    def __init__(
        self,
        source
    ):

        self.capture = cv2.VideoCapture(
            source
        )


    def read(self):

        success, frame = self.capture.read()

        if success:
            return frame

        return None
```

Now you can read:

* phone stream
* webcam
* mp4 video

---

# Step 5 — Connect YOLO detection

`vision/detector.py`

```python
class Detector:


    def __init__(
        self,
        model
    ):

        self.model = model


    def detect(
        self,
        frame
    ):

        results = self.model(
            frame
        )

        return results
```

---

# Step 6 — Create the pipeline

This is the brain.

`vision/pipeline.py`

```python
class VisionPipeline:


    def __init__(
        self,
        stream,
        detector
    ):

        self.stream = stream
        self.detector = detector


    def run(self):

        while True:

            frame = self.stream.read()

            if frame is None:
                break


            results = self.detector.detect(
                frame
            )


            print(results)
```

Flow:

```
Camera
  |
Stream
  |
Detector
  |
YOLO
```

---

# Step 7 — Add people counting

`crowd/counter.py`

Start simple:

```python
class CrowdCounter:


    def count(
        self,
        results
    ):

        people = 0


        for result in results:

            for box in result.boxes:

                cls = int(
                    box.cls[0]
                )

                if cls == 0:
                    people += 1


        return people
```

COCO:

```
class 0 = person
```

---

# Step 8 — Main entry point

`main.py`

This starts everything.

```python
from models.yolov_model.loader import YOLOLoader

from vision.stream import VideoStream
from vision.detector import Detector
from vision.pipeline import VisionPipeline



model = YOLOLoader().get_model()


stream = VideoStream(
    "assets/sample_videos/test.mp4"
)


detector = Detector(
    model
)


pipeline = VisionPipeline(
    stream,
    detector
)


pipeline.run()
```

Run:

```bash
python main.py
```

Expected:

```
YOLO loaded

Frame received

Detection results...

```

---

# Phase 2 — Add multiple cameras

After one camera works:

Create:

```
vision/camera_manager.py
```

Example:

```python
class CameraManager:


    def __init__(self):

        self.cameras=[]


    def add(
        self,
        camera
    ):

        self.cameras.append(camera)


    def get_all(self):

        return self.cameras
```

Then:

```
Camera 1
   |
Pipeline 1


Camera 2
   |
Pipeline 2
```

---

# Phase 3 — Add ByteTrack

Only after detection works.

Pipeline becomes:

```
OpenCV
  |
YOLO
  |
ByteTrack
  |
Person ID
  |
Crowd counting
```

---

# Phase 4 — Connect to your completed backend

Your backend already has:

```
POST /api/v1/ai/detection
```

The AI engine sends:

```json
{
 "camera_id":1,
 "people_count":45,
 "density":"Medium",
 "risk_score":30
}
```

using:

```
api/http_client.py
```

---

## Your first milestone should be:

Do not think about heat, risk, reports, analytics yet.

Your first success condition:

> "I can give Astravon Live Arena a phone video, and it returns the number of people detected."

Once that works, everything else becomes connecting modules.

Your backend is already ready. The AI engine now only needs to become the **data generator**.


For the **Astravon Live Arena AI Engine MVP**, install the core computer vision and integration libraries first.

Run this inside your `ai_engine` environment:

```bash
pip install ultralytics opencv-python numpy requests pydantic pyyaml python-dotenv
```

These cover:

| Library         | Purpose                                        |
| --------------- | ---------------------------------------------- |
| `ultralytics`   | YOLOv8/YOLO11 object detection                 |
| `opencv-python` | Camera feeds, video processing, frame handling |
| `numpy`         | Image/frame mathematical operations            |
| `requests`      | Sending AI results to your FastAPI backend     |
| `pydantic`      | Data validation schemas                        |
| `pyyaml`        | Reading AI/camera/risk configuration files     |
| `python-dotenv` | Environment variables                          |

---

For tracking with **ByteTrack**, install:

```bash
pip install supervision
```

`supervision` provides easy integration with ByteTrack.

---

For better video handling:

```bash
pip install av imageio
```

Useful for:

* video streams
* frame extraction
* additional formats

---

For testing:

```bash
pip install pytest pytest-asyncio
```

---

For development/debugging:

```bash
pip install tqdm matplotlib
```

Useful for:

* progress bars
* visualizing detections
* testing AI outputs

---

Your complete initial `requirements.txt` could be:

```txt
ultralytics
opencv-python
numpy

supervision

requests
pydantic
pyyaml
python-dotenv

pytest
pytest-asyncio

tqdm
matplotlib

av
imageio
```

Then install everything with:

```bash
pip install -r requirements.txt
```

---

For your first AI milestone, you only need:

```bash
pip install ultralytics opencv-python numpy
```

That is enough to achieve:

```
Phone Camera
      ↓
OpenCV
      ↓
YOLO
      ↓
Person Detection
      ↓
People Count
```

Then add ByteTrack and backend communication after detection is working.


I actually think you're at a good milestone to stop adding features and strengthen the architecture before moving to multiple cameras. Looking at everything we've built, I'd prioritize it like this:

---

# Phase 1 — Stabilize the Dashboard (Do this now)

**Priority: Critical**

Before touching the AI engine, make the frontend and backend behave like a professional monitoring system.

## 1. Fix page navigation ⭐⭐⭐⭐⭐

This should be your first task.

Right now you are loading HTML like:

```javascript
await fetch(`pages/${page}.html`)
```

then replacing

```html
<div id="mainContent"></div>
```

with new HTML.

The problem is:

* components are recreated
* event listeners disappear
* WebSocket callbacks still point to old DOM nodes
* charts and maps are destroyed
* camera panel is recreated

This is why navigation feels fragile.

### Better architecture

```
App
│
├── Navbar
├── Sidebar
├── Footer
│
├── Router
│
├── Dashboard Page
├── Reports Page
├── Settings Page
└── About Page
```

Instead of replacing the entire page, keep all JS modules alive.

Only replace the content area.

Even better:

```
Dashboard
    hide()

Reports
    show()

Settings
    show()
```

instead of recreating them.

That alone will remove many subtle bugs.

---

## 2. Create a global State Manager ⭐⭐⭐⭐⭐

Instead of

```
Statistics Component

Camera Component

Alerts Component

Charts Component
```

all receiving websocket messages independently...

have

```
WebSocket
      │
      ▼
 State Manager
      │
 ├───────────────┐
 ▼               ▼
Camera       Statistics
 ▼               ▼
Charts       Alerts
```

Example

```
LiveState

statistics

frame

alerts

connection

system

camera
```

Every component subscribes to state changes.

This becomes extremely useful once you have:

* multiple cameras
* recording
* playback
* analytics

---

## 3. System Integrity Card ⭐⭐⭐⭐☆

Instead of fake

```
Backend Offline

AI Offline
```

show real values.

```
✔ Backend

✔ WebSocket

✔ AI Engine

✔ Camera

✔ Statistics

✔ Alerts

Last update
```

---

## 4. Improve Camera Panel ⭐⭐⭐⭐☆

I'd add

```
Resolution

FPS

Latency

Frames Received

Dropped Frames

Last Frame
```

When debugging streaming, these are invaluable.

---

# Phase 2 — Improve the Backend

Once the UI is stable...

---

## Event Bus

Instead of

```
Pipeline

↓

OutputManager

↓

WebSocket

↓

HTTP
```

I'd have

```
Pipeline

↓

Event Bus

├──────── HTTP
├──────── WebSocket
├──────── Recorder
├──────── Logger
├──────── Database
```

Then adding a recorder later takes minutes.

---

## Live State

You already started.

Expand it.

```
LiveState

latest_frame

latest_statistics

latest_detection

latest_alert

latest_system

latest_route

camera_status

engine_status

backend_status

clients
```

---

## Health Monitor

Every few seconds

```
Camera Alive

AI Alive

Backend Alive

WebSocket Alive

Frame Age

Inference FPS

Memory

CPU
```

Broadcast

```
type

system
```

---

# Phase 3 — AI Engine

Only after everything above.

Then you can improve

* YOLO
* ByteTrack
* Heatmaps
* Pose estimation
* Violence detection
* Crowd flow
* Route prediction

without touching the frontend.

---

# Phase 4 — Multiple Cameras

This is where your current architecture will pay off.

Instead of

```
frame
```

everything becomes

```
camera_id

frame

statistics

alerts

tracks
```

Example

```json
{
    "type":"frame",

    "camera":"gate_01",

    "data":{

        "frame":"...",

        "fps":14.3
    }
}
```

Then the frontend simply creates

```
CameraPanel(camera_id)
```

No rewrites.

---

# What I would do tomorrow

If I were developing Astravon Live Arena, my order would be:

1. ✅ Fix navigation so pages don't recreate components.
2. ✅ Build a centralized frontend `StateManager`.
3. ✅ Add a live System Integrity panel (real backend, AI, WebSocket, camera status).
4. ✅ Clean up the WebSocket protocol so every message follows the same `{type, data}` structure.
5. ✅ Refactor the backend into an event-driven architecture with `LiveState`.
6. 🚀 Then return to the AI engine and improve detection accuracy, tracking, and performance.

This sequence minimizes rework. By stabilizing the UI and communication layers now, you'll be able to upgrade the AI engine—and later add multiple cameras—without repeatedly modifying the frontend. Given the direction of Astravon Live Arena, I think investing in the navigation and state architecture first will save you considerably more time than jumping straight into AI enhancements.


backend/
│
├── requirements.txt
├── main.py
├── config.py
│
├── api/
│   ├── routes.py
│   ├── websocket.py
│   ├── alerts.py
│   ├── statistics.py
│   ├── reports.py
│   └── routes/
│       └── routes.py
│
├── services/
│   ├── ai_service.py
│   ├── camera_service.py          ← NEW
│   ├── event_service.py
│   ├── notification_service.py    ← NEW
│   ├── route_service.py
│   └── report_service.py
│
├── managers/
│   ├── camera_manager.py          ← NEW
│   ├── stream_manager.py          ← NEW
│   ├── statistics_manager.py      ← NEW
│   ├── alert_manager.py           ← NEW
│   └── websocket_manager.py       ← NEW
│
├── cache/
│   ├── frame_cache.py             ← NEW
│   ├── statistics_cache.py        ← NEW
│   └── alert_cache.py             ← NEW
│
├── storage/
│   ├── json_storage.py            ← NEW
│   └── archive_storage.py         ← NEW
│
├── models/
│   ├── camera.py                  ← NEW
│   ├── event.py
│   ├── statistics.py
│   ├── alert.py
│   └── report.py
│
├── middleware/
│   ├── logging.py
│   ├── exception_handler.py
│   └── cors.py
│
├── schemas/
│   ├── camera.py                  ← NEW
│   ├── detection.py
│   ├── event.py
│   ├── statistics.py
│   ├── alert.py
│   ├── report.py
│   └── route.py
│
├── database/
│   ├── connection.py
│   └── session.py
│
└── utils/
    ├── constants.py
    ├── helpers.py
    ├── logger.py
    ├── responses.py
    └── validators.py


    I actually think this is the perfect time to redesign the frontend. Your backend has evolved from a simple detection pipeline into a **real-time command center**. The frontend should reflect that evolution.

Your original frontend structure is good, but it still resembles a standard dashboard. The backend now supports:

* Multi-camera streaming
* Real-time WebSocket updates
* Person ReID
* Weather integration
* Risk analysis
* Congestion analysis
* Occupancy
* Crowd trends
* Statistics
* Alerts
* Future emergency response

The UI should expose those capabilities.

---

# Proposed Astravon Live Arena v2 Dashboard

```
frontend/
│
├── index.html
│
├── assets/
│   ├── images/
│   ├── icons/
│   ├── fonts/
│   ├── sounds/
│   ├── animations/
│   └── videos/
│
├── css/
│   ├── variables.css
│   ├── global.css
│   ├── layout.css
│   ├── animations.css
│   ├── dashboard.css
│   ├── camera.css
│   ├── analytics.css
│   ├── maps.css
│   ├── alerts.css
│   ├── reports.css
│   ├── settings.css
│   └── responsive.css
│
├── js/
│   ├── app.js
│   ├── api.js
│   ├── websocket.js
│   ├── router.js
│   ├── state.js
│   ├── event_bus.js
│   ├── utils.js
│   └── constants.js
│
├── components/
│   │
│   ├── layout/
│   │   ├── navbar.js
│   │   ├── sidebar.js
│   │   ├── footer.js
│   │   └── notifications.js
│   │
│   ├── cameras/
│   │   ├── camera_grid.js
│   │   ├── camera_card.js
│   │   ├── camera_toolbar.js
│   │   └── fullscreen.js
│   │
│   ├── analytics/
│   │   ├── statistics.js
│   │   ├── charts.js
│   │   ├── density.js
│   │   ├── occupancy.js
│   │   ├── congestion.js
│   │   ├── movement.js
│   │   ├── weather.js
│   │   ├── heat_index.js
│   │   └── trends.js
│   │
│   ├── risk/
│   │   ├── risk_gauge.js
│   │   ├── alerts.js
│   │   ├── emergency.js
│   │   └── evacuation.js
│   │
│   ├── maps/
│   │   ├── venue_map.js
│   │   ├── heatmap.js
│   │   ├── routes.js
│   │   └── gps.js
│   │
│   ├── people/
│   │   ├── reid.js
│   │   ├── tracking.js
│   │   ├── identities.js
│   │   └── history.js
│   │
│   └── reports/
│       ├── report_table.js
│       ├── report_export.js
│       └── report_filters.js
│
├── pages/
│   ├── dashboard.html
│   ├── analytics.html
│   ├── cameras.html
│   ├── map.html
│   ├── reports.html
│   ├── settings.html
│   └── about.html
│
└── workers/
    ├── websocket_worker.js
    └── chart_worker.js

css/
│
├── variables.css          ← Colors, spacing, typography, shadows, z-index
│
├── global.css             ← Reset, body, links, typography, scrollbar, utilities
│
├── layout.css             ← App shell
│                           Navbar
│                           Sidebar
│                           Footer
│                           Main layout
│                           Content wrappers
│
├── animations.css         ← Keyframes, transitions, loading animations
│
├── components.css         ← Buttons
│                           Cards
│                           Forms
│                           Tables
│                           Badges
│                           Modals
│                           Toasts
│                           Dropdowns
│                           Progress bars
│                           Reusable widgets
│
├── dashboard.css          ← Dashboard homepage ONLY
│                           Dashboard overview
│                           Live statistics
│                           Dashboard cards
│                           Dashboard widgets
│
├── monitoring.css         ← Camera page
│                           Analytics page
│                           Maps page
│                           Live monitoring widgets
│                           Camera grids
│                           AI metrics
│                           Heatmaps
│                           Charts
│                           Venue maps
│
├── management.css         ← Alerts
│                           Reports
│                           Settings
│                           Tables
│                           Filters
│                           Forms
│                           Logs
│                           Configuration panels
│
├── pages.css              ← About page
│                           Empty states
│                           Generic page headers
│                           Timeline
│                           Documentation layouts
│
└── responsive.css         ← ALL media queries
                            Desktop
                            Laptop
                            Tablet
                            Mobile
```

---

# Dashboard Layout

I'd redesign the dashboard into something that resembles a professional security operations center.

```
┌───────────────────────────────────────────────────────────────┐
│ Astravon Live Arena                               User Status │
├───────────────┬───────────────────────────────────────────────┤
│               │                                               │
│               │        LIVE CAMERA GRID                       │
│               │                                               │
│ Navigation    │   Camera 1     Camera 2     Camera 3          │
│               │                                               │
│ Dashboard     │                                               │
│ Cameras       │                                               │
│ Analytics     │                                               │
│ Risk          │                                               │
│ Map           │                                               │
│ Reports       │                                               │
│ Settings      │                                               │
├───────────────┼───────────────────────────────────────────────┤
│ Risk Gauge    │ People      Density      Occupancy            │
│               │                                               │
│ Weather       │ Heat Index  Congestion   Movement             │
│               │                                               │
│ Alerts        │ Charts      Trends       Statistics           │
└───────────────┴───────────────────────────────────────────────┘
```

---

# WebSocket Channels

Your backend already sends multiple kinds of messages, so the frontend should subscribe to each separately.

```
Frame Stream

↓

Camera Component

Detection Stream

↓

Detection Overlay

Statistics Stream

↓

Statistics Cards

Alert Stream

↓

Alert Panel

Risk Stream

↓

Risk Gauge

Weather Stream

↓

Weather Widget
```

This keeps the UI modular and makes it easier to extend later.

---

# Components to Add

Since your backend now calculates these, surface them in the UI:

* Live Risk Gauge (green → yellow → red)
* Crowd Density Meter
* Occupancy Gauge
* Congestion Gauge
* Heat Index Card
* Weather Card
* Camera Health Indicator
* AI Performance (FPS, inference time)
* Global Person ID display
* Recent Alerts panel
* Trend graphs

---

# Presentation Mode

I'd also add a dedicated presentation mode.

Pressing **F11** or a "Presentation" button would:

* Hide developer controls
* Enlarge camera feeds
* Increase font sizes
* Highlight alerts
* Animate metric updates smoothly
* Display the Astravon branding prominently

That makes the system much more engaging during a live demo.

---

## Development priority

Given where your project is now, I'd tackle the frontend in this order:

1. **Core layout** (navbar, sidebar, camera grid, responsive design).
2. **WebSocket integration** (live frames, detections, statistics, alerts).
3. **Analytics widgets** (risk, density, occupancy, weather, congestion).
4. **Charts and trends** (historical data visualization).
5. **Map and emergency views** (heatmaps, routes, future-ready features).
6. **Presentation mode** and final polish (animations, branding, transitions).

At this stage, I'd treat the frontend as an **operations center** rather than a simple dashboard. That design will better showcase the sophistication of the backend you've built and create a much stronger impression during your presentation.


Or, even better, since all five charts follow exactly the same logic, create a single reusable helper.

/*
============================================================
Generic Streaming Chart Update
============================================================
*/

updateStreamingChart(id, value) {

    const chart = this.charts.get(id);

    if (!chart) return;

    chart.data.labels.push("");

    chart.data.datasets[0].data.push(value);

    while (chart.data.labels.length > this.maxHistory) {

        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();

    }

    chart.update();

}

Now every specialized function becomes a one-liner.

updatePeopleChart(value) {

    this.updateStreamingChart(
        "peopleChart",
        value
    );

}

updateDensityChart(value) {

    this.updateStreamingChart(
        "densityChart",
        value
    );

}

updateRiskChart(value) {

    this.updateStreamingChart(
        "riskChart",
        value
    );

}

updateMovementChart(value) {

    this.updateStreamingChart(
        "movementChart",
        value
    );

}

updateOccupancyChart(value) {

    this.updateStreamingChart(
        "occupancyChart",
        value
    );

}