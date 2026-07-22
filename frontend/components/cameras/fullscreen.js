/*
============================================================
Astravon Live Arena
Fullscreen Manager

Purpose:
    Provides fullscreen functionality for the
    dashboard, camera grid, venue map and other
    monitoring panels.

Author:
    House of Astravon
Version:
    1.0.0
============================================================
*/

class FullscreenManager {

    constructor() {

        this.currentElement = null;

        this.callbacks = {

            enter: [],

            exit: [],

            change: []

        };

        this.initialize();

    }

    /*==========================================================
        Initialize
    ==========================================================*/

    initialize() {

        document.addEventListener(

            "fullscreenchange",

            () => this.handleFullscreenChange()

        );

    }

    /*==========================================================
        Enter Fullscreen
    ==========================================================*/

    async enter(element) {

        if (!element) return false;

        try {

            if (document.fullscreenElement) {

                await document.exitFullscreen();

            }

            await element.requestFullscreen();

            this.currentElement = element;

            return true;

        }

        catch (error) {

            console.error(

                "Unable to enter fullscreen:",

                error

            );

            return false;

        }

    }

    /*==========================================================
        Exit Fullscreen
    ==========================================================*/

    async exit() {

        try {

            if (document.fullscreenElement) {

                await document.exitFullscreen();

            }

        }

        catch (error) {

            console.error(

                "Unable to exit fullscreen:",

                error

            );

        }

    }

    /*==========================================================
        Toggle Fullscreen
    ==========================================================*/

    async toggle(element) {

        if (this.isFullscreen()) {

            return this.exit();

        }

        return this.enter(element);

    }

    /*==========================================================
        State
    ==========================================================*/

    isFullscreen() {

        return !!document.fullscreenElement;

    }

    getCurrentElement() {

        return document.fullscreenElement;

    }

    /*==========================================================
        Event Handler
    ==========================================================*/

    handleFullscreenChange() {

        const active = this.isFullscreen();

        if (!active) {

            this.currentElement = null;

            this.callbacks.exit.forEach(

                callback => callback()

            );

        }

        else {

            this.currentElement =

                document.fullscreenElement;

            this.callbacks.enter.forEach(

                callback => callback(this.currentElement)

            );

        }

        this.callbacks.change.forEach(

            callback => callback(

                active,

                this.currentElement

            )

        );

    }

    /*==========================================================
        Callback Registration
    ==========================================================*/

    onEnter(callback) {

        this.callbacks.enter.push(callback);

    }

    onExit(callback) {

        this.callbacks.exit.push(callback);

    }

    onChange(callback) {

        this.callbacks.change.push(callback);

    }

    /*==========================================================
        Helpers
    ==========================================================*/

    fullscreenById(id) {

        const element = document.getElementById(id);

        if (!element) {

            console.warn(

                `Fullscreen: '${id}' not found.`

            );

            return;

        }

        this.toggle(element);

    }

}

/*============================================================
    Singleton
============================================================*/

export const Fullscreen = new FullscreenManager();

export default Fullscreen;