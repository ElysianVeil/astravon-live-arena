/*
============================================================
Astravon Live Arena
WebSocket Manager

Purpose:
    Centralized real-time communication layer
    between the frontend and the AI Backend.

Responsibilities

    • Connection lifecycle
    • Automatic reconnection
    • Heartbeat monitoring
    • Outgoing queue
    • Event routing (Part 2)
    • Request/Response system (Part 2)

Author:
    House of Astravon

Version:
    2.0.0
============================================================
*/

import EventBus from "./event_bus.js";
import AppState from "./state.js";

export default class WebSocketManager {

    constructor(options = {}) {

        /*
        ======================================================
        Configuration
        ======================================================
        */

        this.url =
            options.url ??
            "ws://127.0.0.1:8000/ws";

        this.protocols =
            options.protocols ?? [];

        /*
        ======================================================
        Socket
        ======================================================
        */

        this.socket = null;

        this.connected = false;

        this.connecting = false;

        /*
        ======================================================
        Reconnection
        ======================================================
        */

        this.autoReconnect =
            options.autoReconnect ?? true;

        this.reconnectAttempts = 0;

        this.maxReconnectAttempts =
            options.maxReconnectAttempts ?? Infinity;

        this.reconnectDelay =
            options.reconnectDelay ?? 3000;

        this.maxReconnectDelay =
            options.maxReconnectDelay ?? 30000;

        this.backoffMultiplier =
            options.backoffMultiplier ?? 1.8;

        this.reconnectTimer = null;

        /*
        ======================================================
        Heartbeat
        ======================================================
        */

        this.heartbeatEnabled =
            options.heartbeat ?? true;

        this.heartbeatInterval =
            options.heartbeatInterval ?? 10000;

        this.heartbeatTimeout =
            options.heartbeatTimeout ?? 30000;

        this.heartbeatTimer = null;

        this.lastHeartbeat = 0;

        this.lastPing = 0;

        this.lastPong = 0;

        /*
        ======================================================
        Queue
        ======================================================
        */

        this.outgoingQueue = [];

        this.maxQueueSize =
            options.maxQueueSize ?? 500;

        /*
        ======================================================
        Event Handlers
        ======================================================
        */

        this.handlers = new Map();

        this.openCallbacks = [];

        this.closeCallbacks = [];

        this.errorCallbacks = [];

        /*
        ======================================================
        Request System
        (Implemented in Part 2)
        ======================================================
        */

        this.pendingRequests = new Map();

        this.requestCounter = 0;

        /*
        ======================================================
        Statistics
        ======================================================
        */

        this.statistics = {

            connectedAt: null,

            disconnectedAt: null,

            sent: 0,

            received: 0,

            reconnects: 0,

            queueSize: 0,

            latency: 0

        };

        this.lastFrameTime = 0;

        this.frameInterval = 100; // 10 FPS

    }

    /*
    ======================================================
    Initialize
    ======================================================
    */

    initialize() {

        EventBus.emit(

            "websocket:initialized"

        );

    }

    /*
    ======================================================
    Connect
    ======================================================
    */

    async connect() {

        if (

            this.connected ||

            this.connecting

        ) {

            return;

        }

        this.connecting = true;

        EventBus.emit(

            "websocket:connecting"

        );

        return new Promise((resolve, reject) => {

            try {

                this.socket = new WebSocket(

                    this.url,

                    this.protocols

                );

            }

            catch (error) {

                this.connecting = false;

                reject(error);

                return;

            }

            /*
            -----------------------------------------
            OPEN
            -----------------------------------------
            */

            this.socket.onopen = () => {

                this.connected = true;

                this.connecting = false;

                this.reconnectAttempts = 0;

                this.statistics.connectedAt =
                    Date.now();

                AppState.set(

                    "connection.websocket",

                    true

                );

                this.flushQueue();

                this.startHeartbeat();

                this.openCallbacks.forEach(

                    callback => callback()

                );

                EventBus.emit(

                    "websocket:connected"

                );

                resolve();

            };

            /*
            -----------------------------------------
            MESSAGE
            -----------------------------------------
            */

            this.socket.onmessage = (event) => {

                this.statistics.received++;

                this.lastHeartbeat = Date.now();

                this.receive(event.data);

            };

            /*
            -----------------------------------------
            ERROR
            -----------------------------------------
            */

            this.socket.onerror = (error) => {

                this.errorCallbacks.forEach(

                    callback => callback(error)

                );

                EventBus.emit(

                    "websocket:error",

                    error

                );

            };

            /*
            -----------------------------------------
            CLOSE
            -----------------------------------------
            */

            this.socket.onclose = (event) => {

                this.connected = false;

                this.connecting = false;

                this.statistics.disconnectedAt =
                    Date.now();

                AppState.set(

                    "connection.websocket",

                    false

                );

                this.stopHeartbeat();

                this.closeCallbacks.forEach(

                    callback => callback(event)

                );

                EventBus.emit(

                    "websocket:closed",

                    event

                );

                if (

                    this.autoReconnect

                ) {

                    this.scheduleReconnect();

                }

            };

        });

    }

