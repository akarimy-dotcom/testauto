""" Class to manage TDM loads, temperature, status-transition and inverter communication (through PRG026) """

__version__ = '0.6.0'
__author__ = 'Nicolò Ruggeri, Raffaela Caddori'

# ------------------------------------------------
# Libraries Module
# ------------------------------------------------

import ctypes
import os
import time

import classes.CTRL_BOX_ID as CTRL_BOX_ID
import classes.LAB_MODE as LAB_MODE
# Import Modules
import libs.Inverter_APIs as Inverter_APIs
from classes.RAM_VAR import VAR as RAM_VAR
from libs.TestLib import TestLib
from libs.TestLib import __version__ as TestLib_version

''' ----------------------------------- '''
''' --- Framework Version = 1.09.00 --- '''
''' ----------------------------------- '''

Framework_Ver = "1.8.0"  # The target TestLib version to use
TDA_TestAutomation = "60ff8000df12"  # Target TDA, if is not present TDM_Manager object cannot works

"""
Changelog:
[0.7.0] - 2025-??-??:
- Added methods:
  "get_FAN_2_Speed": method to get the feedback of Fan 2 
  "get_FAN_2_Target": method to get the setpoint of Fan 2
  "check_suct_press_sensor_available": method to check if the suction pressure sensor is present for that CTRL_BOX_ID
  "check_disch_press_sensor_available": method to check if the discharge pressure sensor is present for that CTRL_BOX_ID
  
- Updated defines:
    "HEAT_COOLING_TIMER" changed from 60s to 80s because there's a new protection in the state 11 (Water Sensor Deviation),
    so the time of the cycle is increased
  
- Updated methods:
  "get_FAN_Target": added the new DGTO for Fan 1 feedback when Fan1 is active
  "get_FAN_Speed": added the new DGTO for Fan 1 setpoint when Fan1 is active
  "set_defrost_basic_conditions": updated the temperatures for entering in defrost status
  "set_lab_mode_active": added check if the lab_mode is already active
  "set_tdm_status": updated the part for defrost for Water Sensor Deviation
  "set_stanby": added the writing for ewt_filter (to avoid long wait), fix the EWT temperature for Water Sensor 
  Deviation and added the Suction Temperature to write
  "set_heating_state": added the new DGTO for Water Sensor Deviation (to avoid long wait) and fix EWT and LWT for Water 
  Sensor Deviation
  "set_cooling_state": added the new DGTO for Water Sensor Deviation (to avoid long wait) and fix EWT and LWT for Water 
  Sensor Deviation
  "set_exv_init_heating_state": added the new DGTO for Water Sensor Deviation (to avoid long wait) and fix EWT and LWT 
  for Water Sensor Deviation
  "set_exv_init_cooling_state": added the new DGTO for Water Sensor Deviation (to avoid long wait) and fix EWT and LWT 
  for Water Sensor Deviation
  "set_startup_heating_state": added the new DGTO for Water Sensor Deviation (to avoid long wait) and fix EWT and LWT 
  for Water Sensor Deviation
  "set_startup_cooling_state": added the new DGTO for Water Sensor Deviation (to avoid long wait) and fix EWT and LWT 
  for Water Sensor Deviation
  "set_waiting_activation_heating_state": added the new DGTO for Water Sensor Deviation (to avoid long wait),
  fix EWT and LWT for Water Sensor Deviation and fix method to stay in state 11 (and not in 14)
  "set_waiting_activation_cooling_state": added the new DGTO for Water Sensor Deviation (to avoid long wait),
  fix EWT and LWT for Water Sensor Deviation and fix method to stay in state 21 (and not in 24)
  "set_DEFROST_ENABLE_ON": updated the wait time for avoid problem with COP_CD calculation and added a Fault_Code reading
  in case a fault is present
  "set_Discharge_Pressure": updated the DGTO "CONTROL_BOARD_REG_RD_PD" because now it's public, tha names doesn't change
  "set_SuctionPressure: updated the DGTO "CONTROL_BOARD_REG_RD_PS" because now it's public, tha names doesn't change and
  fix the inverter management because the sensor is not present in the Ruking model but there is in the Ariston model.
  "write_dgto": updated number DGTO for "CONTROL_BOARD_REG_RD_PD" and "CONTROL_BOARD_REG_RD_PS"
  "set_FanSpeed_Feedback": updated DGTO to check the Fan1 speed feedback
  "get_pressure_sensor_presence": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter
  "get_CMP_Target": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter
  "check_suct_press_sensor_available": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter
  "check_disch_press_sensor_available": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter
  "set_HP_Evaporator_Temp_OCT": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter
  "set_Discharge_Temp_TD": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter
  "set_Suction_Temp": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter
  "set_Discharge_Pressure": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter
  "set_DriveStatus_InputPower": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter
  "set_DriveStatus_InputCurrent": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter
  "set_EM_HP_Evaporator_AUX": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter
  "set_LoadStatus_ControlMode": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter
  "set_Exv1Position_ControlMode": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter
  "set_LoadStatus_Feedback": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter
  "set_Exv1Position_Feedback": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter
  "set_FanSpeed_Feedback": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter
  "set_HP_Outdoor_Temp_OAT": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter
  "set_heatsink_temperature": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter
  "set_inverter_output_current": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter
  "set_inverter_cmp_heater_cur": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter
  "set_SYSTEM_SHUT_OFF_RD": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter
  "set_SYSTEM_FAULT_Shut_Down_EK_RD": added the set of WOLF CTRL_BOX_ID, because the fan is not handled inside the inverter

Changelog:
[0.6.0] - 2025-02-17:
- Added methods:

    "set_SYSTEM_SHUT_OFF_RD": added to write dgto "SYSTEM_SHUT_OFF_RD" (10-2-2-5)
    "set_SYSTEM_FAULT_Shut_Down_EK_RD": added to write dgto "SYSTEM_FAULT_SHUT_DOWN_EK_RD" (10-7-2-0)
    "set_TDM_HHP_INV_SYS_FAULT": added to write dgto "TDM_HHP_INV_SYS_FAULT" (10-4-3-2)

- Updated methods:
    "set_tdm_status": fixed temperatures when the TDM goes in DEFROST AUTOMATIC or DEFROST MANUAL
    
Changelog:
[0.5.0] - 2024-12-13:

- Updated methods:

    "read_var_ram": added reading of array in RAM
    "set_tdm_status": changed all wiring/reading reference from private DGTO "TDM_STATUS" to public DGTO "TDM - Status"
    "reset_tdm": changed all wiring/reading reference from private DGTO "TDM_STATUS" to public DGTO "TDM - Status"
    "service_reset_tdm": changed all wiring/reading reference from private DGTO "TDM_STATUS" to public DGTO "TDM - Status"
    "set_stanby": changed all wiring/reading reference from private DGTO "TDM_STATUS" to public DGTO "TDM - Status"
    "set_hard_stop": changed all wiring/reading reference from private DGTO "TDM_STATUS" to public DGTO "TDM - Status"
    "set_fault": changed all wiring/reading reference from private DGTO "TDM_STATUS" to public DGTO "TDM - Status"
    "set_hard_fault": changed all wiring/reading reference from private DGTO "TDM_STATUS" to public DGTO "TDM - Status"
    "set_heating_state": changed all wiring/reading reference from private DGTO "TDM_STATUS" to public DGTO "TDM - Status"
    "set_cooling_state": changed all wiring/reading reference from private DGTO "TDM_STATUS" to public DGTO "TDM - Status"
    "set_exv_init_heating_state": changed all wiring/reading reference from private DGTO "TDM_STATUS" to public DGTO "TDM - Status"
    "set_exv_init_cooling_state": changed all wiring/reading reference from private DGTO "TDM_STATUS" to public DGTO "TDM - Status"
    "set_defrost_basic_conditions": changed all wiring/reading reference from private DGTO "TDM_STATUS" to public DGTO "TDM - Status"
    "set_MANUALDEFROST_ENABLE_ON": changed all wiring/reading reference from private DGTO "TDM_STATUS" to public DGTO "TDM - Status"
    "set_DEFROST_ENABLE_ON": changed all wiring/reading reference from private DGTO "TDM_STATUS" to public DGTO "TDM - Status"
    "set_startup_heating_state": changed all wiring/reading reference from private DGTO "TDM_STATUS" to public DGTO "TDM - Status"
    "set_startup_cooling_state": changed all wiring/reading reference from private DGTO "TDM_STATUS" to public DGTO "TDM - Status"
    "set_waiting_activation_heating_state": changed all wiring/reading reference from private DGTO "TDM_STATUS" to public DGTO "TDM - Status"
    "set_waiting_activation_cooling_state": changed all wiring/reading reference from private DGTO "TDM_STATUS" to public DGTO "TDM - Status"
    
- Added methods:

    "ReadTDA": inherited from TestLib
    "WriteTDA": inherited from TestLib
    "readIdentTable": inherited from TestLib
    "send_reset": added function to send a real reset on TDM machine (no reset command for fault, real reset of the machine)
    "write_ram": added function to write RAM memory on TDM

Changelog:
[0.4.0] - 2024-11-21:
- Added methods:

    "set_LoadStatusNoise_ControlMode": added to enable/disable auto control of LoadStatus on Ariston inverters

- Updated methods:

    "get_FAN_Target": updated to requirement T_R290_A2W-2471
    "__init__": updated to work with all CTRL BOX ID
    "reset_tdm": check after reset on TDM Status  changed from visible wait at 5 seconds to invisible wait at 0.5 seconds
    "service_reset_tdm": check after reset on TDM Status changed from visible wait at 5 seconds to invisible wait at 0.5 seconds
    "set_stanby": added check on TDM Status to wait until TDM is not in Init after a reset
    "set_DEFROST_ENABLE_ON": added check on TDM Status to verify if TDM goes in fault during defrost operations
    "get_pressure_sensor_presence": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "get_CMP_Target": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "get_FAN_Speed": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "set_HP_Evaporator_Temp_OCT": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "set_Discharge_Temp_TD": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "set_Suction_Temp": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "set_Discharge_Pressure": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "set_DriveStatus_InputPower": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "set_DriveStatus_InputCurrent": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "set_EM_HP_Evaporator_AUX": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "set_LoadStatus_ControlMode": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "set_CompressorFrequency_ControlMode": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "set_Exv1Position_ControlMode": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "set_LoadStatus_Feedback": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "set_CompressorFrequency_Feedback": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "set_Exv1Position_Feedback": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "set_FanSpeed_ControlMode": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "set_FanSpeed_Feedback": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "set_SuctionPressure": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "set_HP_Outdoor_Temp_OAT": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "set_heatsink_temperature": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "set_inverter_output_current": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID
    "set_inverter_cmp_heater_cur": added gesture for all CTRL BOX ID contained in module CTRL_BOX_ID


Changelog:
[0.3.1] - 2024-11-07:

- Added methods:

    "set_Suction_Temp": added to write dgto "TS_RD" (10-1-2-25) TS 

- Updated defines:

    "PING_DEFAULT_TIMER" changed from 45s to 30s to speed up test execution

- Updated methods:    

    "__init__": added new parameter check_test_auto, if True at startup the TDM will check if the target device has the TestAutomation TDA
    "set_stanby": Moved some settings of DGTOs
    "set_DEFROST_ENABLE_ON": Updated from DGTO HP COP to COP_I_CMP_9_7
    "write_dgto": added DGTO HP_LOADS_POWER_W and EM HP Suction Temp
    "set_DriveStatus_InputPower": Updated target DGTO to CMP_ELECTRICAL_PWR_W and added gesture for CTRL BOX ID 112
    "get_pressure_sensor_presence": added gesture for CTRL BOX ID 112
    "get_CMP_Target": added gesture for CTRL BOX ID 112
    "get_FAN_Targete": added gesture for CTRL BOX ID 112
    "get_FAN_Speed": added gesture for CTRL BOX ID 112
    "set_HP_Evaporator_Temp_OCT": added gesture for CTRL BOX ID 112
    "set_Discharge_Temp_TD": added gesture for CTRL BOX ID 112
    "set_Discharge_Pressure": added gesture for CTRL BOX ID 112
    "set_DriveStatus_InputCurrent": added gesture for CTRL BOX ID 112
    "set_EM_HP_Evaporator_AUX": added gesture for CTRL BOX ID 112
    "set_LoadStatus_ControlMode": added gesture for CTRL BOX ID 112
    "set_Exv1Position_ControlMode": added gesture for CTRL BOX ID 112
    "set_LoadStatus_Feedback": added gesture for CTRL BOX ID 112
    "set_Exv1Position_Feedback": added gesture for CTRL BOX ID 112
    "set_FanSpeed_ControlMode": added gesture for CTRL BOX ID 112
    "set_FanSpeed_Feedback": added gesture for CTRL BOX ID 112
    "set_SuctionPressure": added gesture for CTRL BOX ID 112
    "set_HP_Outdoor_Temp_OAT": added gesture for CTRL BOX ID 112
    "set_heatsink_temperature": added gesture for CTRL BOX ID 112
    "set_inverter_output_current": added gesture for CTRL BOX ID 112
    "set_inverter_cmp_heater_cur": added gesture for CTRL BOX ID 112

Changelog:
[0.3.0] - 2024-09-30:

- Added functions:

    "set_exv_init_heating_state": used to set set_exv_init_heating_state on Inverter  
    "set_exv_init_cooling_state": used to set set_exv_init_cooling_state on Inverter  
    "set_DriveStatus_InputCurrent": used to set set_DriveStatus_InputCurrent on Inverter  
    "set_heatsink_temperature": used to set set_heatsink_temperature on Inverter  
    "set_inverter_output_current": used to set set_inverter_output_current on Inverter  
    "set_inverter_cmp_heater_cur": used to set set_inverter_cmp_heater_cur on Inverter  
    "set_CMP_Warning": used to set set_CMP_Warning on Inverter  
    "set_Speed_Drop_Protection_EK": used to set set_Speed_Drop_Protection_EK on Inverter  
    "set_TDM_HHP_Inv_Speed_Drop_Protect": used to set TDM_HHP_Inv_Speed_Drop_Protect on Inverter 
    "read_var_ram": to read variables directly from ram (only ariables present in module RAM_VAR)
    "read_ram": to read data from ram starting from an address (used from read_var_ram)
    "write_memory": inherited from TestLib

- Added modules:

    - import of new module for RAM VAR data: RAM_VAR

- Updated methods:

    "set_tdm_status": added status EXV_INIT_HEATING and EXV_INIT_COOLING

    "set_heating_state": fixed reset of counter TIMER1SEC_CMP_TIMEGUARD and TIMER1SEC_CMP_ANTICYCLING_TIMEGUARD if an 
    heating state is requested coming from another different heating/cooling state

    "set_cooling_state": fixed reset of counter TIMER1SEC_CMP_TIMEGUARD and TIMER1SEC_CMP_ANTICYCLING_TIMEGUARD if a 
    cooling state is requested coming from another different heating/cooling state

    "set_DriveStatus_InputPower": updated to new inverter register DGTO

    "write_dgto": added new DGTOs for Inverter: HP Power Calculation, INVERTER_INPUT_CURRENT, INVERTER_OUTPUT_CURRENT, 
    CMP_WARNINIG_RD, SPEED_DROP_PROTECTION_EK_RD, TDM_HHP_INV_SPEED_DROP_PROTECT, HEATSINK_TEMPERATURE, 
    INVERTER_REG_RD_OUTCURR_U, INVERTER_REG_RD_CMP_HTR_I_RD

    moved "calculate_cmd_from_status" from methods to function

Changelog:
[0.2.0] - 2024-07-01:

- Added functions:

    set_HP_Outdoor_Temp_OAT: used to set the value of dgto "HP Outdoor Temp (OAT)" (1-0-3-24) OutdoorTemperature
    set_lab_mode_active: used to activate Laboratory Mode
    set_tdm_status: used to bring the TDM to the requested status
    set_cooling_state: used to bring the TDM to the selected Status (Only cooling state: 25, 26, 27)
    reset_tdm: used to reset the TDM using a normal Reset Command and set the TDM_STATUS in init (101)
    call_keyword: used to call another testcases script as a keyword
    set_tdm_status: used to bring the TDM to the requested status 
    service_reset_tdm: used to reset the TDM using a Service Reset Command and set the TDM_STATUS in init (101)
    set_hard_stop: used to bring the TDM to Hard Stop Heating State (TDM_STATUS = 19) using fault 1992/1993
    set_fault: used to bring the TDM to Fault State (TDM_STATUS = 51) using fault 2067
    set_hard_fault: used to bring the TDM to Hard Fault State (TDM_STATUS = 52) using fault 2068
    calculate_cmd_from_status: used to calculate the value of the commmand to send on DGTO Generator External Request  
    (15-7-2-4) to enable the selected Status
    set_MANUALDEFROST_ENABLE_ON: used to set DEFROST_ENABLE = 1 to start ManualDefrost routine
    set_HP_Outdoor_Temp_OAT: Ticket #34, used to set the value of dgto "HP Outdoor Temp (OAT)" (1-0-3-24) OutdoorTemperature
    set_startup_heating_state: used to bring the TDM to the selected Status 14
    set_startup_cooling_state: used to bring the TDM to the selected Status 24
    set_waiting_activation_heating_state: used to bring the TDM to the selected Status 14
    set_waiting_activation_cooling_state: used to bring the TDM to the selected Status 24
    

- Modified functions:
    set_stanby
    __init_
    __del__: Ticket #30
    set_heating_state
    set_stanby
    set_heating_state
    set_cooling_state
    set_defrost_basic_conditions
    set_DEFROST_ENABLE_ON
    write_dgto: Ticket #35

- Added class/structures:

    TDM_STATUS_LIST: 
    TDMException: 
    
- Added defines:
 
    DEFAULT_EWT_FILTER_TIME_MSEC: New value of DGTO EWT_FILTER_TIME_MSEC due to Ticket #14594
    
[0.1.3] - 2024-05-23:

- Added functions:
    get_active_compressor_control_mode: Used to get the compressor control mode in use
    get_generator_status: Used to get the generator status value
    get_hr_mode: Used to get the current heat request mode
    get_modulation_mode: Used to get the current modulation mode setting
    get_external_request: Used to get the current external request setting
    set_generator_external_request: Used to set the Generator Request (simulation of EM command)
    __del__: Destructor of the class, used to update the report
    
- Modified functions:
    __init__: added single_report parameter(to be used in destructor).
    set_heating_state: updated to the new interface

[0.1.2] - 2024-04-04:

- Added function "get_pressure_sensor_presence":
    Function used to understand if the current inverter has pressure sensor
    
- Added function "get_FAN_Target": 
    Function to read the Fan rpm Target in base of the inverter connected
    
- Added function "get_FAN_Speed":
    Function to read the Fan rpm feedback value of the inverter connected

- Renamed function "get_CMP_Freq" to "get_CMP_Target".


[0.1.1] - 2024-03-12:

- Added function "get_CMP_Freq":
    Function used to read the CMP_Freq with every type of Inverter

- Fixed function "set_DEFROST_ENABLE_ON": 
    Removed useless code
    
- Changed function "set_DriveStatus_InputPower": 
    Now the input power can be passed without dividing it by 4

[0.1.0] - 2024-03-12:

- First release
"""

