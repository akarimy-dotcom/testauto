"""
This module manages the Ares5 environment configuration loaded from an XML file.

Changelog:
[2.2.2] - 2025-11-04

Added methods:

- "checkIfDataIDisSigned": Check if a specific DataID has a signed data type

Modified methods:


[2.2.1] - 2025-10-03

Modified methods:

- _LoadDataPoint: Now the Name field is used as the reference for the name of the DataIDs, associated with the old DGTO naming convention present in Ares4. Previously, the 'Identifier' field was used.

2.2.0 2025-09-01
"""

__version__ = '2.2.2'
__author__ = 'Ruggeri Nicolò'

import re
import xml.etree.ElementTree as ET
from enum import Enum

# Lists of supported data types, used to understand how to Read/Write a specific DataPoint
DATA_TYPE_STANDARD = ['BOOL', 'FLOAT', 'INT16', 'UINT16', 'UINT32', 'UINT8']
DATA_TYPE_ARRAY = ['UINT8_FIXED_SIZE_ARRAY', 'UINT8_DYNAMIC_SIZE_ARRAY']
DATA_TYPE_STREAM = ['UINT8_STREAM']

# Identifier used to detect board-related category groups
ENV_BRD_IDENTIFIER = "BRD"


class DataTypeFunction(Enum):
    """
    Enum representing the type of a DataID.

    - DATA_TYPE_STANDARD: Standard scalar value.
    - DATA_TYPE_ARRAY: Fixed or dynamic size array.
    - DATA_TYPE_STREAM: Stream of values.
    """
    DATA_TYPE_STANDARD = 0
    DATA_TYPE_ARRAY = 1
    DATA_TYPE_STREAM = 2


class AccessType(Enum):
    """
    Enum representing access permissions for a DataID field.

    - READ_ONLY: Field can only be read.
    - READ_AND_WRITE: Field can be read and written.
    - WRITE_ONLY: Field can only be written.
    - DEFINED_AT_RUNTIME: Access type is determined by another field.
    - INHERIT_FROM_DATAINDEX: Access type is inherited from the DataIndex.
    """
    READ_ONLY = 0
    READ_AND_WRITE = 1
    WRITE_ONLY = 2
    DEFINED_AT_RUNTIME = 3  # defined by a specific field
    INHERIT_FROM_DATAINDEX = 4


def int_to_DATAID(data_id_int: int) -> str:
    """
    Converts an integer DataID to its string representation in DataType-DataIndex-Field format.

    :param data_id_int: Integer representation of the DataID. [int]
    :returns: String format of the DataID. [str]
    """

    field = data_id_int & 0xFF
    dindex = data_id_int & 0x1FFF00
    dindex = dindex >> 8
    dtype = data_id_int & 0xFFE00000
    dtype = dtype >> 21

    return f"{dtype}-{dindex}-{field}"


def DATAID_to_DGTO(data_id: str) -> str:
    """
    Converts a DataID (DataType-DataIndex-Field) string to DGTO format (Device-Group-Type-Occurrence).

    :param data_id: DataID in DataType-DataIndex-Field format. [str]
    :returns: DGTO formatted string. [str]
    """

    appo = data_id.split("-")

    dindex = int(appo[1])
    dtype = int(appo[0])

    T = dtype & 0x07
    O = dindex & 0x1F
    G = (dindex & 0x1E0) >> 5
    D = (dindex & 0x1E00) >> 9

    return f"{D}-{G}-{T}-{O}"


def DATAID_to_int(data_id: str) -> int:
    """
    Converts a DataID string to its integer representation.

    :param data_id: DataID in DataType-DataIndex-Field format. [str]
    :returns: Integer representation of the DataID. [int]
    """

    appo = data_id.split("-")

    field = int(appo[2])
    dindex = int(appo[1]) << 8
    dtype = int(appo[0]) << 21

    return field + dindex + dtype


def IsDataID(data_id: str) -> bool:
    """
      Validates the format of a DataID string.

      :param data_id: DataID string to validate. [str]
      :returns: True if valid, False otherwise. [bool]
      """

    pattern = r'^[0-9]\d*-[0-9]\d*-[0-9]\d*$'

    if re.match(pattern, data_id) is None:
        return False

    return True


class Ares5EnvError(Exception):
    """
      Custom exception class for errors related to Ares5 environment configuration.
    """
    pass


