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