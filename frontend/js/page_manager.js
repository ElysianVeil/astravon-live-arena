class PageManager {

    constructor() {

        this.activePage = null;

    }

    async load(name) {

        if (this.activePage?.destroy) {
            await this.activePage.destroy();
        }

        const response =
            await fetch(`./pages/${name}.html`);

        const html =
            await response.text();

        document.getElementById("mainContent").innerHTML =
            html;

        await new Promise(resolve =>
            requestAnimationFrame(resolve)
        );

        await new Promise(resolve =>
            requestAnimationFrame(resolve)
        );

        return name;
    }

}

/*
============================================================
Singleton
============================================================
*/

export const pageManager = new PageManager();

export default pageManager;