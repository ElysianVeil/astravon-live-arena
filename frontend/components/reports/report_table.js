/*
============================================================
Astravon Live Arena
Report Table Component

Purpose:
    Renders reusable report tables for the Reports page.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

export default class ReportTable {

    constructor(container) {

        this.container =
            typeof container === "string"
                ? document.querySelector(container)
                : container;

        this.columns = [];
        this.rows = [];

    }

    /*
    ==========================================================
        Configure Columns
    ==========================================================
    */

    setColumns(columns = []) {

        this.columns = columns;

        return this;

    }

    /*
    ==========================================================
        Configure Rows
    ==========================================================
    */

    setRows(rows = []) {

        this.rows = rows;

        return this;

    }

    /*
    ==========================================================
        Render
    ==========================================================
    */

    render() {

        if (!this.container) return;

        this.container.innerHTML = "";

        const table = document.createElement("table");

        table.className = "dashboard-table report-table";

        table.appendChild(this.#createHeader());

        table.appendChild(this.#createBody());

        this.container.appendChild(table);

    }

    /*
    ==========================================================
        Update Data
    ==========================================================
    */

    update(rows = []) {

        this.rows = rows;

        this.render();

    }

    /*
    ==========================================================
        Clear
    ==========================================================
    */

    clear() {

        this.rows = [];

        this.render();

    }

    /*
    ==========================================================
        Header
    ==========================================================
    */

    #createHeader() {

        const thead = document.createElement("thead");

        const tr = document.createElement("tr");

        this.columns.forEach(column => {

            const th = document.createElement("th");

            th.textContent = column.label;

            tr.appendChild(th);

        });

        thead.appendChild(tr);

        return thead;

    }

    /*
    ==========================================================
        Body
    ==========================================================
    */

    #createBody() {

        const tbody = document.createElement("tbody");

        if (this.rows.length === 0) {

            const tr = document.createElement("tr");

            const td = document.createElement("td");

            td.colSpan = this.columns.length;

            td.className = "table-empty";

            td.textContent = "No report data available.";

            tr.appendChild(td);

            tbody.appendChild(tr);

            return tbody;

        }

        this.rows.forEach(row => {

            const tr = document.createElement("tr");

            this.columns.forEach(column => {

                const td = document.createElement("td");

                td.textContent = row[column.key] ?? "";

                tr.appendChild(td);

            });

            tbody.appendChild(tr);

        });

        return tbody;

    }

}