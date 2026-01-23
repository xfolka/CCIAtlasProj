import os
from importlib.resources import files
from pathlib import Path, PureWindowsPath

from ccipy.atlas.cci_atlas_dom_model import CCIAtlasDomModel
from ccipy.atlas.cci_atlas_protocol_model import CCIAtlasProtocolModel

from PySide6.QtCore import QObject, Slot, QModelIndex
from PySide6.QtXml import QDomDocument
from PySide6.QtGui import QImage, QTransform

from cci_atlas_proj import data
from cci_atlas_proj.atlas_geometry import AtlasGeometry
from cci_atlas_proj.atlas_region import AtlasRegion
from cci_atlas_proj.atlas_transform import AtlasTransform
from cci_atlas_proj.atlas_region_factory import create_atlas_regions
from cci_atlas_proj.image_loader import load_image


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

    def load_image_from_index(self, index: QModelIndex) -> tuple[QImage, QTransform] | None:
        index_tag_name = self.atlas_model.data(index)
        if index_tag_name != "PlaceableImage":
            return None
        
        img_path: PureWindowsPath = PureWindowsPath(self.atlas_model.data_by_index_and_column(self.atlas_model.find_index_by_name("FileName", parent=index), 1))
        img_file_name = img_path.name
        new_img_path = self.atlas_model.get_imported_folder() / img_file_name
        img = load_image(new_img_path)
        
        transform_idx = self.atlas_model.find_index_by_name("ParentTransform", parent=index)
        transform_item = self.atlas_model.get_item(transform_idx)
        atlas_transform = AtlasTransform(transform_item)
        
        img_width_proj, img_height_proj = atlas_transform.get_actual_scale()
        tb_trans = atlas_transform.center_to_bottom_left(img_width_proj, img_height_proj)
        
        img_w_idx = self.atlas_model.find_index_by_name("Width", index)
        image_width = int(self.atlas_model.data_by_index_and_column(img_w_idx, 1))
        img_h_idx = self.atlas_model.find_index_by_name("Height", index)
        image_height = int(self.atlas_model.data_by_index_and_column(img_h_idx, 1))

        clx_idx = self.atlas_model.find_index_by_name("CenterLocalX", index)
        cly_idx = self.atlas_model.find_index_by_name("CenterLocalY", index)
        center_local_x = float(self.atlas_model.data_by_index_and_column(clx_idx, 1))
        center_local_y = float(self.atlas_model.data_by_index_and_column(cly_idx, 1))
        
        #scale image to [0,1] interval
        scale: QTransform = QTransform()
        scale.scale(1 / image_width, 1 / image_height)

        pivot = QTransform()
        pivot.translate(center_local_x, center_local_y)
        
        flip_y: QTransform = QTransform()
        flip_y.scale(1, -1)
        
        pivot_inv, ok = pivot.inverted()
        if not ok:
            raise ValueError("Pivot transform not invertible")
        tot_trans = atlas_transform.to_qtransform() * scale * pivot * tb_trans * pivot_inv
#        tot_trans = atlas_transform.to_qtransform() * pivot * scale * tb_trans * flip_y * pivot_inv
        
        return img, tot_trans
    
    def get_atlas_regions(self) -> list[AtlasRegion]:
        return create_atlas_regions(self.atlas_model)
        
    def save_dom_to_file(self, file_path: str):
        str_path = file_path
        path = Path(str_path)
        if path.suffix != ".a5proj":
            str_path += ".a5proj"
        path = Path(str_path)
            
        self.atlas_model.update_name(path.name)
        file = open(str_path, "w")
        file.write(self.atlas_model.get_document().toString(indent=2))
        file.close()

    def get_atlas_model(self) -> None | CCIAtlasDomModel:
        return self.atlas_model

    def get_protocols_model(self) -> None | CCIAtlasProtocolModel:
        return self.protocols_model

    def create_new_region(self, geometry: AtlasGeometry, protocol_uid: str, x_trans, y_trans, rot) -> None:
        region: AtlasRegion = AtlasRegion(geometry, protocol_uid)
        region.set_translation(x_trans, y_trans)
        region.set_rotation(rot)
        res = self.atlas_model.add_atlas_region(region.to_dom_node())
        if not res:
            print("Failed to add region to model")
            
        #get the protocol node by uid
        proto_node = self.protocols_model.get_protocol_node_by_uid(protocol_uid)
        if proto_node is None:
            print("Failed to find protocol node by UID")
            return
        
        self.atlas_model.add_protocol(proto_node)
