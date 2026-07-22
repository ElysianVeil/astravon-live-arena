/*
============================================================
Astravon Live Arena
Utility Functions

Purpose:
    Shared utility library used throughout
    the Astravon Live Arena frontend.

Part:
    1 — DOM, Elements, Math,
        Formatting, Dates,
        Objects, Arrays

Author:
    House of Astravon

Version:
    2.0.0
============================================================
*/

/*==========================================================
    DOM Helpers
==========================================================*/

export function $(selector, parent = document) {

    return parent.querySelector(selector);

}

export function $$(selector, parent = document) {

    return [...parent.querySelectorAll(selector)];

}

export function byId(id) {

    return document.getElementById(id);

}

export function exists(selector, parent = document) {

    return parent.querySelector(selector) !== null;

}

export function ready(callback) {

    if (

        document.readyState === "loading"

    ) {

        document.addEventListener(

            "DOMContentLoaded",

            callback

        );

    }

    else {

        callback();

    }

}

/*==========================================================
    Element Helpers
==========================================================*/

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

    if (text !== "") {

        element.textContent = text;

    }

    return element;

}

export function clearElement(element) {

    if (!element) return;

    element.innerHTML = "";

}

export function removeElement(element) {

    if (!element) return;

    element.remove();

}

export function show(element) {

    if (!element) return;

    element.style.display = "";

}

export function hide(element) {

    if (!element) return;

    element.style.display = "none";

}

export function toggle(

    element,

    visible = true

) {

    if (!element) return;

    element.style.display =

        visible

            ? ""

            : "none";

}

export function addClass(

    element,

    className

) {

    element?.classList.add(className);

}

export function removeClass(

    element,

    className

) {

    element?.classList.remove(className);

}

export function toggleClass(

    element,

    className

) {

    element?.classList.toggle(className);

}

/*==========================================================
    Number Helpers
==========================================================*/

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

        Number(value).toFixed(decimals)

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

export function lerp(

    start,

    end,

    alpha

) {

    return start +

        (end - start) * alpha;

}

export function mapRange(

    value,

    inMin,

    inMax,

    outMin,

    outMax

) {

    return (

        (

            value - inMin

        ) *

        (

            outMax - outMin

        ) /

        (

            inMax - inMin

        )

    ) + outMin;

}

/*==========================================================
    Formatting
==========================================================*/

export function formatNumber(value) {

    return new Intl.NumberFormat()

        .format(value);

}

export function formatMetric(

    value,

    unit,

    decimals = 1

) {

    return `${

        round(value, decimals)

    } ${unit}`;

}

export function formatTemperature(value) {

    return formatMetric(

        value,

        "°C"

    );

}

export function formatHumidity(value) {

    return formatMetric(

        value,

        "%"

    );

}

export function formatFPS(value) {

    return formatMetric(

        value,

        "FPS"

    );

}

export function formatMilliseconds(value) {

    return formatMetric(

        value,

        "ms"

    );

}

export function formatPercentage(value) {

    return `${

        round(value, 1)

    }%`;

}

/*==========================================================
    Date & Time
==========================================================*/

export function now() {

    return Date.now();

}

export function timestamp() {

    return new Date()

        .toISOString();

}

export function formatTime(

    date = new Date()

) {

    return date.toLocaleTimeString();

}

export function formatDate(

    date = new Date()

) {

    return date.toLocaleDateString();

}

export function formatDateTime(

    date = new Date()

) {

    return `${

        formatDate(date)

    } ${

        formatTime(date)

    }`;

}

/*==========================================================
    Object Helpers
==========================================================*/

export function deepClone(object) {

    return structuredClone(object);

}

export function merge(

    target,

    source

) {

    return Object.assign(

        {},

        target,

        source

    );

}

export function freeze(object) {

    return Object.freeze(object);

}

