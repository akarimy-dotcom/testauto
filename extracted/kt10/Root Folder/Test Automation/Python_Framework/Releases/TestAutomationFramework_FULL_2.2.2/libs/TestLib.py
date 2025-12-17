__version__ = '2.2.2'
__author__ = 'Juan Pablo Perruzza & Intelligentia SRL, Ruggeri Nicolò'

"""
Changelog:
[2.2.2] - 2025-11-04

# Ares4 #:
- Added private attribute "_fwprj" (istance of new class FWPRJ) to manage .fwprj files. Ticket: #54

Modified methods: 

- "__init__": Added new management of _fwprj from configs. Ticket: #54
- "_search_dgto": Added management of _fwprj (DGTO will be searched in .fwprj). Ticket: #54
- "_search_phantom" Added management of _fwprj (Phantom DGTO will be searched in .fwprj). Ticket: #54
- "_writeBroadcastDGTOonEbus": Fixed packet value calculation

Added methods:

- "dfls_download": Added method to download dfls files in the target device


# Ares5 #:
Renamed methods:

- "read_DataIdFromCZO": renamed to read_DataId
- "read_DataIdListFromCZO": renamed to read_DataIdList
- "write_DataIdToCZO": renamed to write_DataId
- "write_DataIdListToCZO": renamed to write_DataIdList

Modified methods:

- "write_DataId": added management of probe writings for Ares5 devices
- "_write_probe": added better management of ADC index (needed to allow writings of negative value in probes for Ares5 devices)
- "ReadTDA": Fixed in case of reading an empty TDA in Ares5 devices
- "read_DataId": added gesture of negative value for Int32 datatype


Added methods:

- "read_DataIdFromBoard": New method to read a DataID from board using Handle instead of CZO
- "write_DataIdToBoard" New method to write a DataID from board using Handle instead of CZO

- "_read_DataIdsStandardFromBoard": needed for implementation of method read_DataIdFromBoard
- "_read_DataIdArrayFromBoard": needed for implementation of method read_DataIdFromBoard
- "_read_DataIdStreamSizeFromBoard": needed for implementation of method read_DataIdFromBoard
- "_read_DataIdStreamFromBoard": needed for implementation of method read_DataIdFromBoard

- "_write_DataIdsStandardToBoard": needed for implementation of method write_DataIdToBoard
- "_write_DataIdArrayToBoard": needed for implementation of method write_DataIdToBoard
- "_write_DataIdStreamToBoard": needed for implementation of method write_DataIdToBoard

Changelog:
[2.2.1] - 2025-10-03

Modified methods: 

Added exception handling to fix the crash caused by the lack of error management in the ATG protocol present in the MTSTestLib DLL (module: pymtstestlib) Ver. 00.05.00 for the following methods:

- _read_DataIdsStandard
- _read_DataIdArray
- _read_DataIdStream
- _read_DataIdStreamSize
- _write_DataIdsStandard
- _write_DataIdArray
- _write_DataIdStream


[2.2.0] - 2025-09-05

Added classes:

- Ares5Error: added class to generate exception when Ares5 related methods are called before _ares5_env are initialized or when Ares5 method fails.

Added class attributes:

- _ares5_env: contains the instance of Ares5Env to manages the Ares5 environment configuration loaded from an XML file

Modified methods: 

- __init__: added loading of Ares5Env if Ares5EnvSourcePath settings is configured.
- _write_phantom_dgto: now reading operation after write will not generate any comment if everything is ok (aligned to other write methods)
- write_dgto: now is possible to specify Category, Zone and Occurrence even for Phantom DGTO
- multiwrite_dgto: Ticket #56, now the method use the check time taken from Config.txt
- multiwrite_dgto: now a warning will be triggered if the method try to write Probe DGTO
- write_memory: now is possible to specify Category, Zone and Occurrence of the target device
- operation_control_set: added print of error in report if command fails

Added methods:

- multiread_dgto: Ticket #56, added method to read multiple DGTO at once with only one command
- operation_control_get: Ticket #56, added method to get information from OperationControlGet commands

- _searchDataIDInfo: new Ares5 method for DataID management, uses the Ares5Env object to retrieve information about the specified DataID.
- _searchCZOInfo:  new Ares5 method for DataID management, uses the Ares5Env object to retrieve information about the specified CZO.
- read_DataId:  new Ares5 method for DataID management, reads a DataID using either its name and field or its code and address.
- read_DataIdList:  new Ares5 method for DataID management, reads multiple DataIDs of type Standard using either their names and fields or their codes.
- write_DataId:  new Ares5 method for DataID management, writes a value to a DataID using either its name and field or its code and address.
- write_DataIdList:  new Ares5 method for DataID management, writes multiple DataIDs of type Standard using either their names and fields or their codes.
- _read_DataIdsStandard:  new Ares5 method for DataID management, reads multiple Standard DataType DataIDs from the specified CZO.
- _read_DataIdArray:  new Ares5 method for DataID management, reads an Array DataType DataID from the specified CZO.
- _read_DataIdStream:  new Ares5 method for DataID management, reads a DataType Stream DataID from the specified CZO with optional offset.
- _read_DataIdStreamSize:  new Ares5 method for DataID management, retrieves the size of a Stream DataID from the specified CZO.
- _write_DataIdsStandard:  new Ares5 method for DataID management, writes values to multiple Standard DataIDs on the specified CZO.
- _write_DataIdArray:  new Ares5 method for DataID management, writes values to an Array DataID on the specified CZO.
- _write_DataIdStream:  new Ares5 method for DataID management, writes values to a Stream DataID on the specified CZO with optional offset.

[2.1.1] - 2025-05-09

Modified methods:

- set_channel_values: #55 changed call of _operation_control_set to operation_control_set
- save_channel_values: #55 changed call of _operation_control_set to operation_control_set
- restore_channel_values: #55 changed call of _operation_control_set to operation_control_set

[2.1.0] - 2025-05-05

- Added classes:

- ReportExceptionError: added class to generate exception when report methods are called before report are initialized

Added class attributes:

- _api: contains the instance of PyMTSTestLib on a specific COM (needed to allows multiple instance)

Added "_actions" string for report:

- Added report actions "RETRIEVE": "RETRIEVE_TOPOLOGY" for new method GetEbusTopology

Added methods:

- GetEbusTopology: used to get all eBus2 device presence
- send_pc_control_command: used to send PC Control Command to the device
- _writeBroadcastDGTOonEbus: used from other public methods (WriteSetBroadcastDGTOonEbus and WriteSendBroadcastDGTOonEbus) to send or set DGTOs on eBus
- WriteSetBroadcastDGTOonEbus: used to write set DGTO on eBus

Modified methods:

- _operation_control_set became public: operation_control_set
- update_report: now an exception is generated if the method is called but _report is not instantiate 
- add_comment_row: now an exception is generated if the method is called but _report is not instantiate 
- set_report_name: now an exception is generated if the method is called but _report is not instantiate 
- _open_comm: updated to new structure of PyMTSTestLib 00.01.00 who allows multiple instance
- _system_startup: updated to new structure of PyMTSTestLib 00.01.00 who allows multiple instance
- _close_comm: updated to new structure of PyMTSTestLib 00.01.00 who allows multiple instance
- _write_generic_dgto: updated to new structure of PyMTSTestLib 00.01.00 who allows multiple instance
- _read_generic_dgto: updated to new structure of PyMTSTestLib 00.01.00 who allows multiple instance
- multiwrite_dgto: updated to new structure of PyMTSTestLib 00.01.00 who allows multiple instance
- ping_dgto: updated to new structure of PyMTSTestLib 00.01.00 who allows multiple instance
- multiping_dgto: updated to new structure of PyMTSTestLib 00.01.00 who allows multiple instance
- detect_dgto_change: updated to new structure of PyMTSTestLib 00.01.00 who allows multiple instance
- read_memory: updated to new structure of PyMTSTestLib 00.01.00 who allows multiple instance
- _raw_request: updated to new structure of PyMTSTestLib 00.01.00 who allows multiple instance
- operation_control_set: updated to new structure of PyMTSTestLib 00.01.00 who allows multiple instance
- SendRawMessageToEbus: updated to new structure of PyMTSTestLib 00.01.00 who allows multiple instance
- SendRawRequestToEbus: updated to new structure of PyMTSTestLib 00.01.00 who allows multiple instance
- ReadTDA: updated to new structure of PyMTSTestLib 00.01.00 who allows multiple instance
- WriteTDA: updated to new structure of PyMTSTestLib 00.01.00 who allows multiple instance
- send_reset: updated to new structure of PyMTSTestLib 00.01.00 who allows multiple instance
- suspend_com: updated to new structure of PyMTSTestLib 00.01.00 who allows multiple instance
- resume_com: updated to new structure of PyMTSTestLib 00.01.00 who allows multiple instance

Fixed all return type for the following methods:

- _split_hex
- _search_dgto
- _search_phantom
- read_memory
- _raw_request
- _read_id_table
- get_channel_values
- readIdentTable

[2.0.0] - 2025-03-06

Added class attributes:

- _com_status: #49 Adapted to Python lib
- _default_write_check_time_dgto: #48 added possibility to change default value of reading after a write on a dgto
- _default_write_check_time_probe: #48 added possibility to change default value of reading after a write on a probe

Modified class attributes:

- _actions: added key SEND for SEND_EBUS message (used by SendRawMessageToEbus, SendRawRequestToEbus and WriteSendBroadcastDGTOonEbus methods)

Added static function:

- _get_dgto_size_and_sign: added static function to evaluate the T of the D-G-T-O, returns the size of the DGTO and if is signed or not
- convert_hex_to_dgto: #32 added static function to convert the DGTO address to the DGTO code (used by read_dgto_range funct)

Added methods:

- update_report: #51 added public method to access method _report.update_report()
- add_comment_row: #51 added public method to access method _report.add_comment_row()
- set_report_name: #19 added the possibility to change the name of the report
- SendRawMessageToEbus: Added the possibility to send raw message directly on ebus
- SendRawRequestToEbus: Added the possibility to send raw request directly on ebus
- WriteSendBroadcastDGTOonEbus: #52 added the possibility to write send DGTO on eBus (command 0x2010 with destination broadcast 0xFE)
- send_reset: #36 Added implementation of ATG Reset Command (with specified timer before the reset)
- suspend_com: Added command to suspend the use of the COM port
- resume_com: Added command to resume the use of the COM port


Modified methods:

- convert_dgto_to_hex: moved from class method to static func
- _merge_hex: moved from class method to static func
- _split_hex: moved from class method to static func
- _get_hex: moved from class method to static func

- __init__: #49 Adapted to Python lib, #48 added reading from config.txt of probe_check_time and dgto_check_time
- __del__: #49 Adapted to Python lib
- _open_comm: #49 Adapted to Python lib
- _close_comm:  #49 Adapted to Python lib
- _system_startup: #49 Adapted to Python lib
- _search_dgto: #50 Adapted to return a tuple with [DGTO_ADDRESS, DGTO_NAME_TXT, DGTO_CODE_TXT]
- _search_phantom: #49 Adapted to Python lib, #50 Adapted to return a tuple with [PHANTOM_DGTO_ADDRESS, PHANTOM_DGTO_TYPE, PHANTOM_CODE, DGTO_NAME_TXT, DGTO_CODE_TXT]
- _write_generic_dgto: #49 Adapted to Python lib, #21 Added the possibility to specify Cat/Zone/Occ of the device, #50 upgraded to print always DGTO Name + DGTO Code if available
- _write_probe: #50 upgraded to print always DGTO Name + DGTO Code if available
- _write_phantom_dgto: #50 upgraded to print always DGTO Name + DGTO Code if available
- _read_generic_dgto: #49 Adapted to Python lib, #21 Added the possibility to specify Cat/Zone/Occ of the device, #50 upgraded to print always DGTO Name + DGTO Code if available
- _read_phantom_dgto: #50 upgraded to print always DGTO Name + DGTO Code if available
- read_dgto_until: #21 Added the possibility to specify Cat/Zone/Occ of the device
- read_dgto: #21 Added the possibility to specify Cat/Zone/Occ of the device, #50 upgraded to print always DGTO Name + DGTO Code if available
- write_dgto: #21 Added the possibility to specify Cat/Zone/Occ of the device, #50 upgraded to print always DGTO Name + DGTO Code if available, #48 added possibility to change default value of reading after a write on a dgto or probe separately
- multiwrite_dgto: #49 Adapted to Python lib, #21 Added the possibility to specify Cat/Zone/Occ of the device, #15 Now this method use the WriteDGTOList and WriteDGTOList_MI to write up to 8 DGTO at the same time with only one command (the reading check is done at the same way reading up to 8 DGTO at once)
- ping_dgto: #49 Adapted to Python lib, #21 Added the possibility to specify Cat/Zone/Occ of the device, #50 upgraded to print always DGTO Name + DGTO Code if available
- multiping_dgto: #49 Adapted to Python lib, #21 Added the possibility to specify Cat/Zone/Occ of the device, #50 upgraded to print always DGTO Name + DGTO Code if available
- detect_dgto_change: #49 Adapted to Python lib, #21 Added the possibility to specify Cat/Zone/Occ of the device, #50 upgraded to print always DGTO Name + DGTO Code if available
- read_dgto_range: #32 fixed when DGTO name is used, #21 Added the possibility to specify Cat/Zone/Occ of the device
- read_memory: #49 Adapted to Python lib
- write_memory: #49 Adapted to Python lib
- wait_time: #22 Fixed the issue about waiting 1s more than the set value
- _raw_request: #49 Adapted to Python lib, #21 Added the possibility to specify Cat/Zone/Occ of the device
- _raw_message: #49 Adapted to Python lib, #21 Added the possibility to specify Cat/Zone/Occ of the device
- _operation_control_set: #49 Adapted to Python lib
- _read_id_table: #49 Adapted to Python lib
- get_channel_values: #49 Adapted to Python lib
- ReadTDA: #49 Adapted to Python lib
- WriteTDA: #49 Adapted to Python lib
- readIdentTable: #49 Adapted to Python lib

- Added classes:

- CommExceptionError: added class to generate exception when COM cannot be open

Changelog:
[1.9.0] - 2024-06-27
Added methods:
- "_read_id_table":  # Ticket #24

Modified methods:

- "readIdentTable":   # Ticket #24
- "_search_dgto":     # Ticket #18

[1.8.0] - 2024-05-29
Added methods:

- "ReadTDA"
- "WriteTDA"
- "readIdentTable"

Modified methods:

- "write_memory" method property access moved from private to public
- "read_memory" method property access moved from private to public

[1.7.0] - 2024-01-23

Added methods:

- "_raw_message"

Modified methods:

- "write_memory" now uses a "RAW Message" instead of a "RAW Request"

Modified variables:

- "probeSourcePath" and "phantomSourcePath" path are not used if the string "None" is indicated in "Config.txt"


[1.6.0] - 2024-01-23

- Enable Read/Write DGTO Phantom

[1.5.0] - 2023-11-15

>>>>>> NOTE: THESE METHODS HAVE NOT YET BEEN TESTED, SO THEY MUST BE CONSIDERED AS NOT USABLE!! <<<<<<

Added methods:

- "_search_phantom"
- "read_memory"
- "write_memory"
- "_read_phantom_dgto"
- "_write_phantom_dgto"

Modified methods:

- "_search_probe" now doesn't perform another "search_dgto" and the parameter "dgto_name" has been changed for
"dgto_code" with the hexadecimal code of DGTO (for robustness in case of Phantom inputs)
- "write_dgto" now writes also Phantom DGTOs
- new "read_dgto" now reads also Phantom DGTOs
- old "read_dgto" is now called "read_generic_dgto"

Added variables:

- "_phantomExcelFile"

Modified variables:

- "_probeExcelFile" has now the "None" type value if the file is not present
- "_phantomExcelFile" has now the "None" type value if the file is not present
- "_excelFile" has now the "None" type value if the file is not present (for retro-compatibility)


[1.4.4] - 2022-05-27
- "write_probe" check if written value isn't correct and increase or decrease the ADC value until written value is correct

[1.4.3] - 2022-05-25
- "write_probe" set not working code if value of the probe is out of the range. If DGTO is no probe, set to max

[1.4.2] - 2022-05-24
- "write_probe" set not working code if value is out of the range

[1.4.1] - 2022-05-23
- changed log

[1.4.0] - 2022-05-17
Rewritten TestLibPy as class
- "write_dgto" renamed to "write_generic_dgto"
- "write_generic_dgto" and "write_probe" became private methods
- new method "write_dgto" is used to detect and write generic dgto and probes
- "multiwrite_dgto" can write both probes and generic dgto
- "_search_dgto" return DGTO conversion if Excel file non present

[1.3.0] - 2022-01-31
Overall optimization by Intelligentia Team

[1.2.0]
Modified function "Read_Variable_Description": The check for the return value of RAW_Request now is applied to the 
"boolean value" of the TUPLE returned (so "True" if it is not empty)
and NOT in the first element, because if the RAW_Request returns a "False", it is not a TUPLE, so it generates a 
sintax error

Modified Test Automation Module functions:

- "Set_Channel_Values"
- "Save_Channel_Values"
- "Restore_Channel_Values"
- "Get_Channel_Values"
- "write_DGTO": Now it is possible to set directly the ADC Channel with Test Automation

Added functions:

- open_sensor_excel
- write_Probe

Added variables:

- sensor_table
- SensorFileIsPresent

[1.1.0]
MTSTestLib functions:

Added function "Read_Variable_Description"
Modified function "write_DGTO" (now it is possible to select a number of attemps)
Added function "status_COM" to verify if the COM is open or not

Test Automation Module functions:

Added function "Set_Channel_Values"
Added function "Save_Channel_Values"
Added function "Restore_Channel_Values"
Added function "Get_Channel_Values"

Other functions:

Added function "RAW_Request"
Added function "Split_Hex"
Added function "Merge_Hex"
Added function "Operation_ControlSET"

"""

import re
import sys
import time
import ctypes
import pandas as pd
from libs.Report import Report  # TODO: Vedere import dinamico
from pymtstestlib.api import API
from pymtstestlib.shared.error_defs import EErrors
from libs.Ares5Env import Ares5Env, IsDataID, int_to_DATAID, DATAID_to_int, DataTypeFunction, DATA_TYPE_STANDARD, \
    AccessType, DATAID_to_DGTO
from enum import Enum
from pymtstestlib.shared.export_defs import ESetupStatus
from libs.FWPRJ import FWPRJ  # TODO: Vedere import dinamico


def _get_dgto_size_and_sign(dgto: str) -> tuple[int, int]:
    """
    Sw Spec : Na\n
    descriptions: used to get the size and sign of a DGTO

    :param dgto: represent the code of given DGTO [str]\n
    :returns: tuple[int, int] : first value indicate the size in byte, the second is 1 if signed, otherwise 0\n

         Word equal to 2Byte
    -------------------------------------
    | Code | Dimension | Type           |
    -------------------------------------
    | 0	   | 1bit	   | Flag           |
    | 1	   | 1word	   | bitmap word    |
    | 2	   | 1word	   | unsigned word  |
    | 3	   | 1word	   | signed word    |
    | 4	   | Free	   | free           |
    | 5	   | 1byte	   | bitmap byte    |
    | 6	   | 1byte	   | unsigned byte  |
    | 7	   | Free	   | free           |
    -------------------------------------
    """

    appo = dgto.split('-')
    t = appo[2]

    bytes = [None, None]

    if t == '0':
        bytes = [1, 0]  # 1 bit in ATG packets is handled as 1 byte
    elif t == '1':
        bytes = [2, 0]
    elif t == '2':
        bytes = [2, 0]
    elif t == '3':
        bytes = [2, 1]
    # elif t == '4':  # Not handled
    #    bytes = [1, 0]
    elif t == '5':
        bytes = [1, 0]
    elif t == '6':
        bytes = [1, 0]
    # elif t == '7':  # Not handled
    #    bytes = [1, 0]

    return bytes


def convert_dgto_to_hex(dgto_code: str) -> int:
    """
    Sw Spec : Na\n

    :param dgto_code: represent the code of given DGTO [str]\n
    :returns: esa  hexadecimal value\n

    description : Convert the DGTO code (D-G-T-O) in hexadecimal value according a specific algorithm\n
                  Return a list of the substring, using sep as the separator string.\n
                  Split the DGTO code and convert into hexadecimal value.\n
    remarks : none\n
    """
    esa = None
    err = False

    try:
        app = dgto_code.split("-")

        # Verifica correttezza DGTO (4bit - 4bit - 3bit - 5bit)
        if int(app[0]) < 16 or int(app[1]) < 15 or int(app[2]) < 7 or int(app[3]) < 31:
            esa = "0x"
            esa += _get_hex(int(app[0]))
            esa += _get_hex(int(app[1]))
            o = int(app[3])
            t = int(app[2]) * 2

            if o > 15:
                o = o % 16
                t += 1

            esa += _get_hex(t)
            esa += _get_hex(o)
            esa = int(esa, 16)
        else:
            err = True
    except:
        err = True

    if err:
        print("Formato DGTO errato.")
        raise ValueError("Formato DGTO non corretto.")

    return esa


def convert_hex_to_dgto(dgto_hex: int) -> str:
    """
    Sw Spec : Na\n

    :param dgto_hex: represent the address of given DGTO [str]\n
    :returns: DGTO esa  the DGTO code in string format "D-G-T-O"\n

    description : Function to convert hex DGTO value (address) to DGTO code in string format "D-G-T-O"\n
    remarks : none\n
    """
    if dgto_hex < 0 or dgto_hex > 65535:
        raise Exception("ERROR! dgto_hex has to be 0 <= dgto_hex <= 65535 (16 bit unsigned)")

    D = dgto_hex & 0xF000
    D = D >> 12

    G = dgto_hex & 0x0F00
    G = G >> 8

    T = dgto_hex & 0x00E0
    T = T >> 5

    O = dgto_hex & 0x001F

    DGTO = F"{D}-{G}-{T}-{O}"

    return DGTO


