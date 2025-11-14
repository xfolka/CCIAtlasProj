import os

from ccipy.atlas.cci_atlas_dom_model import CCIAtlasDomModel
from PySide6.QtCore import QObject, Slot
from PySide6.QtXml import QDomDocument

from CCIAtlasProj.atlas_geometry import AtlasGeometry
from CCIAtlasProj.atlas_region import AtlasRegion


class Controller(QObject):

    def __init__(self):
        self.atlas_model = CCIAtlasDomModel()

    @Slot(str, name="load_file")
    def load_file(self, file_name: str):

        doc = QDomDocument()
        file = open(file_name)
        doc.setContent(file.read())
        file.close()
        base_folder = os.path.dirname(file_name)
        self.atlas_model.load_from_dom(doc, base_folder)
        #self.projTreeView.setModel(self.projModel)

        #self.atlas_model.lo

    def get_atlas_model(self) -> None | CCIAtlasDomModel:
        return self.atlas_model

    def save_project(self, file_name: str) -> None:
        pass

    def create_new_region(self, geometry: AtlasGeometry) -> None:
        region : AtlasRegion = AtlasRegion(geometry)
        res = self.atlas_model.add_atlas_region(region.to_dom_node())
        if not res:
            print("Failed to add region to model")
