from enum import Enum

from PySide6.QtXml import QDomElement, QDomNode, QDomText, QDomDocument
from ccipy.atlas.cci_atlas_xml_model import CCIAtlasXmlItem


class AtlasGeometryType(Enum):
    RECTANGLE = "Rectangle"
    OVAL = "Oval"
    POLYGON = "Polygon"


#   <Geometry> these should be implemented as classes... generated xml should be able to simply be put in in the project structure
#     <Type>Oval</Type>
#     <Center>
#       <X>0</X> it makes sense that these are 0 if the matrix above is a translation
#       <Y>0</Y>
#     </Center>
#     <Size>
#       <X>1886.86346435547</X>
#       <Y>1834.08227539062</Y>
#     </Size>
#   </Geometry>


class AtlasGeometry:
    NODENAME: str = "Geometry"
    TYPENODENAME: str = "Type"

    def __init__(self, type: AtlasGeometryType, dom_doc: QDomDocument):
        self.type: AtlasGeometryType = type
        self.dom_doc: QDomDocument = dom_doc

    def to_dom_node(self) -> QDomNode:
        qde_geom: QDomElement = self.dom_doc.createElement(AtlasGeometry.NODENAME)
        qde_type: QDomElement = self.dom_doc.createElement(AtlasGeometry.TYPENODENAME)
        qte_type_name: QDomText = self.dom_doc.createTextNode(str(self.type.value))

        qde_type.appendChild(qte_type_name)
        qde_geom.appendChild(qde_type)

        return qde_geom


class AtlasSimpleGeom(AtlasGeometry):
    CENTERNAME = "Center"
    SIZENAME = "Size"

    def __init__(self, type: AtlasGeometryType, dom_doc: QDomDocument):
        super().__init__(type, dom_doc)
        self.center_x: float = 0
        self.center_x: float = 0
        self.width: float = 0
        self.height: float = 0

    def set(self, x: float, y: float, w: float, h: float):
        self.center_x = x
        self.center_y = y
        self.width = w
        self.height = h
        
    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height

    def _get_dom_from_data(self, tag_name: str, x: float, y: float) -> QDomNode:
        qde_root: QDomElement = self.dom_doc.createElement(tag_name)
        qde_x: QDomElement = self.dom_doc.createElement("X")
        qte_x: QDomText = self.dom_doc.createTextNode(str(x))
        qde_x.appendChild(qte_x)

        qde_y: QDomElement = self.dom_doc.createElement("Y")
        qte_y: QDomText = self.dom_doc.createTextNode(str(y))
        qde_y.appendChild(qte_y)

        qde_root.appendChild(qde_x)
        qde_root.appendChild(qde_y)

        return qde_root

    def to_dom_node(self) -> QDomNode:
        root = super().to_dom_node()
        qde_center: QDomNode = self._get_dom_from_data(self.CENTERNAME, self.center_x, self.center_y)
        root.appendChild(qde_center)

        qde_size: QDomNode = self._get_dom_from_data(self.SIZENAME, self.width, self.height)

        root.appendChild(qde_size)
        return root


class AtlasRectangle(AtlasSimpleGeom):
    def __init__(self, x: float, y: float, w: float, h: float, dom_doc: QDomDocument):
        super().__init__(AtlasGeometryType.RECTANGLE, dom_doc)
        self.set(x, y, w, h)


class AtlasOval(AtlasSimpleGeom):
    def __init__(self, x: float, y: float, w: float, h: float, dom_doc: QDomDocument):
        super().__init__(AtlasGeometryType.OVAL, dom_doc)
        self.set(x, y, w, h)


class AtlasPolygon(AtlasGeometry):
    def __init__(self, vertices: list[tuple[float, float]], dom_doc: QDomDocument):
        super().__init__(AtlasGeometryType.POLYGON, dom_doc)
        self.vertices = vertices


def create_geometry(item: CCIAtlasXmlItem, doc: QDomDocument) -> AtlasGeometry | None:
    if item.get_node_name() != "Geometry":
        raise ValueError("Not a Geometry node")
    
    t = ""
    x = 0
    y = 0
    w = 0
    h = 0
    for cn in range(item.get_nr_of_children()):
        child = item.child(cn)
        match child.get_node_name():
            case "Type":
                t = child.get_node_text()
            case "Center":
                x = float(child.child(0).get_node_text())
                y = float(child.child(1).get_node_text())
            case "Size":
                w = float(child.child(0).get_node_text())
                h = float(child.child(1).get_node_text())
                
    match t:
        case "Rectangle":
            return AtlasRectangle(x, y, w, h, doc)
        # case Oval:
            #     return 
            # case Polygon
        case _:
            return None
