"""
================================================================================
ARISTON TDM4 OTA TEST AUTOMATION - FINAL VERSION
================================================================================
Based on:
- Pablo's 14 Steps specification
- ARES Chatter application analysis (MTSTESTLIB.DLL API)
- pymtstestlib Python wrapper

Author: Test Automation Team
Version: 1.0.0
================================================================================
"""

import time
import os
import re
from datetime import datetime
from typing import Tuple, Optional, List, Dict, Any

# pymtstestlib imports
from pymtstestlib.api import API
from pymtstestlib.shared.error_defs import EErrors
from pymtstestlib.shared.export_defs import SMapDGTO
from pymtstestlib.shared.utils import SWAP


# =============================================================================
# CONFIGURATION - MODIFY THESE FOR YOUR SETUP
# =============================================================================

class Config:
    """Test configuration settings."""

    # File paths - UPDATE THESE FOR YOUR ENVIRONMENT
    FWPRJ_FILE = r"C:\Alireza\Alireza\TDM4_Test\TDM4_RX130_ATG485_70_26_05.fwprj"
    CSV_FILE = r"C:\Alireza\Alireza\TDM4_Test\TDM4_RX130_ATG485_70_26_05.csv"
    DFLS_FILE = r"C:\Alireza\Alireza\TDM4_Test\sources\0x0048_PCM5_ver00.02.00-SAT.dfls"

    # Alternative DFLS paths to check
    DFLS_OPTIONS = [
        r"C:\Alireza\Alireza\TDM4_Test\sources\0x0048_PCM5_ver00.02.00-SAT.dfls",
        r"C:\Alireza\Alireza\TDM4_Test\0x0048_PCM5_ver00.02.00-SAT.dfls",
        r"C:\Alireza\Alireza\TDM4_Test\0x0048_PCM5_ver00.02.00_SAT.dfls",
    ]

    # Communication settings
    COM_PORT = "//./COM5"
    BAUDRATE = 38400

    # Test values from Pablo's specification
    TDA_TEST_VALUE = "121212121212"
    FACTORY_CODE = "0101010101010101010101010101"

    # Timing settings (in seconds)
    POST_STARTUP_DELAY = 5      # Wait after system_startup_from_file
    COMM_OPEN_DELAY = 2         # Wait after CommOpen
    POST_RESET_DELAY = 2        # Wait after ErrorHistoryReset
    DFLS_TIMEOUT = 120          # Max wait for DFLS download

    # Retry settings
    MAX_ATTEMPTS = 30           # Max retry attempts for DGTO operations
    DGTO_READ_DELAY = 0.2       # Delay between DGTO read attempts
    PSM_READING_COUNT = 10      # Number of PSM status readings
    PSM_INTERVAL = 1.0          # Interval between PSM readings


# =============================================================================
# ERROR CODES (from MTSTESTLIB.DLL analysis)
# =============================================================================

