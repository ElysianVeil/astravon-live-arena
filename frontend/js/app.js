/*
============================================================
Astravon Live Arena
Application Entry Point

Purpose:
    Initializes the frontend application,
    loads components, establishes API and
    WebSocket connections, and starts the
    live dashboard.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

import API from "./api.js";
import WebSocketManager from "./websocket.js";

import Dashboard from "./dashboard.js";
import Charts from "./charts.js";
import AlertManager from "./alerts.js";
import EventModes from "./event_modes.js";
import MapManager from "./map.js";

import {
    showToast,
    formatTime,
    setLoading,
    hideLoading
} from "./utils.js";

import Navbar from "../components/navbar.js";
import Sidebar from "../components/sidebar.js";
import Footer from "../components/footer.js";

import Statistics from "../components/statistics.js";
import CameraPanel from "../components/camera_panel.js";
import AlertPanel from "../components/alert_panel.js";

/**
 * ==========================================================
 * Application
 * ==========================================================
 */

class AstravonLiveArena {

    constructor() {

        this.api = new API();

        this.websocket = new WebSocketManager();

        this.dashboard = new Dashboard();

        this.charts = new Charts();

        this.alerts = new AlertManager();

        this.events = new EventModes();

        this.map = new MapManager();

         /*
        UI Components
        */

        this.navbar = new Navbar();

        this.sidebar = new Sidebar();

        this.footer = new Footer();

        this.statistics = new Statistics();

        this.cameraPanel = new CameraPanel();

        this.alertPanel = new AlertPanel();

        this.connected = false;

        this.started = false;

        this.currentPage = "dashboard";

        this.pageInitializers = {

            dashboard: () => {

                this.statistics.initialize();

                this.cameraPanel.initialize();

                this.alertPanel.initialize();

                this.dashboard.initialize();

                this.charts.initialize();

                this.events.initialize();

                this.map.initialize();

            },

            reports: () => {

                console.log("Reports");

            },

            settings: () => {

                console.log("Settings");

            },

            about: () => {

                console.log("About");

            }

        };

    }

    async loadPage(page) {

        try {

            const response =
                await fetch(`pages/${page}.html`);

            if (!response.ok) {

                throw new Error(
                    `Unable to load ${page}.html`
                );

            }

            const html =
                await response.text();

            document.getElementById(
                "mainContent"
            ).innerHTML = html;

            this.currentPage = page;

            this.sidebar.setActive(page);

            /*
            Reinitialize components
            */

            const initializer = this.pageInitializers[page];

            if (initializer) {

                initializer();

            }

        }

        catch (error) {

            console.error(error);

            showToast(
                "Unable to load page.",
                "error"
            );

        }

    }

    /**
     * ------------------------------------------------------
     * Initialize Application
     * ------------------------------------------------------
     */

    async initialize() {

        console.log(
            "========================================"
        );

        console.log(
            "Astravon Live Arena Dashboard"
        );

        console.log(
            "Initializing..."
        );

        console.log(
            "========================================"
        );

        setLoading();

        try {
            // Layout exists immediately
            this.navbar.initialize();

            this.sidebar.initialize();

            this.footer.initialize();

            await this.loadPage("dashboard");

            await this.loadDashboard();

            await this.connectBackend();

            // this.initializeModules();

            this.registerEvents();

            this.started = true;

            hideLoading();

            showToast(
                "Dashboard Ready",
                "success"
            );

            console.log(
                "Dashboard initialized."
            );

        }

        catch (error) {

            console.error(error);

            hideLoading();

            showToast(
                "Failed to initialize dashboard.",
                "error"
            );

        }

    }

    /**
     * ------------------------------------------------------
     * Load Dashboard
     * ------------------------------------------------------
     */

    async loadDashboard() {

        try {

            const statistics =
                await this.api.getStatistics();

            if (statistics) {

                this.dashboard.updateStatistics(
                    statistics
                );

            }

        }

        catch (error) {

            console.warn(
                "Unable to load statistics."
            );

        }

    }

    /**
     * ------------------------------------------------------
     * Connect Backend
     * ------------------------------------------------------
     */

    async connectBackend() {

        await this.websocket.connect();

        this.connected = true;

        console.log(
            "WebSocket Connected"
        );

    }

    /**
     * ------------------------------------------------------
     * Initialize Modules
     * ------------------------------------------------------
     */

    initializeModules() {

        /*
        Layout
        */

        this.navbar.initialize();

        this.sidebar.initialize();

        this.footer.initialize();

        /*
        Dashboard Widgets
        */

        this.statistics.initialize();

        this.cameraPanel.initialize();

        this.alertPanel.initialize();

        /*
        Dashboard Logic
        */

        this.dashboard.initialize();

        this.charts.initialize();

        this.alerts.initialize();

        this.events.initialize();

        // this.map.initialize();

    }

    /**
     * ------------------------------------------------------
     * Register Events
     * ------------------------------------------------------
     */

    registerEvents() {

        /**
         * Live statistics
         */

        this.websocket.on(
            "statistics",
            (data) => {

                this.statistics.update(data)
                this.dashboard.updateStatistics(
                    data
                );

                this.charts.update(data);

            }
        );

        /**
         * AI detections
         */

        this.websocket.on(
            "detection",
            (data) => {

                this.dashboard.updateDetection(
                    data
                );

            }
        );

        /**
         * Alerts
         */

        this.websocket.on(
            "alert",
            (alert) => {

                this.alertPanel.addAlert(alert);

            }
        );

        /**
         * Event Mode
         */

        this.websocket.on(
            "event_mode",
            (mode) => {

                this.events.change(mode);

            }
        );

        /**
         * Camera Frame
         */

        this.websocket.on(
            "frame",
            (data) => {

                this.cameraPanel.updateFrame(data.frame);

                this.cameraPanel.updateInfo({

                    width: data.width,

                    height: data.height,

                    fps: data.fps

                });

            }
        );

        /**
         * Connection Status
         */

        this.websocket.onOpen(() => {

            this.connected = true;

            this.navbar.setConnected();

            this.footer.setBackendStatus("Online");

            this.footer.setWebSocketStatus("Connected");

        });

        this.websocket.onClose(() => {

            this.connected = false;

            this.navbar.setDisconnected();

            this.footer.setBackendStatus("Offline");

            this.footer.setWebSocketStatus("Disconnected");

        });

    }

    /**
     * ------------------------------------------------------
     * Refresh Dashboard
     * ------------------------------------------------------
     */

    async refresh() {

        console.log(
            "Refreshing Dashboard..."
        );

        await this.loadDashboard();

    }

    /**
     * ------------------------------------------------------
     * Shutdown
     * ------------------------------------------------------
     */

    destroy() {

        this.websocket.disconnect();

        console.log(
            "Dashboard stopped."
        );

    }

}





/**
 * ==========================================================
 * Start Application
 * ==========================================================
 */

document.addEventListener(

    "DOMContentLoaded",

    async () => {

        window.Astravon =
            new AstravonLiveArena();

        await window.Astravon.initialize();

        console.log(
            "Started at:",
            formatTime(new Date())
        );

    }

);

/**
 * ==========================================================
 * Cleanup
 * ==========================================================
 */

window.addEventListener(

    "beforeunload",

    () => {

        if (window.Astravon) {

            window.Astravon.destroy();

        }

    }

);