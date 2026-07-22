/*
============================================================
Astravon Live Arena
Camera Grid Component

Purpose:
    Manages live camera cards and routes
    incoming camera updates to the correct card.

Author:
    House of Astravon
Version:
    2.0.0
============================================================
*/

import CameraCard from "./camera_card.js";
import EventBus from "../../js/event_bus.js";

class CameraGrid {

    constructor(containerId = "cameraGrid") {

        this.containerId = containerId;

        this.container = null;

        this.bound = false;

        this.columns = 2;

        this.cards = new Map();

    }

    /*==========================================================
        Initialize
    ==========================================================*/

    initialize(containerId = null) {

        if (containerId) {

            this.containerId = containerId;

        }

        console.log("CameraGrid.initialize()");

        this.container = document.getElementById(
            this.containerId
        );

        if (!this.container) {

            console.warn(
                `CameraGrid: '${this.containerId}' not found.`
            );

            return false;

        }

        console.log(this.container);

        this.configureGrid();

        if (this.cards.size === 0) {

            this.renderEmpty();

        } else {

            for (const card of this.cards.values()) {

                this.container.appendChild(card.element);

            }

        }

        // this.bindEvents();

        return true;

    }

    /*==========================================================
        Grid Layout
    ==========================================================*/

    configureGrid() {

        if (!this.container) return;

        this.container.style.display = "grid";

        this.container.style.gridTemplateColumns =
            `repeat(${this.columns}, 1fr)`;

        this.container.style.gap = "1rem";

    }

    setColumns(columns = 2) {

        this.columns = columns;

        this.configureGrid();

    }

    /*==========================================================
        Cameras
    ==========================================================*/

    setCameras(cameras = []) {

        this.clear();

        cameras.forEach(camera => {

            this.addCamera(camera);

        });

    }

    addCamera(camera) {

        if (!this.container) return;

        console.log("Adding camera:", camera);

        const card = new CameraCard(camera);

        this.cards.set(camera.id, card);

        this.removeEmptyState();

        this.container.appendChild(

            card.render()

        );

    }

    removeCamera(cameraId) {

        const card = this.cards.get(cameraId);

        if (!card) return;

        card.element.remove();

        this.cards.delete(cameraId);

        if (this.cards.size === 0) {

            this.renderEmpty();

        }

    }

    /*==========================================================
        Stream Management
    ==========================================================*/

    updateFrame(cameraId, payload) {

        console.log("container =", this.container);
        console.log("cards before =", this.cards.size);

        let card = this.cards.get(cameraId);

        if (!card) {

            console.log("Creating card...");

            this.addCamera({

                id: cameraId,

                name:
                    payload.camera_name ??
                    "Unknown Camera",

                resolution:
                    `${payload.width} × ${payload.height}`,

                fps: payload.fps,

                people:
                    payload.statistics?.detection?.people_count ?? 0,

                risk:
                    payload.statistics?.risk?.risk_level ?? "Low"

            });

            console.log("cards after =", this.cards.size);

            card = this.cards.get(cameraId);

            console.log("card =", card);

        }

        card.updateFrame(payload.frame);

        card.updateInfo({

            fps: payload.fps,

            resolution:
                `${payload.width} × ${payload.height}`,

            people:
                payload.statistics?.detection?.people_count ?? 0,

            risk:
                payload.statistics?.risk?.level ?? "Low"

        });

    }

    updateStatistics(cameraId, statistics){

        const card =
            this.cards.get(cameraId);


        if(!card) return;


        card.updateStatistics(statistics);

    }

    bindEvents() {

        console.log("bindEvents() called");

        if (this.bound) {
            return;
        }

        this.bound = true;

        EventBus.on("camera:frame", payload => {

            console.log("camera:frame received", payload);

            this.updateFrame(
                payload.camera_id,
                payload
            );

        });

    }

    connectCamera(cameraId) {

        const card =

            this.cards.get(cameraId);

        if (!card) return;

        card.connect();

    }

    disconnectCamera(cameraId) {

        const card =

            this.cards.get(cameraId);

        if (!card) return;

        card.disconnect();

    }

    updateInfo(cameraId, data = {}) {

        const card =

            this.cards.get(cameraId);

        if (!card) return;

        card.updateInfo(data);

    }

    showLoading(cameraId) {

        const card =

            this.cards.get(cameraId);

        if (!card) return;

        card.showLoading();

    }

    showError(cameraId, message) {

        const card =

            this.cards.get(cameraId);

        if (!card) return;

        card.showError(message);

    }

    clearCamera(cameraId) {

        const card =

            this.cards.get(cameraId);

        if (!card) return;

        card.clear();

    }

    /*==========================================================
        Lookup
    ==========================================================*/

    getCamera(cameraId) {

        return this.cards.get(cameraId);

    }

    getAll() {

        return Array.from(

            this.cards.values()

        );

    }

    count() {

        return this.cards.size;

    }

    /*==========================================================
        Empty State
    ==========================================================*/

    renderEmpty() {

        if (!this.container) return;

        if (this.cards.size !== 0) return;

        this.container.innerHTML = `

            <div class="empty-state">

                <h3>

                    No Cameras Connected

                </h3>

                <p>

                    Connect a camera to begin monitoring.

                </p>

            </div>

        `;

    }

    removeEmptyState() {

        const empty =

            this.container.querySelector(

                ".empty-state"

            );

        if (empty) {

            empty.remove();

        }

    }

    /*==========================================================
        Clear
    ==========================================================*/

    clear() {

        if (!this.container) return;

        this.cards.clear();

        this.container.innerHTML = "";

        this.renderEmpty();

    }

    /*==========================================================
        Refresh
    ==========================================================*/

    refresh() {

        this.cards.forEach(card => {

            card.updateInfo(

                card.getData()

            );

        });

    }

}

export const cameraGrid = new CameraGrid();

export default CameraGrid;