# ------------------------------------------------
# Defines Version
# ------------------------------------------------

# Defines for Inverter management
DEFAULT_CHECK_VALUE = DEFAULT_SAVE_VALUE = True  # If true every writing action will be checked
DEFAULT_CHECK_TIMER = 7  # 10s between writing and read-check value
AVAILABLE_BOX_ID = CTRL_BOX_ID.BOX_ID

# Defines for TDM management
HEAT_COOLING_TIMER = 80  # 60s as max time to reach an heating/cooling state
PING_DEFAULT_TIMER = 30  # 30s as max time to reach the expected value with TestLib function ping_dgto()
HEATING_DEFAULT_SETPOINT = 600  # 60°C
COOLING_DEFAULT_SETPOINT = 100  # 10°C
MAX_HP_POWER_CALC = 7690
BROKEN_PROBE_VALUE = 0x7FFF  # 32767
DEFAULT_EWT_FILTER_TIME_MSEC = 100

TDM_STATUS_LIST = {
    "INIT":                       101,
    "STANDBY":                    1,
    "HARD_STOP":                  50,
    "FAULT":                      51,
    "HARD_FAULT":                 52,
    "HEATING_HARD_STOP":          19,
    "COOLING_HARD_STOP":          29,
    "WAITING_ACTIVATION_HEATING": 11,
    "WAITING_ACTIVATION_COOLING": 21,
    "EXV_RESET_HEATING":          12,
    "EXV_INIT_HEATING":           13,
    "STARTUP_HEATING":            14,
    "EXV_RESET_COOLING":          22,
    "EXV_INIT_COOLING":           23,
    "STARTUP_COOLING":            24,
    "MODULATION_HEATING":         15,
    "MODULATION_COOLING":         25,
    "BOOST_HEATING":              16,
    "RATING_HEATING":             17,
    "BOOST_COOLING":              26,
    "RATING_COOLING":             27,
    "DEFROST_AUTOMATIC":          18,
    "DEFROST_MANUAL":             40
}


# ------------------------------------------------
# Function Module
# ------------------------------------------------
def calculate_cmd_from_status(status: int) -> int:
    """
        Calculate the value of the command to send on DGTO Generator External Request  (15-7-2-4) to enable the selected TDM_STATUS
        :param status: the status related to the command

        :return: the var command with the command related to the selected status
    """
    command = None

    if status == TDM_STATUS_LIST["MODULATION_HEATING"]:  # Modulating
        command = 3
    elif status == TDM_STATUS_LIST["BOOST_HEATING"]:  # Boost Mode
        command = 5
    elif status == TDM_STATUS_LIST["RATING_HEATING"]:  # Rating Mode
        command = 4
    elif status == TDM_STATUS_LIST["MODULATION_COOLING"]:  # Modulating
        command = 6
    elif status == TDM_STATUS_LIST["BOOST_COOLING"]:  # Boost Mode
        command = 8
    elif status == TDM_STATUS_LIST["RATING_COOLING"]:  # Rating Mode
        command = 7

    return command


# ------------------------------------------------
# Classes Module
# ------------------------------------------------

# Classes for Inverter exception (e.g. CTRL_BOX_ID not recognized)
class InverterException(Exception):
    pass


# Classes for TDM exception (e.g. Wrong TDA or wrong TestLib Version detected)
class TDMException(Exception):
    pass