export function deepFreeze(object) {

    Object.freeze(object);

    Object.keys(object).forEach(key => {

        const value = object[key];

        if (

            value &&

            typeof value === "object" &&

            !Object.isFrozen(value)

        ) {

            deepFreeze(value);

        }

    });

    return object;

}

/*==========================================================
    Array Helpers
==========================================================*/

export function unique(array) {

    return [

        ...new Set(array)

    ];

}

export function chunk(

    array,

    size

) {

    const result = [];

    for (

        let i = 0;

        i < array.length;

        i += size

    ) {

        result.push(

            array.slice(

                i,

                i + size

            )

        );

    }

    return result;

}

export function last(array) {

    return array[

        array.length - 1

    ];

}

export function first(array) {

    return array[0];

}

export function shuffle(array) {

    return [

        ...array

    ].sort(

        () =>

            Math.random() - 0.5

    );

}

/*==========================================================
    Validation
==========================================================*/

export function isNumber(value) {

    return !Number.isNaN(Number(value));

}

export function isInteger(value) {

    return Number.isInteger(Number(value));

}

export function isString(value) {

    return typeof value === "string";

}

export function isBoolean(value) {

    return typeof value === "boolean";

}

export function isObject(value) {

    return (

        value !== null &&

        typeof value === "object" &&

        !Array.isArray(value)

    );

}

export function isArray(value) {

    return Array.isArray(value);

}

export function isFunction(value) {

    return typeof value === "function";

}

export function isEmpty(value) {

    return (

        value === null ||

        value === undefined ||

        value === "" ||

        (Array.isArray(value) && value.length === 0)

    );

}

export function hasValue(value) {

    return !isEmpty(value);

}

export function between(

    value,

    min,

    max

) {

    return value >= min && value <= max;

}

export function validateRange(

    value,

    min,

    max

) {

    if (!isNumber(value)) return false;

    return between(

        Number(value),

        min,

        max

    );

}

/*==========================================================
    Storage
==========================================================*/

export const Storage = {

    save(

        key,

        value

    ) {

        localStorage.setItem(

            key,

            JSON.stringify(value)

        );

    },

    load(

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

    },

    remove(key) {

        localStorage.removeItem(key);

    },

    clear() {

        localStorage.clear();

    },

    exists(key) {

        return (

            localStorage.getItem(key)

            !== null

        );

    }

};

/*==========================================================
    Browser Helpers
==========================================================*/

export function reload() {

    window.location.reload();

}

export function redirect(url) {

    window.location.href = url;

}

export function openWindow(

    url,

    target = "_blank"

) {

    window.open(

        url,

        target

    );

}

export function currentURL() {

    return window.location.href;

}

export function userAgent() {

    return navigator.userAgent;

}

export function online() {

    return navigator.onLine;

}

/*==========================================================
    Network
==========================================================*/

export async function fetchJSON(

    url,

    options = {}

) {

    const response =

        await fetch(

            url,

            options

        );

    if (!response.ok) {

        throw new Error(

            response.statusText

        );

    }

    return response.json();

}

export async function fetchText(

    url,

    options = {}

) {

    const response =

        await fetch(

            url,

            options

        );

    if (!response.ok) {

        throw new Error(

            response.statusText

        );

    }

    return response.text();

}

export async function ping(url) {

    try {

        await fetch(

            url,

            {

                method: "HEAD"

            }

        );

        return true;

    }

    catch {

        return false;

    }

}

/*==========================================================
    Async Helpers
==========================================================*/

export function sleep(ms) {

    return new Promise(

        resolve =>

            setTimeout(

                resolve,

                ms

            )

    );

}

export async function retry(

    callback,

    retries = 3

) {

    for (

        let i = 0;

        i < retries;

        i++

    ) {

        try {

            return await callback();

        }

        catch (error) {

            if (

                i === retries - 1

            ) {

                throw error;

            }

        }

    }

}

