"""
============================================================
Astravon Live Arena
YOLO Model Loader

Purpose:
    Loads and manages the YOLO detection model.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from pathlib import Path

from ultralytics import YOLO

from config import settings

from utils.logger import get_logger


# ============================================================
# Logger
# ============================================================

logger = get_logger("YOLOLoader")


# ============================================================
# Loader
# ============================================================

class YOLOModelLoader:
    """
    Loads a YOLO model once and returns
    the initialized model.
    """

    def __init__(self, model_path: Path | str | None = None):

        self.model_path = Path(
            model_path or settings.YOLO_MODEL
        )

        self.labels = []
        self.model = None

    def model_info(self) -> dict:

        return {
            "path": str(self.model_path),
            "loaded": self.loaded,
            "classes": len(self.labels),
            "model_name": self.model_path.name
        }
    
    def class_name(self, class_id: int) -> str:

        if 0 <= class_id < len(self.labels):
            return self.labels[class_id]

        return "Unknown"
    
    def class_id(self, name: str) -> int:

        try:
            return self.labels.index(name)

        except ValueError:
            return -1

    # ========================================================
    # Load
    # ========================================================

    def load(self):
        """
        Loads the YOLO model.

        Returns
        -------
        ultralytics.YOLO
        """

        if self.model is not None:

            return self.model

        if not self.model_path.exists():

            raise FileNotFoundError(
                f"YOLO model not found:\n{self.model_path}"
            )

        logger.info(
            f"Loading model: {self.model_path.name}"
        )

        self.model = YOLO(str(self.model_path))
        self.labels = self.load_labels()

        logger.info("YOLO model loaded successfully.")

        return self.model

    # ========================================================
    # Load Labels
    # ========================================================

    def load_labels(self) -> list[str]:
        """
        Loads COCO class labels.
        """

        labels_file = self.model_path.parent / "labels.txt"

        if not labels_file.exists():
            raise FileNotFoundError(labels_file)

        with open(labels_file, "r", encoding="utf-8") as file:
            return [
                line.strip()
                for line in file
                if line.strip()
            ]

    # ========================================================
    # Reload
    # ========================================================

    def reload(self):
        """
        Reloads the model from disk.
        """

        self.model = None

        return self.load()

    # ========================================================
    # Is Loaded
    # ========================================================

    @property
    def loaded(self):

        return self.model is not None
    
loader = YOLOModelLoader()

model = loader.load()

if __name__ == "__main__":

    loader = YOLOModelLoader()

    model = loader.load()

    print(loader.model_info())

    print(loader.class_name(0))

    print(loader.class_id("person"))