/*
============================================================
Astravon Live Arena
Application Bootstrap

Purpose:
    Main frontend application responsible for
    initializing every subsystem, coordinating
    communication between modules and managing
    the overall application lifecycle.

Author:
    House of Astravon

Version:
    2.0.0
============================================================
*/

import api from "./api.js";
import WebSocketManager from "./websocket.js";
import router from "./router.js";
import State from "./state.js";
import EventBus from "./event_bus.js";

import {
    APP,
    DEFAULT_PAGE
} from "./constants.js";

import {
    log,
    warn,
    error,
    showLoading,
    hideLoading,
    showToast
} from "./utils.js";

/*
============================================================
Layout
============================================================
*/

import Navbar from "../components/layout/navbar.js";
import Sidebar from "../components/layout/sidebar.js";
import Footer from "../components/layout/footer.js";
import Notifications from "../components/layout/notifications.js";

/*
============================================================
Camera Components
============================================================
*/

import CameraGrid from "../components/cameras/camera_grid.js";
import CameraToolbar from "../components/cameras/camera_toolbar.js";

/*
============================================================
Analytics
============================================================
*/

import statisticsManager from "../components/analytics/statistics.js";
import charts from "../components/analytics/charts.js";
import density from "../components/analytics/density.js";
import Occupancy from "../components/analytics/occupancy.js";
import Congestion from "../components/analytics/congestion.js";
import Movement from "../components/analytics/movement.js";
import Weather from "../components/analytics/weather.js";
import { HeatIndex } from "../components/analytics/heat_index.js";
import Trends from "../components/analytics/trends.js";

/*
============================================================
Risk
============================================================
*/

import riskGauge from "../components/risk/risk_gauge.js";
import alertManager from "../components/risk/alerts.js";
import emergencyManager from "../components/risk/emergency.js";
import evacuationManager from "../components/risk/evacuation.js";

/*
============================================================
Maps
============================================================
*/

import venueMap from "../components/maps/venue_map.js";
import heatmapManager from "../components/maps/heatmap.js";
import Routes from "../components/maps/routes.js";
import pageManager from "./page_manager.js";
import { gpsManager } from "../components/maps/gps.js";

/*
============================================================
People
============================================================
*/

import ReID from "../components/people/reid.js";
import Tracking from "../components/people/tracking.js";
import Identities from "../components/people/identities.js";
import History from "../components/people/history.js";

/*
============================================================
Reports
============================================================
*/

import ReportTable from "../components/reports/report_table.js";
import ReportExport from "../components/reports/report_export.js";
import ReportFilters from "../components/reports/report_filters.js";



/*
============================================================
Application
============================================================
*/

class AstravonLiveArena {

