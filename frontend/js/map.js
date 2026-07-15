/*
============================================================
Astravon Live Arena
Map Manager

Purpose:
    Handles the live venue map, emergency units,
    crowd hotspots and evacuation routes.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

export default class MapManager {

    constructor() {

        /*
        =====================================================
        Map
        =====================================================
        */

        this.map = null;

        this.center = [-1.286389, 36.817223]; // Nairobi

        this.zoom = 17;

        /*
        =====================================================
        Layers
        =====================================================
        */

        this.crowdLayer = null;

        this.vehicleLayer = null;

        this.routeLayer = null;

        this.cameraLayer = null;

        this.hotspotLayer = null;

    }

    /*
    ==========================================================
    Initialize
    ==========================================================
    */

    initialize() {

        if (!window.L) {

            console.warn(
                "Leaflet.js not loaded."
            );

            return;

        }

        this.map = L.map(
            "crowdMap"
        ).setView(

            this.center,
            this.zoom

        );

        L.tileLayer(

            "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",

            {

                attribution:
                    "&copy; OpenStreetMap"

            }

        ).addTo(this.map);

        this.crowdLayer =
            L.layerGroup().addTo(this.map);

        this.vehicleLayer =
            L.layerGroup().addTo(this.map);

        this.routeLayer =
            L.layerGroup().addTo(this.map);

        this.cameraLayer =
            L.layerGroup().addTo(this.map);

        this.hotspotLayer =
            L.layerGroup().addTo(this.map);

        console.log(
            "[Map] Initialized."
        );

    }

    /*
    ==========================================================
    Add Camera
    ==========================================================
    */

    addCamera(

        latitude,
        longitude,
        name = "Camera"

    ) {

        if (!this.cameraLayer) {

            return;

        }

        L.marker([

            latitude,
            longitude

        ])

            .bindPopup(name)

            .addTo(
                this.cameraLayer
            );

    }

    /*
    ==========================================================
    Add Crowd Location
    ==========================================================
    */

    addCrowdMarker(

        latitude,
        longitude,
        people

    ) {

        if (!this.crowdLayer) {

            return;

        }

        L.circleMarker(

            [

                latitude,
                longitude

            ],

            {

                radius: 8

            }

        )

            .bindPopup(

                `People: ${people}`

            )

            .addTo(
                this.crowdLayer
            );

    }

    /*
    ==========================================================
    Add Hotspot
    ==========================================================
    */

    addHotspot(

        latitude,
        longitude,
        risk

    ) {

        if (!this.hotspotLayer) {

            return;

        }

        L.circle(

            [

                latitude,
                longitude

            ],

            {

                radius: 20

            }

        )

            .bindPopup(

                `Risk Score: ${risk}`

            )

            .addTo(
                this.hotspotLayer
            );

    }

    /*
    ==========================================================
    Add Emergency Vehicle
    ==========================================================
    */

    addEmergencyVehicle(

        latitude,
        longitude,
        label

    ) {

        if (!this.vehicleLayer) {

            return;

        }

        L.marker([

            latitude,
            longitude

        ])

            .bindPopup(label)

            .addTo(
                this.vehicleLayer
            );

    }

    /*
    ==========================================================
    Draw Route
    ==========================================================
    */

    drawRoute(points) {

        if (!this.routeLayer) {

            return;

        }

        L.polyline(

            points,

            {

                weight: 5

            }

        )

            .addTo(
                this.routeLayer
            );

    }

    /*
    ==========================================================
    Clear Crowd
    ==========================================================
    */

    clearCrowd() {

        if (this.crowdLayer) {

            this.crowdLayer.clearLayers();

        }

    }

    /*
    ==========================================================
    Clear Vehicles
    ==========================================================
    */

    clearVehicles() {

        if (this.vehicleLayer) {

            this.vehicleLayer.clearLayers();

        }

    }

    /*
    ==========================================================
    Clear Routes
    ==========================================================
    */

    clearRoutes() {

        if (this.routeLayer) {

            this.routeLayer.clearLayers();

        }

    }

    /*
    ==========================================================
    Clear Hotspots
    ==========================================================
    */

    clearHotspots() {

        if (this.hotspotLayer) {

            this.hotspotLayer.clearLayers();

        }

    }

    /*
    ==========================================================
    Clear Everything
    ==========================================================
    */

    clear() {

        this.clearCrowd();

        this.clearVehicles();

        this.clearRoutes();

        this.clearHotspots();

    }

}