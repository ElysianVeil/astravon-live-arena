/*
============================================================
Astravon Live Arena
Navigation Bar Component

Purpose:
    Creates and manages the top navigation bar.

Author:
    House of Astravon
Version:
    1.1.0
============================================================
*/

export default class Navbar {

    constructor() {

        this.container = null;

        this.currentTimeElement = null;

        this.connectionBadge = null;

        this.eventModeBadge = null;

        this.clockTimer = null;

        this.version = "v1.0.0";

    }

    /*==========================================================
        Initialize
    ==========================================================*/

    initialize() {

        this.container =
            document.getElementById("navbar");

        if (!this.container) {

            console.warn("[Navbar] Container missing.");

            return;

        }

        this.render();

        this.cache();

        this.startClock();

    }

    /*==========================================================
        Cache
    ==========================================================*/

    cache() {

        this.currentTimeElement =
            document.getElementById("currentTime");

        this.connectionBadge =
            document.getElementById("connectionStatus");

        this.eventModeBadge =
            document.getElementById("eventMode");

    }

    /*==========================================================
        Render
    ==========================================================*/

    render() {

        this.container.innerHTML = `

            <!-- ================= Left ================= -->

            <div class="navbar-left">

                <div class="navbar-brand">

                    <div class="navbar-logo">

                        🌌

                    </div>

                    <div class="navbar-title">

                        <h1>

                            Astravon Live Arena

                        </h1>

                        <small>

                            Intelligent Crowd Monitoring Platform

                        </small>

                    </div>

                </div>

            </div>

            <!-- ================= Center ================= -->

            <div class="navbar-center">

                <div
                    id="eventMode"
                    class="mode-badge"
                >

                    Training Mode

                </div>

            </div>

            <!-- ================= Right ================= -->

            <div class="navbar-right">

                <div
                    id="connectionStatus"
                    class="status-pill disconnected"
                >

                    ● Offline

                </div>

                <div class="navbar-divider"></div>

                <div class="navbar-clock">

                    🕒

                    <span id="currentTime">

                        --:--:--

                    </span>

                </div>

                <div class="navbar-divider"></div>

                <div class="navbar-version">

                    ${this.version}

                </div>

            </div>

        `;

    }

    /*==========================================================
        Clock
    ==========================================================*/

    startClock() {

        this.updateClock();

        this.clockTimer = setInterval(

            () => this.updateClock(),

            1000

        );

    }

    updateClock() {

        if (!this.currentTimeElement) return;

        this.currentTimeElement.textContent =

            new Date().toLocaleTimeString(

                [],

                {

                    hour: "2-digit",

                    minute: "2-digit",

                    second: "2-digit"

                }

            );

    }

    /*==========================================================
        Connection
    ==========================================================*/

    setConnected() {

        if (!this.connectionBadge) return;

        this.connectionBadge.textContent =

            "● Connected";

        this.connectionBadge.className =

            "status-pill connected";

    }

    setDisconnected() {

        if (!this.connectionBadge) return;

        this.connectionBadge.textContent =

            "● Offline";

        this.connectionBadge.className =

            "status-pill disconnected";

    }

    /*==========================================================
        Event Mode
    ==========================================================*/

    setEventMode(mode) {

        if (!this.eventModeBadge) return;

        this.eventModeBadge.textContent = mode;

    }

    /*==========================================================
        Version
    ==========================================================*/

    setVersion(version) {

        this.version = version;

        const element =

            this.container.querySelector(

                ".navbar-version"

            );

        if (element) {

            element.textContent = version;

        }

    }

    /*==========================================================
        Destroy
    ==========================================================*/

    destroy() {

        if (this.clockTimer) {

            clearInterval(this.clockTimer);

            this.clockTimer = null;

        }

    }

}