    /*
    ======================================================
    Disconnect
    ======================================================
    */

    disconnect() {

        this.autoReconnect = false;

        this.stopHeartbeat();

        clearTimeout(

            this.reconnectTimer

        );

        if (this.socket) {

            this.socket.close();

        }

    }

    /*
    ======================================================
    Heartbeat
    ======================================================
    */

    startHeartbeat() {

        if (

            !this.heartbeatEnabled

        ) {

            return;

        }

        this.stopHeartbeat();

        this.heartbeatTimer = setInterval(() => {

            if (!this.connected) {

                return;

            }

            const now = Date.now();

            if (

                this.lastHeartbeat &&

                now - this.lastHeartbeat >

                this.heartbeatTimeout

            ) {

                console.warn(

                    "[WebSocket] Heartbeat timeout."

                );

                this.socket.close();

                return;

            }

            this.lastPing = now;

            this.send({

                type: "ping",

                timestamp: now

            });

        },

        this.heartbeatInterval);

    }

    stopHeartbeat() {

        clearInterval(

            this.heartbeatTimer

        );

        this.heartbeatTimer = null;

    }

    /*
    ======================================================
    Reconnection
    ======================================================
    */

    scheduleReconnect() {

        if (

            this.reconnectAttempts >=

            this.maxReconnectAttempts

        ) {

            return;

        }

        this.reconnectAttempts++;

        this.statistics.reconnects++;

        const delay = Math.min(

            this.reconnectDelay *

            Math.pow(

                this.backoffMultiplier,

                this.reconnectAttempts - 1

            ),

            this.maxReconnectDelay

        );

        clearTimeout(

            this.reconnectTimer

        );

        this.reconnectTimer = setTimeout(() => {

            this.connect();

        },

        delay);

    }

    /*
    ======================================================
    Queue
    ======================================================
    */

    enqueue(data) {

        if (

            this.outgoingQueue.length >=

            this.maxQueueSize

        ) {

            this.outgoingQueue.shift();

        }

        this.outgoingQueue.push(data);

        this.statistics.queueSize =

            this.outgoingQueue.length;

    }

    flushQueue() {

        while (

            this.connected &&

            this.outgoingQueue.length

        ) {

            const message =

                this.outgoingQueue.shift();

            this.socket.send(

                JSON.stringify(message)

            );

        }

        this.statistics.queueSize = 0;

    }

    /*
    ======================================================
    Send
    ======================================================
    */

    send(data) {

        if (!this.connected) {

            this.enqueue(data);

            return;

        }

        this.statistics.sent++;

        this.socket.send(

            JSON.stringify(data)

        );

    }

        /*
    ======================================================
    Receive
    ======================================================
    */

    receive(message) {

        let payload;

        try {

            payload = JSON.parse(message);

        }

        catch (error) {

            console.warn(

                "[WebSocket] Invalid JSON:",

                message

            );

            return;

        }

        this.route(payload);

    }

    /*
    ======================================================
    Route Incoming Messages
    ======================================================
    */

    route(payload) {

        const type = payload.type;

        switch (type) {

            case "pong":

                this.handlePong(payload);

                break;

            case "frame":

                this.handleCameraFrame(payload);

                break;

            case "camera_info":

                this.handleCameraInfo(payload);

                break;

            // case "statistics":

            //     this.handleStatistics(payload);

                break;

            case "risk":

                this.handleRisk(payload);

                break;

            case "weather":

                this.handleWeather(payload);

                break;

            case "alert":

                this.handleAlert(payload);

                break;

            case "people":

                this.handlePeople(payload);

                break;

            case "tracking":

                this.handleTracking(payload);

                break;

            case "report":

                this.handleReport(payload);

                break;

            case "backend_status":

                this.handleBackend(payload);

                break;

            case "response":

                this.handleResponse(payload);

                break;

            default:

                this.handleCustom(payload);

        }

    }

    /*
    ======================================================
    Heartbeat
    ======================================================
    */

    handlePong(payload) {

        this.lastPong = Date.now();

        this.statistics.latency =

            this.lastPong -

            this.lastPing;

        EventBus.emit(

            "websocket:latency",

            this.statistics.latency

        );

    }

    /*
    ======================================================
    Camera
    ======================================================
    */