class TDM_Manager:
    _testlib = None
    _CTRL_BOX_ID = None
    _single_report = False


    def __init__(self, tdm_object: dict, single_report: bool = False, check_test_auto: bool = True) -> None:
        """
            Constructor of the class.

            :param tdm_object: configuration given by ConfigParser, used to create object TestLib
            :param single_report: if True, the report will be update in destructor
            :param check_test_auto: if True, the object will be created only if the target device has the TDA of TestAutomation

            :return: None

            :raise InverterException: if the CTRL_BOX_ID is not correctly read from TDM or if is not recognized
                   TDMException: if check_test_auto is True and the TDA read from the board is not the one for Test Automation (defined in var TDA_TestAutomation)
        """
        if TestLib_version != Framework_Ver:
            self._testlib._report.add_comment_row(f"WARNING: "
                                                  f"TestLib ver. detected: {TestLib_version} but TDM_Manager needs "
                                                  f"TestLib ver. {Framework_Ver}.", print_on_console=True,
                                                  background_color="WARNING")

        self._tdm_object = tdm_object
        self._testlib = TestLib(tdm_object)

        if check_test_auto:
            tda = self._testlib.ReadTDA()

            if tda is not None:
                if tda != TDA_TestAutomation:
                    raise TDMException(f"ERROR! TDM not in test automation, TDA read = {tda}, "
                                       f"please set TDA equal to {TDA_TestAutomation} and reboot the TDM.")
            else:
                raise TDMException(f"ERROR! Impossible to read the TDA.")

        self._CTRL_BOX_ID = self._testlib.read_dgto(
                "HP CTRL BOX ID RD")  # Take the value of "HP CTRL BOX ID RD" (9-12-6-11)
        self._single_report = single_report

        config_discovered = False

        if self._CTRL_BOX_ID is not None:
            for box_id in AVAILABLE_BOX_ID:
                if self._CTRL_BOX_ID == box_id:
                    config_discovered = True

        if not config_discovered:
            raise InverterException(
                    f"CTRL_BOX_ID = {self._CTRL_BOX_ID} not valid, communication with the Inverter absent,"
                    f" please check the communication on PRG026.")

        if self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            self._modifier = 10

        ewt_filter = self._testlib.read_dgto("EWT_FILTER_TIME_CONST_MSEC")

        if ewt_filter != DEFAULT_EWT_FILTER_TIME_MSEC:
            self._testlib.write_dgto("EWT_FILTER_TIME_CONST_MSEC", DEFAULT_EWT_FILTER_TIME_MSEC, 1)

        self._testlib._report.add_comment_row(f"CTRL_BOX_ID = {self._CTRL_BOX_ID} found.", "INFO", True)


    def __del__(self):
        """
            Destructor of the class.

            this function updates the report and closes the instance of the TestLib

            :return: None
        """
        if self._single_report:
            print("Test passed" if self.test_passed else "Test failed")
            self._testlib._report.update_report(self.test_passed)

        if self._testlib is not None:
            del self._testlib


    """
                                    ---------------------
                                    --  TDM functions  --
                                    ---------------------
    """


    def call_keyword(self, keyword: str, parameters: str = "") -> bool:
        """
            Call the selected keyword, used to call another testcases script as a keyword

            NOTE: the py file of the keyword must be present in the same directory of the script who calls it

            :param keyword: a string contained the selected keyword to use
            :param parameters: eventual parameters to be added to the keyword

            see section Keywords on doc. TDM_Manager_SWSpecifications_XvY.docx for all info about keywords

            :return: the value of result: "True" if the keyword is executed successfully with positive result, otherwise "False"
        """
        del self._testlib
        time.sleep(3)
        response = os.system(f"python {keyword}.py {parameters}")

        self._testlib = TestLib(self._tdm_object)

        result = response == 0

        return result


    def set_tdm_status(self, status: int = None):
        """
            Bring the TDM to the requested status

            :param status: the target status to set, the value to use can be found in dict TDM_Manager.TDM_STATUS_LIST

            Available Status:
                - STANDBY: (1)
                - DEFROST_MANUAL: (40)
                - DEFROST_AUTOMATIC: (18)
                - HEATING_HARD_STOP: (19)
                - FAULT: (51)
                - HARD_FAULT: (52)
                - STARTUP_HEATING: (14)
                - STARTUP_COOLING: (24)
                - INIT: (101)
                - WAITING_ACTIVATION_HEATING: (11)
                - WAITING_ACTIVATION_COOLING: (21)
                - MODULATION_HEATING: (15)
                - MODULATION_COOLING: (25)
                - BOOST_HEATING: (16)
                - RATING_HEATING: (17)
                - BOOST_COOLING: (26)
                - RATING_COOLING:(27)

            :return: "True" if the TDM goes correctly to the requested status, otherwise "False"
        """
        res = False
        tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status != status:
            if status == TDM_STATUS_LIST["STANDBY"]:
                res = self.set_stanby(True)
            elif TDM_STATUS_LIST["MODULATION_HEATING"] <= status <= TDM_STATUS_LIST["RATING_HEATING"]:
                res = self.set_heating_state(status)
            elif TDM_STATUS_LIST["MODULATION_COOLING"] <= status <= TDM_STATUS_LIST["RATING_COOLING"]:
                res = self.set_cooling_state(status)
            elif TDM_STATUS_LIST["DEFROST_MANUAL"] == status:
                if self.set_tdm_status(15) and self.set_MANUALDEFROST_ENABLE_ON():
                    tdm_status = self.read_dgto("TDM - Status", True)

                    for i in range(30):
                        if tdm_status == TDM_STATUS_LIST["DEFROST_MANUAL"]:
                            break
                        self.wait_time(1)
                        tdm_status = self.read_dgto("TDM - Status", True)

                    if tdm_status == TDM_STATUS_LIST["DEFROST_MANUAL"]:
                        lwt = self.read_dgto("HP Water Flow Temp (LWT)")
                        self.write_dgto("HP Water Return Temp (EWT)", lwt + 10)
                        res = True
            elif TDM_STATUS_LIST["DEFROST_AUTOMATIC"] == status:
                if self.set_tdm_status(15) and self.set_DEFROST_ENABLE_ON():
                    tdm_status = self.read_dgto("TDM - Status", True)

                    for i in range(30):
                        if tdm_status == TDM_STATUS_LIST["DEFROST_AUTOMATIC"]:
                            break
                        self.wait_time(1)
                        tdm_status = self.read_dgto("TDM - Status", True)

                    if tdm_status == TDM_STATUS_LIST["DEFROST_AUTOMATIC"]:
                        lwt = self.read_dgto("HP Water Flow Temp (LWT)")
                        self.write_dgto("HP Water Return Temp (EWT)", lwt + 10)
                        res = True
            elif TDM_STATUS_LIST["HEATING_HARD_STOP"] == status:
                res = self.set_hard_stop()
            elif TDM_STATUS_LIST["FAULT"] == status:
                res = self.set_fault()
            elif TDM_STATUS_LIST["HARD_FAULT"] == status:
                res = self.set_hard_fault()
            elif TDM_STATUS_LIST["STARTUP_HEATING"] == status:
                res = self.set_startup_heating_state(TDM_STATUS_LIST["MODULATION_HEATING"])
            elif TDM_STATUS_LIST["STARTUP_COOLING"] == status:
                res = self.set_startup_cooling_state(TDM_STATUS_LIST["MODULATION_COOLING"])
            elif TDM_STATUS_LIST["INIT"] == status:
                res = self.reset_tdm()
            elif TDM_STATUS_LIST["WAITING_ACTIVATION_HEATING"] == status:
                res = self.set_waiting_activation_heating_state(TDM_STATUS_LIST["MODULATION_HEATING"])
            elif TDM_STATUS_LIST["WAITING_ACTIVATION_COOLING"] == status:
                res = self.set_waiting_activation_cooling_state(TDM_STATUS_LIST["MODULATION_COOLING"])
            elif TDM_STATUS_LIST["EXV_INIT_HEATING"] == status:
                res = self.set_exv_init_heating_state(TDM_STATUS_LIST["MODULATION_HEATING"])
            elif TDM_STATUS_LIST["EXV_INIT_COOLING"] == status:
                res = self.set_exv_init_cooling_state(TDM_STATUS_LIST["MODULATION_COOLING"])
        else:
            res = True

        return res


    def reset_tdm(self) -> bool:
        """
            Reset the TDM using a normal Reset Command and set the TDM_STATUS in init (101)

            :return: "True" if the TDM reset itself correctly, otherwise "False"
        """

        self._testlib.write_dgto("RESET Cmd", 30)

        tdm_status = self._testlib.read_dgto("TDM - Status")

        for i in range(30):
            if tdm_status == 101:
                break
            time.sleep(0.5)
            tdm_status = self._testlib.read_dgto("TDM - Status")

        return tdm_status == TDM_STATUS_LIST["INIT"]


    def service_reset_tdm(self) -> bool:
        """
            Reset the TDM using a Service Reset Command and set the TDM_STATUS in init (101)

            :return: "True" if the TDM reset itself correctly, otherwise "False"
        """

        self._testlib.write_dgto("HP Service RESET", 30)

        tdm_status = self._testlib.read_dgto("TDM - Status")

        for i in range(30):
            if tdm_status == 101:
                break
            time.sleep(0.5)
            tdm_status = self._testlib.read_dgto("TDM - Status")

        return tdm_status == TDM_STATUS_LIST["INIT"]


    def set_stanby(self, force: bool = False) -> bool:
        """
            Bring the TDM to Standby Status (TDM_STATUS = 1)

            :param force:   if True the function will perform any action to set
                            the TDM in stanby even if is already the current status

            :return: "True" if the TDM goes correctly to Standby, otherwise "False"
        """
        tdm_status = self._testlib.read_dgto("TDM - Status", True)
        c = 0
        while tdm_status == 101:
            time.sleep(1)
            tdm_status = self._testlib.read_dgto("TDM - Status", True)
            if c >= PING_DEFAULT_TIMER:
                break
            c = c + 1

        lab_mode_state = self._testlib.read_dgto("LAB_MODE_ENABLE_STATE")

        if lab_mode_state == 4:
            self._testlib.write_dgto("LAB_MODE_ENABLE_KEY1", 0)
            self._testlib.write_dgto("LAB_MODE_ENABLE_KEY2", 0)

        tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status == TDM_STATUS_LIST["STANDBY"] and not force:
            return True

        if tdm_status == TDM_STATUS_LIST["DEFROST_AUTOMATIC"] or tdm_status == TDM_STATUS_LIST["DEFROST_MANUAL"]:
            defrost_exit_tmp = self.read_dgto("TE_DEFROST_EXIT_HI")
            self.write_dgto("HP Evaporator Temp (OCT)", defrost_exit_tmp + 20)
        elif tdm_status == TDM_STATUS_LIST["FAULT"]:
            self.reset_tdm()

            status = self._testlib.read_dgto("TDM - Status", True)
            c = 0
            while status == 101:
                time.sleep(1)
                status = self._testlib.read_dgto("TDM - Status", True)
                if c >= PING_DEFAULT_TIMER:
                    break
                c = c + 1
        elif tdm_status == TDM_STATUS_LIST["HARD_FAULT"]:
            self.service_reset_tdm()

            status = self._testlib.read_dgto("TDM - Status", True)
            c = 0
            while status == 101:
                time.sleep(1)
                status = self._testlib.read_dgto("TDM - Status", True)
                if c >= PING_DEFAULT_TIMER:
                    break
                c = c + 1

        ewt_filter = self._testlib.read_dgto("EWT_FILTER_TIME_CONST_MSEC")

        if ewt_filter != DEFAULT_EWT_FILTER_TIME_MSEC:
            self._testlib.write_dgto("EWT_FILTER_TIME_CONST_MSEC", DEFAULT_EWT_FILTER_TIME_MSEC, 1)

        self._testlib.write_dgto("TEST_BENCH_EBUS2", 1, 1)
        self._testlib.write_dgto("HP EXTERNAL Set Point", 0, 1)
        self.set_generator_external_request(0, 0, 0)
        # Set DGTOs of the sensors' temperatures connected to the TDM
        self._testlib._report.add_comment_row("Set DGTOs of the sensors' temperatures connected to the TDM")
        self._testlib.write_dgto("HP Water Flow Temp (LWT)", 290, 1)
        self._testlib.write_dgto("HP Water Return Temp (EWT)", 280, 1)
        self._testlib.write_dgto("EM HP Refrigerant Temp", 300, 1)
        self.write_dgto("EM HP Suction Temp", 80, 10)
        self._testlib.write_dgto("START_TEMP_LWT_MAX", 820, 1)
        self._testlib.write_dgto("START_TEMP_LWT_MIN", 50, 1)

        self.set_LoadStatus_ControlMode(1, False)
        self.set_LoadStatusNoise_ControlMode(1, False)
        self.set_CompressorFrequency_ControlMode(1, False)
        self.set_Exv1Position_ControlMode(1, False)
        self.set_FanSpeed_ControlMode(1, False)
        self.set_Discharge_Pressure(500, False)
        self.set_SuctionPressure(400, False)
        self.set_DriveStatus_InputPower(0, False)

        self.set_HP_Evaporator_Temp_OCT(20, False)
        self.set_Discharge_Temp_TD(20, False)
        self.set_EM_HP_Evaporator_AUX(25, False)
        self.set_HP_Outdoor_Temp_OAT(20, False)

        self.save_InverterValue()

        # Set the EM related DGTOs
        self._testlib._report.add_comment_row("Set the EM related DGTOs")

        self._testlib.write_dgto("Generator Max Thermal Power Percentage", 25600)  # Max CMP power = 100%, var in 8_8
        self._testlib.write_dgto("Demand Integral Min", 10000, 1)
        self._testlib.write_dgto("Demand Integral Max", 20000, 1)
        self._testlib.write_dgto("Demand Generator Max Overshoot", 50, 1)
        self._testlib.write_dgto("Demand Coefficient K", 256, 1)
        self._testlib.write_dgto("Demand Generator Max Undershoot", 50, 1)

        # Check of the flowmeter
        flow = self._testlib.read_dgto("EM Flow meter")

        if flow < 10:
            self._testlib.write_dgto("Circulator Control Mode Running", 0, 1)
            self._testlib.write_dgto("Circulator MIN PWM", 10, 1)
            self._testlib.write_dgto("Circulator MAX PWM", 100, 1)
        else:
            self._testlib.write_dgto("Circulator Control Mode Running", 1, 1)
            self._testlib.write_dgto("Circulator MIN PWM", 10, 1)
            self._testlib.write_dgto("Circulator MAX PWM", 100, 1)

        self._testlib.wait_time(10)

        tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status != 1:
            self._testlib._report.add_comment_row("TDM_STATUS = 1 not reached.",
                                                  background_color="WARNING", print_on_console=True)
            return False

        return True


    def set_hard_stop(self) -> bool:
        """
            Bring the TDM to Hard Stop Heating State (TDM_STATUS = 19) using fault 1992/1993

            :return: "True" if the TDM goes correctly to Hard Stop state, otherwise "False"
        """
        self._testlib._report.add_comment_row(f"Procedure to set TDM on Startup State in Cooling started.",
                                              print_on_console=True)

        tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status == TDM_STATUS_LIST["HEATING_HARD_STOP"]:
            self._testlib._report.add_comment_row(
                    f"TDM_STATUS {TDM_STATUS_LIST['HEATING_HARD_STOP']} was already active.",
                    background_color="WARNING", print_on_console=True)
            return True

        # Check of the flowmeter
        flow = self._testlib.read_dgto("EM Flow meter")

        if flow < 10:
            self._testlib.write_dgto("Circulator Control Mode Running", 1, 1)
        else:
            self._testlib.write_dgto("Circulator Control Mode Running", 0, 1)

        for i in range(HEAT_COOLING_TIMER):
            if tdm_status == TDM_STATUS_LIST["HEATING_HARD_STOP"]:
                break
            self._testlib.wait_time(1)
            tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status == TDM_STATUS_LIST["HEATING_HARD_STOP"]:
            return True

        self._testlib._report.add_comment_row(f"TDM_STATUS {TDM_STATUS_LIST['HEATING_HARD_STOP']} not reached.",
                                              background_color="WARNING", print_on_console=True)

        return False


    def set_fault(self) -> bool:
        """
            Bring the TDM to Fault State (TDM_STATUS = 51) using fault 2067

            :return: "True" if the TDM goes correctly to Fault, otherwise "False"
        """
        self._testlib._report.add_comment_row(f"Procedure to set TDM on Startup State in Cooling started.",
                                              print_on_console=True)

        tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status == TDM_STATUS_LIST["FAULT"]:
            self._testlib._report.add_comment_row(f"TDM_STATUS {TDM_STATUS_LIST['FAULT']} was already active.",
                                                  background_color="WARNING", print_on_console=True)
            return True

        self._testlib.write_dgto("DGTO_PERMANENT_TDMFAULT_FREEZE_N", 4)
        self._testlib.write_dgto("TWALL_MIN", -32767)
        self._testlib.write_dgto("TWALL_OFF", 0)
        self._testlib.write_dgto("C2_BPHE_8_8", 0)
        self._testlib.write_dgto("C1_BPHE_8_8", 0)

        self._testlib.write_dgto("TIMER1SEC_CMP_TIMEGUARD", 0, 1)
        self._testlib.write_dgto("TIMER1SEC_CMP_ANTICYCLING_TIMEGUARD", 0, 1)
        self._testlib.write_dgto("START_TD_TIME_PARAM", 0, 1)
        self._testlib.write_dgto("START_TEMP_LWT_MIN", 50, 1)
        self._testlib.write_dgto("HP Water Flow Temp (LWT)", 240, 1)
        self._testlib.write_dgto("HP Water Return Temp (EWT)", 235, 1)
        self.write_dgto("EM HP Refrigerant Temp", 170, 3)
        self.write_dgto("HP Evaporator Temp (OCT)", 200, 3)
        self._testlib.write_dgto("HP EXTERNAL Set Point", 100, 1)
        self.set_generator_external_request(6, 0, 1)

        for i in range(HEAT_COOLING_TIMER):
            if tdm_status == TDM_STATUS_LIST["FAULT"]:
                break
            self._testlib.wait_time(1)
            tdm_status = self._testlib.read_dgto("TDM - Status")

        self.set_generator_external_request(0, 0, 0)
        self._testlib.write_dgto("TWALL_MIN", 0)

        if tdm_status == TDM_STATUS_LIST["FAULT"]:
            return True

        self._testlib._report.add_comment_row(f"TDM_STATUS {TDM_STATUS_LIST['FAULT']} not reached.",
                                              background_color="WARNING", print_on_console=True)

        return False


    def set_hard_fault(self) -> bool:
        """
            Bring the TDM to Hard Fault State (TDM_STATUS = 52) using fault 2068

            :return: "True" if the TDM goes correctly to Fault, otherwise "False"
        """
        self._testlib._report.add_comment_row(f"Procedure to set TDM on Startup State in Cooling started.",
                                              print_on_console=True)

        tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status == TDM_STATUS_LIST["HARD_FAULT"]:
            self._testlib._report.add_comment_row(f"TDM_STATUS {TDM_STATUS_LIST['HARD_FAULT']} was already active.",
                                                  background_color="WARNING", print_on_console=True)
            return True

        self._testlib.write_dgto("DGTO_PERMANENT_TDMFAULT_FREEZE_N", 4)
        self._testlib.write_dgto("PERMANENT_TDMFAULT_FREEZE_M", 3)
        self._testlib.write_dgto("TWALL_MIN", -32767)
        self._testlib.write_dgto("TWALL_OFF", 0)
        self._testlib.write_dgto("C2_BPHE_8_8", 0)
        self._testlib.write_dgto("C1_BPHE_8_8", 0)

        self._testlib.write_dgto("TIMER1SEC_CMP_TIMEGUARD", 0, 1)
        self._testlib.write_dgto("TIMER1SEC_CMP_ANTICYCLING_TIMEGUARD", 0, 1)
        self._testlib.write_dgto("START_TD_TIME_PARAM", 0, 1)
        self._testlib.write_dgto("START_TEMP_LWT_MIN", 50, 1)
        self._testlib.write_dgto("HP Water Flow Temp (LWT)", 240, 1)
        self._testlib.write_dgto("HP Water Return Temp (EWT)", 235, 1)
        self.write_dgto("EM HP Refrigerant Temp", 170, 3)
        self.write_dgto("HP Evaporator Temp (OCT)", 200, 3)
        self._testlib.write_dgto("HP EXTERNAL Set Point", 100, 1)
        self.set_generator_external_request(6, 0, 1)

        for i in range(HEAT_COOLING_TIMER):
            if tdm_status == TDM_STATUS_LIST["HARD_FAULT"]:
                break
            self._testlib.wait_time(1)
            tdm_status = self._testlib.read_dgto("TDM - Status")

        self.set_generator_external_request(0, 0, 0)
        self._testlib.write_dgto("TWALL_MIN", 0)

        if tdm_status == TDM_STATUS_LIST["HARD_FAULT"]:
            return True

        self._testlib._report.add_comment_row(f"TDM_STATUS {TDM_STATUS_LIST['HARD_FAULT']} not reached.",
                                              background_color="WARNING", print_on_console=True)

        return False


    def get_CTRL_BOX_ID(self):
        """
            Return the current CTRL_BOX_ID loaded on TDM

            :return: value of DGTO "HP CTRL BOX ID RD" (9-12-6-11)
        """
        return self._CTRL_BOX_ID


    def set_heating_state(self, status: int, target: int = HEATING_DEFAULT_SETPOINT) -> bool:
        """
            Bring the TDM to the selected Status (Only heating state: 15, 16, 17)

            :param status: the status to set:
                15 - Modulation
                16 - Boost Mode
                17 - Rating Mode
            :param target: The target temperature to set (in Heating)

            :return: "True" if the TDM goes correctly trough all phases before the selected state, otherwise "False"
        """

        control_mode = calculate_cmd_from_status(status)

        if status == TDM_STATUS_LIST["BOOST_HEATING"]:  # Boost Mode
            self._testlib.write_dgto("TDM Compressor Fixed Frequency", 45, 1)
        elif status == TDM_STATUS_LIST["RATING_HEATING"]:  # Rating Mode
            self._testlib.write_dgto("EM Fixed Frequency", 52, 1)
            self._testlib.write_dgto("EM Fixed FAN 1 Speed (rpm)", 500, 1)
            self._testlib.write_dgto("EM Fixed FAN 2 Speed (rpm)", 450, 1)

        if control_mode is None:
            self._testlib._report.add_comment_row(
                    f"TDM_STATUS {status} cannot be settled with set_heating_state function.",
                    background_color="WARNING", print_on_console=True)
            return False

        self._testlib._report.add_comment_row(f"Procedure to set TDM on Heating State {status} started.",
                                              print_on_console=True)

        self._testlib.write_dgto("TIMER1SEC_CMP_TIMEGUARD", 0, 1)
        self._testlib.write_dgto("TIMER1SEC_CMP_ANTICYCLING_TIMEGUARD", 0, 1)
        self._testlib.write_dgto("START_TD_TIME_PARAM", 0, 1)
        self._testlib.write_dgto("START_TEMP_LWT_MAX", 820, 1)
        self._testlib.write_dgto("WATER_DT_START_TIME_MAX", 200, 1)
        self._testlib.write_dgto("WATER_DT_TIME_INITIAL", 5, 1)
        self._testlib.write_dgto("WATER_DT_THRESHOLD_TIME_MAX", 5, 1)
        self._testlib.write_dgto("HP Water Flow Temp (LWT)", target - 180, 1)
        self._testlib.write_dgto("HP Water Return Temp (EWT)", target - 190, 1)
        self.write_dgto("EM HP Refrigerant Temp", 200, 3)
        self.write_dgto("HP Evaporator Temp (OCT)", 170, 3)
        self._testlib.write_dgto("HP EXTERNAL Set Point", target, 1)
        self.set_generator_external_request(control_mode, 0, 0)

        self._testlib.wait_time(2)

        self._testlib.write_dgto("TIMER1SEC_CMP_TIMEGUARD", 0)
        self._testlib.write_dgto("TIMER1SEC_CMP_ANTICYCLING_TIMEGUARD", 0)

        tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status == status:
            self._testlib._report.add_comment_row(f"TDM_STATUS {status} was already active.",
                                                  background_color="WARNING", print_on_console=True)
            return True

        for i in range(HEAT_COOLING_TIMER):
            if tdm_status == TDM_STATUS_LIST["EXV_INIT_HEATING"] or tdm_status == TDM_STATUS_LIST["STARTUP_HEATING"]:
                break
            self._testlib.wait_time(1)
            tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status != TDM_STATUS_LIST["EXV_INIT_HEATING"] and tdm_status != TDM_STATUS_LIST["STARTUP_HEATING"]:
            self._testlib._report.add_comment_row("TDM_STATUS 13 not reached.",
                                                  background_color="WARNING", print_on_console=True)
            return False

        self.set_DriveStatus_InputPower(500, True, False)  # Set Input Drive for compressor

        tdm_status = self._testlib.read_dgto("TDM - Status")

        for i in range(HEAT_COOLING_TIMER):
            if tdm_status == TDM_STATUS_LIST["STARTUP_HEATING"]:
                break
            self._testlib.wait_time(1)
            tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status != TDM_STATUS_LIST["STARTUP_HEATING"]:
            self._testlib._report.add_comment_row("TDM_STATUS 14 not reached.",
                                                  background_color="WARNING", print_on_console=True)
            return False

        timer_startup = self._testlib.read_dgto("TIMER1SEC_STARTUP")
        for i in range(HEAT_COOLING_TIMER):
            if timer_startup <= 177:
                break
            self._testlib.wait_time(1)
            timer_startup = self._testlib.read_dgto("TIMER1SEC_STARTUP")

        if timer_startup > 177:
            self._testlib._report.add_comment_row("TDM blocked in status 14, TIMER1SEC_STARTUP doesn't start.",
                                                  background_color="WARNING", print_on_console=True)
            return False

        self._testlib.write_dgto("TIMER1SEC_STARTUP", 0, 1)

        for i in range(HEAT_COOLING_TIMER):
            if tdm_status == status:
                break
            self._testlib.wait_time(1)
            tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status != status:
            self._testlib._report.add_comment_row(f"TDM_STATUS {status} not reached.",
                                                  background_color="WARNING", print_on_console=True)
            return False

        return True


    def set_cooling_state(self, status: int, target: int = COOLING_DEFAULT_SETPOINT) -> bool:
        """
            Bring the TDM to the selected Status (Only cooling state: 25, 26, 27)

            :param status: the status to set:
                25 - Modulation
                26 - Boost Mode
                27 - Rating Mode
            :param target: The target temperature to set (in Cooling)

            :return: "True" if the TDM goes correctly trough all phases before the selected state, otherwise "False"
        """

        control_mode = calculate_cmd_from_status(status)

        if status == TDM_STATUS_LIST["BOOST_COOLING"]:  # Boost Mode
            self._testlib.write_dgto("TDM Compressor Fixed Frequency", 45, 1)
        elif status == TDM_STATUS_LIST["RATING_COOLING"]:  # Rating Mode
            self._testlib.write_dgto("EM Fixed Frequency", 52, 1)
            self._testlib.write_dgto("EM Fixed FAN 1 Speed (rpm)", 500, 1)  # TO VERIFY IF IS NECESSARY

        if control_mode is None:
            self._testlib._report.add_comment_row(
                    f"TDM_STATUS {status} cannot be settled with set_cooling_state function.",
                    background_color="WARNING", print_on_console=True)
            return False

        self._testlib._report.add_comment_row(f"Procedure to set TDM on Cooling State {status} started.",
                                              print_on_console=True)
        self._testlib.write_dgto("TIMER1SEC_CMP_TIMEGUARD", 0, 1)
        self._testlib.write_dgto("TIMER1SEC_CMP_ANTICYCLING_TIMEGUARD", 0, 1)
        self._testlib.write_dgto("START_TD_TIME_PARAM", 0, 1)
        self._testlib.write_dgto("START_TEMP_LWT_MIN", 50, 1)
        self._testlib.write_dgto("WATER_DT_START_TIME_MAX", 200, 1)
        self._testlib.write_dgto("WATER_DT_TIME_INITIAL", 5, 1)
        self._testlib.write_dgto("WATER_DT_THRESHOLD_TIME_MAX", 5, 1)
        self._testlib.write_dgto("HP Water Flow Temp (LWT)", target + 160, 1)
        self._testlib.write_dgto("HP Water Return Temp (EWT)", target + 170, 1)
        self.write_dgto("EM HP Refrigerant Temp", 170, 3)
        self.write_dgto("HP Evaporator Temp (OCT)", 200, 3)
        self._testlib.write_dgto("HP EXTERNAL Set Point", target, 1)
        self.set_generator_external_request(control_mode, 0, 1)

        self._testlib.wait_time(2)

        self._testlib.write_dgto("TIMER1SEC_CMP_TIMEGUARD", 0)
        self._testlib.write_dgto("TIMER1SEC_CMP_ANTICYCLING_TIMEGUARD", 0)

        tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status == status:
            self._testlib._report.add_comment_row(f"TDM_STATUS {status} was already active.",
                                                  background_color="WARNING", print_on_console=True)
            return True

        for i in range(HEAT_COOLING_TIMER):
            if tdm_status == TDM_STATUS_LIST["EXV_INIT_COOLING"] or tdm_status == TDM_STATUS_LIST["STARTUP_COOLING"]:
                break
            self._testlib.wait_time(1)
            tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status != TDM_STATUS_LIST["EXV_INIT_COOLING"] and tdm_status != TDM_STATUS_LIST["STARTUP_COOLING"]:
            self._testlib._report.add_comment_row("TDM_STATUS 23 not reached.",
                                                  background_color="WARNING", print_on_console=True)
            return False

        self.set_DriveStatus_InputPower(500, True, False)  # Set Input Drive for compressor

        tdm_status = self._testlib.read_dgto("TDM - Status")

        for i in range(HEAT_COOLING_TIMER):
            if tdm_status == TDM_STATUS_LIST["STARTUP_COOLING"]:
                break
            self._testlib.wait_time(1)
            tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status != TDM_STATUS_LIST["STARTUP_COOLING"]:
            self._testlib._report.add_comment_row("TDM_STATUS 24 not reached.",
                                                  background_color="WARNING", print_on_console=True)
            return False

        timer_startup = self._testlib.read_dgto("TIMER1SEC_STARTUP")
        for i in range(HEAT_COOLING_TIMER):
            if timer_startup <= 177:
                break
            self._testlib.wait_time(1)
            timer_startup = self._testlib.read_dgto("TIMER1SEC_STARTUP")

        if timer_startup > 177:
            self._testlib._report.add_comment_row("TDM blocked in status 24, TIMER1SEC_STARTUP doesn't start.",
                                                  background_color="WARNING", print_on_console=True)
            return False

        self._testlib.write_dgto("TIMER1SEC_STARTUP", 0, 1)

        for i in range(HEAT_COOLING_TIMER):
            if tdm_status == status:
                break
            self._testlib.wait_time(1)
            tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status != status:
            self._testlib._report.add_comment_row(f"TDM_STATUS {status} not reached.",
                                                  background_color="WARNING", print_on_console=True)
            return False

        return True


    def get_pressure_sensor_presence(self) -> bool:
        """
            Function to understand if the current inverter has pressure sensor

            The P_DISCHARGE and P_SUCTION sensor could be only virtual on some Inverter

            :return: False if there is no pressure sensor, True if P_SUCTION and P_DISCHARGE sensor are present.
        """

        if self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON or self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING or \
                self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            return True

        return False


    def get_CMP_Target(self):
        """
            Function to read the CMP freq Target

            The CMP Target DGTO could change in base of the Inverter connected

            :return: the CMP freq Target value
        """
        result = None

        if self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            result = self._testlib.read_dgto("CMP_FREQ_SP_WR")
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON or self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING or \
                self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            result = self._testlib.read_dgto("CMP_FREQ_SP_WR") / 60

        return result


    def check_CMP_ON(self):
        """
            Function to check if the Compressor is active

            :return: "True" if the CMP is ON, otherwise "False"
        """
        inverter_selector = self._testlib.read_dgto("INVERTER_SELECTOR")
        compressor_status_2 = self._testlib.read_dgto("CMP_DRIVE_STATUS_INFO_EK_RD")
        compressor_status_1 = self._testlib.read_dgto("LOAD_STATUS_REAL_RD")
        compressor_status_3 = self._testlib.read_dgto("TDM_HHP_INV_DRIVE_STATUS")

        if (compressor_status_2 & 16) == 16 and inverter_selector == 2 or (
                compressor_status_3 & 16) == 16 and inverter_selector == 3 or (
                compressor_status_1 & 1) == 1 and inverter_selector == 1:
            return True
        else:
            return False


    def get_FAN_Target(self):
        """
            Function to read the Fan 1 rpm Target

            The Fan 1 Target DGTO could change in base of the Inverter connected

            :return: the RPM value of the Fan 1 Target
        """
        result = dgto = None

        fan_cfg = self.read_dgto("FAN_CONFIG")

        if fan_cfg & 0x0F == 1:
            dgto = "FAN_ISO_SPEED_SP_WR"
        elif fan_cfg & 0x0F == 2:
            dgto = "FAN1_SPEED_SP_WR"
        elif fan_cfg & 0x0F == 4:
            dgto = "FAN2_SPEED_SP_WR"
        else:
            dgto = "FAN_1_SPEED_SP_LOGICAL"

        if dgto is not None:
            result = self.read_dgto(dgto)

        return result


    def get_FAN_2_Target(self):
        """
            Function to read the Fan 2 rpm Target

            The Fan 2 Target DGTO could change in base of the Inverter connected

            :return: the RPM value of the Fan 2 Target
        """
        result = dgto = None

        fan_cfg = self.read_dgto("FAN_CONFIG")

        if fan_cfg & 0xF0 == 0x10:
            dgto = "FAN_ISO_SPEED_SP_WR"
        elif fan_cfg & 0xF0 == 0x20:
            dgto = "FAN1_SPEED_SP_WR"
        elif fan_cfg & 0xF0 == 0x40:
            dgto = "FAN2_SPEED_SP_WR"
        else:
            dgto = "FAN_2_SPEED_SP_LOGICAL"

        if dgto is not None:
            result = self.read_dgto(dgto)

        return result


    def get_FAN_Speed(self):
        """
            Function to read the Fan 1 rpm feedback value

            The Fan 1 Feedback DGTO could change in base of the Inverter connected

            :return: the RPM value of the Fan 1 Speed feedback
        """

        result = dgto = None

        fan_cfg = self.read_dgto("FAN_CONFIG")

        if fan_cfg & 0x0F == 1:
            dgto = "FAN_ISO_SPEED_SP"
        elif fan_cfg & 0x0F == 2:
            dgto = "FAN1_SPEED_REAL_RD"
        elif fan_cfg & 0x0F == 4:
            dgto = "FAN2_SPEED_REAL_RD"
        else:
            dgto = "FAN 1 Speed Real"

        if dgto is not None:
            result = self.read_dgto(dgto)

        return result


    def get_FAN_2_Speed(self):
        """
            Function to read the Fan 2 rpm feedback value

            The Fan 2 Feedback DGTO could change in base of the Inverter connected

            :return: the RPM value of the Fan 2 Speed feedback
        """

        result = dgto = None

        fan_cfg = self.read_dgto("FAN_CONFIG")

        if fan_cfg & 0xF0 == 0x10:
            dgto = "FAN_ISO_SPEED_SP"
        elif fan_cfg & 0xF0 == 0x20:
            dgto = "FAN1_SPEED_REAL_RD"
        elif fan_cfg & 0xF0 == 0x40:
            dgto = "FAN2_SPEED_REAL_RD"
        else:
            dgto = "FAN 2 Speed Real"

        if dgto is not None:
            result = self.read_dgto(dgto)

        return result


    def set_exv_init_heating_state(self, status: int, target: int = HEATING_DEFAULT_SETPOINT) -> bool:
        """
            Bring the TDM to the selected Status 13

            :param status: The final status to reach after status 13
            :param target: The target temperature to set (in Heating)

            :return: "True" if the TDM goes correctly through all phases before the selected state, otherwise "False"
        """
        heat_cool_timeout = 120
        command = calculate_cmd_from_status(status)
        self._testlib._report.add_comment_row(f"Procedure to set TDM on EXV Init State in Heating started.",
                                              print_on_console=True)
        self._testlib.write_dgto("TIMER1SEC_CMP_TIMEGUARD", 0, 1)
        self._testlib.write_dgto("TIMER1SEC_CMP_ANTICYCLING_TIMEGUARD", 0, 1)
        self._testlib.write_dgto("START_TD_TIME_PARAM", 0, 1)
        self._testlib.write_dgto("START_TEMP_LWT_MAX", 820, 1)
        self._testlib.write_dgto("WATER_DT_START_TIME_MAX", 200, 1)
        self._testlib.write_dgto("WATER_DT_TIME_INITIAL", 5, 1)
        self._testlib.write_dgto("WATER_DT_THRESHOLD_TIME_MAX", 5, 1)
        self._testlib.write_dgto("HP Water Flow Temp (LWT)", target - 90, 1)
        self._testlib.write_dgto("HP Water Return Temp (EWT)", target - 100, 1)
        self.write_dgto("EM HP Refrigerant Temp", 200, 3)
        self.write_dgto("HP Evaporator Temp (OCT)", 170, 3)
        self._testlib.write_dgto("HP EXTERNAL Set Point", target, 1)
        self.set_generator_external_request(command, 0, 0)

        # Set control mode of exv in slow ramp to avoid the fast exit from the state 13
        self.set_Exv1Position_ControlMode(4)

        tdm_status = self._testlib.read_dgto("TDM - Status")

        for i in range(heat_cool_timeout):
            if tdm_status == TDM_STATUS_LIST["EXV_INIT_HEATING"]:
                break
            self._testlib.wait_time(1)
            tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status != TDM_STATUS_LIST["EXV_INIT_HEATING"]:
            self._testlib._report.add_comment_row(f"TDM_STATUS 13 not reached.",
                                                  background_color="WARNING", print_on_console=True)
            return False

        return True


    def set_exv_init_cooling_state(self, status: int, target: int = COOLING_DEFAULT_SETPOINT) -> bool:
        """
            Bring the TDM to the selected Status 23

            :param status: The final status to reach after status 23
            :param target: The target temperature to set (in Cooling)

            :return: "True" if the TDM goes correctly through all phases before the selected state, otherwise "False"
        """

        heat_cool_timeout = 120
        command = calculate_cmd_from_status(status)
        self._testlib._report.add_comment_row(f"Procedure to set TDM on EXV Init State in Cooling started.",
                                              print_on_console=True)
        self._testlib.write_dgto("TIMER1SEC_CMP_ANTICYCLING_TIMEGUARD", 0, 1)
        self._testlib.write_dgto("TIMER1SEC_CMP_TIMEGUARD", 0, 1)
        self._testlib.write_dgto("START_TD_TIME_PARAM", 0, 1)
        self._testlib.write_dgto("START_TEMP_LWT_MIN", 50, 1)
        self._testlib.write_dgto("WATER_DT_START_TIME_MAX", 200, 1)
        self._testlib.write_dgto("WATER_DT_TIME_INITIAL", 5, 1)
        self._testlib.write_dgto("WATER_DT_THRESHOLD_TIME_MAX", 5, 1)
        self._testlib.write_dgto("HP Water Flow Temp (LWT)", target + 160, 1)
        self._testlib.write_dgto("HP Water Return Temp (EWT)", target + 170, 1)
        self.write_dgto("EM HP Refrigerant Temp", 170, 3)
        self.write_dgto("HP Evaporator Temp (OCT)", 200, 3)
        self._testlib.write_dgto("HP EXTERNAL Set Point", target, 1)
        self.set_generator_external_request(command, 0, 1)

        # Set control mode of exv in slow ramp to avoid the fast exit from the state 13
        self.set_Exv1Position_ControlMode(4)

        tdm_status = self._testlib.read_dgto("TDM - Status")

        for i in range(heat_cool_timeout):
            if tdm_status == TDM_STATUS_LIST["EXV_INIT_COOLING"]:
                break
            self._testlib.wait_time(1)
            tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status != TDM_STATUS_LIST["EXV_INIT_COOLING"]:
            self._testlib._report.add_comment_row(f"TDM_STATUS 23 not reached.",
                                                  background_color="WARNING", print_on_console=True)
            return False

        return True


    def set_defrost_basic_conditions(self) -> bool:
        """
            Check if defrost basic condition preconditions are true and then set the defrost basic condition ON

                This function will set:
                 - "HP Water Return Temp (EWT)" = 15°C
                 - "HP Water Flow Temp (LWT)" = 35,5°C
                 - "EM HP Evaporator AUX" = -2°C
                 - "HP Evaporator Temp (OCT)" = "TE_DEFROST_EXIT_LO" - 1°C

            :return: "True" if defrost basic condition are correctly settled, otherwise "False"
        """

        probe_ewt = 150
        probe_lwt = 355
        activation_timeout = 10  # Cannot be 0
        self._testlib.write_dgto("DEFROST_TIMER_MIN_SEC", 1)
        self._testlib.write_dgto("DEFROST_ACTIVATION_REQUEST_TIMEOUT", activation_timeout)
        self._testlib.write_dgto("HP Water Return Temp (EWT)", probe_ewt, 1)
        self._testlib.write_dgto("HP Water Flow Temp (LWT)", probe_lwt, 1)

        # Check if V4W is in Heating Mode
        load_status_real_rd = self._testlib.read_dgto("LOAD_STATUS_REAL_RD")
        is_v4w_heating_mode = (load_status_real_rd & 64) == 0

        # Check if compressor is ON
        is_cmp_on = self.check_CMP_ON()

        # Check if TDM_Status != 18 and 40
        tdm_status = self._testlib.read_dgto("TDM - Status")

        if is_v4w_heating_mode is True and is_cmp_on is True and tdm_status != TDM_STATUS_LIST[
            "DEFROST_AUTOMATIC"] and tdm_status != TDM_STATUS_LIST["DEFROST_MANUAL"]:
            # Set SST <= 0:
            def_exit_low = self._testlib.read_dgto("TE_DEFROST_EXIT_LO") / 10
            self._testlib.write_dgto("PSUCT_SOURCE", 0, 2)  # SST Virtual
            self.set_EM_HP_Evaporator_AUX(-14, False)  # SST = -20
            self.set_HP_Evaporator_Temp_OCT(-12, False)  # Defrost Reset CND = False
            self.set_HP_Outdoor_Temp_OAT(-7, False)
            self.set_Discharge_Temp_TD(37, False)
            self.set_Suction_Temp(-18, False)
            self.save_InverterValue()
        else:
            self._testlib._report.add_comment_row(
                    f"Defrost Basic Condition cannot be setted:\nis_v4w_heating_mode = {is_v4w_heating_mode}, is_cmp_on = {is_cmp_on}, tdm_status = {tdm_status}",
                    background_color="WARNING", print_on_console=True)
            return False

        '''
        if not self._testlib.ping_dgto("15-13-3-16", -20, 1, PING_DEFAULT_TIMER):
            self._testlib._report.add_comment_row(
                    "Defrost Basic Condition cannot be setted:\nProblem during the setting of SST",
                    background_color="WARNING", print_on_console=True)
            return False
        '''
        self._testlib.wait_time(10)
        if not self._testlib.read_dgto("15-13-3-16") <= 0:
            self._testlib._report.add_comment_row(
                    "Defrost Basic Condition cannot be setted:\nProblem during the setting of SST",
                    background_color="WARNING", print_on_console=True)
            return False

        counter_defrost_old = self._testlib.read_dgto("COUNTER1SEC_DEFROST")

        for i in range(30):
            self._testlib.wait_time(1)
            counter_defrost = self._testlib.read_dgto("COUNTER1SEC_DEFROST")
            if counter_defrost > counter_defrost_old:
                return True

        return False


    def set_MANUALDEFROST_ENABLE_ON(self, set_basic_condition: bool = True) -> bool:
        """
            Set DEFROST_ENABLE = 1 to start ManualDefrost routine, defrost basic conditions is requested to start the routine

                This function will change the value of:
                 - "HP Water Flow Temp (LWT)"
                 - "HP Power Calculation"

            :param set_basic_condition: if True this function will automatically set the defrost basic conditions

            :return: "True" if DEFROST_ENABLE is successfully set to 1, otherwise "False"
        """
        if set_basic_condition:
            if not self.set_defrost_basic_conditions():
                self._testlib._report.add_comment_row(
                        "DEFROST_ENABLE = 1 cannot be setted without Defrost Basic Condition on.",
                        background_color="WARNING", print_on_console=True)
                return False

        self._testlib.write_dgto("EM Defrost Manual ON Cmd", 30)
        self._testlib.wait_time(3)

        self._testlib._report.add_comment_row(
                f"Waiting for DEFROST_ENABLE = 1 or TDM_STATUS = 40.", print_on_console=True)
        defrost_enable = self._testlib.read_dgto("DEFROST_ENABLE", True)
        tdm_status = self._testlib.read_dgto("TDM - Status", True)

        for i in range(30):
            if defrost_enable == 1 or tdm_status == TDM_STATUS_LIST["DEFROST_MANUAL"]:
                break
            self.wait_time(1)
            defrost_enable = self._testlib.read_dgto("DEFROST_ENABLE", True)

        return defrost_enable == 1 or tdm_status == TDM_STATUS_LIST["DEFROST_MANUAL"]


    def set_DEFROST_ENABLE_ON(self, set_basic_condition: bool = True) -> bool:
        """
            Set DEFROST_ENABLE = 1 to start Defrost routine, defrost basic conditions is requested to start the routine

                This function will change the value of:
                 - "HP Water Flow Temp (LWT)"
                 - "HP Power Calculation"

            :param set_basic_condition: if True this function will automatically set the defrost basic conditions

            :return: "True" if DEFROST_ENABLE is successfully set to 1, otherwise "False"
        """
        if set_basic_condition:
            if not self.set_defrost_basic_conditions():
                self._testlib._report.add_comment_row(
                        "DEFROST_ENABLE = 1 cannot be setted without Defrost Basic Condition on.",
                        background_color="WARNING", print_on_console=True)
                return False

        probe_ewt = self._testlib.read_dgto("HP Water Return Temp (EWT)")
        probe_lwt = self._testlib.read_dgto("HP Water Flow Temp (LWT)")
        activation_timeout = self._testlib.read_dgto("DEFROST_TIMER_MIN_SEC")

        self._testlib.wait_time(1)

        cop_i_old = self._testlib.read_dgto("COP_I_CMP_9_7")
        cop_cd_old = self._testlib.read_dgto("COP_CD_9_7")

        probe_lwt = probe_lwt - 10  # 1°C less

        self._testlib.write_dgto("HP Water Flow Temp (LWT)", probe_lwt, 1)

        self._testlib.wait_time(10)

        cop_i = self._testlib.read_dgto("COP_I_CMP_9_7")
        cop_cd = self._testlib.read_dgto("COP_CD_9_7")

        if (cop_cd == cop_cd_old) or (cop_i == cop_i_old):
            self._testlib._report.add_comment_row(
                    f"COP_CD = {cop_cd} or COP_I = {cop_i} not calculated.",
                    background_color="WARNING", print_on_console=True)
            self._testlib.read_dgto_until("Fault_Code", "==", 65535)
            self._testlib.read_dgto("Fault_Code")
            return False

        while cop_i > cop_cd:
            probe_lwt = probe_lwt - 5
            if probe_lwt > probe_ewt:
                self._testlib.write_dgto("HP Water Flow Temp (LWT)", probe_lwt, 1)
            else:
                if cop_cd < 0:
                    self._testlib._report.add_comment_row(
                            "COP_CD is too low, Defrost cannot start, please set LWT > EWT, "
                            "send an Heating Request and wait untill COP_CD > 0\n"
                            "otherwise reprogram the TDM to erase the COP_CD memory",
                            background_color="WARNING", print_on_console=True)
                    return False
                if tdm_status != 15 or tdm_status != 16 or tdm_status != 17 or tdm_status != 18:
                    fault_code = self._testlib.read_dgto("Fault_Code", True)
                    self._testlib._report.add_comment_row(
                        f"TDM_STATUS: {tdm_status}, impossible to enter in defrost from this state.\nFault_Code: {fault_code}",
                        background_color="WARNING", print_on_console=True)
                    return False
                self._testlib.wait_time(3)

            hp_power_calculation = self._testlib.read_dgto("HP Power Calculation")

            if hp_power_calculation < MAX_HP_POWER_CALC:
                new_hp_power_calculation = hp_power_calculation + 125
                self.set_DriveStatus_InputPower(new_hp_power_calculation)  # Set Input Drive for compressor
            else:
                self._testlib.wait_time(3)

            tdm_status = self._testlib.read_dgto("TDM - Status", True)

            cop_i = self._testlib.read_dgto("COP_I_CMP_9_7")
            cop_cd = self._testlib.read_dgto("COP_CD_9_7")

        self._testlib.read_dgto("Fault_Code")
        return self._testlib.ping_dgto("DEFROST_ENABLE", 1, 1, 15)


    def set_generator_external_request(self, external_request: int, modulation_mode: int, hr_mode: int) -> bool:
        """
            Set the Generator Request (simulation of EM command)

            :param external_request: the external request to set:

            	0 = Off_protection (the System Manager tells to the TDM4 to switch off immediately for a dangerous situation in the system)
                1 = Off_hard *NOT USED* (the System Manager tells to the TDM4 to switch off immediately, but the TDM4 can complete the protection algorithms)
                2 = Off_soft (with this command the TDM4 continues to work until the TDM4 decides to switch off)
                3 = Modulation Heating
                4 = Rating Heating
                5 = Booster Heating
                6 = Modulation Cooling
                7 = Rating Cooling
                8 = Booster Cooling
                9 = Soft Lockout *NOT USED* (the TDM4 switches off the heaters and carry on the defrost if it is running)
                10 = Hard Lockout *NOT USED* (the TDM4 disables all the Inverter Fault)

            :param modulation_mode: used to set the modulation modality to deliver thermal power:

                0 = Temperature mode (the TDM4 generator target is the LWT)
                1 = Thermal Power percentage mode (the TDM4 generator target is the thermal power expressed in percentage 0-100%)
                2 = Thermal Power (the TDM4 generator target is the thermal power expressed in Watts)
                3 = Free mode control (the TDM4 can decides by itself the most efficient way to modulate with a specific target, assuring the maximum efficiency)


            :param hr_mode: used to select the heat request mode:

            0 = heating,
            1 = cooling.

            :return: "True" if the DGTO "Generator External Request" is correctly set, otherwise False
        """
        modulation_mode_bitmap = modulation_mode << 8
        hr_mode_bitmap = hr_mode << 15
        generator_external_request = external_request | modulation_mode_bitmap | hr_mode_bitmap
        if self._testlib.write_dgto("Generator External Request", generator_external_request, 1):
            return True
        else:
            return False

    def set_hr_mode_only(self, hr_mode: int) -> bool:
        """
            Set HR Mode in Generator Request (simulation of EM command)

            :param hr_mode: used to select the heat request mode:

            0 = heating,
            1 = cooling.

            :return: "True" if the DGTO "Generator External Request" is correctly set, otherwise False
        """
        bitmap = self._testlib.read_dgto("Generator External Request")
        bitmap = bitmap & 0x7FFF
        hr_mode_bitmap = hr_mode << 15
        generator_external_request = bitmap | hr_mode_bitmap
        if self._testlib.write_dgto("Generator External Request", generator_external_request, 1):
            return True
        else:
            return False


    def get_external_request(self) -> int:
        """
            Get the current external request setting

            :return: the value of the current external request:
                0 = Off_protection (the System Manager tells to the TDM4 to switch off immediately for a dangerous situation in the system)
                1 = Off_hard *NOT USED* (the System Manager tells to the TDM4 to switch off immediately, but the TDM4 can complete the protection algorithms)
                2 = Off_soft (with this command the TDM4 continues to work until the TDM4 decides to switch off)
                3 = Modulation Heating
                4 = Rating Heating
                5 = Booster Heating
                6 = Modulation Cooling
                7 = Rating Cooling
                8 = Booster Cooling
                9 = Soft Lockout *NOT USED* (the TDM4 switches off the heaters and carry on the defrost if it is running)
                10 = Hard Lockout *NOT USED* (the TDM4 disables all the Inverter Fault)
        """
        generator_external_request = self._testlib.read_dgto("Generator External Request")
        bitmask = 31  # in hex: 0x001F
        external_request = generator_external_request & bitmask
        return external_request


    def get_modulation_mode(self) -> int:
        """
            Get the current modulation mode setting

            :return: the value of the modulation mode active:
                0 = Temperature mode (the TDM4 generator target is the LWT)
                1 = Thermal Power percentage mode (the TDM4 generator target is the thermal power expressed in percentage 0-100%)
                2 = Thermal Power (the TDM4 generator target is the thermal power expressed in Watts)
                3 = Free mode control (the TDM4 can decides by itself the most efficient way to modulate with a specific target, assuring the maximum efficiency)
        """
        generator_external_request = self._testlib.read_dgto("Generator External Request")
        bitmask = 15 << 8  # in hex: 0x000F -> 0x0F00
        modulation_mode = (generator_external_request & bitmask) >> 8
        return modulation_mode


    def get_hr_mode(self) -> int:
        """
            Get the current heat request mode

            :return: the value of the heat request mode active:
                0 = Heating
                1 = Cooling
        """
        generator_external_request = self._testlib.read_dgto("Generator External Request")
        bitmask = 1 << 15  # in hex: 0x0001 -> 0x8000
        hr_mode = (generator_external_request & bitmask) >> 15
        return hr_mode


    def get_generator_status(self) -> int:
        """
            Get the generator status value

            :return: the value of the current generator status:
                0 = initialization
                1 = Stanby
                2 = Permanent not available (Hardstop/Fault/Hardfault)
                3 = Temporary not available (LWT under or over threshold / Timerguard / ecc.)
                4 = Heating active
                5 = Cooling active
                6 = Heating active without external request (for instance Antifrost protection)
                7 = Cooling active without external request
                8 = Heating active without external request (for instance Manual Defrost)
                9 = Cooling active without external request (for instance Pump Down)
                32 = Reserved state (The TDM4 will use this state only for special mode like DEBUG MODE, PC CONTROL or SETUP MODE during the writing of DFLS)

        """
        hp_generator_state = self._testlib.read_dgto("HP Generator State")
        bitmask = 63  # in hex: 0x003F
        generator_status = hp_generator_state & bitmask
        return generator_status


    def get_active_compressor_control_mode(self) -> int:
        """
            Get the compressor control mode in use

            :return: the value of the compressor control mode active:
                0 = Temperature mode (the TDM4 generator target is the LWT)
                1 = Thermal Power percentage mode (the TDM4 generator target is the thermal power expressed in percentage 0-100%)
                2 = Thermal Power (the TDM4 generator target is the thermal power expressed in Watts)
                3 = Free mode control (the TDM4 can decides by itself the most efficient way to modulate with a specific target, assuring the maximum efficiency)
        """
        hp_generator_state = self._testlib.read_dgto("HP Generator State")
        bitmask = 15 << 8  # in hex: 0x000F -> 0x0F00
        active_compressor_control_mode = (hp_generator_state & bitmask) >> 8
        return active_compressor_control_mode


    def set_lab_mode_algorithm_state(self, algorithm: int, state: bool):
        """
            Set a specific algorithm state ON/OFF

            :param state: the state4 to set, ON = True, OFF = False
            :param algorithm:

            :return: "True" the function is performed correctly, otherwise "False"
        """
        valid_algo = False

        for alg in LAB_MODE.ALGORITHMS:
            if alg == algorithm:
                valid_algo = True
                break

        if not valid_algo:
            self._testlib._report.add_comment_row(
                    f"WARNING: Wrong algorithm passed {algorithm}.",
                    background_color="WARNING", print_on_console=True)
            return False

        r = self.set_lab_mode_active()

        if not r:
            self._testlib._report.add_comment_row(
                    "Impossible to set a lab mode algorithm state if lab mode is not enabled.",
                    background_color="WARNING", print_on_console=True)
            return False

        if state:
            self._testlib.write_dgto("LAB_MODE_ALGORITHMS_STATE", 0 & algorithm)
        else:
            self._testlib.write_dgto("LAB_MODE_ALGORITHMS_STATE", 0xFFFF & algorithm)

        return True


    def set_lab_mode_active(self) -> bool:
        """
            Method to activate Laboratory Mode

            :return: "True" if LabMode is enabled
                        "False" if LabMode is not enabled
        """
        if self._testlib.read_dgto("LAB_MODE_ENABLE_STATE") == 4:
            return True

        # Preconditions: Lab_Mode_Enable = 1
        self._testlib.write_dgto("LAB_MODE_ENABLE_KEY1", 65535, 1)
        self._testlib.write_dgto("LAB_MODE_ENABLE_KEY2", 65535, 1)

        if not self._testlib.ping_dgto("LAB_MODE_ENABLE_STATE", 1, 1, 10):
            self._testlib._report.add_comment_row("Lab Mode is not enabled. Check the functionality",
                                                  background_color="WARNING", print_on_console=True)
            return False

        # First step: write key1 and key2 to 0 -> Lab_Mode_Enable = 2
        self._testlib.write_dgto("LAB_MODE_ENABLE_KEY1", 0, 1)
        self._testlib.write_dgto("LAB_MODE_ENABLE_KEY2", 0, 1)

        if not self._testlib.ping_dgto("LAB_MODE_ENABLE_STATE", 2, 1, 10):
            self._testlib._report.add_comment_row("Lab Mode is not enabled. Check the functionality",
                                                  background_color="WARNING", print_on_console=True)
            return False

        # Second step: write key1 to 0x5555 and key2 to 0 -> Lab_Mode_Enable = 3
        self._testlib.write_dgto("LAB_MODE_ENABLE_KEY1", 21845, 1)
        self._testlib.write_dgto("LAB_MODE_ENABLE_KEY2", 0, 1)

        if not self._testlib.ping_dgto("LAB_MODE_ENABLE_STATE", 3, 1, 10):
            self._testlib._report.add_comment_row("Lab Mode is not enabled. Check the functionality",
                                                  background_color="WARNING", print_on_console=True)
            return False

        # Third step: write key1 to 0x5555 and key2 to 0xAAAA within 10 seconds -> Lab_Mode_Enable = 4
        self._testlib.write_dgto("LAB_MODE_ENABLE_KEY1", 21845, 1)
        self._testlib.write_dgto("LAB_MODE_ENABLE_KEY2", 43690, 1)

        if not self._testlib.ping_dgto("LAB_MODE_ENABLE_STATE", 4, 1, 10):
            self._testlib._report.add_comment_row("Lab Mode is not enabled. Check the functionality",
                                                  background_color="WARNING", print_on_console=True)
            return False

        return True


    def set_startup_heating_state(self, status: int, target: int = HEATING_DEFAULT_SETPOINT) -> bool:
        """
            Bring the TDM to the selected Status 14

            :param status: The final status to reach after status 14
            :param target: The target temperature to set (in Heating)

            :return: "True" if the TDM goes correctly through all phases before the selected state, otherwise "False"
        """

        command = calculate_cmd_from_status(status)
        self._testlib._report.add_comment_row(f"Procedure to set TDM on Startup State in Heating started.",
                                              print_on_console=True)
        self._testlib.write_dgto("TIMER1SEC_CMP_TIMEGUARD", 0, 1)
        self._testlib.write_dgto("TIMER1SEC_CMP_ANTICYCLING_TIMEGUARD", 0, 1)
        self._testlib.write_dgto("START_TD_TIME_PARAM", 0, 1)
        self._testlib.write_dgto("START_TEMP_LWT_MAX", 820, 1)
        self._testlib.write_dgto("WATER_DT_START_TIME_MAX", 200, 1)
        self._testlib.write_dgto("WATER_DT_TIME_INITIAL", 5, 1)
        self._testlib.write_dgto("WATER_DT_THRESHOLD_TIME_MAX", 5, 1)
        self._testlib.write_dgto("HP Water Flow Temp (LWT)", target - 100, 1)
        self._testlib.write_dgto("HP Water Return Temp (EWT)", target - 110, 1)
        self.write_dgto("EM HP Refrigerant Temp", 200, 7)
        self.write_dgto("HP Evaporator Temp (OCT)", 170, 7)
        self._testlib.write_dgto("HP EXTERNAL Set Point", target, 1)
        self.set_generator_external_request(command, 0, 0)

        tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status == TDM_STATUS_LIST["STARTUP_HEATING"]:
            self._testlib._report.add_comment_row(f"TDM_STATUS 14 was already active.",
                                                  background_color="WARNING", print_on_console=True)
            return True

        for i in range(HEAT_COOLING_TIMER):
            if tdm_status == TDM_STATUS_LIST["EXV_INIT_HEATING"] or tdm_status == TDM_STATUS_LIST["STARTUP_HEATING"]:
                break
            self._testlib.wait_time(1)
            tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status != TDM_STATUS_LIST["EXV_INIT_HEATING"] and tdm_status != TDM_STATUS_LIST["STARTUP_HEATING"]:
            self._testlib._report.add_comment_row("TDM_STATUS 13 not reached.",
                                                  background_color="WARNING", print_on_console=True)
            return False

        self.set_DriveStatus_InputPower(500, True, False)  # Set Input Drive for compressor

        tdm_status = self._testlib.read_dgto("TDM - Status")

        for i in range(HEAT_COOLING_TIMER):
            if tdm_status == TDM_STATUS_LIST["STARTUP_HEATING"]:
                break
            self._testlib.wait_time(1)
            tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status != TDM_STATUS_LIST["STARTUP_HEATING"]:
            self._testlib._report.add_comment_row(f"TDM_STATUS 14 not reached.",
                                                  background_color="WARNING", print_on_console=True)
            return False

        return True


    def set_startup_cooling_state(self, status: int, target: int = COOLING_DEFAULT_SETPOINT) -> bool:
        """
            Bring the TDM to the selected Status 24

            :param status: The final status to reach after status 24
            :param target: The target temperature to set (in Cooling)

            :return: "True" if the TDM goes correctly through all phases before the selected state, otherwise "False"
        """
        command = calculate_cmd_from_status(status)
        self._testlib._report.add_comment_row(f"Procedure to set TDM on Startup State in Cooling started.",
                                              print_on_console=True)
        self._testlib.write_dgto("TIMER1SEC_CMP_TIMEGUARD", 0, 1)
        self._testlib.write_dgto("TIMER1SEC_CMP_ANTICYCLING_TIMEGUARD", 0, 1)
        self._testlib.write_dgto("START_TD_TIME_PARAM", 0, 1)
        self._testlib.write_dgto("START_TEMP_LWT_MIN", 50, 1)
        self._testlib.write_dgto("WATER_DT_START_TIME_MAX", 200, 1)
        self._testlib.write_dgto("WATER_DT_TIME_INITIAL", 5, 1)
        self._testlib.write_dgto("WATER_DT_THRESHOLD_TIME_MAX", 5, 1)
        self._testlib.write_dgto("HP Water Flow Temp (LWT)", target + 160, 1)
        self._testlib.write_dgto("HP Water Return Temp (EWT)", target + 170, 1)
        self.write_dgto("EM HP Refrigerant Temp", 170, 3)
        self.write_dgto("HP Evaporator Temp (OCT)", 200, 3)
        self._testlib.write_dgto("HP EXTERNAL Set Point", target, 1)
        self.set_generator_external_request(command, 0, 1)

        tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status == TDM_STATUS_LIST["STARTUP_HEATING"]:
            self._testlib._report.add_comment_row(f"TDM_STATUS 24 was already active.",
                                                  background_color="WARNING", print_on_console=True)
            return True

        for i in range(HEAT_COOLING_TIMER):
            if tdm_status == TDM_STATUS_LIST["EXV_INIT_COOLING"] or tdm_status == TDM_STATUS_LIST["STARTUP_COOLING"]:
                break
            self._testlib.wait_time(1)
            tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status != TDM_STATUS_LIST["EXV_INIT_COOLING"] and tdm_status != TDM_STATUS_LIST["STARTUP_COOLING"]:
            self._testlib._report.add_comment_row("TDM_STATUS 23 not reached.",
                                                  background_color="WARNING", print_on_console=True)
            return False

        self.set_DriveStatus_InputPower(500, True, False)  # Set Input Drive for compressor

        tdm_status = self._testlib.read_dgto("TDM - Status")

        for i in range(HEAT_COOLING_TIMER):
            if tdm_status == TDM_STATUS_LIST["STARTUP_COOLING"]:
                break
            self._testlib.wait_time(1)
            tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status != TDM_STATUS_LIST["STARTUP_COOLING"]:
            self._testlib._report.add_comment_row(f"TDM_STATUS 24 not reached.",
                                                  background_color="WARNING", print_on_console=True)
            return False

        return True


    def set_waiting_activation_heating_state(self, status: int, target: int = HEATING_DEFAULT_SETPOINT) -> bool:
        """
            Bring the TDM to the selected Status 11: to do this, "Demand Integral Min" is set to 0.
            To exit from this state, write "Demand Integral Min" != 0

            :param status:
            :param target: The target temperature to set (in Heating)

            :return: "True" if the TDM goes correctly through all phases before the selected state, otherwise "False"
        """
        command = calculate_cmd_from_status(status)

        self._testlib._report.add_comment_row(f"Procedure to set TDM on Waiting Activation State in Heating started.",
                                              print_on_console=True)
        self._testlib.write_dgto("Demand Integral Min", 0, 1)
        self._testlib.write_dgto("START_TEMP_LWT_MAX", 820, 1)
        self._testlib.write_dgto("TIMER1SEC_CMP_TIMEGUARD", 0, 1)
        self._testlib.write_dgto("TIMER1SEC_CMP_ANTICYCLING_TIMEGUARD", 0, 1)
        self._testlib.write_dgto("START_TD_TIME_PARAM", 0, 1)
        self._testlib.write_dgto("START_TEMP_LWT_MAX", 0, 1)
        self._testlib.write_dgto("WATER_DT_START_TIME_MAX", 200, 1)
        self._testlib.write_dgto("WATER_DT_TIME_INITIAL", 5, 1)
        self._testlib.write_dgto("WATER_DT_THRESHOLD_TIME_MAX", 0, 1)
        self._testlib.write_dgto("HP Water Flow Temp (LWT)", target - 90, 1)
        self._testlib.write_dgto("HP Water Return Temp (EWT)", target - 100, 1)
        self.write_dgto("EM HP Refrigerant Temp", 200, 3)
        self.write_dgto("HP Evaporator Temp (OCT)", 170, 3)
        self._testlib.write_dgto("HP EXTERNAL Set Point", target, 1)
        self.set_generator_external_request(command, 0, 0)

        tdm_status = self._testlib.read_dgto("TDM - Status")

        for i in range(HEAT_COOLING_TIMER):
            if tdm_status == TDM_STATUS_LIST["WAITING_ACTIVATION_HEATING"]:
                break
            self._testlib.wait_time(1)
            tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status != TDM_STATUS_LIST["WAITING_ACTIVATION_HEATING"]:
            self._testlib._report.add_comment_row("TDM_STATUS 11 not reached.",
                                                  background_color="WARNING", print_on_console=True)
            return False

        return True


    def set_waiting_activation_cooling_state(self, status: int, target: int = COOLING_DEFAULT_SETPOINT) -> bool:
        """
            Bring the TDM to the selected Status 21: to do this, "Demand Integral Min" is set to 0.
            To exit from this state, write "Demand Integral Min" != 0

            :param status:
            :param target: The target temperature to set (in Cooling)

            :return: "True" if the TDM goes correctly through all phases before the selected state, otherwise "False"
        """
        command = calculate_cmd_from_status(status)

        self._testlib._report.add_comment_row(f"Procedure to set TDM on Waiting Activation State in Cooling started.",
                                              print_on_console=True)
        self._testlib.write_dgto("Demand Integral Min", 0, 1)
        self._testlib.write_dgto("START_TEMP_LWT_MAX", 820, 1)
        self._testlib.write_dgto("TIMER1SEC_CMP_TIMEGUARD", 0, 1)
        self._testlib.write_dgto("TIMER1SEC_CMP_ANTICYCLING_TIMEGUARD", 0, 1)
        self._testlib.write_dgto("START_TD_TIME_PARAM", 0, 1)
        self._testlib.write_dgto("START_TEMP_LWT_MIN", 820, 1)
        self._testlib.write_dgto("WATER_DT_START_TIME_MAX", 200, 1)
        self._testlib.write_dgto("WATER_DT_TIME_INITIAL", 5, 1)
        self._testlib.write_dgto("WATER_DT_THRESHOLD_TIME_MAX", 0, 1)
        self._testlib.write_dgto("HP Water Flow Temp (LWT)", target + 20, 1)
        self._testlib.write_dgto("HP Water Return Temp (EWT)", target + 30, 1)
        self.write_dgto("EM HP Refrigerant Temp", 170, 3)
        self.write_dgto("HP Evaporator Temp (OCT)", 200, 3)
        self._testlib.write_dgto("HP EXTERNAL Set Point", target, 1)
        self.set_generator_external_request(command, 0, 1)

        tdm_status = self._testlib.read_dgto("TDM - Status")

        for i in range(HEAT_COOLING_TIMER):
            if tdm_status == TDM_STATUS_LIST["WAITING_ACTIVATION_COOLING"]:
                break
            self._testlib.wait_time(1)
            tdm_status = self._testlib.read_dgto("TDM - Status")

        if tdm_status != TDM_STATUS_LIST["WAITING_ACTIVATION_COOLING"]:
            self._testlib._report.add_comment_row("TDM_STATUS 21 not reached.",
                                                  background_color="WARNING", print_on_console=True)
            return False

        return True


    def check_suct_press_sensor_available(self) -> bool:
        """
            Check if the suction pressure sensor is available or not

            :return: bool value:
                False = Suction pressure sensor is not available
                True = Suction pressure sensor is available
        """
        ctrl_board_reg_sens_enable = self._testlib.read_dgto("CONTROL_BOARD_REG_WR_SENS_ENABLE")
        if self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            result = ctrl_board_reg_sens_enable & 0x0020
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON or self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING  or \
                self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            result = ctrl_board_reg_sens_enable & 0x0040
        if result == 0:
            return False
        else:
            return True


    def check_disch_press_sensor_available(self) -> bool:
        """
            Check if the discharge pressure sensor is available or not

            :return: bool value:
                False = Suction pressure sensor is not available
                True = Suction pressure sensor is available
        """
        ctrl_board_reg_sens_enable = self._testlib.read_dgto("CONTROL_BOARD_REG_WR_SENS_ENABLE")
        if self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            result = ctrl_board_reg_sens_enable & 0x0040
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON or self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING or \
                self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            result = ctrl_board_reg_sens_enable & 0x0080
        if result == 0:
            return False
        else:
            return True




    """
                                ----------------------------
                                --   Inverter functions   --
                                ----------------------------

                            Based on Inverter_APIs.py Ver. 1.7.0
    """


    def save_InverterValue(self):
        """
            Used to save all the inverter values previously settled with func Inverter_APIs.set_parameter()

            :return: None
        """
        Inverter_APIs.save_parameters()
        self._testlib.wait_time(1)


    def set_HP_Evaporator_Temp_OCT(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                                   check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto "HP Evaporator Temp (OCT)" (1-0-3-25) CoilTemperature

        :param save_value: If true the value will be saved on Inverter.
        :param value: The value to set.
        :param check_value: If True the value will be checked on dgto.

        :return: "True" if the dgto is set at the requested value and check_value = True or if check_value = False,
            "False" if if the dgto is not set at the requested value and check_value = True
        """
        if self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING or self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOTemperatures]", "CoilTemperatureValue_DBL", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            Inverter_APIs.set_parameter("[PacmanHpChatter.TDMTemperatures]", "CoilTemperatureValue_DBL",
                                        value * self._modifier)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOTemperatures]", "CoilTemperatureValue_DBL", value)

        if save_value:
            Inverter_APIs.save_parameters()
            if check_value:
                self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                ris = self._testlib.read_dgto("1-0-3-25")

                if value * 10 != ris:
                    return False

        return True


    def set_Discharge_Temp_TD(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                              check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto "TD_RD" (10-1-2-26)

        :param save_value: If true the value will be saved on Inverter.
        :param value: The value to set.
        :param check_value: If True the value will be checked on dgto.

        :return: "True" if the dgto is set at the requested value and check_value = True or if check_value = False,
            "False" if if the dgto is not set at the requested value and check_value = True
        """
        if self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING or self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOTemperatures]", "DischargeTemperatureValue_DBL", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            Inverter_APIs.set_parameter("[PacmanHpChatter.TDMTemperatures]", "DischargeTemperatureValue_DBL",
                                        value * self._modifier)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOTemperatures]", "DischargeTemperatureValue_DBL", value)

        if save_value:
            Inverter_APIs.save_parameters()
            if check_value:
                self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                ris = self._testlib.read_dgto("10-1-2-26")

                if (value * 10) + 550 != ris:
                    return False
        return True


    def set_Suction_Temp(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                         check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto "TS_RD" (10-1-2-25)

        :param save_value: If true the value will be saved on Inverter.
        :param value: The value to set.
        :param check_value: If True the value will be checked on dgto.

        :return: "True" if the dgto is set at the requested value and check_value = True or if check_value = False,
            "False" if if the dgto is not set at the requested value and check_value = True
        """
        if self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING or self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON \
                or self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOTemperatures]", "SuctionTemperatureValue_DBL", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            Inverter_APIs.set_parameter("[PacmanHpChatter.TDMTemperatures]", "SuctionTemperatureValue", value * 10)

        if save_value:
            Inverter_APIs.save_parameters()
            if check_value:
                self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                ris = self._testlib.read_dgto("10-1-2-25")

                if (value + 55) * 10 != ris:
                    return False
        return True


    def set_Discharge_Pressure(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                               check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto "CONTROL_BOARD_REG_RD_PD" (15-7-3-20)

        :param save_value: If true the value will be saved on Inverter.
        :param value: The value to set.
        :param check_value: If True the value will be checked on dgto.

        :return: "True" if the dgto is set at the requested value and check_value = True or if check_value = False,
            "False" if if the dgto is not set at the requested value and check_value = True
        """
        if self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING or self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON \
                or self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOTemperatures]", "DischargePressureValue_DBL", value)

        if save_value:
            Inverter_APIs.save_parameters()
            if check_value:
                self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                ris = self._testlib.read_dgto("15-7-3-20")

                if value != ris:
                    return False
        return True


    def set_DriveStatus_InputPower(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                                   check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto "CMP_ELECTRICAL_PWR_W"

        :param save_value: If true the value will be saved on Inverter.
        :param value: The value to set.
        :param check_value: If True the value will be checked on dgto.

        :return: "True" if the dgto is set at the requested value and check_value = True or if check_value = False,
            "False" if if the dgto is not set at the requested value and check_value = True
        """

        if self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING or self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            Inverter_APIs.set_parameter("[PacmanHpChatter.INVDriveStatus]", "DriveStatusInputPower_DBL", value * 4)
            if save_value:
                Inverter_APIs.save_parameters()

        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON:
            Inverter_APIs.set_parameter("[PacmanHpChatter.POWPower]", "InputPower_DBL", value * 4)
            if save_value:
                Inverter_APIs.save_parameters()

        elif self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            Inverter_APIs.set_parameter("[PacmanHpChatter.TDMDiagnostic]", "SystemAcInputPower_DBL", value)
            if save_value:
                Inverter_APIs.save_parameters()

        if check_value:
            self._testlib.wait_time(DEFAULT_CHECK_TIMER)
            ris = self._testlib.read_dgto("CMP_ELECTRICAL_PWR_W")
            if value != ris:
                return False

        return True


    def set_DriveStatus_InputCurrent(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                                     check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto "INVERTER_INPUT_CURRENT" (10-9-2-7)

        :param save_value: If true the value will be saved on Inverter.
        :param value: The value to set.
        :param check_value: If True the value will be checked on dgto.

        :return: "True" if the dgto is set at the requested value and check_value = True or if check_value = False,
            "False" if if the dgto is not set at the requested value and check_value = True
        """

        if self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING or self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            Inverter_APIs.set_parameter("[PacmanHpChatter.INVDriveStatus]", "DriveStatusACInputCurr_DBL", value * 256)

            if save_value:
                Inverter_APIs.save_parameters()

                if check_value:
                    self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                    ris = (self._testlib.read_dgto("10-9-2-7") / 256)
                    if value != ris:
                        return False
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON:
            Inverter_APIs.set_parameter("[PacmanHpChatter.POWPower]", "AcInputCurrent_DBL", value * 100)

            if save_value:
                Inverter_APIs.save_parameters()

                if check_value:
                    self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                    ris = (self._testlib.read_dgto("10-9-2-7") / 256)
                    if value != ris:
                        return False
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            Inverter_APIs.set_parameter("[PacmanHpChatter.TDMDiagnostic]", "SystemAcInputCurrent_DBL", value * 10)

            if save_value:
                Inverter_APIs.save_parameters()

                if check_value:
                    self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                    ris = (self._testlib.read_dgto("10-9-2-7") / 256)

                    if value != ris:
                        return False

        return True


    def set_EM_HP_Evaporator_AUX(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                                 check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto "EM HP Evaporator AUX" (1-7-3-20) CoilOutletTemperature

        :param save_value: If true the value will be saved on Inverter.
        :param value: The value to set.
        :param check_value: If True the value will be checked on dgto.

        :return: "True" if the dgto is set at the requested value and check_value = True or if check_value = False,
            "False" if if the dgto is not set at the requested value and check_value = True
        """

        if self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING or self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOTemperatures]", "CoilOutletTemperatureValue_DBL", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            Inverter_APIs.set_parameter("[PacmanHpChatter.TDMTemperatures]", "CoilOutletTemperatureValue_DBL",
                                        value * self._modifier)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOTemperatures]", "CoilOutletTemperatureValue_DBL", value)

        if save_value:
            Inverter_APIs.save_parameters()
            if check_value:
                self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                ris = self._testlib.read_dgto("1-7-3-20")

                if value * 10 != ris:
                    return False

        return True


    def set_LoadStatus_ControlMode(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE):
        """
        Set the value of Control Mode for LoadStatus register
        :param save_value: If true the value will be saved on Inverter.
        :param value: The value to set (0 = Free, 1 = Instantaneous).

        :return: None
        """
        if self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING or self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOLoads]", "LoadsStatusControlMode_DBL", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            Inverter_APIs.set_parameter("[PacmanHpChatter.TDMLoads]", "LoadsStatusControlMode_DBL", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOLoads]", "LoadsStatusControlMode_DBL", value)

        if save_value:
            Inverter_APIs.save_parameters()

    def set_LoadStatusNoise_ControlMode(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE):
        """
        Set the value of Control Mode for LoadStatus register
        :param save_value: If true the value will be saved on Inverter.
        :param value: The value to set (0 = Free, 1 = Instantaneous).

        :return: None
        """
        if self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOLoads]", "LoadsStatusNoiseGeneration_DBL", value)

        if save_value:
            Inverter_APIs.save_parameters()


    def set_CompressorFrequency_ControlMode(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE):
        """
        Set the value of Control Mode for CompressorFrequency register
        :param save_value: If true the value will be saved on Inverter.
        :param value: The value to set (0 = Free, 1 = Instantaneous).

        :return: None
        """
        if self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            Inverter_APIs.set_parameter("[PacmanHpChatter.TDMLoads]", "CompressorFrequencyControlMode_DBL", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON:
            Inverter_APIs.set_parameter("[PacmanHpChatter.POWPower]", "CompressorSpeedControlMode_DBL", value)

        if save_value:
            Inverter_APIs.save_parameters()


    def set_Exv1Position_ControlMode(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE):
        """
        Set the value of Control Mode for LoadStatus register
        :param save_value: If true the value will be saved on Inverter.
        :param value: The value to set (0 = Free, 1 = Instantaneous).

        :return: None
        """
        if self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING or self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOLoads]", "Exv1PositionControlMode_DBL", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            Inverter_APIs.set_parameter("[PacmanHpChatter.TDMLoads]", "ExvPositionControlMode_DBL", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOLoads]", "Exv1PositionControlMode_DBL", value)

        if save_value:
            Inverter_APIs.save_parameters()


    def set_LoadStatus_Feedback(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                                check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto "LOAD_STATUS_REAL_RD" (10-1-2-22)
        :param save_value: If true the value will be saved on Inverter.
        :param check_value: If True the value will be checked on dgto.
        :param value: The value to set.

        :return: "True" if the dgto is set at the requested value and check_value = True or if check_value = False,
            "False" if if the dgto is not set at the requested value and check_value = True
        """
        if self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING or self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOLoads]", "LoadsStatusFeedback_DBL", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            Inverter_APIs.set_parameter("[PacmanHpChatter.TDMLoads]", "LoadsStatusFeedback_DBL", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOLoads]", "LoadsStatusFeedback_DBL", value)

        if save_value:
            Inverter_APIs.save_parameters()

            if check_value:
                self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                ris = self._testlib.read_dgto("10-1-2-22")

                if value != ris:
                    return False

        return True


    def set_CompressorFrequency_Feedback(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                                         check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto "HP Compressor Freq" (4-6-6-11)
        :param save_value: If true the value will be saved on Inverter.
        :param check_value: If True the value will be checked on dgto.
        :param value: The value to set ().

        :return: "True" if the dgto is setted at the requested value and check_value = True or if check_value = False,
            "False" if if the dgto is not setted at the requested value and check_value = True
        """
        set = False

        if self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            Inverter_APIs.set_parameter("[PacmanHpChatter.TDMLoads]", "CompressorFrequencyFeedbackValue_DBL", value)
            set = True
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON:
            Inverter_APIs.set_parameter("[PacmanHpChatter.POWPower]", "CompressorSpeed_DBL", value * 60)
            set = True

        if set and save_value:
            Inverter_APIs.save_parameters()

            if check_value:
                self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                ris = self._testlib.read_dgto("4-6-6-11")

                if value != ris:
                    return False

        return True


    def set_Exv1Position_Feedback(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                                  check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto "EXV1_REAL_RD" (10-1-2-21)
        :param save_value: If true the value will be saved on Inverter.
        :param check_value: If True the value will be checked on dgto.
        :param value: The value to set ().

        :return: "True" if the dgto is setted at the requested value and check_value = True or if check_value = False,
            "False" if if the dgto is not setted at the requested value and check_value = True
        """
        if self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING or self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOLoads]", "Exv1PositionFeedbackValue_DBL", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            Inverter_APIs.set_parameter("[PacmanHpChatter.TDMLoads]", "ExvPositionFeedbackValue_DBL", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOLoads]", "Exv1PositionFeedbackValue_DBL", value)

        if save_value:
            Inverter_APIs.save_parameters()

            if check_value:
                self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                ris = self._testlib.read_dgto("10-1-2-21")

                if value != ris:
                    return False

        return True


    def set_FanSpeed_ControlMode(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE):
        """
        Set the value for the Control Mode of Fan 1 Speed
        :param save_value: If true the value will be saved on Inverter.
        :param value: The value to set (0 = Free, 1 = Instantaneous, ...).

        :return: None
        """
        if self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOLoads]", "Fan1SpeedControlMode_DBL", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            Inverter_APIs.set_parameter("[PacmanHpChatter.TDMLoads]", "Fan1SpeedControlMode_DBL", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOLoads]", "FanIsoSpeedControlMode_DBL", value)

        if save_value:
            Inverter_APIs.save_parameters()


    def set_FanSpeed_Feedback(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                              check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto "FAN 1 Speed Real" (4-15-3-14) Fan 1 Speed Feedback

        :param save_value: If true the value will be saved on Inveter.
        :param value: The value to set.
        :param check_value: If True the value will be checked on dgto.

        :return: "True" if the dgto is set at the requested value and check_value = True or if check_value = False,
            "False" if if the dgto is not set at the requested value and check_value = True
        """

        if self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOLoads]", "Fan1SpeedFeedbackValue_DBL", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            Inverter_APIs.set_parameter("[PacmanHpChatter.TDMLoads]", "Fan1SpeedFeedbackValue_DBL", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOLoads]", "FanIsoSpeedFeedbackValue_DBL", value)

        if save_value:
            Inverter_APIs.save_parameters()

            if check_value:
                self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                ris = self._testlib.read_dgto("4-15-3-14")

                if value != ris:
                    return False

        return True


    def set_SuctionPressure(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                            check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto "CONTROL_BOARD_REG_RD_PS" (15-7-3-19) SuctionPressureValue

        :param save_value: If true the value will be saved on Inverter.
        :param value: The value to set.
        :param check_value: If True the value will be checked on dgto.

        :return: "True" if the dgto is set at the requested value and check_value = True or if check_value = False,
            "False" if if the dgto is not set at the requested value and check_value = True
        """

        if self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING or self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON  \
                or self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOTemperatures]", "SuctionPressureValue_DBL", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            return True  # NOT PRESENT ON THESE CTRL_BOX_ID

        if save_value:
            Inverter_APIs.save_parameters()

            if check_value:
                self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                ris = self._testlib.read_dgto("15-7-3-19")

                if value != ris:
                    return False

        return True


    def set_HP_Outdoor_Temp_OAT(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                                check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto "HP Outdoor Temp (OAT)" (1-0-3-24) OutdoorTemperature

        :param save_value: If true the value will be saved on Inveter.
        :param value: The value to set.
        :param check_value: If True the value will be checked on dgto.

        :return: "True" if the dgto is setted at the requested value and check_value = True or if check_value = False,
            "False" if the dgto is not setted at the requested value and check_value = True
        """
        if self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING or self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOTemperatures]", "OutdoorTemperatureValue_DBL", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            Inverter_APIs.set_parameter("[PacmanHpChatter.TDMTemperatures]", "OutdoorTemperatureValue_DBL",
                                        value * self._modifier)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBOTemperatures]", "OutdoorTemperatureValue_DBL", value)

        if save_value:
            Inverter_APIs.save_parameters()
            if check_value:
                self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                ris = self._testlib.read_dgto("1-0-3-24")

                if value * 10 != ris:
                    return False
        return True


    def set_heatsink_temperature(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                                 check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto "HEATSINK_TEMPERATURE"

        :param save_value: If true the value will be saved on Inveter.
        :param value: The value to set.
        :param check_value: If True the value will be checked on dgto.

        :return: "True" if the dgto is setted at the requested value and check_value = True or if check_value = False,
            "False" if the dgto is not setted at the requested value and check_value = True
        """
        if self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING or self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            Inverter_APIs.set_parameter("[PacmanHpChatter.INVDriveStatus]", "DriveStatusIPMTemp", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            Inverter_APIs.set_parameter("[PacmanHpChatter.TDMTemperatures]", "HeatsinkTemperatureValue_DBL",
                                        value - 550)  # Ticket #15026
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON:
            Inverter_APIs.set_parameter("[PacmanHpChatter.POWPower]", "DriveInternalTemp_DBL", value)

        if save_value:
            Inverter_APIs.save_parameters()
            if check_value:
                self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                ris = self._testlib.read_dgto("HEATSINK_TEMPERATURE")

                if value != ris:
                    return False
        return True


    def set_inverter_output_current(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                                    check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto inverter output current writing in the inverter register
        :param save_value: If true the value will be saved on Inverter.
        :param check_value: If True the value will be checked on dgto.
        :param value: The value to set ().

        :return: "True" if the dgto is setted at the requested value and check_value = True or if check_value = False,
            "False" if the dgto is not setted at the requested value and check_value = True
        """
        if self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING or self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            Inverter_APIs.set_parameter("[PacmanHpChatter.INVDriveStatus]", "DriveStatusINVPhaseCurr_DBL", value * 256)

            if save_value:
                Inverter_APIs.save_parameters()

                if check_value:
                    self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                    ris = (self._testlib.read_dgto("10-9-2-8") / 256)
                    if value != ris:
                        return False
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON:
            Inverter_APIs.set_parameter("[PacmanHpChatter.POWPower]", "PhaseUCurrent_DBL", value * 100)
            Inverter_APIs.set_parameter("[PacmanHpChatter.POWPower]", "PhaseVCurrent_DBL", value * 100)
            Inverter_APIs.set_parameter("[PacmanHpChatter.POWPower]", "PhaseWCurrent_DBL", value * 100)

            if save_value:
                Inverter_APIs.save_parameters()

                if check_value:
                    self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                    ris = (self._testlib.read_dgto("10-9-2-8") / 256)
                    if value != ris:
                        return False
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            Inverter_APIs.set_parameter("[PacmanHpChatter.TDMDiagnostic]", "CompressorCompressorPhaseCurrent_DBL",
                                        value * 10)

            if save_value:
                Inverter_APIs.save_parameters()

                if check_value:
                    self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                    ris = (self._testlib.read_dgto("10-9-2-8") / 256)

                    if value != ris:
                        return False

        return True


    def set_inverter_cmp_heater_cur(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                                    check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto inverter compressor heater current writing in the inverter register
        :param save_value: If true the value will be saved on Inverter.
        :param check_value: If True the value will be checked on dgto.
        :param value: The value to set ().

        :return: "True" if the dgto is setted at the requested value and check_value = True or if check_value = False,
            "False" if the dgto is not setted at the requested value and check_value = True
        """
        if self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING or self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            w_val = round((value * 256) / 10)
            Inverter_APIs.set_parameter("[PacmanHpChatter.INVDriveStatus]", "DriveStatusINVUPhCurr_DBL", w_val)

            if save_value:
                Inverter_APIs.save_parameters()

                if check_value:
                    self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                    ris = (self._testlib.read_dgto("INVERTER_REG_RD_OUTCURR_U"))
                    if value != ris:
                        return False

        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON:
            Inverter_APIs.set_parameter("[PacmanHpChatter.POWPower]", "CompressorHeatCurrent_DBL", value)

            if save_value:
                Inverter_APIs.save_parameters()

                if check_value:
                    self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                    ris = (self._testlib.read_dgto("INVERTER_REG_RD_CMP_HTR_I_RD"))
                    if value != ris:
                        return False
        else:
            return False

        return True


    def set_CMP_Warning(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                        check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto CMP_WARNINING_RD writing in the inverter register
        :param save_value: If true the value will be saved on Inverter.
        :param check_value: If True the value will be checked on dgto.
        :param value: The value to set ().

        :return: "True" if the dgto is setted at the requested value and check_value = True or if check_value = False,
            "False" if the dgto is not setted at the requested value and check_value = True
        """
        Inverter_APIs.set_parameter("[PacmanHpChatter.TDMDiagnostic]", "CompressorCompressorWarningFaultCode_DBL",
                                    value)

        if save_value:
            Inverter_APIs.save_parameters()

            if check_value:
                self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                ris = self._testlib.read_dgto("10-2-2-2")

                if value != ris:
                    return False
        return True


    def set_Speed_Drop_Protection_EK(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                                     check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto SET_SPEED_DROP_PROTECTION_EK_RD writing in the inverter register
        :param save_value: If true the value will be saved on Inverter.
        :param check_value: If True the value will be checked on dgto.
        :param value: The value to set ().

        :return: "True" if the dgto is setted at the requested value and check_value = True or if check_value = False,
            "False" if the dgto is not setted at the requested value and check_value = True
        """
        Inverter_APIs.set_parameter("[PacmanHpChatter.INVDiagnostic]", "SpeedDropProtectionFault_DBL", value)

        if save_value:
            Inverter_APIs.save_parameters()

            if check_value:
                self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                ris = self._testlib.read_dgto("10-7-2-4")

                if value != ris:
                    return False
        return True


    def set_TDM_HHP_Inv_Speed_Drop_Protect(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                                           check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto TDM_HHP_INV_SPEED_DROP_PROTECT writing in the inverter register
        :param save_value: If true the value will be saved on Inverter.
        :param check_value: If True the value will be checked on dgto.
        :param value: The value to set ().

        :return: "True" if the dgto is setted at the requested value and check_value = True or if check_value = False,
            "False" if the dgto is not setted at the requested value and check_value = True
        """
        Inverter_APIs.set_parameter("[PacmanHpChatter.POWInputParameter3]", "SpeedDropProtect_DBL", value)

        if save_value:
            Inverter_APIs.save_parameters()

            if check_value:
                self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                ris = self._testlib.read_dgto("10-4-3-3")

                if value != ris:
                    return False
        return True


    def set_SYSTEM_SHUT_OFF_RD(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                               check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto SYSTEM_SHUT_OFF_RD writing in the inverter register
        :param save_value: If true the value will be saved on Inverter.
        :param check_value: If True the value will be checked on dgto.
        :param value: The value to set ().

        :return: "True" if the dgto is setted at the requested value and check_value = True or if check_value = False,
            "False" if the dgto is not setted at the requested value and check_value = True
        """
        if self._CTRL_BOX_ID in CTRL_BOX_ID.RUKING:
            Inverter_APIs.set_parameter("[PacmanHpChatter.TDMDiagnostic]", "SystemSystemShutOffFaultCode_DBL", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING or self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBODiagnostics]", "SystemSystemShutOffFaultCode_DBL", value)
        elif self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON:
            Inverter_APIs.set_parameter("[PacmanHpChatter.CBODiagnostics]", "SystemSystemShutOffFaultCode_DBL", value)

        if save_value:
            Inverter_APIs.save_parameters()

            if check_value:
                self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                ris = self._testlib.read_dgto("10-2-2-5")

                if value != ris:
                    return False
        return True


    def set_SYSTEM_FAULT_Shut_Down_EK_RD(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                                                 check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto SYSTEM_FAULT_SHUT_DOWN_EK_RD writing in the inverter register
        :param save_value: If true the value will be saved on Inverter.
        :param check_value: If True the value will be checked on dgto.
        :param value: The value to set ().

        :return: "True" if the dgto is setted at the requested value and check_value = True or if check_value = False,
            "False" if the dgto is not setted at the requested value and check_value = True
        """
        if self._CTRL_BOX_ID in CTRL_BOX_ID.ECOKING or self._CTRL_BOX_ID in CTRL_BOX_ID.WOLF:
            Inverter_APIs.set_parameter("[PacmanHpChatter.INVDiagnostic]", "SystemFault_DBL", value)

        if save_value:
            Inverter_APIs.save_parameters()

            if check_value:
                self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                ris = self._testlib.read_dgto("10-7-2-0")

                if value != ris:
                    return False
        return True


    def set_TDM_HHP_INV_SYS_FAULT(self, value: int, save_value: bool = DEFAULT_SAVE_VALUE,
                                                 check_value: bool = DEFAULT_CHECK_VALUE):
        """
        Set the value of dgto TDM_HHP_INV_SYS_FAULT writing in the inverter register
        :param save_value: If true the value will be saved on Inverter.
        :param check_value: If True the value will be checked on dgto.
        :param value: The value to set ().

        :return: "True" if the dgto is setted at the requested value and check_value = True or if check_value = False,
            "False" if the dgto is not setted at the requested value and check_value = True
        """
        if self._CTRL_BOX_ID in CTRL_BOX_ID.ARISTON:
            Inverter_APIs.set_parameter("[PacmanHpChatter.POWInputParameter3]", "SysFault_DBL", value)

        if save_value:
            Inverter_APIs.save_parameters()

            if check_value:
                self._testlib.wait_time(DEFAULT_CHECK_TIMER)
                ris = self._testlib.read_dgto("10-4-3-2")

                if value != ris:
                    return False
        return True


    def read_var_ram(self, namevar: str, skipComment=False):
        """
        Read a specific variable present on module RAM_VAR

        :param namevar: the name of the variable to be read
        :param skipComment: FALSE -> if True, comment doesn't write in report [bool]

        :return: Returns var “r”, if the operation is completed successfully res will contain the data read, otherwise will contain None
        """
        r = None

        if namevar not in RAM_VAR:
            self.add_comment(f"Error! \'{namevar}\' not found in RAM_VAR.py.", print_on_console=True,
                             background_color="ERROR")
        if RAM_VAR[namevar]['format'] == 0:
            r = self.read_ram(RAM_VAR[namevar]['address'], RAM_VAR[namevar]['len'], RAM_VAR[namevar]['signed'],
                              RAM_VAR[namevar]['endian'])

            if r is None:
                print(f"An error occurred during reading operation: RAM_VAR {namevar} has not been read")
                self._testlib._report.add_action_row(
                        self._testlib._options["device"], self._testlib._actions["READ"], namevar, None, None,
                        self._testlib._results["ERROR"], "Error occurred during reading operation")
            elif not skipComment:
                print(f"RAM_VAR {namevar} = {r}")
                self._testlib._report.add_action_row(
                        self._testlib._options["device"], self._testlib._actions["READ"], namevar, r, None,
                        self._testlib._results["SUCCESS"], None)
        else:
            array_len = None
            try:
                array_len = int(RAM_VAR[namevar]['len'] / RAM_VAR[namevar]['element_dim'])
            except:
                print("Error during calculation of array length")
                return r

            r = []

            for i in range(array_len):
                addr_val = int(RAM_VAR[namevar]['address'])
                addr_val = addr_val + i * RAM_VAR[namevar]['element_dim']
                r_e = self.read_ram(addr_val, RAM_VAR[namevar]['element_dim'], RAM_VAR[namevar]['signed'],
                                  RAM_VAR[namevar]['endian'])
                r.append(r_e)

        return r


    def write_ram(self, mem_address: int, num_byte_rx: int, signed: int = 1, endian: int = 0, value: int = None):
        if endian != 1 and endian != 0 and signed != 0 and signed != 1 or value is None:
            self.add_comment("Wrong endian, signed or value, please insert 0 for Little Endian and 1 for Big Endian, "
                             "0 for unsigned and 1 for signed and pass the correct value to write.", print_on_console=True, background_color="ERROR")
            return None

        if signed == 0 and (value >= pow(2, (8 * num_byte_rx)) or value < 0):
            self.add_comment(f"Wrong value insert for unsigned type, the value can't be smaller than 0 or higher than {pow(2, num_byte_rx) - 1}.",
                             print_on_console=True, background_color="ERROR")
            return None
        elif signed == 1 and (value >= pow(2, (8 * num_byte_rx) - 1) or value <= (pow(2, (8 * num_byte_rx) - 1) * -1)):
            self.add_comment(
                f"Wrong value insert for signed type, the value can't be smaller than {(pow(2, (8 * num_byte_rx) - 1) * -1)} or higher than {pow(2, ( 8 * num_byte_rx) - 1)}.",
                print_on_console=True, background_color="ERROR")
            return None

        value_in_bytes = None

        if signed == 0:
            if num_byte_rx == 1:
                value_in_bytes = ctypes.c_uint8(value)
            elif num_byte_rx == 2:
                value_in_bytes = ctypes.c_uint16(value)
            elif num_byte_rx == 4:
                value_in_bytes = ctypes.c_uint32(value)
            elif num_byte_rx == 8:
                value_in_bytes = ctypes.c_uint64(value)
        if signed == 1:
            if num_byte_rx == 1:
                value_in_bytes = ctypes.c_int8(value)
            elif num_byte_rx == 2:
                value_in_bytes = ctypes.c_int16(value)
            elif num_byte_rx == 4:
                value_in_bytes = ctypes.c_int32(value)
            elif num_byte_rx == 8:
                value_in_bytes = ctypes.c_int64(value)

        value_in_bytes_splitted = self._testlib._split_hex(value_in_bytes.value)

        res = self._testlib.write_flash(mem_address, value_in_bytes_splitted)

        return res


    def read_ram(self, mem_address: int, num_byte_rx: int, signed: int = 1, endian: int = 0):
        """
        Sw spec :NA
        parameter: self: class instance
        parameter: Mem_address integer that contains the address in RAM memory of the frame requested [int]
        parameter: num_byte_rx indicates the number of bytes that will be received [int]
        parameter: signed: 0 unsigned, 1 signed
        parameter: endianess: 0 little endian, 1 big endian
        description: This function reads a frame of RAM data by direct access to the internal memory (RAM/ROM or EEPROM)
            If the dllhandler read memory =  false, for no of bytes read with in the Value
            (try the second value is > first value)it will add to list and print ,else return false
        :Remarks	:Create the variable for RAM Address, Buffer and no of bytes to read
        """

        if endian != 1 and endian != 0 and signed != 0 and signed != 1:
            self.add_comment("Wrong endian or signed value, please insert 0 for Little Endian and 1 for Big Endian, "
                             "0 for unsigned and 1 for signed.", print_on_console=True, background_color="ERROR")
            return None

        res = self._testlib.read_memory(mem_address, num_byte_rx)

        if not res or len(res) != 2:
            return None

        data = res[1]

        if endian == 1:
            data = data[::-1]

        val = 0

        for i in range(len(data)):
            raw = data[i] << (i * 8)
            val = val + raw

        if signed == 1:
            last_byte = pow(2, ((num_byte_rx * 8) - 1))
            sign = val & last_byte

            if sign == last_byte:
                v_sign = 0
                for i in range((num_byte_rx * 8) - 1):
                    e = pow(2, i)
                    if val & e == 0:
                        v_sign = v_sign + e

                v_sign = v_sign + 1
                val = v_sign * -1

        return val


    def send_reset(self):
        """
            :Sw Spec	: Na
            :param self:    instance class
            :param time:    the time to wait before the reset
            :Return values : None
            :Description    :This function use a raw request to send a reset command)
            :Remarks: none
        """
        self.add_comment("Reset operation started", print_on_console=True, background_color="INFO")

        data_msg = [0x03]  # 3s the reset will occur at the end of 3s

        # Command 0x53 = "RESET COMMAND"
        total_data_return = self._testlib._raw_request(0x53, data_msg)  # Attualmente la _raw_request non permette di controllare il risultato dell'operazione

    """
                                ---------------------------
                                --   TestLib functions   --
                                ---------------------------
    """


    def add_comment(self, comment: str, background_color: str = "TRANSPARENT", print_on_console: bool = False) -> None:
        """
        Add a comment on Report.
        """
        self._testlib._report.add_comment_row(comment, background_color, print_on_console)


    def read_dgto(self, dgto: str, skipComment: bool = False) -> int:

        return self._testlib.read_dgto(dgto, skipComment)


    def read_dgto_until(self, dgto: str, operator: str, limit: int, custom_string: str = "") -> None:

        return self._testlib.read_dgto_until(dgto, operator, limit, custom_string)


    def write_dgto(self, dgto_name: str, value: int, check_time: int = None, is_multiwrite: bool = False) -> bool:
        dgto = None
        corrective_factor = 1  # Ticket #35:  added the management of DGTO in fixed setpoint in check value step.

        if dgto_name == "1-0-3-25" or dgto_name == "HP Evaporator Temp (OCT)":
            dgto = "1-0-3-25"
            self.set_HP_Evaporator_Temp_OCT(value / 10, True, False)
        elif dgto_name == "1-7-3-20" or dgto_name == "EM HP Evaporator AUX":
            dgto = "1-7-3-20"
            self.set_EM_HP_Evaporator_AUX(value / 10, True, False)
        elif dgto_name == "1-7-3-19" or dgto_name == "EM HP Discharge Temp":
            dgto = "1-7-3-19"
            self.set_Discharge_Temp_TD(value / 10, True, False)
        elif dgto_name == "1-0-3-24" or dgto_name == "HP Outdoor Temp (OAT)":
            dgto = "1-0-3-24"
            self.set_HP_Outdoor_Temp_OAT(value / 10, True, False)
        elif dgto_name == "4-15-3-28" or dgto_name == "HP Power Calculation":
            dgto = "4-15-3-28"
            delta_pw = self._testlib.read_dgto("HP_LOADS_POWER_W")
            self.set_DriveStatus_InputPower(value - delta_pw, True, False)
        elif dgto_name == "10-4-3-12" or dgto_name == "CMP_ELECTRICAL_PWR_W":
            dgto = "10-4-3-12"
            self.set_DriveStatus_InputPower(value, True, False)
        elif dgto_name == "10-9-2-7" or dgto_name == "INVERTER_INPUT_CURRENT":
            dgto = "INVERTER_INPUT_CURRENT"
            corrective_factor = 256
            self.set_DriveStatus_InputCurrent(value, True, False)
        elif dgto_name == "10-9-2-8" or dgto_name == "INVERTER_OUTPUT_CURRENT":
            dgto = "INVERTER_OUTPUT_CURRENT"
            corrective_factor = 256
            self.set_inverter_output_current(value, True, False)
        elif dgto_name == "10-2-2-2" or dgto_name == "CMP_WARNINIG_RD":
            dgto = "CMP_WARNINIG_RD"
            self.set_CMP_Warning(value, True, False)
        elif dgto_name == "10-7-2-4" or dgto_name == "SPEED_DROP_PROTECTION_EK_RD":
            dgto = "SPEED_DROP_PROTECTION_EK_RD"
            self.set_Speed_Drop_Protection_EK(value, True, False)
        elif dgto_name == "10-4-3-3" or dgto_name == "TDM_HHP_INV_SPEED_DROP_PROTECT":
            dgto = "TDM_HHP_INV_SPEED_DROP_PROTECT"
            self.set_TDM_HHP_Inv_Speed_Drop_Protect(value, True, False)
        elif dgto_name == "10-4-3-17" or dgto_name == "HEATSINK_TEMPERATURE":
            dgto = "HEATSINK_TEMPERATURE"
            self.set_heatsink_temperature(value, True, False)
        elif dgto_name == "10-4-3-19" or dgto_name == "INVERTER_REG_RD_OUTCURR_U":
            dgto = "INVERTER_REG_RD_OUTCURR_U"
            self.set_inverter_cmp_heater_cur(value, True, False)
        elif dgto_name == "10-4-3-13" or dgto_name == "INVERTER_REG_RD_CMP_HTR_I_RD":
            dgto = "INVERTER_REG_RD_CMP_HTR_I_RD"
            self.set_inverter_cmp_heater_cur(value, True, False)
        elif dgto_name == "1-7-3-18" or dgto_name == "EM HP Suction Temp":
            dgto = "EM HP Suction Temp"
            self.set_Suction_Temp(value / 10, True, False)
        elif dgto_name == "10-2-2-5" or dgto_name == "SYSTEM_SHUT_OFF_RD":
            dgto = "SYSTEM_SHUT_OFF_RD"
            self.set_SYSTEM_SHUT_OFF_RD(value, True, False)
        elif dgto_name == "10-7-2-0" or dgto_name == "SYSTEM_FAULT_SHUT_DOWN_EK_RD":
            dgto = "SYSTEM_FAULT_SHUT_DOWN_EK_RD"
            self.set_SYSTEM_FAULT_Shut_Down_EK_RD(value, True, False)
        elif dgto_name == "10-4-3-2" or dgto_name == "TDM_HHP_INV_SYS_FAULT":
            dgto = "TDM_HHP_INV_SYS_FAULT"
            self.set_TDM_HHP_INV_SYS_FAULT(value, True, False)
        elif dgto == "15-7-3-20" or dgto_name == "CONTROL_BOARD_REG_RD_PD":
            dgto = "CONTROL_BOARD_REG_RD_PD"
            self.set_Discharge_Pressure(value, True, False)
        elif dgto_name == "15-7-3-19" or dgto_name == "CONTROL_BOARD_REG_RD_PS":
            dgto = "CONTROL_BOARD_REG_RD_PS"
            self.set_SuctionPressure(value, True, False)
        if dgto is not None:
            if check_time is None:
                check_time = 10

            self._testlib.wait_time(check_time)
            r_value = self.read_dgto(dgto, True)
            r_value = r_value / corrective_factor

            result = r_value == value

            if result:
                print(f"Inverter DGTO {dgto_name} has been written correctly with value {str(value)}")
                self._testlib._report.add_action_row(
                        self._testlib._options["device"], self._testlib._actions["WRITE"], dgto_name, None, r_value,
                        self._testlib._results["SUCCESS"], None)
            else:
                print(f"WARNING: Inverter DGTO {dgto_name} has been NOT written with value {str(value)}")
                self._testlib._report.add_action_row(
                        self._testlib._options["device"], self._testlib._actions["WRITE"], dgto_name, None, r_value,
                        self._testlib._results["WARNING"], f"NOT written with value {value}")

            return result

        return self._testlib.write_dgto(dgto_name, value, check_time, is_multiwrite)


    def multiwrite_dgto(self, array_dgto: list, array_values: list, check_time: int = 10) -> bool:

        return self._testlib.multiwrite_dgto(array_dgto, array_values, check_time)


    def ping_dgto(self, dgto: str, expected_value: int, step_time: int = 1, expire_time: int = 60) -> bool:

        return self._testlib.ping_dgto(dgto, expected_value, step_time, expire_time)


    def multiping_dgto(self, array_dgto: list, array_expected_values: list, step_time: int = 1,
                       expire_time: int = 60) -> list:

        return self._testlib.multiping_dgto(array_dgto, array_expected_values, step_time, expire_time)


    def detect_dgto_change(self, dgto: str, expected_value: int = None, step_time: int = 1, expire_time: int = 60):

        return self._testlib.detect_dgto_change(dgto, expected_value, step_time, expire_time)


    def wait_time(self, waiting_time: int):

        return self._testlib.wait_time(waiting_time)


    def read_dgto_range(self, dgto_name: str):

        return self._testlib.read_dgto_range(dgto_name)


    def set_Channel_values(self, channels: dict, values: dict) -> bool:

        return self._testlib.set_channel_values(channels, values)


    def get_channel_values(self, list_channels):

        return self._testlib.get_channel_values(list_channels)


    def restore_channel_values(self):

        return self._testlib.restore_channel_values()


    def save_channel_values(self):

        return self._testlib.save_channel_values()


    def update_report(self, test_passed: bool):

        return self._testlib._report.update_report(test_passed)


    def write_memory(self, mem_address: int, data: list[int]) -> bool:
        """
        Sw spec :NA\n
        parameter: self class instance\n
        parameter: mem_address RAM address [int]\n
        parameter: data    information to write in RAM [list of int]\n
        return values  True=Success or False= Unsuccessful [bool]\n
        description	This function write a frame in RAM data by direct\n
        access to the internal memory (RAM/ROM or EEPROM)\n
        remarks	: none
        """

        return self._testlib.write_memory(mem_address, data)

    def ReadTDA(self) -> str:
        """
            :Sw Spec	: Na
            :param self:     instance class
            :return values :str :  TDA value if the TDA reading operation is performed successfully, None if the reading operation fails
            :Description  :Call function TDAReadInfo() This function read all the TDA from the main board.
            :Remarks: none
        """

        return self._testlib.ReadTDA()

    def WriteTDA(self, tda: str, plant: str = "") -> bool:
        """
            :Sw Spec	: Na
            :param self:     instance class
            :param tda: a string containing the TDA board_code value
            :param plant: a string containing the plant value to set
            :return values :bool :  true if the TDA writing operation is performed successfully, None if the writing operation fails
            :Description  :Call function TDAWriteInfo() and TDARegisterTest() This two functions write the TDA board_code, plant and test result on the main board.
            :Remarks: none
        """

        return self._testlib.WriteTDA(tda, plant)

    def readIdentTable(self):
        """
            :Sw Spec	: Na
            :param self:     instance class
            :Return values : Bool : "True", Result[] if request condition has been satisfied, where Result[] contains all IdentTable info
                                    "False" if request condition has not satisfied
            :Description    :This function use a raw request to read a Specific Data (command = 0x24),
                            in this case the data is the Ident Table (ID_Msg = 0x00), if the data are received correctly
                            the function proceeds to extract all info of Ident Table (see doc. IdentTableType2_XvYY.docx)
            :Remarks: none
        """

        return self._testlib.readIdentTable