    constructor(dependencies = {}) {

        /*
        ======================================================
        Dependency Injection
        ======================================================
        */

        this.api =
            dependencies.api ??
            api;

        this.websocket =
            dependencies.websocket ??
            new WebSocketManager();

        this.router =
            dependencies.router ??
            router;

        this.pageManager =
            dependencies.pageManager ??
            pageManager;

        this.state =
            dependencies.state ??
            State;

        this.events =
            dependencies.events ??
            EventBus;

        /*
        ======================================================
        Metadata
        ======================================================
        */

        this.name = APP.NAME;

        this.version = APP.VERSION;

        /*
        ======================================================
        Lifecycle
        ======================================================
        */

        this.started = false;

        this.initialized = false;

        this.destroyed = false;

        this.connected = false;

        this.loading = false;

        /*
        ======================================================
        Active Page
        ======================================================
        */

        this.currentPage = DEFAULT_PAGE;

        /*
        ======================================================
        Component Registry
        ======================================================
        */

        this.components = new Map();

        /*
        ======================================================
        Service Registry
        ======================================================
        */

        this.services = new Map();

        /*
        ======================================================
        Module Registry
        ======================================================
        */

        this.modules = new Map();

        /*
        ======================================================
        Register Components
        ======================================================
        */

        this.registerComponent("navbar", new Navbar());

        this.registerComponent("sidebar", new Sidebar());

        this.registerComponent("footer", new Footer());

        this.registerComponent("notifications", new Notifications());

        this.registerComponent("cameraGrid", new CameraGrid());

        this.registerComponent("cameraToolbar", new CameraToolbar());

        this.registerComponent("statistics", statisticsManager);

        this.registerComponent("charts", charts);

        this.registerComponent("density", density);

        this.registerComponent("occupancy", Occupancy);

        this.registerComponent("congestion", Congestion);

        this.registerComponent("movement", Movement);

        this.registerComponent("weather", Weather);

        this.registerComponent("heatIndex", new HeatIndex());

        this.registerComponent("trends", Trends);

        this.registerComponent("riskGauge", riskGauge);

        this.registerComponent("alerts", alertManager);

        this.registerComponent("emergency", emergencyManager);

        this.registerComponent("evacuation", evacuationManager);

        this.registerComponent("venueMap", venueMap);

        this.registerComponent("heatMap", heatmapManager);

        this.registerComponent("routes", Routes);

        this.registerComponent("pageManager", pageManager);

        this.registerComponent("gps", gpsManager);

        this.registerComponent("reid", new ReID());

        this.registerComponent("tracking", Tracking);

        this.registerComponent("identities", Identities);

        this.registerComponent("history", History);

        this.registerComponent("reportTable", new ReportTable());

        this.registerComponent("reportExport", new ReportExport());

        this.registerComponent("reportFilters", new ReportFilters());

        /*
        ======================================================
        Register Services
        ======================================================
        */

        this.registerService("api", this.api);

        this.registerService("websocket", this.websocket);

        this.registerService("router", this.router);

        this.registerService("pageManager", this.pageManager);

        this.registerService("state", this.state);

        this.registerService("events", this.events);

    }

    /*
    ==========================================================
    Component Registration
    ==========================================================
    */

    registerComponent(name, component) {

        this.components.set(name, component);

        return component;

    }

    getComponent(name) {

        return this.components.get(name);

    }

    /*
    ==========================================================
    Service Registration
    ==========================================================
    */

    registerService(name, service) {

        this.services.set(name, service);

        return service;

    }

    getService(name) {

        return this.services.get(name);

    }

    /*
    ==========================================================
    Module Registration
    ==========================================================
    */

    registerModule(name, module) {

        this.modules.set(name, module);

        return module;

    }

    getModule(name) {

        return this.modules.get(name);

    }

    /*
    ==========================================================
    Initialize
    ==========================================================
    */

    async initialize() {

        if (this.initialized) {

            return;

        }

        this.loading = true;

        showLoading("Initializing Live Arena...");

        log(`${this.name} ${this.version}`);

        this.initialized = true;

    }

        /*
    ==========================================================
    Startup
    ==========================================================
    */

    async start() {

        if (this.started) {

            warn("Application already started.");

            return;

        }

        try {

            /*
            --------------------------------------------
            Bootstrap
            --------------------------------------------
            */

            await this.bootstrap();

            /*
            --------------------------------------------
            Layout
            --------------------------------------------
            */

            await this.initializeLayout();

            /*
            --------------------------------------------
            Router
            --------------------------------------------
            */

            await this.initializeRouter();

            this.events.on(
                "page:loaded",
                async (page) => {

                    console.log("Initializing:", page);
                    await this.initializePage(page);

                }
            );

            /*
            --------------------------------------------
            Global State
            --------------------------------------------
            */

            await this.initializeState();

            /*
            --------------------------------------------
            Event Bus
            --------------------------------------------
            */

            await this.initializeEvents();

            /*
            --------------------------------------------
            API
            --------------------------------------------
            */

            await this.initializeAPI();

            /*
            --------------------------------------------
            Feature Modules
            --------------------------------------------
            */

            // await this.initializeModules();

            /*
            --------------------------------------------
            Default Page
            --------------------------------------------
            */

            const page =
                await this.pageManager.load(DEFAULT_PAGE);

            await this.initializePage(page);

            this.started = true;

            this.loading = false;

            hideLoading();

            showToast(

                "Astravon Live Arena Ready",

                "success"

            );

            log("Application Started.");

        }

        catch (exception) {

            error(

                "Startup Failed",

                exception

            );

            hideLoading();

            showToast(

                "Startup Failed",

                "error"

            );

            throw exception;

        }

    }

