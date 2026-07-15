/*
============================================================
Astravon Live Arena
Sidebar Component

Purpose:
    Creates and manages the dashboard sidebar
    navigation.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

export default class Sidebar {

    constructor() {

        this.container = null;

        this.activePage = "dashboard";

        this.items = [

            {
                id: "dashboard",
                icon: "🏠",
                label: "Dashboard",
                page: "dashboard.html"
            },

            {
                id: "reports",
                icon: "📊",
                label: "Reports",
                page: "reports.html"
            },

            {
                id: "settings",
                icon: "⚙️",
                label: "Settings",
                page: "settings.html"
            },

            {
                id: "about",
                icon: "ℹ️",
                label: "About",
                page: "about.html"
            }

        ];

    }

    /*
    ==========================================================
    Initialize
    ==========================================================
    */

    initialize() {

        this.container = document.getElementById(
            "sidebar"
        );

        if (!this.container) {

            console.warn(
                "[Sidebar] Container not found."
            );

            return;

        }

        this.render();

        console.log(
            "[Sidebar] Initialized."
        );

    }

    /*
    ==========================================================
    Render
    ==========================================================
    */

    render() {

        let html = `

            <div class="sidebar-header">

                <div class="sidebar-logo">

                    🌌

                </div>

                <h2>

                    Live Arena

                </h2>

            </div>

            <nav class="sidebar-menu">

        `;

        this.items.forEach(item => {

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

            </nav>

            <div class="sidebar-footer">

                <div class="system-status">

                    <span class="status-dot"></span>

                    System Ready

                </div>

            </div>

        `;

        this.container.innerHTML = html;

        this.attachEvents();

    }

    /*
    ==========================================================
    Events
    ==========================================================
    */

    attachEvents() {

        const buttons =

            this.container.querySelectorAll(
                ".sidebar-item"
            );

        buttons.forEach(button => {

            button.addEventListener(

                "click",

                async () => {

                    const page =

                        button.dataset.page;

                    await this.navigate(page);

                }

            );

        });

    }

    /*
    ==========================================================
    Navigation
    ==========================================================
    */

    async navigate(page) {
        if (page === this.activePage) {

            return;

        }

        this.activePage = page;

        this.highlight(page);

        // const selected =

        //     this.items.find(

        //         item => item.id === page

        //     );

        // if (!selected) {

        //     return;

        // }

        // console.log(

        //     `[Sidebar] ${selected.label}`

        // );

        /*
        ------------------------------------------------------
        Future SPA Router
        ------------------------------------------------------

        When the frontend becomes a full
        single-page application, replace
        the redirect below with router logic.

        */

        window.Astravon.loadPage(page);

    }

    /*
    ==========================================================
    Highlight Active Item
    ==========================================================
    */

    highlight(page) {

        this.container

            .querySelectorAll(".sidebar-item")

            .forEach(item => {

                item.classList.remove(

                    "active"

                );

            });

        const active =

            this.container.querySelector(

                `[data-page="${page}"]`

            );

        if (active) {

            active.classList.add(

                "active"

            );

        }

    }

    /*
    ==========================================================
    Set Active
    ==========================================================
    */

    setActive(page) {

        this.activePage = page;

        this.highlight(page);

    }

    /*
    ==========================================================
    Enable Item
    ==========================================================
    */

    enable(page) {

        const button =

            this.container.querySelector(

                `[data-page="${page}"]`

            );

        if (button) {

            button.disabled = false;

        }

    }

    /*
    ==========================================================
    Disable Item
    ==========================================================
    */

    disable(page) {

        const button =

            this.container.querySelector(

                `[data-page="${page}"]`

            );

        if (button) {

            button.disabled = true;

        }

    }

    /*
    ==========================================================
    Update Status
    ==========================================================
    */

    setStatus(message) {

        const status =

            this.container.querySelector(
                ".system-status"
            );

        if (status) {

            status.innerHTML = `

                <span class="status-dot"></span>

                ${message}

            `;

        }

    }

}