def _merge_hex(tuple_hex: tuple, two_complement: bool = False) -> int:
    """
    Sw Spec	: Na

    :param tuple_hex: tuple that contains the hexadecimals to merge
    :param two_complement: indicate if values are complement in base 2

    :returns: hex hexadecimal representation

    Description: This function concatenates two bytes decimal numbers and then converted them in decimal format.
         Concatenate two bytes in hexadecimal format. Check if value.
         Check if values can be negative (int16_t).Return hex value.
         Else Index 0 tuple is the High Byte and Index 1tuple is the Low byte and return hex value.
    Remarks : none
    """
    # Concatenate the two bytes
    result = (tuple_hex[0] << 8) + tuple_hex[1]

    # Check if values can be negative (int16_t)
    if two_complement and result > 32767:
        result = (-1) * (65535 + 1 - result)

    return result


def _split_hex(exa_value: int) -> tuple[int, int]:
    """
    Sw Spec	: Na

    :param exa_value : decimal representation of hexadecimal value
    :returns: first_byte, second_byte : tuple of integer

    description : Split an hexadecimal value, given as decimal representation,
                Splitting the hexadecimal value into first_byte and second_byte. Then return it.
    remarks: none
    """
    second_byte = exa_value >> 8
    first_byte = exa_value & 255

    # the information is insert in the returned tuple (tuple of two integers)
    return first_byte, second_byte


def _get_hex(value: int) -> str:
    """
    Sw Spec	: Na

    :param value: value to convert
    :returns: values string of the hexadecimal value converted

    :Description :This function it is used to convert the DGTO name to hex
    Remarks : none
    """
    if value < 10:
        return str(value)
    return chr(ord('A') + value % 10)


class CommExceptionError(Exception):
    pass


class ReportExceptionError(Exception):
    pass


class Ares5Error(Exception):
    pass


