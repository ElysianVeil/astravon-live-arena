/*
============================================================
Astravon Live Arena
Sidebar Component

Purpose:
    Command Center Navigation

Author:
    House of Astravon

Version:
    2.0.0
============================================================
*/

export default class Sidebar {

    constructor() {

        this.container = null;

        this.activePage = "dashboard";

        this.sections = [

            {
                title: "Monitoring",

                items: [

                    {
                        id: "dashboard",
                        icon: "🏠",
                        label: "Dashboard"
                    },

                    {
                        id: "cameras",
                        icon: "📹",
                        label: "Cameras"
                    },

                    {
                        id: "analytics",
                        icon: "📈",
                        label: "Analytics"
                    },

                    {
                        id: "map",
                        icon: "🗺️",
                        label: "Maps"
                    }

                ]

            },

            {
                title: "Management",

                items: [

                    {
                        id: "alerts",
                        icon: "🚨",
                        label: "Alerts"
                    },

                    {
                        id: "reports",
                        icon: "📋",
                        label: "Reports"
                    }

                ]

            },

            {
                title: "System",

                items: [

                    {
                        id: "settings",
                        icon: "⚙️",
                        label: "Settings"
                    },

                    {
                        id: "about",
                        icon: "ℹ️",
                        label: "About"
                    }

                ]

            }

        ];

    }

    /*====================================================*/

    initialize() {

        this.container =
            document.getElementById("sidebar");

        if (!this.container) {

            console.warn("[Sidebar] Missing container.");

            return;

        }

        this.render();

        this.attachEvents();

    }

    /*====================================================*/

    render() {

        let html = `

            <div class="sidebar-header">

                <div class="sidebar-logo">

                    🌌

                </div>

                <div>

                    <h2>

                        Astravon

                    </h2>

                    <small>

                        Live Arena

                    </small>

                </div>

            </div>

        `;

        this.sections.forEach(section => {

            html += `

                <div class="sidebar-section">

                    <div class="sidebar-section-title">

                        ${section.title}

                    </div>

            `;

            section.items.forEach(item => {

                html += `

                    <button

                        class="sidebar-item ${item.id === this.activePage ? "active" : ""}"

                        data-page="${item.id}"

                    >

                        <span class="sidebar-icon">

                            ${item.icon}

                        </span>

                        <span class="sidebar-label">

                            ${item.label}

                        </span>

                    </button>

                `;

            });

            html += `

                </div>

            `;

        });

        html += `

            <div class="sidebar-footer">

                <div class="system-status">

                    <span class="status-dot"></span>

                    AI Engine Ready

                </div>

            </div>

        `;

        this.container.innerHTML = html;

    }

    /*====================================================*/

    attachEvents() {

        this.container

            .querySelectorAll(".sidebar-item")

            .forEach(button => {

                button.addEventListener(

                    "click",

                    () => {

                        this.navigate(

                            button.dataset.page

                        );

                    }

                );

            });

    }

    /*====================================================*/

    navigate(page) {

        if (page === this.activePage) {

            return;

        }

        this.activePage = page;

        this.highlight(page);

        if (

            window.Astravon &&
            typeof window.Astravon.loadPage === "function"

        ) {

            window.Astravon.loadPage(page);

        }

    }

    /*====================================================*/

    highlight(page) {

        this.container

            .querySelectorAll(".sidebar-item")

            .forEach(button =>

                button.classList.remove("active")

            );

        const active =

            this.container.querySelector(

                `[data-page="${page}"]`

            );

        if (active) {

            active.classList.add("active");

        }

    }

    /*====================================================*/

    setActive(page) {

        this.activePage = page;

        this.highlight(page);

    }

    /*====================================================*/

    enable(page) {

        const item =

            this.container.querySelector(

                `[data-page="${page}"]`

            );

        if (item) {

            item.disabled = false;

        }

    }

    /*====================================================*/

    disable(page) {

        const item =

            this.container.querySelector(

                `[data-page="${page}"]`

            );

        if (item) {

            item.disabled = true;

        }

    }

    /*====================================================*/

    setStatus(message) {

        const status =

            this.container.querySelector(

                ".system-status"

            );

        if (!status) return;

        status.innerHTML = `

            <span class="status-dot"></span>

            ${message}

        `;

    }

}