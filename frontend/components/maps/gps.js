/*
============================================================
Astravon Live Arena
GPS & Location Manager

Purpose:
    Handles GPS positions for cameras, emergency
    vehicles, crowd markers and venue assets.

Author:
    House of Astravon
============================================================
*/

class GPSManager {

    constructor() {

        this.cameraLocations = new Map();
        this.vehicleLocations = new Map();
        this.personLocations = new Map();
        this.zoneLocations = new Map();

        this.userLocation = null;

        this.watchId = null;

        this.listeners = [];

    }

    /*==========================================================
        User Location
    ==========================================================*/

    async getCurrentLocation() {

        if (!navigator.geolocation) {

            throw new Error("Geolocation not supported.");

        }

        return new Promise((resolve, reject) => {

            navigator.geolocation.getCurrentPosition(

                (position) => {

                    this.userLocation = {

                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                        accuracy: position.coords.accuracy,
                        timestamp: Date.now()

                    };

                    resolve(this.userLocation);

                },

                reject,

                {

                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 5000

                }

            );

        });

    }

    startWatching() {

        if (!navigator.geolocation) return;

        this.watchId = navigator.geolocation.watchPosition(

            (position) => {

                this.userLocation = {

                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    accuracy: position.coords.accuracy,
                    timestamp: Date.now()

                };

                this.notify();

            },

            console.error,

            {

                enableHighAccuracy: true

            }

        );

    }

    stopWatching() {

        if (this.watchId !== null) {

            navigator.geolocation.clearWatch(this.watchId);

            this.watchId = null;

        }

    }

    /*==========================================================
        Cameras
    ==========================================================*/

    setCameraLocation(id, latitude, longitude) {

        this.cameraLocations.set(id, {

            id,
            latitude,
            longitude

        });

        this.notify();

    }

    getCameraLocation(id) {

        return this.cameraLocations.get(id);

    }

    getAllCameraLocations() {

        return [...this.cameraLocations.values()];

    }

    /*==========================================================
        Vehicles
    ==========================================================*/

    setVehicleLocation(id, latitude, longitude, status = "available") {

        this.vehicleLocations.set(id, {

            id,
            latitude,
            longitude,
            status

        });

        this.notify();

    }

    updateVehicle(id, latitude, longitude) {

        const vehicle = this.vehicleLocations.get(id);

        if (!vehicle) return;

        vehicle.latitude = latitude;
        vehicle.longitude = longitude;

        this.notify();

    }

    getVehicles() {

        return [...this.vehicleLocations.values()];

    }

    /*==========================================================
        Crowd / People
    ==========================================================*/

    setPersonLocation(id, latitude, longitude) {

        this.personLocations.set(id, {

            id,
            latitude,
            longitude

        });

    }

    removePerson(id) {

        this.personLocations.delete(id);

    }

    getPeople() {

        return [...this.personLocations.values()];

    }

    /*==========================================================
        Zones
    ==========================================================*/

    setZone(name, coordinates) {

        this.zoneLocations.set(name, {

            name,
            coordinates

        });

    }

    getZone(name) {

        return this.zoneLocations.get(name);

    }

    getZones() {

        return [...this.zoneLocations.values()];

    }

    /*==========================================================
        Distance
    ==========================================================*/

    calculateDistance(a, b) {

        const R = 6371000;

        const φ1 = a.latitude * Math.PI / 180;
        const φ2 = b.latitude * Math.PI / 180;

        const Δφ = (b.latitude - a.latitude) * Math.PI / 180;
        const Δλ = (b.longitude - a.longitude) * Math.PI / 180;

        const x =

            Math.sin(Δφ / 2) ** 2 +

            Math.cos(φ1) *

            Math.cos(φ2) *

            Math.sin(Δλ / 2) ** 2;

        const c =

            2 *

            Math.atan2(

                Math.sqrt(x),

                Math.sqrt(1 - x)

            );

        return R * c;

    }

    nearestCamera(position) {

        let nearest = null;

        let min = Infinity;

        this.cameraLocations.forEach(camera => {

            const d = this.calculateDistance(position, camera);

            if (d < min) {

                min = d;

                nearest = camera;

            }

        });

        return {

            camera: nearest,
            distance: min

        };

    }

    nearestVehicle(position) {

        let nearest = null;

        let min = Infinity;

        this.vehicleLocations.forEach(vehicle => {

            const d = this.calculateDistance(position, vehicle);

            if (d < min) {

                min = d;

                nearest = vehicle;

            }

        });

        return {

            vehicle: nearest,
            distance: min

        };

    }

    /*==========================================================
        Import / Export
    ==========================================================*/

    load(data = {}) {

        data.cameras?.forEach(c =>

            this.setCameraLocation(

                c.id,

                c.latitude,

                c.longitude

            )

        );

        data.vehicles?.forEach(v =>

            this.setVehicleLocation(

                v.id,

                v.latitude,

                v.longitude,

                v.status

            )

        );

        data.zones?.forEach(z =>

            this.setZone(

                z.name,

                z.coordinates

            )

        );

    }

    export() {

        return {

            cameras: this.getAllCameraLocations(),

            vehicles: this.getVehicles(),

            zones: this.getZones(),

            people: this.getPeople(),

            user: this.userLocation

        };

    }

    /*==========================================================
        Events
    ==========================================================*/

    subscribe(callback) {

        this.listeners.push(callback);

    }

    unsubscribe(callback) {

        this.listeners =

            this.listeners.filter(

                listener => listener !== callback

            );

    }

    notify() {

        const snapshot = this.export();

        this.listeners.forEach(

            listener => listener(snapshot)

        );

    }

}

const gpsManager = new GPSManager();

export {

    GPSManager,
    gpsManager

};