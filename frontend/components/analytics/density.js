/*
============================================================
Astravon Live Arena
Density Analytics Component

Purpose:
    Handles crowd density analytics, density charts,
    density calculations, occupancy estimation and
    live density monitoring.

Author:
    House of Astravon
============================================================
*/

import charts from "./charts.js";
import eventBus from "../../js/event_bus.js";
import state from "../../js/state.js";

class DensityManager {

    constructor() {

        this.chartId = "densityChart";

        this.labels = [];

        this.values = [];

        this.currentDensity = 0;

        this.maxHistory = 30;

        this.levels = {
            LOW: "Low",
            MODERATE: "Moderate",
            HIGH: "High",
            CRITICAL: "Critical"
        };

    }

    /*
    ============================================================
    Initialize
    ============================================================
    */

    initialize() {

        charts.createDensityChart(this.chartId);

    }

    /*
    ============================================================
    Update
    ============================================================
    */

    update(data = {}) {

        const density = Number(data.density ?? 0);

        const label = data.time ?? this.currentTime();

        this.currentDensity = density;

        this.labels.push(label);

        this.values.push(density);

        if (this.labels.length > this.maxHistory) {

            this.labels.shift();

            this.values.shift();

        }

        charts.update(

            this.chartId,

            [...this.labels],

            [

                charts.barDataset(

                    "Crowd Density",

                    [...this.values],

                    this.getDensityColor(density)

                )

            ]

        );

    }

    /*
    ============================================================
    Density Level
    ============================================================
    */

    getDensityLevel(value = this.currentDensity) {

        if (value < 30) {

            return this.levels.LOW;

        }

        if (value < 60) {

            return this.levels.MODERATE;

        }

        if (value < 85) {

            return this.levels.HIGH;

        }

        return this.levels.CRITICAL;

    }

    /*
    ============================================================
    Density Color
    ============================================================
    */

    getDensityColor(value = this.currentDensity) {

        if (value < 30) {

            return "#22C55E";

        }

        if (value < 60) {

            return "#3B82F6";

        }

        if (value < 85) {

            return "#F59E0B";

        }

        return "#EF4444";

    }

    /*
    ============================================================
    Occupancy Percentage
    ============================================================
    */

    calculateOccupancy(currentPeople, capacity) {

        if (!capacity || capacity <= 0) {

            return 0;

        }

        return Number(

            ((currentPeople / capacity) * 100)

            .toFixed(1)

        );

    }

    /*
    ============================================================
    People Per Square Meter
    ============================================================
    */

    peoplePerSquareMeter(people, area) {

        if (!area || area <= 0) {

            return 0;

        }

        return Number(

            (people / area)

            .toFixed(2)

        );

    }

    /*
    ============================================================
    Status Object
    ============================================================
    */

    getStatus() {

        return {

            density: this.currentDensity,

            level: this.getDensityLevel(),

            color: this.getDensityColor(),

            history: [...this.values]

        };

    }

    /*
    ============================================================
    Reset
    ============================================================
    */

    reset() {

        this.labels = [];

        this.values = [];

        this.currentDensity = 0;

        charts.update(

            this.chartId,

            [],

            [

                charts.barDataset(

                    "Crowd Density",

                    [],

                    "#3B82F6"

                )

            ]

        );

    }

    /*
    ============================================================
    Utilities
    ============================================================
    */

    currentTime() {

        return new Date().toLocaleTimeString([], {

            hour: "2-digit",

            minute: "2-digit"

        });

    }

}

const density = new DensityManager();

export default density;