    /*
    ==========================================================
    Bootstrap
    ==========================================================
    */

    async bootstrap() {

        this.state.set(

            "application",

            {

                name: this.name,

                version: this.version,

                started: false,

                connected: false,

                page: DEFAULT_PAGE

            }

        );

        log("Bootstrap Complete.");

    }

    /*
    ==========================================================
    Layout
    ==========================================================
    */

    async initializeLayout() {

        for (

            const component

            of

            [

                "navbar",

                "sidebar",

                "footer",

                "notifications"

            ]

        ) {

            const instance =

                this.getComponent(

                    component

                );

            if (

                instance?.initialize

            ) {

                await instance.initialize();

            }

        }

        log(

            "Layout Initialized."

        );

    }

    /*
    ==========================================================
    Router
    ==========================================================
    */

    async initializeRouter() {

        this.router.initialize();

        this.router.beforeEach(

            async (from, to) => {

                this.state.set(

                    "navigation.loading",

                    true

                );

            }

        );

        this.router.afterEach(

            async (from, to) => {

                this.currentPage = to;

                this.state.set(

                    "application.page",

                    to

                );

                this.state.set(

                    "navigation.loading",

                    false

                );

                log(

                    `Page Loaded: ${to}`

                );

            }

        );

        log(

            "Router Initialized."

        );

    }

    /*
    ==========================================================
    State
    ==========================================================
    */

    async initializeState() {

        this.state.set(

            "connection",

            {

                websocket: false,

                backend: false

            }

        );

        this.state.set(

            "statistics",

            {}

        );

        this.state.set(

            "alerts",

            []

        );

        this.state.set(

            "cameras",

            []

        );

        this.state.set(

            "reports",

            []

        );

        this.state.subscribe(

            "application.page",

            page => {

                this.currentPage = page;

            }

        );

        log(

            "State Initialized."

        );

    }

    /*
    ==========================================================
    Event Bus
    ==========================================================
    */

    async initializeEvents() {

        this.events.on(

            "application:start",

            () => {

                log(

                    "Application Event Received"

                );

            }

        );

        this.events.on(

            "application:error",

            errorMessage => {

                showToast(

                    errorMessage,

                    "error"

                );

            }

        );

        this.events.on(

            "page:changed",

            page => {

                this.state.set(

                    "application.page",

                    page

                );

            }

        );

        log(

            "Event Bus Initialized."

        );

    }

    /*
    ==========================================================
    API
    ==========================================================
    */

    async initializeAPI() {

        try {

            const health =

                await this.api.health();

            this.state.set(

                "connection.backend",

                true

            );

            this.state.set(

                "backend.health",

                health

            );

            this.events.emit(

                "backend:connected",

                health

            );

            log(

                "Backend Online."

            );

        }

        catch (exception) {

            this.state.set(

                "connection.backend",

                false

            );

            this.events.emit(

                "backend:offline"

            );

            warn(

                "Backend Offline."

            );

        }

    }

    /*
    ==========================================================
    Feature Modules
    ==========================================================
    */

    async initializeModules() {

        for (

            const [

                name,

                component

            ]

            of

            this.components

        ) {

            if (

                component.initialize

            ) {

                await component.initialize();

            }

        }

        log(

            "Feature Modules Initialized."

        );

    }

        /*
    ==========================================================
    WebSocket
    ==========================================================
    */

