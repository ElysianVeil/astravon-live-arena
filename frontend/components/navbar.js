/*
============================================================
Astravon Live Arena
Navigation Bar Component

Purpose:
    Creates and manages the top navigation bar
    for the dashboard.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

export default class Navbar {

    constructor() {

        this.container = null;

        this.currentTimeElement = null;

        this.connectionBadge = null;

        this.eventModeBadge = null;

        this.clockTimer = null;

    }

    /*
    ==========================================================
    Initialize
    ==========================================================
    */

    initialize() {

        this.container = document.getElementById(
            "navbar"
        );

        if (!this.container) {

            console.warn(
                "[Navbar] Container not found."
            );

            return;

        }

        this.render();

        this.startClock();

        console.log(
            "[Navbar] Initialized."
        );

    }

    /*
    ==========================================================
    Render
    ==========================================================
    */

    render() {

        this.container.innerHTML = `

            <div class="navbar">

                <div class="navbar-left">

                    <div class="navbar-logo">

                        🌌 Astravon Live Arena

                    </div>

                    <div class="navbar-version">

                        v1.0.0

                    </div>

                </div>

                <div class="navbar-center">

                    <span
                        id="eventMode"
                        class="event-mode"
                    >

                        Training

                    </span>

                </div>

                <div class="navbar-right">

                    <span
                        id="connectionStatus"
                        class="connection disconnected"
                    >

                        ● Offline

                    </span>

                    <span
                        id="currentTime"
                        class="current-time"
                    >

                        --:--:--

                    </span>

                </div>
                
            </div>

        `;

        this.currentTimeElement =

            document.getElementById(
                "currentTime"
            );

        this.connectionBadge =

            document.getElementById(
                "connectionStatus"
            );

        this.eventModeBadge =

            document.getElementById(
                "eventMode"
            );

    }

    /*
    ==========================================================
    Clock
    ==========================================================
    */

    startClock() {

        this.updateClock();

        this.clockTimer = setInterval(

            () => {

                this.updateClock();

            },

            1000

        );

    }

    updateClock() {

        if (!this.currentTimeElement) {

            return;

        }

        this.currentTimeElement.textContent =

            new Date().toLocaleTimeString();

    }

    /*
    ==========================================================
    Connection Status
    ==========================================================
    */

    setConnected() {

        if (!this.connectionBadge) {

            return;

        }

        this.connectionBadge.textContent =

            "● Connected";

        this.connectionBadge.className =

            "connection connected";

    }

    setDisconnected() {

        if (!this.connectionBadge) {

            return;

        }

        this.connectionBadge.textContent =

            "● Offline";

        this.connectionBadge.className =

            "connection disconnected";

    }

    /*
    ==========================================================
    Event Mode
    ==========================================================
    */

    setEventMode(name) {

        if (!this.eventModeBadge) {

            return;

        }

        this.eventModeBadge.textContent =

            name;

    }

    /*
    ==========================================================
    Version
    ==========================================================
    */

    setVersion(version) {

        const versionElement =

            this.container.querySelector(
                ".navbar-version"
            );

        if (!versionElement) {

            return;

        }

        versionElement.textContent =

            version;

    }

    /*
    ==========================================================
    Destroy
    ==========================================================
    */

    destroy() {

        if (this.clockTimer) {

            clearInterval(
                this.clockTimer
            );

        }

    }

}