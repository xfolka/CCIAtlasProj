from ccipy.atlas.cci_atlas_xml_model import CCIAtlasXmlItem
from PySide6.QtGui import QTransform
import math


class AtlasTransform():
    
    def __init__(self, item: CCIAtlasXmlItem):
        if item.get_node_name() != "ParentTransform":
            raise ValueError("Wrong node")
        
        for cn in range(item.get_nr_of_children()):
            c = item.child(cn)
            match c.get_node_name():
                case "M11":
                    self.m11 = float(c.get_node_text())
                case "M12":
                    self.m12 = float(c.get_node_text())
                case "M13":
                    self.m13 = float(c.get_node_text())
                case "M14":
                    self.m14 = float(c.get_node_text())
                case "M21":
                    self.m21 = float(c.get_node_text())
                case "M22":
                    self.m22 = float(c.get_node_text())
                case "M23":
                    self.m23 = float(c.get_node_text())
                case "M24":
                    self.m24 = float(c.get_node_text())
                case "M31":
                    self.m31 = float(c.get_node_text())
                case "M32":
                    self.m32 = float(c.get_node_text())
                case "M33":
                    self.m33 = float(c.get_node_text())
                case "M34":
                    self.m34 = float(c.get_node_text())
                case "M41":
                    self.m41 = float(c.get_node_text())
                case "M42":
                    self.m42 = float(c.get_node_text())
                case "M43":
                    self.m43 = float(c.get_node_text())
                case "M44":
                    self.m44 = float(c.get_node_text())
                    
    def get_actual_scale(self):
        sx = math.hypot(self.m11, self.m12)
        sy = math.hypot(self.m21, self.m22)
        return sx, sy

    def center_to_bottom_left(self, width, height):
        m11, m12 = self.m11, self.m12
        m21, m22 = self.m21, self.m22
        tx, ty = self.m41, self.m42

        vx = 0  # -width / 2.0
        vy = 0

        ux_x, ux_y = m11 / width, m12 / width
        uy_x, uy_y = m21 / height, m22 / height

        # apply ONLY linear part (ignore translation)
        dx = ux_x * vx + uy_x * vy
        dy = ux_y * vx + uy_y * vy

        
        #self.m41 = tx + dx
        #self.m42 = ty + dy
        return QTransform(1, 0, 0, 1, tx + dx, ty + dy)

    def to_qtransform(self) -> QTransform:

        a = self.m11  # M11
        b = self.m12  # M12
        c = self.m21  # M21
        d = self.m22  # M22
        tx = self.m41  # M41
        ty = self.m42  # M42

        return QTransform(a, b, c, d, tx, ty)