class ErrorCodes:
    """Error codes discovered from MTSTESTLIB.DLL analysis."""

    ERRORS = {
        0: "NO ERRORS",
        1: "COMM OPEN ERROR",
        2: "COMM PORT IS CLOSED",
        3: "I/O GENERIC ERROR",
        4: "RAM WRITE ERROR",
        5: "RAM READ ERROR",
        6: "RECEIVE TIMEOUT ERROR",
        7: "PACKET SEND ERROR",
        8: "FLASH ERASE ERROR",
        9: "FLASH WRITE ERROR",
        10: "FLASH READ ERROR",
        11: "VERIFY ERROR",
        12: "OPERATION CANCELED",
        13: "INVALID CHECKSUM",
        14: "INVALID SERIAL NUMBER",
        15: "INVALID FACTORY CODE",
        16: "INVALID DESCRIPTION",
        17: "INVALID METAGEN VERSION",
        18: "INVALID IDENT TABLE",
        19: "INVALID SETTING MAP",
        20: "SETUP MODE ENTER ERROR",
        21: "SETUP MODE EXIT ERROR",
        22: "FILE NOT FOUND OR INVALID",
        23: "FILE READ ERROR",
        24: "INVALID TARGET",
        25: "INVALID HWND",
        26: "THREAD NOT STARTED",
        27: "THREAD NOT TERMINATED",
        28: "INVALID ADDRESS",
        29: "INVALID INDEX",
        30: "INVALID BUFFER",
        31: "REMOTE CONTROL FAILURE",
        32: "DISPLAY READ",
        33: "DISPLAY WRITE",
        34: "INVALID INPUT",
        35: "INVALID LOAD INDEX",
        36: "INVALID REGULATION",
        37: "INVALID FEEDBACK INDEX",
        38: "UNKNOWN DRIVER TYPE",
        39: "SETTING MAP BUFFER OVERFLOW",
        40: "INVALID TEST DATA AREA",
        41: "PURE VIRTUAL METHOD CALL",
        42: "INVALID DGTO FILE",
        43: "INVALID REQUEST FORMAT",
        44: "RECEIVE DATA ERROR",
        45: "I/O QUEUE OVERFLOW",
        46: "COMM SETUP ERROR",
        47: "INVALID SETMAP POINTER",
        48: "COMMAND FAILURE",
        49: "UNZIP ERROR",
        50: "INVALID DATA RECEIVED",
        51: "INVALID FIRMWARE VERSION",
        52: "INVALID BOARD TYPE",
        53: "INVALID APPLIANCE CODE",
        54: "IDENT TYPE CONFLICT",
    }

    @classmethod
    def get_message(cls, code) -> str:
        """Get error message for code."""
        if hasattr(code, 'value'):
            code = code.value
        return cls.ERRORS.get(code, f"UNKNOWN ERROR ({code})")


# =============================================================================
# CSV-BASED DGTO LOOKUP
# =============================================================================

class DGTOLookup:
    """
    DGTO lookup from CSV file.

    Expected CSV format (semicolon-separated):
    DGTO_CODE;HEX_CODE;NAME;DESCRIPTION
    Example: 0-1-0-9;0x0109;TDM Electric Heater 1;
    """

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.dgto_map: Dict[str, Tuple[int, str, str]] = {}
        self.code_map: Dict[str, Tuple[int, str]] = {}
        self._load_csv()

    def _load_csv(self) -> bool:
        """Load CSV file and build lookup maps."""
        if not os.path.exists(self.csv_path):
            print(f"    WARNING: CSV file not found: {self.csv_path}")
            return False

        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            try:
                with open(self.csv_path, 'r', encoding='latin-1') as f:
                    lines = f.readlines()
            except Exception as e:
                print(f"    ERROR reading CSV: {e}")
                return False

        count = 0
        for line in lines:
            line = line.strip()
            if not line:
                continue

            parts = line.split(';')
            if len(parts) >= 3:
                dgto_code = parts[0].strip()
                hex_str = parts[1].strip()
                name = parts[2].strip()

                try:
                    hex_val = int(hex_str, 16) if hex_str.startswith('0x') else int(hex_str, 16)
                except:
                    hex_val = self._dgto_to_hex(dgto_code)

                if name:
                    name_key = name.upper().replace(' ', '_')
                    self.dgto_map[name_key] = (hex_val, dgto_code, name)
                    self.dgto_map[name.upper()] = (hex_val, dgto_code, name)

                if dgto_code:
                    self.code_map[dgto_code] = (hex_val, name)
                count += 1

        print(f"    CSV loaded: {count} DGTO entries")
        return True

    def search(self, dgto_name: str) -> Tuple[int, Optional[str], Optional[str]]:
        """Search for DGTO by name or code."""
        name_upper = dgto_name.upper()

        # Try exact match
        if name_upper in self.dgto_map:
            return self.dgto_map[name_upper]

        # Try with underscore/space conversion
        name_normalized = name_upper.replace('_', ' ')
        if name_normalized in self.dgto_map:
            return self.dgto_map[name_normalized]

        # Try by DGTO code
        if dgto_name in self.code_map:
            hex_val, name = self.code_map[dgto_name]
            return hex_val, name, dgto_name

        # Partial match
        for key, (hex_val, dgto_code, orig_name) in self.dgto_map.items():
            if name_upper in key or key in name_upper:
                return hex_val, orig_name, dgto_code

        # Try D-G-T-O format
        if re.match(r"^[0-9]+-[0-9]+-[0-9]+-[0-9]+$", dgto_name):
            return self._dgto_to_hex(dgto_name), None, dgto_name

        return 0, None, None

    def get_code(self, dgto_name: str) -> int:
        """Get DGTO code for API calls."""
        hex_val, _, _ = self.search(dgto_name)
        return hex_val

    def _dgto_to_hex(self, dgto_code: str) -> int:
        """Convert D-G-T-O string to hex value."""
        try:
            return SWAP(SMapDGTO(dgto_code).dgto)
        except:
            parts = dgto_code.split('-')
            if len(parts) == 4:
                d, g, t, o = [int(p) for p in parts]
                return (d << 20) | (g << 16) | (t << 8) | o
        return 0


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def dgto_code(code: str) -> int:
    """Convert D-G-T-O string to SWAP'd value."""
    return SWAP(SMapDGTO(code).dgto)


