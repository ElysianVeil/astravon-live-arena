/*
============================================================
Astravon Live Arena
Chart Manager

Purpose:
    Centralized Chart.js management for the
    entire application.

Author:
    House of Astravon
============================================================
*/

class ChartManager {

    constructor() {

        this.charts = new Map();

        this.defaultOptions = this.createDefaultOptions();

        this.history = {

            labels: [],

            people: [],

            density: [],

            risk: [],

            movement: []

        };

        this.maxHistory = 30;

    }

    initialize() {

        this.createIfExists(
            "occupancyChart",
            () => this.createOccupancyChart("occupancyChart")
        );

        this.createIfExists(
            "peopleChart",
            () => this.createPeopleChart("peopleChart")
        );

        this.createIfExists(
            "densityChart",
            () => this.createDensityChart("densityChart")
        );

        this.createIfExists(
            "riskChart",
            () => this.createRiskChart("riskChart")
        );

        this.createIfExists(
            "movementChart",
            () => this.createMovementChart("movementChart")
        );

    }

    /*
    ============================================================
    Default Theme
    ============================================================
    */

    createDefaultOptions() {

        return {

            responsive: true,

            maintainAspectRatio: false,

            animation: {

                duration: 600

            },

            interaction: {

                mode: "nearest",

                intersect: false

            },

            plugins: {

                legend: {

                    labels: {

                        color: "#D1D5DB",

                        font: {

                            family: "Inter",

                            size: 13

                        }

                    }

                },

                tooltip: {

                    backgroundColor: "#0B1A3A",

                    borderColor: "#D4AF37",

                    borderWidth: 1,

                    titleColor: "#FFFFFF",

                    bodyColor: "#D1D5DB",

                    displayColors: true

                }

            },

            scales: {

                x: {

                    ticks: {

                        color: "#9CA3AF"

                    },

                    grid: {

                        color: "rgba(255,255,255,.06)"

                    }

                },

                y: {

                    ticks: {

                        color: "#9CA3AF"

                    },

                    grid: {

                        color: "rgba(255,255,255,.06)"

                    }

                }

            }

        };

    }

    /*
    ============================================================
    Create
    ============================================================
    */

    create(id, config) {

        this.destroy(id);

        const canvas = document.getElementById(id);

        if (!canvas) {

            console.warn(`Chart '${id}' not found.`);

            return null;

        }

        const chart = new Chart(canvas, {

            ...config,

            options: {

                ...this.defaultOptions,

                ...(config.options || {})

            }

        });

        this.charts.set(id, chart);

        return chart;

    }

    renderChart() {

        charts.update(
            "occupancyChart",
            this.labels,
            [
                charts.lineDataset(
                    "Occupancy %",
                    this.history,
                    "#D4AF37"
                )
            ]
        );

    }

    /*
    ============================================================
    History Helper
    ============================================================
    */

    pushHistory(label, collection, value) {

        this.history.labels.push(label);

        this.history[collection].push(value);

        if (this.history.labels.length > this.maxHistory) {

            this.history.labels.shift();

        }

        if (this.history[collection].length > this.maxHistory) {

            this.history[collection].shift();

        }

    }

    /*
    ============================================================
    People Chart
    ============================================================
    */

    updatePeopleChart(value) {

        const chart = this.charts.get("peopleChart");

        if (!chart) return;

        chart.data.labels.push("");

        chart.data.datasets[0].data.push(value);

        if (chart.data.labels.length > this.maxHistory) {

            chart.data.labels.shift();

            chart.data.datasets[0].data.shift();

        }

        chart.update();

    }

    /*
    ============================================================
    Density Chart
    ============================================================
    */

    updateDensityChart(value) {

        const chart = this.charts.get("densityChart");

        if (!chart) return;

        chart.data.labels.push("");

        chart.data.datasets[0].data.push(value);

        if (chart.data.labels.length > this.maxHistory) {

            chart.data.labels.shift();

            chart.data.datasets[0].data.shift();

        }

        chart.update();

    }

    /*
    ============================================================
    Risk Chart
    ============================================================
    */

    updateRiskChart(value) {

        const chart = this.charts.get("riskChart");

        if (!chart) return;

        chart.data.labels.push("");

        chart.data.datasets[0].data.push(value);

        if (chart.data.labels.length > this.maxHistory) {

            chart.data.labels.shift();

            chart.data.datasets[0].data.shift();

        }

        chart.update();

    }

    /*
    ============================================================
    Movement Chart
    ============================================================
    */

