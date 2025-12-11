"""
<AtlasRegion>
  <CreatedIndex>2</CreatedIndex> this needs to be looked up probably
  <CustomName>false</CustomName>
  <Name>Region 2</Name> give this a namoe of our own? like "cci generated region 3"
  <UID>1873110719</UID>
  <ParentTransform>
    <M11>1</M11>
    <M12>0</M12>
    <M13>0</M13>
    <M14>0</M14>
    <M21>0</M21>
    <M22>1</M22>
    <M23>0</M23>
    <M24>0</M24>
    <M31>0</M31>
    <M32>0</M32>
    <M33>1</M33>
    <M34>0</M34>
    <M41>-868.615295410156</M41>
    <M42>15483.775390625</M42>
    <M43>0</M43>
    <M44>1</M44>
    <CenterLocalX>0</CenterLocalX>
    <CenterLocalY>0</CenterLocalY>
  </ParentTransform>
  <IsVisible>true</IsVisible>
  <DefaultAlignment>
    <ParentTransform>
      <M11>1</M11>
      <M12>0</M12>
      <M13>0</M13>
      <M14>0</M14>
      <M21>0</M21>
      <M22>1</M22>
      <M23>0</M23>
      <M24>0</M24>
      <M31>0</M31>
      <M32>0</M32>
      <M33>1</M33>
      <M34>0</M34>
      <M41>0</M41>
      <M42>0</M42>
      <M43>0</M43>
      <M44>1</M44>
      <CenterLocalX>0</CenterLocalX>
      <CenterLocalY>0</CenterLocalY>
    </ParentTransform>
  </DefaultAlignment>
  <MinZ>0</MinZ>
  <MaxZ>0</MaxZ>
  <Geometry> these should be implemented as classes... generated xml should be able to simply be put in in the project structure
    <Type>Oval</Type>
    <Center>
      <X>0</X>
      <Y>0</Y>
    </Center>
    <Size>
      <X>1886.86346435547</X>
      <Y>1834.08227539062</Y>
    </Size>
  </Geometry>
  <RotationCentre>
    <X>0</X>
    <Y>0</Y>
  </RotationCentre>
  <LinkUID>825902018</LinkUID>
  <GeometryAcquired>false</GeometryAcquired>
  <SectionIndex>2</SectionIndex>
  <AcquisitionSpec>  this is a bit unclear to me what it actually is atm... ask fibics?
    <Name>Acquisition Spec 3</Name>
    <UID>825902018</UID>
    <PlaceableDataUID>-1</PlaceableDataUID>
    <AcquisitionTypeEnum>ForAcquisition</AcquisitionTypeEnum>
    <AcquisitionDataTypeEnum>2DData</AcquisitionDataTypeEnum>
    <AcquisitionStateEnum>Fresh</AcquisitionStateEnum>
    <AcquisitionMode>Mosaic</AcquisitionMode>
    <WorkingProtocolUID>1508866406</WorkingProtocolUID> this should also be asked to fibics i think...does all atlasregions need a workingprotocoluid?
  </AcquisitionSpec>
</AtlasRegion>
"""

import uuid
from importlib.resources import files

from PySide6.QtXml import QDomDocument, QDomNode

from cci_atlas_proj import data
from cci_atlas_proj.atlas_geometry import AtlasGeometry


def generate_uuid_decimal() -> int:
  
    # Generate a UUID (128 bits of entropy)
    u = uuid.uuid4()

    # Get the raw 16 bytes
    raw = u.bytes

    # Convert bytes → big integer (unsigned, big-endian)
    num = int.from_bytes(raw, byteorder="big", signed=False)

    #print("UUID:", u)
    #print("As decimal:", num)
    return num
  

class AtlasRegion:

    DATAFILENAME: str = "atlas_region.xml"
    CREATED_INDEX_CNT: int = 1

    def __init__(self, geometry: AtlasGeometry, protocol_uid: str, name: str | None = None):

        self.dom_document: QDomDocument = QDomDocument()
        file = open(files(data) / self.DATAFILENAME)
        self.dom_document.setContent(file.read())
        self.root_element = self.dom_document.documentElement()
        file.close()

        new_uid = str(generate_uuid_decimal())[0:10]
        uid_nodes = self.root_element.elementsByTagName("UID")
        if uid_nodes.count() > 0:
            uid_node = uid_nodes.item(0)
            uid_node.firstChild().setNodeValue(new_uid)

        if name is not None:
            self.set_name(name)
        else:
            self.set_name(f"CCI Generated Region {new_uid[0:4]}")

            self.set_created_index(self.CREATED_INDEX_CNT)
            AtlasRegion.CREATED_INDEX_CNT += 1

        self.geometry: AtlasGeometry = geometry
        g_node = geometry.to_dom_node()
        self.root_element.appendChild(g_node)
        self.set_working_protocol_uid(protocol_uid)

    def set_name(self, name: str):
        name_nodes = self.root_element.elementsByTagName("Name")
        if name_nodes.count() > 0:
            name_node = name_nodes.item(0)
            name_node.firstChild().setNodeValue(name)
            
    def set_working_protocol_uid(self, protocol_uid: str):
        protocol_nodes = self.root_element.elementsByTagName("WorkingProtocolUID")
        if protocol_nodes.count() > 0:
            protocol_node = protocol_nodes.item(0)
            protocol_node.firstChild().setNodeValue(protocol_uid)

    def set_created_index(self, index: int):
        ci_nodes = self.root_element.elementsByTagName("CreatedIndex")
        if ci_nodes.count() > 0:
            ci_node = ci_nodes.item(0)
            ci_node.firstChild().setNodeValue(str(index))

    # def save_to_file(self, file_path: Path):
    #     file = open(file_path, "w")
    #     file.write(self.dom_document.toString(indent=2))
    #     file.close()

    def to_dom_node(self) -> QDomNode:
        return self.root_element