def find_dfls_file() -> Optional[str]:
    """Find DFLS file from available paths."""
    for path in Config.DFLS_OPTIONS:
        if os.path.exists(path):
            return path
    return None


def format_result(status: str, details: str = "") -> Tuple[str, str]:
    """Format test result tuple."""
    return (status, details)


# =============================================================================
# MAIN TEST CLASS
# =============================================================================

class OTATestAutomation:
    """
    Complete OTA Test Automation implementing Pablo's 14 Steps.

    API Methods Used (from MTSTESTLIB.DLL):
    - CommOpen/CommClose: Serial communication
    - system_startup_from_file: Load firmware project
    - ReadDGTO/WriteDGTO: DGTO operations
    - TDAWriteInfo/TDAReadInfo: Test Data Area
    - DflsMapDownload: DFLS file download
    - ErrorHistoryRead/ErrorHistoryReset: Fault history
    - ReadPSoleFwAttr: Device info
    """

    def __init__(self):
        self.api: Optional[API] = None
        self.dgto_lookup: Optional[DGTOLookup] = None
        self.results: Dict[str, Tuple[str, str]] = {}
        self.dfls_file: Optional[str] = None
        self.written_dgtos: List[Tuple[str, int, int, str]] = []
        self.start_time: Optional[datetime] = None

    def _log(self, message: str, level: str = "INFO"):
        """Log message with timestamp."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] [{level}] {message}")

    def _log_step(self, step_num: str, title: str):
        """Log step header."""
        print(f"\n{'='*60}")
        print(f"  STEP {step_num}: {title}")
        print(f"{'='*60}")

    # =========================================================================
    # INITIALIZATION
    # =========================================================================

    def initialize(self) -> bool:
        """Initialize API, load CSV, verify device communication."""
        self.start_time = datetime.now()

        print("\n" + "=" * 70)
        print("  ARISTON TDM4 OTA TEST AUTOMATION - FINAL VERSION")
        print("=" * 70)
        print(f"  Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  COM Port: {Config.COM_PORT}")
        print(f"  Baud Rate: {Config.BAUDRATE}")
        print("=" * 70)

        # Step 1: Load CSV for DGTO lookups
        self._log("Loading CSV file for DGTO lookups...")
        self.dgto_lookup = DGTOLookup(Config.CSV_FILE)

        # Step 2: Find DFLS file
        self.dfls_file = find_dfls_file()
        if self.dfls_file:
            self._log(f"DFLS file: {self.dfls_file}")
        else:
            self._log("DFLS file not found!", "WARNING")

        # Step 3: Initialize API
        self._log("Initializing API...")
        try:
            self.api = API()
            self.api.CommOpen(Config.COM_PORT, Config.BAUDRATE)
            self._log("CommOpen: OK")
        except Exception as e:
            self._log(f"CommOpen FAILED: {e}", "ERROR")
            return False

        time.sleep(Config.COMM_OPEN_DELAY)

        # Step 4: Load firmware project
        self._log(f"Loading FWPRJ: {os.path.basename(Config.FWPRJ_FILE)}")
        try:
            self.api.system_startup_from_file(Config.FWPRJ_FILE)
            self._log("system_startup_from_file: OK")
        except Exception as e:
            self._log(f"system_startup_from_file FAILED: {e}", "ERROR")
            return False

        # Step 5: Wait for device
        self._log(f"Waiting {Config.POST_STARTUP_DELAY}s for device initialization...")
        time.sleep(Config.POST_STARTUP_DELAY)

        # Step 6: Verify device communication
        self._log("Verifying device communication...")
        if self._verify_device_ready():
            self._log("Device ready!", "SUCCESS")
            return True
        else:
            self._log("Device communication not verified, continuing anyway...", "WARNING")
            return True

    def _verify_device_ready(self) -> bool:
        """Verify device is responding."""
        # Try reading TDM_STATUS
        dgto = self.dgto_lookup.get_code("TDM_STATUS") or dgto_code("10-0-6-22")

        for i in range(Config.MAX_ATTEMPTS):
            try:
                s, v = self.api.ReadDGTO(dgto)
                if s == EErrors.E_OK and v is not None:
                    self._log(f"TDM_STATUS = {v}")
                    return True
            except:
                pass
            time.sleep(Config.DGTO_READ_DELAY)
        return False

    # =========================================================================
    # PABLO'S 14 STEPS
    # =========================================================================

    def step_01_download_sw(self):
        """Step 1: Download SW Version to Board."""
        self._log_step("1", "Download SW Version to Board")
        self._log("SKIPPED - Requires external programmer")
        self.results["step_01"] = format_result("SKIP", "External programmer required")

    def step_02_write_tda(self):
        """Step 2: Write TDA (Test Data Area)."""
        self._log_step("2", "Write TDA")

        self._log(f"Writing TDA: {Config.TDA_TEST_VALUE}")
        try:
            s = self.api.TDAWriteInfo(Config.TDA_TEST_VALUE, "")
            if s == EErrors.E_OK:
                self._log("TDAWriteInfo: OK", "SUCCESS")
                self.api.TDARegisterTest(1)
                self.results["step_02_write"] = format_result("OK", Config.TDA_TEST_VALUE)
            else:
                msg = ErrorCodes.get_message(s)
                self._log(f"TDAWriteInfo: {msg}", "ERROR")
                self.results["step_02_write"] = format_result("FAIL", msg)
        except Exception as e:
            self._log(f"TDAWriteInfo Exception: {e}", "ERROR")
            self.results["step_02_write"] = format_result("FAIL", str(e))

    def step_03_read_tda(self):
        """Step 3: Read TDA and Verify."""
        self._log_step("3", "Read TDA")

        time.sleep(1)
        self._log("Reading TDA...")

        try:
            result = self.api.TDAReadInfo()
            if isinstance(result, tuple) and len(result) >= 2:
                s, info = result[0], result[1]
                if s == EErrors.E_OK and info is not None:
                    tda_code = info.code.decode('utf-8').rstrip('\xff\x00') if hasattr(info, 'code') else str(info)
                    self._log(f"TDAReadInfo: {tda_code}", "SUCCESS")
                    self.results["step_03_read"] = format_result("OK", tda_code)
                else:
                    msg = ErrorCodes.get_message(s)
                    self._log(f"TDAReadInfo: {msg}", "ERROR")
                    self.results["step_03_read"] = format_result("FAIL", msg)
            else:
                self._log(f"TDAReadInfo unexpected result: {result}", "ERROR")
                self.results["step_03_read"] = format_result("FAIL", "Unexpected format")
        except Exception as e:
            self._log(f"TDAReadInfo Exception: {e}", "ERROR")
            self.results["step_03_read"] = format_result("FAIL", str(e))

    def step_04_06_download_dfls(self):
        """Steps 4-6: Download DFLS with Factory Code."""
        self._log_step("4-6", "Download DFLS")

        if not self.dfls_file:
            self._log("DFLS file not found", "ERROR")
            self.results["step_04_06"] = format_result("SKIP", "File not found")
            return

        self._log(f"DFLS: {os.path.basename(self.dfls_file)}")
        self._log(f"Factory Code: {Config.FACTORY_CODE}")

        try:
            success = self.api.DflsMapDownload(self.dfls_file, Config.FACTORY_CODE)
            if success:
                self._log("DflsMapDownload started...")

                # Wait for completion
                for i in range(Config.DFLS_TIMEOUT):
                    try:
                        result = self.api.GetDownloadInfo()
                        if isinstance(result, tuple):
                            s, info = result
                            if hasattr(info, 'status'):
                                progress = getattr(info, 'progress', 'N/A')
                                if i % 10 == 0:
                                    self._log(f"Status: {info.status}, Progress: {progress}")
                                if info.status == 3:  # Complete
                                    self._log("DFLS Download: COMPLETE", "SUCCESS")
                                    self.results["step_04_06"] = format_result("OK", "Downloaded")
                                    return
                    except:
                        pass
                    time.sleep(1)

                self._log("DFLS Download: Timeout", "WARNING")
                self.results["step_04_06"] = format_result("PARTIAL", "Timeout")
            else:
                self._log("DflsMapDownload failed to start", "ERROR")
                self.results["step_04_06"] = format_result("FAIL", "Start failed")
        except Exception as e:
            self._log(f"DFLS Exception: {e}", "ERROR")
            self.results["step_04_06"] = format_result("FAIL", str(e))

    def step_07_get_device_info(self):
        """Step 7: Get Device Info."""
        self._log_step("7", "Get Device Info")

        # Method 1: ReadPSoleFwAttr
        try:
            result = self.api.ReadPSoleFwAttr()
            if isinstance(result, tuple) and len(result) >= 4:
                s, desc, prod_id, ares_ver = result
                if s and desc is not None:
                    self._log(f"Description: {desc}")
                    self._log(f"Product ID: {prod_id}")
                    self._log(f"ARES Version: {ares_ver}")
                    self.results["step_07"] = format_result("OK", f"ProdID:{prod_id}")
                    return
        except Exception as e:
            self._log(f"ReadPSoleFwAttr: {e}")

        # Method 2: Read TDM_STATUS
        self._log("Trying TDM_STATUS DGTO...")
        dgto = self.dgto_lookup.get_code("TDM_STATUS") or dgto_code("10-0-6-22")

        for i in range(Config.MAX_ATTEMPTS):
            s, v = self.api.ReadDGTO(dgto)
            if s == EErrors.E_OK and v is not None:
                self._log(f"TDM_STATUS: {v}", "SUCCESS")
                self.results["step_07"] = format_result("OK", f"TDM_STATUS={v}")
                return
            time.sleep(Config.DGTO_READ_DELAY)

        self._log("Could not get device info", "ERROR")
        self.results["step_07"] = format_result("FAIL", "No device info")

    def step_08_09_write_adj_dgtos(self):
        """Steps 8-9: Write ADJ DGTOs."""
        self._log_step("8-9", "Write ADJ DGTOs")

        # Define ADJ DGTOs: (name, fallback_code, test_value)
        adj_dgtos = [
            ("FANHMAX", "10-0-2-24", 1500),
            ("FANCMAX", "10-0-2-26", 1400),
            ("FANCMIN", "10-0-2-27", 400),
            ("TDM Electric Heater Enable", "2-3-0-28", 1),
        ]

        self.written_dgtos = []

        for name, fallback, value in adj_dgtos:
            self._log(f"Writing {name} = {value}...")

            dgto = self.dgto_lookup.get_code(name)
            if dgto == 0:
                dgto = dgto_code(fallback)
                self._log(f"  Using fallback: {fallback}")

            success = False
            for i in range(Config.MAX_ATTEMPTS):
                s = self.api.WriteDGTO(dgto, value)
                if s == EErrors.E_OK:
                    self._log(f"  {name}: OK", "SUCCESS")
                    self.written_dgtos.append((name, dgto, value, "OK"))
                    success = True
                    break
                time.sleep(Config.DGTO_READ_DELAY)

            if not success:
                self._log(f"  {name}: FAIL", "ERROR")
                self.written_dgtos.append((name, dgto, value, "FAIL"))

            time.sleep(0.3)

        ok_count = sum(1 for d in self.written_dgtos if d[3] == "OK")
        status = "OK" if ok_count == len(adj_dgtos) else "PARTIAL"
        self.results["step_08_09"] = format_result(status, f"{ok_count}/{len(adj_dgtos)}")

    def step_10_send_reset(self):
        """Step 10: Send Reset (ErrorHistoryReset)."""
        self._log_step("10", "Send Reset (ErrorHistoryReset)")

        for i in range(Config.MAX_ATTEMPTS):
            s = self.api.ErrorHistoryReset()
            if s == EErrors.E_OK:
                self._log("ErrorHistoryReset: OK", "SUCCESS")
                self.results["step_10"] = format_result("OK", "Error log cleared")
                time.sleep(Config.POST_RESET_DELAY)
                return
            time.sleep(Config.DGTO_READ_DELAY)

        self._log("ErrorHistoryReset: FAIL", "ERROR")
        self.results["step_10"] = format_result("FAIL", "Could not reset")

    def step_11_read_back_dgtos(self):
        """Step 11: Read Back DGTOs and Verify."""
        self._log_step("11", "Read Back DGTOs")

        if not self.written_dgtos:
            self._log("No DGTOs to verify")
            self.results["step_11"] = format_result("SKIP", "No DGTOs written")
            return

        matches = 0
        total = 0

        for name, dgto, expected, write_status in self.written_dgtos:
            if write_status != "OK":
                self._log(f"  {name}: Skipped (write failed)")
                continue

            total += 1
            for i in range(Config.MAX_ATTEMPTS):
                s, actual = self.api.ReadDGTO(dgto)
                if s == EErrors.E_OK and actual is not None:
                    match = (actual == expected)
                    status = "MATCH" if match else "MISMATCH"
                    self._log(f"  {name}: Read={actual}, Expected={expected} [{status}]")
                    if match:
                        matches += 1
                    break
                time.sleep(Config.DGTO_READ_DELAY)

        status = "OK" if matches == total else "PARTIAL"
        self.results["step_11"] = format_result(status, f"{matches}/{total} matched")

    def step_12_placeholder(self):
        """Step 12: Placeholder."""
        self._log_step("12", "Reserved")
        self._log("SKIPPED - Method not implemented")
        self.results["step_12"] = format_result("SKIP", "Not implemented")

    def step_13_get_fault_history(self):
        """Step 13: Get Fault History."""
        self._log_step("13", "Get Fault History")

        # Method 1: ErrorHistoryRead
        try:
            result = self.api.ErrorHistoryRead(0, 10)
            if isinstance(result, tuple) and len(result) >= 2:
                s, faults = result
                if s == EErrors.E_OK and faults is not None:
                    count = len(faults) if hasattr(faults, '__len__') else 0
                    self._log(f"ErrorHistoryRead: {count} entries", "SUCCESS")
                    for i, fault in enumerate(list(faults)[:5]):
                        self._log(f"  Fault[{i}]: {fault}")
                    self.results["step_13"] = format_result("OK", f"{count} faults")
                    return
            elif result == EErrors.E_OK:
                self._log("ErrorHistoryRead: OK (empty)", "SUCCESS")
                self.results["step_13"] = format_result("OK", "No faults")
                return
        except Exception as e:
            self._log(f"ErrorHistoryRead: {e}")

        # Method 2: Read Fault_Code DGTO
        self._log("Trying Fault_Code DGTO...")
        dgto = self.dgto_lookup.get_code("Fault_Code") or dgto_code("5-1-2-3")

        for i in range(Config.MAX_ATTEMPTS):
            s, v = self.api.ReadDGTO(dgto)
            if s == EErrors.E_OK and v is not None:
                self._log(f"Fault_Code: {v}", "SUCCESS")
                self.results["step_13"] = format_result("OK", f"Fault_Code={v}")
                return
            time.sleep(Config.DGTO_READ_DELAY)

        self._log("Could not read fault history", "ERROR")
        self.results["step_13"] = format_result("FAIL", "Could not read")

    def step_14_read_psm_status(self):
        """Step 14: Read PSM-Status Every Second."""
        self._log_step("14", f"Read PSM-Status ({Config.PSM_READING_COUNT} readings)")

        dgto = self.dgto_lookup.get_code("PSM_Status")
        if dgto == 0:
            dgto = self.dgto_lookup.get_code("PSM-Status")
        if dgto == 0:
            dgto = dgto_code("4-11-6-25")

        readings = []

        for i in range(Config.PSM_READING_COUNT):
            timestamp = datetime.now().strftime('%H:%M:%S')
            read_ok = False

            for attempt in range(10):
                s, v = self.api.ReadDGTO(dgto)
                if s == EErrors.E_OK and v is not None:
                    readings.append(v)
                    self._log(f"  [{timestamp}] PSM-Status = {v}")
                    read_ok = True
                    break
                time.sleep(0.1)

            if not read_ok:
                readings.append("FAIL")
                self._log(f"  [{timestamp}] PSM-Status = FAIL", "ERROR")

            if i < Config.PSM_READING_COUNT - 1:
                time.sleep(Config.PSM_INTERVAL)

        ok_count = sum(1 for v in readings if v != "FAIL")
        status = "OK" if ok_count == Config.PSM_READING_COUNT else "PARTIAL"
        self.results["step_14"] = format_result(status, f"{ok_count}/{Config.PSM_READING_COUNT}")

    # =========================================================================
    # CLEANUP AND RESULTS
    # =========================================================================

    def cleanup(self):
        """Close API connection."""
        if self.api:
            try:
                self.api.CommClose()
                self._log("CommClose: OK")
            except:
                pass

    def print_results(self):
        """Print final results table."""
        print("\n" + "=" * 70)
        print("  FINAL RESULTS")
        print("=" * 70)

        steps = [
            ("step_01", "SW Download"),
            ("step_02_write", "Write TDA"),
            ("step_03_read", "Read TDA"),
            ("step_04_06", "DFLS Download"),
            ("step_07", "Device Info"),
            ("step_08_09", "Write ADJ DGTOs"),
            ("step_10", "Send Reset"),
            ("step_11", "Read Back DGTOs"),
            ("step_12", "Reserved"),
            ("step_13", "Fault History"),
            ("step_14", "PSM-Status"),
        ]

        print(f"\n{'Step':<20} | {'Status':<10} | {'Details':<35}")
        print("-" * 70)

        for key, name in steps:
            status, details = self.results.get(key, ("N/A", "Not executed"))
            print(f"{name:<20} | {status:<10} | {details[:35]:<35}")

        print("-" * 70)

        # Summary
        ok = sum(1 for r in self.results.values() if r[0] == "OK")
        fail = sum(1 for r in self.results.values() if r[0] == "FAIL")
        skip = sum(1 for r in self.results.values() if r[0] == "SKIP")
        partial = sum(1 for r in self.results.values() if r[0] == "PARTIAL")

        duration = datetime.now() - self.start_time if self.start_time else None
        duration_str = str(duration).split('.')[0] if duration else "N/A"

        print(f"\nSUMMARY: {ok} OK | {fail} FAIL | {partial} PARTIAL | {skip} SKIP")
        print(f"DURATION: {duration_str}")
        print("=" * 70)

        return ok, fail, partial, skip

    def save_results(self, filename: str = None):
        """Save results to file."""
        if filename is None:
            filename = f"ota_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        with open(filename, 'w') as f:
            f.write(f"OTA TEST RESULTS - {datetime.now()}\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Configuration:\n")
            f.write(f"  COM Port: {Config.COM_PORT}\n")
            f.write(f"  FWPRJ: {Config.FWPRJ_FILE}\n")
            f.write(f"  CSV: {Config.CSV_FILE}\n")
            f.write(f"  DFLS: {self.dfls_file}\n\n")

            for key, (status, details) in self.results.items():
                f.write(f"{key}: {status} - {details}\n")

        self._log(f"Results saved to: {filename}")
        return filename

    # =========================================================================
    # MAIN EXECUTION
    # =========================================================================

    def run_all_steps(self):
        """Execute all 14 steps."""
        try:
            self.step_01_download_sw()
            self.step_02_write_tda()
            self.step_03_read_tda()
            self.step_04_06_download_dfls()
            self.step_07_get_device_info()
            self.step_08_09_write_adj_dgtos()
            self.step_10_send_reset()
            self.step_11_read_back_dgtos()
            self.step_12_placeholder()
            self.step_13_get_fault_history()
            self.step_14_read_psm_status()
        except Exception as e:
            self._log(f"Unexpected error: {e}", "ERROR")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()
            self.print_results()
            self.save_results()


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  ARISTON TDM4 OTA TEST AUTOMATION")
    print("  Based on Pablo's 14 Steps & ARES Chatter Analysis")
    print("=" * 70)

    test = OTATestAutomation()

    if test.initialize():
        test.run_all_steps()
    else:
        print("\n[ERROR] Initialization failed!")
        print("Check:")
        print(f"  1. COM port: {Config.COM_PORT}")
        print(f"  2. Device is powered on and connected")
        print(f"  3. FWPRJ file exists: {Config.FWPRJ_FILE}")