class Ares5Env:
    """
        Manages the Ares5 environment configuration loaded from an XML file.
        Provides access to DataID metadata, CZO mappings, and category group information.
    """

    _DataType = None  # DataType info, used to understand the type of the field to read/write
    _CategoryGroupIndex = None  # DataPoint present in every CategoryGroup
    _CategoryGroup = None  # CategoryGroup of all devices
    _DataPointName = None  # Dict with DataPointName as key and all values are the address of the DataPoint
    _DataPointId = None  # Dict with DataType-DataID as key and all values are the DataPoints names
    _CZOList = None  # Dict with all CZO as key and CZO name as value

    _CZO_OF_BOARDS = None  # List of CZO associated to Board
    _MAP_BOARDCZO_TO_CZO = None  # Map for the conversion from Board CZO to Device CZO


    def __init__(self, filepath: str):
        """
        Initializes the Ares5Env object and loads the environment configuration from the given XML file.

        :param filepath: Path to the Env.XML file. [str]
        """

        self.LoadEnv(filepath)


    """
        --------------- ENV RELATED FUNCTION ---------------
    """


    def LoadEnv(self, filepath: str):
        """
        Loads the environment configuration from the specified XML file.

        :param filepath: Path to the Env.XML file. [str]
        """
        tree = ET.parse(filepath)
        element = tree.getroot()

        self._LoadDataType(element)
        self._LoadDataPoint(element)
        self._LoadCategoryGroupIndex(element)
        self._LoadCategoryGroup(element)
        self._LoadBusCategory(element)
        print(f"Env of Ares5 loaded from {filepath}.")


    def _LoadDataPoint(self, element: ET.Element):

        """
        Loads DataPoint definitions from the XML element.

        :param element: Root XML element. [ET.Element]
        """

        data_n = {}
        data_d = {}

        datap = element.findall(".//DatapointCnf")

        if len(datap) != 1:
            raise Ares5EnvError("Error: Unable to locate 'DatapointCnf' in Env.XML. The file may be missing or "
                                "incorrectly formatted.")
        else:
            datap = datap[0]

        for CGI in datap.findall(".//Datapoint"):
            elem = CGI.findall(".//Desc")  # Previously was Identifier

            identifier = elem[0].text.strip()

            elem = CGI.findall(".//DatatypeIndex")
            data_type = elem[0].text.strip()

            elem = CGI.findall(".//DataIndex")
            data_index = elem[0].text.strip()

            id = f"{data_type}-{data_index}"

            data_n[identifier] = id
            data_d[id] = identifier

        self._DataPointName = data_n
        self._DataPointId = data_d


    def _LoadCategoryGroupIndex(self, element: ET.Element):
        """
        Loads CategoryGroupIndex mappings from the XML element.

        :param element: Root XML element. [ET.Element]
        """

        data = {}

        for CGI in element.findall(".//DatapointMapping"):
            elem = CGI.findall(".//CategoryGroupIndex")
            str_czo = elem[0].text.strip()
            czo = hex(int(str_czo))

            elem = CGI.findall(".//DatatypeIndex")
            data_type = elem[0].text.strip()

            elem = CGI.findall(".//DataIndex")
            data_index = elem[0].text.strip()

            if czo not in data.keys():
                data[czo] = []

            data[czo].append(f"{data_type}-{data_index}")

        self._CategoryGroupIndex = data


    def _LoadCategoryGroup(self, element: ET.Element):
        """
        Loads CategoryGroup definitions and sets board-to-CZO mappings.

        :param element: Root XML element. [ET.Element]
        """

        CategoryGroup = []

        for CGI in element.findall(".//CategoryGroup"):
            elem = CGI.findall(".//Desc")
            desc = elem[0].text.strip()

            elem = CGI.findall(".//Label")
            label = elem[0].text.strip()

            elem = CGI.findall(".//Index")
            index = int(elem[0].text)

            CategoryGroup.append({
                'index':       index,
                'description': desc,
                'label':       label
            })

        self._SetBoardToCZOMap(CategoryGroup)
        self._CategoryGroup = CategoryGroup


    def _LoadBusCategory(self, element: ET.Element):
        """
          Loads BusCategory definitions and builds the list of valid CZOs.

          :param element: Root XML element. [ET.Element]
        """

        CZO_List = []

        datap = element.findall(".//BusCategories")

        if len(datap) != 1:
            raise Ares5EnvError("Error: Unable to locate 'BusCategories' in Env.XML. The file may be missing or "
                                "incorrectly formatted.")
        else:
            datap = datap[0]

        for CAT in datap.findall(".//Category"):
            elem = CAT.findall(".//Desc")
            desc = elem[0].text.strip()

            elem = CAT.findall(".//AbsoluteCategoryIndex")
            index = int(elem[0].text)

            for PAIRS in CAT.findall(".//ZoneOccurrencePair"):
                elem = PAIRS.findall(".//Zone")
                zone = int(elem[0].text)

                elem = PAIRS.findall(".//Occurrence")
                occ = int(elem[0].text)

                czo = (index << 16)
                czo = czo + (zone << 8)
                czo = czo + occ

                CZO_List.append(czo)

        self._CZOList = CZO_List


    def _LoadDataType(self, element: ET.Element):
        """
           Loads DataType definitions and field metadata from the XML element.

           :param element: Root XML element. [ET.Element]
        """

        data_type_data = []

        for DT in element.findall(".//Datatype"):
            elem = DT.findall(".//Index")
            index = elem[0].text.strip()

            elem = DT.findall(".//Desc")
            description = elem[0].text.strip()

            elem = DT.findall(".//ReleasedFields")
            released_fields = elem[0].text.strip()

            elem = DT.findall(".//ValueFieldIndex")
            value_field_index = elem[0].text.strip()

            elem = DT.findall(".//Field0Meaning")
            field_0_meaning = elem[0].text.strip()

            elem = DT.findall(".//Identifier")
            identifier = elem[0].text.strip()

            fields_data = []
            for field in DT.findall(".//Field"):
                elem = field.findall(".//Index")
                field_index = elem[0].text.strip()

                elem = field.findall(".//Desc")
                field_desc = elem[0].text.strip()

                elem = field.findall(".//Identifier")
                field_identifier = elem[0].text.strip()

                elem = field.findall(".//Type")
                field_type = elem[0].text.strip()

                elem = field.findall(".//NumberOfElements")
                if len(elem) > 0:
                    field_number_of_elements = elem[0].text.strip()
                else:
                    field_number_of_elements = None

                elem = field.findall(".//AccessType")
                field_access_type = AccessType(int(elem[0].text))

                elem = field.findall(".//AccessTypeFieldIndex")
                if len(elem) > 0:
                    field_access_type_field = int(elem[0].text)
                else:
                    field_access_type_field = None

                elem = field.findall(".//MeasureUnitIndex")
                if len(elem) > 0:
                    field_measure_unit_index = elem[0].text.strip()
                else:
                    field_measure_unit_index = None

                fields_data.append({
                    'index':                        field_index,
                    'desc':                         field_desc,
                    'identifier':                   field_identifier,
                    'type':                         field_type,
                    'number_of_elements':           field_number_of_elements,
                    'access_type':                  field_access_type,
                    # index of AccessType Field if AccessType = 3 (DefinedAtRuntime)
                    'field_access_type_fieldindex': field_access_type_field,
                    'measure_unit_index':           field_measure_unit_index,
                })

            data_type_data.append({
                'index':             index,
                'description':       description,
                'released_fields':   released_fields,
                'value_field_index': value_field_index,
                'field_0_meaning':   field_0_meaning,
                'identifier':        identifier,
                'fields':            fields_data
            })

        self._DataType = data_type_data


    """
        --------------- Data FUNCTION ---------------
    """


    def _SetBoardToCZOMap(self, category_group):
        """
        Sets up mappings between board CZOs and device CZOs based on category group labels.

        :param category_group: List of category group dictionaries. [list[dict]]
        """

        czo_boards = []
        map_board_czo = {}

        for cat in category_group:
            if ENV_BRD_IDENTIFIER in cat['label']:
                czo_boards.append(cat['index'])

                for cat2 in category_group:
                    if cat2['label'] in cat['label'] and cat2['label'] != cat['label']:
                        map_board_czo[cat['index']] = (cat2['index'] << 16)

        self._CZO_OF_BOARDS = czo_boards
        self._MAP_BOARDCZO_TO_CZO = map_board_czo


    def GetDataIdDataTypeFieldInfo(self, DataID: str) -> tuple[DataTypeFunction, int, str, AccessType]:
        """
        Retrieves the DataType, length, identifier, and access type for a given DataID.

        :param DataID: DataID string in DataType-DataIndex-Field format. [str]
        :returns: Tuple containing:
            - DataTypeFunction: Type of the DataID.
            - int: Length or number of elements.
            - str: Identifier of the field.
            - AccessType: Access permission type.
        :raises Ares5EnvError: If the DataID is not found or invalid.
        """

        dtype = None
        leng = None
        identifier = None
        access_type = None
        found = False
        try:
            DataID_type = DataID.split("-")[0]
            DataID_field = int(DataID.split("-")[2])

            for dtl in self._DataType:
                if dtl['index'] == DataID_type:
                    if dtl['fields'][DataID_field]['number_of_elements'] is not None:
                        leng = int(dtl['fields'][DataID_field]['number_of_elements'])
                    dtype = dtl['fields'][DataID_field]['type']
                    identifier = dtl['fields'][DataID_field]['identifier']
                    access_type = dtl['fields'][DataID_field]['access_type']

                    if dtype in DATA_TYPE_STANDARD:
                        dtype = 0
                        leng = 1
                    elif dtype in DATA_TYPE_ARRAY:
                        dtype = 1
                    elif dtype in DATA_TYPE_STREAM:
                        dtype = 2
                        leng = 0

                    dtype = DataTypeFunction(dtype)
                    found = True
                    break
        except Exception as e:
            print(f"Error during GetDataIdDataTypeFieldInfo: {e}")

        if not found:
            raise Ares5EnvError(f"ERROR! Impossible to get the DataType of DataID {DataID}:")

        return dtype, leng, identifier, access_type


    def CheckIfCZOisValid(self, CZO: int) -> bool:
        """
        Checks if the given CZO is valid according to the loaded environment.

        :param CZO: CZO address to validate. [int]
        :returns: True if valid, False otherwise. [bool]
        """

        return CZO in self._CZOList


    def CheckIfCZOisBoard(self, CZO: int) -> bool:
        """
        Determines if the given CZO corresponds to a board.

        :param CZO: CZO address to check. [int]
        :returns: True if it's a board CZO, False otherwise. [bool]
        """

        c_raw = CZO & 0xFFFF0000
        c = c_raw >> 16

        return c in self._CZO_OF_BOARDS


    def GetCZOLabel(self, CZO: int) -> tuple[str, str]:
        """
        Retrieves the label associated with a given CZO.

        :param CZO: CZO address. [int]
        :returns: Label string if found, otherwise None. [str]
        """

        c_raw = CZO & 0xFFFF0000
        c = c_raw >> 16

        label = None

        for category in self._CategoryGroup:
            if category['index'] == c:
                label = category['label']

        return label


    def BoardCZOToDeviceCZO(self, CZO: int) -> int:
        """
        Converts a board CZO to its corresponding device CZO.

        :param CZO: Board CZO address. [int]
        :returns: Device CZO address. [int]
        """

        c_raw = CZO & 0xFFFF0000
        c = c_raw >> 16

        try:
            new_czo = (self._MAP_BOARDCZO_TO_CZO[c]) + (CZO & 0x0000FFFF)
        except:
            print(f"WARNING!\nThe CZO: {CZO:08x} is not a Board CZO.\nThe item will remain in its original format!")
            new_czo = CZO

        return new_czo


    def GetDataIDFromName(self, identifier: str):
        """
        Retrieves the DataID string corresponding to a given DataPoint name.

        :param identifier: Name of the DataID. [str]
        :returns: DataID string if found in format DataType-DataIndex-Field, otherwise None. [str]
        """

        result = None

        if identifier in self._DataPointName.keys():
            result = self._DataPointName[identifier]

        return result


    def GetDataNameFromID(self, identifier: str):
        """
        Retrieves the DataPoint name corresponding to a given DataID string.

        :param identifier: DataID string in DataType-DataIndex-Field format. [str]
        :returns: DataPoint name if found, otherwise None. [str]
        """

        result = None

        if IsDataID(identifier):
            appo = identifier.split("-")
            data = f"{appo[0]}-{appo[1]}"
            if data in self._DataPointId.keys():
                result = self._DataPointId[data]
        else:
            print("WARNING! Impossible to get DataID Name from an incomplete DataID.")

        return result


    def checkIfDataIDisSigned(self, DataID) -> bool:
        """
        Check if a specific DataID has a signed type data or not.

        :param DataID: DataID string in DataType-DataIndex-Field format. [str]
        :returns: True if is signed, otherwise False.
        """

        isSigned = False
        found = False
        try:
            DataID_type = DataID.split("-")[0]
            DataID_field = int(DataID.split("-")[2])

            for dtl in self._DataType:
                if dtl['index'] == DataID_type:
                    if dtl['fields'][DataID_field]['number_of_elements'] is not None:
                        leng = int(dtl['fields'][DataID_field]['number_of_elements'])
                    dtype = dtl['fields'][DataID_field]['d_type']

                    if dtype == "INT16":
                        isSigned = True

                    found = True
                    break
        except Exception as e:
            print(f"Error during GetDataIdDataTypeFieldInfo: {e}")

        if not found:
            raise Ares5EnvError(f"ERROR! Impossible to get the DataType of DataID {DataID}:")

        return isSigned