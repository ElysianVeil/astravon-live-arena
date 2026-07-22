/*
============================================================
Astravon Live Arena
Statistics Manager

Purpose:
    Handles all dashboard and analytics statistics.

Responsibilities
    • Store live statistics
    • Update statistics
    • Render dashboard statistics
    • Render overview cards
    • Publish changes
    • Provide snapshots

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

import EventBus from "../../js/event_bus.js";
import State from "../../js/state.js";
import charts from "./charts.js";
import density from "./density.js";
import Occupancy from "./occupancy.js";
import Congestion from "./congestion.js";
import Movement from "./movement.js";
import Weather from "./weather.js";
import riskGauge from "../risk/risk_gauge.js";

class StatisticsManager {

    constructor() {

        this.statistics = {};

        this.listeners = [];

        this.container = null;

        this.bound = false;

    }

    /*==========================================================
        Initialization
    ==========================================================*/

    initialize(containerId = "statisticsContainer") {

        this.container = document.getElementById(containerId);

        console.log(this.container);

        // Render the latest cached statistics
        const statistics = State.get("statistics");

        if (statistics) {
            this.update(statistics);
        }
        else {
            this.render();
        }

        // Listen for live updates
        if (!this.bound) {

            this.bound = true;

            EventBus.on(
                "statistics:updated",
                statistics => {

                    this.update(statistics);

                }
            );

        }
    }

    /*==========================================================
        Generic Update
    ==========================================================*/

    update(statistics) {

        if (!statistics) return;

        this.statistics = statistics;

        this.render();

        this.renderAnalytics();

        // Weather Panel
        this.renderWeather();

        // Occupancy Panel
        this.renderOccupancy();

        // Density Panel
        this.renderDensity();

        // Congestion Panel
        this.renderCongestion();

        // Movement Panel
        this.renderMovement();

        // Risk Gauge
        this.renderRisk();

        this.notify();

    }

    /*==========================================================
        Individual Updates
    ==========================================================*/

    updatePeople(value) {

        this.statistics.people = value;

        this.refresh();

    }

    updateDensity(value) {

        this.statistics.density = value;

        this.refresh();

    }

    updateOccupancy(value) {

        this.statistics.occupancy = value;

        this.refresh();

    }

    updateMovement(value) {

        this.statistics.movement = value;

        this.refresh();

    }

    updateCongestion(value) {

        this.statistics.congestion = value;

        this.refresh();

    }

    updateRisk(value) {

        this.statistics.risk = value;

        this.refresh();

    }

    updateWeather({

        temperature,

        humidity,

        heat_index

    }) {

        this.statistics.weather = {

            temperature,

            humidity,

            heat_index

        };

        this.refresh();

    }

    updateAI({

        fps,

        processingTime,

        detections,

        tracks,

        identities

    }) {

        this.statistics.ai = {

            fps,

            processingTime,

            detections,

            tracks,

            identities

        };

        this.refresh();

    }

    renderAnalytics() {

        if (!this.statistics) {
            return;
        }

        this.renderPeopleChart();

        this.renderDensityChart();

        this.renderRiskChart();

        this.renderMovementChart();

    }

    renderPeopleChart() {

        const value =
            this.statistics?.detection?.people_count ?? 0;

        charts.updatePeopleChart(value);

    }

    renderDensityChart() {

        const density =
            this.statistics?.density?.average_density ?? 0;

        charts.updateDensityChart(density);

    }

    renderRiskChart() {

        const risk =
            this.statistics?.risk?.risk_score ?? 0;

        charts.updateRiskChart(risk);

    }

    renderMovementChart() {

        const speed =
            this.statistics?.risk?.movement?.average_speed ?? 0;

        charts.updateMovementChart(speed);

    }

    renderWeather() {

        Weather.update(
            this.statistics.weather
        );

    }

    renderOccupancy() {

        Occupancy?.update?.(
            this.statistics.occupancy
        );

    }

    renderDensity() {

        density?.update?.(
            this.statistics.density
        );

    }

    renderCongestion() {

        Congestion?.update?.(
            this.statistics.congestion
        );

    }

    renderMovement() {

        Movement?.update?.(
            this.statistics.movement
        );

    }

    renderRisk() {

        riskGauge?.update?.(
            this.statistics.risk
        );

    }

    refresh() {

        this.render();

        this.notify();

    }

    /*==========================================================
        Rendering
    ==========================================================*/

    render() {
        console.log(
            "[StatisticsManager] Rendering into:",
            this.container
        );

        if (!this.container) return;

        this.container.innerHTML = `

        <div class="statistics-grid">

            ${this.card(
                "People:",
                this.getPeopleCount()
            )}

            ${this.card(
                "Density:",
                `${this.getDensity()}%`
            )}

            ${this.card(
                "Occupancy:",
                `${this.getOccupancy()}%`
            )}

            ${this.card(
                "Movement Speed:",
                this.statistics?.risk?.movement?.average_speed ?? 0
            )}

            ${this.card(
                "Congestion Level:",
                `${this.statistics.congestion?.current_level ?? "-"}`
            )}

            ${this.card(
                "Risk Level:",
                `${this.statistics.risk?.risk_level ?? "Unknown"}`
            )}

            ${this.card(
                "Temperature:",
                `${this.getWeather()?.temperature ?? 0.0}°C`
            )}

            ${this.card(
                "Humidity:",
                `${this.getWeather()?.humidity ?? 0.0}%`
            )}

            ${this.card(
                "Heat Index:",
                `${this.getWeather()?.heat_index ?? 0}°C`
            )}

            ${this.card(
                "FPS:",
                this.statistics
                    ?.performance
                    ?.current_fps ?? 0
            )}

            ${this.card(
                "Processing Time:",
                `${this.statistics
                    ?.performance
                    ?.processing_time ?? 0} ms`
            )}

            ${this.card(
                "Detections:",
                this.statistics
                    ?.detection
                    ?.detector
                    ?.total_detections ?? 0
            )}

        </div>

        `;

    }

    /*==========================================================
        Card
    ==========================================================*/

    card(label, value) {

        return `

        <article class="stat-box">

            <h3>

                ${label}

            </h3>

            <div class="stat-number">

                ${value}

            </div>

        </article>

        `;

    }

    /*==========================================================
        Getters
    ==========================================================*/

    getSnapshot() {

        return structuredClone(

            this.statistics

        );

    }

    getPeopleCount() {

        return this.statistics
        ?.detection
        ?.people_count ?? 0;

    }

    getDensity() {

        return this.statistics
            ?.density
            ?.rolling_density ?? 0;

    }

    getOccupancy() {

        return this.statistics
            ?.occupancy
            ?.occupancy_percentage ?? 0;

    }

    getRiskLevel() {

        return this.statistics
            ?.risk
            ?.risk_level ?? "Unknown";

    }

    getWeather() {

        return this.statistics.weather ?? {};

    }

    getAI() {

        return structuredClone(

            this.statistics.ai

        );

    }

    /*==========================================================
        Camera Statistics Helpers
    ==========================================================*/


    getCameraStatistics(){

        return {

            people:
                this.getPeopleCount(),


            occupancy:
                this.getOccupancy(),


            occupancyStatus:
                this.statistics
                    ?.occupancy
                    ?.status ?? "Unknown",


            density:
                this.statistics
                    ?.density
                    ?.rolling_density ?? 0,


            congestion:
                this.statistics
                    ?.congestion
                    ?.current_level ?? "Unknown",


            risk:
                this.statistics
                    ?.risk
                    ?.risk_level ?? "Unknown",


            fps:
                this.statistics
                    ?.performance
                    ?.current_fps ?? 0,


            processingTime:
                this.statistics
                    ?.performance
                    ?.processing_time ?? 0,


            cameraCount:
                this.statistics
                    ?.camera
                    ?.camera_count ?? 0,


            connectedCameras:
                this.statistics
                    ?.camera
                    ?.connected ?? 0

        };

    }

    /*==========================================================
        Reset
    ==========================================================*/

    reset() {

        this.statistics.people = 0;

        this.statistics.density = 0;

        this.statistics.occupancy = 0;

        this.statistics.movement = 0;

        this.statistics.congestion = 0;

        this.statistics.risk = 0;

        this.statistics.weather = {

            temperature: 0,

            humidity: 0,

            heat_index: 0

        };

        this.statistics.ai = {

            fps: 0,

            processingTime: 0,

            detections: 0,

            tracks: 0,

            identities: 0

        };

        this.refresh();

    }

    /*==========================================================
        Events
    ==========================================================*/

    subscribe(callback) {

        this.listeners.push(callback);

    }

    unsubscribe(callback) {

        this.listeners =

            this.listeners.filter(

                listener =>

                    listener !== callback

            );

    }

    notify() {

        const snapshot =

            this.getSnapshot();

        this.listeners.forEach(

            listener => listener(snapshot)

        );

    }

}

/*============================================================
Singleton
============================================================*/

const statisticsManager =
    new StatisticsManager();

export default statisticsManager;

export {

    StatisticsManager

};