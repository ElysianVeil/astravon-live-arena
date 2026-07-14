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

from typing import Dict, List, Optional

from vision.camera import Camera

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

        self.cameras[camera_id] = camera

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

        return camera.connect()

    # ========================================================
    # Connect All Cameras
    # ========================================================

    def connect_all(self):
        """
        Connects every registered camera.
        """

        for camera in self.cameras.values():

            camera.connect()

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

        return camera.read()

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

        for camera_id, camera in self.cameras.items():

            success, frame = camera.read()

            frames[camera_id] = {
                "success": success,
                "frame": frame
            }

        return frames

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

    # ========================================================
    # List Cameras
    # ========================================================

    def list_cameras(self) -> List[dict]:
        """
        Returns information about every camera.
        """

        return [
            camera.info()
            for camera in self.cameras.values()
        ]

    # ========================================================
    # Count
    # ========================================================

    @property
    def count(self) -> int:
        """
        Number of registered cameras.
        """

        return len(self.cameras)

    # ========================================================
    # Clear
    # ========================================================

    def clear(self):
        """
        Removes every camera.
        """

        self.disconnect_all()

        self.cameras.clear()

        logger.info(
            "All cameras removed."
        )