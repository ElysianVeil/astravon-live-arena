/*
============================================================
Astravon Live Arena
API Client

Purpose:
    Centralized HTTP client for all frontend to
    backend communication.

Features:
    • Automatic retries
    • Request timeout
    • Authentication
    • Request/Response interceptors
    • File uploads
    • Download support
    • AbortController support
    • Endpoint helpers
    • Consistent error handling

Author:
    House of Astravon
Version:
    2.0.0
============================================================
*/

import EventBus from "./event_bus.js";
import State from "./state.js";
import {
    API as API_CONFIG
} from "./constants.js";

class API {

    constructor() {

        /*
        ======================================================
        Configuration
        ======================================================
        */

        this.baseURL =
            `${API_CONFIG.BASE_URL}${API_CONFIG.VERSION}`;

        this.timeout =
            API_CONFIG.TIMEOUT;

        this.retryCount = 3;

        this.defaultHeaders = {
            "Content-Type": "application/json"
        };

        /*
        ======================================================
        Authentication
        ======================================================
        */

        this.token = null;

        /*
        ======================================================
        Interceptors
        ======================================================
        */

        this.requestInterceptors = [];

        this.responseInterceptors = [];

        this.errorInterceptors = [];

    }

    /*
    ======================================================
    Authentication
    ======================================================
    */

    setToken(token) {

        this.token = token;

    }

    clearToken() {

        this.token = null;

    }

    getHeaders(extra = {}) {

        const headers = {
            ...this.defaultHeaders,
            ...extra
        };

        if (this.token) {

            headers.Authorization =
                `Bearer ${this.token}`;

        }

        return headers;

    }

    /*
    ======================================================
    Interceptors
    ======================================================
    */

    useRequest(callback) {

        this.requestInterceptors.push(callback);

    }

    useResponse(callback) {

        this.responseInterceptors.push(callback);

    }

    useError(callback) {

        this.errorInterceptors.push(callback);

    }

    /*
    ======================================================
    Timeout
    ======================================================
    */

    createTimeout() {

        const controller = new AbortController();

        const timer = setTimeout(

            () => controller.abort(),

            this.timeout

        );

        return {

            controller,

            timer

        };

    }

    /*
    ======================================================
    Core Request
    ======================================================
    */

    async request(

        endpoint,

        options = {},

        retry = 0

    ) {

        const {

            controller,

            timer

        } = this.createTimeout();

        let config = {

            method: "GET",

            headers: this.getHeaders(

                options.headers

            ),

            signal: controller.signal,

            ...options

        };

        for (const interceptor of this.requestInterceptors) {

            config = await interceptor(config) || config;

        }

        try {

            EventBus.emit("api:request:start", {

                endpoint,

                config

            });

            const response = await fetch(

                `${this.baseURL}${endpoint}`,

                config

            );

            clearTimeout(timer);

            let data = null;

            const contentType =

                response.headers.get(

                    "content-type"

                ) || "";

            if (

                contentType.includes(

                    "application/json"

                )

            ) {

                data = await response.json();

            }

            else {

                data = await response.text();

            }

            if (!response.ok) {

                throw {

                    status: response.status,

                    message:

                        data?.message ||

                        response.statusText,

                    data

                };

            }

            for (const interceptor of this.responseInterceptors) {

                data = await interceptor(data) || data;

            }

            EventBus.emit(

                "api:request:success",

                {

                    endpoint,

                    data

                }

            );

            return data;

        }

        catch (error) {

            clearTimeout(timer);

            if (

                retry < this.retryCount

            ) {

                return this.request(

                    endpoint,

                    options,

                    retry + 1

                );

            }

            for (const interceptor of this.errorInterceptors) {

                interceptor(error);

            }

            EventBus.emit(

                "api:request:error",

                error

            );

            throw error;

        }

    }

    /*
    ======================================================
    HTTP Methods
    ======================================================
    */

    get(endpoint) {

        return this.request(

            endpoint,

            {

                method: "GET"

            }

        );

    }

    post(

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

    put(

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

    patch(

        endpoint,

        body = {}

    ) {

        return this.request(

            endpoint,

            {

                method: "PATCH",

                body: JSON.stringify(body)

            }

        );

    }

    delete(endpoint) {

        return this.request(

            endpoint,

            {

                method: "DELETE"

            }

        );

    }

    /*
    ======================================================
    Upload
    ======================================================
    */

    upload(

        endpoint,

        formData

    ) {

        const headers = {};

        if (this.token) {

            headers.Authorization =

                `Bearer ${this.token}`;

        }

        return this.request(

            endpoint,

            {

                method: "POST",

                headers,

                body: formData

            }

        );

    }

    /*
    ======================================================
    Download
    ======================================================
    */

    async download(endpoint) {

        const response = await fetch(

            `${this.baseURL}${endpoint}`,

            {

                headers: this.getHeaders()

            }

        );

        return response.blob();

    }

    /*
    ======================================================
    Health
    ======================================================
    */

    health() {

        return this.get("/status");

    }

    /*
    ======================================================
    Dashboard
    ======================================================
    */

    getDashboard() {

        return this.get("/dashboard");

    }

    /*
    ======================================================
    Cameras
    ======================================================
    */

    getCameras() {

        return this.get("/camera");

    }

    getCamera(id) {

        return this.get(`/camera/${id}`);

    }

    getCameraStatus(id) {

        return this.get(

            `/camera/${id}/status`

        );

    }

    connectCamera(id) {

        return this.post(

            `/camera/${id}/connect`

        );

    }

    disconnectCamera(id) {

        return this.post(

            `/camera/${id}/disconnect`

        );

    }

    snapshotCamera(id) {

        return this.post(

            `/camera/${id}/snapshot`

        );

    }

    recordCamera(id) {

        return this.post(

            `/camera/${id}/record`

        );

    }

    /*
    ======================================================
    AI
    ======================================================
    */

    getDetections() {

        return this.get("/ai/detection");

    }

    sendDetection(data) {

        return this.post(

            "/ai/detection",

            data

        );

    }

    /*
    ======================================================
    Statistics
    ======================================================
    */

    getStatistics() {

        return this.get("/statistics");

    }

    getStatisticsHistory() {

        return this.get(

            "/statistics/history"

        );

    }

    getStatisticsSummary() {

        return this.get(

            "/statistics/summary"

        );

    }

    /*
    ======================================================
    Alerts
    ======================================================
    */

    getAlerts() {

        return this.get("/alerts");

    }

    acknowledgeAlert(id) {

        return this.put(

            `/alerts/${id}`,

            {

                acknowledged: true

            }

        );

    }

    dismissAlert(id) {

        return this.delete(

            `/alerts/${id}`

        );

    }

    /*
    ======================================================
    Reports
    ======================================================
    */

    getReports() {

        return this.get("/reports");

    }

    generateReport(data) {

        return this.post(

            "/reports",

            data

        );

    }

    /*
    ======================================================
    Event Modes
    ======================================================
    */

    getEventModes() {

        return this.get(

            "/event-modes"

        );

    }

    setEventMode(mode) {

        return this.post(

            "/event-modes",

            {

                mode

            }

        );

    }

    /*
    ======================================================
    Dashboard State
    ======================================================
    */

    async refreshDashboard() {

        const data =

            await this.getDashboard();

        State.set(

            "dashboard",

            data

        );

        return data;

    }

}

export const api = new API();

export default api;