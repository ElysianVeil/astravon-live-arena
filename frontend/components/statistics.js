/*
============================================================
Astravon Live Arena
Statistics Component

Purpose:
    Displays live crowd statistics received from
    the AI Engine.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

export default class Statistics {

    constructor() {

        this.container = null;

        this.statistics = {

            people_count: 0,
            occupancy: 0,
            density: "Low",

            temperature: 0,
            humidity: 0,
            heat_index: 0,

            risk_score: 0,
            risk_level: "Low",

            detected_objects: 0,

            confidence: 0,

            processing_time: 0,

            fps: 0

        };

    }

    /*
    ==========================================================
    Initialize
    ==========================================================
    */

    initialize() {

        this.container = document.getElementById(
            "statisticsPanel"
        );

        if (!this.container) {

            console.warn(
                "[Statistics] Container not found."
            );

            return;

        }

        this.render();

        console.log(
            "[Statistics] Initialized."
        );

    }

    /*
    ==========================================================
    Update Statistics
    ==========================================================
    */

    update(data) {

        this.statistics = {

            ...this.statistics,

            ...data

        };

        this.render();

    }

    /*
    ==========================================================
    Render
    ==========================================================
    */

    render() {

        if (!this.container) {

            return;

        }

        const s = this.statistics;

        this.container.innerHTML = `

            <div class="statistics-grid">

                ${this.card(
                    "👥",
                    "People",
                    s.people_count
                )}

                ${this.card(
                    "🏟️",
                    "Occupancy",
                    `${s.occupancy}%`
                )}

                ${this.card(
                    "📍",
                    "Density",
                    s.density
                )}

                ${this.card(
                    "🌡️",
                    "Temperature",
                    `${s.temperature.toFixed(1)} °C`
                )}

                ${this.card(
                    "💧",
                    "Humidity",
                    `${s.humidity.toFixed(1)} %`
                )}

                ${this.card(
                    "🔥",
                    "Heat Index",
                    `${s.heat_index.toFixed(1)} °C`
                )}

                ${this.card(
                    "⚠️",
                    "Risk Score",
                    s.risk_score
                )}

                ${this.card(
                    "🚨",
                    "Risk Level",
                    s.risk_level
                )}

                ${this.card(
                    "🎯",
                    "Objects",
                    s.detected_objects
                )}

                ${this.card(
                    "✔️",
                    "Confidence",
                    `${(s.confidence * 100).toFixed(1)}%`
                )}

                ${this.card(
                    "⚡",
                    "Processing",
                    `${s.processing_time.toFixed(1)} ms`
                )}

                ${this.card(
                    "🎥",
                    "FPS",
                    s.fps.toFixed(1)
                )}

            </div>

        `;

    }

    /*
    ==========================================================
    Card
    ==========================================================
    */

    card(

        icon,

        title,

        value

    ) {

        return `

            <div class="stat-card">

                <div class="stat-header">

                    <span class="stat-icon">

                        ${icon}

                    </span>

                    <span class="stat-title">

                        ${title}

                    </span>

                </div>

                <div class="stat-value">

                    ${value}

                </div>

            </div>

        `;

    }

    /*
    ==========================================================
    Reset
    ==========================================================
    */

    reset() {

        this.statistics = {

            people_count: 0,
            occupancy: 0,
            density: "Low",

            temperature: 0,
            humidity: 0,
            heat_index: 0,

            risk_score: 0,
            risk_level: "Low",

            detected_objects: 0,

            confidence: 0,

            processing_time: 0,

            fps: 0

        };

        this.render();

    }

    /*
    ==========================================================
    Get Statistics
    ==========================================================
    */

    getStatistics() {

        return this.statistics;

    }

}