export function timeout(

    promise,

    ms

) {

    return Promise.race([

        promise,

        new Promise(

            (_, reject) =>

                setTimeout(

                    () =>

                        reject(

                            new Error(

                                "Timeout"

                            )

                        ),

                    ms

                )

        )

    ]);

}

/*==========================================================
    Performance
==========================================================*/

export function debounce(

    callback,

    delay = 300

) {

    let timeout;

    return (...args) => {

        clearTimeout(timeout);

        timeout = setTimeout(

            () =>

                callback(...args),

            delay

        );

    };

}

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

export function measure(

    name,

    callback

) {

    const start =

        performance.now();

    const result =

        callback();

    const end =

        performance.now();

    console.log(

        `${name}: ${

            round(

                end - start,

                2

            )

        } ms`

    );

    return result;

}

export function nextFrame() {

    return new Promise(

        resolve =>

            requestAnimationFrame(resolve)

    );

}

export function idle(callback) {

    if (

        "requestIdleCallback"

        in window

    ) {

        requestIdleCallback(

            callback

        );

    }

    else {

        setTimeout(

            callback,

            1

        );

    }

}

/*
============================================================
Camera Helpers
============================================================
*/

/*
------------------------------------------------------------
Convert Base64 Frame
------------------------------------------------------------
*/

export function frameToDataURL(frame) {

    if (!frame) {

        return "";

    }

    return `data:image/jpeg;base64,${frame}`;

}

/*
------------------------------------------------------------
Frame Exists
------------------------------------------------------------
*/

export function hasFrame(frame) {

    return (

        typeof frame === "string" &&

        frame.length > 50

    );

}

/*
------------------------------------------------------------
Camera Online
------------------------------------------------------------
*/

export function isCameraOnline(camera) {

    if (!camera) {

        return false;

    }

    return (

        camera.online === true ||

        camera.connected === true

    );

}

/*
------------------------------------------------------------
Camera Badge
------------------------------------------------------------
*/

export function cameraStatusClass(camera) {

    if (!camera) {

        return "offline";

    }

    if (camera.recording) {

        return "recording";

    }

    return isCameraOnline(camera)

        ? "online"

        : "offline";

}

/*
------------------------------------------------------------
FPS Color
------------------------------------------------------------
*/

export function fpsColor(fps) {

    if (fps >= 25) return "success";

    if (fps >= 15) return "warning";

    return "danger";

}

/*
------------------------------------------------------------
Resolution String
------------------------------------------------------------
*/

export function resolution(width, height) {

    return `${width} × ${height}`;

}

/*
============================================================
Statistics Helpers
============================================================
*/

/*
------------------------------------------------------------
Occupancy Percentage
------------------------------------------------------------
*/

export function occupancyPercentage(

    people,

    capacity

) {

    if (!capacity) {

        return 0;

    }

    return round(

        (people / capacity) * 100,

        1

    );

}

/*
------------------------------------------------------------
Density Label
------------------------------------------------------------
*/

export function densityLabel(value) {

    if (value >= 8) {

        return "Critical";

    }

    if (value >= 6) {

        return "High";

    }

    if (value >= 4) {

        return "Medium";

    }

    return "Low";

}

/*
------------------------------------------------------------
Density Color
------------------------------------------------------------
*/

export function densityColor(value) {

    if (value >= 8) return "danger";

    if (value >= 6) return "warning";

    if (value >= 4) return "moderate";

    return "safe";

}

/*
------------------------------------------------------------
Heat Index Label
------------------------------------------------------------
*/

export function heatLabel(value) {

    if (value >= 41) return "Extreme";

    if (value >= 33) return "Danger";

    if (value >= 27) return "Warm";

    return "Comfortable";

}

/*
------------------------------------------------------------
Heat Color
------------------------------------------------------------
*/

export function heatColor(value) {

    if (value >= 41) return "danger";

    if (value >= 33) return "warning";

    if (value >= 27) return "moderate";

    return "safe";

}

