/*
============================================================
Astravon Live Arena
Identity History Component

Purpose:
    Stores and manages historical Person
    Re-Identification (ReID) events.

Responsibilities:
    • Record sightings
    • Maintain chronological history
    • Search history
    • Filter history
    • Generate simple statistics
    • Render history timeline/table

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

class IdentityHistory {

    constructor(maxRecords = 1000) {

        this.records = [];

        this.maxRecords = maxRecords;

    }

    /*==========================================================
        Add History Record
    ==========================================================*/

    add(record = {}) {

        this.records.unshift({

            id: record.id ?? "UNKNOWN",

            name: record.name ?? "Unknown",

            camera: record.camera ?? "Unknown",

            confidence: record.confidence ?? 0,

            timestamp: record.timestamp ??
                new Date().toISOString(),

            event: record.event ?? "Detected",

            duration: record.duration ?? 0,

            image: record.image ?? ""

        });

        if (this.records.length > this.maxRecords) {

            this.records.pop();

        }

    }

    /*==========================================================
        Clear History
    ==========================================================*/

    clear() {

        this.records = [];

    }

    /*==========================================================
        Retrieval
    ==========================================================*/

    getAll() {

        return [...this.records];

    }

    getRecent(limit = 20) {

        return this.records.slice(0, limit);

    }

    getByPerson(id) {

        return this.records.filter(record =>

            record.id === id

        );

    }

    getByCamera(camera) {

        return this.records.filter(record =>

            record.camera === camera

        );

    }

    /*==========================================================
        Search
    ==========================================================*/

    search(query = "") {

        query = query.toLowerCase();

        return this.records.filter(record =>

            record.id.toLowerCase().includes(query) ||

            record.name.toLowerCase().includes(query) ||

            record.camera.toLowerCase().includes(query)

        );

    }

    /*==========================================================
        Statistics
    ==========================================================*/

    count() {

        return this.records.length;

    }

    getUniquePeopleCount() {

        return new Set(

            this.records.map(record => record.id)

        ).size;

    }

    getAverageConfidence() {

        if (!this.records.length) {

            return 0;

        }

        const total = this.records.reduce(

            (sum, record) =>

                sum + record.confidence,

            0

        );

        return total / this.records.length;

    }

    /*==========================================================
        Rendering
    ==========================================================*/

    render(container) {

        if (!container) {

            return;

        }

        container.innerHTML = "";

        if (!this.records.length) {

            container.innerHTML = `

                <div class="empty-state">

                    <h3>No Identity History</h3>

                    <p>

                        Waiting for detections...

                    </p>

                </div>

            `;

            return;

        }

        const table = document.createElement("table");

        table.className = "dashboard-table";

        table.innerHTML = `

            <thead>

                <tr>

                    <th>Person</th>

                    <th>Camera</th>

                    <th>Confidence</th>

                    <th>Event</th>

                    <th>Time</th>

                </tr>

            </thead>

            <tbody></tbody>

        `;

        const tbody = table.querySelector("tbody");

        this.records.forEach(record => {

            const row = document.createElement("tr");

            row.innerHTML = `

                <td>

                    ${record.name}

                    <br>

                    <small>${record.id}</small>

                </td>

                <td>

                    ${record.camera}

                </td>

                <td>

                    ${(record.confidence * 100).toFixed(1)}%

                </td>

                <td>

                    ${record.event}

                </td>

                <td>

                    ${new Date(record.timestamp)
                        .toLocaleString()}

                </td>

            `;

            tbody.appendChild(row);

        });

        container.appendChild(table);

    }

}

const identityHistory = new IdentityHistory();

export default identityHistory;

export { IdentityHistory };