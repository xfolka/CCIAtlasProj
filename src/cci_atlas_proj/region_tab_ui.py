from typing import Tuple
from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QLineEdit,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class ShapeTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the three tab pages
        self.rectangle_tab = self._create_rectangle_tab()
        self.polygon_tab = self._create_polygon_tab()
        self.ellipse_tab = self._create_ellipse_tab()

        # Add them to the QTabWidget
        self.addTab(self.rectangle_tab, "Rectangle")
        #self.addTab(self.polygon_tab, "Polygon")
        self.addTab(self.ellipse_tab, "Oval")

    def _create_rectangle_tab(self) -> QWidget:
        widget = QWidget()
        layout = QGridLayout(widget)

        # Validator for numeric input
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)

        # Create labels + inputs
        self.x_rect_edit = QLineEdit("0")
        self.y_rect_edit = QLineEdit("0")
        self.w_rect_edit = QLineEdit("0")
        self.h_rect_edit = QLineEdit("0")
        self.r_rect_edit = QLineEdit("0")

        for edit in (self.x_rect_edit, self.y_rect_edit, self.w_rect_edit, self.h_rect_edit):
            edit.setValidator(validator)

        # Grid layout: label left, field right
        layout.addWidget(QLabel("X:"), 0, 0)
        layout.addWidget(self.x_rect_edit, 0, 1)

        layout.addWidget(QLabel("Y:"), 1, 0)
        layout.addWidget(self.y_rect_edit, 1, 1)

        layout.addWidget(QLabel("Width:"), 2, 0)
        layout.addWidget(self.w_rect_edit, 2, 1)

        layout.addWidget(QLabel("Height:"), 3, 0)
        layout.addWidget(self.h_rect_edit, 3, 1)
        
        layout.addWidget(QLabel("Rotation (deg):"), 4, 0)
        layout.addWidget(self.r_rect_edit, 4, 1)

        layout.setColumnStretch(2, 1)
        return widget

    def _create_polygon_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Polygon tab content goes here"))
        layout.addStretch()
        return widget

    def _create_ellipse_tab(self) -> QWidget:
        widget = QWidget()
        layout = QGridLayout(widget)
        
        # Validator for numeric input
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)

        # Create labels + inputs
        self.x_ell_edit = QLineEdit("0")
        self.y_ell_edit = QLineEdit("0")
        self.w_ell_edit = QLineEdit("0")
        self.h_ell_edit = QLineEdit("0")
        self.r_ell_edit = QLineEdit("0")

        for edit in (self.x_ell_edit, self.y_ell_edit, self.w_ell_edit, self.h_ell_edit):
            edit.setValidator(validator)

        # Grid layout: label left, field right
        layout.addWidget(QLabel("X:"), 0, 0)
        layout.addWidget(self.x_ell_edit, 0, 1)

        layout.addWidget(QLabel("Y:"), 1, 0)
        layout.addWidget(self.y_ell_edit, 1, 1)

        layout.addWidget(QLabel("Width:"), 2, 0)
        layout.addWidget(self.w_ell_edit, 2, 1)

        layout.addWidget(QLabel("Height:"), 3, 0)
        layout.addWidget(self.h_ell_edit, 3, 1)
        
        layout.addWidget(QLabel("Rotation (deg):"), 4, 0)
        layout.addWidget(self.h_ell_edit, 4, 1)

        layout.setColumnStretch(2, 1)
        return widget

    def get_current_geometry_data(self) -> tuple[str, int, int, int, int, int]:
        if self.currentIndex() == 0:
            return ("Rectangle", int(self.x_rect_edit.text()), int(self.y_rect_edit.text()), int(self.w_rect_edit.text()), int(self.h_rect_edit.text()), int(self.r_rect_edit.text()))
        else:  # if self.currentIndex() == 0:
            return ("Oval", int(self.x_ell_edit.text()), int(self.y_ell_edit.text()), int(self.w_ell_edit.text()), int(self.h_ell_edit.text()), int(self.r_ell_edit.text()))
