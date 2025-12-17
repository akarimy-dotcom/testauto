# Ariston Test Automation Framework - Complete Analysis Report

**Report Date:** 2025-12-17
**Analyst:** Claude AI
**Repository:** testauto

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Repository Structure](#2-repository-structure)
3. [Core Framework Analysis (kt10)](#3-core-framework-analysis-kt10)
4. [TDM4 Project Analysis (kt12)](#4-tdm4-project-analysis-kt12)
5. [pymtstestlib Analysis](#5-pymtstestlib-analysis)
6. [Component Relationships](#6-component-relationships)
7. [OTA Test Script Evaluation](#7-ota-test-script-evaluation)
8. [Identified Issues & Gaps](#8-identified-issues--gaps)
9. [Recommendations](#9-recommendations)

---

## 1. Executive Summary

This repository contains **Ariston's Python-based test automation framework** for HVAC/Heat Pump systems, specifically targeting **TDM4 (Thermal Device Manager)** devices. The codebase is split across multiple ZIP archives with **version inconsistencies** and **missing dependencies**.

### Key Findings

| Aspect | Status | Details |
|--------|--------|---------|
| Framework Version | v2.2.2 | TestAutomationFramework_FULL_2.2.2 |
| TDM4 Classes Version | v0.6.0 | TDM4_Classes_00_07_00 |
| pymtstestlib Version | v00.00.06 | Only setup.py present, **source code missing** |
| Code Organization | Poor | Files scattered across nested ZIP archives |
| Dependencies | Incomplete | Missing Inverter_APIs.py, pymtstestlib source |
| Version Compatibility | Mismatch | TDM_Manager expects TestLib v1.8.0, actual is v2.2.2 |

---

## 2. Repository Structure

### 2.1 Root Level Files

```
testauto/
├── README.md              # pymtstestlib documentation
├── setup.py               # pymtstestlib package installer (source missing)
├── kt_zip (10).zip        # Core framework archive
├── kt_zip (12).zip        # TDM4 project classes archive
└── extracted/             # Extracted contents for analysis
```

### 2.2 Extracted Structure

```
extracted/
├── kt10/Root Folder/Test Automation/Python_Framework/Releases/
│   └── TestAutomationFramework_FULL_2.2.2/
│       ├── libs/                    # Core library modules
│       │   ├── __init__.py
│       │   ├── TestLib.py          # Main test library (2,800+ lines)
│       │   ├── Report.py           # Excel/TXT report generation
│       │   ├── ConfigParser.py     # Configuration file parser
│       │   ├── FWPRJ.py            # DGTO index from .fwprj files
│       │   └── Ares5Env.py         # Ares5 environment configuration
│       ├── configs/                 # Configuration files
│       │   ├── __init__.py
│       │   ├── Config.py           # Configuration loader
│       │   ├── Config.txt          # Device settings
│       │   └── Config_Ares5_example.txt
│       ├── sources/                 # Source configuration files
│       │   └── Config_PRG026.cfg
│       ├── reports/                 # Output directory (empty)
│       └── new_ares5_method_example.py  # Usage example
│
└── kt12/Root Folder/Test Automation/Projects/TDM4/
    └── TDM4_Classes_00_07_00/
        ├── __init__.py
        ├── TDM_Manager.py          # Main TDM controller (1,800+ lines)
        ├── RAM_VAR.py              # RAM variable addresses
        ├── CTRL_BOX_ID.py          # Control box identifiers
        ├── LAB_MODE.py             # Lab mode algorithms
        ├── OVERRIDE.py             # Override bit flags
        ├── FILE_INIT.py            # Device initialization data
        └── TDM_Manager_SWSpecifications_1v9.docx  # Documentation
```

---

## 3. Core Framework Analysis (kt10)

### 3.1 TestLib.py - Main Test Library

**Location:** `extracted/kt10/.../libs/TestLib.py`
**Version:** 2.2.2
**Author:** Juan Pablo Perruzza & Intelligentia SRL, Ruggeri Nicolò
**Size:** ~2,800 lines

#### Purpose
Central hub for all device communication, providing abstraction over the low-level pymtstestlib API.

#### Key Classes

```python
class TestLib:
    """Main test library class"""
    _api = None           # pymtstestlib API instance
    _ares5_env = None     # Ares5 environment config
    _fwprj = None         # FWPRJ DGTO index
    _report = None        # Report generator instance
```

#### Key Methods - DGTO Operations (Ares4)

| Method | Description | Parameters |
|--------|-------------|------------|
| `read_dgto(dgto, silent)` | Read single DGTO value | dgto: name or code |
| `write_dgto(dgto, value, ...)` | Write single DGTO value | Includes verification |
| `multiread_dgto(dgto_list)` | Read multiple DGTOs | Up to 8 at once |
| `multiwrite_dgto(dgto_list, values)` | Write multiple DGTOs | Up to 8 at once |
| `ping_dgto(dgto, expected, timeout)` | Wait for value | Polling with timeout |
| `detect_dgto_change(dgto, timeout)` | Detect value change | Returns when changed |

#### Key Methods - DataID Operations (Ares5)

| Method | Description | Parameters |
|--------|-------------|------------|
| `read_DataId(data_id, czo)` | Read DataID by name/code | Supports Standard/Array/Stream |
| `write_DataId(data_id, czo, value)` | Write DataID value | With verification |
| `read_DataIdList(data_ids, czo)` | Multi-read DataIDs | Standard types only |
| `write_DataIdList(data_ids, czo, values)` | Multi-write DataIDs | Standard types only |

#### Key Methods - Device Operations

| Method | Description |
|--------|-------------|
| `ReadTDA()` | Read Test Data Area |
| `WriteTDA(code, info)` | Write Test Data Area |
| `send_reset(timer)` | Send ATG Reset Command |
| `read_memory(address, length, czo)` | Read device memory |
| `write_memory(address, data, czo)` | Write device memory |
| `operation_control_set(command, params)` | Send operation control |
| `ErrorHistoryReset()` | Clear error history |

#### Configuration Requirements

```python
settings = {
    "port": 13,                      # COM port number
    "baudRate": 38400,               # Baud rate
    "dgtoSourcePath": "path/to/dgto", # Excel file with DGTO definitions
    "probeSourcePath": "path/to/probe", # Probe calibration data
    "phantomSourcePath": "path/to/phantom", # Phantom DGTO definitions
    "fwprjSourcePath": "path/to/fwprj", # .fwprj file path
    "Ares5EnvSourcePath": "path/to/env", # Env.XML for Ares5
    "probe_check_time": 10,          # Seconds to wait after probe write
    "dgto_check_time": 1,            # Seconds to wait after DGTO write
    "device": "Device xx.yy.zz"      # Device identifier
}
```

---

### 3.2 Report.py - Report Generation

**Location:** `extracted/kt10/.../libs/Report.py`
**Version:** 2.2.2

#### Purpose
Generates test reports in both TXT and XLSX (Excel) formats with color-coded results.

#### Key Features

```python
class Report:
    def add_action_row(device, action, dgto, value, expected, result, note)
    def add_comment_row(comment, background_color)
    def update_report(test_passed, test_result_info)
    def create_report(testResult)  # TXT format
```

#### Result Color Codes

| Result | Color | Hex Code |
|--------|-------|----------|
| SUCCESS | Green | #70AD47 |
| ERROR | Red | #C00000 |
| WARNING | Orange | #FFC000 |
| INFO | Blue | #4397B1 |

#### Test Result Info Codes

| Code | Meaning | Report Text |
|------|---------|-------------|
| 0 | Standard Fail | "TEST FAILED" |
| 1 | Precondition Fail | "TEST FAILED PRECONDITION" |
| 2 | Step Fail | "TEST FAILED STEP" |
| 3 | Blocked | "TEST BLOCKED" |
| 4 | Incomplete | "TO BE COMPLETED" |

---

### 3.3 ConfigParser.py - Configuration Parser

**Location:** `extracted/kt10/.../libs/ConfigParser.py`
**Version:** 2.2.2

#### Purpose
Parses configuration files with section-based format.

#### Config File Format

```
@section_name
key1:value1
key2:"string_value"
key3:123

@another_section
key1:456
```

#### Usage

```python
parser = ConfigParser("./configs/Config.txt")
device_config = parser.get_configuration("device_config")
# Returns: {"port": 13, "baudRate": 38400, ...}
```

---

### 3.4 FWPRJ.py - DGTO Index Parser

**Location:** `extracted/kt10/.../libs/FWPRJ.py`
**Version:** 2.2.2
**Author:** Ruggeri Nicolò

#### Purpose
Parses `.fwprj` XML files to build DGTO lookup tables for Ares4 devices.

#### DGTO Types

1. **Standard DGTOs** - Regular datapoints
2. **Phantom DGTOs** - Variable address-backed datapoints

#### Key Methods

```python
class FWPRJ:
    def searchStandardDGTO(dgto: str) -> tuple[name, code, code_value]
    def searchPhantomDGTO(dgto: str) -> tuple[name, code, code_value, address, offset]
```

#### DGTO Code Format

```
D-G-T-O format: Device-Group-Type-Occurrence
Example: "10-0-6-22" = Device 10, Group 0, Type 6, Occurrence 22

Hex conversion: 0xDGTO where each nibble represents D, G, T*2+O/16, O%16
```

---

### 3.5 Ares5Env.py - Ares5 Environment

**Location:** `extracted/kt10/.../libs/Ares5Env.py`
**Version:** 2.2.2
**Author:** Ruggeri Nicolò

#### Purpose
Manages Ares5 environment configuration from XML files.

#### DataID Format

```
DataType-DataIndex-Field format
Example: "2-4360-2" = DataType 2, DataIndex 4360, Field 2
```

#### Key Classes

```python
class DataTypeFunction(Enum):
    DATA_TYPE_STANDARD = 0  # Scalar values
    DATA_TYPE_ARRAY = 1     # Fixed/dynamic arrays
    DATA_TYPE_STREAM = 2    # Stream values

class AccessType(Enum):
    READ_ONLY = 0
    READ_AND_WRITE = 1
    WRITE_ONLY = 2
    DEFINED_AT_RUNTIME = 3
    INHERIT_FROM_DATAINDEX = 4
```

#### Supported Data Types

```python
DATA_TYPE_STANDARD = ['BOOL', 'FLOAT', 'INT16', 'UINT16', 'UINT32', 'UINT8']
DATA_TYPE_ARRAY = ['UINT8_FIXED_SIZE_ARRAY', 'UINT8_DYNAMIC_SIZE_ARRAY']
DATA_TYPE_STREAM = ['UINT8_STREAM']
```

---

## 4. TDM4 Project Analysis (kt12)

### 4.1 TDM_Manager.py - TDM Controller

**Location:** `extracted/kt12/.../TDM_Manager.py`
**Version:** 0.6.0
**Authors:** Nicolò Ruggeri, Raffaela Caddori
**Size:** ~1,800 lines

#### Purpose
High-level TDM state management, controlling heating/cooling cycles, defrost, and inverter communication.

#### Dependencies

```python
import classes.CTRL_BOX_ID as CTRL_BOX_ID
import classes.LAB_MODE as LAB_MODE
import libs.Inverter_APIs as Inverter_APIs  # MISSING!
from classes.RAM_VAR import VAR as RAM_VAR
from libs.TestLib import TestLib
```

#### Version Requirement

```python
Framework_Ver = "1.8.0"  # MISMATCH: Actual TestLib is 2.2.2!
```

#### TDM Status States

```python
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
```

#### Key Methods

| Method | Description |
|--------|-------------|
| `set_tdm_status(status)` | Transition to target state |
| `reset_tdm()` | Reset to INIT state (101) |
| `service_reset_tdm()` | Service reset to INIT |
| `set_standby()` | Go to STANDBY (1) |
| `set_heating_state(target)` | Enter heating mode (15-17) |
| `set_cooling_state(target)` | Enter cooling mode (25-27) |
| `set_DEFROST_ENABLE_ON()` | Enable automatic defrost |
| `set_MANUALDEFROST_ENABLE_ON()` | Enable manual defrost |
| `set_lab_mode_active()` | Activate laboratory mode |
| `read_var_ram(var_name)` | Read RAM variable |
| `write_ram(address, data)` | Write to RAM |

#### Timing Constants

```python
HEAT_COOLING_TIMER = 80      # Max seconds to reach heating/cooling state
PING_DEFAULT_TIMER = 30      # Max seconds for ping_dgto timeout
HEATING_DEFAULT_SETPOINT = 600  # 60°C
COOLING_DEFAULT_SETPOINT = 100  # 10°C
DEFAULT_EWT_FILTER_TIME_MSEC = 100
```

---

### 4.2 CTRL_BOX_ID.py - Device Identifiers

**Location:** `extracted/kt12/.../CTRL_BOX_ID.py`

#### Supported Devices

```python
# Individual IDs
R290_10KW_PRELIMINARY = 101
R290_PCM5_PROTOTYPES_ARISTON = 102
R290_PCM5_PROTOTYPES_ID = 103
PCM5_XS_1ph = 104
PCM5_S_1ph = 105
PCM5_M_1ph = 106
PCM5_M_3ph = 107
PCM5_L_1ph = 108
PCM5_L_3ph = 109
PCM5_XL_1ph = 110
PCM5_XL_3ph = 111
MINI2_5KW = 112
WOLF_1UP7kW = 113
WOLF_1UP10kW = 114
WOLF_1UP13kW = 115

# Grouped by inverter type
RUKING = [R290_PCM5_PROTOTYPES_ID, PCM5_XS_1ph, PCM5_S_1ph, PCM5_M_1ph]
ARISTON = [R290_PCM5_PROTOTYPES_ARISTON, PCM5_M_3ph, PCM5_L_3ph, PCM5_XL_3ph]
ECOKING = [R290_10KW_PRELIMINARY, PCM5_L_1ph, PCM5_XL_1ph, MINI2_5KW]
WOLF = [WOLF_1UP7kW, WOLF_1UP10kW, WOLF_1UP13kW]
```

---

### 4.3 RAM_VAR.py - RAM Variable Addresses

**Location:** `extracted/kt12/.../RAM_VAR.py`

#### Purpose
Defines RAM addresses for direct memory access operations.

#### Structure

```python
VAR = {
    'm_heatsinkTemperature_9_7': {
        'address': 0x0000a2d2,
        'len': 2,
        'endian': 0,    # 0 = Little, 1 = Big
        'format': 0,    # 0 = Scalar, 1 = Array
        'signed': 1     # 0 = Unsigned, 1 = Signed
    },
    # ... 50+ more variables
}
```

#### Notable Variables

| Variable | Address | Description |
|----------|---------|-------------|
| m_heatsinkTemperature_9_7 | 0xa2d2 | Heatsink temperature |
| m_cmpHeatsinkMaxTemp_9_7 | 0xa2a2 | Compressor heatsink max temp |
| m_SST_raw_x10Celsius | 0xa26c | Suction superheat temp |
| DefrostData.ActivationData.R_20_12 | 0x2a7f | Defrost R value |

---

### 4.4 OVERRIDE.py - Override Flags

**Location:** `extracted/kt12/.../OVERRIDE.py`

#### Bit Flag Definitions

```python
COMPRESSOR_SILENT_MODE = 1      # bit 0 (0x0001)
EM = 2                          # bit 1 (0x0002)
OAT = 4                         # bit 2 (0x0004)
THR = 8                         # bit 3 (0x0008)
WMAX = 16                       # bit 4 (0x0010)
FREEZE = 32                     # bit 5 (0x0020)
HIGH_TD = 64                    # bit 6 (0x0040)
HIGH_SDT = 128                  # bit 7 (0x0080)
LOW_SST = 256                   # bit 8 (0x0100)
IMAX_INPUT = 512                # bit 9 (0x0200)
IMAX_OUTPUT = 1024              # bit 10 (0x0400)
COMPRESSOR_HEATSINK = 2048      # bit 11 (0x0800)
FAN_SILENT_MODE = 4096          # bit 12 (0x1000)
FAN_HEATSINK = 8192             # bit 13 (0x2000)
COMPRESSOR_HEATER_HEATSINK = 16384  # bit 14 (0x4000)
CMP_MIN_FREQUENCY_OAT = 32768   # bit 15 (0x8000)
```

---

### 4.5 FILE_INIT.py - Device Initialization Data

**Location:** `extracted/kt12/.../FILE_INIT.py`
**Size:** Very large (~5,000+ lines)

#### Purpose
Contains default initialization values for all supported CTRL_BOX_IDs.

#### Sample Data (MINI2_5KW - ID 112)

```python
{
    "FANHMAX": 2300,
    "FANCMAX": 2300,
    "FANCMIN": 400,
    # ... many more parameters
}
```

#### FANHMAX/FANCMAX Values by Device

| Device | FANHMAX | FANCMAX | FANCMIN |
|--------|---------|---------|---------|
| PCM5_XS_1ph (104) | 650 | 650 | 50 |
| PCM5_S_1ph (105) | 1000 | 1000 | 50 |
| MINI2_5KW (112) | 2300 | 2300 | 400 |
| WOLF devices | 1000 | 1000 | 200 |

---

### 4.6 LAB_MODE.py - Lab Mode Configuration

**Location:** `extracted/kt12/.../LAB_MODE.py`

```python
ALGORITHM_FANABS = 1
ALGORITHMS = [ALGORITHM_FANABS]
```

---

## 5. pymtstestlib Analysis

### 5.1 Available Information

**setup.py contents:**
```python
setup(
    name='pymtstestlib',
    version='00.00.06',
    packages=find_packages(include=['pymtstestlib', 'pymtstestlib.*']),
    description='Python MTSTestLib library porting',
    author='Luca Santini Phoenix S.c.p.a',
    install_requires=['pyserial>=3.0'],
)
```

### 5.2 Expected API (from TestLib imports)

```python
from pymtstestlib.api import API
from pymtstestlib.shared.error_defs import EErrors
from pymtstestlib.shared.export_defs import ESetupStatus
```

### 5.3 Known API Methods (from usage)

| Method | Description |
|--------|-------------|
| `CommOpen(port, baudrate)` | Open COM port |
| `CommClose()` | Close COM port |
| `system_startup_from_file(fwprj)` | Initialize from .fwprj |
| `ReadDGTO(dgto_address)` | Read DGTO value |
| `WriteDGTO(dgto_address, value)` | Write DGTO value |
| `TDAReadInfo()` | Read Test Data Area |
| `TDAWriteInfo(code, info)` | Write Test Data Area |
| `TDARegisterTest(flag)` | Register TDA test |
| `DflsMapDownload(file, factory_code)` | Download DFLS file |
| `GetDownloadInfo()` | Get download status |
| `ErrorHistoryRead(start, count)` | Read error history |
| `ErrorHistoryReset()` | Clear error history |
| `ReadPSoleFwAttr()` | Read firmware attributes (Ares5) |

### 5.4 CRITICAL: Source Code Missing

The `pymtstestlib` package source code is **NOT included** in the repository. Only the setup.py file exists, which references:
- `pymtstestlib/__init__.py`
- `pymtstestlib/api.py`
- `pymtstestlib/shared/error_defs.py`
- `pymtstestlib/shared/export_defs.py`
- `pymtstestlib/shared/utils.py`

**These files must be obtained separately.**

---

## 6. Component Relationships

### 6.1 Dependency Graph

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER TEST SCRIPT                         │
└─────────────────────────────────────────────────────────────────┘
                                   │
                 ┌─────────────────┴─────────────────┐
                 │                                   │
                 ▼                                   ▼
    ┌────────────────────┐              ┌────────────────────┐
    │   TDM_Manager.py   │              │    TestLib.py      │
    │   (TDM4 Project)   │─────uses────▶│  (Core Framework)  │
    │      v0.6.0        │              │      v2.2.2        │
    └────────────────────┘              └────────────────────┘
              │                                   │
    ┌─────────┴─────────┐               ┌────────┴────────┐
    │                   │               │                 │
    ▼                   ▼               ▼                 ▼
┌──────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐
│CTRL_BOX  │    │  RAM_VAR  │    │  Report   │    │  FWPRJ    │
│LAB_MODE  │    │  OVERRIDE │    │           │    │ Ares5Env  │
│FILE_INIT │    │           │    │           │    │           │
└──────────┘    └───────────┘    └───────────┘    └───────────┘
                                       │                 │
                                       │                 │
                                       ▼                 ▼
                                ┌───────────┐    ┌───────────┐
                                │  openpyxl │    │   .fwprj  │
                                │  pandas   │    │  Env.XML  │
                                └───────────┘    └───────────┘

                    ALL PATHS LEAD TO:
                           │
                           ▼
              ┌────────────────────────┐
              │     pymtstestlib       │
              │    (MISSING SOURCE)    │
              └────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │      pyserial          │
              │   (Serial/COM Port)    │
              └────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   PHYSICAL HARDWARE    │
              │   (TDM4 Device)        │
              └────────────────────────┘
```

### 6.2 Import Path Requirements

**TDM_Manager expects this structure:**
```
project_root/
├── classes/
│   ├── CTRL_BOX_ID.py
│   ├── LAB_MODE.py
│   ├── RAM_VAR.py
│   ├── OVERRIDE.py
│   └── FILE_INIT.py
├── libs/
│   ├── TestLib.py
│   ├── Report.py
│   ├── ConfigParser.py
│   ├── FWPRJ.py
│   ├── Ares5Env.py
│   └── Inverter_APIs.py    # MISSING!
├── configs/
│   ├── Config.py
│   └── Config.txt
└── pymtstestlib/           # MISSING!
    ├── api.py
    └── shared/
```

---

## 7. OTA Test Script Evaluation

### 7.1 Script Overview

The user's OTA test script implements **Pablo's 14-step test sequence** for TDM4 devices.

### 7.2 Script Architecture

```python
# Direct API usage (bypasses TestLib)
from pymtstestlib.api import API
from pymtstestlib.shared.error_defs import EErrors
from pymtstestlib.shared.export_defs import SMapDGTO
from pymtstestlib.shared.utils import SWAP

api = API()
api.CommOpen(COM_PORT, BAUDRATE)
api.system_startup_from_file(FWPRJ)
```

### 7.3 Step-by-Step Evaluation

| Step | Description | Script Implementation | Evaluation |
|------|-------------|----------------------|------------|
| 1 | SW Download | SKIPPED | ✓ Correct (no method) |
| 2 | Write/Read TDA | `TDAWriteInfo`, `TDAReadInfo` | ⚠️ TDA format may be wrong |
| 3-6 | DFLS Download | `DflsMapDownload` | ⚠️ Timeout may be too short |
| 7 | Device Info | `ReadPSoleFwAttr` + fallback | ⚠️ Ares5-specific method |
| 8-9 | Write ADJ DGTOs | Direct `WriteDGTO` | ❌ Hardcoded codes |
| 10 | Send Reset | `ErrorHistoryReset` | ✓ Correct |
| 11 | Read Back DGTOs | Direct `ReadDGTO` | ❌ Depends on Step 8-9 |
| 12 | (Unknown) | SKIPPED | - |
| 13 | Fault History | `ErrorHistoryRead` + fallback | ⚠️ May not be supported |
| 14 | PSM-Status Loop | Direct `ReadDGTO` | ⚠️ DGTO code may be wrong |

### 7.4 Identified Issues in Script

#### Issue 1: Hardcoded DGTO Codes

```python
# Script uses hardcoded codes:
DGTO_PSM_STATUS = dgto("4-11-6-25")
DGTO_FAULT_CODE = dgto("5-1-2-3")
DGTO_TDM_STATUS = dgto("10-0-6-22")

ADJ_DGTOS = [
    ("FANHMAX", dgto("10-0-2-24"), 1500),
    ("FANCMAX", dgto("10-0-2-26"), 1400),
    ("FANCMIN", dgto("10-0-2-27"), 400),
    ("TDM_EH_Enable", dgto("2-3-0-28"), 1),
]
```

**Problem:** DGTO codes vary by:
- Firmware version
- Device model (CTRL_BOX_ID)
- .fwprj file version

**Solution:** Use TestLib which looks up codes from .fwprj by NAME.

#### Issue 2: Values May Exceed Device Limits

```python
("FANHMAX", ..., 1500),  # Writing 1500
```

**But FILE_INIT.py shows:**
- PCM5_XS_1ph: FANHMAX = 650 (max)
- PCM5_S_1ph: FANHMAX = 1000 (max)
- MINI2_5KW: FANHMAX = 2300 (max)

**Problem:** Value 1500 exceeds limits for some devices.

#### Issue 3: Missing Device State Management

```python
# Script directly writes DGTOs without checking device state
api.WriteDGTO(dgto_val, test_value)
```

**Problem:** Many DGTOs are read-only unless device is in:
- LAB_MODE
- STANDBY state
- Specific operating state

#### Issue 4: TDA Format

```python
TDA_TEST_VALUE = "121212121212"  # 12 hex chars
```

**Framework uses:**
```python
TDA_TestAutomation = "60ff8000df12"  # Known working format
```

#### Issue 5: Insufficient Timing

```python
time.sleep(2)  # After operations
```

**Framework uses:**
```python
HEAT_COOLING_TIMER = 80  # 80 seconds for state transitions
PING_DEFAULT_TIMER = 30  # 30 seconds for value wait
```

### 7.5 API Method Compatibility

| Script Method | TestLib Equivalent | Notes |
|---------------|-------------------|-------|
| `api.ReadDGTO(code)` | `testlib.read_dgto(name)` | TestLib uses names |
| `api.WriteDGTO(code, val)` | `testlib.write_dgto(name, val)` | TestLib verifies |
| `api.TDAReadInfo()` | `testlib.ReadTDA()` | Wrapped method |
| `api.TDAWriteInfo()` | `testlib.WriteTDA()` | Wrapped method |
| `api.ErrorHistoryReset()` | (same) | Direct API |
| `api.ErrorHistoryRead()` | (same) | Direct API |
| N/A | `testlib.ping_dgto()` | Wait for value |
| N/A | `testlib.set_lab_mode_active()` | Via TDM_Manager |

---

## 8. Identified Issues & Gaps

### 8.1 Critical Missing Components

| Component | Impact | Required Action |
|-----------|--------|-----------------|
| pymtstestlib source | Cannot run anything | Obtain from Ariston |
| Inverter_APIs.py | TDM_Manager fails | Obtain from Ariston |
| .fwprj files | No DGTO lookup | Obtain for target device |
| Env.XML | No Ares5 support | Obtain if using Ares5 |
| Probe Excel files | Probe writes fail | Obtain for probes |

### 8.2 Version Mismatches

| Component | Expected | Actual | Impact |
|-----------|----------|--------|--------|
| TestLib | v1.8.0 | v2.2.2 | Warning at startup |
| pymtstestlib | v00.05.00+ | v00.00.06 | Unknown |

### 8.3 Structural Issues

1. **Scattered Files:** Code split across multiple ZIPs
2. **Wrong Import Paths:** TDM4 classes expect different structure
3. **No Package Structure:** Missing `__init__.py` in key locations
4. **Duplicate Patterns:** Similar code in multiple places

### 8.4 Documentation Gaps

1. No API documentation for pymtstestlib
2. No DGTO code reference guide
3. Limited comments in complex methods
4. TDM_Manager_SWSpecifications_1v9.docx not analyzed (binary)

---

## 9. Recommendations

### 9.1 Immediate Actions

1. **Obtain Missing Files:**
   - pymtstestlib source code
   - Inverter_APIs.py
   - Target device .fwprj file
   - Env.XML (if Ares5)

2. **Reorganize Repository:**
   ```
   testauto/
   ├── libs/           # Merge from kt10
   ├── classes/        # Rename from kt12
   ├── configs/
   ├── pymtstestlib/   # Add source
   └── tests/          # User test scripts
   ```

3. **Fix Import Paths:**
   - Update TDM_Manager imports
   - Create proper `__init__.py` files

### 9.2 For OTA Test Script

1. **Use TestLib Instead of Direct API:**
   ```python
   from libs.TestLib import TestLib
   from configs.Config import device_config

   testlib = TestLib(device_config)
   value = testlib.read_dgto("FANHMAX")  # By name
   ```

2. **Add Device State Management:**
   ```python
   from classes.TDM_Manager import TDMManager

   tdm = TDMManager(settings)
   tdm.set_standby()  # Ensure proper state
   tdm.set_lab_mode_active()  # Enable writes
   ```

3. **Use Device-Specific Limits:**
   ```python
   from classes.FILE_INIT import get_init_values
   from classes.CTRL_BOX_ID import MINI2_5KW

   limits = get_init_values(MINI2_5KW)
   max_fan = limits["FANHMAX"]  # Device-specific
   ```

4. **Add Proper Timing:**
   ```python
   # After reset
   time.sleep(10)  # Not 2

   # For state transitions
   testlib.ping_dgto("TDM - Status", expected_state, timeout=80)
   ```

### 9.3 Long-Term Improvements

1. Create unified test framework package
2. Add comprehensive logging
3. Create DGTO reference documentation
4. Implement device auto-detection
5. Add unit tests for framework

---

## Appendix A: File Checksums

| File | Size | Lines |
|------|------|-------|
| TestLib.py | ~100KB | ~2,800 |
| TDM_Manager.py | ~70KB | ~1,800 |
| Report.py | ~10KB | ~302 |
| ConfigParser.py | ~2KB | ~66 |
| FWPRJ.py | ~6KB | ~195 |
| Ares5Env.py | ~20KB | ~631 |
| RAM_VAR.py | ~15KB | ~493 |
| CTRL_BOX_ID.py | ~1KB | ~38 |
| FILE_INIT.py | ~150KB | ~5,000+ |

---

## Appendix B: DGTO Code Reference

### Common DGTOs (from TDM_Manager usage)

| Name | Likely Code | Description |
|------|-------------|-------------|
| TDM - Status | 10-0-6-22 | TDM state machine status |
| Generator External Request | 15-7-2-4 | Command to change state |
| FANHMAX | 10-0-2-24 | Fan max heating RPM |
| FANCMAX | 10-0-2-26 | Fan max cooling RPM |
| FANCMIN | 10-0-2-27 | Fan min RPM |
| PSM-Status | 4-11-6-25 | Power supply module status |
| Fault_Code | 5-1-2-3 | Current fault code |

**Note:** These codes may vary by firmware version. Always verify against .fwprj file.

---

*End of Analysis Report*