    async initializeWebSocket() {

        this.websocket.onOpen(() => {

            this.connected = true;

            this.state.set(
                "connection.websocket",
                true
            );

            this.state.set(
                "application.connected",
                true
            );

            this.events.emit(
                "websocket:connected"
            );

            this.getComponent("navbar")?.setConnected?.();

            this.getComponent("footer")?.setWebSocketStatus?.(
                "Connected"
            );

            log("WebSocket Connected.");

        });

        this.websocket.onClose(() => {

            this.connected = false;

            this.state.set(
                "connection.websocket",
                false
            );

            this.state.set(
                "application.connected",
                false
            );

            this.events.emit(
                "websocket:disconnected"
            );

            this.getComponent("navbar")?.setDisconnected?.();

            this.getComponent("footer")?.setWebSocketStatus?.(
                "Disconnected"
            );

            warn("WebSocket Disconnected.");

        });

        this.websocket.onError(error => {

            this.events.emit(
                "websocket:error",
                error
            );

            console.error(error);

        });

        this.websocket.on(
            "statistics",
            statistics => {

                const data =
                    statistics.data ?? statistics;

                console.log("Statistics packet received");
                console.log(data);

                this.state.set(
                    "statistics",
                    data
                );

                this.updateDashboardOverview(data);
                this.updateSystemStatus(data);

                this.getComponent("statistics")
                    ?.update(data);

                /*
                ------------------------------------------------------
                ReID Identities
                ------------------------------------------------------
                */

                const identities =
                    data.performance?.identity_database?.identities;

                console.log(
                    "Identity Database:",
                    data.performance?.identity_database
                );

                console.log(
                    "Identities:",
                    data.performance?.identity_database?.identities
                );

                if (identities) {

                    const manager =
                        this.getComponent("identities");

                    console.log(manager);

                    identities.forEach(identity => {

                        manager.update({

                            id: String(identity.global_id),

                            name: `Person ${identity.global_id}`,

                            camera: identity.camera_id,

                            confidence: identity.confidence,

                            firstSeen: identity.first_seen,

                            lastSeen: identity.last_seen,

                            visits: identity.appearances,

                            status: "Active"

                        });

                    });

                    const container = document.getElementById("identityContainer");

                    console.log(container);

                    manager.render(container);

                }

                const engine = data.engine;

                const container =
                    document.getElementById("systemStatus");

                if (container && engine) {

                    container.innerHTML = `
                        <div><strong>Status:</strong> ${engine.status}</div>
                        <div><strong> System Name:</strong> ${engine.name}</div>
                        <div><strong>Uptime:</strong> ${engine.uptime}</div>
                        <div><strong>Version:</strong> ${engine.version}</div>
                    `;

                }

                this.events.emit(
                    "statistics:updated",
                    data
                );

            }
        );
        /*
        ------------------------------------------------------
        Camera Frames
        ------------------------------------------------------
        */

        this.websocket.on(
            "frame",
            message => {

                const frame = message;

                this.getComponent("cameraGrid")
                    ?.updateFrame(
                        frame.camera_id,
                        frame
                    );

                if(frame.statistics){

                    this.getComponent("cameraGrid")
                        ?.updateStatistics(
                            frame.camera_id,
                            frame.statistics
                        );

                }

                this.getComponent("cameraGrid")
                    ?.updateInfo(
                        frame.camera_id,
                        {
                            fps: frame.fps,
                            resolution:
                                `${frame.width}×${frame.height}`,
                            people: frame.people,
                            risk: frame.risk
                        }
                    );

                this.events.emit(
                    "camera:frame",
                    frame
                );

                // NEW
                if (frame.statistics) {

                    this.state.set(
                        "statistics",
                        frame.statistics
                    );

                    this.updateDashboardOverview(
                        frame.statistics
                    );

                    this.getComponent("statistics")
                        ?.update(
                            frame.statistics
                        );


                    this.events.emit(
                        "statistics:updated",
                        frame.statistics
                    );

                }

            }
        );


        /*
        ------------------------------------------------------
        Camera Status
        ------------------------------------------------------
        */

        this.websocket.on(
            "camera_status",
            status => {

                if (status.connected) {

                    this.getComponent("cameraGrid")
                        ?.connectCamera(
                            status.camera_id
                        );

                }
                else {

                    this.getComponent("cameraGrid")
                        ?.disconnectCamera(
                            status.camera_id
                        );

                }

            }
        );

        /*
        ------------------------------------------------------
        Alerts
        ------------------------------------------------------
        */

        this.websocket.on(
            "alert",
            alert => {

                const alerts =
                    this.state.get("alerts") ?? [];

                alerts.unshift(alert);

                this.state.set(
                    "alerts",
                    alerts
                );

                const manager =
                    this.getComponent("alerts");

                manager.add(alert);

                this.events.emit(
                    "alert:received",
                    alert
                );

            }
        );

        /*
        ------------------------------------------------------
        Weather
        ------------------------------------------------------
        */

        this.websocket.on(
            "weather",
            weather => {

                this.getComponent("weather")
                    ?.update?.(weather);

                this.events.emit(
                    "weather:updated",
                    weather
                );

            }
        );

        /*
        ------------------------------------------------------
        Risk
        ------------------------------------------------------
        */

        this.websocket.on(
            "risk",
            risk => {

                this.getComponent("riskGauge")
                    ?.update?.(risk);

                this.events.emit(
                    "risk:updated",
                    risk
                );

            }
        );

        await this.websocket.connect();

    }

