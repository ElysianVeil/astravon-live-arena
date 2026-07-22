/*
============================================================
Astravon Live Arena
Weather Analytics Component

Purpose:
    Monitors environmental conditions around the venue,
    maintains weather history, updates dashboard statistics,
    and renders weather charts.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

import { StatisticsManager } from "./statistics.js";
import charts from "./charts.js";

class WeatherAnalytics {

    constructor() {

        this.temperatureChart = null;
        this.humidityChart = null;
        this.heatIndexChart = null;

        this.temperatureChartId = "temperatureChart";
        this.humidityChartId = "humidityChart";
        this.heatIndexChartId = "heatIndexChart";

        this.temperature = 0;
        this.humidity = 0;
        this.heatIndex = 0;
        this.windSpeed = 0;

        this.history = [];

    }

    initialize() {

        /*
        ===========================================================
        Dashboard
        ===========================================================
        */

        this.container =
            document.getElementById("weatherContainer");

        /*
        ===========================================================
        Analytics
        ===========================================================
        */

        this.temperatureCanvas =
            document.getElementById(this.temperatureChartId);

        this.humidityCanvas =
            document.getElementById(this.humidityChartId);

        this.heatIndexCanvas =
            document.getElementById(this.heatIndexChartId);

        /*
        ===========================================================
        Create charts ONLY if they exist
        ===========================================================
        */

        if (this.temperatureCanvas) {

            charts.create(this.temperatureChartId, {

                type: "line",

                data: {

                    labels: [],

                    datasets: [

                        charts.lineDataset(
                            "Temperature",
                            [],
                            "#EF4444"
                        )

                    ]

                }

            });

        }

        if (this.humidityCanvas) {

            charts.create(this.humidityChartId, {

                type: "line",

                data: {

                    labels: [],

                    datasets: [

                        charts.lineDataset(
                            "Humidity",
                            [],
                            "#3B82F6"
                        )

                    ]

                }

            });

        }

        if (this.heatIndexCanvas) {

            charts.create(this.heatIndexChartId, {

                type: "line",

                data: {

                    labels: [],

                    datasets: [

                        charts.lineDataset(
                            "Heat Index",
                            [],
                            "#F59E0B"
                        )

                    ]

                }

            });

        }

    }

    /*==========================================================
        Update Weather
    ==========================================================*/

    update(data = {}) {

        this.temperature = Number(data.temperature ?? 0);

        this.humidity = Number(data.humidity ?? 0);

        this.windSpeed = Number(data.windSpeed ?? 0);

        this.heatIndex = this.calculateHeatIndex(
            this.temperature,
            this.humidity
        );

        this.history.push({

            time: new Date().toLocaleTimeString(),

            temperature: this.temperature,

            humidity: this.humidity,

            heatIndex: this.heatIndex

        });

        if (this.history.length > 30) {

            this.history.shift();

        }

        // this.renderStatistics();

        this.renderDashboard();

        this.renderCharts();

    }

    /*==========================================================
        Heat Index
    ==========================================================*/

    calculateHeatIndex(temp, humidity) {

        return Number(

            (
                temp +
                (humidity * 0.05)

            ).toFixed(1)

        );

    }

    /*==========================================================
        Weather Status
    ==========================================================*/

    getWeatherStatus() {

        if (this.heatIndex >= 45) {

            return "Extreme";

        }

        if (this.heatIndex >= 35) {

            return "High";

        }

        if (this.heatIndex >= 28) {

            return "Warm";

        }

        return "Normal";

    }

    /*==========================================================
        Status Colour
    ==========================================================*/

    getStatusColor() {

        switch (this.getWeatherStatus()) {

            case "Extreme":
                return "#EF4444";

            case "High":
                return "#F59E0B";

            case "Warm":
                return "#D4AF37";

            default:
                return "#22C55E";

        }

    }

    /*==========================================================
        Dashboard Statistics
    ==========================================================*/

    // renderStatistics() {

    //     Statistics.set(

    //         "Temperature",

    //         `${this.temperature.toFixed(1)} °C`

    //     );

    //     Statistics.set(

    //         "Humidity",

    //         `${this.humidity.toFixed(1)} %`

    //     );

    //     Statistics.set(

    //         "Heat Index",

    //         `${this.heatIndex.toFixed(1)} °C`

    //     );

    //     Statistics.set(

    //         "Weather Status",

    //         this.getWeatherStatus()

    //     );

    // }

    renderDashboard() {

        if (!this.container) {

            return;

        }

        this.container.innerHTML = `

            <div class="weather-grid">

                <article class="weather-card">

                    <h3>🌡 Temperature</h3>

                    <div class="weather-value">

                        ${this.temperature.toFixed(1)}°C

                    </div>

                </article>

                <article class="weather-card">

                    <h3>💧 Humidity</h3>

                    <div class="weather-value">

                        ${this.humidity.toFixed(1)}%

                    </div>

                </article>

                <article class="weather-card">

                    <h3>🔥 Heat Index</h3>

                    <div class="weather-value">

                        ${this.heatIndex.toFixed(1)}°C

                    </div>

                </article>

                <article class="weather-card">

                    <h3>Status</h3>

                    <div
                        class="weather-value"
                        style="color:${this.getStatusColor()}"
                    >

                        ${this.getWeatherStatus()}

                    </div>

                </article>

            </div>

        `;

    }

    /*==========================================================
        Charts
    ==========================================================*/

    renderCharts() {

        if (
            !this.temperatureCanvas &&
            !this.humidityCanvas &&
            !this.heatIndexCanvas
        ) {

            return;

        }

        const labels = this.history.map(item => item.time);

        if (this.temperatureCanvas) {

            charts.update(
                this.temperatureChartId,
                labels,
                [
                    charts.lineDataset(
                        "Temperature",
                        this.history.map(item => item.temperature),
                        "#EF4444"
                    )
                ]
            );

        }

        if (this.humidityCanvas) {
            charts.update(

                this.humidityChartId,

                labels,

                [

                    charts.lineDataset(

                        "Humidity",

                        this.history.map(item => item.humidity),

                        "#3B82F6"

                    )

                ]

            );
        }
        
        if (this.heatIndexCanvas) {
            charts.update(

                this.heatIndexChartId,

                labels,

                [

                    charts.lineDataset(

                        "Heat Index",

                        this.history.map(item => item.heatIndex),

                        "#F59E0B"

                    )

                ]

            );
        }
        

    }
    /*==========================================================
        Reset
    ==========================================================*/

    reset() {

        this.temperature = 0;

        this.humidity = 0;

        this.heatIndex = 0;

        this.windSpeed = 0;

        this.history = [];

        this.renderCharts();

    }

    /*==========================================================
        Export
    ==========================================================*/

    exportData() {

        return {

            temperature: this.temperature,

            humidity: this.humidity,

            heatIndex: this.heatIndex,

            windSpeed: this.windSpeed,

            status: this.getWeatherStatus(),

            history: [...this.history]

        };

    }

}

export const Weather = new WeatherAnalytics();

export default Weather;