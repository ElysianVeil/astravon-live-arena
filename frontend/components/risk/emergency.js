/*
============================================================
Astravon Live Arena
Emergency Manager

Purpose:
    Coordinates emergency states across the
    Astravon Live Arena platform.

Responsibilities
    • Emergency activation
    • Emergency cancellation
    • Escalation levels
    • Emergency banner
    • Emergency listeners
    • Emergency history

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

class EmergencyManager {

    constructor() {

        this.active = false;

        this.level = "none";

        this.message = "";

        this.startedAt = null;

        this.history = [];

        this.listeners = [];

        this.banner = null;

        this.messageElement = null;

    }

    /*==========================================================
        Initialization
    ==========================================================*/

    initialize() {

        this.banner =
            document.getElementById(
                "emergencyBanner"
            );

        this.messageElement =
            document.getElementById(
                "emergencyMessage"
            );

    }

    /*==========================================================
        Activate
    ==========================================================*/

    activate({

        level = "critical",

        message = "Emergency detected.",

        source = "AI Engine"

    } = {}) {

        this.active = true;

        this.level = level;

        this.message = message;

        this.startedAt = new Date();

        this.history.unshift({

            level,

            message,

            source,

            timestamp: this.startedAt

        });

        this.render();

        this.notify();

    }

    /*==========================================================
        Resolve
    ==========================================================*/

    resolve() {

        this.active = false;

        this.level = "none";

        this.message = "";

        this.startedAt = null;

        this.render();

        this.notify();

    }

    /*==========================================================
        Escalate
    ==========================================================*/

    escalate() {

        if (!this.active) return;

        switch (this.level) {

            case "low":

                this.level = "medium";
                break;

            case "medium":

                this.level = "high";
                break;

            case "high":

                this.level = "critical";
                break;

        }

        this.render();

        this.notify();

    }

    /*==========================================================
        Downgrade
    ==========================================================*/

    downgrade() {

        if (!this.active) return;

        switch (this.level) {

            case "critical":

                this.level = "high";
                break;

            case "high":

                this.level = "medium";
                break;

            case "medium":

                this.level = "low";
                break;

        }

        this.render();

        this.notify();

    }

    /*==========================================================
        Banner
    ==========================================================*/

    render() {

        if (!this.banner) return;

        if (!this.active) {

            this.banner.classList.add("hidden");

            return;

        }

        this.banner.classList.remove("hidden");

        this.banner.className = "";

        this.banner.classList.add(
            "emergency-banner",
            this.level
        );

        if (this.messageElement) {

            this.messageElement.textContent =
                `${this.level.toUpperCase()} • ${this.message}`;

        }

    }

    /*==========================================================
        Getters
    ==========================================================*/

    isActive() {

        return this.active;

    }

    getLevel() {

        return this.level;

    }

    getMessage() {

        return this.message;

    }

    getDuration() {

        if (!this.startedAt) return 0;

        return Date.now() -

            this.startedAt.getTime();

    }

    getHistory() {

        return [...this.history];

    }

    clearHistory() {

        this.history = [];

    }

    getSnapshot() {

        return {

            active: this.active,

            level: this.level,

            message: this.message,

            duration: this.getDuration(),

            history: this.getHistory()

        };

    }

    /*==========================================================
        Events
    ==========================================================*/

    subscribe(callback) {

        this.listeners.push(callback);

    }

    unsubscribe(callback) {

        this.listeners =
            this.listeners.filter(

                listener => listener !== callback

            );

    }

    notify() {

        const snapshot =
            this.getSnapshot();

        this.listeners.forEach(

            listener => listener(snapshot)

        );

    }

}

/*============================================================
Singleton
============================================================*/

const emergencyManager =
    new EmergencyManager();

export default emergencyManager;

export {

    EmergencyManager

};