import os
from importlib.resources import files
from pathlib import Path

from ccipy.atlas.cci_atlas_dom_model import CCIAtlasDomModel
from ccipy.atlas.cci_atlas_protocol_model import CCIAtlasProtocolModel
from PySide6.QtCore import QObject, Slot
from PySide6.QtXml import QDomDocument

from cci_atlas_proj import data
from cci_atlas_proj.atlas_geometry import AtlasGeometry
from cci_atlas_proj.atlas_region import AtlasRegion


class Controller(QObject):

    def __init__(self):
        self.atlas_model = CCIAtlasDomModel()
        self.protocols_model = CCIAtlasProtocolModel()
        doc = self.load_file_to_dom(files(data) / "Protocols-V1.0.xml")
        self.protocols_model.load_from_dom(doc)

    def load_file_to_dom(self, file_name: str) -> QDomDocument:
        doc = QDomDocument()
        file = open(file_name)
        doc.setContent(file.read())
        file.close()
        return doc

    @Slot(str, name="load_file")
    def load_file(self, file_name: str):

        doc = self.load_file_to_dom(file_name)
        base_folder = os.path.dirname(file_name)
        self.atlas_model.load_from_dom(doc, base_folder)
        #self.projTreeView.setModel(self.projModel)

        #self.atlas_model.lo

    def save_dom_to_file(self, file_path: str):
        str_path = file_path
        path = Path(str_path)
        if path.suffix != ".a5proj":
            str_path += ".a5proj"
            
        file = open(str_path, "w")
        file.write(self.atlas_model.get_document().toString(indent=2))
        file.close()

    def get_atlas_model(self) -> None | CCIAtlasDomModel:
        return self.atlas_model

    def get_protocols_model(self) -> None | CCIAtlasProtocolModel:
        return self.protocols_model

    def create_new_region(self, geometry: AtlasGeometry, protocol_uid: str) -> None:
        region: AtlasRegion = AtlasRegion(geometry, protocol_uid)
        res = self.atlas_model.add_atlas_region(region.to_dom_node())
        if not res:
            print("Failed to add region to model")
            
        #get the protocol node by uid
        proto_node = self.protocols_model.get_protocol_node_by_uid(protocol_uid)
        if proto_node is None:
            print("Failed to find protocol node by UID")
            return
        
        self.atlas_model.add_protocol(proto_node)
