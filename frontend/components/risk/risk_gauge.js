/*
============================================================
Astravon Live Arena
Risk Gauge Component

Purpose:
    Displays the overall venue risk level.

Responsibilities:
    • Update risk score
    • Animate progress
    • Update status text
    • Apply severity colors
    • Render recommendations

Author:
    House of Astravon

Version:
    1.0.0
============================================================
*/

class RiskGauge {

    constructor() {

        this.container = null;
        this.score = 0;

    }

    /*==========================================================
        Initialize
    ==========================================================*/

    initialize(containerId = "riskTrendPanel") {

        this.container = document.getElementById(containerId);

        if (!this.container) {

            console.warn(
                `[RiskGauge] Container "${containerId}" not found.`
            );

            return;

        }

        this.render();

    }

    /*==========================================================
        Render
    ==========================================================*/

    render() {

        if (!this.container) return;

        this.container.innerHTML = `

            <div class="risk-meter">

                <div class="risk-meter-header">

                    <span class="risk-label">

                        Overall Risk

                    </span>

                    <span
                        id="riskGaugeValue"
                        class="risk-value"
                    >

                        ${this.score}%

                    </span>

                </div>

                <div class="risk-bar">

                    <div
                        id="riskGaugeProgress"
                        class="risk-progress"
                        style="width:${this.score}%"
                    ></div>

                </div>

                <div
                    id="riskGaugeStatus"
                    class="risk-status"
                >

                    ${this.getStatus()}

                </div>

            </div>

        `;

        this.updateColor();

    }

    /*==========================================================
        Update
    ==========================================================*/

    setRisk(score) {

        this.score = Math.max(
            0,
            Math.min(100, score)
        );

        const value =
            document.getElementById(
                "riskGaugeValue"
            );

        const progress =
            document.getElementById(
                "riskGaugeProgress"
            );

        const status =
            document.getElementById(
                "riskGaugeStatus"
            );

        if (!value || !progress || !status) {

            this.render();
            return;

        }

        value.textContent = `${this.score}%`;

        progress.style.width = `${this.score}%`;

        status.textContent = this.getStatus();

        this.updateColor();

    }

    /*==========================================================
        Status
    ==========================================================*/

    getStatus() {

        if (this.score >= 80) {

            return "Critical Risk";

        }

        if (this.score >= 60) {

            return "High Risk";

        }

        if (this.score >= 40) {

            return "Moderate Risk";

        }

        if (this.score >= 20) {

            return "Low Risk";

        }

        return "Safe";

    }

    /*==========================================================
        Color
    ==========================================================*/

    updateColor() {

        const progress =
            document.getElementById(
                "riskGaugeProgress"
            );

        const status =
            document.getElementById(
                "riskGaugeStatus"
            );

        if (!progress || !status) {

            return;

        }

        progress.className = "risk-progress";

        status.className = "risk-status";

        if (this.score >= 80) {

            progress.classList.add("progress-danger");
            status.classList.add("status-danger");

        }

        else if (this.score >= 60) {

            progress.classList.add("progress-warning");
            status.classList.add("status-warning");

        }

        else {

            progress.classList.add("progress-good");
            status.classList.add("status-success");

        }

    }

    /*==========================================================
        Recommendation
    ==========================================================*/

    getRecommendation() {

        if (this.score >= 80) {

            return "Immediate emergency response recommended.";

        }

        if (this.score >= 60) {

            return "Increase monitoring and prepare responders.";

        }

        if (this.score >= 40) {

            return "Continue observation and monitor crowd.";

        }

        return "Normal operations.";

    }

    /*==========================================================
        Snapshot
    ==========================================================*/

    getSnapshot() {

        return {

            score: this.score,

            status: this.getStatus(),

            recommendation:
                this.getRecommendation()

        };

    }

}

const riskGauge = new RiskGauge();

export default riskGauge;

export { RiskGauge };