    updateMovementChart(value) {

        const chart = this.charts.get("movementChart");

        if (!chart) return;

        chart.data.labels.push("");

        chart.data.datasets[0].data.push(value);

        if (chart.data.labels.length > this.maxHistory) {

            chart.data.labels.shift();

            chart.data.datasets[0].data.shift();

        }

        chart.update();

    }

    /*
    ============================================================
    Update Dataset
    ============================================================
    */

    update(id, labels, datasets) {

        const chart = this.charts.get(id);

        if (!chart) return;

        chart.data.labels = labels;

        chart.data.datasets = datasets;

        chart.update();

    }

    /*
    ============================================================
    Update Values Only
    ============================================================
    */

    updateDataset(id, index, values) {

        const chart = this.charts.get(id);

        if (!chart) return;

        if (!chart.data.datasets[index]) return;

        chart.data.datasets[index].data = values;

        chart.update();

    }

    /*
    ============================================================
    Resize
    ============================================================
    */

    resize(id) {

        const chart = this.charts.get(id);

        if (chart) {

            chart.resize();

        }

    }

    resizeAll() {

        this.charts.forEach(chart => chart.resize());

    }

    /*
    ============================================================
    Destroy
    ============================================================
    */

    destroy(id) {

        const chart = this.charts.get(id);

        if (!chart) return;

        chart.destroy();

        this.charts.delete(id);

    }

    destroyAll() {

        this.charts.forEach(chart => chart.destroy());

        this.charts.clear();

    }

    /*
    ============================================================
    Helpers
    ============================================================
    */

    lineDataset(label, data, color) {

        return {

            label,

            data,

            borderColor: color,

            backgroundColor: color + "33",

            tension: .35,

            fill: true

        };

    }

    barDataset(label, data, color) {

        return {

            label,

            data,

            backgroundColor: color,

            borderRadius: 8

        };

    }

    pieDataset(data, colors) {

        return {

            data,

            backgroundColor: colors,

            borderWidth: 0

        };

    }

    doughnutDataset(data, colors) {

        return {

            data,

            backgroundColor: colors,

            borderWidth: 0

        };

    }

    radarDataset(label, data, color) {

        return {

            label,

            data,

            borderColor: color,

            backgroundColor: color + "33",

            pointBackgroundColor: color

        };

    }

    /*
    ============================================================
    Sample Charts
    ============================================================
    */

    createPeopleChart(id) {

        return this.create(id, {

            type: "line",

            data: {

                labels: [],

                datasets: [

                    this.lineDataset(

                        "People",

                        [],

                        "#D4AF37"

                    )

                ]

            }

        });

    }

    createDensityChart(id) {

        return this.create(id, {

            type: "bar",

            data: {

                labels: [],

                datasets: [

                    this.barDataset(

                        "Density",

                        [],

                        "#3B82F6"

                    )

                ]

            }

        });

    }

    createRiskChart(id) {

        return this.create(id, {

            type: "line",

            data: {

                labels: [],

                datasets: [

                    this.lineDataset(

                        "Risk",

                        [],

                        "#EF4444"

                    )

                ]

            }

        });

    }

    createMovementChart(id) {

        return this.create(id, {

            type: "line",

            data: {

                labels: [],

                datasets: [

                    this.lineDataset(

                        "Movement Speed",

                        [],

                        "#22C55E"

                    )

                ]

            }

        });

    }

    /*
    ============================================================
    Occupancy Chart
    ============================================================
    */

    createOccupancyChart(id) {

        return this.create(id, {

            type: "line",

            data: {

                labels: [],

                datasets: [

                    this.lineDataset(

                        "Occupancy %",

                        [],

                        "#D4AF37"

                    )

                ]

            },

            options: {

                scales: {

                    y: {

                        min: 0,

                        max: 100

                    }

                }

            }

        });

    }

    /*
    ============================================================
    Occupancy Chart Update
    ============================================================
    */

    updateOccupancyChart(value) {

        const chart = this.charts.get("occupancyChart");

        if (!chart) return;

        chart.data.labels.push("");

        chart.data.datasets[0].data.push(value);

        if (chart.data.labels.length > this.maxHistory) {

            chart.data.labels.shift();

            chart.data.datasets[0].data.shift();

        }

        chart.update();

    }

    createIfExists(id, callback) {

        if (!document.getElementById(id)) {

            return;

        }

        callback();

    }

    createPieChart(id) {

        return this.create(id, {

            type: "pie",

            data: {

                labels: [],

                datasets: [

                    this.pieDataset(

                        [],

                        [

                            "#D4AF37",

                            "#3B82F6",

                            "#22C55E",

                            "#EF4444",

                            "#F59E0B"

                        ]

                    )

                ]

            }

        });

    }

}

const charts = new ChartManager();

export default charts;