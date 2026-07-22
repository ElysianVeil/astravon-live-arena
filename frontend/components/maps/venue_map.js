/*
============================================================
Astravon Live Arena
Venue Map Component

Purpose:
    Manages the interactive venue map using Leaflet.

Responsibilities:
    • Initialize venue map
    • Manage camera markers
    • Manage crowd markers
    • Manage emergency markers
    • Draw evacuation routes
    • Control map layers

Dependencies:
    Leaflet.js

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

class VenueMap {

    constructor(containerId = "venueMap") {

        this.containerId = containerId;

        this.map = null;

        this.layers = {

            cameras: L.layerGroup(),

            crowd: L.layerGroup(),

            emergency: L.layerGroup(),

            routes: L.layerGroup(),

            zones: L.layerGroup()

        };

        this.center = [-1.286389, 36.817223];

        this.zoom = 18;

    }

    /*
    ==========================================================
        Initialize Map
    ==========================================================
    */

    initialize(options = {}) {

        if (this.map) {

            this.resize();

            return this.map;

        }

        this.center = options.center ?? this.center;

        this.zoom = options.zoom ?? this.zoom;

        this.map = L.map(this.containerId, {

            zoomControl: true,

            attributionControl: false

        });

        L.tileLayer(

            "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",

            {

                maxZoom: 22

            }

        ).addTo(this.map);

        this.map.setView(

            this.center,

            this.zoom

        );

        Object.values(this.layers).forEach(layer =>

            layer.addTo(this.map)

        );

        return this.map;

    }

    /*
    ==========================================================
        Camera Markers
    ==========================================================
    */

    setCameras(cameras = []) {

        this.layers.cameras.clearLayers();

        cameras.forEach(camera => {

            const marker = L.marker(camera.position)

                .bindPopup(

                    `
                    <strong>${camera.name}</strong>
                    <br>
                    Status: ${camera.status}
                    `
                );

            marker.addTo(this.layers.cameras);

        });

    }

    /*
    ==========================================================
        Crowd Markers
    ==========================================================
    */

    setCrowdPoints(points = []) {

        this.layers.crowd.clearLayers();

        points.forEach(point => {

            const circle = L.circleMarker(

                point.position,

                {

                    radius: point.radius ?? 10,

                    color: point.color ?? "#22c55e",

                    fillOpacity: 0.7

                }

            );

            circle.bindPopup(

                `
                Crowd Density:
                ${point.density}
                `
            );

            circle.addTo(this.layers.crowd);

        });

    }

    /*
    ==========================================================
        Emergency Units
    ==========================================================
    */

    setEmergencyUnits(units = []) {

        this.layers.emergency.clearLayers();

        units.forEach(unit => {

            const marker = L.marker(unit.position)

                .bindPopup(

                    `
                    <strong>${unit.name}</strong>
                    <br>
                    ${unit.status}
                    `
                );

            marker.addTo(this.layers.emergency);

        });

    }

    /*
    ==========================================================
        Evacuation Routes
    ==========================================================
    */

    setRoutes(routes = []) {

        this.layers.routes.clearLayers();

        routes.forEach(route => {

            const polyline = L.polyline(

                route.coordinates,

                {

                    color: route.color ?? "#2563eb",

                    weight: 5

                }

            );

            polyline.addTo(this.layers.routes);

        });

    }

    /*
    ==========================================================
        Safety Zones
    ==========================================================
    */

    setZones(zones = []) {

        this.layers.zones.clearLayers();

        zones.forEach(zone => {

            const polygon = L.polygon(

                zone.coordinates,

                {

                    color: zone.color ?? "#f59e0b",

                    fillOpacity: 0.25

                }

            );

            polygon.bindPopup(

                zone.name

            );

            polygon.addTo(this.layers.zones);

        });

    }

    /*
    ==========================================================
        Visibility
    ==========================================================
    */

    showLayer(name) {

        if (

            this.layers[name] &&

            !this.map.hasLayer(this.layers[name])

        ) {

            this.layers[name].addTo(this.map);

        }

    }

    hideLayer(name) {

        if (

            this.layers[name] &&

            this.map.hasLayer(this.layers[name])

        ) {

            this.map.removeLayer(

                this.layers[name]

            );

        }

    }

    toggleLayer(name) {

        if (!this.layers[name]) {

            return;

        }

        if (this.map.hasLayer(this.layers[name])) {

            this.hideLayer(name);

        }

        else {

            this.showLayer(name);

        }

    }

    /*
    ==========================================================
        Utilities
    ==========================================================
    */

    fitBounds(bounds) {

        if (!this.map) return;

        this.map.fitBounds(bounds);

    }

    setCenter(position, zoom = this.zoom) {

        if (!this.map) return;

        this.map.setView(

            position,

            zoom

        );

    }

    resize() {

        if (!this.map) return;

        this.map.invalidateSize();

    }

    destroy() {

        if (!this.map) return;

        this.map.remove();

        this.map = null;

    }

}

const venueMap = new VenueMap();

export default venueMap;

export { VenueMap };