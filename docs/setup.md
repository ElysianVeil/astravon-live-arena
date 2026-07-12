# Astravon Live Arena
## Setup Guide

**Version:** 1.0.0

**Project Lead:** Johnpaul Kiwinga

---

# 1. Purpose

This guide explains how to install, configure, and run Astravon Live Arena for development.

By following this guide, a new contributor should be able to clone the repository and have the application running within a few minutes.

---

# 2. System Requirements

## Operating Systems

- Windows 10 / 11
- Ubuntu 22.04+
- macOS 13+

---

## Recommended Hardware

Minimum

- Intel Core i5
- 8 GB RAM
- Webcam
- 5 GB Free Storage

Recommended

- Intel Core i7 / Ryzen 7
- 16 GB RAM
- NVIDIA GPU (optional)
- SSD
- 10 GB Free Storage

---

# 3. Required Software

Install the following before continuing.

## Git

Download

https://git-scm.com/

Verify

```bash
git --version
```

---

## Python

Version

```
Python 3.11+
```

Download

https://www.python.org/

Verify

```bash
python --version
```

---

## PostgreSQL

Download

https://www.postgresql.org/

Verify

```bash
psql --version
```

---

## Visual Studio Code

Download

https://code.visualstudio.com/

Recommended Extensions

- Python
- Pylance
- GitLens
- PostgreSQL
- Error Lens
- Live Server
- Docker (optional)

---

## Node.js (Optional)

Only required if frontend tooling is introduced later.

```bash
node --version
```

---

# 4. Clone Repository

```bash
git clone https://github.com/ElysianVeil/astravon-live-arena.git

cd astravon-live-arena
```

---

# 5. Project Structure

```
astravon-live-arena/

backend/

frontend/

database/

docs/

ai_engine/

tests/
```

---

# 6. Create Virtual Environment

Windows

```powershell
python -m venv .venv
```

Linux/macOS

```bash
python3 -m venv .venv
```

---

# 7. Activate Virtual Environment

Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Windows CMD

```cmd
.venv\Scripts\activate.bat
```

Linux/macOS

```bash
source .venv/bin/activate
```

Successful activation

```
(.venv)
```

appears before your terminal prompt.

---

# 8. Install Python Dependencies

Backend

```bash
cd backend

pip install -r requirements.txt
```

AI Engine

```bash
cd ../ai_engine

pip install -r requirements.txt
```

---

# 9. Install Core Libraries

If requirements are unavailable

```bash
pip install fastapi
pip install uvicorn
pip install ultralytics
pip install opencv-python
pip install numpy
pip install pandas
pip install matplotlib
pip install sqlalchemy
pip install psycopg2-binary
pip install python-dotenv
pip install websockets
```

---

# 10. Environment Variables

Create

```
.env
```

Example

```env
APP_NAME=Astravon Live Arena

DEBUG=True

HOST=127.0.0.1

PORT=8000

DATABASE_URL=postgresql://postgres:password@localhost/astravon_live_arena

AI_HOST=http://127.0.0.1:9000

SECRET_KEY=CHANGE_ME
```

Never commit

```
.env
```

to GitHub.

---

# 11. Database Setup

Create database

```
astravon_live_arena
```

Run

```sql
database/schema.sql
```

Optional

```sql
database/seed.sql
```

Verify

```
Database Created

Tables Created
```

---

# 12. Running the Backend

Navigate

```bash
cd backend
```

Start

```bash
uvicorn main:app --reload
```

Default

```
http://127.0.0.1:8000
```

API Documentation

```
http://127.0.0.1:8000/docs
```

---

# 13. Running the AI Engine

Navigate

```bash
cd ai_engine
```

Run

```bash
python main.py
```

Expected

```
Loading Camera...

Loading YOLO...

Waiting for Frames...
```

---

# 14. Running the Frontend

If using plain HTML

Simply open

```
frontend/index.html
```

Recommended

Use Live Server extension

or

```bash
python -m http.server 5500
```

Open

```
http://localhost:5500
```

---

# 15. Running the Complete System

Start in this order

```
Database

↓

Backend

↓

AI Engine

↓

Frontend
```

System Flow

```
Camera

↓

AI Engine

↓

Backend

↓

Database

↓

Dashboard
```

---

# 16. Verify Installation

Checklist

Backend

```
✓ Running
```

AI Engine

```
✓ Detecting People
```

Frontend

```
✓ Dashboard Visible
```

Database

```
✓ Connected
```

Camera

```
✓ Working
```

---

# 17. Expected Output

Dashboard should display

```
Camera Feed

People Count

Crowd Density

Temperature

Safety Score

Alerts

Charts
```

---

# 18. Running Tests

Backend

```bash
pytest
```

AI

```bash
pytest
```

Expected

```
All Tests Passed
```

---

# 19. Updating Dependencies

```bash
pip install -U -r requirements.txt
```

Generate updated requirements

```bash
pip freeze > requirements.txt
```

---

# 20. Git Workflow

Before starting

```bash
git pull
```

After changes

```bash
git add .

git commit -m "feat: implemented crowd density"

git push
```

---

# 21. Common Problems

## Camera not detected

Check

- Webcam connected
- Webcam permissions
- Camera not used by another application

---

## YOLO model missing

Verify

```
ai_engine/models/yolov_model/
```

contains

```
best.pt
```

or

```
yolov8n.pt
```

---

## Database connection failed

Verify

- PostgreSQL running
- Username
- Password
- Database exists

---

## Port already in use

Use another port

Example

```bash
uvicorn main:app --reload --port 8080
```

---

## Module not found

Install missing package

```bash
pip install package_name
```

---

# 22. Development Checklist

Before committing

- Code formatted
- Tests passed
- Documentation updated
- No debugging code
- No hardcoded passwords
- No unnecessary files

---

# 23. Recommended Development Order

```
Repository

↓

Backend

↓

AI Engine

↓

Frontend

↓

Database

↓

Integration

↓

Testing

↓

Documentation

↓

Presentation
```

---

# 24. First Successful Run

You have successfully completed setup when:

```
✓ Backend starts

✓ Camera opens

✓ YOLO detects people

✓ Dashboard loads

✓ API responds

✓ Database connected

✓ Crowd count displayed
```

---

# 25. Next Steps

After completing setup:

1. Verify the webcam feed.
2. Test person detection.
3. Connect the AI Engine to the backend.
4. Display live statistics on the dashboard.
5. Commit your changes.
6. Update the project board.
7. Continue with the next milestone according to the project plan.

---

**Congratulations!**

Your Astravon Live Arena development environment is now ready. From this point forward, you can begin implementing features, integrating components, and preparing the project for demonstrations and future enhancements.