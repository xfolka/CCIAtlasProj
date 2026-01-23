from pathlib import Path

import numpy as np
import tifffile
from PySide6.QtGui import QImage, QPixmap


def load_image(file_path: Path) -> QImage:
    if file_path.suffix == ".tif" or file_path.suffix == ".tif":
        return load_tiff(file_path)
    
    
def load_tiff(file_path: Path) -> QImage:
    arr = tifffile.imread(file_path)
    arr = np.ascontiguousarray(arr, dtype=np.uint8)
    if arr.ndim == 2:
        h, w = arr.shape
        qimg = QImage(arr.data, w, h, w, QImage.Format_Grayscale8)
    elif arr.ndim == 3 and arr.shape[2] == 3:
        h, w, _ = arr.shape
    # Qt wants RGB888
        qimg = QImage(arr.data, w, h, 3 * w, QImage.Format_RGB888)
    elif arr.ndim == 3 and arr.shape[2] == 4:
        h, w, _ = arr.shape
        qimg = QImage(arr.data, w, h, 4 * w, QImage.Format_RGBA8888)
    else:
        raise ValueError("Unsupported TIFF format")
    
    return qimg
