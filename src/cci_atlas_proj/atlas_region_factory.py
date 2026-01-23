# from typing import list
from PySide6.QtXml import QDomDocument
from cci_atlas_proj.atlas_region import AtlasRegion
from cci_atlas_proj.atlas_geometry import AtlasGeometry
from ccipy.atlas.cci_atlas_dom_model import CCIAtlasDomModel


def create_atlas_regions(atlas_model: CCIAtlasDomModel) -> list[AtlasRegion]:

    atlas_regions = atlas_model.get_atlas_region_indices()
    region_list = []
    dom_doc = atlas_model.get_document()

    for region in atlas_regions:
        region_item = atlas_model.get_item(region)
        region: AtlasRegion = AtlasRegion(region_item, dom_doc)
        region_list.append(region)
    
    return region_list
