/*
============================================================
Astravon Live Arena
Occupancy Analytics Component
============================================================
*/

import charts from "./charts.js";
import EventBus from "../../js/event_bus.js";
import State from "../../js/state.js";

class OccupancyAnalytics {

    constructor() {

        this.chartId = "occupancyChart";

        this.maxCapacity = 1000;

        this.currentOccupancy = 0;

        this.history = [];

        this.chartCreated = false;

    }

    /*
    ==========================================================
    Initialize
    ==========================================================
    */

    initialize() {

        this.container =
            document.getElementById("occupancy");

        // Create the chart once
        if (!this.chartCreated) {

            charts.create(this.chartId, {

                type: "line",

                data: {

                    labels: [],

                    datasets: [

                        charts.lineDataset(
                            "Occupancy",
                            [],
                            "#D4AF37"
                        )

                    ]

                }

            });

            this.chartCreated = true;

        }

        // Cached statistics
        const statistics = State.get("statistics");

        if (statistics) {

            this.update(statistics);

        }

        // Live statistics
        EventBus.on(
            "statistics:update",
            statistics => this.update(statistics)
        );

    }

    /*
    ==========================================================
    Capacity
    ==========================================================
    */

    setCapacity(capacity) {

        this.maxCapacity = capacity;

    }

    /*
    ==========================================================
    Update
    ==========================================================
    */

    update(statistics) {

        if (!statistics) return;

        this.currentOccupancy =
            statistics?.occupancy?.people_inside ??
            statistics?.detection?.people_count ??
            0;

        this.history.push({

            time: new Date().toLocaleTimeString(),

            value: this.currentOccupancy

        });

        if (this.history.length > 30) {

            this.history.shift();

        }

        // this.renderStatistics();

        this.renderChart();

    }

    /*
    ==========================================================
    Percentage
    ==========================================================
    */

    getPercentage() {

        if (this.maxCapacity <= 0) {

            return 0;

        }

        return (

            this.currentOccupancy /

            this.maxCapacity *

            100

        ).toFixed(1);

    }

    /*
    ==========================================================
    Status
    ==========================================================
    */

    getStatus() {

        const value = Number(this.getPercentage());

        if (value >= 90) return "Critical";

        if (value >= 70) return "High";

        if (value >= 40) return "Moderate";

        return "Low";

    }

    /*
    ==========================================================
    Statistics
    ==========================================================
    */

    // renderStatistics() {

    //     const people =
    //         document.getElementById("occupancyPeople");

    //     const percent =
    //         document.getElementById("occupancyPercent");

    //     const status =
    //         document.getElementById("occupancyStatus");

    //     if (people) {

    //         people.textContent =
    //             this.currentOccupancy;

    //     }

    //     if (percent) {

    //         percent.textContent =
    //             `${this.getPercentage()}%`;

    //     }

    //     if (status) {

    //         status.textContent =
    //             this.getStatus();

    //     }

    // }

    /*
    ==========================================================
    Chart
    ==========================================================
    */

    renderChart() {

        charts.update(

            this.chartId,

            this.history.map(item => item.time),

            [

                charts.lineDataset(

                    "Occupancy",

                    this.history.map(item => item.value),

                    "#D4AF37"

                )

            ]

        );

    }

    /*
    ==========================================================
    Reset
    ==========================================================
    */

    reset() {

        this.currentOccupancy = 0;

        this.history = [];

        this.renderChart();

    }

    /*
    ==========================================================
    Export
    ==========================================================
    */

    exportData() {

        return {

            occupancy: this.currentOccupancy,

            capacity: this.maxCapacity,

            percentage: this.getPercentage(),

            status: this.getStatus(),

            history: [...this.history]

        };

    }

}

const Occupancy = new OccupancyAnalytics();

export default Occupancy;

export { OccupancyAnalytics };