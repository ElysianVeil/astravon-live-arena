/*
============================================================
Astravon Live Arena
Trend Analytics Component

Purpose:
    Tracks historical trends for live analytics,
    provides rolling history for charts, calculates
    averages and trend direction.

Author:
    House of Astravon
Version:
    1.0.0
============================================================
*/

import charts from "./charts.js";

class TrendAnalytics {

    constructor() {

        this.maximumSamples = 60;

        this.datasets = new Map();

        this.charts = new Map();

    }

    /*==========================================================
        Dataset Management
    ==========================================================*/

    create(name) {

        if (!this.datasets.has(name)) {

            this.datasets.set(name, []);

        }

        return this.datasets.get(name);

    }

    exists(name) {

        return this.datasets.has(name);

    }

    clear(name) {

        if (this.datasets.has(name)) {

            this.datasets.set(name, []);

        }

    }

    clearAll() {

        this.datasets.clear();

        this.charts.clear();

    }

    /*==========================================================
        Update Trend
    ==========================================================*/

    update(name, value) {

        const dataset = this.create(name);

        dataset.push({

            time: new Date().toLocaleTimeString(),

            value: Number(value)

        });

        if (dataset.length > this.maximumSamples) {

            dataset.shift();

        }

        return dataset;

    }

    /*==========================================================
        Chart Rendering
    ==========================================================*/

    render(name, chartId, label = name) {

        if (!this.datasets.has(name)) {

            return;

        }

        const dataset = this.datasets.get(name);

        const labels = dataset.map(item => item.time);

        const values = dataset.map(item => item.value);

        const chart = this.charts.get(name) || null;

        charts.update(
            this.chartId,
            labels,
            [
                charts.lineDataset(
                    label,
                    values,
                    this.getColor()
                )
            ]
        );

        this.charts.set(name, updatedChart);

    }

    /*==========================================================
        Trend Direction
    ==========================================================*/

    getDirection(name) {

        const dataset = this.datasets.get(name);

        if (!dataset || dataset.length < 2) {

            return "Stable";

        }

        const latest = dataset.at(-1).value;

        const previous = dataset.at(-2).value;

        if (latest > previous) {

            return "Increasing";

        }

        if (latest < previous) {

            return "Decreasing";

        }

        return "Stable";

    }

    /*==========================================================
        Average
    ==========================================================*/

    getAverage(name) {

        const dataset = this.datasets.get(name);

        if (!dataset || dataset.length === 0) {

            return 0;

        }

        const total = dataset.reduce(

            (sum, point) => sum + point.value,

            0

        );

        return Number(

            (total / dataset.length).toFixed(2)

        );

    }

    /*==========================================================
        Maximum
    ==========================================================*/

    getMaximum(name) {

        const dataset = this.datasets.get(name);

        if (!dataset || dataset.length === 0) {

            return 0;

        }

        return Math.max(

            ...dataset.map(item => item.value)

        );

    }

    /*==========================================================
        Minimum
    ==========================================================*/

    getMinimum(name) {

        const dataset = this.datasets.get(name);

        if (!dataset || dataset.length === 0) {

            return 0;

        }

        return Math.min(

            ...dataset.map(item => item.value)

        );

    }

    /*==========================================================
        Latest
    ==========================================================*/

    getLatest(name) {

        const dataset = this.datasets.get(name);

        if (!dataset || dataset.length === 0) {

            return null;

        }

        return dataset.at(-1);

    }

    /*==========================================================
        Export
    ==========================================================*/

    export(name) {

        return {

            name,

            direction: this.getDirection(name),

            average: this.getAverage(name),

            minimum: this.getMinimum(name),

            maximum: this.getMaximum(name),

            history: [...(this.datasets.get(name) || [])]

        };

    }

    exportAll() {

        const output = {};

        this.datasets.forEach((_, name) => {

            output[name] = this.export(name);

        });

        return output;

    }

}

export const Trends = new TrendAnalytics();

export default Trends;