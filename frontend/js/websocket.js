/*
============================================================
Astravon Live Arena
WebSocket Manager

Purpose:
    Handles all real-time communication between
    the frontend dashboard and the backend.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

export default class WebSocketManager {

    constructor() {

        /**
         * --------------------------------------
         * Configuration
         * --------------------------------------
         */

        this.url = "ws://127.0.0.1:8000/ws";

        this.socket = null;

        this.connected = false;

        this.reconnectDelay = 3000;

        this.maxReconnectAttempts = Infinity;

        this.reconnectAttempts = 0;

        /**
         * --------------------------------------
         * Event Callbacks
         * --------------------------------------
         */

        this.handlers = {};

        this.openCallbacks = [];

        this.closeCallbacks = [];

        this.errorCallbacks = [];

    }

    /*
    ==========================================================
    Connect
    ==========================================================
    */

    async connect() {

        return new Promise((resolve, reject) => {

            console.log(
                "[WebSocket] Connecting..."
            );

            this.socket = new WebSocket(
                this.url
            );

            this.socket.onopen = () => {

                console.log(
                    "[WebSocket] Connected."
                );

                this.connected = true;

                this.reconnectAttempts = 0;

                this.openCallbacks.forEach(
                    callback => callback()
                );

                resolve();

            };

            this.socket.onmessage = (event) => {

                this.receive(event.data);

            };

            this.socket.onerror = (error) => {

                console.error(
                    "[WebSocket] Error:",
                    error
                );

                this.errorCallbacks.forEach(
                    callback => callback(error)
                );

            };

            this.socket.onclose = () => {

                console.warn(
                    "[WebSocket] Disconnected."
                );

                this.connected = false;

                this.closeCallbacks.forEach(
                    callback => callback()
                );

                this.reconnect();

            };

        });

    }

    /*
    ==========================================================
    Disconnect
    ==========================================================
    */

    disconnect() {

        if (!this.socket) {

            return;

        }

        this.socket.close();

        this.connected = false;

    }

    /*
    ==========================================================
    Automatic Reconnection
    ==========================================================
    */

    reconnect() {

        if (
            this.reconnectAttempts >=
            this.maxReconnectAttempts
        ) {

            return;

        }

        this.reconnectAttempts++;

        console.log(

            `[WebSocket] Reconnecting (${this.reconnectAttempts})...`

        );

        setTimeout(() => {

            this.connect();

        }, this.reconnectDelay);

    }

    /*
    ==========================================================
    Send JSON
    ==========================================================
    */

    send(data) {

        if (!this.connected) {

            console.warn(
                "[WebSocket] Not connected."
            );

            return;

        }

        this.socket.send(
            JSON.stringify(data)
        );

    }

    /*
    ==========================================================
    Receive JSON
    ==========================================================
    */

    receive(message) {

        let payload;

        try {

            payload = JSON.parse(message);

        }

        catch (error) {

            console.warn(
                "[WebSocket] Invalid JSON received."
            );

            return;

        }

        /**
         * --------------------------------------
         * Message Type
         * --------------------------------------
         */

        const type = payload.type;

        const data = payload.data;

        if (
            type &&
            this.handlers[type]
        ) {

            this.handlers[type].forEach(

                callback => callback(data)

            );

        }

    }

    /*
    ==========================================================
    Register Event
    ==========================================================
    */

    on(
        event,
        callback
    ) {

        if (!this.handlers[event]) {

            this.handlers[event] = [];

        }

        this.handlers[event].push(
            callback
        );

    }

    /*
    ==========================================================
    Remove Event
    ==========================================================
    */

    off(
        event,
        callback
    ) {

        if (!this.handlers[event]) {

            return;

        }

        this.handlers[event] =

            this.handlers[event].filter(

                handler =>

                    handler !== callback

            );

    }

    /*
    ==========================================================
    Open Event
    ==========================================================
    */

    onOpen(callback) {

        this.openCallbacks.push(
            callback
        );

    }

    /*
    ==========================================================
    Close Event
    ==========================================================
    */

    onClose(callback) {

        this.closeCallbacks.push(
            callback
        );

    }

    /*
    ==========================================================
    Error Event
    ==========================================================
    */

    onError(callback) {

        this.errorCallbacks.push(
            callback
        );

    }

    /*
    ==========================================================
    Remove All Handlers
    ==========================================================
    */

    clear() {

        this.handlers = {};

        this.openCallbacks = [];

        this.closeCallbacks = [];

        this.errorCallbacks = [];

    }

    /*
    ==========================================================
    Connection Status
    ==========================================================
    */

    isConnected() {

        return this.connected;

    }

}