    /*
    ==========================================================
    Page Lifecycle
    ==========================================================
    */

    async pageLoaded(page) {

        this.currentPage = page;

        this.state.set(
            "application.page",
            page
        );

        this.events.emit(
            "page:loaded",
            page
        );

    }

    async pageUnloaded(page) {

        this.events.emit(
            "page:unloaded",
            page
        );

        if(
            page === "dashboard" ||
            page === "map"
        ){

            const map =
                this.getComponent("venueMap");


            map?.destroy();

        }

    }

    /*
    ==========================================================
    Page Navigation
    ==========================================================
    */

    async loadPage(pageName) {
        try {
            // Emit "page:unloaded" for the current page if needed
            if (this.currentPage) {
                await this.pageUnloaded(this.currentPage);
            }

            // Use PageManager to load the new HTML
            await this.pageManager.load(pageName);

            // Update state and emit "page:loaded"
            await this.pageLoaded(pageName);

            // Let the sidebar know which page is active (optional)
            this.getComponent("sidebar")?.setActive(pageName);
        }
        catch (exception) {
            error(
                "Page Load Failed",
                exception
            );

            showToast(
                "Unable to change page",
                "error"
            );
        }
    }

    /*
    ==========================================================
    Dashboard Overview
    ==========================================================
    */

    updateDashboardOverview(statistics) {

        if (!statistics) return;

        /*
        ------------------------------------------------------
        People
        ------------------------------------------------------
        */

        const peopleCard =
            document.getElementById("overviewPeople");

        if (peopleCard) {

            peopleCard.innerHTML = `

                <h3>👥 People:</h3>

                <div class="overview-value">

                    ${statistics.detection?.people_count ?? 0}

                </div>

                <div class="overview-details">

                    <div>
                        Current:
                        <strong>${statistics.detection?.people_count ?? 0}</strong>
                    </div>

                    <div>
                        Tracked:
                        <strong>${statistics.movement?.tracked_people ?? 0}</strong>
                    </div>

                    <div>
                        Capacity:
                        <strong>${statistics.occupancy?.capacity ?? 0}</strong>
                    </div>

                    <div>
                        Occupancy:
                        <strong>${statistics.occupancy?.occupancy_percentage ?? 0}%</strong>
                    </div>

                </div>

            `;

        }

        /*
        ------------------------------------------------------
        Risk
        ------------------------------------------------------
        */

        const riskCard =
            document.getElementById("overviewRisk");

        if (riskCard) {

            riskCard.innerHTML = `

                <h3>⚠ Risk:</h3>

                <div class="overview-value">

                    ${statistics.risk?.risk_level ?? "Unknown"}

                </div>

                <div class="overview-details">

                    <div>
                        Score:
                        <strong>${statistics.risk?.risk_score ?? 0}</strong>
                    </div>

                    <div>
                        Congestion:
                        <strong>${statistics.congestion?.current_level ?? "-"}</strong>
                    </div>

                    <div>
                        Density:
                        <strong>${statistics.risk?.density ?? "-"}</strong>
                    </div>

                </div>

            `;

        }

        /*
        ------------------------------------------------------
        Weather
        ------------------------------------------------------
        */

        const weatherCard =
            document.getElementById("overviewWeather");

        if (weatherCard) {

            weatherCard.innerHTML = `

                <h3>☁ Weather:</h3>

                <div class="overview-value">

                    ${statistics.weather?.temperature ?? "--"}°C

                </div>

                <div class="overview-details">

                    <div>
                        Description:
                        ${statistics.weather?.weather_desc ?? "-"}
                    </div>

                    <div>
                        Humidity:
                        <strong>${statistics.weather?.humidity ?? 0}%</strong>
                    </div>

                    <div>
                        Comfort Level:
                        ${statistics.weather?.comfort ?? "-"}
                    </div>

                </div>

            `;

        }

        /*
        ------------------------------------------------------
        Performance
        ------------------------------------------------------
        */

        const performanceCard =
            document.getElementById("overviewPerformance");

        if (performanceCard) {

            performanceCard.innerHTML = `

                <h3>AI Performance:</h3>

                <div class="overview-value">

                    ${statistics.detection?.detector?.fps ?? "--"}

                </div>

                <div class="overview-details">

                    <div>
                        FPS:
                        <strong>${statistics.detection?.detector?.fps ?? "--"}</strong>
                    </div>

                    <div>
                        Average Processing Time:
                        <strong>${statistics.detection?.detector?.average_processing_time_ms ?? "--"} ms</strong>
                    </div>

                    <div>
                        Total Frames:
                        <strong>${statistics.camera?.frames ?? 0}</strong>
                    </div>

                </div>

            `;

        }

    }

