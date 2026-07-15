/*
============================================================
Astravon Live Arena
Camera Panel Component

Purpose:
    Displays the live AI camera feed together
    with camera status and stream information.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

export default class CameraPanel {

    constructor() {

        this.container = null;

        this.imageElement = null;

        this.statusElement = null;

        this.infoElement = null;

        this.connected = false;

        this.frameCount = 0;

    }

    /*
    ==========================================================
    Initialize
    ==========================================================
    */

    initialize() {

        this.container = document.getElementById(
            "cameraPanel"
        );

        if (!this.container) {

            console.warn(
                "[Camera Panel] Container not found."
            );

            return;

        }

        this.render();

        console.log(
            "[Camera Panel] Initialized."
        );

    }

    /*
    ==========================================================
    Render
    ==========================================================
    */

    render() {

        this.container.innerHTML = `

            <div class="camera-header">

                <h2>

                    📷 Live Camera

                </h2>

                <span
                    id="cameraStatus"
                    class="camera-status offline"
                >

                    Offline

                </span>

            </div>

            <div class="camera-body">

                <img

                    id="cameraFrame"

                    class="camera-frame"

                    src=""

                    alt="Camera Feed"

                />

                <div
                    id="cameraPlaceholder"
                    class="camera-placeholder"
                >

                    Waiting for video stream...

                </div>

            </div>

            <div
                id="cameraInfo"
                class="camera-info"
            >

                Frames: 0

            </div>

        `;

        this.imageElement =

            document.getElementById(
                "cameraFrame"
            );

        this.statusElement =

            document.getElementById(
                "cameraStatus"
            );

        this.infoElement =

            document.getElementById(
                "cameraInfo"
            );

    }

    /*
    ==========================================================
    Connect
    ==========================================================
    */

    connect() {

        this.connected = true;

        this.statusElement.textContent =

            "Live";

        this.statusElement.className =

            "camera-status online";

    }

    /*
    ==========================================================
    Disconnect
    ==========================================================
    */

    disconnect() {

        this.connected = false;

        this.statusElement.textContent =

            "Offline";

        this.statusElement.className =

            "camera-status offline";

    }

    /*
    ==========================================================
    Update Frame
    ==========================================================
    */

    updateFrame(payload) {

        if (!this.imageElement) return;

        let image = payload;

        if (typeof payload === "object") {
            image = payload.frame;
        }

        if (!image) {
            console.warn("No frame received.");
            return;
        }

        this.connect();

        this.imageElement.src =
            `data:image/jpeg;base64,${image}`;

        this.imageElement.style.display = "block";

        document.getElementById(
            "cameraPlaceholder"
        )?.style.setProperty(
            "display",
            "none"
        );

        this.frameCount++;

        this.infoElement.innerHTML = `
            Frames: ${this.frameCount}
        `;
    }

    /*
    ==========================================================
    Update Camera Information
    ==========================================================
    */

    updateInfo(info = {}) {

        if (!this.infoElement) {

            return;

        }

        const {

            width = "--",

            height = "--",

            fps = "--"

        } = info;

        this.infoElement.innerHTML = `

            Resolution :
            ${width} × ${height}

            <br>

            FPS :
            ${fps}

            <br>

            Frames :
            ${this.frameCount}

        `;

    }

    /*
    ==========================================================
    Clear Stream
    ==========================================================
    */

    clear() {

        this.disconnect();

        this.frameCount = 0;

        if (this.imageElement) {

            this.imageElement.src = "";

            this.imageElement.style.display =

                "none";

        }

        const placeholder =

            document.getElementById(
                "cameraPlaceholder"
            );

        if (placeholder) {

            placeholder.style.display =

                "flex";

        }

        if (this.infoElement) {

            this.infoElement.textContent =

                "Frames: 0";

        }

    }

    /*
    ==========================================================
    Loading
    ==========================================================
    */

    showLoading() {

        const placeholder =

            document.getElementById(
                "cameraPlaceholder"
            );

        if (placeholder) {

            placeholder.textContent =

                "Connecting to AI Engine...";

        }

    }

    /*
    ==========================================================
    Error
    ==========================================================
    */

    showError(message) {

        this.disconnect();

        const placeholder =

            document.getElementById(
                "cameraPlaceholder"
            );

        if (placeholder) {

            placeholder.textContent =

                message;

            placeholder.style.display =

                "flex";

        }

    }

}