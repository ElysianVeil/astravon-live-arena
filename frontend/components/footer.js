/*
============================================================
Astravon Live Arena
Footer Component

Purpose:
    Displays the application footer with
    version, system status, copyright,
    and useful links.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

export default class Footer {

    constructor() {

        this.container = null;

        this.version = "1.0.0";

        this.backendStatus = "Offline";

        this.aiStatus = "Offline";

        this.websocketStatus = "Disconnected";

    }

    /*
    ==========================================================
    Initialize
    ==========================================================
    */

    initialize() {

        this.container = document.getElementById(
            "footer"
        );

        if (!this.container) {

            console.warn(
                "[Footer] Container not found."
            );

            return;

        }

        this.render();

        console.log(
            "[Footer] Initialized."
        );

    }

    /*
    ==========================================================
    Render
    ==========================================================
    */

    render() {

        if (!this.container) {

            return;

        }

        const year =

            new Date().getFullYear();

        this.container.innerHTML = `

            <footer class="footer">

                <div class="footer-left">

                    <div class="footer-title">

                        Astravon Live Arena

                    </div>

                    <div class="footer-version">

                        Version ${this.version}

                    </div>

                </div>

                <div class="footer-center">

                    <span>

                        Backend:
                        <strong>
                            ${this.backendStatus}
                        </strong>

                    </span>

                    <span>

                        AI Engine:
                        <strong>
                            ${this.aiStatus}
                        </strong>

                    </span>

                    <span>

                        WebSocket:
                        <strong>
                            ${this.websocketStatus}
                        </strong>

                    </span>

                </div>

                <div class="footer-right">

                    © ${year}

                    House of Astravon

                </div>

            </footer>

        `;

    }

    /*
    ==========================================================
    Backend Status
    ==========================================================
    */

    setBackendStatus(status) {

        this.backendStatus = status;

        this.render();

    }

    /*
    ==========================================================
    AI Engine Status
    ==========================================================
    */

    setAIStatus(status) {

        this.aiStatus = status;

        this.render();

    }

    /*
    ==========================================================
    WebSocket Status
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
    All Statuses
    ==========================================================
    */

    update({

        backend,

        ai,

        websocket

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

        this.render();

    }

}