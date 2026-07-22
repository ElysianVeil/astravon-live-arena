/*
============================================================
Astravon Live Arena
Movement Analytics Component

Purpose:
    Tracks crowd movement, calculates average speed,
    movement direction, flow trends and updates the
    movement chart and dashboard statistics.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

import { StatisticsManager } from "./statistics.js";
import charts from "./charts.js";

class MovementAnalytics {

    constructor() {

        this.chart = null;

        this.chartId = "movementChart";

        this.currentSpeed = 0;

        this.direction = "Stationary";

        this.flow = "Normal";

        this.history = [];

    }

    /*==========================================================
        Update Movement
    ==========================================================*/

    update(data = {}) {

        this.currentSpeed = Number(data.speed ?? 0);

        this.direction = data.direction ?? "Unknown";

        this.flow = this.calculateFlow(this.currentSpeed);

        this.history.push({

            time: new Date().toLocaleTimeString(),

            speed: this.currentSpeed

        });

        if (this.history.length > 30) {

            this.history.shift();

        }

        // this.renderStatistics();

        this.renderChart();

    }

    /*==========================================================
        Flow Classification
    ==========================================================*/

    calculateFlow(speed) {

        if (speed <= 0.2) {

            return "Stationary";

        }

        if (speed <= 0.8) {

            return "Slow";

        }

        if (speed <= 1.5) {

            return "Normal";

        }

        if (speed <= 2.5) {

            return "Fast";

        }

        return "Running";

    }

    /*==========================================================
        Flow Colour
    ==========================================================*/

    getFlowColor() {

        switch (this.flow) {

            case "Running":
                return "#EF4444";

            case "Fast":
                return "#F59E0B";

            case "Normal":
                return "#22C55E";

            case "Slow":
                return "#3B82F6";

            default:
                return "#9CA3AF";

        }

    }

    /*==========================================================
        Statistics
    ==========================================================*/

    // renderStatistics() {

    //     Statistics.set(

    //         "Movement Speed",

    //         `${this.currentSpeed.toFixed(2)} m/s`

    //     );

    //     Statistics.set(

    //         "Direction",

    //         this.direction

    //     );

    //     Statistics.set(

    //         "Flow",

    //         this.flow

    //     );

    // }

    /*==========================================================
        Chart
    ==========================================================*/

    renderChart() {

        const labels = this.history.map(item => item.time);

        const values = this.history.map(item => item.speed);

        charts.update(
            this.chartId,
            labels,
            [
                charts.lineDataset(
                    "Movement Speed",
                    values,
                    "#3B82F6"
                )
            ]
        );

    }

    /*==========================================================
        Reset
    ==========================================================*/

    reset() {

        this.currentSpeed = 0;

        this.direction = "Stationary";

        this.flow = "Normal";

        this.history = [];

        this.renderChart();

    }

    /*==========================================================
        Export
    ==========================================================*/

    exportData() {

        return {

            speed: this.currentSpeed,

            direction: this.direction,

            flow: this.flow,

            history: [...this.history]

        };

    }

}

export const Movement = new MovementAnalytics();

export default Movement;