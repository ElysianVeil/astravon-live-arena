/*
============================================================
Astravon Live Arena
Alert Manager

Purpose:
    Manages dashboard alerts, notifications,
    warning banners and emergency events.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

export default class AlertManager {

    constructor() {

        /*
        =====================================================
        Configuration
        =====================================================
        */

        this.maxAlerts = 50;

        this.alerts = [];

        this.container = null;

        this.soundEnabled = true;

    }

    /*
    ==========================================================
    Initialize
    ==========================================================
    */

    initialize() {

        this.container = document.getElementById(
            "alertContainer"
        );

        console.log(
            "[Alerts] Initialized."
        );

    }

    /*
    ==========================================================
    Add Alert
    ==========================================================
    */

    add(

        title,
        message,
        level = "info"

    ) {

        const alert = {

            id: Date.now(),

            title,

            message,

            level,

            timestamp: new Date()

        };

        this.alerts.unshift(alert);

        if (

            this.alerts.length >

            this.maxAlerts

        ) {

            this.alerts.pop();

        }

        this.render();

        this.playSound(level);

    }

    /*
    ==========================================================
    Success
    ==========================================================
    */

    success(message) {

        this.add(

            "Success",

            message,

            "success"

        );

    }

    /*
    ==========================================================
    Information
    ==========================================================
    */

    info(message) {

        this.add(

            "Information",

            message,

            "info"

        );

    }

    /*
    ==========================================================
    Warning
    ==========================================================
    */

    warning(message) {

        this.add(

            "Warning",

            message,

            "warning"

        );

    }

    /*
    ==========================================================
    Emergency
    ==========================================================
    */

    emergency(message) {

        this.add(

            "Emergency",

            message,

            "danger"

        );

    }

    /*
    ==========================================================
    Crowd Risk
    ==========================================================
    */

    crowdRisk(statistics) {

        if (

            statistics.risk_score >= 80

        ) {

            this.emergency(

                "Critical crowd risk detected."

            );

        }

        else if (

            statistics.risk_score >= 60

        ) {

            this.warning(

                "Crowd risk is increasing."

            );

        }

    }

    /*
    ==========================================================
    Heat Warning
    ==========================================================
    */

    heatWarning(statistics) {

        if (

            statistics.heat_index >= 35

        ) {

            this.warning(

                "Dangerous heat index."

            );

        }

    }

    /*
    ==========================================================
    Occupancy Warning
    ==========================================================
    */

    occupancyWarning(statistics) {

        if (

            statistics.occupancy >= 90

        ) {

            this.emergency(

                "Venue occupancy exceeded."

            );

        }

        else if (

            statistics.occupancy >= 75

        ) {

            this.warning(

                "Venue nearing capacity."

            );

        }

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

        this.container.innerHTML = "";

        this.alerts.forEach(

            alert => {

                const element =

                    document.createElement(
                        "div"
                    );

                element.className =

                    `alert ${alert.level}`;

                element.innerHTML = `

                    <div class="alert-title">

                        ${alert.title}

                    </div>

                    <div class="alert-message">

                        ${alert.message}

                    </div>

                    <div class="alert-time">

                        ${alert.timestamp.toLocaleTimeString()}

                    </div>

                `;

                this.container.appendChild(

                    element

                );

            }

        );

    }

    /*
    ==========================================================
    Clear Alerts
    ==========================================================
    */

    clear() {

        this.alerts = [];

        this.render();

    }

    /*
    ==========================================================
    Toggle Sound
    ==========================================================
    */

    enableSound() {

        this.soundEnabled = true;

    }

    disableSound() {

        this.soundEnabled = false;

    }

    /*
    ==========================================================
    Play Notification
    ==========================================================
    */

    playSound(level) {

        if (!this.soundEnabled) {

            return;

        }

        /*
        Future:
            Different alarm sounds
            for warning, danger,
            evacuation, fire,
            medical emergencies.
        */

        console.log(

            `[Alert Sound] ${level}`

        );

    }

}