    handleCameraFrame(payload) {

        const now = performance.now();

        if (now - this.lastFrameTime < this.frameInterval) {
            return;
        }

        this.lastFrameTime = now;

        const frame = payload.data;

        AppState.set("latestFrame", frame);

        AppState.set("statistics", frame.statistics);

        AppState.updateStatistics(frame.statistics);

        const handlers = this.handlers.get("frame");

        if (handlers) {

            handlers.forEach(callback => callback(frame));

        }

        EventBus.emit(
            "camera:frame",
            frame
        );

        EventBus.emit(
            "statistics:update",
            frame.statistics
        );

    }

    

    handleCameraInfo(payload) {

        EventBus.emit(

            "camera:info",

            payload

        );

    }

    /*
    ======================================================
    Statistics
    ======================================================
    */

    handleStatistics(payload) {

        AppState.updateStatistics(

            payload.data

        );

        EventBus.emit(

            "statistics:update",

            payload.data

        );

    }

    /*
    ======================================================
    Risk
    ======================================================
    */

    handleRisk(payload) {

        AppState.merge(

            "risk",

            payload.data

        );

        EventBus.emit(

            "risk:update",

            payload.data

        );

    }

    /*
    ======================================================
    Weather
    ======================================================
    */

    handleWeather(payload) {

        AppState.updateWeather(

            payload.data

        );

        EventBus.emit(

            "weather:update",

            payload.data

        );

    }

    /*
    ======================================================
    Alerts
    ======================================================
    */

    handleAlert(payload) {

        AppState.addAlert(

            payload.data

        );

        EventBus.emit(

            "alert:new",

            payload.data

        );

    }

    /*
    ======================================================
    People
    ======================================================
    */

    handlePeople(payload) {

        EventBus.emit(

            "people:update",

            payload.data

        );

    }

    /*
    ======================================================
    Tracking
    ======================================================
    */

    handleTracking(payload) {

        EventBus.emit(

            "tracking:update",

            payload.data

        );

    }

    /*
    ======================================================
    Reports
    ======================================================
    */

    handleReport(payload) {

        AppState.addReport(

            payload.data

        );

        EventBus.emit(

            "report:new",

            payload.data

        );

    }

    /*
    ======================================================
    Backend
    ======================================================
    */

    handleBackend(payload) {

        AppState.updateBackend(

            payload.data

        );

        EventBus.emit(

            "backend:update",

            payload.data

        );

    }

    /*
    ======================================================
    Custom Messages
    ======================================================
    */

    handleCustom(payload) {

        if (

            !payload.type

        ) {

            return;

        }

        const handlers =

            this.handlers.get(

                payload.type

            );

        if (!handlers) {

            EventBus.emit(

                "websocket:unknown",

                payload

            );

            return;

        }

        handlers.forEach(

            callback =>

                callback(payload)

        );

    }

    /*
    ======================================================
    Request / Response
    ======================================================
    */

    request(

        type,

        data = {}

    ) {

        return new Promise((resolve) => {

            const id =

                ++this.requestCounter;

            this.pendingRequests.set(

                id,

                resolve

            );

            this.send({

                id,

                type,

                data

            });

        });

    }

    handleResponse(payload) {

        const callback =

            this.pendingRequests.get(

                payload.id

            );

        if (!callback) {

            return;

        }

        callback(payload.data);

        this.pendingRequests.delete(

            payload.id

        );

    }

    /*
    ======================================================
    Event Registration
    ======================================================
    */

    on(

        event,

        callback

    ) {

        if (

            !this.handlers.has(event)

        ) {

            this.handlers.set(

                event,

                []

            );

        }

        this.handlers

            .get(event)

            .push(callback);

    }

    off(

        event,

        callback

    ) {

        if (

            !this.handlers.has(event)

        ) {

            return;

        }

        const list =

            this.handlers.get(event);

        this.handlers.set(

            event,

            list.filter(

                handler =>

                    handler !== callback

            )

        );

    }

    subscribe(

        event,

        callback

    ) {

        this.on(

            event,

            callback

        );

    }

    unsubscribe(

        event,

        callback

    ) {

        this.off(

            event,

            callback

        );

    }

    onOpen(callback) {

        this.openCallbacks.push(

            callback

        );

    }

    onClose(callback) {

        this.closeCallbacks.push(

            callback

        );

    }

    onError(callback) {

        this.errorCallbacks.push(

            callback

        );

    }

    /*
    ======================================================
    Utilities
    ======================================================
    */

    isConnected() {

        return this.connected;

    }

    isConnecting() {

        return this.connecting;

    }

    latency() {

        return this.statistics.latency;

    }

    statisticsSnapshot() {

        return {

            ...this.statistics

        };

    }

    clear() {

        this.handlers.clear();

        this.pendingRequests.clear();

        this.openCallbacks = [];

        this.closeCallbacks = [];

        this.errorCallbacks = [];

    }

    destroy() {

        this.disconnect();

        this.clear();

        this.outgoingQueue = [];

    }

}

/*
============================================================
Singleton
============================================================
*/

export const websocket =

    new WebSocketManager();

export {

    WebSocketManager

};