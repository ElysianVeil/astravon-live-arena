/*
============================================================
Astravon Live Arena
Global State Store

Purpose:
    Centralized frontend state management.

    Acts as the single source of truth for all
    application data.

Author:
    House of Astravon

Version:
    2.0.0
============================================================
*/

import eventBus from "./event_bus.js";

class StateStore {

    constructor() {

        /*
        ====================================================
        Global State
        ====================================================
        */

        this.state = {

            app: {

                initialized: false,

                loading: true,

                theme: "dark",

                page: "dashboard"

            },

            backend: {

                connected: false,

                latency: 0,

                version: null

            },

            websocket: {

                connected: false,

                reconnecting: false

            },

            ai: {

                online: false,

                processing: false,

                model: null

            },

            cameras: [],

            statistics: {},

            alerts: [],

            weather: {},

            emergency: {},

            reports: [],

            user: {}

        };

    }

    /*
    ============================================================
    Entire State
    ============================================================
    */

    getState() {

        return structuredClone(this.state);

    }

    /*
    ============================================================
    Get
    ============================================================
    */

    get(key) {

        return this.state[key];

    }

    /*
    ============================================================
    Set
    ============================================================
    */

    set(key, value) {

        this.state[key] = value;

        eventBus.emit(

            `state:${key}`,

            value

        );

        eventBus.emit(

            "state:changed",

            {

                key,

                value

            }

        );

    }

    /*
    ============================================================
    Merge
    ============================================================
    */

    merge(

        key,

        value

    ) {

        if (

            typeof this.state[key] !== "object"

        ) {

            this.state[key] = value;

        }

        else {

            this.state[key] = {

                ...this.state[key],

                ...value

            };

        }

        eventBus.emit(

            `state:${key}`,

            this.state[key]

        );

        eventBus.emit(

            "state:changed",

            {

                key,

                value: this.state[key]

            }

        );

    }

    /*
    ============================================================
    Reset
    ============================================================
    */

    reset() {

        this.constructor.call(this);

        eventBus.emit(

            "state:reset"

        );

    }

    /*
    ============================================================
    Cameras
    ============================================================
    */

    getCameras() {

        return this.state.cameras;

    }

    setCameras(cameras) {

        this.set(

            "cameras",

            cameras

        );

    }

    addCamera(camera) {

        this.state.cameras.push(camera);

        eventBus.emit(

            "state:cameras",

            this.state.cameras

        );

    }

    removeCamera(id) {

        this.state.cameras =

            this.state.cameras.filter(

                camera =>

                    camera.id !== id

            );

        eventBus.emit(

            "state:cameras",

            this.state.cameras

        );

    }

    updateCamera(

        id,

        updates

    ) {

        const camera =

            this.state.cameras.find(

                camera =>

                    camera.id === id

            );

        if (!camera) {

            return;

        }

        Object.assign(

            camera,

            updates

        );

        eventBus.emit(

            "state:cameras",

            this.state.cameras

        );

    }

    /*
    ============================================================
    Statistics
    ============================================================
    */

    updateStatistics(data) {

        this.merge(

            "statistics",

            data

        );

    }

    /*
    ============================================================
    Weather
    ============================================================
    */

    updateWeather(data) {

        this.merge(

            "weather",

            data

        );

    }

    /*
    ============================================================
    AI
    ============================================================
    */

    updateAI(data) {

        this.merge(

            "ai",

            data

        );

    }

    /*
    ============================================================
    Backend
    ============================================================
    */

    updateBackend(data) {

        this.merge(

            "backend",

            data

        );

    }

    /*
    ============================================================
    WebSocket
    ============================================================
    */

    updateWebSocket(data) {

        this.merge(

            "websocket",

            data

        );

    }

    /*
    ============================================================
    Alerts
    ============================================================
    */

    getAlerts() {

        return this.state.alerts;

    }

    addAlert(alert) {

        this.state.alerts.unshift(alert);

        eventBus.emit(

            "state:alerts",

            this.state.alerts

        );

    }

    removeAlert(id) {

        this.state.alerts =

            this.state.alerts.filter(

                alert =>

                    alert.id !== id

            );

        eventBus.emit(

            "state:alerts",

            this.state.alerts

        );

    }

    clearAlerts() {

        this.state.alerts = [];

        eventBus.emit(

            "state:alerts",

            []

        );

    }

    /*
    ============================================================
    Reports
    ============================================================
    */

    addReport(report) {

        this.state.reports.push(report);

        eventBus.emit(

            "state:reports",

            this.state.reports

        );

    }

    /*
    ============================================================
    Emergency
    ============================================================
    */

    updateEmergency(data) {

        this.merge(

            "emergency",

            data

        );

    }

    /*
    ============================================================
    User
    ============================================================
    */

    updateUser(data) {

        this.merge(

            "user",

            data

        );

    }

    /*
    ============================================================
    Subscribe
    ============================================================
    */

    subscribe(key, callback) {

        eventBus.on(
            `state:${key}`,
            callback
        );

    }

    /*
    ============================================================
    Unsubscribe
    ============================================================
    */

    unsubscribe(key, callback) {

        eventBus.off?.(
            `state:${key}`,
            callback
        );

    }

}

/*
============================================================
Singleton
============================================================
*/

export const state =

    new StateStore();

export default state;