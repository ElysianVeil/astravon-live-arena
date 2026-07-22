/*
============================================================
Astravon Live Arena
Congestion Analytics Component

Purpose:
    Monitors crowd congestion levels, calculates congestion
    percentage, determines congestion status, tracks history,
    and renders congestion statistics and charts.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

import { StatisticsManager } from "./statistics.js";
import charts from "./charts.js";

class CongestionAnalytics {

    constructor() {

        this.chart = null;

        this.chartId = "congestionChart";

        this.congestion = 0;

        this.history = [];

        this.maximumDensity = 10;

    }

    initialize() {

        charts.create(this.chartId, {

            type: "line",

            data: {

                labels: [],

                datasets: [

                    charts.lineDataset(
                        "Congestion",
                        [],
                        "#EF4444"
                    )

                ]

            }

        });

    }

    /*==========================================================
        Configuration
    ==========================================================*/

    setMaximumDensity(value = 10) {

        this.maximumDensity = value;

    }

    /*==========================================================
        Update
    ==========================================================*/

    update(statistics) {

        if (!statistics) return;

        this.congestion =
            statistics?.congestion?.congestion_level ??
            statistics?.congestion?.percentage ??
            0;

        this.history.push({

            time: new Date().toLocaleTimeString(),

            value: this.congestion

        });

        if (this.history.length > 30) {

            this.history.shift();

        }

        // this.renderStatistics();

        this.renderChart();

    }

    /*==========================================================
        Congestion Percentage
    ==========================================================*/

    getPercentage() {

        if (this.maximumDensity <= 0) {

            return 0;

        }

        return Number(

            (this.congestion / this.maximumDensity) * 100

        ).toFixed(1);

    }

    /*==========================================================
        Congestion Status
    ==========================================================*/

    getStatus() {

        const percentage = Number(this.getPercentage());

        if (percentage >= 90) {

            return "Severe";

        }

        if (percentage >= 70) {

            return "High";

        }

        if (percentage >= 45) {

            return "Moderate";

        }

        if (percentage >= 20) {

            return "Low";

        }

        return "Minimal";

    }

    /*==========================================================
        Color
    ==========================================================*/

    getColor() {

        const percentage = Number(this.getPercentage());

        if (percentage >= 90) return "#EF4444";

        if (percentage >= 70) return "#F59E0B";

        if (percentage >= 45) return "#D4AF37";

        return "#22C55E";

    }

    /*==========================================================
        Statistics
    ==========================================================*/

    // renderStatistics() {

    //     Statistics.set(

    //         "Congestion",

    //         this.congestion.toFixed(2)

    //     );

    //     Statistics.set(

    //         "Congestion Level",

    //         `${this.getPercentage()}%`

    //     );

    //     Statistics.set(

    //         "Congestion Status",

    //         this.getStatus()

    //     );

    // }

    /*==========================================================
        Chart
    ==========================================================*/

    renderChart() {

        const labels = this.history.map(item => item.time);

        const values = this.history.map(item => item.value);

        charts.update(
            this.chartId,
            labels,
            [
                charts.lineDataset(
                    "Congestion",
                    values,
                    this.getColor()
                )
            ]
        );

    }

    /*==========================================================
        Reset
    ==========================================================*/

    reset() {

        this.congestion = 0;

        this.history = [];

        this.renderChart();

    }

    /*==========================================================
        Export
    ==========================================================*/

    exportData() {

        return {

            congestion: this.congestion,

            percentage: this.getPercentage(),

            status: this.getStatus(),

            history: [...this.history]

        };

    }

}

export const Congestion = new CongestionAnalytics();

export default Congestion;