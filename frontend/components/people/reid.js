/*
============================================================
Astravon Live Arena
Person Re-Identification Component

Purpose:
    Manages the frontend representation of
    Person Re-Identification (ReID).

Responsibilities:
    • Store identified people
    • Update identities
    • Search identities
    • Render identity cards
    • Emit selection events

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

export default class ReIdentification {

    constructor(container) {

        this.container =
            typeof container === "string"
                ? document.querySelector(container)
                : container;

        this.identities = [];

        this.selectedIdentity = null;

        this.selectCallbacks = [];

    }

    /*
    ==========================================================
        Set Identities
    ==========================================================
    */

    setIdentities(data = []) {

        this.identities = [...data];

        this.render();

        return this;

    }

    /*
    ==========================================================
        Add Identity
    ==========================================================
    */

    add(identity) {

        if (!identity) return;

        this.identities.push(identity);

        this.render();

    }

    /*
    ==========================================================
        Update Identity
    ==========================================================
    */

    update(id, updates = {}) {

        const identity = this.identities.find(

            person => person.id === id

        );

        if (!identity) return;

        Object.assign(identity, updates);

        this.render();

    }

    /*
    ==========================================================
        Remove Identity
    ==========================================================
    */

    remove(id) {

        this.identities = this.identities.filter(

            person => person.id !== id

        );

        this.render();

    }

    /*
    ==========================================================
        Clear
    ==========================================================
    */

    clear() {

        this.identities = [];

        this.render();

    }

    /*
    ==========================================================
        Find
    ==========================================================
    */

    find(id) {

        return this.identities.find(

            person => person.id === id

        );

    }

    /*
    ==========================================================
        Search
    ==========================================================
    */

    search(keyword = "") {

        keyword = keyword.toLowerCase();

        return this.identities.filter(identity =>

            identity.name?.toLowerCase().includes(keyword) ||

            identity.id?.toLowerCase().includes(keyword)

        );

    }

    /*
    ==========================================================
        Register Selection Listener
    ==========================================================
    */

    onSelect(callback) {

        if (typeof callback === "function") {

            this.selectCallbacks.push(callback);

        }

    }

    /*
    ==========================================================
        Render
    ==========================================================
    */

    render() {

        if (!this.container) return;

        this.container.innerHTML = "";

        if (this.identities.length === 0) {

            this.container.innerHTML =

                `
                <div class="empty-state">

                    <h3>No Identified People</h3>

                    <p>
                        Waiting for AI detections...
                    </p>

                </div>
                `;

            return;

        }

        this.identities.forEach(identity => {

            this.container.appendChild(

                this.#createCard(identity)

            );

        });

    }

    /*
    ==========================================================
        Identity Card
    ==========================================================
    */

    #createCard(identity) {

        const card = document.createElement("div");

        card.className = "identity-card";

        card.dataset.id = identity.id;

        card.innerHTML = `

            <div class="identity-image">

                <img
                    src="${identity.image || "assets/images/avatar.png"}"
                    alt="${identity.name || "Unknown"}"
                >

            </div>

            <div class="identity-information">

                <h3>

                    ${identity.name || "Unknown"}

                </h3>

                <p>

                    ID:
                    ${identity.id}

                </p>

                <p>

                    Confidence:
                    ${identity.confidence ?? "--"}%

                </p>

                <p>

                    Camera:
                    ${identity.camera || "--"}

                </p>

                <p>

                    Last Seen:
                    ${identity.lastSeen || "--"}

                </p>

            </div>

        `;

        card.addEventListener(

            "click",

            () => this.#select(identity)

        );

        return card;

    }

    /*
    ==========================================================
        Select Identity
    ==========================================================
    */

    #select(identity) {

        this.selectedIdentity = identity;

        this.selectCallbacks.forEach(callback =>

            callback(identity)

        );

    }

    /*
    ==========================================================
        Get Selected
    ==========================================================
    */

    getSelected() {

        return this.selectedIdentity;

    }

}