/*
============================================================
Risk Helpers
============================================================
*/

/*
------------------------------------------------------------
Risk Class
------------------------------------------------------------
*/

export function riskClass(level) {

    switch (

        String(level).toLowerCase()

    ) {

        case "critical":

            return "danger";

        case "high":

            return "danger";

        case "medium":

            return "warning";

        case "moderate":

            return "moderate";

        case "low":

            return "safe";

        default:

            return "secondary";

    }

}

/*
------------------------------------------------------------
Risk Icon
------------------------------------------------------------
*/

export function riskIcon(level) {

    switch (

        String(level).toLowerCase()

    ) {

        case "critical":

            return "🛑";

        case "high":

            return "🚨";

        case "medium":

            return "⚠️";

        case "low":

            return "✅";

        default:

            return "ℹ️";

    }

}

/*
------------------------------------------------------------
Risk Message
------------------------------------------------------------
*/

export function riskMessage(score) {

    if (score >= 90)

        return "Immediate evacuation required.";

    if (score >= 75)

        return "Emergency teams should respond.";

    if (score >= 50)

        return "Monitor crowd closely.";

    return "Situation stable.";

}

/*
============================================================
Fullscreen Helpers
============================================================
*/

/*
------------------------------------------------------------
Toggle Element
------------------------------------------------------------
*/

export async function toggleFullscreen(element) {

    if (!element) {

        return;

    }

    if (document.fullscreenElement) {

        await document.exitFullscreen();

    }

    else {

        await element.requestFullscreen();

    }

}

/*
------------------------------------------------------------
Fullscreen State
------------------------------------------------------------
*/

export function isFullscreen() {

    return !!document.fullscreenElement;

}

/*
============================================================
Downloads
============================================================
*/

/*
------------------------------------------------------------
Download Text
------------------------------------------------------------
*/

