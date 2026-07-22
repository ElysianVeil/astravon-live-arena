/*
============================================================
Astravon Live Arena
Tracking Component

Purpose:
    Handles live person tracking information received
    from the backend and provides helper utilities for
    rendering tracking statistics.

Author:
    House of Astravon
Version:
    1.0.0
============================================================
*/

class TrackingManager {

    constructor() {

        this.tracks = new Map();

        this.lastUpdated = null;

    }

    /*==========================================================
        Track Management
    ==========================================================*/

    update(trackingData = []) {

        this.tracks.clear();

        trackingData.forEach(track => {

            if (!track.id) {

                return;

            }

            this.tracks.set(track.id, {

                id: track.id,

                camera: track.camera ?? "Unknown",

                bbox: track.bbox ?? [],

                confidence: track.confidence ?? 0,

                duration: track.duration ?? 0,

                velocity: track.velocity ?? 0,

                direction: track.direction ?? "Unknown",

                status: track.status ?? "Tracking"

            });

        });

        this.lastUpdated = new Date();

    }

    clear() {

        this.tracks.clear();

    }

    /*==========================================================
        Getters
    ==========================================================*/

    getTrack(id) {

        return this.tracks.get(id) ?? null;

    }

    getTracks() {

        return [...this.tracks.values()];

    }

    getCount() {

        return this.tracks.size;

    }

    getLastUpdated() {

        return this.lastUpdated;

    }

    /*==========================================================
        Statistics
    ==========================================================*/

    getAverageConfidence() {

        if (!this.tracks.size) {

            return 0;

        }

        const total = this.getTracks().reduce((sum, track) => {

            return sum + track.confidence;

        }, 0);

        return total / this.tracks.size;

    }

    getAverageVelocity() {

        if (!this.tracks.size) {

            return 0;

        }

        const total = this.getTracks().reduce((sum, track) => {

            return sum + track.velocity;

        }, 0);

        return total / this.tracks.size;

    }

    /*==========================================================
        Rendering
    ==========================================================*/

    render(container) {

        if (!container) {

            return;

        }

        container.innerHTML = "";

        if (!this.tracks.size) {

            container.innerHTML = `

                <div class="empty-state">

                    <h3>No Active Tracks</h3>

                    <p>
                        Waiting for tracking data...
                    </p>

                </div>

            `;

            return;

        }

        this.getTracks().forEach(track => {

            const card = document.createElement("div");

            card.className = "tracking-card";

            card.innerHTML = `

                <div class="tracking-header">

                    <strong>Track #${track.id}</strong>

                    <span>${track.status}</span>

                </div>

                <div class="tracking-body">

                    <p><strong>Camera:</strong> ${track.camera}</p>

                    <p><strong>Confidence:</strong> ${(track.confidence * 100).toFixed(1)}%</p>

                    <p><strong>Direction:</strong> ${track.direction}</p>

                    <p><strong>Speed:</strong> ${track.velocity.toFixed(2)} px/s</p>

                    <p><strong>Duration:</strong> ${track.duration.toFixed(1)} s</p>

                </div>

            `;

            container.appendChild(card);

        });

    }

}

const trackingManager = new TrackingManager();

export default trackingManager;
export { TrackingManager };