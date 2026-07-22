/*
============================================================
Astravon Live Arena
Heatmap Component

Purpose:
    Manages crowd density heatmaps displayed on the
    venue map.

Responsibilities:
    • Store heat points
    • Render heat layer
    • Update heat data
    • Clear heatmap
    • Toggle visibility

Dependencies:
    Leaflet
    Leaflet.heat plugin

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

class HeatmapManager {

    constructor() {

        this.map = null;

        this.layer = null;

        this.points = [];

        this.visible = true;

        this.options = {

            radius: 30,

            blur: 25,

            maxZoom: 20,

            minOpacity: 0.35,

            max: 1.0,

            gradient: {

                0.2: "#22c55e",
                0.4: "#84cc16",
                0.6: "#facc15",
                0.8: "#f97316",
                1.0: "#dc2626"

            }

        };

    }

    /*
    ==========================================================
        Initialize
    ==========================================================
    */

    initialize(map, options = {}) {

        if (!map) {

            throw new Error(
                "Heatmap requires a Leaflet map instance."
            );

        }

        this.map = map;

        this.options = {

            ...this.options,

            ...options

        };

        this.layer = L.heatLayer(

            [],

            this.options

        );

        this.layer.addTo(this.map);

        return this;

    }

    /*
    ==========================================================
        Set Heat Points

        Format:

        [
            {
                lat,
                lng,
                intensity
            }
        ]
    ==========================================================
    */

    setPoints(points = []) {

        this.points = points.map(point => [

            point.lat,

            point.lng,

            point.intensity ?? 0.5

        ]);

        this.#refresh();

    }

    /*
    ==========================================================
        Add Point
    ==========================================================
    */

    addPoint(point) {

        this.points.push([

            point.lat,

            point.lng,

            point.intensity ?? 0.5

        ]);

        this.#refresh();

    }

    /*
    ==========================================================
        Clear
    ==========================================================
    */

    clear() {

        this.points = [];

        this.#refresh();

    }

    /*
    ==========================================================
        Refresh Layer
    ==========================================================
    */

    #refresh() {

        if (!this.layer) {

            return;

        }

        this.layer.setLatLngs(

            this.points

        );

    }

    /*
    ==========================================================
        Visibility
    ==========================================================
    */

    show() {

        if (

            this.map &&
            this.layer &&
            !this.map.hasLayer(this.layer)

        ) {

            this.layer.addTo(this.map);

        }

        this.visible = true;

    }

    hide() {

        if (

            this.map &&
            this.layer &&
            this.map.hasLayer(this.layer)

        ) {

            this.map.removeLayer(

                this.layer

            );

        }

        this.visible = false;

    }

    toggle() {

        this.visible

            ? this.hide()

            : this.show();

    }

    /*
    ==========================================================
        Options
    ==========================================================
    */

    updateOptions(options = {}) {

        this.options = {

            ...this.options,

            ...options

        };

        if (!this.map) {

            return;

        }

        if (this.layer) {

            this.map.removeLayer(

                this.layer

            );

        }

        this.layer = L.heatLayer(

            this.points,

            this.options

        );

        if (this.visible) {

            this.layer.addTo(this.map);

        }

    }

    /*
    ==========================================================
        Utilities
    ==========================================================
    */

    getPoints() {

        return [...this.points];

    }

    isVisible() {

        return this.visible;

    }

}

const heatmapManager = new HeatmapManager();

export default heatmapManager;

export { HeatmapManager };