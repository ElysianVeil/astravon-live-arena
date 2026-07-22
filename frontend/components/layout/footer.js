/*
============================================================
Astravon Live Arena
Footer Component

Purpose
    Application footer for the Live Arena dashboard.

Author
    House of Astravon

Version
    2.0.0
============================================================
*/

export default class Footer {

    constructor() {

        this.container = null;

        this.version = "1.0.0";

        this.backendStatus = "Offline";

        this.aiStatus = "Offline";

        this.websocketStatus = "Disconnected";

        this.currentEvent = "Simulation";

        this.build = "Stable";

    }

    /*
    ==========================================================
    Initialize
    ==========================================================
    */

    initialize() {

        this.container = document.getElementById("footer");

        if (!this.container) {

            console.warn("[Footer] Container not found.");

            return;

        }

        this.render();

    }

    /*
    ==========================================================
    Render
    ==========================================================
    */

    render() {

        const year = new Date().getFullYear();

        this.container.innerHTML = `

        <footer class="footer">

            <div class="footer-left">

                <div class="footer-brand">

                    <strong>Astravon Live Arena</strong>

                </div>

                <div class="footer-meta">

                    Version ${this.version}

                    <span class="footer-divider">•</span>

                    ${this.build}

                </div>

            </div>

            <div class="footer-center">

                <div class="footer-status">

                    <span class="status-pill ${this.getStatusClass(this.backendStatus)}">

                        Backend

                    </span>

                    <span>

                        ${this.backendStatus}

                    </span>

                </div>

                <div class="footer-status">

                    <span class="status-pill ${this.getStatusClass(this.aiStatus)}">

                        AI

                    </span>

                    <span>

                        ${this.aiStatus}

                    </span>

                </div>

                <div class="footer-status">

                    <span class="status-pill ${this.getStatusClass(this.websocketStatus)}">

                        WS

                    </span>

                    <span>

                        ${this.websocketStatus}

                    </span>

                </div>

            </div>

            <div class="footer-right">

                <div>

                    Event:

                    <strong>

                        ${this.currentEvent}

                    </strong>

                </div>

                <div>

                    © ${year} House of Astravon

                </div>

            </div>

        </footer>

        `;

    }

    /*
    ==========================================================
    Helpers
    ==========================================================
    */

    getStatusClass(status) {

        const value = status.toLowerCase();

        if (
            value.includes("online") ||
            value.includes("connected") ||
            value.includes("running")
        ) {

            return "online";

        }

        if (
            value.includes("warning")
        ) {

            return "warning";

        }

        return "offline";

    }

    /*
    ==========================================================
    Backend
    ==========================================================
    */

    setBackendStatus(status) {

        this.backendStatus = status;

        this.render();

    }

    /*
    ==========================================================
    AI
    ==========================================================
    */

    setAIStatus(status) {

        this.aiStatus = status;

        this.render();

    }

    /*
    ==========================================================
    WebSocket
    ==========================================================
    */

    setWebSocketStatus(status) {

        this.websocketStatus = status;

        this.render();

    }

    /*
    ==========================================================
    Version
    ==========================================================
    */

    setVersion(version) {

        this.version = version;

        this.render();

    }

    /*
    ==========================================================
    Build
    ==========================================================
    */

    setBuild(build) {

        this.build = build;

        this.render();

    }

    /*
    ==========================================================
    Event
    ==========================================================
    */

    setEvent(eventName) {

        this.currentEvent = eventName;

        this.render();

    }

    /*
    ==========================================================
    Update Everything
    ==========================================================
    */

    update({

        backend,

        ai,

        websocket,

        version,

        build,

        event

    }) {

        if (backend !== undefined) {

            this.backendStatus = backend;

        }

        if (ai !== undefined) {

            this.aiStatus = ai;

        }

        if (websocket !== undefined) {

            this.websocketStatus = websocket;

        }

        if (version !== undefined) {

            this.version = version;

        }

        if (build !== undefined) {

            this.build = build;

        }

        if (event !== undefined) {

            this.currentEvent = event;

        }

        this.render();

    }

}