export function downloadText(

    filename,

    text

) {

    const blob =

        new Blob(

            [text],

            {

                type: "text/plain"

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
------------------------------------------------------------
Download CSV
------------------------------------------------------------
*/

export function downloadCSV(

    filename,

    rows = []

) {

    const csv = rows

        .map(

            row => row.join(",")

        )

        .join("\n");

    downloadText(

        filename,

        csv

    );

}

/*
------------------------------------------------------------
Download Image
------------------------------------------------------------
*/

export function downloadImage(

    filename,

    imageURL

) {

    const link =

        document.createElement("a");

    link.href = imageURL;

    link.download = filename;

    link.click();

}

/*
============================================================
Loading Manager
============================================================
*/

class LoadingManager {

    constructor() {

        this.screen = null;

        this.messageElement = null;

        this.visible = false;

    }

    initialize() {

        this.screen = document.getElementById(
            "loadingScreen"
        );

        if (!this.screen) return;

        this.messageElement =
            this.screen.querySelector("p");

    }

    show(message = "Loading...") {

        if (!this.screen) {

            this.initialize();

        }

        if (!this.screen) return;

        this.visible = true;

        this.screen.style.display = "flex";

        this.screen.style.opacity = "1";

        this.setMessage(message);

    }

    hide() {

        if (!this.screen) return;

        this.visible = false;

        this.screen.style.opacity = "0";

        setTimeout(() => {

            if (!this.visible) {

                this.screen.style.display = "none";

            }

        }, 300);

    }

    setMessage(message) {

        if (this.messageElement) {

            this.messageElement.textContent =

                message;

        }

    }

}

export const Loading = new LoadingManager();


/*
============================================================
Toast Manager
============================================================
*/

class ToastManager {

    constructor() {

        this.container = null;

    }

    initialize() {

        this.container = document.getElementById(

            "toastContainer"

        );

        if (!this.container) {

            this.container =

                document.createElement("div");

            this.container.id =

                "toastContainer";

            document.body.appendChild(

                this.container

            );

        }

    }

    show(

        message,

        type = "info",

        duration = 3000

    ) {

        if (!this.container) {

            this.initialize();

        }

        const toast =

            document.createElement("div");

        toast.className =

            `toast ${type}`;

        toast.textContent =

            message;

        this.container.appendChild(

            toast

        );

        requestAnimationFrame(() => {

            toast.classList.add(

                "show"

            );

        });

        setTimeout(() => {

            toast.classList.remove(

                "show"

            );

            setTimeout(() => {

                toast.remove();

            }, 300);

        }, duration);

    }

    success(message) {

        this.show(

            message,

            "success"

        );

    }

    info(message) {

        this.show(

            message,

            "info"

        );

    }

    warning(message) {

        this.show(

            message,

            "warning"

        );

    }

    error(message) {

        this.show(

            message,

            "danger"

        );

    }

}

export const Toast = new ToastManager();


/*
============================================================
Logger
============================================================
*/

class Logger {

    constructor(prefix = "Astravon") {

        this.prefix = prefix;

    }

    info(message, data = null) {

        console.info(

            `[${this.prefix}] ${message}`,

            data ?? ""

        );

    }

    log(message, data = null) {

        console.log(

            `[${this.prefix}] ${message}`,

            data ?? ""

        );

    }

    warn(message, data = null) {

        console.warn(

            `[${this.prefix}] ${message}`,

            data ?? ""

        );

    }

    error(message, data = null) {

        console.error(

            `[${this.prefix}] ${message}`,

            data ?? ""

        );

    }

    table(data) {

        console.table(data);

    }

    group(title) {

        console.group(

            `[${this.prefix}] ${title}`

        );

    }

    groupEnd() {

        console.groupEnd();

    }

}

export const logger =

    new Logger();


/*
============================================================
Color Helpers
============================================================
*/

export function hexToRGB(hex) {

    hex =

        hex.replace("#", "");

    const bigint =

        parseInt(hex, 16);

    return {

        r: (bigint >> 16) & 255,

        g: (bigint >> 8) & 255,

        b: bigint & 255

    };

}

export function rgbToHex(

    r,

    g,

    b

) {

    return "#" +

        [r, g, b]

            .map(

                value =>

                    value

                        .toString(16)

                        .padStart(2, "0")

            )

            .join("");

}

export function randomColor() {

    return rgbToHex(

        randomInt(0,255),

        randomInt(0,255),

        randomInt(0,255)

    );

}


/*
============================================================
Miscellaneous
============================================================
*/

export function noop(){}

export function identity(value){

    return value;

}

export function capitalize(text){

    if(!text) return "";

    return

        text.charAt(0)

        .toUpperCase()

        +

        text.slice(1);

}

export function titleCase(text){

    return String(text)

        .split(" ")

        .map(capitalize)

        .join(" ");

}

export function copy(text){

    navigator.clipboard?.writeText(

        text

    );

}

export function uid(prefix="id"){

    return `${prefix}_${Date.now()}_${randomInt(1000,9999)}`;

}

export function once(fn){

    let called = false;

    return (...args)=>{

        if(called) return;

        called = true;

        return fn(...args);

    };

}


/*
============================================================
Backward Compatibility
============================================================
*/

export const showLoading =

    (...args)=>

        Loading.show(...args);

export const hideLoading =

    (...args)=>

        Loading.hide(...args);

export const setLoading =

    (...args)=>

        Loading.setMessage(...args);

export const showToast =

    (...args)=>

        Toast.show(...args);

export const log =

    (...args)=>

        logger.log(...args);

export const warn =

    (...args)=>

        logger.warn(...args);

export const error =

    (...args)=>

        logger.error(...args);


/*
============================================================
Initialize Utilities
============================================================
*/

export function initializeUtilities(){

    Loading.initialize();

    Toast.initialize();

}


/*
============================================================
Default Export
============================================================
*/

export default {

    Loading,

    Toast,

    logger,

    initializeUtilities

};