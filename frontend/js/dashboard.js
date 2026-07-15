/*
============================================================
Astravon Live Arena
Dashboard Controller

Purpose:
    Controls the dashboard by coordinating the
    API, WebSocket, Charts and UI components.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

import API from "./api.js";
import WebSocketManager from "./websocket.js";

export default class Dashboard {

    constructor() {

        /*
        =====================================================
        Services
        =====================================================
        */

        this.api = new API();

        this.websocket = new WebSocketManager();

        /*
        =====================================================
        Dashboard State
        =====================================================
        */

        this.statistics = {};

        this.alerts = [];

        this.cameras = [];

        this.summary = {};

        this.connected = false;

        this.lastUpdate = null;

    }

    /*
    ==========================================================
    Initialize
    ==========================================================
    */

    async initialize() {

        console.log(
            "[Dashboard] Initializing..."
        );

        await this.loadDashboard();

        await this.initializeWebSocket();

        this.initializeEvents();

        console.log(
            "[Dashboard] Ready."
        );

    }

    /*
    ==========================================================
    Load Dashboard
    ==========================================================
    */

    async loadDashboard() {

        try {

            await Promise.all([

                this.loadStatistics(),

                this.loadSummary(),

                this.loadAlerts()

            ]);

        }

        catch (error) {

            console.error(
                "[Dashboard]",
                error
            );

        }

    }

    /*
    ==========================================================
    Statistics
    ==========================================================
    */

    async loadStatistics() {

        try {

            const response =

                await this.api.getStatistics();

            this.statistics =

                response.data ?? {};

            this.updateStatistics();

        }

        catch (error) {

            console.error(error);

        }

    }

    /*
    ==========================================================
    Summary
    ==========================================================
    */

    async loadSummary() {

        try {

            const response =

                await this.api.getStatisticsSummary();

            this.summary =

                response.data ?? {};

            this.updateSummary();

        }

        catch (error) {

            console.error(error);

        }

    }

    /*
    ==========================================================
    Alerts
    ==========================================================
    */

    async loadAlerts() {

        try {

            const response =

                await this.api.getAlerts();

            this.alerts =

                response.data ?? [];

            this.updateAlerts();

        }

        catch (error) {

            console.error(error);

        }

    }

    /*
    ==========================================================
    Cameras
    ==========================================================
    */

    async loadCameras() {

        try {

            const response =

                await this.api.getCameras();

            this.cameras =

                response.data ?? [];

            this.updateCameraPanel();

        }

        catch (error) {

            console.error(error);

        }

    }

    /*
    ==========================================================
    WebSocket
    ==========================================================
    */

    async initializeWebSocket() {

        await this.websocket.connect();

        this.websocket.onOpen(() => {

            this.connected = true;

            this.updateConnectionStatus(
                true
            );

        });

        this.websocket.onClose(() => {

            this.connected = false;

            this.updateConnectionStatus(
                false
            );

        });

        /*
        --------------------------------------------
        Live Statistics
        --------------------------------------------
        */

        this.websocket.on(

            "statistics",

            statistics => {

                this.statistics = statistics;

                this.lastUpdate =

                    new Date();

                this.updateStatistics();

            }

        );

        /*
        --------------------------------------------
        Live Alerts
        --------------------------------------------
        */

        this.websocket.on(

            "alert",

            alert => {

                this.alerts.unshift(

                    alert

                );

                this.updateAlerts();

            }

        );

        /*
        --------------------------------------------
        Live Detection
        --------------------------------------------
        */

        this.websocket.on(

            "detection",

            detection => {

                this.updateDetection(

                    detection

                );

            }

        );

        /*
        --------------------------------------------
        Camera
        --------------------------------------------
        */

        this.websocket.on(

            "camera",

            frame => {

                this.updateCamera(

                    frame

                );

            }

        );

    }

    /*
    ==========================================================
    UI Updates
    ==========================================================
    */

    updateStatistics() {

        this.setText(

            "peopleCount",

            this.statistics.people_count

        );

        this.setText(

            "occupancy",

            this.statistics.occupancy

        );

        this.setText(

            "density",

            this.statistics.density

        );

        this.setText(

            "temperature",

            this.statistics.temperature

        );

        this.setText(

            "humidity",

            this.statistics.humidity

        );

        this.setText(

            "heatIndex",

            this.statistics.heat_index

        );

        this.setText(

            "riskScore",

            this.statistics.risk_score

        );

        this.setText(

            "riskLevel",

            this.statistics.risk_level

        );

        this.setText(

            "fps",

            this.statistics.fps

        );

    }

    updateSummary() {

        console.log(

            "[Dashboard] Summary Updated"

        );

    }

    updateAlerts() {

        console.log(

            "[Dashboard] Alerts:",

            this.alerts.length

        );

    }

    updateCameraPanel() {

        console.log(

            "[Dashboard] Camera Ready"

        );

    }

    updateCamera(frame) {

        console.log(

            "[Dashboard] Frame Received"

        );

    }

    updateDetection(data) {

        console.log(

            "[Dashboard] Detection",

            data

        );

    }

    /*
    ==========================================================
    Connection Status
    ==========================================================
    */

    updateConnectionStatus(

        connected

    ) {

        const element =

            document.getElementById(

                "connectionStatus"

            );

        if (!element) {

            return;

        }

        element.textContent =

            connected

                ? "Connected"

                : "Disconnected";

        element.className =

            connected

                ? "status-online"

                : "status-offline";

    }

    /*
    ==========================================================
    DOM Utilities
    ==========================================================
    */

    setText(

        id,

        value

    ) {

        const element =

            document.getElementById(id);

        if (!element) {

            return;

        }

        element.textContent =

            value ?? "--";

    }

    /*
    ==========================================================
    Events
    ==========================================================
    */

    initializeEvents() {

        console.log(

            "[Dashboard] Events Initialized"

        );

    }

    /*
    ==========================================================
    Refresh
    ==========================================================
    */

    async refresh() {

        await this.loadDashboard();

    }

}