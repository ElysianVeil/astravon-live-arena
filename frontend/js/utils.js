/*
============================================================
Astravon Live Arena
Utility Functions

Purpose:
    Shared helper functions used throughout
    the frontend dashboard.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

/*
============================================================
DOM Helpers
============================================================
*/

export function $(selector) {

    return document.querySelector(selector);

}

export function $$(selector) {

    return document.querySelectorAll(selector);

}

/*
============================================================
Element
============================================================
*/

export function createElement(

    tag,

    className = "",

    text = ""

) {

    const element =

        document.createElement(tag);

    if (className) {

        element.className = className;

    }

    if (text) {

        element.textContent = text;

    }

    return element;

}

/*
============================================================
Numbers
============================================================
*/

export function clamp(

    value,

    min,

    max

) {

    return Math.min(

        Math.max(value, min),

        max

    );

}

export function round(

    value,

    decimals = 2

) {

    return Number(

        value.toFixed(decimals)

    );

}

export function percentage(

    value,

    total

) {

    if (total <= 0) {

        return 0;

    }

    return round(

        (value / total) * 100,

        1

    );

}

/*
============================================================
Formatting
============================================================
*/

export function formatNumber(number) {

    return new Intl.NumberFormat()

        .format(number);

}

export function formatTemperature(value) {

    return `${round(value)} °C`;

}

export function formatHumidity(value) {

    return `${round(value)} %`;

}

export function formatFPS(value) {

    return `${round(value)} FPS`;

}

export function formatMilliseconds(value) {

    return `${round(value)} ms`;

}

export function formatTime(date = new Date()) {

    return date.toLocaleTimeString();

}

export function formatDate(date = new Date()) {

    return date.toLocaleDateString();

}

export function formatDateTime(date = new Date()) {

    return `${

        formatDate(date)

    } ${

        formatTime(date)

    }`;

}

/*
============================================================
Risk Helpers
============================================================
*/

export function riskColor(score) {

    if (score >= 80) {

        return "danger";

    }

    if (score >= 60) {

        return "warning";

    }

    if (score >= 30) {

        return "moderate";

    }

    return "safe";

}

export function riskLabel(score) {

    if (score >= 80) {

        return "Critical";

    }

    if (score >= 60) {

        return "High";

    }

    if (score >= 30) {

        return "Moderate";

    }

    return "Low";

}

/*
============================================================
Storage
============================================================
*/

export function save(

    key,

    value

) {

    localStorage.setItem(

        key,

        JSON.stringify(value)

    );

}

export function load(

    key,

    defaultValue = null

) {

    const item =

        localStorage.getItem(key);

    if (!item) {

        return defaultValue;

    }

    try {

        return JSON.parse(item);

    }

    catch {

        return defaultValue;

    }

}

export function remove(key) {

    localStorage.removeItem(key);

}

export function clearStorage() {

    localStorage.clear();

}

/*
============================================================
Random
============================================================
*/

export function uuid() {

    return crypto.randomUUID();

}

export function randomInt(

    min,

    max

) {

    return Math.floor(

        Math.random() *

        (max - min + 1)

    ) + min;

}

/*
============================================================
Delay
============================================================
*/

export function sleep(ms) {

    return new Promise(

        resolve =>

            setTimeout(

                resolve,

                ms

            )

    );

}

/*
============================================================
Debounce
============================================================
*/

export function debounce(

    callback,

    delay = 300

) {

    let timeout;

    return (...args) => {

        clearTimeout(timeout);

        timeout = setTimeout(

            () => callback(...args),

            delay

        );

    };

}

/*
============================================================
Throttle
============================================================
*/

export function throttle(

    callback,

    limit = 100

) {

    let waiting = false;

    return (...args) => {

        if (waiting) {

            return;

        }

        callback(...args);

        waiting = true;

        setTimeout(

            () => {

                waiting = false;

            },

            limit

        );

    };

}

/*
============================================================
Validation
============================================================
*/

export function isNumber(value) {

    return !Number.isNaN(

        Number(value)

    );

}

export function isEmpty(value) {

    return (

        value === null ||

        value === undefined ||

        value === ""

    );

}

/*
============================================================
Fullscreen
============================================================
*/

export function enterFullscreen() {

    document.documentElement

        .requestFullscreen?.();

}

export function exitFullscreen() {

    document.exitFullscreen?.();

}

/*
============================================================
Download JSON
============================================================
*/

export function downloadJSON(

    filename,

    data

) {

    const blob =

        new Blob(

            [

                JSON.stringify(

                    data,

                    null,

                    4

                )

            ],

            {

                type: "application/json"

            }

        );

    const url =

        URL.createObjectURL(blob);

    const link =

        document.createElement("a");

    link.href = url;

    link.download = filename;

    link.click();

    URL.revokeObjectURL(url);

}

/*
============================================================
Loading Screen
============================================================
*/

export function showLoading(message = "Loading...") {

    const screen = document.getElementById("loadingScreen");

    if (!screen) return;

    screen.style.display = "flex";

    const text = screen.querySelector("p");

    if (text) {
        text.textContent = message;
    }

}

export function hideLoading() {

    const screen = document.getElementById("loadingScreen");

    if (!screen) return;

    screen.style.opacity = "0";

    setTimeout(() => {

        screen.style.display = "none";

    }, 300);

}

export function setLoading(message) {

    const screen = document.getElementById("loadingScreen");

    if (!screen) return;

    const text = screen.querySelector("p");

    if (text) {
        text.textContent = message;
    }

}

/*
============================================================
Toast Notifications
============================================================
*/

export function showToast(

    message,

    type = "info",

    duration = 3000

) {

    let container = document.getElementById("toastContainer");

    if (!container) {

        container = document.createElement("div");

        container.id = "toastContainer";

        document.body.appendChild(container);

    }

    const toast = document.createElement("div");

    toast.className = `toast ${type}`;

    toast.textContent = message;

    container.appendChild(toast);

    requestAnimationFrame(() => {

        toast.classList.add("show");

    });

    setTimeout(() => {

        toast.classList.remove("show");

        setTimeout(() => {

            toast.remove();

        }, 300);

    }, duration);

}

/*
============================================================
Logger
============================================================
*/

export function log(

    message,

    data = null

) {

    console.log(

        `[Astravon] ${message}`,

        data ?? ""

    );

}

export function warn(

    message,

    data = null

) {

    console.warn(

        `[Astravon] ${message}`,

        data ?? ""

    );

}

export function error(

    message,

    data = null

) {

    console.error(

        `[Astravon] ${message}`,

        data ?? ""

    );

}