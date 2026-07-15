/*
============================================================
Astravon Live Arena
Event Modes Manager

Purpose:
    Controls the operating mode of the AI Engine
    and dashboard depending on the event type.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

export default class EventModeManager {

    constructor() {

        /*
        =====================================================
        Available Modes
        =====================================================
        */

        this.modes = {

            concert: {
                name: "Concert",
                occupancyLimit: 90,
                riskThreshold: 75,
                emergencyVehicles: 3,
                color: "#C084FC"
            },

            football: {
                name: "Football Match",
                occupancyLimit: 95,
                riskThreshold: 80,
                emergencyVehicles: 5,
                color: "#22C55E"
            },

            basketball: {
                name: "Basketball Game",
                occupancyLimit: 90,
                riskThreshold: 75,
                emergencyVehicles: 3,
                color: "#F97316"
            },

            conference: {
                name: "Conference",
                occupancyLimit: 80,
                riskThreshold: 60,
                emergencyVehicles: 2,
                color: "#3B82F6"
            },

            exhibition: {
                name: "Exhibition",
                occupancyLimit: 85,
                riskThreshold: 65,
                emergencyVehicles: 2,
                color: "#14B8A6"
            },

            festival: {
                name: "Festival",
                occupancyLimit: 95,
                riskThreshold: 85,
                emergencyVehicles: 6,
                color: "#EF4444"
            },

            training: {
                name: "Training / Demo",
                occupancyLimit: 40,
                riskThreshold: 40,
                emergencyVehicles: 1,
                color: "#6B7280"
            }

        };

        /*
        =====================================================
        Current Mode
        =====================================================
        */

        this.currentMode = this.modes.training;

    }

    /*
    ==========================================================
    Initialize
    ==========================================================
    */

    initialize() {

        console.log(
            "[Event Mode] Initialized."
        );

        this.render();

    }

    /*
    ==========================================================
    Set Mode
    ==========================================================
    */

    setMode(mode) {

        if (!(mode in this.modes)) {

            console.warn(
                `Unknown mode: ${mode}`
            );

            return;

        }

        this.currentMode = this.modes[mode];

        console.log(

            `[Event Mode] ${this.currentMode.name}`

        );

        this.render();

    }

    /*
    ==========================================================
    Current Mode
    ==========================================================
    */

    getMode() {

        return this.currentMode;

    }

    /*
    ==========================================================
    Risk Threshold
    ==========================================================
    */

    getRiskThreshold() {

        return this.currentMode.riskThreshold;

    }

    /*
    ==========================================================
    Occupancy Limit
    ==========================================================
    */

    getOccupancyLimit() {

        return this.currentMode.occupancyLimit;

    }

    /*
    ==========================================================
    Emergency Vehicles
    ==========================================================
    */

    getEmergencyVehicles() {

        return this.currentMode.emergencyVehicles;

    }

    /*
    ==========================================================
    Validate Statistics
    ==========================================================
    */

    evaluate(statistics) {

        const warnings = [];

        if (

            statistics.occupancy >=
            this.currentMode.occupancyLimit

        ) {

            warnings.push(

                "Venue occupancy exceeded."

            );

        }

        if (

            statistics.risk_score >=
            this.currentMode.riskThreshold

        ) {

            warnings.push(

                "Risk threshold exceeded."

            );

        }

        return warnings;

    }

    /*
    ==========================================================
    Update Dashboard Badge
    ==========================================================
    */

    render() {

        const badge =

            document.getElementById(
                "eventMode"
            );

        if (!badge) {

            return;

        }

        badge.textContent =

            this.currentMode.name;

        badge.style.background =

            this.currentMode.color;

    }

    /*
    ==========================================================
    Reset
    ==========================================================
    */

    reset() {

        this.currentMode =

            this.modes.training;

        this.render();

    }

}