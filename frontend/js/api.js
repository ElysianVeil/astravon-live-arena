/*
============================================================
Astravon Live Arena
API Client

Purpose:
    Handles all HTTP communication with the
    Astravon Live Arena Backend.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

export default class API {

    constructor() {

        /**
         * --------------------------------------
         * Backend Configuration
         * --------------------------------------
         */

        this.baseURL = "http://127.0.0.1:8000/api/v1";

        this.defaultHeaders = {

            "Content-Type": "application/json"

        };

    }

    /*
    ==========================================================
    Core Request
    ==========================================================
    */

    async request(
        endpoint,
        options = {}
    ) {

        const config = {

            headers: {

                ...this.defaultHeaders,

                ...(options.headers || {})

            },

            ...options

        };

        try {

            const response = await fetch(

                `${this.baseURL}${endpoint}`,

                config

            );

            const data = await response.json();

            if (!response.ok) {

                throw new Error(

                    data.message ||

                    `HTTP ${response.status}`

                );

            }

            return data;

        }

        catch (error) {

            console.error(

                "[API]",

                error.message

            );

            throw error;

        }

    }

    /*
    ==========================================================
    GET
    ==========================================================
    */

    async get(endpoint) {

        return this.request(

            endpoint,

            {

                method: "GET"

            }

        );

    }

    /*
    ==========================================================
    POST
    ==========================================================
    */

    async post(
        endpoint,
        body = {}
    ) {

        return this.request(

            endpoint,

            {

                method: "POST",

                body: JSON.stringify(body)

            }

        );

    }

    /*
    ==========================================================
    PUT
    ==========================================================
    */

    async put(
        endpoint,
        body = {}
    ) {

        return this.request(

            endpoint,

            {

                method: "PUT",

                body: JSON.stringify(body)

            }

        );

    }

    /*
    ==========================================================
    DELETE
    ==========================================================
    */

    async delete(endpoint) {

        return this.request(

            endpoint,

            {

                method: "DELETE"

            }

        );

    }

    /*
    ==========================================================
    AI Detection
    ==========================================================
    */

    async getLatestDetection() {

        return this.get(

            "/ai/detection"

        );

    }

    async sendDetection(

        detection

    ) {

        return this.post(

            "/ai/detection",

            detection

        );

    }

    /*
    ==========================================================
    Statistics
    ==========================================================
    */

    async getStatistics() {

        return this.get(

            "/statistics"

        );

    }

    async getStatisticsHistory() {

        return this.get(

            "/statistics/history"

        );

    }

    async getStatisticsSummary() {

        return this.get(

            "/statistics/summary"

        );

    }

    async sendStatistics(

        statistics

    ) {

        return this.post(

            "/statistics/",

            statistics

        );

    }

    /*
    ==========================================================
    Alerts
    ==========================================================
    */

    async getAlerts() {

        return this.get(

            "/alerts"

        );

    }

    async acknowledgeAlert(

        alertID

    ) {

        return this.put(

            `/alerts/${alertID}`,

            {

                acknowledged: true

            }

        );

    }

    /*
    ==========================================================
    Cameras
    ==========================================================
    */

    async getCameras() {

        return this.get(

            "/camera"

        );

    }

    async getCameraStatus() {

        return this.get(

            "/camera/status"

        );

    }

    /*
    ==========================================================
    Dashboard
    ==========================================================
    */

    async getDashboard() {

        return this.get(

            "/dashboard"

        );

    }

    /*
    ==========================================================
    Reports
    ==========================================================
    */

    async getReports() {

        return this.get(

            "/reports"

        );

    }

    /*
    ==========================================================
    Event Modes
    ==========================================================
    */

    async getEventModes() {

        return this.get(

            "/event-modes"

        );

    }

    async setEventMode(

        mode

    ) {

        return this.post(

            "/event-modes",

            {

                mode

            }

        );

    }

    /*
    ==========================================================
    Health Check
    ==========================================================
    */

    async health() {

        return this.get(

            "/health"

        );

    }

}