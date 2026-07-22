/*
============================================================
Astravon Live Arena
Identities Component

Purpose:
    Manages identified persons detected by the
    Person Re-Identification (ReID) engine.

Responsibilities:
    • Store known identities
    • Update identity information
    • Search identities
    • Render identity cards
    • Filter identities
    • Remove inactive identities

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

class IdentityManager {

    constructor() {

        this.identities = new Map();

        this.lastUpdated = null;

    }

    /*==========================================================
        Identity Management
    ==========================================================*/

    add(identity = {}) {

        if (!identity.id) {

            return;

        }

        this.identities.set(identity.id, {

            id: identity.id,

            name: identity.name ?? "Unknown",

            confidence: identity.confidence ?? 0,

            camera: identity.camera ?? "Unknown",

            lastSeen: identity.lastSeen ?? "--",

            firstSeen: identity.firstSeen ?? "--",

            status: identity.status ?? "Active",

            visits: identity.visits ?? 1,

            image: identity.image ?? "",

            notes: identity.notes ?? ""

        });

        this.lastUpdated = new Date();

    }

    update(identity = {}) {

        if (!identity.id) {

            return;

        }

        const existing = this.identities.get(identity.id);

        if (!existing) {

            this.add(identity);

            return;

        }

        this.identities.set(identity.id, {

            ...existing,

            ...identity

        });

        this.lastUpdated = new Date();

    }

    remove(id) {

        this.identities.delete(id);

    }

    clear() {

        this.identities.clear();

    }

    /*==========================================================
        Retrieval
    ==========================================================*/

    get(id) {

        return this.identities.get(id) ?? null;

    }

    getAll() {

        return [...this.identities.values()];

    }

    count() {

        return this.identities.size;

    }

    /*==========================================================
        Search
    ==========================================================*/

    search(query = "") {

        query = query.toLowerCase();

        return this.getAll().filter(identity =>

            identity.name.toLowerCase().includes(query) ||

            identity.id.toLowerCase().includes(query)

        );

    }

    filterByStatus(status) {

        return this.getAll().filter(identity =>

            identity.status === status

        );

    }

    /*==========================================================
        Statistics
    ==========================================================*/

    getAverageConfidence() {

        if (!this.identities.size) {

            return 0;

        }

        const total = this.getAll().reduce((sum, identity) => {

            return sum + identity.confidence;

        }, 0);

        return total / this.identities.size;

    }

    /*==========================================================
        Rendering
    ==========================================================*/

    render(container) {

        if (!container) {

            return;

        }

        container.innerHTML = "";

        if (!this.identities.size) {

            container.innerHTML = `

                <div class="empty-state">

                    <h3>No Identified Persons</h3>

                    <p>

                        Waiting for ReID detections...

                    </p>

                </div>

            `;

            return;

        }

        this.getAll().forEach(identity => {

            const card = document.createElement("div");

            card.className = "identity-card";

            card.innerHTML = `

                <div class="identity-card-image">

                    <img
                        src="${identity.image || "assets/images/avatar.png"}"
                        alt="${identity.name}"
                    >

                </div>

                <div class="identity-card-body">

                    <h3>${identity.name}</h3>

                    <p><strong>ID:</strong> ${identity.id}</p>

                    <p><strong>Camera:</strong> ${identity.camera}</p>

                    <p><strong>Confidence:</strong> ${(identity.confidence * 100).toFixed(1)}%</p>

                    <p><strong>Visits:</strong> ${identity.visits}</p>

                    <p><strong>Status:</strong> ${identity.status}</p>

                    <p><strong>Last Seen:</strong> ${identity.lastSeen}</p>

                </div>

            `;

            container.appendChild(card);

        });

    }

}

const identityManager = new IdentityManager();

export default identityManager;

export { IdentityManager };