    /*
    ==========================================================
    Global Status Update
    ==========================================================
    */

    updateSystemStatus(statistics) {

        if (!statistics) {
            return;
        }

        console.group("===== SYSTEM STATUS =====");

        console.log("Engine:");
        console.log(statistics.engine);

        console.log("Camera:");
        console.log(statistics.camera);

        console.log("Detection:");
        console.log(statistics.detection);

        console.log("Performance:");
        console.log(statistics.performance);

        console.groupEnd();

        /*
        ------------------------------------------------------
        Backend
        ------------------------------------------------------
        */

        const backendStatus =
            statistics.backend?.status ??
            (this.state.get("connection.backend")
                ? "Online"
                : "Offline");

        /*
        ------------------------------------------------------
        WebSocket
        ------------------------------------------------------
        */

        const websocketStatus =
            this.connected
                ? "Connected"
                : "Disconnected";

        /*
        ------------------------------------------------------
        AI Engine
        ------------------------------------------------------
        */

        const engine =
            statistics.engine ?? {};

        const aiStatus =
            engine.status ?? "Stopped";

        /*
        ------------------------------------------------------
        Cameras
        ------------------------------------------------------
        */

        const cameras =
            statistics.camera?.active ??
            statistics.camera?.connected ??
            statistics.camera?.camera_count ??
            0;

        /*
        ------------------------------------------------------
        FPS
        ------------------------------------------------------
        */

        const fps =
            statistics.detection?.detector?.fps ??
            statistics.performance?.current_fps ??
            "--";

        /*
        ------------------------------------------------------
        Footer
        ------------------------------------------------------
        */

        this.getComponent("footer")?.update({

            backend: backendStatus,

            websocket: websocketStatus,

            ai: aiStatus,

            version:
                engine.version ??
                APP.VERSION,

            build:
                statistics.build ??
                "Stable",

            event:
                statistics.event?.name ??
                "Simulation"

        });

        /*
        ------------------------------------------------------
        System Status Bar
        ------------------------------------------------------
        */

        document.getElementById("backendStatus").textContent =
            backendStatus;

        document.getElementById("backendStatus").className =
            `status-indicator ${
                backendStatus.toLowerCase() === "online"
                    ? "online"
                    : "offline"
            }`;

        document.getElementById("socketStatus").textContent =
            websocketStatus;

        document.getElementById("socketStatus").className =
            `status-indicator ${
                websocketStatus === "Connected"
                    ? "online"
                    : "offline"
            }`;

        document.getElementById("engineStatus").textContent =
            aiStatus;

        document.getElementById("engineStatus").className =
            `status-indicator ${
                aiStatus.toLowerCase() === "running"
                    ? "online"
                    : "offline"
            }`;

        document.getElementById("cameraCount").textContent =
            cameras;

        document.getElementById("globalFPS").textContent =
            fps;

    }

    /*
    ==========================================================
    Page-Specific Initialization
    ==========================================================
    */