class TestLib:
    _not_working_code = 32767
    _com_status = -1  # -1 = closed, 0 = suspended, 1 = active
    _api = None
    _ares5_env = None
    _fwprj = None
    _default_write_check_time_dgto = 1
    _default_write_check_time_probe = 10

    _options = {
        "port":           None,
        "baudRate":       None,
        "dgtoSourcePath": "",
        "dllPath":        "",
        "device":         ""
    }
    _actions = {
        "SEARCH":   "SEARCH",
        "READ":     "READ",
        "WRITE":    "WRITE",
        "PING":     "PING",
        "CHANGE":   "CHANGE",
        "SEND":     "SEND_EBUS",
        "RETRIEVE": "RETRIEVE_TOPOLOGY"
    }
    _results = {
        "SUCCESS": "SUCCESS",
        "WARNING": "WARNING",
        "ERROR":   "ERROR"
    }


    def __init__(self, settings: dict, report_instance: Report = None) -> None:
        """
        sw spec : n.a.\n

        :parameter settings: configuration given by ConfigParser\n
        :parameter report_instance: Instance of Report class used to create report.

        This instance must be created before the initialization of the MainConnector\n

        :returns: None

        description: Class init and open the connection via dll with the DUT\n

        remarks: none\n
        """
        # update options with customs
        self._options = settings

        # TODO: Gestione .FWPRJ

        # open excel file
        if "dgtoSourcePath" in self._options:
            self._excelFile = pd.read_excel(self._options['dgtoSourcePath'] + ".xlsx")
        else:
            self._excelFile = None

        # open excel file for probes
        if ("probeSourcePath" in self._options) and (self._options['probeSourcePath'] != "None"):
            self._probeExcelFile = pd.read_excel(self._options['probeSourcePath'] + ".xlsx")
        else:
            self._probeExcelFile = None

        # open excel file for dgto phantom
        if ("phantomSourcePath" in self._options) and (self._options['phantomSourcePath'] != "None"):
            self._phantomExcelFile = pd.read_excel(self._options['phantomSourcePath'] + ".xlsx")
        else:
            self._phantomExcelFile = None

        # open excel file for probes
        if ("fwprjSourcePath" in self._options) and (self._options['fwprjSourcePath'] != "None"):
            self._fwprj = FWPRJ(self._options['fwprjSourcePath'] + ".fwprj")
        else:
            self._fwprj = None

        if "probe_check_time" in self._options:
            self._default_write_check_time_probe = self._options['probe_check_time']

        if "dgto_check_time" in self._options:
            self._default_write_check_time_dgto = self._options['dgto_check_time']

        if "Ares5EnvSourcePath" in self._options:
            self._ares5_env = Ares5Env(self._options['Ares5EnvSourcePath'] + ".xml")

        # init report
        if not isinstance(report_instance, Report):
            self._report = Report({
                "path": "./reports/"
            })
        else:
            self._report = report_instance

        # board startup
        self._open_comm(self._options['port'], self._options['baudRate'])
        self._system_startup()

        # add device to report
        self._report.add_device(self._options['device'])


    def __del__(self):
        """
        sw spec : n.a.\n
        :param self: class instance\n
        :returns: none\n
        description : Close the connection with dll\n
        remarks : none\n
        """
        self._close_comm()


    def _open_comm(self, port: int, baud_rate: int):
        """
        sw spec: none\n

        :parameter self: class instance\n
        :parameter port: port number\n
        :parameter baud_rate: speed port\n
        :returns: none\n
        :raises CommExceptionError:  if COM already open or not present

        description : open serial port communication\n
        remarks none\n
        """
        COM = None

        if self._api is None:
            self._api = API()

        if self._com_status != 1:
            if sys.platform.startswith("win"):  # Windows
                COM = f"//./COM{port}"
            elif sys.platform.startswith("linux"):  # Unix
                COM = f"/dev/ttyUSB{port}"
            elif sys.platform.startswith("darwin"):  # Mac
                COM = f"/dev/cu.usbserial-{port}"

            response = self._api.CommOpen(COM, baud_rate)

            if response != EErrors.E_OK:
                self._report.add_comment_row("An error occurred during COMM opening operation.",
                                             print_on_console=True, background_color="ERROR")
                raise CommExceptionError("COMM Opening operation Error, "
                                         f"please check if the {COM} is the correct one and not already in use.")
            else:
                self._com_status = 1
        else:
            self._report.add_comment_row(f"ERROR! port {COM} already open.",
                                         print_on_console=True, background_color="ERROR")


    def _system_startup(self) -> None:
        """
        sw spec: none\n

        :parameter self: class instance\n
        :returns: none\n

        description : system startup\n
        remarks none\n
        """
        response = self._api.SystemStartup()

        if response != EErrors.E_OK:
            message = "An error occurred during Startup operation"
            self._report.print_on_console(message)
            self._report.add_comment_row(message)


    def _close_comm(self) -> None:
        """
        sw spec: none\n

        :parameter self: class instance\n
        :returns: none\n

        description : Close communication with board\n
        remarks none\n
        """
        if self._com_status == 1 and self._api is not None:
            response = self._api.CommClose()

            if response != EErrors.E_OK:
                self._com_status = -1
                message = "An error occurred during COMM closing operation"
                self._report.print_on_console(message)
                self._report.add_comment_row(message)
            else:
                self._api = None


    """ ---------------- Begin: Excel file functions --------------- """


    def _search_dgto(self, dgto: str) -> tuple[int, str, str]:
        """
        sw spec: none\n

        :parameter self: instance class\n
        :parameter dgto: name ot the DGTO to search\n
        :returns: tuple[int, str, str] with hex dgto code format, DGTO Name, DGTO Code if the DGTO is found, otherwise returns 0, None, None

        description: Search if the incoming DGTO is a valid data.\n
        remarks: none\n
        """
        res_val = 0
        name = None
        code = None

        if self._fwprj is not None:
            name, code, res_val = self._fwprj.searchStandardDGTO(dgto)
            if res_val is None:
                res_val = 0
        elif type(self._excelFile) == pd.DataFrame:
            # search DGTO, name or code, in file
            for i in range(len(self._excelFile)):
                if self._excelFile["DGTO"][i] == dgto or self._excelFile["Name"][i] == dgto:
                    dgto_code = self._excelFile['Code'][i]
                    res_val = int(dgto_code, 16)
                    name = self._excelFile["Name"][i]
                    code = self._excelFile["DGTO"][i]

        if res_val == 0 and re.match("^[0-9]+\\-[0-9]+\\-[0-9]+\\-[0-9]+$", dgto):
            res_val = convert_dgto_to_hex(dgto)  # Ticket #18
            name = None
            code = dgto

        if res_val == 0:  # not found
            self._report.print_on_console(f"DGTO {dgto} has not been found")
            self._report.add_action_row(
                    self._options["device"], self._actions["SEARCH"], dgto, None, None,
                    self._results["ERROR"], "Not been found")

        return res_val, name, code


    def _search_probe(self, dgto_code: int) -> int:
        """
        sw spec: n.a.\n

        :parameter self: class instance\n
        :parameter dgto_code: a string with name or code of the DGTO to search\n
        :returns:  index:  > 0 index in probes file if dgto_name is valid\n
                            otherwise 0 [int]\n

        description: Search if dgto_name is a probe\n
        remarks: none\n
        """
        if type(self._probeExcelFile) == pd.DataFrame:
            probes_keys = self._probeExcelFile.keys()

            for index, value in enumerate(probes_keys):
                if re.sub("[^0-9a-zA-Z]+", "", str(value)).isnumeric() and dgto_code == int(
                        re.sub("[^0-9a-zA-Z]+", "", str(value))):
                    return index
        return 0


    def _search_phantom(self, dgto: str) -> tuple[int, int, int, str, str]:
        """
        sw spec: n.a.\n

        :parameter self: class instance\n
        :parameter dgto: name of code of DGTO PHANTOM\n
        :returns: tuple[int, int, int, str, str] with phantom_address, phantom_type, phantom_code, str_phantom_name, str_phantom_code if the phantom is found, otherwise all None

        description: Search if dgto is a probe\n
        remarks: none\n
        """
        phantom_address = None
        phantom_type = None
        phantom_code = None
        name = None
        code = None

        if self._fwprj is not None:
            name, code, phantom_code, address, offset = self._fwprj.searchPhantomDGTO(dgto)

            if name is not None:
                calc_type = code.split("-")
                phantom_type = int(calc_type[2])
                phantom_address = address + offset
        elif type(self._phantomExcelFile) == pd.DataFrame:
            # search DGTO, name or code, in file
            for i in range(len(self._phantomExcelFile)):
                if self._phantomExcelFile["DGTO"][i] == dgto or self._phantomExcelFile["Name"][i] == dgto:
                    phantom_address = int(self._phantomExcelFile['Address'][i]) + int(
                            self._phantomExcelFile['Offset'][i])
                    calc_type = str(self._phantomExcelFile["DGTO"][i])
                    calc_type = calc_type.split("-")
                    phantom_type = int(calc_type[2])
                    dgto_code = self._phantomExcelFile['Code'][i]
                    phantom_code = int(dgto_code, 16)
                    name = self._phantomExcelFile["Name"][i]
                    code = self._phantomExcelFile["DGTO"][i]

        return phantom_address, phantom_type, phantom_code, name, code


    def update_report(self, test_result: bool, test_fail_info: int = None) -> None:
        """
        :param test_result:	If set to False and test_result_info is none or "Failed" the last row in the generated
        report will be TEST FAILED, if set to true the report will be generated with last row as "TEST PASSED"

        :param test_fail_info: Additional info for FAILED test (explains why the test is failed):
            0 = STANDARD FAIL (text on report: "TEST FAILED", associated to a fail in the final check on Test Result).
            1 = PRECONDITION FAIL (text on report: "TEST FAILED PRECONDITION").
            2 = STEP FAIL (text on report: "TEST FAILED STEP").
            3 = BLOCKED (text on report: "TEST BLOCKED").
            4 = TO BE COMPLETED (text on report: "TEST TO BE COMPLETED", associated to a script who fail but has already tested some case).

        :returns: None

        :Description   : This function will add a new tab in the report file with the test result passed
        if the report.xlsx already exist, otherwise will add a new .xlsx file

        Remarks: none
        """
        if self._report is None:
            raise ReportExceptionError("The instance of _report is None, is not possible to generate the report.")
        else:
            self._report.update_report(test_result, test_fail_info)


    def add_comment_row(self, comment, background_color="TRANSPARENT", print_on_console=False) -> None:
        """
        :param self: class instance
        :param comment: the comment to add in report
        :param background_color: the background color of the comment
        :param print_on_console: if True, is printed even on console
        :returns: None

        :Description: add a comment in the printable report
        Remarks: none
        """
        if self._report is None:
            raise ReportExceptionError("The instance of _report is None, is not possible to add a comment row.")
        else:
            self._report.add_comment_row(comment, background_color, print_on_console)


    def set_report_name(self, report_file_name: str) -> None:
        """
        :param report_file_name: the new name to use when update_report is called without path and file extension

        :returns: None
        :Description   : this function allows to change the name of the report
        Remarks: none
        """
        if self._report is None:
            raise ReportExceptionError("The instance of _report is None, is not possible to change the report name.")
        else:
            self._report.set_report_name(report_file_name)


    """ ---------------- End: Excel file functions --------------- """

    """ ---------------- Begin: DGTO functions --------------- """


    def _write_generic_dgto(self, dgto_name: str, dgto_code: int, value: int, check_time: int = 1,
                            is_multiwrite: bool = False, name: str = None, code: str = None, cat: int = None,
                            zone: int = None, occ: int = None) -> bool:
        """
        sw spec:  n.a.\n
        :parameter self: class instance\n
        :parameter dgto_name:  name of the DGTO to write [string]\n
        :parameter dgto_code: code of the DGTO to write [int]\n
        :parameter value: to write [int]\n
        :parameter check_time: seconds to wait in order to check if value it is written [int]\\\n
        :parameter is_multiwrite: if True, doesn't check the written value and not print message on console [bool]\n
        :parameter name: DGTO Name to print in report
        :parameter code: DGTO Code to print in report
        :parameter cat: category of the DGTO owner
        :parameter zone: zone of the DGTO owner
        :parameter occ: occurrence of the DGTO owner
        :returns: True if value is written, False if dgto is invalid or value is not written after check_time\n

        description: Write DGTO by given name or code\n
        remarks: none\n
        """
        is_mi = False

        if name is not None and code is not None:
            dgto_text_info = f"{name} ({code})"
        elif name is not None:
            dgto_text_info = f"{name} ({dgto_name})"
        else:
            dgto_text_info = dgto_name

        if cat is not None and zone is not None and occ is not None:
            dgto_text_info = f"{dgto_text_info} 0x{cat:02x}/0x{zone:02x}/0x{occ:02x}"
            is_mi = True

        self._report.print_on_console(f"Writing {dgto_text_info} with value {str(value)} ...")

        if is_mi:
            response = self._api.WriteDGTO_MI(cat, zone, occ, dgto_code, value)
        else:
            response = self._api.WriteDGTO(dgto_code, value)  # Writing DGTO

        if response != EErrors.E_OK:
            self._report.print_on_console(
                    f"An error occurred during writing operation: DGTO {dgto_text_info} has not been written")
            self._report.add_action_row(
                    self._options["device"], self._actions["WRITE"], dgto_text_info, None, value,
                    self._results["ERROR"], "Error occurred during writing operation")

        if not is_multiwrite:
            if response != EErrors.E_OK:
                return False
            else:
                self.wait_time(check_time)
                current_value = self.read_dgto(dgto_name, True, cat=cat, zone=zone, occ=occ)
                if current_value == value:
                    self._report.print_on_console(
                            f"DGTO {dgto_text_info} has been written correctly with value {str(value)}")
                    self._report.add_action_row(
                            self._options["device"], self._actions["WRITE"], dgto_text_info, None, value,
                            self._results["SUCCESS"], None)
                    return True
                else:
                    self._report.print_on_console(
                            f"WARNING: DGTO {dgto_text_info} has been NOT written with value {str(value)}")
                    self._report.add_action_row(
                            self._options["device"], self._actions["WRITE"], dgto_text_info, None, value,
                            self._results["WARNING"], "NOT written with value")
                    return False
        else:
            return response


    def _write_probe(self, dgto_name: str, probe_index: int, value: int, check_time: int = 10,
                     is_multiwrite: bool = False, name: str = None, code: str = None) -> bool:
        """
        Sw spec : n.a.\n

        :parameter dgto_name: name of the DGTO to write\n
        :parameter probe_index: index of to write\n
        :parameter value: value to write\n
        :parameter check_time: seconds to wait in order to check if value it is written\n
        :parameter is_multiwrite: if True, doesn't check the written value and not print message on console\n
        :parameter name: DGTO Name to print in report
        :parameter code: DGTO Code to print in report

        description:  write probe value in specific probe passed by name or code\n

        :returns: True if value is written, False if dgto is invalid or value is not written after check_time\n
        """
        if name is not None and code is not None:
            dgto_text_info = f"{name} ({code})"
        elif name is not None:
            dgto_text_info = f"{name} ({dgto_name})"
        else:
            dgto_text_info = dgto_name

        self._report.print_on_console(f"Writing probe {dgto_text_info} with value {str(value)} ...")

        # get probes' list
        dgto_probe = self._probeExcelFile.keys()

        # range of value of given probe
        min_probe_value = int(self._probeExcelFile[dgto_probe[probe_index]][len(self._probeExcelFile) - 1])
        max_probe_value = int(self._probeExcelFile[dgto_probe[probe_index]][len(self._probeExcelFile) - 2])

        # the value for ADC = 0, row 3 of Execel, is set to 32767 only for probes
        is_probe = int(self._probeExcelFile[dgto_probe[probe_index]][3]) == self._not_working_code

        if is_probe and (value < min_probe_value or value > max_probe_value):
            value = self._not_working_code
            self._report.print_on_console(
                    f"INFO: value is out of the range. It will be written {str(value)} ...")
        # setting max value if given value is greater than that
        elif value > max_probe_value:
            value = max_probe_value
            self._report.print_on_console(
                    f"INFO: value is greater than the maximum values. It will be written {str(value)} ...")
        # setting min value if given value is lower than that
        elif value < min_probe_value:
            value = min_probe_value
            self._report.print_on_console(
                    f"INFO: value is lower than the minimum values. It will be written {str(value)} ...")

        # Get the list of ADC values of current probe removing the first that is the hexadecimal value of probe.
        probe_value_serie = self._probeExcelFile[dgto_probe[probe_index]]
        adc_values = probe_value_serie.tolist()[1:]
        # Get the list of temp in °C/10 values removing the first that is the hexadecimal value of probe.
        probe_value_value = self._probeExcelFile[dgto_probe[0]]
        temp_values = probe_value_value.tolist()[1:-3]
        # Since the ADC values are increasing, having removed the first two lines of the Excel file, I get that the
        # index of the element within the list corresponds to the ADC value to be written on the channel.
        index = temp_values.index(value)
        adc = int(adc_values[index])
        self.set_channel_values([int(probe_value_serie[0])], [adc])

        is_written = True
        if not is_multiwrite:
            self.wait_time(check_time)
            current_value = self.read_dgto(dgto_name, True)
            is_written = (current_value == value)

            if is_probe and not is_written:
                self._report.print_on_console(f"The written value doesn't match the expected value.")
                # check written value and desidered value
                if value < current_value:
                    self._report.print_on_console(f"Increasing ADC...")
                    while value < current_value:
                        adc += 1
                        self.set_channel_values([int(probe_value_serie[0])], [adc])
                        self.wait_time(check_time)
                        current_value = self.read_dgto(dgto_name, True)
                elif value > current_value:
                    self._report.print_on_console(f"Decreasing ADC...")
                    while value > current_value:
                        adc -= 1
                        self.set_channel_values([int(probe_value_serie[0])], [adc])
                        self.wait_time(check_time)
                        current_value = self.read_dgto(dgto_name, True)

                is_written = (current_value == value)

            if is_written:
                self._report.print_on_console(
                        f"Probe {dgto_text_info} has been written correctly with value {str(value)}")
                self._report.add_action_row(
                        self._options["device"], self._actions["WRITE"], dgto_text_info, None, value,
                        self._results["SUCCESS"], None)
            else:
                self._report.print_on_console(
                        f"WARNING: Probe {dgto_text_info} has been NOT written with value {str(value)}")
                self._report.add_action_row(
                        self._options["device"], self._actions["WRITE"], dgto_text_info, None, value,
                        self._results["WARNING"], "NOT written with value")

        return is_written


    def _write_phantom_dgto(self, dgto_name: str, dgto_phantom_address: int, dgto_phantom_type: int, value: int,
                            check_time: int = 1,
                            is_multiwrite: bool = False, name: str = None, code: str = None,
                            cat: int = None, zone: int = None, occ: int = None) -> bool:
        """
        SW spec :	NA\n

        :parameter self: class instance\n
        :parameter dgto_name: name of the DGTO to search[String]\n
        :parameter dgto_phantom_address:  address in RAM  of DGTO [int]\n
        :parameter dgto_phantom_type:  type of DGTO [int]\n
        :parameter value: data to write [int]\n
        :parameter is_multiwrite: bool = FALSE -> if True, comment doesn't write in report\n
        :parameter name: DGTO Name to print in report
        :parameter code: DGTO Code to print in report
        :returns: value of DGTO if name is valid\n

        description :Read DGTO by given name or code\n
        remarks: none\n
        """
        if name is not None and code is not None:
            dgto_text_info = f"{name} ({code})"
        elif name is not None:
            dgto_text_info = f"{name} ({dgto_name})"
        else:
            dgto_text_info = dgto_name

        # contains the intermediate
        # function result (False,True) [bool]
        aux_result = False  # auxiliary result,

        response = False  # contains the write_memory response (False,True) [bool]

        value_in_bytes_splitted = 0  # used to store intermediate value to write in memory

        # First of all, I have to perform a check to verify if the variable "value" contains an integer value

        if type(value) != type(1):  # In this case, the Test Automator gives a wrong value type
            # return False
            aux_result = False
            self._report.add_comment_row(f'The type value of "{value}" is wrong for DGTO "{dgto_text_info}".',
                                         background_color="WARNING")
        else:
            aux_result = True

        # 16 bit unsigned handling
        if aux_result and dgto_phantom_type == 2:  # 16 bit unsigned
            # Perform a check to verify if the variable "value" contains a value that can be
            # hold in a word (so 16 bits -> [0 - 65535])
            if (value < 0) or (value > 65535):
                aux_result = False  # Unsuccessful
                self._report.add_comment_row(f'The value {value} of DGTO "{dgto_text_info}" is out of range.',
                                             background_color="WARNING")
            else:  # the value is in right range
                aux_result = True  # Success
                # I need to use an "uint16" type variable to manage the correct format of the data
                # It is the same procedure both for signed and unsigned bytes
                value_in_bytes = ctypes.c_uint16(value)
                # "split_hex" method returns a tuple, but also it has the attribute "leng", so I can use it instead of a
                # list in "write_memory" without change his variable type
                value_in_bytes_splitted = _split_hex(value_in_bytes.value)

        # handling 16 bit signed
        elif aux_result and dgto_phantom_type == 3:
            # Perform a check to verify if the variable "value" contains a value that can be
            # hold in a word (so 16 bits -> [-32768 - 32768])
            if value < -32768 or value > 32767:
                aux_result = False  # Unsuccessful #
                self._report.add_comment_row(f'The value {value} of DGTO "{dgto_text_info}" is out of range.',
                                             background_color="WARNING")
            else:  # the value is in range
                aux_result = True  # Success
                value_in_bytes = ctypes.c_int16(value)
                value_in_bytes_splitted = _split_hex(value_in_bytes.value)
        elif aux_result and (dgto_phantom_type != 3 or dgto_phantom_type != 2):
            # Handling flag,word,signed byte,unsigned byte types
            # Perform a check to verify if the variable "value" contains a value that can be
            # hold in a word (so 8 bits -> [0 - 255])
            if value < 0 or value > 255:
                aux_result = False  # unsuccessful
                self._report.add_comment_row(f'The value {value}  of DGTO "{dgto_text_info}" is out of range.',
                                             background_color="WARNING")
            else:  # the value is in range
                aux_result = True  # Success
                value_in_bytes_splitted = [ctypes.c_uint8(value).value]

        if aux_result:  # success in previous operation
            self._report.print_on_console(f"Writing {dgto_text_info} with value {str(value)} ...")
            response = self.write_memory(dgto_phantom_address, value_in_bytes_splitted, cat, zone,
                                         occ)  # Writing Phantom DGTO
        else:
            # in case of failure in previous operation
            response = aux_result

        if not is_multiwrite:
            self.wait_time(check_time)
            current_value = self.read_dgto(dgto_name, skipComment=True, cat=cat, zone=zone, occ=occ)
            if current_value == value:
                self._report.print_on_console(
                        f"DGTO {dgto_text_info} has been written correctly with value {str(value)}")
                self._report.add_action_row(
                        self._options["device"], self._actions["WRITE"], dgto_text_info, None, value,
                        self._results["SUCCESS"], None)
                # return True
                response = True
            else:
                self._report.print_on_console(
                        f"WARNING: DGTO {dgto_text_info} has been NOT written with value {str(value)}")
                self._report.add_action_row(
                        self._options["device"], self._actions["WRITE"], dgto_text_info, None, value,
                        self._results["WARNING"], "NOT written with value")
                # return False
                response = False

        return response


    def _read_generic_dgto(self, dgto_name: str, dgto_code: int, skipComment: bool = False,
                           name: str = None, code: str = None,
                           cat: int = None, zone: int = None, occ: int = None) -> int:
        """
        SW spec:	NA\n

        :parameter self:      instance class\n
        :parameter dgto_name:  name of the DGTO to search\n
        :parameter dgto_code:  hexadecimal code of the DGTO to search\n
        :parameter skipComment:  if True, comment doesn't write in report\n
        :parameter name: DGTO Name to print in report
        :parameter code: DGTO Code to print in report
        :parameter cat: category of the DGTO owner
        :parameter zone: zone of the DGTO owner
        :parameter occ: occurrence of the DGTO owner
        :returns: value of DGTO if name is valid\n

        description : read Generic DGTO by given name or code\n
        remarks : na\n
        """
        if name is not None and code is not None:
            dgto_text_info = f"{name} ({code})"
        elif name is not None:
            dgto_text_info = f"{name} ({dgto_name})"
        else:
            dgto_text_info = dgto_name

        if cat is None or zone is None or occ is None:
            response = self._api.ReadDGTO(dgto_code)
        else:
            response = self._api.ReadDGTO_MI(cat, zone, occ, dgto_code)
            dgto_text_info = f"{dgto_text_info} {hex(cat)}/{hex(zone)}/{hex(occ)}"

        result = response[0]
        value = response[1]

        if result != EErrors.E_OK:
            self._report.print_on_console(
                    f"An error (EErrors code = {response}) occurred during reading operation: DGTO {dgto_text_info} has not been read")
            self._report.add_action_row(
                    self._options["device"], self._actions["READ"], dgto_text_info, None, None,
                    self._results["ERROR"], "Error occurred during reading operation")
        else:
            if not skipComment:
                self._report.print_on_console(f"DGTO {dgto_text_info} = {value}")
                self._report.add_action_row(
                        self._options["device"], self._actions["READ"], dgto_text_info, value, None,
                        self._results["SUCCESS"], None)
            return value


    def _read_phantom_dgto(self, dgto_name: str, dgto_address: int, dgto_type: int, skipComment: bool = False,
                           name: str = None, code: str = None) -> int:
        """
        SW spec:NA\n

        :parameter dgto_name:  name of the Phantom DGTO to read\n
        :parameter dgto_address:  address in RAM memory of Phantom DGTO to read\n
        :parameter dgto_type:  type of Phantom DGTO to read\n
        :parameter skipComment:  if True, comment doesn't write in report\n
        :parameter name: DGTO Name to print in report
        :parameter code: DGTO Code to print in report
        :returns:  value of DGTO if name is valid

        description: read Phantom DGTO by given name or code\n
        remarks : none\n
        """
        if name is not None and code is not None:
            dgto_text_info = f"{name} ({code})"
        elif name is not None:
            dgto_text_info = f"{name} ({dgto_name})"
        else:
            dgto_text_info = dgto_name

        if 1 <= dgto_type <= 3:  # 16 bit
            num_byte_rx = 2
        else:  # 8 bit
            num_byte_rx = 1

        response = self.read_memory(dgto_address, num_byte_rx)

        if not response[0]:
            self._report.print_on_console(
                    f"An error occurred during reading operation: DGTO {dgto_text_info} has not been read")
            self._report.add_action_row(
                    self._options["device"], self._actions["READ"], dgto_text_info, None, None,
                    self._results["ERROR"], "Error occurred during reading operation")
        else:
            data_return = response[1]

            if dgto_type == 1 or dgto_type == 2:  # 16 bit unsigned
                value = _merge_hex((data_return[1], data_return[0]), False)

            elif dgto_type == 3:  # 16 bit signed
                value = _merge_hex((data_return[1], data_return[0]), True)

            else:
                value = data_return[0]

            if not skipComment:
                self._report.print_on_console(f"DGTO {dgto_text_info} = {value}")
                self._report.add_action_row(
                        self._options["device"], self._actions["READ"], dgto_text_info, value, None,
                        self._results["SUCCESS"], None)
            return value


    def read_dgto_until(self, dgto: str, operator: str, limit: int, custom_string: str = "",
                        cat: int = None, zone: int = None, occ: int = None) -> None:
        """
        SW spec:NA\n

        :parameter self:  class instance\n
        :parameter dgto: name of dgto to read [string]\n
        :parameter operator:  operation of condition [String]\n
        :parameter limit:  limit to reach [int]\n
        :parameter custom_string:  alternative to print in console otherwise dgto name[string]\n
        :parameter cat: category of the DGTO owner
        :parameter zone: zone of the DGTO owner
        :parameter occ: occurrence of the DGTO owner
        :returns: None

        description	: Execute a reading operation until dgto value meet condition\n
                    if all the operations completed with\n
                      in the limits print the DGTO name otherwise operations and operators not allowed\n

        remarks : none\n
        """
        operations = ["<", ">", "==", "<=", ">=", "!="]
        if operator in operations:
            dgto_value = self.read_dgto(dgto, True, cat, zone, occ)
            operation = f"{dgto_value} {operator} {limit}"

            while eval(operation):
                dgto_value = self.read_dgto(dgto, True, cat, zone, occ)
                operation = f"{dgto_value} {operator} {limit}"
                print(f"\r{custom_string if custom_string else dgto}: " + str(dgto_value), end="")

            print("")
        else:
            raise Exception(f"Operation {operator} is not allowed")


    def read_dgto(self, dgto: str, skipComment: bool = False, cat: int = None, zone: int = None,
                  occ: int = None) -> int:
        """
        SW spec:	NA\n
        :parameter self: class instance\n
        :parameter dgto: name of the DGTO to search[String]\n
        :parameter skipComment: FALSE -> if True, comment doesn't write in report [bool]\n
        :parameter cat: category of the DGTO owner
        :parameter zone: zone of the DGTO owner
        :parameter occ: occurrence of the DGTO owner
        :returns: int: value of DGTO if name is valid\n

        description: Read DGTO by given name or code\n
        remarks: none\n
        """
        result = None
        # Searching DGTO on Phantom Excel file
        dgto_phantom = self._search_phantom(dgto)

        # Check if Phantom DGTO has been found
        if dgto_phantom[0] is not None:
            dgto_phantom_address = dgto_phantom[0]
            dgto_phantom_type = dgto_phantom[1]
            name = dgto_phantom[3]
            code = dgto_phantom[4]
            result = self._read_phantom_dgto(dgto, dgto_phantom_address, dgto_phantom_type, skipComment, name, code)
        else:
            # Searching DGTO on Excel file
            dgto_code, name, code = self._search_dgto(dgto)

            if dgto_code != 0:
                result = self._read_generic_dgto(dgto, dgto_code, skipComment, name, code, cat, zone, occ)

        return result


    def multiread_dgto(self, array_dgto: list, skipComment: bool = False, cat: int = None, zone: int = None,
                       occ: int = None) -> list[int]:
        """
        SW spec:	NA\n
        :param skipComment: FALSE -> if True, comment doesn't write in report [bool]\n
        :parameter self: class instance\n
        :parameter array_dgto: list of names of the DGTOs to search[String], Phantom not supported\n
        :parameter cat: category of the DGTO owner
        :parameter zone: zone of the DGTO owner
        :parameter occ: occurrence of the DGTO owner
        :returns: list[int]: value of DGTO if names are valid, otherwise None\n

        description: Read multiple DGTO by given name or code, if not found will be skipped\n
        remarks: This function cannot be used to read phantom DGTO\n
        """
        if len(array_dgto) > 8:
            array_dgto_address = []
            array_dgto_text = []
            is_mi = False

            for i in range(len(array_dgto)):
                # Searching DGTO on Phantom Excel file
                dgto_phantom = self._search_phantom(array_dgto[i])

                if dgto_phantom is not None:
                    self._report.add_comment_row(
                            f"WARNING: DGTO {array_dgto[i]} is a phantom and does not support multiple reads. It will be skipped from multiread.",
                            background_color="WARNING", print_on_console=True)
                else:
                    address, name, code = self._search_dgto(array_dgto[i])

                    if name is not None and code is not None:
                        dgto_text_info = f"{name} ({code})"
                    elif name is not None:
                        dgto_text_info = f"{name} ({array_dgto[i]})"
                    else:
                        dgto_text_info = array_dgto[i]

                    if cat is not None and zone is not None and occ is not None:
                        dgto_text_info = f"{dgto_text_info} 0x{cat:02x}/0x{zone:02x}/0x{occ:02x}"
                        is_mi = True

                    if address == 0:
                        return None
                    else:
                        array_dgto_address.append(address)
                        array_dgto_text.append(dgto_text_info)

            if is_mi:
                result = self._api.ReadDGTOList_MI(cat, zone, occ, array_dgto_address)
            else:
                result = self._api.ReadDGTOList(array_dgto_address)

            if result[0] != EErrors.E_OK:
                result = result[1]
                self._report.print_on_console(
                        f"An error occurred during reading operation: DGTO List has not been read {result}")
                self._report.add_action_row(
                        self._options["device"], self._actions["READ"], "DGTO List", None,
                        "Values List",
                        self._results["ERROR"], f"Error occurred during reading DGTO List operation {result}")
                return None

            if not skipComment:
                for i in range(len(result)):
                    self._report.print_on_console(f"DGTO {array_dgto_text[i]} = {result[i]}")
                    self._report.add_action_row(
                            self._options["device"], self._actions["READ"], array_dgto_text[i], result[i], None,
                            self._results["SUCCESS"], None)

        else:
            self._report.print_on_console("ERROR! multiread_dgto can read max 8 dgto at the same time")

        return result


    def write_dgto(self, dgto_name: str, value: int, check_time: int = None, skip_write_check: bool = False,
                   cat: int = None, zone: int = None, occ: int = None) -> bool:
        """
        SW spec :n.a.\n
        :parameter self:  class instance\n
        :parameter dgto_name:  dgto name [string]\n
        :parameter value:  the value to write[int]\n
        :parameter check_time:  Not used [int]\n
        :parameter skip_write_check: if false the true check is disabled, only single write. [bool]\n
                        false enable the writing check [bool].\n
        :parameter cat: category of the DGTO owner
        :parameter zone: zone of the DGTO owner
        :parameter occ: occurrence of the DGTO owner

        :return: bool : true if writing operation has been completed successfully\n
                       false if writing operation has been completed unsuccessfully [bool]\n

        description: Perform a single write operation of specific incoming data (value) on passed DGTO\n
        remarks : none\n
        """

        # Searching DGTO on Phantom Excel file
        dgto_phantom = self._search_phantom(dgto_name)

        # Check if Phantom DGTO has been found
        if dgto_phantom[0] is not None:
            dgto_code = dgto_phantom[2]
            name = dgto_phantom[3]
            code = dgto_phantom[4]

        # Searching DGTO on Generic Excel file
        else:
            dgto_code, name, code = self._search_dgto(dgto_name)
            if dgto_code == 0:
                return False

        # Searching DGTO on Probe Excel file
        probe_index = self._search_probe(dgto_code)

        if probe_index > 0:
            check_time = self._default_write_check_time_probe if check_time is None else check_time
            return self._write_probe(dgto_name, probe_index, value, check_time, skip_write_check, name, code)
        elif dgto_phantom[0] is None:
            check_time = self._default_write_check_time_dgto if check_time is None else check_time
            return self._write_generic_dgto(dgto_name, dgto_code, value, check_time, skip_write_check, name, code, cat,
                                            zone, occ)
        else:
            dgto_phantom_address = dgto_phantom[0]
            dgto_phantom_type = dgto_phantom[1]
            check_time = self._default_write_check_time_dgto if check_time is None else check_time
            return self._write_phantom_dgto(dgto_name, dgto_phantom_address, dgto_phantom_type, value, check_time,
                                            skip_write_check, name, code, cat, zone, occ)


    def multiwrite_dgto(self, array_dgto: list, array_values: list, skip_write_check: bool = False,
                        check_time: int = None,
                        cat: int = None, zone: int = None, occ: int = None) -> bool:
        """
        SW spec :NA\n
        :parameter self:  class instance\n
        :parameter array_dgto:  list name of involved dgto, NO PROBES NO PHANTOM, max 8 items [str]\n
        :parameter array_values:  list of  value to write, max 8 items  [int]\n
        :parameter skip_write_check: if True the reading check after the writing operation will be skipped
        :parameter check_time:  seconds to wait after each check [int]\n
        :parameter cat: category of the DGTO owner
        :parameter zone: zone of the DGTO owner
        :parameter occ: occurrence of the DGTO owner
        :returns: True if DGTO assumed the desired value, otherwise False [bool]\n

        description	:If dgto==0 ,return False ,else by looping the step time<expected timer if response!=0 error during\n
                             reading ,else DGTO correctly read then expected value is not none, check the expected value in\n
                             range else return not the expected Value ,if the value is not a desired value increase the\n
                             timer,if expected value is none no change in values else value not set return as False\n

        remarks: The number of DGTO than can be written is limited by the device receiving buffer,
                 if the operation fails try to write less DGTO at the same time
                 This function cannot be used to write phantom or probes DGTO
        """

        check_time = self._default_write_check_time_dgto if check_time is None else check_time

        # check if the length of arrays is the same
        if len(array_values) == len(array_dgto) or len(array_dgto) > 8:
            array_dgto_address = []
            array_dgto_text = []
            is_mi = False

            for i in range(len(array_dgto)):
                # Searching DGTO on Probe Excel file
                probe_index = self._search_probe(array_dgto[i])
                # Searching DGTO on Phantom Excel file
                dgto_phantom = self._search_phantom(array_dgto[i])

                if probe_index > 0 or dgto_phantom is not None:
                    if probe_index > 0:
                        self._report.add_comment_row(
                                f"WARNING: DGTO {array_dgto[i]} is a probe and does not support multiple writes. It will be skipped from multiwrite.",
                                background_color="WARNING", print_on_console=True)
                    else:
                        self._report.add_comment_row(
                                f"WARNING: DGTO {array_dgto[i]} is a phantom and does not support multiple writes. It will be skipped from multiwrite.",
                                background_color="WARNING", print_on_console=True)
                else:
                    address, name, code = self._search_dgto(array_dgto[i])

                    if name is not None and code is not None:
                        dgto_text_info = f"{name} ({code})"
                    elif name is not None:
                        dgto_text_info = f"{name} ({array_dgto[i]})"
                    else:
                        dgto_text_info = array_dgto[i]

                    if cat is not None and zone is not None and occ is not None:
                        dgto_text_info = f"{dgto_text_info} 0x{cat:02x}/0x{zone:02x}/0x{occ:02x}"
                        is_mi = True

                    if address == 0:
                        return False
                    else:
                        array_dgto_address.append(address)
                        array_dgto_text.append(dgto_text_info)

            self._report.print_on_console(f"Writing DGTO List {array_dgto_text} with values {array_values} ...")

            if is_mi:
                result = self._api.WriteDGTOList_MI(cat, zone, occ, array_dgto_address, array_values)
            else:
                result = self._api.WriteDGTOList(array_dgto_address, array_values)

            if result != EErrors.E_OK:
                self._report.print_on_console(
                        f"An error occurred during writing operation: DGTO List has not been written {result}")
                self._report.add_action_row(
                        self._options["device"], self._actions["WRITE"], "DGTO List", None,
                        "Values List",
                        self._results["ERROR"], f"Error occurred during writing DGTO List operation {result}")
                return False

            if not skip_write_check:
                self.wait_time(check_time)

                if is_mi:
                    result = self._api.ReadDGTOList_MI(cat, zone, occ, array_dgto_address)
                else:
                    result = self._api.ReadDGTOList(array_dgto_address)

                if result[0] != EErrors.E_OK:
                    return False

                read_values = result[1]
                errors = 0
                for i in range(len(read_values)):
                    if read_values[i] != array_values[i]:
                        errors = errors + 1
                        self._report.print_on_console(
                                f"WARNING: DGTO {array_dgto_text[i]} has been NOT written with value {str(array_values[i])}")
                        self._report.add_action_row(
                                self._options["device"], self._actions["WRITE"], array_dgto_text[i], None,
                                array_values[i],
                                self._results["WARNING"], "NOT written with value")
                    else:
                        self._report.print_on_console(
                                f"DGTO {array_dgto_text[i]} has been written correctly with value {str(array_values[i])}")
                        self._report.add_action_row(
                                self._options["device"], self._actions["WRITE"], array_dgto_text[i], None,
                                array_values[i],
                                self._results["SUCCESS"], None)

                return errors == 0
        else:
            if len(array_values) != len(array_dgto):
                self._report.print_on_console("ERROR! The number of elements of the arrays are not the same")
            else:
                self._report.print_on_console("ERROR! multiwrite_dgto can write max 8 dgto at the same time")

        return False


    def ping_dgto(self, dgto: str, expected_value: int, step_time: int = 1, expire_time: int = 60, cat: int = None,
                  zone: int = None, occ: int = None) -> bool:
        """
        SW spec :NA\n
        self: class instance\n
        :parameter dgto:   name of dgto [str]\n
        :parameter expected_value:  expected value to assume after expire_time [int]\n
        :parameter step_time:  seconds to wait after each check [int]\n
        :parameter expire_time:  seconds to wait for the change [int]\n
        :parameter cat: category of the DGTO owner
        :parameter zone: zone of the DGTO owner
        :parameter occ: occurrence of the DGTO owner
        :returns: True if DGTO assumed the desired value, otherwise False [bool]\n

        description: If dgto == 0, return False ,else by looping the step time < expected timer\n
                    if response != 0 error during reading,
                    else DGTO correctly read then expected value is not none, check the expected value in range\n
                    else return not the expected Value, if the value is not a desired value increase the\n
                    timer, if expected value is none no change in values else value not set return as False\n
        remarks: none
        """
        if step_time % 1 != 0:
            self._report.add_comment_row(
                    f"Warning! ping_dgto step_time can be only an integer value higher or equal to 0s, step_time rounded to {step_time}",
                    print_on_console=True, background_color="WARNING")
            step_time = round(step_time, 0)

        # variable used to count time of steps
        my_timer = 0.0

        value = None

        # Searching DGTO on Excel file
        dgto_code, name, dgto_str_code = self._search_dgto(dgto)

        if name is not None and dgto_str_code is not None:
            dgto_text_info = f"{name} ({dgto_str_code})"
        else:
            dgto_text_info = dgto

        if cat is not None and zone is not None and occ is not None:
            dgto_text_info = f"{dgto_text_info} {hex(cat)}/{hex(zone)}/{hex(occ)}"

        if dgto_code == 0:
            # return "FALSE", because DGTO DOESN'T assumed the desired value
            return False
        else:
            self._report.print_on_console(f"Pinging DGTO {dgto_text_info}...")
            # iterative condition (exits after the expires time or when the ping value is reached)
            while my_timer < expire_time:

                # Reading DGTO
                if cat is None or zone is None or occ is None:
                    response = self._api.ReadDGTO(dgto_code)
                else:
                    response = self._api.ReadDGTO_MI(cat, zone, occ, dgto_code)

                value = response[1]
                if response[0] != EErrors.E_OK:
                    # DGTO NOT read
                    self._report.print_on_console(
                            f"An error (EErrors code = {response}) occurred during reading operation: DGTO {dgto_text_info} has not been read")
                    self._report.add_action_row(
                            self._options["device"], self._actions["PING"], dgto_text_info, None, None,
                            self._results["ERROR"], "Error occurred during reading operation")

                    # increment time
                    self.wait_time(step_time)
                    my_timer = my_timer + step_time
                else:
                    # DGTO correctly read
                    if value == expected_value:  # Check if the value read is the desired value
                        self._report.print_on_console(
                                f"Now DGTO {dgto_text_info} = {str(value)} after {str(my_timer)}s")
                        self._report.add_action_row(
                                self._options["device"], self._actions["PING"], dgto_text_info, value,
                                expected_value,
                                self._results["SUCCESS"],
                                f"Value set after {str(my_timer)}s")

                        # return "TRUE", because DGTO assumed the desired value
                        return True
                    else:  # The value read is NOT the desired value, so the time is incremented
                        self.wait_time(step_time)
                        my_timer = my_timer + step_time

            # The time expires
            self._report.print_on_console(
                    f"After {str(my_timer)}s, DGTO {dgto_text_info} is NOT set to {str(expected_value)}. The current value is "
                    f"{str(value)}")
            self._report.add_action_row(
                    self._options["device"], self._actions["PING"], dgto_text_info, value,
                    expected_value,
                    self._results["WARNING"], f"Value not set after {str(my_timer)}s.")

            # return "FALSE", because DGTO DOESN'T assumed the desired value
            return False


    def multiping_dgto(self, array_dgto: list, array_expected_values: list, step_time: int = 1,
                       expire_time: int = 60, cat: int = None, zone: int = None, occ: int = None) -> list:
        """
        SW spec : NA\n

        :parameter self: class instance\n
        :parameter array_dgto: list of all dgtos to write [list]\n
        :parameter array_expected_values: list of all values [list] \n
        :parameter step_time: seconds to wait after each check [int]\n
        :parameter expire_time: seconds to wait the changing [int = 60]\n
        :parameter cat: category of the DGTO owner
        :parameter zone: zone of the DGTO owner
        :parameter occ: occurrence of the DGTO owner
        :returns:  values: list with Values\n

        description :This function pings the value of an array of DGTOs until them assume the
                    desired values or the waiting time expires.\n
                    If leng of the dgto and expected value equals ,read the dgto if response!=0 ,\n
                    its an error else Check the value read is the desired value, \n
                    the time needed to ping the value of a DGTO for the first time,\n
                    increment counter and save the value,if pingtime==my_timer \n
                    ALL DGTOs are NOT the desired value once time expires check for\n
                    NOT ALL DGTOs have assumed the desired value , if the lengths\n
                    of the two arrays are not the same is the final o/p \n
        remarks	: Ping time,my_timer,step_time are the most important one\n
        """
        read_values = list()

        if step_time % 1 != 0:
            step_time = round(step_time, 0)
            self._report.add_comment_row(
                    f"Warning! multiping_dgto step_time can be only an integer value higher or equal to 0s, step_time rounded to {step_time}",
                    print_on_console=True, background_color="WARNING")

        # check if the length of arrays is the same
        if len(array_expected_values) == len(array_dgto) or len(array_dgto) > 8:
            array_dgto_address = []
            array_dgto_text = []
            is_mi = False

            for i in range(len(array_dgto)):
                address, name, code = self._search_dgto(array_dgto[i])

                if name is not None and code is not None:
                    dgto_text_info = f"{name} ({code})"
                elif name is not None:
                    dgto_text_info = f"{name} ({array_dgto[i]})"
                else:
                    dgto_text_info = array_dgto[i]

                if cat is not None and zone is not None and occ is not None:
                    dgto_text_info = f"{dgto_text_info} 0x{cat:02x}/0x{zone:02x}/0x{occ:02x}"
                    is_mi = True

                if address == 0:
                    return read_values
                else:
                    array_dgto_address.append(address)
                    array_dgto_text.append(dgto_text_info)

            cur_time = 0
            dgto_list_len = len(array_expected_values)
            dgto_printed = []

            for i in range(dgto_list_len):
                dgto_printed.append(False)

            while cur_time < expire_time:
                if is_mi:
                    result = self._api.ReadDGTOList_MI(cat, zone, occ, array_dgto_address)
                else:
                    result = self._api.ReadDGTOList(array_dgto_address)

                if result[0] != EErrors.E_OK:
                    self._report.print_on_console(
                            f"An error occurred during reading operation: DGTO list {array_dgto_text} has not been read")
                    self._report.add_action_row(
                            self._options["device"], self._actions["PING"], array_dgto_text,
                            None, None, self._results["ERROR"], "Error occurred during reading operation")
                else:
                    read_values = result[1]
                    n_checked = 0

                    for i in range(dgto_list_len):
                        if array_expected_values[i] == read_values[i] and not dgto_printed[i]:
                            self._report.print_on_console(
                                    f"Now DGTO {array_dgto_text[i]} = {str(read_values[i])} (after {str(cur_time)}s)")
                            self._report.add_action_row(
                                    self._options["device"], self._actions["PING"],
                                    array_dgto_text[i],
                                    read_values[i], array_expected_values[i],
                                    self._results["SUCCESS"],
                                    f"Value set after {str(cur_time)}s")
                            dgto_printed[i] = True
                            n_checked = n_checked + 1

                    if n_checked == dgto_list_len:
                        return read_values

                # The values read of ALL DGTOs are NOT the desired value, so the time is incremented
                self.wait_time(step_time)
                cur_time = cur_time + step_time

            for i in range(dgto_list_len):
                if not dgto_printed[i]:
                    self._report.print_on_console(
                            f"After {str(cur_time)}s, DGTO {array_dgto_text[i]} is NOT set to "
                            f"{str(array_expected_values[i])}. The current value is {str(read_values[i])}")
                    self._report.add_action_row(
                            self._options["device"], self._actions["PING"], array_dgto_text[i],
                            read_values[i], array_expected_values[i], self._results["WARNING"],
                            f"Value not set after {str(cur_time)}s.")
        else:
            self._report.print_on_console(f"The number of elements of the arrays are not the same")

        return read_values


    def detect_dgto_change(self, dgto: str, expected_value: int = None, step_time: int = 1, expire_time: int = 60,
                           cat: int = None,
                           zone: int = None, occ: int = None) -> bool:
        """
        Sw spec	:NA\n

        :parameter self: class instance\n
        :parameter dgto: list of all dgto to write[str]\n
        :parameter expected_value: expected value to assume after expire_time [int]\n
        :parameter step_time: seconds to wait after each check [int]\n
        :parameter expire_time: seconds to wait the changing [int]\n
        :parameter cat: category of the DGTO owner
        :parameter zone: zone of the DGTO owner
        :parameter occ: occurrence of the DGTO owner
        :returns: False if DGTO name is wrong;\n
                        True  if the value changes to the expected value;\n
                        string value if the value doesn't change to the expected value, new value is returned\n

        description	: This function check if DGTO change its value and assumes the desired value.\n
                    If dgto==0 ,check the initial value by looping the step time<expected timer\n
                    if response!=0 error during reading ,else DGTO correctly read\n
                    then expected value is not none check the expected value in range
                    else return not the expected Value ,\n
                    if the value is not a desired value increase the timer,\n
                    if expected value is none no change in values else value not set\n

        remarks : none
        """
        if step_time % 1 != 0:
            step_time = round(step_time, 0)
            self._report.add_comment_row(
                    f"Warning! detect_dgto_change step_time can be only an integer value higher or equal to 0s, step_time rounded to {step_time}",
                    print_on_console=True, background_color="WARNING")
        # variable used to count time of steps
        my_timer = 0.0
        is_mi = None
        initial_value = None
        # Searching DGTO on Excel file
        dgto_code, name, code = self._search_dgto(dgto)

        if name is not None and code is not None:
            dgto_text_info = f"{name} ({code})"
        else:
            dgto_text_info = dgto

        if cat is not None and zone is not None and occ is not None:
            dgto_text_info = f"{dgto_text_info} {hex(cat)}/{hex(zone)}/{hex(occ)}"
            is_mi = True

        if dgto_code == 0:
            return False
        else:
            # read initial value
            if is_mi:
                response = self._api.ReadDGTO_MI(cat, zone, occ, dgto_code)
            else:
                response = self._api.ReadDGTO(dgto_code)

            value = response[1]
            if response[0] == EErrors.E_OK:
                initial_value = value

            self._report.print_on_console(f"Waiting DGTO {dgto_text_info} changes...")
            # iterative condition (exits after the expires time or when the ping value is reached)
            while my_timer < expire_time:

                # Reading DGTO
                if is_mi:
                    response = self._api.ReadDGTO_MI(cat, zone, occ, dgto_code)
                else:
                    response = self._api.ReadDGTO(dgto_code)

                value = response[1]

                if response[0] != EErrors.E_OK:
                    # DGTO NOT read
                    self._report.print_on_console(
                            f"An error occurred during reading operation: DGTO {dgto_text_info} has not been read")
                    self._report.add_action_row(
                            self._options["device"], self._actions["CHANGE"], dgto_text_info, None, None,
                            self._results["ERROR"], "Error occurred during reading operation")

                    # increment time
                    self.wait_time(step_time)
                    my_timer = my_timer + step_time

                else:
                    # DGTO correctly read
                    if value != initial_value:  # Check if the value read is the desired value
                        if expected_value is not None:
                            if (isinstance(expected_value, range) and value in expected_value) or (
                                    not isinstance(expected_value, range) and value == expected_value):
                                self._report.print_on_console(
                                        f"DGTO {dgto_text_info} changed value to expected {str(value)} after {str(my_timer)}s")
                                self._report.add_action_row(
                                        self._options["device"], self._actions["CHANGE"], dgto_text_info,
                                        value, expected_value,
                                        self._results["SUCCESS"],
                                        f"Value set after {str(my_timer)}s")

                                return True
                            else:
                                self._report.print_on_console(
                                        f"DGTO {dgto_text_info} changed value to {str(value)}, not to {expected_value}, "
                                        f"after {str(my_timer)}s")
                                self._report.add_action_row(
                                        self._options["device"], self._actions["CHANGE"], dgto_text_info,
                                        value, expected_value,
                                        self._results["WARNING"],
                                        f"Value not changed after {str(my_timer)}s.")
                                return value

                        else:
                            self._report.print_on_console(
                                    f"DGTO {dgto_text_info} changed value to {str(value)}, "
                                    f"after {str(my_timer)}s")
                            self._report.add_action_row(
                                    self._options["device"], self._actions["CHANGE"], dgto_text_info,
                                    value, None,
                                    self._results["SUCCESS"],
                                    f"Value changed after {str(my_timer)}s.")
                            return value

                    else:  # The value read is NOT the desired value, so the time is incremented
                        self.wait_time(step_time)
                        my_timer = my_timer + step_time

            # The time expires
            if expected_value is None:
                self._report.print_on_console(
                        f"After {str(my_timer)}s, DGTO {dgto_text_info} has NOT changed its value. The current value "
                        f"is "
                        f"{str(value)}")
                self._report.add_action_row(
                        self._options["device"], self._actions["CHANGE"], dgto_text_info, value,
                        "", self._results["WARNING"], f"Value not set after {str(my_timer)}s.")
            else:
                self._report.print_on_console(
                        f"After {str(my_timer)}s, DGTO {dgto_text_info} is NOT set to {str(expected_value)}. The current value "
                        f"is "
                        f"{str(value)}")
                self._report.add_action_row(
                        self._options["device"], self._actions["CHANGE"], dgto_text_info, value,
                        expected_value, self._results["WARNING"], f"Value not set after {str(my_timer)}s.")

        return False


    def read_dgto_range(self, dgto_name: str, cat: int = None, zone: int = None, occ: int = None) -> tuple[
        int, int, int, int]:
        """
        Sw Spec	: Na
        :parameter self: instance class
        :parameter dgto_name: name of the DGTO to search[str]
        :parameter cat: category of the DGTO owner
        :parameter zone: zone of the DGTO owner
        :parameter occ: occurrence of the DGTO owner
        :returns: tuple with min value, max value, default value, current value if the condition is satisfied.
                  Else returns all None.

        :Description : Get information about the values of given DGTO
                      Search for the code of DGTO. Create a message tuple. Call Raw_Request function.
                      It needs a frame type and a list with the message. Check for any error.
                      If no error check if it is an 8 bit DGTO or a 16 bit DGTO.
                      If dgto_splitted[2]=1 or 2 else if 3 else return min_value, max_value, default_value, current_value.
                      If any error print an error occurred during RAW request function. And return false
        Remarks : none
        """
        min_value = None
        max_value = None
        default_value = None
        current_value = None

        # Search the code of DGTO
        dgto_code, name, code = self._search_dgto(dgto_name)  # "dgto_Code" is and integer

        # Create the message tuple

        msg = _split_hex(dgto_code)

        # Use the RAW_Request function

        total_data_return = self._raw_request(0x25, msg, cat, zone, occ)

        # Check for any error

        if total_data_return[0]:  # No errors in RAW_Request function

            # Use only the buffer returned

            buff_data = total_data_return[2]

            # Check if it is an 8 bit DGTO or a 16 bit DGTO
            dgto_splitted = convert_hex_to_dgto(dgto_code)
            dgto_splitted = dgto_splitted.split("-")

            # it is a 16 bit DGTO, UNSIGNED SHORT (uint16_t)
            if dgto_splitted[2] == "1" or dgto_splitted[2] == "2":

                current_value = _merge_hex((buff_data[1], buff_data[0]))
                min_value = _merge_hex((buff_data[3], buff_data[2]))
                max_value = _merge_hex((buff_data[5], buff_data[4]))
                default_value = _merge_hex((buff_data[7], buff_data[6]))

            # it is a 16 bit DGTO, SIGNED SHORT (int16_t)
            elif dgto_splitted[2] == "3":

                current_value = _merge_hex((buff_data[1], buff_data[0]), True)
                min_value = _merge_hex((buff_data[3], buff_data[2]), True)
                max_value = _merge_hex((buff_data[5], buff_data[4]), True)
                default_value = _merge_hex((buff_data[7], buff_data[6]), True)

            else:  # it is an 8 bit DGTO
                current_value = buff_data[0]
                min_value = buff_data[1]
                max_value = buff_data[2]
                default_value = buff_data[3]
        else:  # Any error in RAW_Request function
            print(f"An error occurred during RAW Request function!")

        return min_value, max_value, default_value, current_value


    """ ---------------- End: DGTO functions --------------- """

    """ ---------------- Start: Utilities functions --------------- """


    def read_memory(self, mem_address: int, num_byte_rx: int) -> tuple[bool, int]:
        """
        Sw spec :NA
        :parameter self: : class instance
        :parameter mem_address: integer that contains the address in RAM memory of the frame requested [int]\n
        :parameter num_byte_rx: indicates the number of bytes that will be received [int]\n
        :returns: tuple[bool, int] with the result of the operation (True/False) and the value read

        description: This function reads a frame of RAM data by direct access to the internal memory (RAM/ROM or EEPROM)\n
            If the dllhandler read memory =  false, for no of bytes read with in the Value\n
            (try the second value is > first value)it will add to list and print ,else return false\n

        Remarks	:Create the variable for RAM Address, Buffer and no of bytes to read\n
        """
        # create a buff rx, IL BUFFER DEVE ESSERE "unsigned byte", altrimenti me lo tira fuora come complemento a 2 TODO: Verificare se ancora vero dopo il porting (probabilmente no)
        buf = (ctypes.c_ubyte * num_byte_rx)()

        # Call function "ReadMemory()"
        response = self._api.ReadMemory(mem_address, num_byte_rx, buf)

        if response == EErrors.E_OK:
            data_list = []

            for i in range(num_byte_rx):
                try:
                    data_list.append(buf[i])  # il secondo elemento è il BYTE alto, il primo byte è quello basso
                except:
                    return False, None

            return True, data_list

        else:
            return False, None


    def write_memory(self, mem_address: int, data: list[int], cat: int = None, zone: int = None,
                     occ: int = None) -> bool:
        """
        Sw spec :NA\n
        :parameter self: class instance\n
        :parameter mem_address: RAM address [int]\n
        :parameter data: information to write in RAM [list of int]\n
        :returns:  True = Success or False = Unsuccessful [bool]\n
        description	This function write a frame in RAM data by direct\n
        access to the internal memory (RAM/ROM or EEPROM)\n
        remarks	: none
        """
        list_hex = []

        for i in range(0, 4, 1):
            num_hex_shift = mem_address >> (8 * i)
            num_hex_shift = num_hex_shift & 0xFF
            list_hex.append(num_hex_shift)

            mem_address = mem_address - (num_hex_shift << (8 * i))

        data_to_write = list_hex

        for i in range(len(data)):
            data_to_write.append((data[i]))

        # TODO: Aggiornare il metodo con la chiamata corretta alla WriteMemory (ancora non verificata), con questa modifica si perderebbe l'indicazione della CZO, da capire se necessaria

        return self._raw_message(0x30, data_to_write, cat, zone, occ)


    def wait_time(self, waiting_time: int) -> None:
        """
        Sw Spec	: Na\n
        :param self: class instance\n
        :param waiting_time: Waiting until the script gets Execute [int] \n
        :return values :None\n

        description :Let the waiting time to Execute until the script executed \n
                     and print the waiting time in Secs \n
                     Let the script wait until waiting time is expired \n
        remarks : none \n
        """
        if waiting_time % 1 != 0:
            waiting_time = round(waiting_time, 0)
            self._report.add_comment_row(
                    f"WARNING wait_time can be used only with integer value in seconds, automatically rounded to {waiting_time}s",
                    print_on_console=True, background_color="WARNING")
        else:
            self._report.add_comment_row(f"Waiting {waiting_time} seconds...")

        while waiting_time > 0:
            print(f"\rWait {waiting_time} seconds", end="")
            time.sleep(1)
            waiting_time -= 1

        print("")


    def _raw_request(self, frame_type, frame_msg, cat: int = None, zone: int = None, occ: int = None) -> tuple[
        bool, int, int]:
        """
        Sw Spec	: Na\n

        :parameter self: instance class\n
        :parameter frame_type: Any\n
        :parameter frame_msg: Any\n
        :parameter cat: category of the DGTO owner
        :parameter zone: zone of the DGTO owner
        :parameter occ: occurrence of the DGTO owner
        :returns: Bool :  tuple[bool, int, int] with operation result (True), data length and data value if operation success, otherwise False, None, None


        :Description :This function executes a raw request. It needs a frame type and a list with the message.\n
                     Defining a frame type and message and limit the variables to read max 32 to 2 bytes or 64 to 1 bytes\n
                     Create an array of bytes, with the length of "frame_msg"" elements, and it is automatically initialized\n
                     Create a byte with the length of "frame_msg". Create a byte array for the buffer\n
                     Create an integer for the buffer length. If not a Raw request Return true else return false\n
        Remarks : none\n
        """

        if cat is not None and zone is not None and occ is not None:
            raw_response = self._api.RAWRequest_MI(cat, zone, occ, frame_type, frame_msg)
        else:
            raw_response = self._api.RAWRequest(frame_type, frame_msg)

        value = raw_response[1]

        if raw_response[0] == EErrors.E_OK:
            return True, len(value), value

        return False, None, None


    def _raw_message(self, frame_type, frame_msg, cat: int = None, zone: int = None, occ: int = None) -> bool:
        """
        Sw Spec	: Na\n

        :parameter: self instance class\n
        :parameter: frame_type  Any\n
        :parameter: frame_msg  Any\n
        :parameter cat: category of the DGTO owner
        :parameter zone: zone of the DGTO owner
        :parameter occ: occurrence of the DGTO owner
        :returns: raw_message_response [bool] (True,False)\n
                        true if request condition has been satisfied\n
                        false if request condition has not satisfied\n

        Description : build a message from incoming data stream and message type information.    .
        remarks : none
        """

        if cat is not None and zone is not None and occ is not None:
            raw_response = self._api.RAWMessage_MI(cat, zone, occ, frame_type, frame_msg)
        else:
            raw_response = self._api.RAWMessage(frame_type, frame_msg)

        return raw_response == EErrors.E_OK

        # Nome da cambiare rimuovere set


    def operation_control_set(self, frame_id_op, frame_id_obj, frame_id_sub, frame_buf) -> bool:
        """
        Sw Spec	: Na
        :param self: instance class
        :param  frame_id_op:Any
        :param frame_id_obj: any
        :param frame_id_sub: any
        :param frame_buf: any
        :returns: Bool :  true if request condition has been satisfied.
                                false if request condition has not satisfied
        :Description : This function executes an Operation Control Set request.
                        It needs the IDs a list with the message. create variables needed. define frame buf:
                        create an array of bytes, whit the length of frame_buf elements, and it is automatically initialized.
                        create a byte with the length of frame_buf. Call function OperationControl.
                        If not operation control value return true else return false.
        Remarks : none
        """
        result = self._api.OperationControl(frame_id_op, frame_id_obj, frame_id_sub, frame_buf)

        if result != EErrors.E_OK:
            self._report.print_on_console(
                    f"An error (EErrors code = {result[0]}) occurred during OperationControl({frame_id_op}, {frame_id_obj}, {frame_id_sub}, {frame_buf}).")
            self._report.add_action_row(
                    self._options["device"], self._actions["WRITE"], f"OP Control Set", None, None,
                    self._results["ERROR"], "Error occurred during writing operation")

        return result == EErrors.E_OK


    def operation_control_get(self, frame_id_obj, frame_id_sub):
        """
        Sw Spec	: Na
        :param self: instance class
        :param frame_id_obj: any
        :param frame_id_sub: any

        :returns :  None if the request fails. Otherwise, returns the data retrieved from the command.

        :Description : This function executes an Operation Control Get request.
                        It needs the IDs a list with the message.
        Remarks : none
        """
        result = self._api.OperationControlGet(frame_id_obj, frame_id_sub)

        if result[0] != EErrors.E_OK:
            self._report.print_on_console(
                    f"An error (EErrors code = {result[0]}) occurred during OperationControlGet({frame_id_obj}, {frame_id_sub}).")
            self._report.add_action_row(
                    self._options["device"], self._actions["READ"], f"OP Control Get({frame_id_obj}, {frame_id_sub})",
                    None, None,
                    self._results["ERROR"], "Error occurred during reading operation")
            return None

        return result[1]


    def _read_id_table(self) -> tuple[bool, int, int]:  # Ticket #24
        """
        Sw Spec	: Na

        :param self: instance class
        :returns: "result" (Bool), "len_data.value" (int), "data_list[]", where:

                           "result" will be True if the operation success, otherwise false,
                           "len_data.value" will contain the length of data_list[] if the operation success, otherwise None,
                           "data_list[]" will contain the raw data readed from the ID Table if the operation success, otherwise None

        :Description : This function executes an ReadIdTable request.
                        Define frame buf: create an array of bytes, whit the length of frame_buf elements, and it is automatically initialized.
                        create a byte with the length of frame_buf. Call function ReadIdTable.
                        If not operation control value return true else return false.
        Remarks : none
        """
        raw_response = self._api.ReadIdTable()
        value = raw_response[1]
        result = raw_response[0] == EErrors.E_OK

        return result, len(value), value


    def suspend_com(self) -> bool:
        """
            Sw Spec	: Na

            :param self:    instance class
            :returns: True if the COM is suspended successfully, otherwise False

            :Description: This function suspend the use of the COM
            Remarks: none
        """
        result = False

        if self._com_status == 1:
            response = self._api.CommSuspend()
            result = response == EErrors.E_OK

            if result:
                self._com_status = 0  # Suspended
        else:
            self._report.add_comment_row("ERROR! Impossible to susped the COM, COM already suspended or closed.",
                                         print_on_console=True, background_color="ERROR")

        return result


    def resume_com(self) -> bool:
        """
            Sw Spec	: Na

            :param self:    instance class
            :returns: True if the COM is resumed successfully, otherwise False

            :Description: This function resume the COM
            Remarks: none
        """
        result = False

        if self._com_status == 0:

            for t in range(3):
                response = self._api.CommResume()
                result = response == EErrors.E_OK

                if result:
                    self._com_status = 1  # Open
                    break
                else:
                    self._report.add_comment_row("WARNING! Error during comm resume operation, retrying...",
                                                 print_on_console=True, background_color="WARNING")
                self.wait_time(3)

        else:
            if self._com_status == 1:
                self._report.add_comment_row("ERROR! Impossible to resume the COM, COM already open.",
                                             print_on_console=True, background_color="ERROR")
            else:
                self._report.add_comment_row("ERROR! Impossible to resume the COM, COM not initialized.",
                                             print_on_console=True, background_color="ERROR")

        return result


    def set_dgto_write_check_time(self, dgto_check_time: int) -> None:
        """
            Sw Spec	: Na

            :param self: instance class
            :param dgto_check_time: the new time to wait
            :returns: None

            :Description: Used to change the default waiting time before reading check operation after a writing on a DGTO
            Remarks: none
        """
        self._default_write_check_time_dgto = dgto_check_time


    def set_probe_write_check_time(self, probe_check_time: int) -> None:
        """
            Sw Spec	: Na

            :param self: instance class
            :param probe_check_time: the new time to wait
            :returns: None

            :Description: Used to change the default waiting time before reading check operation after a writing on a Probe
            Remarks: none
        """
        self._default_write_check_time_probe = probe_check_time


    """ ---------------- End: Utilities functions --------------- """
    """ ---------------- Start: Ares4 Test automation  --------------- """


    def set_channel_values(self, channels: list[int], values: list[int]) -> bool:
        """
        Sw Spec	: Na

        :param  self: instance class
        :param channels: list[int] of channels to write
        :param values: list[int] of values to write
        :returns: bool : True if values are written, otherwise False

        :Description : Set the values of probes by given channels. Check if the input list have not the same length.
                      Create the buff needed in operation_Controlset function. Split the channel and values in 2 bytes.
                      Call the function operation_Controlset.This function executes an operation control set request.
                      It needs the IDs a list with the message. Return true if the values are return otherwise return false
        Remarks : none
        """
        # Check if the input lists have not the same lenght

        if len(channels) != len(values):
            return False

        # create the buff needed in "Operatio_ControlSET" Function

        data_msg = [len(channels) * 4]

        for i in range(len(channels)):
            # Split the channels and values in 2 bytes

            tuple_channel = _split_hex(channels[i])
            tuple_values = _split_hex(values[i])

            # Add information in list
            data_msg.append(tuple_channel[0])
            data_msg.append(tuple_channel[1])
            data_msg.append(tuple_values[0])
            data_msg.append(tuple_values[1])

        # Call function "_operation_controlSet"

        # id_Op = SET (3), id_Obj = Test Automation (36), id_Sub = Set Channel Values (0)
        return self.operation_control_set(0x03, 0x24, 0x00, data_msg)


    def save_channel_values(self) -> bool:
        """
        Sw Spec	: Na

        :param self: instance class
        :returns:  Bool :  true if request condition has been satisfied
                                  false if request condition has not satisfied

        Description : Call function operation_control_set. This function executes an Operation Control Set request.
                      It needs the IDs a list with the message If the operation controls set has given hex value return
                      true else return false
        Remarks : none
        """
        # id_Op = SET (3), id_Obj = Test Automation (36), id_Sub = Save Current Values (1)
        return self.operation_control_set(0x03, 0x24, 0x01, [0x00])


    def restore_channel_values(self) -> bool:
        """
        Sw Spec	: Na

        :param self:     instance class
        :returns: Bool :  true if request condition has been satisfied
                        false if request condition has not satisfied

        :Description  :Call function operation_control_set. This function executes an Operation Control Set request.
                      It needs the IDs a list with the message.
                      if the operation controls set has given hex value return true else return false
        Remarks: none
        """
        # id_Op = SET (3), id_Obj = Test Automation (36), id_Sub = Save Current Values (1)
        return self.operation_control_set(0x03, 0x24, 0x02, [0x00])


    def get_channel_values(self, list_channels) -> tuple[bool, int]:
        """
        Sw Spec : n.a.
        :param self: instance class
        :param list_channels: {__len__, __getitem__}
        :return: tuple[bool, int] :  true if request condition has been satisfied
                        false if request condition has not satisfied

        :description   : Get the values of the channels (Test Automation).
                        Create the buffer needed in Raw_Request function and get the channel value.
                        Split the channels in 2 bytes.Add information in the list.
                        Then call function raw_Request. Check for any error.
                        If no error return true and channel value else return false

        Remarks None
        """

        # create the buff needed in "RAW_Request" Function

        data_msg = [0x02, 0x24, 0x00, len(list_channels) * 2]

        for i in range(len(list_channels)):
            # Split the channels in 2 bytes

            tuple_channel = _split_hex(list_channels[i])

            # Add information in list

            data_msg.append(tuple_channel[0])
            data_msg.append(tuple_channel[1])

        # Call function "RAW_Request"

        total_data_return = self._raw_request(0x52, data_msg)

        # Check for any error

        if total_data_return[0]:  # No errors in RAW_Request function

            # Use only the buffer returned

            buff_data = total_data_return[2]
            channel_value = []
            # The number of bytes is the double of the number of channels
            number_channels = total_data_return[1] // 2

            for i in range(number_channels):
                channel_value.append(
                        _merge_hex((buff_data[(2 * i) + 1], buff_data[2 * i])))

            return True, channel_value

        else:
            return False, None


    def send_pc_control_command(self, duration: int = 250) -> bool:
        """
        Sw Spec	: Na

        :param self:     instance class
        :param duration:     The duration in seconds of the pc control duration, 0 means PC Control OFF

        :returns: Bool :  true if request condition has been satisfied
                        false if request condition has not satisfied

        :Description  :Used to send the PC Control Command to the device, the PC Control status will be keeped
                       for duration seconds.
        Remarks: none
        """
        if duration > 255:
            self.add_comment_row(f"WARNING! PC Control Command duration can't be higher than 255s, "
                                 f"the value will be adjust to 255.",
                                 print_on_console=True, background_color="WARNING")
            duration = 255
        elif duration < 0:
            self.add_comment_row(f"WARNING! PC Control Command duration can't be lower than 0s, "
                                 f"the value will be adjust to 0.",
                                 print_on_console=True, background_color="WARNING")
            duration = 0

        self.add_comment_row(f"Sending PC Control Command to device with duration = {duration}...",
                             print_on_console=True)

        msg = bytearray([duration])

        return self._raw_message(0x50, msg)


    def SendRawMessageToEbus(self, packet_type: int, dest_address: int, msg: bytearray) -> bool:
        """
        Sw Spec : n.a.

        :param self: instance class
        :param packet_type: the type of the packet to sent (i.e. 0x2010)
        :param dest_address: the destination address for the packet (0xFE is the bradcast address)
        :param msg: the message to sent
        :return: bool: True if the message is correctly send on eBus, otherwise False

        :description   : Allows to send any eBus message from the connected device

        Remarks None
        """
        dest_address_str = f"0x{dest_address:02x}"
        packet_type_str = f"0x{packet_type:04x}"
        self._report.print_on_console(
                f"Sending {packet_type_str} packet type on eBus to device {dest_address_str} with values {msg}...")

        response = self._api.SetSenderDestinationAddress(0x7E)  # (7=PC E=Echo Area)

        if response != EErrors.E_OK:
            self._report.print_on_console(
                    f"An error occurred during Sending {packet_type_str} packet type on eBus to device {dest_address_str}: SetSenderDestinationAddress(0x7E) fail")
            self._report.add_action_row(
                    self._options["device"], self._actions["SEND"],
                    f"{packet_type_str} packet type on eBus to device {dest_address_str}", None, f"{msg}",
                    self._results["ERROR"],
                    "Error occurred during send on eBus operation: SetSenderDestinationAddress(0x7E) fail")
            return False

        response = self._api.RAWMessageToEBus(dest_address, packet_type, msg)

        if response != EErrors.E_OK:
            self._report.print_on_console(
                    f"An error occurred during Sending {packet_type_str} packet type on eBus to device {dest_address_str}: Packet not sent.")
            self._report.add_action_row(
                    self._options["device"], self._actions["SEND"],
                    f"{packet_type_str} packet type on eBus to device {dest_address_str}", None, f"{msg}",
                    self._results["ERROR"],
                    "Error occurred during send on eBus operation: RAWMessageToEBus fail")
            return False
        else:
            self._report.print_on_console(
                    f"eBus Packet {packet_type_str} to device {dest_address_str} has been sent on eBus correctly with value {msg}")
            self._report.add_action_row(
                    self._options["device"], self._actions["SEND"],
                    f"{packet_type_str} packet type on eBus to device {dest_address_str}", None, f"{msg}",
                    self._results["SUCCESS"], None)
            # Success

        response = self._api.SetSenderDestinationAddress(0x71)  # (7=PC 1=PrimaryBoard)

        if response != EErrors.E_OK:
            self._report.print_on_console(
                    f"An error occurred after Sending {packet_type_str} packet type on eBus to device {dest_address_str}:"
                    f"packet {msg} is sent but sender destination address is not restored")
            self._report.add_action_row(
                    self._options["device"], self._actions["SEND"],
                    f"{packet_type_str} packet type on eBus to device {dest_address_str}", None, f"{msg}",
                    self._results["ERROR"],
                    "Error occurred during send on eBus operation: SetSenderDestinationAddress(0x71) fail")
            return False

        return True


    def GetEbusTopology(self) -> list[tuple[int, int, int]]:
        """
        Sw Spec : n.a.

        :param self: instance class

        :return: list[tuple[int, int, int]]: a list of tuple[int, int, int]
        for the "Category / Zone / Occurrence" of every device present in the eBus topology

        :description   : Used to get the device presence on eBus

        Remarks None
        """

        self._report.print_on_console(
                f"Retrieving eBus topology...")

        end_reached = False
        devices = []
        i = 0
        while not end_reached:
            x = self._api.OperationControlGet(11, i)
            i = i + 1

            if x[0] != EErrors.E_OK:
                self._report.print_on_console(
                        f"An error occurred while retrieving eBus topology.")
                self._report.add_action_row(
                        self._options["device"], self._actions["RETRIEVE"],
                        "error occurred while retrieving eBus topology", None, None,
                        self._results["ERROR"],
                        f"Error occurred while retrieving eBus topology: OperationControlGet(11, {i}) failed.")
            else:
                row = x[1]

                if row[0] == 0xFF and row[1] == 0xFF and row[2] == 0xFF and row[3] == 0xFF:
                    end_reached = True
                else:
                    devices.append([row[3], row[1], row[2]])
                    self._report.print_on_console(
                            f"C/Z/O: 0x{row[3]:02x}/0x{row[1]:02x}/0x{row[2]:02x} founded")

        return devices


    def SendRawRequestToEbus(self, packet_type: int, dest_address: int, msg: bytearray) -> tuple[bool, int]:
        """
        Sw Spec : n.a.

        :param self: instance class
        :param packet_type: the type of the packet to sent
        :param dest_address: the destination address for the packet (0xFE is the bradcast address)
        :param msg: the request to sent
        :return: bool: True if the request is correctly send on eBus, otherwise False

        :description   : Allows to send any eBus request from the connected device

        Remarks None
        """
        result = None

        dest_address_str = f"0x{dest_address:02x}"
        packet_type_str = f"0x{packet_type:04x}"
        self._report.print_on_console(
                f"Sending {packet_type_str} packet type on eBus to device {dest_address_str} with values {msg}...")

        response = self._api.SetSenderDestinationAddress(0x7E)  # (7=PC E=Echo Area)

        if response != EErrors.E_OK:
            self._report.print_on_console(
                    f"An error occurred during Sending {packet_type_str} packet type on eBus to device {dest_address_str}: SetSenderDestinationAddress(0x7E) fail")
            self._report.add_action_row(
                    self._options["device"], self._actions["SEND"],
                    f"{packet_type_str} packet type on eBus to device {dest_address_str}", None, f"{msg}",
                    self._results["ERROR"],
                    "Error occurred during send on eBus operation: SetSenderDestinationAddress(0x7E) fail")
            return False, result

        response = self._api.RAWRequestToEBus(dest_address, packet_type, msg)

        if response[0] != EErrors.E_OK:
            self._report.print_on_console(
                    f"An error occurred during Sending {packet_type_str} packet type on eBus to device {dest_address_str}: Packet not sent.")
            self._report.add_action_row(
                    self._options["device"], self._actions["SEND"],
                    f"{packet_type_str} packet type on eBus to device {dest_address_str}", None, f"{msg}",
                    self._results["ERROR"],
                    "Error occurred during send on eBus operation: RAWRequestToEBus fail")
            return False, result
        else:
            self._report.print_on_console(
                    f"eBus Packet {packet_type_str} to device {dest_address_str} has been sent on eBus correctly with value {msg}")
            self._report.add_action_row(
                    self._options["device"], self._actions["SEND"],
                    f"{packet_type_str} packet type on eBus to device {dest_address_str}", None, f"{msg}",
                    self._results["SUCCESS"], None)
            # Success

        response = self._api.SetSenderDestinationAddress(0x71)  # (7=PC 1=PrimaryBoard)

        if response != EErrors.E_OK:
            result = response[1]
            self._report.print_on_console(
                    f"An error occurred after Sending {packet_type_str} packet type on eBus to device {dest_address_str}:"
                    f"packet {msg} is sent but sender destination address is not restored")
            self._report.add_action_row(
                    self._options["device"], self._actions["SEND"],
                    f"{packet_type_str} packet type on eBus to device {dest_address_str}", None, f"{msg}",
                    self._results["ERROR"],
                    "Error occurred during send on eBus operation: SetSenderDestinationAddress(0x71) fail")
            return False, result

        return True, result


    def _writeBroadcastDGTOonEbus(self, command: int, dgto_name: str, value: int, check_time: int = 10,
                                  is_multiwrite: bool = False) -> bool:
        """
            Sw Spec : n.a.
            :param command: the command to use: Set 0x2020 or Send 0x2010
            :param dgto_name: the name of the DGTO to sent
            :param value: the value to set on DGTO
            :param check_time: seconds to wait in order to check if value it is written [int]
            :param is_multiwrite: if True, doesn't check the written value and not print message on console [bool]
            :returns: bool: True if the DGTO is correctly sent on eBus, otherwise False

            :description: Allows to send or set a DGTO on eBus using a 0x2010/0x2020 command (write send/set DGTO) to everyone (with 0xFE broadcast destination)

            Remarks None
        """
        dgto_code, name, code = self._search_dgto(dgto_name)

        if dgto_code == 0:
            return False

        if name is not None and code is not None:
            dgto_text_info = f"{name} ({code})"
        elif name is not None:
            dgto_text_info = f"{name} ({dgto_name})"
        else:
            dgto_text_info = dgto_name

        self._report.print_on_console(f"Sending {dgto_text_info} broadcast on eBus with value {str(value)} ...")

        dst_addr = 0xFE  # Broadcast destination address
        ebus_type = command

        dgto_l = dgto_code & 0x00FF
        dgto_h = dgto_code & 0xFF00
        dgto_h = dgto_h >> 8

        dgto_size, dgto_sign = _get_dgto_size_and_sign(code)

        if (dgto_sign == 0 and value < 0) or (dgto_size == 1 and value > 255) or \
                (dgto_size == 2 and dgto_sign == 0 and value > 65535) or \
                (dgto_size == 2 and dgto_sign == 1 and (value > 32767 or value < -32767)):
            return False

        if dgto_size == 1:
            frame_msg = bytearray([dgto_l, dgto_h, value])
        else:
            val_l = value & 0x00FF
            val_h = value & 0xFF00
            val_h = val_h >> 8
            frame_msg = bytearray([dgto_l, dgto_h, val_l, val_h])

        response = self._api.SetSenderDestinationAddress(0x7E)  # (7=PC E=Echo Area)

        if response != EErrors.E_OK:
            self._report.print_on_console(
                    f"An error occurred during sending broadcast on eBus operation: DGTO {dgto_text_info} has not been sent")
            self._report.add_action_row(
                    self._options["device"], self._actions["SEND"], dgto_text_info, None, value,
                    self._results["ERROR"],
                    "Error occurred during send on eBus operation: SetSenderDestinationAddress(0x7E) fail")
            return False

        response = self._api.RAWMessageToEBus(dst_addr, ebus_type, frame_msg)

        if not is_multiwrite:
            if response != EErrors.E_OK:
                self._report.print_on_console(
                        f"An error occurred during sending broadcast on eBus operation: DGTO {dgto_text_info} has not been sent")
                self._report.add_action_row(
                        self._options["device"], self._actions["SEND"], dgto_text_info, None, value,
                        self._results["ERROR"],
                        "Error occurred during send on eBus operation: RAWMessageToEBus fail")
                return False
            else:
                self.wait_time(check_time)
                current_value = self.read_dgto(dgto_name, True)

                if current_value == value:
                    self._report.print_on_console(
                            f"DGTO {dgto_text_info} has been sent on eBus correctly with value {str(value)}")
                    self._report.add_action_row(
                            self._options["device"], self._actions["SEND"], dgto_text_info, None, value,
                            self._results["SUCCESS"], None)
                    # Success
                else:
                    self._report.print_on_console(
                            f"WARNING: DGTO {dgto_text_info} has been NOT sent on eBus with value {str(value)}")
                    self._report.add_action_row(
                            self._options["device"], self._actions["SEND"], dgto_text_info, None, value,
                            self._results["WARNING"], "NOT sent on eBus with value")
                    return False

        response = self._api.SetSenderDestinationAddress(0x71)  # (7=PC 1=PrimaryBoard)

        if response != EErrors.E_OK:
            self._report.print_on_console(
                    f"An error occurred after sending broadcast on eBus operation: "
                    f"DGTO {dgto_text_info} is sent but sender destination address is not restored")
            self._report.add_action_row(
                    self._options["device"], self._actions["SEND"], dgto_text_info, None, value,
                    self._results["ERROR"],
                    "Error occurred during send on eBus operation: SetSenderDestinationAddress(0x71) fail")
            return False

        return True


    def WriteSendBroadcastDGTOonEbus(self, dgto_name: str, value: int, check_time: int = 10,
                                     is_multiwrite: bool = False) -> bool:
        """
            Sw Spec : n.a.

            :param dgto_name: the name of the DGTO to sent
            :param value: the value to set on DGTO
            :param check_time: seconds to wait in order to check if value it is written [int]
            :param is_multiwrite: if True, doesn't check the written value and not print message on console [bool]
            :returns: bool: True if the DGTO is correctly sent on eBus, otherwise False

            :description: Allows to send a DGTO on eBus using a 0x2010 command (write send DGTO) to everyone (with 0xFE broadcast destination)

            Remarks None
        """
        return self._writeBroadcastDGTOonEbus(0x2010, dgto_name, value, check_time, is_multiwrite)


    def WriteSetBroadcastDGTOonEbus(self, dgto_name: str, value: int, check_time: int = 10,
                                    is_multiwrite: bool = False) -> bool:
        """
            Sw Spec : n.a.

            :param dgto_name: the name of the DGTO to set
            :param value: the value to set on DGTO
            :param check_time: seconds to wait in order to check if value it is written [int]
            :param is_multiwrite: if True, doesn't check the written value and not print message on console [bool]
            :returns: bool: True if the DGTO is correctly sent on eBus, otherwise False

            :description: Allows to send a DGTO on eBus using a 0x2020 command (write set DGTO) to everyone (with 0xFE broadcast destination)

            Remarks None
        """
        return self._writeBroadcastDGTOonEbus(0x2020, dgto_name, value, check_time, is_multiwrite)


    def ReadTDA(self) -> str:  # Ticket #27
        """
            Sw Spec	: Na
            :param self:     instance class
            :returns: var res :str :  TDA value if the TDA reading operation is performed successfully, None if the reading operation fails

            :Description: Call function TDAReadInfo() This function read all the TDA from the main board.

            Remarks: none
        """
        EMPTY_TDA = bytearray(b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
        EMPTY_PLANT = bytearray(b'\xff\xff')

        res = None
        self._report.print_on_console(f"Reading TDA operation started")
        info = self._api.TDAReadInfo()
        tda_b = info[1].code
        plant_b = info[1].plant

        if info[0] == EErrors.E_OK:
            if tda_b != EMPTY_TDA:
                res = tda_b.decode('utf-8')
            else:
                res = ""

            if plant_b != EMPTY_PLANT:
                plant = plant_b.decode('utf-8')
            else:
                plant = ""

            self._report.print_on_console(f"TDA: {res}, Plant: {plant}")
        else:
            self._report.add_comment_row(
                    f"An error occurred during TDA reading operation: TDA has not been read",
                    background_color="ERROR", print_on_console=True)
            self._report.add_action_row(
                    self._options["device"], self._actions["READ"], "TDA", None, None,
                    self._results["ERROR"], "Error occurred during TDA reading operation")

        return res


    def WriteTDA(self, tda: str, plant: str = "") -> bool:  # Ticket #27
        """
            Sw Spec	: Na

            :param self:     instance class
            :param tda: a string containing the TDA board_code value (max 12 char, 6 Bytes)
            :param plant: a string containing the plant value to set
            :returns: bool :  true if the TDA writing operation is performed successfully, False if the writing operation fails

            :Description  :Call function TDAWriteInfo() and TDARegisterTest() This two functions write the TDA board_code, plant and test result on the main board.
            Remarks: none
        """
        self._report.print_on_console(f"Writing TDA operation started")

        if tda is None or plant is None or len(tda) > 12 or len(plant) > 2:
            self._report.print_on_console(
                    f"ERROR! Impossible to write TDA values\nWrong TDA {tda} or wrong Plant {plant}")
            return False

        result = self._api.TDAWriteInfo(tda, plant)

        if result != EErrors.E_OK:
            self._report.print_on_console(
                    f"An error occurred during TDA writing operation: TDA {tda} has not been written")
            self._report.add_action_row(
                    self._options["device"], self._actions["WRITE"], "TDA", None, tda,
                    self._results["ERROR"], "Error occurred during TDA writing operation")
            return False

        # Save the test result to enable the TDA
        self._api.TDARegisterTest(1)

        self._report.print_on_console(f"TDA successfully written!\nTDA: {tda}, Plant: {plant}")

        return True


    def readIdentTable(self) -> tuple[bool, dict]:  # Ticket #24
        """
            Sw Spec	: Na
            :param self:     instance class
            :returns: tuple[bool, dict] : "True", Result[] if request condition has been satisfied, where Result[] contains all IdentTable info
                                    "False", None if request condition has not satisfied
            :Description    :This function use a raw request to read a Specific Data (command = 0x24),
                            in this case the data is the Ident Table (ID_Msg = 0x00), if the data are received correctly
                            the function proceeds to extract all info of Ident Table (see doc. IdentTableType2_XvYY.docx)
            Remarks: none
        """
        self._report.print_on_console(f"Reading Ident Table operation started")

        total_data_return = self._read_id_table()

        if total_data_return is None or total_data_return[0] is None or not total_data_return[0] or len(
                total_data_return) != 3:
            print(f"ERROR!\nImpossible to read the Ident Table.")
            self._report.add_action_row(
                    self._options["device"], self._actions["READ"], "IdentTable", None, None,
                    self._results["ERROR"], "Error occurred during IdentTable reading operation")
            return False, None

        res_len = total_data_return[1]
        data = total_data_return[2]

        # Length check on length of IdentTable data
        if (res_len - 7) % 9 != 0:
            self._report.add_action_row(
                    self._options["device"], self._actions["READ"], "IdentTable", None, None,
                    self._results["ERROR"], "Error occurred during IdentTable reading operation")
            print(f"ERROR!\nLength of the IdentTable data readed doesn't match ({res_len}).")
            return False, None

        result = {}

        # Reading the IDTABLE_HEAD of the ID table
        identification = data[1]

        # 0 = Ident0 (BuiltIN Ident Table structure – no more supported)
        # 1 = Ident1 (SWE Gal2 and EVO Ident structure)
        # 2 = Ident2 (Type 2 Ident structure)
        ident = (identification & 0xF0) >> 4  # bit 7 to 4

        # Reading the endian
        # 0 = Little Endian
        # 1 = Big endian
        endian = (identification & 0x08) >> 3  # bit 3

        # Reading the evolution level inside the SW Platform
        # 0 = PSOLE
        # 1 = WHE/SWHP
        # 2 = ARES
        evolution = identification & 0x07  # bit 2, 1, 0

        result["ident"] = ident
        result["endian"] = endian
        result["evolution"] = evolution

        fw_version = f"{data[3]:02}.{data[4]:02}.{data[5]:02}"
        result["fw_version"] = fw_version

        n_block = data[6]
        result["n_logic_block"] = n_block

        # Reading of all IDTABLE_BLOCKLOGIC

        # Length check on length of blocklogic data (block dim: 9 byte)
        if (len(data) - 7) / 9 != n_block:
            print(f"ERROR!\nLength of BLOCKLOGIC to read ({n_block}) doesn't match.")
            self._report.add_action_row(
                    self._options["device"], self._actions["READ"], "IdentTable", None, None,
                    self._results["ERROR"], "Error occurred during IdentTable reading operation")
            return False, None

        block = []

        for i in range(n_block):
            start_block = 7 + (i * 9)  # Where 9 (bytes) is the length of every block info

            d_block = {"name": hex(data[start_block]), "physic_block": data[start_block + 1]}

            mem_attrib = data[start_block + 2]

            # Reading the WriteUnit
            # 0 = 0 = byte
            # 1 = 1 = word
            write_unit = mem_attrib & 0x01  # bit 1

            # Reading the Type
            # 0 = RAM
            # 1 = ROM
            # 2 = DATAFLASH
            # 3 = EEPROM
            type = (mem_attrib & 0x0E) >> 1  # bit 3 to 1

            # Reading the Page (microcontroller paging dimension)
            # 0 = 256
            # 1 = 128
            # 2 = 64
            # 3 = 32
            # 4 = 16
            # 5 = 8
            # 6 = 4
            # 7 = 2
            page = (mem_attrib & 0x70) >> 4  # bit 6 to 4

            # Reading the Sh (Shared)
            # 1 = the current Logic Block is stored in the same Physic Block of other Logic Blocks
            sh = (mem_attrib & 0x80) >> 6  # bit 7

            d_block["WriteUnit"] = write_unit
            d_block["Type"] = type
            d_block["Page"] = page
            d_block["Sh"] = sh

            d_block["address"] = data[start_block + 3]
            d_block["address"] = d_block["address"] << 8
            d_block["address"] = d_block["address"] + data[start_block + 4]
            d_block["address"] = d_block["address"] << 8
            d_block["address"] = d_block["address"] + data[start_block + 5]
            d_block["address"] = d_block["address"] << 8
            d_block["address"] = d_block["address"] + data[start_block + 6]
            d_block["address"] = d_block["address"]
            d_block["size"] = data[start_block + 7]
            d_block["size"] = d_block["size"] << 8
            d_block["size"] = d_block["size"] + data[start_block + 8]
            block.append(d_block)

        result["block_logic"] = block

        # Print the SW Ver to shows the correct reading of IdentTable
        self._report.print_on_console(f"IdentTable successfully readed!\nSW Ver. {result['fw_version']} readed.")

        return True, result


    def send_reset(self, time_before_reset: int = 3) -> bool:  # Ticket #36
        """
            Sw Spec	: Na

            :param self:    instance class
            :param time_before_reset:    the time to wait before the reset
            :returns: None

            :Description: This function use a raw request to send a reset command (0x53 ATG Command)
            Remarks: none
        """
        self._report.print_on_console(f"Reset operation started")

        data_msg = [time_before_reset]  # 3s the reset will occur at the end of 3s

        # Command 0x53 = "RESET COMMAND"
        total_data_return = self._api.RAWMessage(0x53, data_msg)

        return total_data_return == EErrors.E_OK


    def dfls_download(self, dfls_path, finished_good=None) -> bool:
        """
            Sw Spec	: Na

            :param self:    instance class
            :param dfls_path:    the path of the DFLS to download in the target device
            :param finished_good:    finished good serial number to write
            :returns: None

            :Description: This function allows to download a DFLS in the target device
            Remarks: none
        """
        res = False
        success = self._api.DflsMapDownload(dfls_path, finished_good)

        if success:
            self._report.print_on_console("DFLS download started")
            while True:
                success, info = self._api.GetDownloadInfo()
                self._report.print_on_console(f"{info=} status={ESetupStatus(info.status)}")
                if self._report.print_on_console.status == ESetupStatus.EDS_COMPLETE.value:
                    print(f"Download completed - {info=} status={ESetupStatus(info.status)}")
                    res = True
                    break
                time.sleep(1)
        else:
            self._report.print_on_console("Operation failed")

        return res


    """ ---------------- End: ARES4 TestAutomation --------------- """

    """ ---------------- Start: ARES5 TestAutomation --------------- """


    def _searchDataIDInfo(self, DataID, Field: int = None) -> tuple[int, str, str]:
        """
            Software Specification: N/A

            :param self: Instance of the class.
            :param DataID: Identifier of the data to retrieve.
            :param Field: Specific field within the DataID (if applicable).
            :returns: tuple[int, str, str] – A tuple containing:
                - data_id_int: Integer representation of the DataID address.
                - data_id_string: String representation of the DataID address.
                - data_id_name: Name of the DataID if found, otherwise None.

            :raises Ares5Error: If the Ares5Env object is not initialized or
                                if the format of the provided DataID is invalid.

            :description: Uses the Ares5Env object to retrieve information about the specified DataID.

            :remarks: None
        """

        if self._ares5_env is None:
            raise Ares5Error("Error: Cannot run 'read_DataId' without loading an Ares5 Env.XML.\n"
                             "To fix this, add the 'Ares5EnvSourcePath' entry "
                             "with the correct path to your Config.txt file.")

        data_id_string = None
        data_id_int = None
        data_id_name = None

        if type(DataID) == str:
            if IsDataID(DataID):  # DataID format correct Type-Index-Field
                data_id_string = DataID
                data_id_int = DATAID_to_int(DataID)
                data_id_name = self._ares5_env.GetDataNameFromID(DataID)

                if data_id_name is None:
                    print(f"WARNING! DataID: {data_id_string} not found in ENV DataID List")
                    self._report.add_action_row(
                            self._options["device"], self._actions["SEARCH"], data_id_string, None, None,
                            self._results["WARNING"], "DataID not found in ENV DataID list.")

                if Field is not None:
                    print(f"Warning: The DataID '{data_id_string}' already defines a Field. "
                          f"The additional provided Field '{Field}' will not be used.")
                    self._report.add_action_row(
                            self._options["device"], self._actions["SEARCH"], data_id_string, None, None,
                            self._results["WARNING"], f"The DataID already defines a Field."
                                                      f"The additional provided Field '{Field}' will not be used.")

            else:  # It could be a DataID name or an error
                data_id_name = DataID
                data_id_string = self._ares5_env.GetDataIDFromName(DataID)

                if data_id_string is None:
                    raise Ares5Error(f"Error: The DataID '{DataID}' could not be found. Please ensure it"
                                     f" follows the correct Type-Index-Field format or is a valid DataID name.\n"
                                     f"Also verify that the Env.XML file being used is the latest version.")

                if Field is None:
                    print(f"Warning: No Field was specified for DataID '{data_id_name}'.\n"
                          f"Field 0 will be used by default..")
                    self._report.add_action_row(
                            self._options["device"], self._actions["SEARCH"], data_id_name, None, None,
                            self._results["WARNING"], f"Warning: No Field was specified for DataID '{data_id_name}'.\n"
                                                      f"Field 0 will be used by default..")
                    data_id_string = f"{data_id_string}-0"
                else:
                    data_id_string = f"{data_id_string}-{Field}"

                data_id_int = DATAID_to_int(data_id_string)
        elif type(DataID) == int:
            data_id_int = DataID
            data_id_string = int_to_DATAID(DataID)
            data_id_name = self._ares5_env.GetDataNameFromID(data_id_string)

            if data_id_name is None:
                print(f"WARNING! DataID: {data_id_string} DataID not found in ENV DataID list")
                self._report.add_action_row(
                        self._options["device"], self._actions["SEARCH"], data_id_string, None, None,
                        self._results["WARNING"], "DataID not found in ENV DataID list.")

            if Field is not None:
                print(f"Warning: The DataID '{data_id_string}' already defines a Field. "
                      f"The additional provided Field '{Field}' will not be used.")
                self._report.add_action_row(
                        self._options["device"], self._actions["SEARCH"], data_id_string, None, None,
                        self._results["WARNING"], f"The DataID already defines a Field."
                                                  f"The additional provided Field '{Field}' will not be used.")
        else:
            raise Ares5Error("Error: The format of the provided DataID is invalid or unsupported.")

        return data_id_int, data_id_string, data_id_name  # Only data_id_name could be None


    def _searchCZOInfo(self, CZO: int) -> tuple[int, str, str]:
        """
            Software Specification: N/A

            :param self: Instance of the class.
            :param CZO: Identifier of the CZO info to retrieve.

            :returns: tuple[int, str, str] – A tuple containing:
                - CZO: Integer representation of the CZO address.
                - CZO_string: String representation of the CZO address.
                - CZO_info: Name of the CZO if found, otherwise None.

            :raises Ares5Error: If the Ares5Env object is not initialized.

            :description: Uses the Ares5Env object to retrieve information about the specified CZO.

            :remarks: None
        """
        if self._ares5_env is None:
            raise Ares5Error("Error: Cannot run 'read_DataId' without loading an Ares5 Env.XML.\n"
                             "To fix this, add the 'Ares5EnvSourcePath' entry "
                             "with the correct path to your Config.txt file.")

        CZO_string = f"0x{CZO:08x}"
        CZO_info = None

        if not self._ares5_env.CheckIfCZOisValid(CZO):
            print(f"Warning: The CZO entry '{CZO_string}' was not found in Env.XML.\n"
                  f"Please check if the value is correct.")
            self._report.add_action_row(
                    self._options["device"], self._actions["SEARCH"], CZO_string, None, None,
                    self._results["WARNING"], "CZO entry not found in Env.XML.")

        CZO_info = self._ares5_env.GetCZOLabel(CZO)

        return CZO, CZO_string, CZO_info  # Only CZO_info could be None


    def read_DataId(self, DataID, CZO: int, Offset: int = None, Field: int = None, SkipComment: bool = False):
        """
            Software Specification: N/A

            :param self: Instance of the class.
            :param DataID: Name or Code of the DataID to read. [str]
            :param CZO: CZO address associated with the DataID. [int]
            :param Offset: Offset used for Stream DataType only. [int]
            :param Field: Field of the DataID to read, applicable when searching by name. [int]
            :param SkipComment: If True, the comment will not be written to the report. [bool]

            :returns: Value(s) read from the DataID, depending on its DataType:
                - Standard: int – the value read, or None if the operation fails.
                - Array: list[int] – values read, or None if the operation fails.
                - Stream: list[int] – values read, or None if the operation fails.

            :raises Ares5Error: If the Ares5Env object is not initialized or
            if DataID is provided as a list instead of a single element.

            :description: Reads a DataID using either its name and field or its code and address.

            :remarks: None
        """
        if self._ares5_env is None:
            raise Ares5Error("Error: Cannot run 'read_DataId' without loading an Ares5 Env.XML.\n"
                             "To fix this, add the 'Ares5EnvSourcePath' entry "
                             "with the correct path to your Config.txt file.")
        if type(DataID) == list:
            raise Ares5Error("Error: The 'read_DataId' method only supports a single DataID. "
                             "To process multiple DataIDs, please use the 'read_DataIdList' method instead.")

        # TODO: To add conversion of float

        if isinstance(DataID, Enum):
            DataID = DataID.value

        if isinstance(CZO, Enum):
            CZO = CZO.value

        result = None
        data_id_int, data_id_string, data_id_name = self._searchDataIDInfo(DataID, Field)
        czo_int, czo_string, czo_info = self._searchCZOInfo(CZO)
        data_id_type, _, field_identifier, _ = self._ares5_env.GetDataIdDataTypeFieldInfo(data_id_string)

        if data_id_type == DataTypeFunction.DATA_TYPE_STANDARD:
            if data_id_name is None:
                dataid_text_info = f"{data_id_string} (DGTO {DATAID_to_DGTO(data_id_string)}) Field: {field_identifier}"
            else:
                dataid_text_info = f"\"{data_id_name}\".{field_identifier} ({data_id_string}) " \
                                   f"(DGTO {DATAID_to_DGTO(data_id_string)})"
        else:
            if data_id_name is None:
                dataid_text_info = f"{data_id_string} Field: {field_identifier}"
            else:
                dataid_text_info = f"\"{data_id_name}\".{field_identifier} ({data_id_string})"

        if czo_info is None:
            czo_text_info = self._options['device']
            dataid_text_info = f"{dataid_text_info} on CZO: {czo_string}"
        else:
            czo_text_info = f"{self._options['device']}.{czo_info}"
            dataid_text_info = f"{dataid_text_info} on CZO: {czo_info} ({czo_string})"

        resultsBitmap = None

        if data_id_type == DataTypeFunction.DATA_TYPE_STANDARD:
            success, resultsBitmap, value = self._read_DataIdsStandard([data_id_int], czo_int)

            if value is not None:
                value = value[0]
                if self._ares5_env.checkIfDataIDisSigned(data_id_string) and value & 0x80000000 == 0x80000000:
                    value = 0xFFFFFFFF - value
                    value = ~value
            else:
                value = None

        elif data_id_type == DataTypeFunction.DATA_TYPE_ARRAY:
            success, resultsBitmap, value = self._read_DataIdArray(data_id_int, czo_int)
        elif data_id_type == data_id_type == DataTypeFunction.DATA_TYPE_STREAM:
            success, size = self._read_DataIdStreamSize(data_id_int, czo_int)

            if success != EErrors.E_OK:  # Operation to read Stream Size failed
                self._report.print_on_console(
                        f"An error occurred during ReadStreamSizeDataId operation: Size of DataID: {dataid_text_info} has not been read")
                self._report.add_action_row(
                        czo_text_info, self._actions["READ"], dataid_text_info, None, None,
                        self._results["ERROR"], "Error occurred during reading DataID Stream Size operation")
            else:
                success, resultsBitmap, value = self._read_DataIdStream(data_id_int, czo_int, size, Offset)

        if success != EErrors.E_OK:  # Read operation failed
            self._report.print_on_console(
                    f"An error occurred during read DataID operation: DataID: {dataid_text_info} has not been read")
            self._report.add_action_row(
                    czo_text_info, self._actions["READ"], dataid_text_info, None, None,
                    self._results["ERROR"], "Error occurred during reading DataID operation.")
        else:
            if resultsBitmap != 1:  # Read operation ok but no data read, the DataID could be non-existent
                if not SkipComment:
                    self._report.print_on_console(
                            f"DataID: {dataid_text_info} not read. Operation completed successfully, "
                            f"but no response received for DataID.")
                    self._report.add_action_row(
                            czo_text_info, self._actions["READ"], dataid_text_info, None, None,
                            self._results["WARNING"], "A response was not received for the specified DataID.")
            else:
                if not SkipComment:
                    self._report.print_on_console(f"Read DataID: {dataid_text_info}, val = {value}")
                    self._report.add_action_row(
                            czo_text_info, self._actions["READ"], dataid_text_info, f"{value}", None,
                            self._results["SUCCESS"], None)
                result = value

        return result


    def read_DataIdList(self, DataID: list, CZO: int, Field: list[int] = None, SkipComment: bool = False) -> \
            list[int]:
        """
            Software Specification: N/A

            :param self: Instance of the class.
            :param DataID: List of DataID names or codes to read. [list]
            :param CZO: CZO address associated with the DataID list. [int]
            :param Field: List of fields corresponding to each DataID, used when searching by name. [list]
            :param SkipComment: If True, comments will be excluded from the report. [bool]

            :returns: list[int] – Values read from the DataIDs. Returns None if the operation fails.

            :raises Ares5Error: If the Ares5Env object is not initialized or if any DataID has a DataType of Array or Stream.

            :description: Reads multiple DataIDs of type Standard using either their names and fields or their codes.

            :remarks: None
        """

        if self._ares5_env is None:
            raise Ares5Error("Error: Cannot run 'read_DataIdList' without loading an Ares5 Env.XML.\n"
                             "To fix this, add the 'Ares5EnvSourcePath' entry "
                             "with the correct path to your Config.txt file.")
        if Field is not None and len(DataID) != len(Field):
            raise Ares5Error(f"Error: Impossible to read {len(DataID)} DataID by names with only {len(Field)} Fields.")

        if isinstance(CZO, Enum):
            CZO = CZO.value

        result = None

        data_id_text_list = []
        data_id_list = []

        czo_int, czo_string, czo_info = self._searchCZOInfo(CZO)

        if czo_info is None:
            czo_text_info = self._options['device']
        else:
            czo_text_info = f"{self._options['device']}.{czo_info}"

        for i in range(len(DataID)):
            s_data = DataID[i]

            if isinstance(s_data, Enum):
                s_data = s_data.value

            if Field is None:
                s_field = None
            else:
                s_field = Field[i]

            data_id_int, data_id_string, data_id_name = self._searchDataIDInfo(s_data, s_field)
            data_id_type, _, field_identifier, _ = self._ares5_env.GetDataIdDataTypeFieldInfo(data_id_string)

            if data_id_type != DataTypeFunction.DATA_TYPE_STANDARD:
                raise Ares5Error(f"Error: You cannot read multiple DataIDs of type '{data_id_type.name}'.\n"
                                 f"This is only allowed for the following types: {DATA_TYPE_STANDARD}.")

            if data_id_name is None:
                dataid_text_info = f"{data_id_string} (DGTO {DATAID_to_DGTO(data_id_string)}) Field: {field_identifier}"
            else:
                dataid_text_info = f"\"{data_id_name}\".{field_identifier} ({data_id_string}) " \
                                   f"(DGTO {DATAID_to_DGTO(data_id_string)})"

            if czo_info is None:
                dataid_text_info = f"{dataid_text_info} on CZO: {czo_string}"
            else:
                dataid_text_info = f"{dataid_text_info} on CZO: {czo_info} ({czo_string})"

            data_id_text_list.append(dataid_text_info)
            data_id_list.append(data_id_int)

        success, resultsBitmap, value = self._read_DataIdsStandard(data_id_list, czo_int)

        if success != EErrors.E_OK:  # Read operation failed
            self._report.print_on_console(
                    f"An error occurred during multiple DataID read operation: DataIDs: {data_id_text_list} has not been read")
            self._report.add_action_row(
                    czo_text_info, self._actions["READ"], data_id_text_list, None, None,
                    self._results["ERROR"], "Error occurred during multiple DataID reading operation.")
        else:
            result_values = []
            for i in range(len(DataID)):
                single_res = (resultsBitmap & pow(2, i) == pow(2, i))
                if single_res:  # Read operation ok but no data read, the DataID could be non-existent
                    if not SkipComment:
                        self._report.print_on_console(f"Read DataID: {data_id_text_list[i]}, val = {value[i]}")
                        self._report.add_action_row(
                                czo_text_info, self._actions["READ"], data_id_text_list[i], value[i], None,
                                self._results["SUCCESS"], None)
                    result_values.append(value[i])
                else:
                    if not SkipComment:
                        self._report.print_on_console(
                                f"DataID: {data_id_text_list[i]} not read. Operation completed successfully, "
                                f"but no response received for DataID.")
                        self._report.add_action_row(
                                czo_text_info, self._actions["READ"], data_id_text_list[i], None, None,
                                self._results["WARNING"], "A response was not received for the specified DataID.")
                    result_values.append(None)

            result = result_values

        return result


    def write_DataId(self, DataID, CZO: int, value, Offset: int = None, Field: int = None, check_time: int = None,
                     read_after_write: bool = True) -> bool:
        """
            Software Specification: N/A

            :param self: Instance of the class.
            :param DataID: Name or code of the DataID to write. [str]
            :param CZO: CZO address associated with the DataID. [int]
            :param value: Value(s) to be written, depending on the DataType:
                - Standard: int
                - Array: list[int]
                - Stream: list[int]
            :param Offset: Offset used only for Stream DataType. [int]
            :param Field: Field of the DataID, applicable when searching by name. [int]
            :param check_time: Time in seconds to wait before performing the read-back check, if enabled. [int]
            :param read_after_write: If True, performs a read operation after writing to verify the value was set correctly. [bool]

            :returns: True if the operation succeeded, otherwise False.

            :raises Ares5Error: If the Ares5Env object is not initialized or if DataID is provided as a list instead of a single element.

            :description: Writes a value to a DataID using either its name and field or its code and address.

            :remarks: None
        """

        if self._ares5_env is None:
            raise Ares5Error("Error: Cannot run 'write_DataId' without loading an Ares5 Env.XML.\n"
                             "To fix this, add the 'Ares5EnvSourcePath' entry "
                             "with the correct path to your Config.txt file.")
        if type(DataID) == list:
            raise Ares5Error("Error: The 'write_DataId' method only supports a single DataID. "
                             "To process multiple DataIDs, please use the 'write_DataIdList' method instead.")

        if isinstance(DataID, Enum):
            DataID = DataID.value

        if isinstance(CZO, Enum):
            CZO = CZO.value

        result = False

        data_id_int, data_id_string, data_id_name = self._searchDataIDInfo(DataID, Field)
        czo_int, czo_string, czo_info = self._searchCZOInfo(CZO)
        data_id_type, total_len, field_identifier, access_type = self._ares5_env.GetDataIdDataTypeFieldInfo(
                data_id_string)

        dgto_str = DATAID_to_DGTO(data_id_string)
        dgto_int = convert_dgto_to_hex(dgto_str)

        probe_index = self._search_probe(dgto_int)

        if data_id_type == DataTypeFunction.DATA_TYPE_STANDARD:
            if data_id_name is None:
                dataid_text_info = f"{data_id_string}\" (DGTO {DATAID_to_DGTO(data_id_string)}) Field: {field_identifier}"
            else:
                dataid_text_info = f"\"{data_id_name}\".{field_identifier} ({data_id_string}) " \
                                   f"(DGTO {DATAID_to_DGTO(data_id_string)})"
        else:
            if data_id_name is None:
                dataid_text_info = f"{data_id_string} Field: {field_identifier}"
            else:
                dataid_text_info = f"\"{data_id_name}\".{field_identifier} ({data_id_string})"

        if czo_info is None:
            czo_text_info = self._options['device']
            dataid_text_info = f"{dataid_text_info} on CZO: {czo_string}"
        else:
            czo_text_info = f"{self._options['device']}.{czo_info}"
            dataid_text_info = f"{dataid_text_info} on CZO: {czo_info} ({czo_string})"

        check_time = self._default_write_check_time_dgto if check_time is None else check_time

        resultsBitmap = None

        # TODO: Check AccessType at runtime of the DataID to see if is possible to be written,
        #  for now is not implemented in ATG protocol, same for range min, max
        if access_type == AccessType.READ_ONLY and probe_index == 0:
            self._report.print_on_console(
                    f"WARNING: Attempting to write DataID: {dataid_text_info}, but the Access Type is READ_ONLY.")
            self._report.add_action_row(
                    czo_text_info, self._actions["WRITE"], dataid_text_info, None, None,
                    self._results["WARNING"], f"Attempting to write DataID with Access Type READ_ONLY.")

        if probe_index > 0:
            if self._write_probe(dataid_text_info, probe_index, value, check_time, True, None, None):
                success = EErrors.E_OK
                resultsBitmap = 1
            else:
                success = EErrors.E_INVALID_REQ  # TODO: to define a specific error
                resultsBitmap = 0
        elif data_id_type == DataTypeFunction.DATA_TYPE_STANDARD:
            if type(value) != int:
                raise Ares5Error(
                        f"Error: Impossible to write a non integer value on Standard DataID: {dataid_text_info}.")

            success, resultsBitmap = self._write_DataIdsStandard([data_id_int], czo_int, [value])
        elif data_id_type == DataTypeFunction.DATA_TYPE_ARRAY:
            if type(value) != list:
                raise Ares5Error(
                        f"Error: Impossible to write a non list[int] values on Array DataID: {dataid_text_info}.")
            elif len(value) != total_len:
                raise Ares5Error(
                        f"Error: The Array DataID: {dataid_text_info} needs {total_len} values,"
                        f" but only {len(value)} passed.")
            else:
                success, resultsBitmap = self._write_DataIdArray(data_id_int, czo_int, value)
        elif data_id_type == data_id_type == DataTypeFunction.DATA_TYPE_STREAM:
            if type(value) != list:
                raise Ares5Error(
                        f"Error: Impossible to write a non list[int] values on Stream DataID: {dataid_text_info}.")

            success, resultsBitmap = self._write_DataIdStream(data_id_int, czo_int, value, Offset)

        if success != EErrors.E_OK:  # Write operation failed
            self._report.print_on_console(
                    f"An error occurred during write DataID operation: DataID: {dataid_text_info} has not been written")
            self._report.add_action_row(
                    czo_text_info, self._actions["WRITE"], dataid_text_info, None, None,
                    self._results["ERROR"], "Error occurred during writring DataID operation.")
        else:
            if resultsBitmap != 1:  # Read operation ok but no data written, the DataID could be non-existent
                self._report.print_on_console(
                        f"DataID: {dataid_text_info} not written. Operation completed successfully, "
                        f"but no response received for DataID.")
                self._report.add_action_row(
                        czo_text_info, self._actions["WRITE"], dataid_text_info, None, f"{value}",
                        self._results["WARNING"], "A response was not received for the specified DataID.")
            else:  # Read Check
                if read_after_write:
                    time.sleep(check_time)
                    val_read = self.read_DataId(DataID, CZO, Offset, Field, True)

                    if val_read is not None and val_read == value:
                        self._report.print_on_console(f"Written DataID: {dataid_text_info} with val = {value}")
                        self._report.add_action_row(
                                czo_text_info, self._actions["WRITE"], dataid_text_info, None, f"{value}",
                                self._results["SUCCESS"], None)
                        result = True
                    else:
                        self._report.print_on_console(
                                f"DataID: {dataid_text_info} was not updated with {value}. "
                                f"Operation completed successfully, but the requested value is not set (still {val_read}).")
                        self._report.add_action_row(
                                czo_text_info, self._actions["WRITE"], dataid_text_info, f"{val_read}", f"{value}",
                                self._results["WARNING"], "Value not set.")
                else:
                    self._report.print_on_console(f"Written DataID: {dataid_text_info} with val = {value}")
                    self._report.add_action_row(
                            czo_text_info, self._actions["WRITE"], dataid_text_info, None, f"{value}",
                            self._results["SUCCESS"], None)
                    result = True

        return result


    def write_DataIdList(self, DataID: list, CZO: int, value: list[int], Field: list[int] = None,
                         check_time: int = None, read_after_write: bool = True) -> bool:
        """
            Software Specification: N/A

            :param self: Instance of the class.
            :param DataID: List of DataID names or codes to write. [list]
            :param CZO: CZO address associated with the DataID list. [int]
            :param value: List of values to write. [list[int]]
            :param Field: List of fields corresponding to each DataID, used when searching by name. [list]
            :param check_time: Time in seconds to wait before performing the read-back check, if enabled. [int]
            :param read_after_write: If True, performs a read operation after writing to verify that the values were set correctly. [bool]

            :returns: True if the operation succeeded, otherwise False. [bool]

            :raises Ares5Error: If the Ares5Env object is not initialized or if any DataID has a DataType of Array or Stream.

            :description: Writes multiple DataIDs of type Standard using either their names and fields or their codes.

            :remarks: None
        """

        if self._ares5_env is None:
            raise Ares5Error("Error: Cannot run 'write_DataIdList' without loading an Ares5 Env.XML.\n"
                             "To fix this, add the 'Ares5EnvSourcePath' entry "
                             "with the correct path to your Config.txt file.")
        if Field is not None:
            if len(DataID) != len(Field):
                raise Ares5Error(
                        f"Error: Impossible to write {len(DataID)} DataID by names with only {len(Field)} Fields.")
            elif len(DataID) != len(value):
                raise Ares5Error(
                        f"Error: Impossible to write {len(DataID)} DataID by names with only {len(value)} values.")

        if isinstance(CZO, Enum):
            CZO = CZO.value

        result = False

        data_id_text_list = []
        data_id_list = []

        czo_int, czo_string, czo_info = self._searchCZOInfo(CZO)

        if czo_info is None:
            czo_text_info = self._options['device']
        else:
            czo_text_info = f"{self._options['device']}.{czo_info}"

        for i in range(len(DataID)):
            s_data = DataID[i]

            if isinstance(s_data, Enum):
                s_data = s_data.value

            if Field is None:
                s_field = None
            else:
                s_field = Field[i]

            data_id_int, data_id_string, data_id_name = self._searchDataIDInfo(s_data, s_field)
            data_id_type, total_len, field_identifier, access_type = self._ares5_env.GetDataIdDataTypeFieldInfo(
                    data_id_string)

            if data_id_type != DataTypeFunction.DATA_TYPE_STANDARD:
                raise Ares5Error(f"Error: You cannot write multiple DataIDs of type '{data_id_type.name}'.\n"
                                 f"This is only allowed for the following types: {DATA_TYPE_STANDARD}.")

            if data_id_name is None:
                dataid_text_info = f"{data_id_string} (DGTO {DATAID_to_DGTO(data_id_string)}) Field: {field_identifier}"
            else:
                dataid_text_info = f"\"{data_id_name}\".{field_identifier} ({data_id_string}) " \
                                   f"(DGTO {DATAID_to_DGTO(data_id_string)})"

            if czo_info is None:
                dataid_text_info = f"{dataid_text_info} on CZO: {czo_string}"
            else:
                dataid_text_info = f"{dataid_text_info} on CZO: {czo_info} ({czo_string})"

            # TODO: Check AccessType at runtime of the DataID to see if is possible to be written,
            #  for now is not implemented in ATG protocol
            if access_type == AccessType.READ_ONLY:
                self._report.print_on_console(
                        f"WARNING: Attempting to write DataID: {dataid_text_info}, but the Access Type is READ_ONLY.")
                self._report.add_action_row(
                        czo_text_info, self._actions["WRITE"], dataid_text_info, None, None,
                        self._results["WARNING"], f"Attempting to write DataID with Access Type READ_ONLY.")

            data_id_text_list.append(dataid_text_info)
            data_id_list.append(data_id_int)

        success, resultsBitmap = self._write_DataIdsStandard(data_id_list, czo_int, value)

        if success != EErrors.E_OK:  # Write operation failed
            self._report.print_on_console(
                    f"An error occurred during multiple write DataID operation: DataIsD: {data_id_text_list} has not been written")
            self._report.add_action_row(
                    czo_text_info, self._actions["WRITE"], data_id_text_list, None, None,
                    self._results["ERROR"], "Error occurred during multiple write DataIDs operation.")
        else:  # Read Check
            if read_after_write:
                check_time = self._default_write_check_time_dgto if check_time is None else check_time

                time.sleep(check_time)
                vals_read = self.read_DataIdList(DataID, CZO, Field, True)
                errors = 0
                if vals_read is not None:
                    for i in range(len(vals_read)):
                        if vals_read[i] == value[i]:
                            self._report.print_on_console(
                                    f"Written DataID: {data_id_text_list[i]} with val = {value[i]}.")
                            self._report.add_action_row(
                                    czo_text_info, self._actions["WRITE"], data_id_text_list[i], None, value[i],
                                    self._results["SUCCESS"], None)
                        else:
                            self._report.print_on_console(
                                    f"WARNING: DataID {data_id_text_list[i]} has been NOT written with value {value[i]}.")
                            self._report.add_action_row(
                                    czo_text_info, self._actions["WRITE"], data_id_text_list, vals_read[i], value[i],
                                    self._results["WARNING"], "NOT written with value.")
                            errors = errors + 1

                    result = errors == 0
                else:
                    self._report.print_on_console(
                            f"WARNING: Write to DataIDs {data_id_text_list} succeeded, "
                            f"but read-back failed. Unable to confirm if values were correctly set.")
                    self._report.add_action_row(
                            czo_text_info, self._actions["WRITE"], data_id_text_list, None, value[i],
                            self._results["WARNING"], "read-back failed.")
            else:
                errors = 0
                for i in range(len(DataID)):
                    single_res = (resultsBitmap & pow(2, i) == pow(2, i))
                    dataid_text_info = data_id_text_list[i]
                    if single_res:  # Read operation ok but no data read, the DataID could be non-existent
                        self._report.print_on_console(f"Written DataID: {dataid_text_info} with val = {value[i]}.")
                        self._report.add_action_row(
                                czo_text_info, self._actions["WRITE"], dataid_text_info, None, value[i],
                                self._results["SUCCESS"], None)
                        result = True
                    else:
                        self._report.print_on_console(
                                f"DataID: {dataid_text_info} not written. Operation completed successfully, "
                                f"but no response received for DataID.")
                        self._report.add_action_row(
                                czo_text_info, self._actions["WRITE"], dataid_text_info, None, value[i],
                                self._results["WARNING"], "A response was not received for the specified DataID.")
                        errors = errors + 1

                    result = errors == 0
        return result


    def _read_DataIdsStandard(self, data_id: list[int], czo: int) -> tuple[bool, int, list[int]]:
        """
        Software Specification: N/A

        :param self: Instance of the class.
        :param data_id: List of integer addresses of the DataIDs to read. [list[int]]
        :param czo: CZO address to read from. [int]

        :returns: Tuple containing:
            - success: Operation result code.
            - resultsBitmap: Bitmap indicating read status.
            - values: List of values read from the DataIDs. [list[int]]

        :description: Reads multiple Standard DataType DataIDs from the specified CZO.

        :remarks: None
        """
        if self._ares5_env.CheckIfCZOisBoard(czo):
            target_czo = self._ares5_env.BoardCZOToDeviceCZO(czo)

            try:
                success, resultsBitmap, values = self._api.ReadDataIdListFromBrdHostedByCzo(target_czo, data_id)
            except:
                success = EErrors.E_INVALID_REQ
                resultsBitmap = None
                values = None

        else:
            try:
                success, resultsBitmap, values = self._api.ReadDataIdListFromCzo(czo, data_id)
            except:
                success = EErrors.E_INVALID_REQ
                resultsBitmap = None
                values = None

        return success, resultsBitmap, values


    def _read_DataIdArray(self, data_id: int, czo: int) -> tuple[bool, int, list[int]]:
        """
         Software Specification: N/A

         :param self: Instance of the class.
         :param data_id: Integer address of the Array DataID to read. [int]
         :param czo: CZO address to read from. [int]

         :returns: Tuple containing:
             - success: Operation result code.
             - resultsBitmap: Always 1 for compatibility.
             - values: List of values read from the Array DataID. [list[int]]

         :description: Reads an Array DataType DataID from the specified CZO.

         :remarks: None
         """

        if self._ares5_env.CheckIfCZOisBoard(czo):
            target_czo = self._ares5_env.BoardCZOToDeviceCZO(czo)
            try:
                success, values = self._api.ReadArrayDataIdFromBrdHostedByCzo(target_czo, data_id)
            except:
                success = EErrors.E_INVALID_REQ
                values = None
        else:
            try:
                success, values = self._api.ReadArrayDataIdFromCzo(czo, data_id)
            except:
                success = EErrors.E_INVALID_REQ
                values = None

        return success, 1, values


    def _read_DataIdStream(self, data_id: int, czo: int, length: int, offset: int = 0) -> tuple[bool, int, list[int]]:
        """
        Software Specification: N/A

        :param self: Instance of the class.
        :param data_id: Integer address of the Stream DataID to read. [int]
        :param czo: CZO address to read from. [int]
        :param length: Number of elements to read from the stream. [int]
        :param offset: Offset within the stream to start reading from. [int]

        :returns: Tuple containing:
            - success: Operation result code.
            - resultsBitmap: Always 1 for compatibility.
            - values: List of values read from the Stream DataID. [list[int]]

        :description: Reads a DataType Stream DataID from the specified CZO with optional offset.

        :remarks: None
        """

        if self._ares5_env.CheckIfCZOisBoard(czo):
            target_czo = self._ares5_env.BoardCZOToDeviceCZO(czo)
            try:
                success, values = self._api.ReadStreamDataIdFromBrdHostedByCzo(target_czo, data_id, length, offset)
            except:
                success = EErrors.E_INVALID_REQ
                values = None
        else:
            try:
                success, values = self._api.ReadStreamDataIdFromCzo(czo, data_id, length, offset)
            except:
                success = EErrors.E_INVALID_REQ
                values = None

        return success, 1, values


    def _read_DataIdStreamSize(self, data_id: int, czo: int) -> tuple[bool, int]:
        """
        Software Specification: N/A

        :param self: Instance of the class.
        :param data_id: Integer address of the Stream DataID. [int]
        :param czo: CZO address to query. [int]

        :returns: Tuple containing:
            - success: Operation result code.
            - length: Size of the Stream DataID. [int]

        :description: Retrieves the size of a Stream DataID from the specified CZO.

        :remarks: None
        """
        if self._ares5_env.CheckIfCZOisBoard(czo):
            target_czo = self._ares5_env.BoardCZOToDeviceCZO(czo)
            try:
                success, length = self._api.ReadStreamSizeDataIdFromBrdHostedByCzo(target_czo, data_id)
            except:
                success = EErrors.E_INVALID_REQ
                length = None
        else:
            try:
                success, length = self._api.ReadStreamSizeDataIdFromCzo(czo, data_id)
            except:
                success = EErrors.E_INVALID_REQ
                length = None

        return success, length


    def _write_DataIdsStandard(self, data_id: list[int], czo: int, values: list[int]) -> tuple[bool, int]:
        """
            Software Specification: N/A

            :param self: Instance of the class.
            :param data_id: List of integer addresses of the Standard DataIDs to write. [list[int]]
            :param czo: CZO address to write to. [int]
            :param values: List of integer values to write. [list[int]]

            :returns: Tuple containing:
                - success: Operation result code.
                - resultsBitmap: Bitmap indicating write status.

            :description: Writes values to multiple Standard DataIDs on the specified CZO.

            :remarks: None
            """

        if self._ares5_env.CheckIfCZOisBoard(czo):
            target_czo = self._ares5_env.BoardCZOToDeviceCZO(czo)
            try:
                success, resultsBitmap = self._api.WriteDataIdListToBrdHostedByCzo(target_czo, data_id, values)
            except:
                success = EErrors.E_INVALID_REQ
                resultsBitmap = None
        else:
            try:
                success, resultsBitmap = self._api.WriteDataIdListToCzo(czo, data_id, values)
            except:
                success = EErrors.E_INVALID_REQ
                resultsBitmap = None

        return success, resultsBitmap


    def _write_DataIdArray(self, data_id: int, czo: int, values: list[int]) -> tuple[bool, int]:
        """
        Software Specification: N/A

        :param self: Instance of the class.
        :param data_id: Integer address of the Array DataID to write. [int]
        :param czo: CZO address to write to. [int]
        :param values: List of integer values to write. [list[int]]

        :returns: Tuple containing:
            - success: Operation result code.
            - resultsBitmap: Always 1 for compatibility.

        :description: Writes values to an Array DataID on the specified CZO.

        :remarks: None
        """

        if self._ares5_env.CheckIfCZOisBoard(czo):
            target_czo = self._ares5_env.BoardCZOToDeviceCZO(czo)
            try:
                success, _ = self._api.WriteArrayDataIdToBrdHostedByCzo(target_czo, data_id, bytearray(values))
            except:
                success = EErrors.E_INVALID_REQ
        else:
            try:
                success, _ = self._api.WriteArrayDataIdToCzo(czo, data_id, bytearray(values))
            except:
                success = EErrors.E_INVALID_REQ

        return success, 1


    def _write_DataIdStream(self, data_id: int, czo: int, values: list[int], offset: int = 0) -> tuple[bool, int]:
        """
        Software Specification: N/A

        :param self: Instance of the class.
        :param data_id: Integer address of the Stream DataID to write. [int]
        :param czo: CZO address to write to. [int]
        :param values: List of integer values to write. [list[int]]
        :param offset: Offset within the stream to start writing. [int]

        :returns: Tuple containing:
            - success: Operation result code.
            - resultsBitmap: Always 1 for compatibility.

        :description: Writes values to a Stream DataID on the specified CZO with optional offset.

        :remarks: None
        """

        if self._ares5_env.CheckIfCZOisBoard(czo):
            target_czo = self._ares5_env.BoardCZOToDeviceCZO(czo)
            try:
                success, _ = self._api.WriteStreamDataIdToBrdHostedByCzo(target_czo, data_id, offset,
                                                                         bytearray(values))
            except:
                success = EErrors.E_INVALID_REQ
        else:
            try:
                success, _ = self._api.WriteStreamDataIdToCzo(czo, data_id, offset, bytearray(values))
            except:
                success = EErrors.E_INVALID_REQ

        return success, 1


    def read_DataIdFromBoard(self, DataID, Handle: int, Offset: int = None, Field: int = None,
                             SkipComment: bool = False):
        """
            Software Specification: N/A

            :param self: Instance of the class.
            :param DataID: Name or Code of the DataID to read. [str]
            :param Handle: Board Handle address. [int]
            :param Offset: Offset used for Stream DataType only. [int]
            :param Field: Field of the DataID to read, applicable when searching by name. [int]
            :param SkipComment: If True, the comment will not be written to the report. [bool]

            :returns: Value(s) read from the DataID, depending on its DataType:
                - Standard: int – the value read, or None if the operation fails.
                - Array: list[int] – values read, or None if the operation fails.
                - Stream: list[int] – values read, or None if the operation fails.

            :raises Ares5Error: If the Ares5Env object is not initialized or
            if DataID is provided as a list instead of a single element.

            :description: Reads a DataID using either its name and field or its code and address.

            :remarks: None
        """
        if self._ares5_env is None:
            raise Ares5Error("Error: Cannot run 'read_DataIdFromBoard' without loading an Ares5 Env.XML.\n"
                             "To fix this, add the 'Ares5EnvSourcePath' entry "
                             "with the correct path to your Config.txt file.")
        if type(DataID) == list:
            raise Ares5Error("Error: The 'read_DataIdFromBoard' method only supports a single DataID. "
                             "To process multiple DataIDs, please use the 'read_DataIdListFromBoard' method instead.")

        # TODO: To add conversion of float

        if isinstance(DataID, Enum):
            DataID = DataID.value

        result = None
        data_id_int, data_id_string, data_id_name = self._searchDataIDInfo(DataID, Field)
        data_id_type, _, field_identifier, _ = self._ares5_env.GetDataIdDataTypeFieldInfo(data_id_string)

        if data_id_type == DataTypeFunction.DATA_TYPE_STANDARD:
            if data_id_name is None:
                dataid_text_info = f"{data_id_string} (DGTO {DATAID_to_DGTO(data_id_string)}) Field: {field_identifier}"
            else:
                dataid_text_info = f"\"{data_id_name}\".{field_identifier} ({data_id_string}) " \
                                   f"(DGTO {DATAID_to_DGTO(data_id_string)})"
        else:
            if data_id_name is None:
                dataid_text_info = f"{data_id_string} Field: {field_identifier}"
            else:
                dataid_text_info = f"\"{data_id_name}\".{field_identifier} ({data_id_string})"

        czo_text_info = self._options['device']
        dataid_text_info = f"{dataid_text_info} on Handle: {Handle}"

        resultsBitmap = None

        if data_id_type == DataTypeFunction.DATA_TYPE_STANDARD:
            success, resultsBitmap, value = self._read_DataIdsStandardFromBoard([data_id_int], Handle)

            if value is not None:
                value = value[0]
                if self._ares5_env.checkIfDataIDisSigned(data_id_string) and value & 0x80000000 == 0x80000000:
                    value = 0xFFFFFFFF - value
                    value = ~value
            else:
                value = None

        elif data_id_type == DataTypeFunction.DATA_TYPE_ARRAY:
            success, resultsBitmap, value = self._read_DataIdArrayFromBoard(data_id_int, Handle)
        elif data_id_type == data_id_type == DataTypeFunction.DATA_TYPE_STREAM:
            success, size = self._read_DataIdStreamSizeFromBoard(data_id_int, Handle)

            if success != EErrors.E_OK:  # Operation to read Stream Size failed
                self._report.print_on_console(
                        f"An error occurred during ReadStreamSizeDataId operation: Size of DataID: {dataid_text_info} has not been read")
                self._report.add_action_row(
                        czo_text_info, self._actions["READ"], dataid_text_info, None, None,
                        self._results["ERROR"], "Error occurred during reading DataID Stream Size operation")
            else:
                success, resultsBitmap, value = self._read_DataIdStreamFromBoard(data_id_int, Handle, size, Offset)

        if success != EErrors.E_OK:  # Read operation failed
            self._report.print_on_console(
                    f"An error occurred during read DataID operation: DataID: {dataid_text_info} has not been read")
            self._report.add_action_row(
                    czo_text_info, self._actions["READ"], dataid_text_info, None, None,
                    self._results["ERROR"], "Error occurred during reading DataID operation.")
        else:
            if resultsBitmap != 1:  # Read operation ok but no data read, the DataID could be non-existent
                if not SkipComment:
                    self._report.print_on_console(
                            f"DataID: {dataid_text_info} not read. Operation completed successfully, "
                            f"but no response received for DataID.")
                    self._report.add_action_row(
                            czo_text_info, self._actions["READ"], dataid_text_info, None, None,
                            self._results["WARNING"], "A response was not received for the specified DataID.")
            else:
                if not SkipComment:
                    self._report.print_on_console(f"Read DataID: {dataid_text_info}, val = {value}")
                    self._report.add_action_row(
                            czo_text_info, self._actions["READ"], dataid_text_info, f"{value}", None,
                            self._results["SUCCESS"], None)
                result = value

        return result


    def write_DataIdToBoard(self, DataID, Handle: int, value, Offset: int = None, Field: int = None, check_time: int = None,
                     read_after_write: bool = True) -> bool:
        """
            Software Specification: N/A

            :param self: Instance of the class.
            :param DataID: Name or code of the DataID to write. [str]
            :param Handle: handle address associated with the DataID. [int]
            :param value: Value(s) to be written, depending on the DataType:
                - Standard: int
                - Array: list[int]
                - Stream: list[int]
            :param Offset: Offset used only for Stream DataType. [int]
            :param Field: Field of the DataID, applicable when searching by name. [int]
            :param check_time: Time in seconds to wait before performing the read-back check, if enabled. [int]
            :param read_after_write: If True, performs a read operation after writing to verify the value was set correctly. [bool]

            :returns: True if the operation succeeded, otherwise False.

            :raises Ares5Error: If the Ares5Env object is not initialized or if DataID is provided as a list instead of a single element.

            :description: Writes a value to a DataID using either its name and field or its code and address.

            :remarks: None
        """

        if self._ares5_env is None:
            raise Ares5Error("Error: Cannot run 'write_DataId' without loading an Ares5 Env.XML.\n"
                             "To fix this, add the 'Ares5EnvSourcePath' entry "
                             "with the correct path to your Config.txt file.")
        if type(DataID) == list:
            raise Ares5Error("Error: The 'write_DataId' method only supports a single DataID. "
                             "To process multiple DataIDs, please use the 'write_DataIdList' method instead.")

        if isinstance(DataID, Enum):
            DataID = DataID.value

        if isinstance(Handle, Enum):
            Handle = Handle.value

        result = False

        data_id_int, data_id_string, data_id_name = self._searchDataIDInfo(DataID, Field)
        data_id_type, total_len, field_identifier, access_type = self._ares5_env.GetDataIdDataTypeFieldInfo(
                data_id_string)

        if data_id_type == DataTypeFunction.DATA_TYPE_STANDARD:
            if data_id_name is None:
                dataid_text_info = f"{data_id_string}\" (DGTO {DATAID_to_DGTO(data_id_string)}) Field: {field_identifier}"
            else:
                dataid_text_info = f"\"{data_id_name}\".{field_identifier} ({data_id_string}) " \
                                   f"(DGTO {DATAID_to_DGTO(data_id_string)})"
        else:
            if data_id_name is None:
                dataid_text_info = f"{data_id_string} Field: {field_identifier}"
            else:
                dataid_text_info = f"\"{data_id_name}\".{field_identifier} ({data_id_string})"

        czo_text_info = self._options['device']
        dataid_text_info = f"{dataid_text_info} on Handle: {Handle}"

        check_time = self._default_write_check_time_dgto if check_time is None else check_time

        resultsBitmap = None

        # TODO: Check AccessType at runtime of the DataID to see if is possible to be written,
        #  for now is not implemented in ATG protocol, same for range min, max
        if access_type == AccessType.READ_ONLY:
            self._report.print_on_console(
                    f"WARNING: Attempting to write DataID: {dataid_text_info}, but the Access Type is READ_ONLY.")
            self._report.add_action_row(
                    czo_text_info, self._actions["WRITE"], dataid_text_info, None, None,
                    self._results["WARNING"], f"Attempting to write DataID with Access Type READ_ONLY.")

        if data_id_type == DataTypeFunction.DATA_TYPE_STANDARD:
            if type(value) != int:
                raise Ares5Error(
                        f"Error: Impossible to write a non integer value on Standard DataID: {dataid_text_info}.")

            success, resultsBitmap = self._write_DataIdsStandardToBoard([data_id_int], Handle, [value])
        elif data_id_type == DataTypeFunction.DATA_TYPE_ARRAY:
            if type(value) != list:
                raise Ares5Error(
                        f"Error: Impossible to write a non list[int] values on Array DataID: {dataid_text_info}.")
            elif len(value) != total_len:
                raise Ares5Error(
                        f"Error: The Array DataID: {dataid_text_info} needs {total_len} values,"
                        f" but only {len(value)} passed.")
            else:
                success, resultsBitmap = self._write_DataIdArrayToBoard(data_id_int, Handle, value)
        elif data_id_type == data_id_type == DataTypeFunction.DATA_TYPE_STREAM:
            if type(value) != list:
                raise Ares5Error(
                        f"Error: Impossible to write a non list[int] values on Stream DataID: {dataid_text_info}.")

            success, resultsBitmap = self._write_DataIdStreamToBoard(data_id_int, Handle, value, Offset)

        if success != EErrors.E_OK:  # Write operation failed
            self._report.print_on_console(
                    f"An error occurred during write DataID operation: DataID: {dataid_text_info} has not been written")
            self._report.add_action_row(
                    czo_text_info, self._actions["WRITE"], dataid_text_info, None, None,
                    self._results["ERROR"], "Error occurred during writring DataID operation.")
        else:
            if resultsBitmap != 1:  # Read operation ok but no data written, the DataID could be non-existent
                self._report.print_on_console(
                        f"DataID: {dataid_text_info} not written. Operation completed successfully, "
                        f"but no response received for DataID.")
                self._report.add_action_row(
                        czo_text_info, self._actions["WRITE"], dataid_text_info, None, f"{value}",
                        self._results["WARNING"], "A response was not received for the specified DataID.")
            else:  # Read Check
                if read_after_write:
                    time.sleep(check_time)
                    val_read = self.read_DataIdFromBoard(DataID, Handle, Offset, Field, True)

                    if val_read is not None and val_read == value:
                        self._report.print_on_console(f"Written DataID: {dataid_text_info} with val = {value}")
                        self._report.add_action_row(
                                czo_text_info, self._actions["WRITE"], dataid_text_info, None, f"{value}",
                                self._results["SUCCESS"], None)
                        result = True
                    else:
                        self._report.print_on_console(
                                f"DataID: {dataid_text_info} was not updated with {value}. "
                                f"Operation completed successfully, but the requested value is not set (still {val_read}).")
                        self._report.add_action_row(
                                czo_text_info, self._actions["WRITE"], dataid_text_info, f"{val_read}", f"{value}",
                                self._results["WARNING"], "Value not set.")
                else:
                    self._report.print_on_console(f"Written DataID: {dataid_text_info} with val = {value}")
                    self._report.add_action_row(
                            czo_text_info, self._actions["WRITE"], dataid_text_info, None, f"{value}",
                            self._results["SUCCESS"], None)
                    result = True

        return result


    def _read_DataIdsStandardFromBoard(self, data_id: list[int], handle: int) -> tuple[bool, int, list[int]]:
        """
        Software Specification: N/A

        :param self: Instance of the class.
        :param data_id: List of integer addresses of the DataIDs to read. [list[int]]
        :param handle: Board handle address to read from. [int]

        :returns: Tuple containing:
            - success: Operation result code.
            - resultsBitmap: Bitmap indicating read status.
            - values: List of values read from the DataIDs. [list[int]]

        :description: Reads multiple Standard DataType DataIDs from the specified Handle.

        :remarks: None
        """

        try:
            success, resultsBitmap, values = self._api.ReadDataIdListFromBrd(handle, data_id)
        except:
            success = EErrors.E_INVALID_REQ
            resultsBitmap = None
            values = None

        return success, resultsBitmap, values


    def _read_DataIdArrayFromBoard(self, data_id: int, handle: int) -> tuple[bool, int, list[int]]:
        """
         Software Specification: N/A

         :param self: Instance of the class.
         :param data_id: Integer address of the Array DataID to read. [int]
         :param handle: Board handle address to read from. [int]

         :returns: Tuple containing:
             - success: Operation result code.
             - resultsBitmap: Always 1 for compatibility.
             - values: List of values read from the Array DataID. [list[int]]

         :description: Reads an Array DataType DataID from the specified Handle.

         :remarks: None
         """

        try:
            success, values = self._api.ReadArrayDataIdFromBrd(handle, data_id)
        except:
            success = EErrors.E_INVALID_REQ
            values = None

        return success, 1, values


    def _read_DataIdStreamSizeFromBoard(self, data_id: int, handle: int) -> tuple[bool, int]:
        """
        Software Specification: N/A

        :param self: Instance of the class.
        :param data_id: Integer address of the Stream DataID. [int]
        :param handle: Board handle address to query. [int]

        :returns: Tuple containing:
            - success: Operation result code.
            - length: Size of the Stream DataID. [int]

        :description: Retrieves the size of a Stream DataID from the specified handle.

        :remarks: None
        """
        try:
            success, length = self._api.ReadStreamSizeDataIdFromBrd(handle, data_id)
        except:
            success = EErrors.E_INVALID_REQ
            length = None

        return success, length


    def _read_DataIdStreamFromBoard(self, data_id: int, handle: int, length: int, offset: int = 0) -> tuple[
        bool, int, list[int]]:
        """
        Software Specification: N/A

        :param self: Instance of the class.
        :param data_id: Integer address of the Stream DataID to read. [int]
        :param handle: Board handle address to read from. [int]
        :param length: Number of elements to read from the stream. [int]
        :param offset: Offset within the stream to start reading from. [int]

        :returns: Tuple containing:
            - success: Operation result code.
            - resultsBitmap: Always 1 for compatibility.
            - values: List of values read from the Stream DataID. [list[int]]

        :description: Reads a DataType Stream DataID from the specified Handle with optional offset.

        :remarks: None
        """

        try:
            success, values = self._api.ReadStreamDataIdFromBrd(handle, data_id, length, offset)
        except:
            success = EErrors.E_INVALID_REQ
            values = None

        return success, 1, values


    def _write_DataIdsStandardToBoard(self, data_id: list[int], handle: int, values: list[int]) -> tuple[bool, int]:
        """
        Software Specification: N/A

        :param self: Instance of the class.
        :param data_id: List of integer addresses of the Standard DataIDs to write. [list[int]]
        :param handle: Handle address to write to. [int]
        :param values: List of integer values to write. [list[int]]

        :returns: Tuple containing:
            - success: Operation result code.
            - resultsBitmap: Bitmap indicating write status.

        :description: Writes values to multiple Standard DataIDs on the specified Handle.

        :remarks: None
        """

        try:
            success, resultsBitmap = self._api.WriteDataIdListToBrd(handle, data_id, values)
        except:
            success = EErrors.E_INVALID_REQ
            resultsBitmap = None

        return success, resultsBitmap


    def _write_DataIdArrayToBoard(self, data_id: int, handle: int, values: list[int]) -> tuple[bool, int]:
        """
        Software Specification: N/A

        :param self: Instance of the class.
        :param data_id: Integer address of the Array DataID to write. [int]
        :param handle: Handle address to write to. [int]
        :param values: List of integer values to write. [list[int]]

        :returns: Tuple containing:
            - success: Operation result code.
            - resultsBitmap: Always 1 for compatibility.

        :description: Writes values to an Array DataID on the specified Handle.

        :remarks: None
        """

        try:
            success, _ = self._api.WriteArrayDataIdToBrd(handle, data_id, bytearray(values))
        except:
            success = EErrors.E_INVALID_REQ

        return success, 1


    def _write_DataIdStreamToBoard(self, data_id: int, handle: int, values: list[int], offset: int = 0) -> tuple[
        bool, int]:
        """
        Software Specification: N/A

        :param self: Instance of the class.
        :param handle: Integer address of the Stream DataID to write. [int]
        :param czo: CZO address to write to. [int]
        :param values: List of integer values to write. [list[int]]
        :param offset: Offset within the stream to start writing. [int]

        :returns: Tuple containing:
            - success: Operation result code.
            - resultsBitmap: Always 1 for compatibility.

        :description: Writes values to a Stream DataID on the specified Handle with optional offset.

        :remarks: None
        """

        try:
            success, _ = self._api.WriteStreamDataIdToBrd(handle, data_id, offset, bytearray(values))
        except:
            success = EErrors.E_INVALID_REQ

        return success, 1


    """ ---------------- End: ARES5 TestAutomation --------------- """
