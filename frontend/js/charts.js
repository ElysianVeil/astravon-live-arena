/*
============================================================
Astravon Live Arena
Charts Manager

Purpose:
    Creates and updates all dashboard charts.

Dependencies:
    Chart.js

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

export default class ChartsManager {

    constructor() {

        /*
        =====================================================
        Chart Instances
        =====================================================
        */

        this.peopleChart = null;

        this.temperatureChart = null;

        this.riskChart = null;

        this.objectChart = null;

        /*
        =====================================================
        Maximum History
        =====================================================
        */

        this.maxHistory = 30;

    }

    /*
    ==========================================================
    Initialize
    ==========================================================
    */

    initialize() {

        this.createPeopleChart();

        this.createTemperatureChart();

        this.createRiskChart();

        this.createObjectChart();

        console.log(
            "[Charts] Initialized."
        );

    }

    /*
    ==========================================================
    People Count
    ==========================================================
    */

    createPeopleChart() {

        const canvas = document.getElementById(
            "peopleChart"
        );

        if (!canvas) {

            return;

        }

        this.peopleChart = new Chart(

            canvas,

            {

                type: "line",

                data: {

                    labels: [],

                    datasets: [

                        {

                            label: "People",

                            data: [],

                            borderWidth: 3,

                            tension: 0.35,

                            fill: true

                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    animation: false

                }

            }

        );

    }

    /*
    ==========================================================
    Temperature
    ==========================================================
    */

    createTemperatureChart() {

        const canvas = document.getElementById(
            "temperatureChart"
        );

        if (!canvas) {

            return;

        }

        this.temperatureChart = new Chart(

            canvas,

            {

                type: "line",

                data: {

                    labels: [],

                    datasets: [

                        {

                            label: "Temperature (°C)",

                            data: [],

                            borderWidth: 3,

                            tension: 0.35,

                            fill: true

                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    animation: false

                }

            }

        );

    }

    /*
    ==========================================================
    Risk Score
    ==========================================================
    */

    createRiskChart() {

        const canvas = document.getElementById(
            "riskChart"
        );

        if (!canvas) {

            return;

        }

        this.riskChart = new Chart(

            canvas,

            {

                type: "bar",

                data: {

                    labels: [],

                    datasets: [

                        {

                            label: "Risk Score",

                            data: []

                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    animation: false,

                    scales: {

                        y: {

                            min: 0,

                            max: 100

                        }

                    }

                }

            }

        );

    }

    /*
    ==========================================================
    Detected Objects
    ==========================================================
    */

    createObjectChart() {

        const canvas = document.getElementById(
            "objectChart"
        );

        if (!canvas) {

            return;

        }

        this.objectChart = new Chart(

            canvas,

            {

                type: "doughnut",

                data: {

                    labels: [

                        "People",

                        "Vehicles",

                        "Other"

                    ],

                    datasets: [

                        {

                            data: [

                                0,

                                0,

                                0

                            ]

                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false

                }

            }

        );

    }

    /*
    ==========================================================
    Update Live Statistics
    ==========================================================
    */

    update(statistics) {

        const time = new Date()

            .toLocaleTimeString();

        this.append(

            this.peopleChart,

            time,

            statistics.people_count
        );

        this.append(

            this.temperatureChart,

            time,

            statistics.temperature
        );

        this.append(

            this.riskChart,

            time,

            statistics.risk_score
        );

    }

    /*
    ==========================================================
    Update Object Distribution
    ==========================================================
    */

    updateObjects(

        people,

        vehicles,

        others

    ) {

        if (!this.objectChart) {

            return;

        }

        this.objectChart.data.datasets[0].data = [

            people,

            vehicles,

            others

        ];

        this.objectChart.update();

    }

    /*
    ==========================================================
    Append Data
    ==========================================================
    */

    append(

        chart,

        label,

        value

    ) {

        if (!chart) {

            return;

        }

        chart.data.labels.push(

            label

        );

        chart.data.datasets[0].data.push(

            value

        );

        if (

            chart.data.labels.length >

            this.maxHistory

        ) {

            chart.data.labels.shift();

            chart.data.datasets[0].data.shift();

        }

        chart.update();

    }

    /*
    ==========================================================
    Clear All Charts
    ==========================================================
    */

    clear() {

        [

            this.peopleChart,

            this.temperatureChart,

            this.riskChart

        ]

        .forEach(chart => {

            if (!chart) {

                return;

            }

            chart.data.labels = [];

            chart.data.datasets[0].data = [];

            chart.update();

        });

    }

    /*
    ==========================================================
    Destroy
    ==========================================================
    */

    destroy() {

        [

            this.peopleChart,

            this.temperatureChart,

            this.riskChart,

            this.objectChart

        ]

        .forEach(chart => {

            if (chart) {

                chart.destroy();

            }

        });

    }

}