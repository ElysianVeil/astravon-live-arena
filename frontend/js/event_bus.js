/*
============================================================
Astravon Live Arena
Global Event Bus

Purpose:
    Lightweight publish-subscribe system that
    enables communication between independent
    frontend components.

Author:
    House of Astravon

Version:
    2.0.0
============================================================
*/

class EventBus {

    constructor() {

        this.events = new Map();

        this.debug = false;

    }

    /*
    ============================================================
    Debug
    ============================================================
    */

    enableDebug() {

        this.debug = true;

    }

    disableDebug() {

        this.debug = false;

    }

    /*
    ============================================================
    Subscribe
    ============================================================
    */

    on(

        event,

        callback

    ) {

        if (

            typeof callback !== "function"

        ) {

            throw new Error(

                "Event callback must be a function."

            );

        }

        if (

            !this.events.has(event)

        ) {

            this.events.set(

                event,

                new Set()

            );

        }

        this.events

            .get(event)

            .add(callback);

        if (this.debug) {

            console.log(

                `[EventBus] Subscribed -> ${event}`

            );

        }

        return () => {

            this.off(

                event,

                callback

            );

        };

    }

    /*
    ============================================================
    Subscribe Once
    ============================================================
    */

    once(

        event,

        callback

    ) {

        const wrapper = payload => {

            callback(payload);

            this.off(

                event,

                wrapper

            );

        };

        return this.on(

            event,

            wrapper

        );

    }

    /*
    ============================================================
    Unsubscribe
    ============================================================
    */

    off(

        event,

        callback

    ) {

        const listeners =

            this.events.get(event);

        if (!listeners) {

            return;

        }

        listeners.delete(callback);

        if (

            listeners.size === 0

        ) {

            this.events.delete(event);

        }

        if (this.debug) {

            console.log(

                `[EventBus] Unsubscribed -> ${event}`

            );

        }

    }

    /*
    ============================================================
    Emit
    ============================================================
    */

    emit(

        event,

        payload = null

    ) {

        const listeners =

            this.events.get(event);

        if (!listeners) {

            return;

        }

        if (this.debug) {

            console.log(

                `[EventBus] Emit -> ${event}`,

                payload

            );

        }

        listeners.forEach(listener => {

            try {

                listener(payload);

            }

            catch (error) {

                console.error(

                    `[EventBus] ${event}`,

                    error

                );

            }

        });

    }

    /*
    ============================================================
    Async Emit
    ============================================================
    */

    async emitAsync(

        event,

        payload = null

    ) {

        const listeners =

            this.events.get(event);

        if (!listeners) {

            return;

        }

        for (

            const listener of listeners

        ) {

            try {

                await listener(payload);

            }

            catch (error) {

                console.error(

                    `[EventBus] ${event}`,

                    error

                );

            }

        }

    }

    /*
    ============================================================
    Clear Event
    ============================================================
    */

    clear(event) {

        this.events.delete(event);

    }

    /*
    ============================================================
    Clear All
    ============================================================
    */

    clearAll() {

        this.events.clear();

    }

    /*
    ============================================================
    Information
    ============================================================
    */

    listenerCount(event) {

        return this.events.has(event)

            ? this.events

                  .get(event)

                  .size

            : 0;

    }

    has(event) {

        return this.events.has(event);

    }

    eventsList() {

        return [

            ...this.events.keys()

        ];

    }

    /*
    ============================================================
    Diagnostics
    ============================================================
    */

    stats() {

        const stats = {};

        this.events.forEach(

            (

                listeners,

                event

            ) => {

                stats[event] =

                    listeners.size;

            }

        );

        return stats;

    }

}

/*
============================================================
Singleton
============================================================
*/

export const eventBus =

    new EventBus();

export default eventBus;