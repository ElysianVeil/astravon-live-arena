"""
============================================================
Astravon Live Arena
Camera Manager

Purpose:
    Manages multiple camera sources.

Responsibilities:
    • Register cameras
    • Connect cameras
    • Disconnect cameras
    • Read frames from all cameras
    • Remove cameras

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

from typing import Dict, List, Optional, Iterator

from vision.camera import Camera

import uuid

import time

from threading import Lock

from concurrent.futures import ThreadPoolExecutor
from utils.helpers import current_timestamp


from utils.logger import get_logger


# ============================================================
# Logger
# ============================================================

logger = get_logger("CameraManager")


# ============================================================
# Camera Manager
# ============================================================

class CameraManager:
    """
    Manages multiple cameras.
    """

    def __init__(self):

        self.cameras: Dict[str, Camera] = {}

        self.total_frames = 0

        self.lock = Lock()

        self.total_failures = 0

        self.read_duration = None

        self.last_update = None

        # =====================================================
        # Multi-Camera Session
        # =====================================================

        self.session_id = str(uuid.uuid4())

        self.global_frame_index = 0

        self.camera_order = []

        self.synchronized = True

    # ========================================================
    # Add Camera
    # ========================================================

    def add_camera(
        self,
        camera_id: str,
        source,
        name: Optional[str] = None
    ) -> Camera:
        """
        Registers a new camera.
        """

        if camera_id in self.cameras:

            raise ValueError(
                f"Camera '{camera_id}' already exists."
            )

        camera = Camera(
            source=source,
            name=name or camera_id
        )

        with self.lock:
            self.cameras[camera_id] = camera
            camera.manager_id = self.session_id

            camera.camera_index = len(self.camera_order)

            self.camera_order.append(camera_id)

        logger.info(
            f"Added camera '{camera_id}'."
        )

        return camera

    # ========================================================
    # Remove Camera
    # ========================================================

    def remove_camera(
        self,
        camera_id: str
    ) -> bool:
        """
        Removes a camera.
        """

        camera = self.cameras.get(camera_id)

        if camera is None:

            return False

        camera.release()

        with self.lock:
            del self.cameras[camera_id]

        logger.info(
            f"Removed camera '{camera_id}'."
        )

        return True

    # ========================================================
    # Connect One Camera
    # ========================================================

    def connect_camera(
        self,
        camera_id: str
    ) -> bool:
        """
        Connects one camera.
        """

        camera = self.cameras.get(camera_id)

        if camera is None:

            return False

        if camera.is_connected():

            logger.info(
                f"{camera.name} already connected."
            )

            return True

        return camera.connect()

    # ========================================================
    # Connect All Cameras
    # ========================================================

    def connect_all(self):
        """
        Connects every registered camera.
        """

        with ThreadPoolExecutor() as executor:

            results = list(
                executor.map(
                    lambda camera: camera.connect(),
                    self.cameras.values()
                )
            )

        logger.info(

            f"Connected {sum(results)}/{len(results)} cameras."

        )

    def active_camera_ids(self) -> list[str]:
        """
        Returns IDs of connected cameras.
        """

        return [

            camera_id

            for camera_id, camera in self.cameras.items()

            if camera.is_connected()

        ]
            
    # ========================================================
    # Disconnect One Camera
    # ========================================================

    def disconnect_camera(
        self,
        camera_id: str
    ):
        """
        Disconnects one camera.
        """

        camera = self.cameras.get(camera_id)

        if camera:

            camera.release()

    # ========================================================
    # Disconnect All
    # ========================================================

    def disconnect_all(self):
        """
        Disconnects every camera.
        """

        for camera in self.cameras.values():

            camera.release()

    # ========================================================
    # Read One Camera
    # ========================================================

    def read_camera(
        self,
        camera_id: str
    ):
        """
        Reads one frame.
        """

        camera = self.cameras.get(camera_id)

        if camera is None:

            return False, None

        success, frame = camera.read()

        if success:
            with self.lock:
                self.total_frames += 1

        else:

            with self.lock:
                self.total_failures += 1

        return success, frame

    # ========================================================
    # Read All Cameras
    # ========================================================

    def read_all(self):
        """
        Reads frames from all connected cameras.

        Returns
        -------
        {
            camera_id:
            {
                "success": bool,
                "frame": ndarray
            }
        }
        """

        frames = {}

        timestamp = current_timestamp()

        self.global_frame_index += 1
        

        for camera_id, camera in self.cameras.items():
            if not camera.is_connected():

                continue

            start = time.perf_counter()

            success, frame = camera.read()

            elapsed = time.perf_counter() - start

            self.read_duration = elapsed

            if not success:

                logger.warning(
                    f"{camera.name} disconnected."
                )
                with self.lock:
                    self.total_failures += 1
                if camera.reconnect():
                    logger.info(

                        f"{camera.name} reconnected."

                    )

                else:

                    logger.error(

                        f"{camera.name} failed to reconnect."

                    )
            else:
                with self.lock:
                    self.total_frames += 1

            self.last_update = time.time()
            frames[camera_id] = {

                "frame": frame,

                "camera": camera,

                "metadata": camera.info(),

                "camera_id": camera_id,

                "camera_name": camera.name,

                "camera_index": camera.camera_index,

                "manager_id": self.session_id,

                "frame_index": self.global_frame_index,

                "timestamp": timestamp,

                "success": success
            }

        return frames
    
    def synchronized_frames(self):
        """
        Returns synchronized frames from all
        connected cameras.

        This is the primary API used by the
        multi-camera AI pipeline.
        """

        return {

            "session": self.session_id,

            "frame_index": self.global_frame_index,

            "timestamp": current_timestamp(),

            "cameras": self.read_all()
        }
    
    def frames(self) -> Iterator[dict]:
        """
        Generator returning one camera frame
        at a time.

        Useful for pipeline processing.
        """

        data = self.read_all()

        for frame in data.values():

            yield frame

    # ========================================================
    # Get Camera
    # ========================================================

    def get_camera(
        self,
        camera_id: str
    ) -> Optional[Camera]:
        """
        Returns a camera.
        """

        return self.cameras.get(camera_id)
    
    def get_latest_frame(
        self,
        camera_id: str
    ):

        camera = self.cameras.get(camera_id)

        if camera is None:

            return None

        return camera.get_latest_frame()
    
    def latest_frames(self):

        frames = {}

        for camera_id, camera in self.cameras.items():

            frame = camera.get_latest_frame()

            if frame is not None:

                frames[camera_id] = frame

        return frames

    # ========================================================
    # List Cameras
    # ========================================================

    def list_cameras(self) -> List[dict]:
        """
        Returns information about every camera.
        """

        return sorted(

            [camera.info() for camera in self.cameras.values()],

            key=lambda camera: camera["name"]

        )
    
    def get_camera_by_name(

        self,

        name: str

    ):

        for camera in self.cameras.values():

            if camera.name == name:

                return camera

        return None
    
    def connected_cameras(self):

        return [

            camera

            for camera in self.cameras.values()

            if camera.is_connected()

        ]
    
    def performance(self):

        fps = 0

        for camera in self.cameras.values():

            fps += camera.actual_fps

        return {

            "camera_count": len(self.cameras),

            "total_fps": round(fps, 2),

            "frames": self.total_frames,

            "failures": self.total_failures

        }
    
    def synchronization(self) -> dict:
        """
        Multi-camera synchronization status.
        """

        return {

            "session": self.session_id,

            "camera_count": len(self.cameras),

            "connected": len(self.connected_cameras()),

            "frame_index": self.global_frame_index,

            "synchronized": self.synchronized
        }

    # ========================================================
    # Count
    # ========================================================

    @property
    def count(self) -> int:
        """
        Number of registered cameras.
        """

        return len(self.cameras)

    def get_health(self):

        healthy = 0

        reconnecting = 0

        offline = 0

        for camera in self.cameras.values():

            if camera.health == "Healthy":

                healthy += 1

            elif camera.health == "Reconnecting":

                reconnecting += 1

            else:

                offline += 1

        return {

            "total": len(self.cameras),

            "healthy": healthy,

            "reconnecting": reconnecting,

            "offline": offline,

            "frames": self.total_frames,

            "failures": self.total_failures

        }
    
    def info(self):

        return {

            "camera_count": self.count,

            "connected": len(self.connected_cameras()),

            "frames": self.total_frames,

            "failures": self.total_failures,

            "last_update": self.last_update

        }
    
    def summary(self) -> dict:
        """
        Summary for analytics.
        """

        return {

            "session": self.session_id,

            "camera_count": len(self.cameras),

            "connected": len(self.connected_cameras()),

            "active_ids": self.active_camera_ids(),

            "frames": self.total_frames,

            "failures": self.total_failures,

            "frame_index": self.global_frame_index
        }

    # ========================================================
    # Clear
    # ========================================================

    def clear(self):
        """
        Removes every camera.
        """

        self.disconnect_all()

        with self.lock:

            self.cameras.clear()

            self.total_frames = 0

            self.total_failures = 0

            self.read_duration = None

            self.last_update = None

            self.session_id = str(uuid.uuid4())

            self.global_frame_index = 0

            self.camera_order.clear()

        logger.info(
            "All cameras removed."
        )