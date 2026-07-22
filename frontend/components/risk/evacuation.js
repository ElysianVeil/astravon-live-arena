/*
============================================================
Astravon Live Arena
Evacuation Manager

Purpose:
    Coordinates evacuation routes, assembly areas,
    emergency exits and response units during
    emergency situations.

Responsibilities
    • Register evacuation routes
    • Register assembly areas
    • Activate evacuation plan
    • Select safest route
    • Track evacuation status
    • Notify subscribers

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

class EvacuationManager {

    constructor() {

        this.active = false;

        this.routes = [];

        this.assemblyAreas = [];

        this.responseUnits = [];

        this.currentRoute = null;

        this.statistics = {

            evacuated: 0,

            remaining: 0,

            capacity: 0,

            progress: 0

        };

        this.listeners = [];

        this.routeContainer = null;

        this.responseContainer = null;

        this.assemblyContainer = null;

    }

    /*==========================================================
        Initialization
    ==========================================================*/

    initialize() {

        this.routeContainer =
            document.getElementById(
                "evacuationRoutes"
            );

        this.responseContainer =
            document.getElementById(
                "responseVehicles"
            );

        this.assemblyContainer =
            document.getElementById(
                "assemblyAreas"
            );

        this.render();

    }

    /*==========================================================
        Routes
    ==========================================================*/

    setRoutes(routes = []) {

        this.routes = routes;

        this.render();

        this.notify();

    }

    addRoute(route) {

        this.routes.push(route);

        this.render();

        this.notify();

    }

    removeRoute(id) {

        this.routes = this.routes.filter(

            route => route.id !== id

        );

        this.render();

        this.notify();

    }

    /*==========================================================
        Assembly Areas
    ==========================================================*/

    setAssemblyAreas(areas = []) {

        this.assemblyAreas = areas;

        this.render();

    }

    addAssemblyArea(area) {

        this.assemblyAreas.push(area);

        this.render();

    }

    /*==========================================================
        Response Units
    ==========================================================*/

    setResponseUnits(units = []) {

        this.responseUnits = units;

        this.render();

    }

    addResponseUnit(unit) {

        this.responseUnits.push(unit);

        this.render();

    }

    /*==========================================================
        Evacuation
    ==========================================================*/

    start(routeId = null) {

        this.active = true;

        if (routeId) {

            this.currentRoute =
                this.routes.find(

                    route => route.id === routeId

                ) || null;

        } else {

            this.currentRoute =
                this.getSafestRoute();

        }

        this.notify();

        this.render();

    }

    stop() {

        this.active = false;

        this.currentRoute = null;

        this.notify();

        this.render();

    }

    /*==========================================================
        Statistics
    ==========================================================*/

    updateStatistics(data = {}) {

        this.statistics = {

            ...this.statistics,

            ...data

        };

        this.notify();

    }

    /*==========================================================
        Route Selection
    ==========================================================*/

    getSafestRoute() {

        if (this.routes.length === 0) {

            return null;

        }

        return [...this.routes]

            .sort(

                (a, b) =>

                    (a.risk ?? 0) -

                    (b.risk ?? 0)

            )[0];

    }

    /*==========================================================
        Rendering
    ==========================================================*/

    render() {

        this.renderRoutes();

        this.renderAssembly();

        this.renderResponse();

    }

    renderRoutes() {

        if (!this.routeContainer) return;

        if (!this.routes.length) {

            this.routeContainer.innerHTML = `

                <div class="empty-state">

                    <h3>

                        No Evacuation Routes

                    </h3>

                </div>

            `;

            return;

        }

        this.routeContainer.innerHTML =

            this.routes.map(

                route => `

                <article class="dashboard-widget">

                    <div class="widget-header">

                        <strong>

                            ${route.name}

                        </strong>

                        <span>

                            ${route.distance ?? "--"} m

                        </span>

                    </div>

                    <div>

                        Capacity:
                        ${route.capacity ?? "--"}

                    </div>

                    <div>

                        Risk:
                        ${route.risk ?? "--"}

                    </div>

                </article>

                `

            ).join("");

    }

    renderAssembly() {

        if (!this.assemblyContainer) return;

        if (!this.assemblyAreas.length) {

            this.assemblyContainer.innerHTML =

                "<p>No assembly areas.</p>";

            return;

        }

        this.assemblyContainer.innerHTML =

            this.assemblyAreas.map(

                area => `

                <article class="dashboard-widget">

                    <strong>

                        ${area.name}

                    </strong>

                    <div>

                        Capacity:
                        ${area.capacity}

                    </div>

                    <div>

                        Occupancy:
                        ${area.occupancy}

                    </div>

                </article>

                `

            ).join("");

    }

    renderResponse() {

        if (!this.responseContainer) return;

        if (!this.responseUnits.length) {

            this.responseContainer.innerHTML =

                "<p>No response units.</p>";

            return;

        }

        this.responseContainer.innerHTML =

            this.responseUnits.map(

                vehicle => `

                <article class="dashboard-widget">

                    <strong>

                        ${vehicle.name}

                    </strong>

                    <div>

                        Status:
                        ${vehicle.status}

                    </div>

                    <div>

                        ETA:
                        ${vehicle.eta}

                    </div>

                </article>

                `

            ).join("");

    }

    /*==========================================================
        Getters
    ==========================================================*/

    isActive() {

        return this.active;

    }

    getCurrentRoute() {

        return this.currentRoute;

    }

    getRoutes() {

        return [...this.routes];

    }

    getAssemblyAreas() {

        return [...this.assemblyAreas];

    }

    getResponseUnits() {

        return [...this.responseUnits];

    }

    getStatistics() {

        return {

            ...this.statistics

        };

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

        const snapshot = {

            active: this.active,

            currentRoute: this.currentRoute,

            statistics: this.statistics,

            routes: this.routes,

            assemblyAreas: this.assemblyAreas,

            responseUnits: this.responseUnits

        };

        this.listeners.forEach(

            listener => listener(snapshot)

        );

    }

}

/*============================================================
Singleton
============================================================*/

const evacuationManager =
    new EvacuationManager();

export default evacuationManager;

export {

    EvacuationManager

};