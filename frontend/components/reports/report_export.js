/*
============================================================
Astravon Live Arena
Report Export Component

Purpose:
    Handles exporting report data into various formats.

Supported Formats:
    • CSV
    • JSON
    • PDF (Placeholder)

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

export default class ReportExport {

    constructor(filename = "astravon-report") {

        this.filename = filename;

    }

    /*
    ==========================================================
        Update Filename
    ==========================================================
    */

    setFilename(filename) {

        this.filename = filename;

        return this;

    }

    /*
    ==========================================================
        Export CSV
    ==========================================================
    */

    exportCSV(rows = []) {

        if (!Array.isArray(rows) || rows.length === 0) {

            console.warn("No report data to export.");

            return;

        }

        const headers = Object.keys(rows[0]);

        const csv = [];

        csv.push(headers.join(","));

        rows.forEach(row => {

            const values = headers.map(header => {

                const value = row[header] ?? "";

                return `"${String(value).replace(/"/g, '""')}"`;

            });

            csv.push(values.join(","));

        });

        this.#download(
            csv.join("\n"),
            `${this.filename}.csv`,
            "text/csv"
        );

    }

    /*
    ==========================================================
        Export JSON
    ==========================================================
    */

    exportJSON(rows = []) {

        const json = JSON.stringify(rows, null, 4);

        this.#download(
            json,
            `${this.filename}.json`,
            "application/json"
        );

    }

    /*
    ==========================================================
        Export PDF
    ==========================================================
    */

    exportPDF() {

        console.warn(
            "PDF export not implemented. Integrate jsPDF or pdf-lib."
        );

    }

    /*
    ==========================================================
        Generic Download
    ==========================================================
    */

    #download(content, filename, type) {

        const blob = new Blob(
            [content],
            { type }
        );

        const url = URL.createObjectURL(blob);

        const link = document.createElement("a");

        link.href = url;

        link.download = filename;

        document.body.appendChild(link);

        link.click();

        document.body.removeChild(link);

        URL.revokeObjectURL(url);

    }

}