    async initializePage(page) {

        // Dashboard: placeholder for dashboard-specific setup
        if (page === "dashboard") {

            // Camera Grid
            this.getComponent("cameraGrid")
                ?.initialize("cameraGrid");

            // Statistics
            this.getComponent("statistics")
                ?.initialize("statisticsContainer");

            // Charts
            this.getComponent("charts")
                ?.initialize?.();

            // Risk Gauge
            this.getComponent("riskGauge")
                ?.initialize?.("riskGauge");

            // Weather
            this.getComponent("weather")
                ?.initialize?.();

            const mapComponent =
                this.getComponent("venueMap");


            const container =
                document.getElementById("venueMap");


            if (!mapComponent || !container) {
                return;
            }


            requestAnimationFrame(() => {

                mapComponent.initialize();


                setTimeout(() => {

                    mapComponent.resize();

                }, 300);

            });

            const statistics =
                this.state.get("statistics");

            if (statistics?.engine) {

                this.updateDashboardOverview(
                    statistics
                );

                this.updateSystemStatus(statistics);

            }

            this.getComponent("alerts")
                ?.initialize();


            return;

        }

        // Maps: initialize the Leaflet venue map
        if (page === "map") {

            const mapComponent =
                this.getComponent("venueMap");


            const container =
                document.getElementById("venueMap");


            if (!mapComponent || !container) {
                return;
            }


            requestAnimationFrame(() => {

                mapComponent.initialize();


                setTimeout(() => {

                    mapComponent.resize();

                }, 300);

            });


            return;

        }

        if (page === "cameras") {

            const grid = this.getComponent("cameraGrid");

            grid.initialize("cameraGrid");

            this.getComponent("statistics")
                ?.initialize("cameraStatistics");

            return;

        }

        if (page === "analytics") {

            console.log("Initializing Analytics Page");

            this.getComponent("statistics")?.initialize?.();

            this.getComponent("occupancy")?.initialize?.();

            this.getComponent("density")?.initialize?.();

            this.getComponent("congestion")?.initialize?.();

            this.getComponent("movement")?.initialize?.();

            this.getComponent("weather")?.initialize?.();

            this.getComponent("riskGauge")?.initialize?.("riskTrendPanel");

            console.groupEnd();

            return;
        }

        // Other pages can be handled here in future
    }

    /*
    ==========================================================
    Refresh
    ==========================================================
    */

    async refresh() {

        log("Refreshing Application...");

        try {

            const statistics =
                await this.api.getStatistics();

            this.state.set(
                "statistics",
                statistics
            );

            this.updateDashboardOverview(data);

            this.getComponent("statistics")
                ?.update(statistics);


            const cameras =
                await this.api.getCameras();

            this.state.set(
                "cameras",
                cameras
            );

            this.getComponent("cameraGrid")
                ?.setCameras?.(cameras);

            this.events.emit(
                "application:refreshed"
            );

            showToast(
                "Dashboard Refreshed",
                "success"
            );

        }

        catch (exception) {

            error(
                "Refresh Failed",
                exception
            );

            showToast(
                "Refresh Failed",
                "error"
            );

        }

    }

    /*
    ==========================================================
    Shutdown
    ==========================================================
    */

    async destroy() {

        if (this.destroyed) {

            return;

        }

        this.destroyed = true;

        log("Shutting Down...");

        try {

            this.websocket.disconnect();

        }

        catch {}

        this.events.emit(
            "application:shutdown"
        );

        this.components.forEach(component => {

            if (component?.destroy) {

                component.destroy();

            }

        });

        this.modules.forEach(module => {

            if (module?.destroy) {

                module.destroy();

            }

        });

        this.services.clear();

        this.components.clear();

        this.modules.clear();

        this.started = false;

        this.initialized = false;

        this.connected = false;

        this.loading = false;

        log("Shutdown Complete.");

    }

}

/*
============================================================
Application Bootstrap
============================================================
*/

const application =
    new AstravonLiveArena();

window.Astravon =
    application;

document.addEventListener(
    "DOMContentLoaded",
    async () => {

        try {

            await application.initialize();

            await application.start();

            await application.initializeWebSocket();

            application.events.emit(
                "application:start"
            );

        }

        catch (exception) {

            console.error(exception);

            showToast(
                "Unable to Start Application",
                "error"
            );

        }

    }
);

window.addEventListener(
    "beforeunload",
    () => {

        application.destroy();

    }
);

/*
============================================================
Exports
============================================================
*/

export { AstravonLiveArena };

export default application;