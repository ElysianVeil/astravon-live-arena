/*
============================================================
Astravon Live Arena
Frontend Router

Purpose:
    Handles page navigation for the application.

    Keeps browser history synchronized with
    the global application state.

Author:
    House of Astravon

Version:
    2.0.0
============================================================
*/

import state from "./state.js";
import eventBus from "./event_bus.js";

class Router {

    constructor() {

        this.routes = new Map();

        this.currentRoute = null;

        this.defaultRoute = "dashboard";

        this.notFoundRoute = null;

        this.beforeHooks = [];
        this.afterHooks = [];

    }

    /*
    ============================================================
    Initialize
    ============================================================
    */

    initialize() {

        window.addEventListener(

            "popstate",

            () => {

                this.resolve(

                    location.pathname

                );

            }

        );

        this.resolve(

            location.pathname

        );

    }

    /*
    ============================================================
    Register Route
    ============================================================
    */

    register(

        path,

        callback

    ) {

        this.routes.set(

            path,

            callback

        );

    }

    /*
    ============================================================
    Register Multiple
    ============================================================
    */

    registerRoutes(routes) {

        Object.entries(routes).forEach(

            ([path, callback]) => {

                this.register(

                    path,

                    callback

                );

            }

        );

    }

    beforeEach(callback) {

        this.beforeHooks.push(callback);

    }

    afterEach(callback) {

        this.afterHooks.push(callback);

    }

    /*
    ============================================================
    Not Found
    ============================================================
    */

    setNotFound(callback) {

        this.notFoundRoute = callback;

    }

    /*
    ============================================================
    Navigate
    ============================================================
    */

    async navigate(

        path,

        push = true

    ) {

        if (

            !path.startsWith("/")

        ) {

            path = "/" + path;

        }

        if (push) {
            const previous = this.currentRoute;
            const next = path.replace(/^\/+/, "") || this.defaultRoute;

            for (const hook of this.beforeHooks) {
                await hook(previous, next);
            }

            history.pushState(

                {},

                "",

                path

            );

        }

        this.resolve(path);

        for (const hook of this.afterHooks) {
            await hook(previous, next);
        }

    }

    /*
    ============================================================
    Resolve
    ============================================================
    */

    resolve(path) {

        const clean =

            path.replace(/^\/+/,"")

            ||

            this.defaultRoute;

        const callback =

            this.routes.get(clean);

        if (!callback) {

            this.currentRoute =

                "404";

            state.merge(

                "app",

                {

                    page:"404"

                }

            );

            eventBus.emit(

                "route:notFound",

                clean

            );

            this.notFoundRoute?.();

            return;

        }

        this.currentRoute = clean;

        state.merge(

            "app",

            {

                page: clean

            }

        );

        eventBus.emit(

            "route:changed",

            clean

        );

        callback();

    }

    /*
    ============================================================
    Refresh
    ============================================================
    */

    refresh() {

        this.resolve(

            location.pathname

        );

    }

    /*
    ============================================================
    Current
    ============================================================
    */

    current() {

        return this.currentRoute;

    }

    /*
    ============================================================
    Exists
    ============================================================
    */

    has(path) {

        return this.routes.has(path);

    }

    /*
    ============================================================
    List Routes
    ============================================================
    */

    list() {

        return [

            ...this.routes.keys()

        ];

    }

    /*
    ============================================================
    Default Route
    ============================================================
    */

    setDefault(route) {

        this.defaultRoute = route;

    }

    /*
    ============================================================
    Helpers
    ============================================================
    */

    dashboard() {

        this.navigate(

            "/dashboard"

        );

    }

    cameras() {

        this.navigate(

            "/cameras"

        );

    }

    analytics() {

        this.navigate(

            "/analytics"

        );

    }

    risk() {

        this.navigate(

            "/risk"

        );

    }

    maps() {

        this.navigate(

            "/maps"

        );

    }

    people() {

        this.navigate(

            "/people"

        );

    }

    reports() {

        this.navigate(

            "/reports"

        );

    }

    settings() {

        this.navigate(

            "/settings"

        );

    }

}

/*
============================================================
Singleton
============================================================
*/

export const router =

    new Router();

export default router;