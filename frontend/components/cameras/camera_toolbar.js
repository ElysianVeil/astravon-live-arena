/*
============================================================
Astravon Live Arena
Camera Toolbar Component

Purpose:
    Controls the camera toolbar and dispatches
    camera management actions.

Author:
    House of Astravon
Version:
    2.0.0
============================================================
*/

export default class CameraToolbar {

    constructor(options = {}) {

        this.options = {

            connectAllBtn: "connectAllBtn",

            disconnectAllBtn: "disconnectAllBtn",

            refreshBtn: "refreshCamerasBtn",

            fullscreenBtn: "fullscreenGridBtn",

            gridToggleBtn: "toggleGridBtn",

            layoutBtn: "layoutBtn",

            columnsSelect: "cameraColumns",

            snapshotBtn: "snapshotBtn",

            recordBtn: "recordBtn",

            ...options

        };

        this.handlers = {

            connectAll: null,

            disconnectAll: null,

            refresh: null,

            fullscreen: null,

            toggleGrid: null,

            changeLayout: null,

            changeColumns: null,

            snapshot: null,

            record: null

        };

    }

    /*==========================================================
        Initialize
    ==========================================================*/

    initialize() {

        this.connectAllButton =
            document.getElementById(this.options.connectAllBtn);

        this.disconnectAllButton =
            document.getElementById(this.options.disconnectAllBtn);

        this.refreshButton =
            document.getElementById(this.options.refreshBtn);

        this.fullscreenButton =
            document.getElementById(this.options.fullscreenBtn);

        this.gridToggleButton =
            document.getElementById(this.options.gridToggleBtn);

        this.layoutButton =
            document.getElementById(this.options.layoutBtn);

        this.columnsSelect =
            document.getElementById(this.options.columnsSelect);

        this.snapshotButton =
            document.getElementById(this.options.snapshotBtn);

        this.recordButton =
            document.getElementById(this.options.recordBtn);

        this.registerEvents();

    }

    /*==========================================================
        Event Registration
    ==========================================================*/

    registerEvents() {

        this.connectAllButton?.addEventListener(

            "click",

            () => this.handlers.connectAll?.()

        );

        this.disconnectAllButton?.addEventListener(

            "click",

            () => this.handlers.disconnectAll?.()

        );

        this.refreshButton?.addEventListener(

            "click",

            () => this.handlers.refresh?.()

        );

        this.fullscreenButton?.addEventListener(

            "click",

            () => this.handlers.fullscreen?.()

        );

        this.gridToggleButton?.addEventListener(

            "click",

            () => this.handlers.toggleGrid?.()

        );

        this.layoutButton?.addEventListener(

            "click",

            () => this.handlers.changeLayout?.()

        );

        this.columnsSelect?.addEventListener(

            "change",

            event => {

                this.handlers.changeColumns?.(

                    Number(event.target.value)

                );

            }

        );

        this.snapshotButton?.addEventListener(

            "click",

            () => this.handlers.snapshot?.()

        );

        this.recordButton?.addEventListener(

            "click",

            () => this.handlers.record?.()

        );

    }

    /*==========================================================
        Callback Registration
    ==========================================================*/

    onConnectAll(callback) {

        this.handlers.connectAll = callback;

    }

    onDisconnectAll(callback) {

        this.handlers.disconnectAll = callback;

    }

    onRefresh(callback) {

        this.handlers.refresh = callback;

    }

    onFullscreen(callback) {

        this.handlers.fullscreen = callback;

    }

    onToggleGrid(callback) {

        this.handlers.toggleGrid = callback;

    }

    onChangeLayout(callback) {

        this.handlers.changeLayout = callback;

    }

    onChangeColumns(callback) {

        this.handlers.changeColumns = callback;

    }

    onSnapshot(callback) {

        this.handlers.snapshot = callback;

    }

    onRecord(callback) {

        this.handlers.record = callback;

    }

    /*==========================================================
        Button State
    ==========================================================*/

    enableAll() {

        this.setDisabled(false);

    }

    disableAll() {

        this.setDisabled(true);

    }

    setDisabled(state = false) {

        [

            this.connectAllButton,

            this.disconnectAllButton,

            this.refreshButton,

            this.fullscreenButton,

            this.gridToggleButton,

            this.layoutButton,

            this.columnsSelect,

            this.snapshotButton,

            this.recordButton

        ].forEach(control => {

            if (control) {

                control.disabled = state;

            }

        });

    }

    /*==========================================================
        Loading
    ==========================================================*/

    showLoading() {

        if (!this.refreshButton) return;

        this.refreshButton.disabled = true;

        this.refreshButton.dataset.originalText =
            this.refreshButton.textContent;

        this.refreshButton.textContent =
            "Refreshing...";

    }

    hideLoading() {

        if (!this.refreshButton) return;

        this.refreshButton.disabled = false;

        this.refreshButton.textContent =
            this.refreshButton.dataset.originalText ||
            "Refresh";

    }

    /*==========================================================
        Recording State
    ==========================================================*/

    setRecording(recording) {

        if (!this.recordButton) return;

        this.recordButton.classList.toggle(

            "recording",

            recording

        );

        this.recordButton.textContent =

            recording

                ? "Stop Recording"

                : "Record";

    }

    /*==========================================================
        Grid Layout Helpers
    ==========================================================*/

    setColumns(columns) {

        if (!this.columnsSelect) return;

        this.columnsSelect.value = columns;

    }

}