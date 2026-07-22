/*
============================================================
Astravon Live Arena
Camera Card Component

Purpose:
    Represents a single live AI camera feed.

Author:
    House of Astravon
Version:
    2.0.0
============================================================
*/

export default class CameraCard {

    constructor(camera = {}) {

        this.camera = {

            id: camera.id || "",

            name: camera.name || "Unnamed Camera",

            location: camera.location || "Unknown",

            online: camera.online ?? false,

            recording: camera.recording ?? false,

            people: camera.people ?? 0,

            fps: camera.fps ?? "--",

            resolution: camera.resolution || "--",

            risk: camera.risk || "Low",

            ...camera

        };

        this.element = null;

        this.frame = null;

        this.frameCount = 0;

        this.connected = false;

        this.loading = true;

        this.error = null;

        this.latestFrame = null;

        this.rendering = false;

    }

    /*==========================================================
        Render
    ==========================================================*/

    render() {

        const article = document.createElement("article");

        article.className = "camera-card";

        article.dataset.cameraId = this.camera.id;

        article.innerHTML = `

            <div class="camera-card-header">

                <div>

                    <h3>${this.camera.name}</h3>

                    <small>${this.camera.location}</small>

                </div>

                <span class="camera-status badge danger">

                    Offline

                </span>

            </div>

            <div class="camera-preview">

                <img
                    class="camera-frame"
                    src=""
                    alt="${this.camera.name}"
                    style="display:none"
                >

                <div class="camera-placeholder">

                    Waiting for video stream...

                </div>

            </div>

            <div class="camera-info">

                <div>

                    <span>Resolution</span>

                    <strong class="camera-resolution">

                        ${this.camera.resolution}

                    </strong>

                </div>

                <div>

                    <span>FPS</span>

                    <strong class="camera-fps">

                        ${this.camera.fps}

                    </strong>

                </div>

                <div>

                    <span>Frames</span>

                    <strong class="camera-frames">

                        0

                    </strong>

                </div>

                <div>

                    <span>People</span>

                    <strong class="camera-people">

                        ${this.camera.people}

                    </strong>

                </div>

                <div>

                    <span>Risk</span>

                    <strong class="camera-risk">

                        ${this.camera.risk}

                    </strong>

                </div>

            </div>

        `;

        this.element = article;

        return article;

    }

    /*==========================================================
        Connection
    ==========================================================*/

    connect() {

        this.connected = true;

        this.loading = false;

        this.updateBadge();

    }

    disconnect() {

        this.connected = false;

        this.updateBadge();

    }

    updateBadge() {

        if (!this.element) return;

        const badge =

            this.element.querySelector(".camera-status");

        if (!badge) return;

        if (this.connected) {

            badge.textContent = "Live";

            badge.className =

                "camera-status badge success";

        }

        else {

            badge.textContent = "Offline";

            badge.className =

                "camera-status badge danger";

        }

    }

    /*==========================================================
        Live Frame
    ==========================================================*/

    updateFrame(frame) {

        if (!this.element) return;

        const image =

            this.element.querySelector(".camera-frame");

        const placeholder =

            this.element.querySelector(".camera-placeholder");

        if (frame.startsWith("data:")) {
            image.src = frame;
        }
        else {
            image.src = `data:image/jpeg;base64,${frame}`;
        }

        image.style.display = "block";

        placeholder.style.display = "none";

        this.frame = frame;

        this.frameCount++;

        this.connect();

        this.element.querySelector(

            ".camera-frames"

        ).textContent = this.frameCount;

    }

    /*==========================================================
        Camera Information
    ==========================================================*/

    updateInfo(data = {}) {

        Object.assign(this.camera, data);

        if (!this.element) return;

        this.element.querySelector(

            ".camera-resolution"

        ).textContent = this.camera.resolution;

        this.element.querySelector(

            ".camera-fps"

        ).textContent = this.camera.fps;

        this.element.querySelector(

            ".camera-people"

        ).textContent = this.camera.people;

        this.element.querySelector(

            ".camera-risk"

        ).textContent = this.camera.risk;

    }

    /*==========================================================
        Statistics Update
    ==========================================================*/

    updateStatistics(statistics = {}) {

        if (!statistics) return;


        this.updateInfo({

            people:
                statistics
                ?.detection
                ?.people_count ?? 0,


            risk:
                statistics
                ?.risk
                ?.risk_level ?? "Unknown"

        });


    }

    /*==========================================================
        Loading
    ==========================================================*/

    showLoading() {

        this.loading = true;

        if (!this.element) return;

        this.element.querySelector(

            ".camera-placeholder"

        ).textContent =

            "Connecting to AI Engine...";

    }

    /*==========================================================
        Error
    ==========================================================*/

    showError(message) {

        this.loading = false;

        this.connected = false;

        this.error = message;

        if (!this.element) return;

        const image =

            this.element.querySelector(".camera-frame");

        const placeholder =

            this.element.querySelector(".camera-placeholder");

        image.style.display = "none";

        placeholder.style.display = "flex";

        placeholder.textContent = message;

        this.updateBadge();

    }

    /*==========================================================
        Clear
    ==========================================================*/

    clear() {

        if (!this.element) return;

        this.disconnect();

        this.frame = null;

        this.frameCount = 0;

        const image =

            this.element.querySelector(".camera-frame");

        const placeholder =

            this.element.querySelector(".camera-placeholder");

        image.src = "";

        image.style.display = "none";

        placeholder.style.display = "flex";

        placeholder.textContent =

            "Waiting for video stream...";

        this.element.querySelector(

            ".camera-frames"

        ).textContent = "0";

    }

    /*==========================================================
        Data
    ==========================================================*/

    getData() {

        return {

            ...this.camera,

            connected: this.connected,

            frameCount: this.frameCount,

            loading: this.loading,

            error: this.error

        };

    }

}