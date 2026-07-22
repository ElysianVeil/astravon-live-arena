/*
============================================================
Astravon Live Arena
Report Filters Component

Purpose:
    Manages report filtering controls and emits the
    currently selected filter configuration.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

export default class ReportFilters {

    constructor(options = {}) {

        this.periodSelect =
            this.#getElement(options.period || "#reportPeriod");

        this.venueSelect =
            this.#getElement(options.venue || "#venueSelector");

        this.cameraSelect =
            this.#getElement(options.camera || "#cameraSelector");

        this.generateButton =
            this.#getElement(options.generate || "#generateReportBtn");

        this.filters = {

            period: "today",
            venue: "all",
            camera: "all"

        };

        this.callbacks = [];

        this.#bindEvents();

    }

    /*
    ==========================================================
        Private Helpers
    ==========================================================
    */

    #getElement(selector) {

        if (selector instanceof HTMLElement) {

            return selector;

        }

        return document.querySelector(selector);

    }

    /*
    ==========================================================
        Bind Events
    ==========================================================
    */

    #bindEvents() {

        this.periodSelect?.addEventListener(
            "change",
            () => this.#updateFilters()
        );

        this.venueSelect?.addEventListener(
            "change",
            () => this.#updateFilters()
        );

        this.cameraSelect?.addEventListener(
            "change",
            () => this.#updateFilters()
        );

        this.generateButton?.addEventListener(
            "click",
            () => this.#emit()
        );

    }

    /*
    ==========================================================
        Update Filter Object
    ==========================================================
    */

    #updateFilters() {

        this.filters.period =
            this.periodSelect?.value || "today";

        this.filters.venue =
            this.venueSelect?.value || "all";

        this.filters.camera =
            this.cameraSelect?.value || "all";

    }

    /*
    ==========================================================
        Emit Event
    ==========================================================
    */

    #emit() {

        this.#updateFilters();

        this.callbacks.forEach(callback => {

            callback(this.getFilters());

        });

    }

    /*
    ==========================================================
        Register Listener
    ==========================================================
    */

    onGenerate(callback) {

        if (typeof callback === "function") {

            this.callbacks.push(callback);

        }

        return this;

    }

    /*
    ==========================================================
        Get Current Filters
    ==========================================================
    */

    getFilters() {

        return {

            ...this.filters

        };

    }

    /*
    ==========================================================
        Set Filters
    ==========================================================
    */

    setFilters(filters = {}) {

        this.filters = {

            ...this.filters,

            ...filters

        };

        if (this.periodSelect) {

            this.periodSelect.value =
                this.filters.period;

        }

        if (this.venueSelect) {

            this.venueSelect.value =
                this.filters.venue;

        }

        if (this.cameraSelect) {

            this.cameraSelect.value =
                this.filters.camera;

        }

        return this;

    }

    /*
    ==========================================================
        Populate Venue List
    ==========================================================
    */

    setVenues(venues = []) {

        if (!this.venueSelect) return;

        this.venueSelect.innerHTML =
            '<option value="all">All Venues</option>';

        venues.forEach(venue => {

            const option =
                document.createElement("option");

            option.value = venue.id;

            option.textContent = venue.name;

            this.venueSelect.appendChild(option);

        });

    }

    /*
    ==========================================================
        Populate Camera List
    ==========================================================
    */

    setCameras(cameras = []) {

        if (!this.cameraSelect) return;

        this.cameraSelect.innerHTML =
            '<option value="all">All Cameras</option>';

        cameras.forEach(camera => {

            const option =
                document.createElement("option");

            option.value = camera.id;

            option.textContent = camera.name;

            this.cameraSelect.appendChild(option);

        });

    }

    /*
    ==========================================================
        Reset Filters
    ==========================================================
    */

    reset() {

        this.setFilters({

            period: "today",

            venue: "all",

            camera: "all"

        });

    }

}