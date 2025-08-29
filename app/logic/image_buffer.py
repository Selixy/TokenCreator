from __future__ import annotations
from pathlib import Path
import numpy as np
import cv2

if False:
    from ui.workspace import Workspace


class ImageBuffer:
    def __init__(self, workspace: "Workspace") -> None:
        self._workspace = workspace
        self._buffer: np.ndarray | None = None

    def load_image(self, path: str | Path) -> None:

        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(path)

        img = cv2.imread(str(p), cv2.IMREAD_UNCHANGED)
        if img is None:
            raise IOError(f"Impossible de lire l'image: {path}")

        self._buffer = self._to_rgba(img)
        self._workspace.show_from_buffer(self._buffer)


    def _tone_map_hdr(img_f32: np.ndarray) -> np.ndarray:
        img = np.clip(img_f32, 0, None)
        img = img / (1.0 + img)
        img = np.power(img, 1/2.2)
        img_u8 = np.clip(img * 255.0, 0, 255).astype(np.uint8)
        return img_u8

    @staticmethod
    def _to_rgba(img: np.ndarray) -> np.ndarray:
        """ndarray OpenCV -> RGBA8 (H, W, 4)"""
        depth = img.dtype

        if depth == np.uint16:
            img_8 = (img >> 8).astype(np.uint8, copy=False)
            img = img_8
        elif depth == np.float32:
            img = ImageBuffer._tone_map_hdr(img)

        if img.ndim == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGBA)
        elif img.ndim == 3 and img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        elif img.ndim == 3 and img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
        else:
            raise ValueError(f"Format non supporté: shape={img.shape}, dtype={depth}")

        if img.dtype != np.uint8:
            img = img.astype(np.uint8, copy=False)
        return img
