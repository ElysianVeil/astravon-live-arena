/*
============================================================
Astravon Live Arena
Emergency & Navigation Routes

File:
    routes.js

Purpose:
    Handles:
    • Emergency evacuation routes
    • Security patrol routes
    • Medical response routes
    • Route rendering
    • Route visibility
    • Route updates

Author:
    House of Astravon
============================================================
*/

import { VenueMap } from "./venue_map.js";

/* ============================================================
   Internal State
============================================================ */

let evacuationLayer = null;
let responseLayer = null;
let patrolLayer = null;

let evacuationVisible = true;
let responseVisible = true;
let patrolVisible = false;

/* ============================================================
   Layer Creation
============================================================ */

function ensureLayers() {

    const map = getVenueMap();

    if (!map) return;

    if (!evacuationLayer) {

        evacuationLayer = L.layerGroup().addTo(map);

    }

    if (!responseLayer) {

        responseLayer = L.layerGroup().addTo(map);

    }

    if (!patrolLayer) {

        patrolLayer = L.layerGroup().addTo(map);

    }

}

/* ============================================================
   Clear
============================================================ */

function clearLayer(layer) {

    if (layer) {

        layer.clearLayers();

    }

}

/* ============================================================
   Draw Polyline
============================================================ */

function drawRoute(layer, coordinates, options = {}) {

    return L.polyline(coordinates, {

        weight: options.weight ?? 5,

        color: options.color ?? "#D4AF37",

        opacity: options.opacity ?? 0.9,

        dashArray: options.dashArray ?? null

    }).addTo(layer);

}

/* ============================================================
   Evacuation Routes
============================================================ */

export function renderEvacuationRoutes(routes = []) {

    ensureLayers();

    clearLayer(evacuationLayer);

    routes.forEach(route => {

        drawRoute(
            evacuationLayer,
            route.points,
            {
                color: "#22C55E",
                weight: 6
            }
        );

    });

}

/* ============================================================
   Emergency Response
============================================================ */

export function renderResponseRoutes(routes = []) {

    ensureLayers();

    clearLayer(responseLayer);

    routes.forEach(route => {

        drawRoute(
            responseLayer,
            route.points,
            {
                color: "#EF4444",
                weight: 5
            }
        );

    });

}

/* ============================================================
   Security Patrol
============================================================ */

export function renderPatrolRoutes(routes = []) {

    ensureLayers();

    clearLayer(patrolLayer);

    routes.forEach(route => {

        drawRoute(
            patrolLayer,
            route.points,
            {
                color: "#3B82F6",
                dashArray: "8 6",
                weight: 4
            }
        );

    });

}

/* ============================================================
   Visibility
============================================================ */

export function toggleEvacuationRoutes(show) {

    ensureLayers();

    evacuationVisible = show;

    if (show) {

        evacuationLayer.addTo(getVenueMap());

    } else {

        evacuationLayer.remove();

    }

}

export function toggleResponseRoutes(show) {

    ensureLayers();

    responseVisible = show;

    if (show) {

        responseLayer.addTo(getVenueMap());

    } else {

        responseLayer.remove();

    }

}

export function togglePatrolRoutes(show) {

    ensureLayers();

    patrolVisible = show;

    if (show) {

        patrolLayer.addTo(getVenueMap());

    } else {

        patrolLayer.remove();

    }

}

/* ============================================================
   Remove All
============================================================ */

export function clearRoutes() {

    clearLayer(evacuationLayer);

    clearLayer(responseLayer);

    clearLayer(patrolLayer);

}

/* ============================================================
   Sample Data
============================================================ */

export function loadDemoRoutes() {

    renderEvacuationRoutes([
        {
            points: [
                [-1.2860, 36.8170],
                [-1.2855, 36.8180],
                [-1.2850, 36.8190]
            ]
        },
        {
            points: [
                [-1.2864, 36.8162],
                [-1.2860, 36.8170],
                [-1.2852, 36.8176]
            ]
        }
    ]);

    renderResponseRoutes([
        {
            points: [
                [-1.2870, 36.8160],
                [-1.2864, 36.8170],
                [-1.2856, 36.8180]
            ]
        }
    ]);

    renderPatrolRoutes([
        {
            points: [
                [-1.2868, 36.8185],
                [-1.2862, 36.8176],
                [-1.2856, 36.8168]
            ]
        }
    ]);

}

/* ============================================================
   Getters
============================================================ */

export function isEvacuationVisible() {

    return evacuationVisible;

}

export function isResponseVisible() {

    return responseVisible;

}

export function isPatrolVisible() {

    return patrolVisible;

}

/* ============================================================
   Default Export
============================================================ */

export default {

    renderEvacuationRoutes,

    renderResponseRoutes,

    renderPatrolRoutes,

    toggleEvacuationRoutes,

    toggleResponseRoutes,

    togglePatrolRoutes,

    clearRoutes,

    loadDemoRoutes,

    isEvacuationVisible,

    isResponseVisible,

    isPatrolVisible

};