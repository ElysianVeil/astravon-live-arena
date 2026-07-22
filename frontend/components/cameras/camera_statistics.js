/*
============================================================
Astravon Live Arena
Camera Statistics Component

Purpose:
    Displays live AI engine statistics
    for selected camera.

Author:
    House of Astravon
============================================================
*/


class CameraStatistics {


    constructor(){

        this.container = null;

    }



    initialize(){

        this.container =
            document.getElementById(
                "cameraStatistics"
            );


        if(!this.container){

            console.warn(
                "[CameraStatistics] Container missing"
            );

            return;

        }


        this.renderEmpty();

    }




    update(statistics){


        if(!this.container){

            return;

        }


        if(!statistics){

            return;

        }



        const detection =
            statistics.detection ?? {};

        const occupancy =
            statistics.occupancy ?? {};

        const congestion =
            statistics.congestion ?? {};

        const risk =
            statistics.risk ?? {};

        const performance =
            statistics.performance ?? {};



        this.container.innerHTML = `


        <div class="stat-row">

            <strong>People:</strong>

            <span>
                ${detection.people_count ?? 0}
            </span>

        </div>



        <div class="stat-row">

            <strong>Occupancy:</strong>

            <span>
                ${occupancy.occupancy_percentage ?? 0}%
            </span>

        </div>



        <div class="stat-row">

            <strong>Status:</strong>

            <span>
                ${occupancy.status ?? "Unknown"}
            </span>

        </div>



        <div class="stat-row">

            <strong>Density:</strong>

            <span>
                ${occupancy.risk_level ?? "Unknown"}
            </span>

        </div>



        <div class="stat-row">

            <strong>Congestion:</strong>

            <span>
                ${congestion.current_level ?? "Unknown"}
            </span>

        </div>



        <div class="stat-row">

            <strong>Risk:</strong>

            <span>
                ${risk.risk_level ?? "Unknown"}
            </span>

        </div>



        <div class="stat-row">

            <strong>AI FPS:</strong>

            <span>
                ${
                    performance.current_fps ??
                    0
                }
            </span>

        </div>



        `;


    }




    renderEmpty(){

        this.container.innerHTML = `

        <p>
            Waiting for camera statistics...
        </p>

        `;

    }


}



export default new CameraStatistics();