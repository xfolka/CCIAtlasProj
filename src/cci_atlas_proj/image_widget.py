from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PySide6.QtGui import QPainter, QPixmap, QPen, QImage, QTransform
from cci_atlas_proj.atlas_region import AtlasRegion
from cci_atlas_proj.atlas_geometry import AtlasGeometry, AtlasGeometryType
from PySide6.QtCore import QSize, QPoint, QRectF, Qt
import sys
from pathlib import Path


class ImageDrawWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pixmap = QPixmap()      # image + drawing surface
        self._img_transform = QTransform()
        self._last_pos: QPoint | None = None

        # Drawing pen
        self._pen = QPen(Qt.red, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

        # list of rectangle items: {rect, transform, pen}
        self._rect_items: list[dict] = []
        # Optional: background if no image
        self.setAttribute(Qt.WA_StaticContents)

        self.canvas_w = 1200
        self.canvas_h = 1200

        self.proj_half_width = 200000
        self.proj_half_height = 200000
        self._proj_to_canvas_transform = self._project_to_canvas_transform(-self.proj_half_width, -self.proj_half_height, self.proj_half_width, self.proj_half_height, self.canvas_w, self.canvas_h)
        
        self.resize(self.canvas_h, self.canvas_w)
        self.show()

    def _project_to_canvas_transform(self, min_x, min_y, max_x, max_y, canvas_w, canvas_h):
        pw = max_x - min_x
        ph = max_y - min_y
        if pw <= 0 or ph <= 0 or canvas_w <= 0 or canvas_h <= 0:
            return QTransform()  # identity fallback

        s = min(canvas_w / pw, canvas_h / ph)

        tx = -min_x * s + (canvas_w - pw * s) / 2.0
        ty = -min_y * s + (canvas_h - ph * s) / 2.0
        
        t = QTransform()
        t.translate(tx, ty)
        t.scale(s, s)
        return t

    # ---------- Public API ----------

    def load_image_from_image(self, source: QImage, transform: QTransform):
        qpix: QPixmap = QPixmap.fromImage(source)
        self._img_transform = transform
        self.load_image_from_pixmap(qpix)

    def load_image_from_pixmap(self, source: QPixmap):
        # pm = QPixmap(str(source))

        if source.isNull():
            raise ValueError("Failed to load image")

        self._pixmap = source
        self.setFixedSize(self._pixmap.size())
        self.update()

    def set_pen(self, color: Qt.GlobalColor, width: int = 3):
        self._pen = QPen(color, width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

    def get_pixmap(self) -> QPixmap:
        """
        Get the current pixmap (image + drawings), e.g. to save to disk.
        """
        return self._pixmap

    # def sizeHint(self):
    #     # Default size when no image is loaded
    #     if not self._pixmap.isNull():
    #         return self._pixmap.size()
    #     return QSize(800, 800)   # or whatever you like

    def minimumSizeHint(self):
        return QSize(800, 800)

    def add_regions(self, regions: list[AtlasRegion]):
        for region in regions:
            transform = region.get_transform()
            geometry = region.get_geometry()
            
            if geometry.type == AtlasGeometryType.RECTANGLE:
                self.add_rect(geometry.get_width(), geometry.get_height(), transform.to_qtransform())
                #self.add_rect(geometry.get_width(), geometry.get_height(), QTransform())

    def add_rect(self, width: float, height: float,
                 transform: QTransform,
                 color: Qt.GlobalColor = Qt.green,
                 pen_width: int = 2):
        """
        Add a rectangle defined in local coordinates:

            - centered at (0, 0)
            - size = width x height

        and positioned on the image using the given transform.
        """
        flip_y = QTransform()
        flip_y.translate(0, self.canvas_h)
        flip_y.scale(1, -1)
        
        # local rect: centered at (0,0)
        rect = QRectF(-width / 2.0, -height / 2.0, width, height)
        #rect = QRectF(0, 0, width, height)
        pen = QPen(color, pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        pen.setCosmetic(True)
        item = {
            "rect": rect,
            "transform": QTransform(transform * flip_y),  # copy
            "pen": pen,
        }
        self._rect_items.append(item)
        self.update()

    def clear_rects(self):
        self._rect_items.clear()
        self.update()

    # ---------- Events ----------

    def paintEvent(self, event):
        painter = QPainter(self)

        flip_y = QTransform()
        flip_y.translate(0, self.canvas_h)
        flip_y.scale(1, -1)


        painter.setTransform(self._proj_to_canvas_transform, combine=False)

        if not self._pixmap.isNull():
            painter.save()
            painter.setWorldTransform(self._img_transform, combine=True)
            painter.drawPixmap(0,0, self._pixmap)
            painter.restore()
        else:
            # simple gray background if no image
            painter.fillRect(self.rect(), Qt.lightGray)
            
        # 2. draw rectangles using their own transforms
        for item in self._rect_items:
            painter.save()
            painter.setWorldTransform(item["transform"], combine=True)
            painter.setPen(item["pen"])
            #painter.drawRect(QRectF(100000,100000,500000,500000))
            painter.drawRect(item["rect"])
            
            painter.save()
            painter.resetTransform()
            painter.setWorldTransform(item["transform"], combine=True)
            trans = painter.combinedTransform()  # includes current world/view/device transforms
            c_local = item["rect"].center()
            c_dev = trans.map(c_local)

            painter.resetTransform()
            
            painter.drawText(c_dev.x(), c_dev.y(), f"({c_dev.x()},{c_dev.y()})")
            painter.restore()
            painter.restore()
            
            painter.resetTransform()
            painter.setPen(self._pen)
            painter.drawEllipse(1200 / 2, 1200 / 2, 2, 2)

       

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self._pixmap.isNull():
            self._last_pos = event.position().toPoint()
            event.accept()
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        if (
            event.buttons() & Qt.LeftButton
            and self._last_pos is not None
            and not self._pixmap.isNull()
        ):
            current_pos = event.position().toPoint()

            # Draw directly on the pixmap
            painter = QPainter(self._pixmap)
            painter.setPen(self._pen)
            painter.drawLine(self._last_pos, current_pos)

            self._last_pos = current_pos
            self.update()  # trigger repaint
            event.accept()
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._last_pos = None
            event.accept()
        else:
            event.ignore()


class ImageDrawView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the drawing surface
        self.canvas = ImageDrawWidget()

        # Create the scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.canvas)
        #self.scroll.setWidgetResizable(False)   # keep canvas at natural size

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll)

    # ---- Public API ----
    def load_image_from_image(self, source: QImage, transform: QTransform):
        self.canvas.load_image_from_image(source, transform)

    def set_pen(self, *args, **kwargs):
        self.canvas.set_pen(*args, **kwargs)

    def get_pixmap(self):
        return self.canvas.get_pixmap()
    
    def add_regions(self, regions: list[AtlasRegion]):
        self.canvas.add_regions(regions)

