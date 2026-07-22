/*
===============================================================
Astravon Live Arena
Heat Index Component

Purpose:
    Calculates, classifies and renders Heat Index
    information for the Analytics, Dashboard,
    Reports and Camera modules.

Author:
    House of Astravon
===============================================================
*/

const DEFAULTS = {
    temperature: 25,
    humidity: 50
};

export class HeatIndex {

    constructor(containerId = null) {

        this.container =
            containerId
                ? document.getElementById(containerId)
                : null;

        this.temperature = DEFAULTS.temperature;
        this.humidity = DEFAULTS.humidity;
        this.heatIndex = DEFAULTS.temperature;
        this.level = "Comfortable";

    }

    /*
    ===============================================================
    Public API
    ===============================================================
    */

    update(temperature, humidity) {

        this.temperature = Number(temperature);
        this.humidity = Number(humidity);

        this.heatIndex = this.calculate(
            this.temperature,
            this.humidity
        );

        this.level = this.classify(
            this.heatIndex
        );

        this.render();

        return this.getData();

    }

    setTemperature(value) {

        return this.update(
            value,
            this.humidity
        );

    }

    setHumidity(value) {

        return this.update(
            this.temperature,
            value
        );

    }

    getData() {

        return {

            temperature: this.temperature,

            humidity: this.humidity,

            heatIndex: Number(
                this.heatIndex.toFixed(1)
            ),

            level: this.level

        };

    }

    /*
    ===============================================================
    Heat Index Calculation
    (Approximation)
    ===============================================================
    */

    calculate(tempC, humidity) {

        /*
            Simple approximation suitable
            for dashboard visualization.
        */

        if (tempC < 27) {

            return tempC;

        }

        const hi =

            tempC +

            (
                0.33 *
                humidity /
                100 *
                6.105 *
                Math.exp(
                    17.27 *
                    tempC /
                    (237.7 + tempC)
                )
            )

            -

            4;

        return hi;

    }

    /*
    ===============================================================
    Risk Classification
    ===============================================================
    */

    classify(index) {

        if (index < 27)
            return "Comfortable";

        if (index < 32)
            return "Caution";

        if (index < 41)
            return "Extreme Caution";

        if (index < 54)
            return "Danger";

        return "Extreme Danger";

    }

    /*
    ===============================================================
    Badge Color
    ===============================================================
    */

    badgeClass(level) {

        switch (level) {

            case "Comfortable":
                return "status-success";

            case "Caution":
                return "status-info";

            case "Extreme Caution":
                return "status-warning";

            case "Danger":
                return "status-danger";

            default:
                return "status-danger";

        }

    }

    /*
    ===============================================================
    Rendering
    ===============================================================
    */

    render() {

        if (!this.container)
            return;

        this.container.innerHTML = `

            <div class="heat-index-widget">

                <div class="metric">

                    <span class="metric-label">
                        Temperature
                    </span>

                    <span class="metric-value">
                        ${this.temperature.toFixed(1)} °C
                    </span>

                </div>

                <div class="metric">

                    <span class="metric-label">
                        Humidity
                    </span>

                    <span class="metric-value">
                        ${this.humidity.toFixed(0)} %
                    </span>

                </div>

                <div class="metric">

                    <span class="metric-label">
                        Heat Index
                    </span>

                    <span class="metric-value">
                        ${this.heatIndex.toFixed(1)} °C
                    </span>

                </div>

                <div class="badge ${this.badgeClass(this.level)}">

                    ${this.level}

                </div>

            </div>

        `;

    }

}

/*
===============================================================
Singleton
===============================================================
*/

export const heatIndex = new HeatIndex();

/*
===============================================================
Helper Functions
===============================================================
*/

export function calculateHeatIndex(
    temperature,
    humidity
) {

    return heatIndex.calculate(
        temperature,
        humidity
    );

}

export function classifyHeatIndex(index) {

    return heatIndex.classify(index);

}