/*
============================================================
Astravon Live Arena
Notification Manager

Purpose
    Handles toast notifications throughout
    the application.

Author
    House of Astravon

Version
    1.0.0
============================================================
*/

export default class NotificationManager {

    constructor() {

        this.container = null;

        this.defaultDuration = 5000;

        this.counter = 0;

    }

    /*
    ==========================================================
    Initialize
    ==========================================================
    */

    initialize() {

        this.container = document.getElementById(
            "toastContainer"
        );

        if (!this.container) {

            console.warn(
                "[Notifications] Toast container not found."
            );

            return;

        }

        console.log(
            "[Notifications] Initialized."
        );

    }

    /*
    ==========================================================
    Generic Notification
    ==========================================================
    */

    show({

        title = "",

        message = "",

        type = "info",

        duration = this.defaultDuration

    }) {

        if (!this.container) {

            return;

        }

        const id = `toast-${++this.counter}`;

        const toast = document.createElement("div");

        toast.className =
            `toast toast-${type}`;

        toast.id = id;

        toast.innerHTML = `

            <div class="toast-icon">

                ${this.getIcon(type)}

            </div>

            <div class="toast-content">

                <div class="toast-title">

                    ${title}

                </div>

                <div class="toast-message">

                    ${message}

                </div>

            </div>

            <button
                class="toast-close"
                aria-label="Close"
            >

                ×

            </button>

        `;

        this.container.appendChild(toast);

        requestAnimationFrame(() => {

            toast.classList.add("show");

        });

        toast
            .querySelector(".toast-close")
            .addEventListener(

                "click",

                () => this.remove(id)

            );

        if (duration > 0) {

            setTimeout(() => {

                this.remove(id);

            }, duration);

        }

    }

    /*
    ==========================================================
    Remove
    ==========================================================
    */

    remove(id) {

        const toast = document.getElementById(id);

        if (!toast) {

            return;

        }

        toast.classList.remove("show");

        toast.classList.add("hide");

        setTimeout(() => {

            toast.remove();

        }, 250);

    }

    /*
    ==========================================================
    Remove All
    ==========================================================
    */

    clear() {

        if (!this.container) {

            return;

        }

        this.container.innerHTML = "";

    }

    /*
    ==========================================================
    Helpers
    ==========================================================
    */

    success(title, message, duration) {

        this.show({

            title,

            message,

            type: "success",

            duration

        });

    }

    info(title, message, duration) {

        this.show({

            title,

            message,

            type: "info",

            duration

        });

    }

    warning(title, message, duration) {

        this.show({

            title,

            message,

            type: "warning",

            duration

        });

    }

    error(title, message, duration) {

        this.show({

            title,

            message,

            type: "error",

            duration

        });

    }

    /*
    ==========================================================
    Icons
    ==========================================================
    */

    getIcon(type) {

        switch (type) {

            case "success":

                return "✅";

            case "warning":

                return "⚠️";

            case "error":

                return "❌";

            default:

                return "ℹ️";

        }

    }

}