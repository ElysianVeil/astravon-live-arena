/*
============================================================
Astravon Live Arena
Frontend Constants

Purpose:
    Central location for application constants.
    Prevents magic strings and duplicated values
    throughout the frontend.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

/*==========================================================
    Application
==========================================================*/

export const APP = Object.freeze({

    NAME: "Astravon Live Arena",

    VERSION: "1.0.0",

    AUTHOR: "House of Astravon",

    COMPANY: "Astravon Technologies"

});

/*==========================================================
    Environment
==========================================================*/

export const ENVIRONMENT = Object.freeze({

    DEVELOPMENT: "development",

    STAGING: "staging",

    PRODUCTION: "production"

});

/*==========================================================
    API
==========================================================*/

export const API = Object.freeze({

    BASE_URL: "http://127.0.0.1:8000",

    VERSION: "/api/v1",

    TIMEOUT: 15000

});

/*==========================================================
    WebSocket
==========================================================*/

export const WEBSOCKET = Object.freeze({

    URL: "ws://127.0.0.1:8000/ws",

    RECONNECT_INTERVAL: 3000,

    MAX_RECONNECT_ATTEMPTS: Infinity

});

/*==========================================================
    WebSocket Events
==========================================================*/

export const SOCKET_EVENTS = Object.freeze({

    FRAME: "frame",

    STATISTICS: "statistics",

    ALERT: "alert",

    DETECTION: "detection",

    EVENT_MODE: "event_mode",

    CONNECTION: "connection",

    ERROR: "error"

});

/*==========================================================
    Pages
==========================================================*/

export const PAGES = Object.freeze({

    DASHBOARD: "dashboard",

    CAMERAS: "cameras",

    ANALYTICS: "analytics",

    MAPS: "map",

    ALERTS: "alerts",

    REPORTS: "reports",

    SETTINGS: "settings",

    ABOUT: "about"

});

/*
==========================================================
Default Page
==========================================================
*/

export const DEFAULT_PAGE = PAGES.DASHBOARD;

/*==========================================================
    Camera
==========================================================*/

export const CAMERA = Object.freeze({

    DEFAULT_COLUMNS: 2,

    MAX_COLUMNS: 4,

    MIN_COLUMNS: 1,

    PLACEHOLDER_IMAGE:
        "assets/images/camera-placeholder.jpg",

    FRAME_FORMAT: "image/jpeg"

});

/*==========================================================
    Camera Status
==========================================================*/

export const CAMERA_STATUS = Object.freeze({

    ONLINE: "online",

    OFFLINE: "offline",

    RECORDING: "recording",

    IDLE: "idle",

    CONNECTING: "connecting"

});

/*==========================================================
    Risk Levels
==========================================================*/

export const RISK = Object.freeze({

    LOW: "Low",

    MEDIUM: "Medium",

    HIGH: "High",

    CRITICAL: "Critical"

});

/*==========================================================
    Alert Levels
==========================================================*/

export const ALERT = Object.freeze({

    INFO: "INFO",

    SUCCESS: "SUCCESS",

    WARNING: "WARNING",

    DANGER: "DANGER",

    CRITICAL: "CRITICAL"

});

/*==========================================================
    Event Modes
==========================================================*/

export const EVENT_MODE = Object.freeze({

    TRAINING: "Training",

    CONCERT: "Concert",

    STADIUM: "Stadium",

    FESTIVAL: "Festival",

    EMERGENCY: "Emergency",

    TESTING: "Testing"

});

/*==========================================================
    Refresh Rates
==========================================================*/

export const REFRESH = Object.freeze({

    CLOCK: 1000,

    DASHBOARD: 5000,

    STATISTICS: 1000,

    MAP: 2000,

    WEATHER: 300000

});

/*==========================================================
    Layout
==========================================================*/

export const LAYOUT = Object.freeze({

    NAVBAR_HEIGHT: 72,

    SIDEBAR_WIDTH: 280,

    FOOTER_HEIGHT: 48

});

/*==========================================================
    Local Storage Keys
==========================================================*/

export const STORAGE = Object.freeze({

    THEME: "astravon_theme",

    SIDEBAR: "astravon_sidebar",

    CAMERA_LAYOUT: "astravon_camera_layout",

    DASHBOARD: "astravon_dashboard",

    TOKEN: "astravon_token"

});

/*==========================================================
    Themes
==========================================================*/

export const THEME = Object.freeze({

    LIGHT: "light",

    DARK: "dark"

});

/*==========================================================
    Map
==========================================================*/

export const MAP = Object.freeze({

    DEFAULT_ZOOM: 16,

    MIN_ZOOM: 8,

    MAX_ZOOM: 22

});

/*==========================================================
    Chart Types
==========================================================*/

export const CHART = Object.freeze({

    LINE: "line",

    BAR: "bar",

    PIE: "pie",

    AREA: "area"

});

/*==========================================================
    Colors
==========================================================*/

export const COLORS = Object.freeze({

    PRIMARY: "#0B1A3A",

    SECONDARY: "#D4AF37",

    SUCCESS: "#22C55E",

    WARNING: "#F59E0B",

    DANGER: "#EF4444",

    INFO: "#3B82F6"

});

/*==========================================================
    Defaults
==========================================================*/

export const DEFAULTS = Object.freeze({

    FPS: 0,

    PEOPLE: 0,

    OCCUPANCY: 0,

    DENSITY: "Low",

    TEMPERATURE: 0,

    HUMIDITY: 0,

    HEAT_INDEX: 0,

    CONFIDENCE: 0,

    PROCESSING_TIME: 0

});

/*==========================================================
    Freeze Everything
==========================================================*/

export default Object.freeze({

    APP,

    ENVIRONMENT,

    API,

    WEBSOCKET,

    SOCKET_EVENTS,

    PAGES,

    CAMERA,

    CAMERA_STATUS,

    RISK,

    ALERT,

    EVENT_MODE,

    REFRESH,

    LAYOUT,

    STORAGE,

    THEME,

    MAP,

    CHART,

    COLORS,

    DEFAULTS

});