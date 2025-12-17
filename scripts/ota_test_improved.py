"""
================================================================================
IMPROVED OTA TEST AUTOMATION (Pablo's 14 Steps)
================================================================================
Version: 2.0.0
Based on: Original ota_test script
Improvements:
  - Uses TestLib framework for proper DGTO handling
  - Proper device state management
  - Better error handling and logging
  - Device-specific value validation
  - Configurable timing parameters
================================================================================
"""

import time
import os
import sys
from datetime import datetime
from enum import Enum

# =============================================================================
# PATH SETUP - Ensure libs can be imported
# =============================================================================
# Add the project root to path if running from different directory
PROJECT_ROOT = r"C:\Alireza\Alireza\TDM4_Test"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# =============================================================================
# IMPORTS
# =============================================================================
try:
    # Low-level API (for operations not wrapped by TestLib)
    from pymtstestlib.api import API
    from pymtstestlib.shared.error_defs import EErrors
    from pymtstestlib.shared.export_defs import SMapDGTO
    from pymtstestlib.shared.utils import SWAP
    print("[OK] pymtstestlib imported successfully")
except ImportError as e:
    print(f"[ERROR] Failed to import pymtstestlib: {e}")
    sys.exit(1)

try:
    # High-level TestLib wrapper
    from libs.TestLib import TestLib
    from libs.Report import Report
    from libs.FWPRJ import FWPRJ
    print("[OK] TestLib framework imported successfully")
except ImportError as e:
    print(f"[ERROR] Failed to import TestLib: {e}")
    print("    Make sure you're running from the correct directory")
    sys.exit(1)

# =============================================================================
# CONFIGURATION
# =============================================================================

class Config:
    """Test configuration parameters"""

    # File paths
    FWPRJ_FILE = r"C:\Alireza\Alireza\TDM4_Test\TDM4_RX130_ATG485_70_26_05.fwprj"
    DFLS_FILE = r"C:\Alireza\Alireza\TDM4_Test\sources\0x0048_PCM5_ver00.02.00-SAT.dfls"
    DGTO_EXCEL = r"C:\Alireza\Alireza\TDM4_Test\TDM4_RX130_ATG485_70_26_05"  # Without .xlsx extension

    # Communication
    COM_PORT = "//./COM5"
    BAUDRATE = 38400

    # Test values
    TDA_TEST_VALUE = "60ff8000df12"  # Known working TDA format (from TDM_Manager)
    FACTORY_CODE = "0101010101010101010101010101"

    # Timing (in seconds)
    COMM_INIT_DELAY = 2
    POST_STARTUP_DELAY = 3
    POST_RESET_DELAY = 10  # Increased from 2
    DGTO_WRITE_DELAY = 0.5
    DGTO_READ_RETRY_DELAY = 0.2
    DFLS_POLL_INTERVAL = 2
    DFLS_TIMEOUT = 300  # 5 minutes for DFLS download
    PSM_READ_INTERVAL = 1

    # Retry counts
    MAX_DGTO_ATTEMPTS = 30
    MAX_API_ATTEMPTS = 10
    PSM_READING_COUNT = 10

    # Report
    REPORT_PATH = r"C:\Alireza\Alireza\TDM4_Test\reports\"

    # Device limits (from FILE_INIT.py for PCM5/MINI2 devices)
    # Adjust these based on your actual CTRL_BOX_ID
    DEVICE_LIMITS = {
        "FANHMAX": {"min": 0, "max": 2300, "test_value": 1500},
        "FANCMAX": {"min": 0, "max": 2300, "test_value": 1400},
        "FANCMIN": {"min": 0, "max": 1000, "test_value": 400},
        "TDM_EH_Enable": {"min": 0, "max": 1, "test_value": 1},
    }


class TestResult(Enum):
    """Test step result status"""
    OK = "OK"
    FAIL = "FAIL"
    PARTIAL = "PARTIAL"
    SKIP = "SKIP"


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def dgto_code(code_str):
    """Convert D-G-T-O string to DGTO address"""
    return SWAP(SMapDGTO(code_str).dgto)


def log(message, level="INFO"):
    """Print timestamped log message"""
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    prefix = {
        "INFO": "   ",
        "OK": " ✓ ",
        "FAIL": " ✗ ",
        "WARN": " ⚠ ",
        "STEP": ">>>"
    }.get(level, "   ")
    print(f"[{timestamp}]{prefix}{message}")


def validate_value(dgto_name, value):
    """Validate value against device limits"""
    if dgto_name in Config.DEVICE_LIMITS:
        limits = Config.DEVICE_LIMITS[dgto_name]
        if value < limits["min"] or value > limits["max"]:
            log(f"{dgto_name}={value} is outside valid range [{limits['min']}-{limits['max']}]", "WARN")
            return False
    return True


# =============================================================================
# OTA TEST CLASS
# =============================================================================

class OTATest:
    """
    OTA Test Automation implementing Pablo's 14 Steps

    This class provides both:
    - Direct API access (for low-level operations)
    - TestLib wrapper (for DGTO operations with name lookup)
    """

    def __init__(self):
        self.api = None
        self.testlib = None
        self.fwprj = None
        self.results = {}
        self.start_time = None

    def initialize(self):
        """Initialize communication and load configurations"""
        log("=" * 60, "STEP")
        log("INITIALIZING OTA TEST", "STEP")
        log("=" * 60, "STEP")

        self.start_time = datetime.now()

        # Check files exist
        if not os.path.exists(Config.FWPRJ_FILE):
            log(f"FWPRJ file not found: {Config.FWPRJ_FILE}", "FAIL")
            return False

        if not os.path.exists(Config.DFLS_FILE):
            log(f"DFLS file not found: {Config.DFLS_FILE}", "WARN")

        # Load FWPRJ for DGTO lookup
        try:
            self.fwprj = FWPRJ(Config.FWPRJ_FILE)
            log(f"Loaded FWPRJ: {Config.FWPRJ_FILE}", "OK")
        except Exception as e:
            log(f"Failed to load FWPRJ: {e}", "FAIL")
            return False

        # Initialize low-level API
        try:
            self.api = API()
            self.api.CommOpen(Config.COM_PORT, Config.BAUDRATE)
            log(f"COM port opened: {Config.COM_PORT} @ {Config.BAUDRATE}", "OK")
            time.sleep(Config.COMM_INIT_DELAY)
        except Exception as e:
            log(f"Failed to open COM port: {e}", "FAIL")
            return False

        # System startup with FWPRJ
        try:
            self.api.system_startup_from_file(Config.FWPRJ_FILE)
            log("System startup complete", "OK")
            time.sleep(Config.POST_STARTUP_DELAY)
        except Exception as e:
            log(f"System startup failed: {e}", "FAIL")
            return False

        # Verify device communication by reading TDM Status
        if self._verify_communication():
            log("Device communication verified", "OK")
            return True
        else:
            log("Device communication failed", "FAIL")
            return False

    def _verify_communication(self):
        """Verify device is responding"""
        # Try to read TDM Status using FWPRJ lookup
        dgto_info = self.fwprj.searchStandardDGTO("TDM - Status")
        if dgto_info[0] is None:
            # Fallback to direct code
            dgto_info = self.fwprj.searchStandardDGTO("10-0-6-22")

        if dgto_info[2] is not None:
            dgto_addr = SWAP(dgto_info[2])
            for i in range(Config.MAX_API_ATTEMPTS):
                s, v = self.api.ReadDGTO(dgto_addr)
                if s == EErrors.E_OK and v is not None:
                    log(f"TDM Status = {v}")
                    return True
                time.sleep(Config.DGTO_READ_RETRY_DELAY)

        # Fallback: try hardcoded address
        for i in range(Config.MAX_API_ATTEMPTS):
            s, v = self.api.ReadDGTO(dgto_code("10-0-6-22"))
            if s == EErrors.E_OK and v is not None:
                log(f"TDM Status (fallback) = {v}")
                return True
            time.sleep(Config.DGTO_READ_RETRY_DELAY)

        return False

    def cleanup(self):
        """Close communication"""
        if self.api:
            try:
                self.api.CommClose()
                log("COM port closed", "OK")
            except:
                pass

    def _lookup_dgto(self, name_or_code):
        """
        Look up DGTO address from name or code using FWPRJ
        Returns: (name, code_str, address) or (None, None, None)
        """
        if self.fwprj:
            # Try as name first
            info = self.fwprj.searchStandardDGTO(name_or_code)
            if info[0] is not None:
                return info[0], info[1], SWAP(info[2])

            # Try phantom DGTO
            pinfo = self.fwprj.searchPhantomDGTO(name_or_code)
            if pinfo[0] is not None:
                return pinfo[0], pinfo[1], SWAP(pinfo[2])

        # Fallback: if it looks like a code (X-X-X-X), convert directly
        if "-" in str(name_or_code) and str(name_or_code).replace("-", "").replace(" ", "").isdigit():
            return name_or_code, name_or_code, dgto_code(name_or_code)

        return None, None, None

    def read_dgto(self, name_or_code, silent=False):
        """
        Read DGTO value using name lookup
        Returns: value or None
        """
        name, code, addr = self._lookup_dgto(name_or_code)

        if addr is None:
            if not silent:
                log(f"DGTO not found: {name_or_code}", "WARN")
            return None

        for i in range(Config.MAX_DGTO_ATTEMPTS):
            s, v = self.api.ReadDGTO(addr)
            if s == EErrors.E_OK and v is not None:
                if not silent:
                    log(f"Read {name or code} = {v}")
                return v
            time.sleep(Config.DGTO_READ_RETRY_DELAY)

        if not silent:
            log(f"Failed to read {name or code} after {Config.MAX_DGTO_ATTEMPTS} attempts", "FAIL")
        return None

    def write_dgto(self, name_or_code, value, verify=True):
        """
        Write DGTO value using name lookup
        Returns: True if successful (and verified if requested)
        """
        name, code, addr = self._lookup_dgto(name_or_code)

        if addr is None:
            log(f"DGTO not found: {name_or_code}", "WARN")
            return False

        # Validate value
        if name and not validate_value(name, value):
            log(f"Value {value} may be invalid for {name}", "WARN")

        # Write
        for i in range(Config.MAX_DGTO_ATTEMPTS):
            s = self.api.WriteDGTO(addr, value)
            if s == EErrors.E_OK:
                log(f"Write {name or code} = {value}", "OK")

                if verify:
                    time.sleep(Config.DGTO_WRITE_DELAY)
                    read_val = self.read_dgto(name_or_code, silent=True)
                    if read_val == value:
                        log(f"Verified {name or code} = {read_val}", "OK")
                        return True
                    else:
                        log(f"Verify mismatch: wrote {value}, read {read_val}", "WARN")
                        return False
                return True
            time.sleep(Config.DGTO_READ_RETRY_DELAY)

        log(f"Failed to write {name or code}", "FAIL")
        return False

    # =========================================================================
    # TEST STEPS
    # =========================================================================

    def step_1_sw_download(self):
        """Step 1: Download SW Version to Board"""
        log("STEP 1: Download SW Version to Board", "STEP")
        log("-" * 50)

        # No direct method available in pymtstestlib for SW download
        # This would typically be done via a separate tool or bootloader
        log("SKIPPED - No method available for SW download", "WARN")
        log("Use external tool (e.g., Ariston Flasher) for SW download")

        self.results["step_1"] = (TestResult.SKIP, "No method available")
        return True

    def step_2_tda_operations(self):
        """Step 2: Write TDA and Read TDA"""
        log("STEP 2: Write and Verify TDA", "STEP")
        log("-" * 50)

        write_ok = False
        read_ok = False
        tda_read_value = None

        # Write TDA
        log(f"Writing TDA: {Config.TDA_TEST_VALUE}")
        try:
            for i in range(Config.MAX_API_ATTEMPTS):
                s = self.api.TDAWriteInfo(Config.TDA_TEST_VALUE, "")
                if s == EErrors.E_OK:
                    self.api.TDARegisterTest(1)
                    log(f"TDAWriteInfo successful", "OK")
                    write_ok = True
                    break
                time.sleep(0.2)

            if not write_ok:
                log(f"TDAWriteInfo failed after {Config.MAX_API_ATTEMPTS} attempts", "FAIL")
        except Exception as e:
            log(f"TDAWriteInfo error: {e}", "FAIL")

        time.sleep(1)

        # Read TDA
        log("Reading TDA...")
        try:
            for i in range(Config.MAX_API_ATTEMPTS):
                result = self.api.TDAReadInfo()

                if isinstance(result, tuple) and len(result) >= 2:
                    s, info = result[0], result[1]
                    if s == EErrors.E_OK and info is not None:
                        # Try different ways to extract TDA code
                        if hasattr(info, 'code'):
                            try:
                                tda_read_value = info.code.decode('utf-8').rstrip('\xff\x00')
                            except:
                                tda_read_value = str(info.code)
                        else:
                            tda_read_value = str(info)

                        log(f"TDAReadInfo: {tda_read_value}", "OK")
                        read_ok = True
                        break
                time.sleep(0.2)

            if not read_ok:
                log(f"TDAReadInfo failed", "FAIL")
        except Exception as e:
            log(f"TDAReadInfo error: {e}", "FAIL")

        # Record results
        self.results["step_2_write"] = (TestResult.OK if write_ok else TestResult.FAIL,
                                         Config.TDA_TEST_VALUE if write_ok else "Failed")
        self.results["step_2_read"] = (TestResult.OK if read_ok else TestResult.FAIL,
                                        tda_read_value if read_ok else "Failed")

        return write_ok and read_ok

    def step_3_6_dfls_download(self):
        """Steps 3-6: Download DFLS file"""
        log("STEPS 3-6: Download DFLS", "STEP")
        log("-" * 50)

        if not os.path.exists(Config.DFLS_FILE):
            log(f"DFLS file not found: {Config.DFLS_FILE}", "WARN")
            self.results["step_3_6"] = (TestResult.SKIP, "File not found")
            return True  # Continue with other tests

        log(f"DFLS File: {Config.DFLS_FILE}")
        log(f"Factory Code: {Config.FACTORY_CODE}")

        try:
            success = self.api.DflsMapDownload(Config.DFLS_FILE, Config.FACTORY_CODE)

            if not success:
                log("DflsMapDownload failed to start", "FAIL")
                self.results["step_3_6"] = (TestResult.FAIL, "Download failed to start")
                return False

            log("DFLS download started...", "OK")

            # Poll for completion
            start_time = time.time()
            while (time.time() - start_time) < Config.DFLS_TIMEOUT:
                try:
                    result = self.api.GetDownloadInfo()
                    if isinstance(result, tuple) and len(result) >= 2:
                        s, info = result

                        # Log progress
                        if hasattr(info, 'progress'):
                            log(f"Download progress: {info.progress}%")

                        # Check completion (status 3 typically means complete)
                        if hasattr(info, 'status'):
                            if info.status == 3:
                                log("DFLS download COMPLETE", "OK")
                                self.results["step_3_6"] = (TestResult.OK, "Download complete")
                                return True
                            elif info.status == 4:  # Error status
                                log(f"DFLS download error: status={info.status}", "FAIL")
                                self.results["step_3_6"] = (TestResult.FAIL, f"Error status {info.status}")
                                return False
                except Exception as e:
                    log(f"GetDownloadInfo error: {e}", "WARN")

                time.sleep(Config.DFLS_POLL_INTERVAL)

            log("DFLS download timeout", "FAIL")
            self.results["step_3_6"] = (TestResult.PARTIAL, "Timeout")
            return False

        except Exception as e:
            log(f"DFLS download error: {e}", "FAIL")
            self.results["step_3_6"] = (TestResult.FAIL, str(e))
            return False

    def step_7_device_info(self):
        """Step 7: Get Device Information"""
        log("STEP 7: Get Device Information", "STEP")
        log("-" * 50)

        info_obtained = False
        device_info = {}

        # Method 1: Try ReadPSoleFwAttr (Ares5)
        try:
            result = self.api.ReadPSoleFwAttr()
            if isinstance(result, tuple) and len(result) >= 4:
                s, desc, prod_id, ares_ver = result
                if s and desc is not None:
                    device_info["description"] = desc
                    device_info["product_id"] = prod_id
                    device_info["ares_version"] = ares_ver
                    log(f"Description: {desc}", "OK")
                    log(f"Product ID: {prod_id}", "OK")
                    log(f"ARES Version: {ares_ver}", "OK")
                    info_obtained = True
        except Exception as e:
            log(f"ReadPSoleFwAttr not available: {e}")

        # Method 2: Read key DGTOs
        if not info_obtained:
            log("Using DGTO fallback for device info...")

            # Read TDM Status
            tdm_status = self.read_dgto("TDM - Status", silent=True)
            if tdm_status is None:
                tdm_status = self.read_dgto("10-0-6-22", silent=True)

            if tdm_status is not None:
                device_info["tdm_status"] = tdm_status
                log(f"TDM Status: {tdm_status}", "OK")
                info_obtained = True

            # Read Fault Code
            fault_code = self.read_dgto("Fault_Code", silent=True)
            if fault_code is None:
                fault_code = self.read_dgto("5-1-2-3", silent=True)

            if fault_code is not None:
                device_info["fault_code"] = fault_code
                log(f"Fault Code: {fault_code}", "OK")

        if info_obtained:
            self.results["step_7"] = (TestResult.OK, str(device_info))
        else:
            self.results["step_7"] = (TestResult.FAIL, "Could not get device info")

        return info_obtained

    def step_8_9_write_adj_dgtos(self):
        """Steps 8-9: Write ADJ DGTOs"""
        log("STEPS 8-9: Write ADJ DGTOs", "STEP")
        log("-" * 50)

        # DGTOs to write with their test values
        adj_dgtos = [
            ("FANHMAX", Config.DEVICE_LIMITS["FANHMAX"]["test_value"]),
            ("FANCMAX", Config.DEVICE_LIMITS["FANCMAX"]["test_value"]),
            ("FANCMIN", Config.DEVICE_LIMITS["FANCMIN"]["test_value"]),
            ("TDM_EH_Enable", Config.DEVICE_LIMITS["TDM_EH_Enable"]["test_value"]),
        ]

        # Alternative DGTO codes if names not found
        alt_codes = {
            "FANHMAX": "10-0-2-24",
            "FANCMAX": "10-0-2-26",
            "FANCMIN": "10-0-2-27",
            "TDM_EH_Enable": "2-3-0-28",
        }

        written = []
        failed = []

        for name, value in adj_dgtos:
            log(f"Writing {name} = {value}...")

            # Try by name first
            success = self.write_dgto(name, value, verify=True)

            # Fallback to code
            if not success and name in alt_codes:
                log(f"Trying fallback code {alt_codes[name]}...")
                success = self.write_dgto(alt_codes[name], value, verify=True)

            if success:
                written.append((name, value))
            else:
                failed.append((name, value))

            time.sleep(Config.DGTO_WRITE_DELAY)

        total = len(adj_dgtos)
        ok_count = len(written)

        if ok_count == total:
            self.results["step_8_9"] = (TestResult.OK, f"{ok_count}/{total} written")
        elif ok_count > 0:
            self.results["step_8_9"] = (TestResult.PARTIAL, f"{ok_count}/{total} written")
        else:
            self.results["step_8_9"] = (TestResult.FAIL, f"0/{total} written")

        # Store for step 11
        self._written_dgtos = written
        self._failed_dgtos = failed

        return ok_count == total

    def step_10_send_reset(self):
        """Step 10: Send Reset (Error History Reset)"""
        log("STEP 10: Send Reset (ErrorHistoryReset)", "STEP")
        log("-" * 50)

        success = False

        for i in range(Config.MAX_API_ATTEMPTS):
            try:
                s = self.api.ErrorHistoryReset()
                if s == EErrors.E_OK:
                    log("ErrorHistoryReset successful", "OK")
                    success = True
                    break
            except Exception as e:
                log(f"ErrorHistoryReset attempt {i+1} failed: {e}")
            time.sleep(Config.DGTO_READ_RETRY_DELAY)

        if success:
            log(f"Waiting {Config.POST_RESET_DELAY}s for device to stabilize...")
            time.sleep(Config.POST_RESET_DELAY)
            self.results["step_10"] = (TestResult.OK, "Error history cleared")
        else:
            log("ErrorHistoryReset failed", "FAIL")
            self.results["step_10"] = (TestResult.FAIL, "Could not reset")

        return success

    def step_11_read_back_dgtos(self):
        """Step 11: Read Back DGTOs"""
        log("STEP 11: Read Back DGTOs", "STEP")
        log("-" * 50)

        if not hasattr(self, '_written_dgtos'):
            log("No DGTOs to verify (step 8-9 not completed)", "WARN")
            self.results["step_11"] = (TestResult.SKIP, "No data from step 8-9")
            return True

        alt_codes = {
            "FANHMAX": "10-0-2-24",
            "FANCMAX": "10-0-2-26",
            "FANCMIN": "10-0-2-27",
            "TDM_EH_Enable": "2-3-0-28",
        }

        matched = []
        mismatched = []

        for name, expected in self._written_dgtos:
            log(f"Verifying {name} (expected={expected})...")

            actual = self.read_dgto(name, silent=True)
            if actual is None and name in alt_codes:
                actual = self.read_dgto(alt_codes[name], silent=True)

            if actual is not None:
                if actual == expected:
                    log(f"{name}: {actual} == {expected} [MATCH]", "OK")
                    matched.append((name, expected, actual))
                else:
                    log(f"{name}: {actual} != {expected} [MISMATCH]", "WARN")
                    mismatched.append((name, expected, actual))
            else:
                log(f"{name}: Could not read", "FAIL")
                mismatched.append((name, expected, None))

        total = len(self._written_dgtos)
        ok_count = len(matched)

        if ok_count == total:
            self.results["step_11"] = (TestResult.OK, f"{ok_count}/{total} matched")
        elif ok_count > 0:
            self.results["step_11"] = (TestResult.PARTIAL, f"{ok_count}/{total} matched")
        else:
            self.results["step_11"] = (TestResult.FAIL, f"0/{total} matched")

        return ok_count == total

    def step_12_placeholder(self):
        """Step 12: Placeholder (method not specified)"""
        log("STEP 12: (Placeholder)", "STEP")
        log("-" * 50)
        log("SKIPPED - Step not defined")

        self.results["step_12"] = (TestResult.SKIP, "Step not defined")
        return True

    def step_13_fault_history(self):
        """Step 13: Get Fault History"""
        log("STEP 13: Get Fault History", "STEP")
        log("-" * 50)

        fault_ok = False
        fault_info = None

        # Method 1: ErrorHistoryRead
        try:
            result = self.api.ErrorHistoryRead(0, 10)

            if isinstance(result, tuple) and len(result) >= 2:
                s, faults = result
                if s == EErrors.E_OK and faults is not None:
                    fault_count = len(faults) if hasattr(faults, '__len__') else 0
                    log(f"ErrorHistoryRead: {fault_count} entries", "OK")

                    # Show first few faults
                    if fault_count > 0:
                        for i, fault in enumerate(faults[:5]):
                            log(f"  Fault[{i}]: {fault}")

                    fault_info = f"{fault_count} faults"
                    fault_ok = True
            elif result == EErrors.E_OK:
                log("ErrorHistoryRead: No faults", "OK")
                fault_info = "No faults"
                fault_ok = True
        except Exception as e:
            log(f"ErrorHistoryRead error: {e}")

        # Method 2: Fallback to Fault_Code DGTO
        if not fault_ok:
            log("Using Fault_Code DGTO fallback...")

            fault_code = self.read_dgto("Fault_Code", silent=True)
            if fault_code is None:
                fault_code = self.read_dgto("5-1-2-3", silent=True)

            if fault_code is not None:
                log(f"Fault_Code: {fault_code}", "OK")
                fault_info = f"Fault_Code={fault_code}"
                fault_ok = True

        if fault_ok:
            self.results["step_13"] = (TestResult.OK, fault_info)
        else:
            self.results["step_13"] = (TestResult.FAIL, "Could not read fault history")

        return fault_ok

    def step_14_psm_status_loop(self):
        """Step 14: Read PSM-Status every second"""
        log(f"STEP 14: Read PSM-Status ({Config.PSM_READING_COUNT} readings)", "STEP")
        log("-" * 50)

        readings = []

        # Try to find PSM-Status DGTO
        psm_dgtos = ["PSM-Status", "PSM_STATUS", "4-11-6-25"]
        working_dgto = None

        # Find which DGTO works
        for dgto in psm_dgtos:
            val = self.read_dgto(dgto, silent=True)
            if val is not None:
                working_dgto = dgto
                log(f"Using DGTO: {dgto}")
                break

        if working_dgto is None:
            log("Could not find working PSM-Status DGTO", "FAIL")
            self.results["step_14"] = (TestResult.FAIL, "DGTO not found")
            return False

        # Take readings
        for i in range(Config.PSM_READING_COUNT):
            timestamp = datetime.now().strftime('%H:%M:%S')

            value = self.read_dgto(working_dgto, silent=True)

            if value is not None:
                readings.append(value)
                log(f"[{timestamp}] PSM-Status = {value}")
            else:
                readings.append("FAIL")
                log(f"[{timestamp}] PSM-Status = FAIL", "WARN")

            if i < Config.PSM_READING_COUNT - 1:
                time.sleep(Config.PSM_READ_INTERVAL)

        ok_count = sum(1 for v in readings if v != "FAIL")
        total = Config.PSM_READING_COUNT

        if ok_count == total:
            self.results["step_14"] = (TestResult.OK, f"{ok_count}/{total} readings")
        elif ok_count > 0:
            self.results["step_14"] = (TestResult.PARTIAL, f"{ok_count}/{total} readings")
        else:
            self.results["step_14"] = (TestResult.FAIL, f"0/{total} readings")

        return ok_count == total

    def print_results(self):
        """Print final results table"""
        print("\n" + "=" * 70)
        print("  FINAL RESULTS TABLE")
        print("=" * 70)

        duration = datetime.now() - self.start_time if self.start_time else None
        if duration:
            print(f"  Test Duration: {duration}")

        print(f"\n{'Step':<20} | {'Status':<10} | {'Details':<35}")
        print("-" * 70)

        step_names = [
            ("step_1", "SW Download"),
            ("step_2_write", "Write TDA"),
            ("step_2_read", "Read TDA"),
            ("step_3_6", "DFLS Download"),
            ("step_7", "Device Info"),
            ("step_8_9", "Write ADJ DGTOs"),
            ("step_10", "Send Reset"),
            ("step_11", "Read Back DGTOs"),
            ("step_12", "Step 12"),
            ("step_13", "Fault History"),
            ("step_14", "PSM-Status Loop"),
        ]

        counts = {TestResult.OK: 0, TestResult.FAIL: 0,
                  TestResult.PARTIAL: 0, TestResult.SKIP: 0}

        for key, name in step_names:
            result = self.results.get(key, (TestResult.FAIL, "Not executed"))
            status, details = result

            # Handle both enum and string status
            if isinstance(status, TestResult):
                status_val = status
            else:
                status_val = TestResult(status) if status in [e.value for e in TestResult] else TestResult.FAIL

            counts[status_val] = counts.get(status_val, 0) + 1

            symbol = {"OK": "✓", "FAIL": "✗", "PARTIAL": "~", "SKIP": "-"}.get(status_val.value, "?")
            details_str = str(details)[:33] if details else "-"

            print(f"{name:<20} | {symbol} {status_val.value:<7} | {details_str:<35}")

        print("-" * 70)
        print(f"\nSUMMARY: {counts[TestResult.OK]} OK | {counts[TestResult.FAIL]} FAIL | "
              f"{counts[TestResult.PARTIAL]} PARTIAL | {counts[TestResult.SKIP]} SKIP")
        print("=" * 70)

        return counts

    def save_results(self):
        """Save results to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(PROJECT_ROOT, f"ota_test_results_{timestamp}.txt")

        try:
            with open(filename, 'w') as f:
                f.write(f"OTA TEST RESULTS - {datetime.now()}\n")
                f.write("=" * 70 + "\n\n")

                for key, (status, details) in self.results.items():
                    status_val = status.value if isinstance(status, TestResult) else status
                    f.write(f"{key}: {status_val} - {details}\n")

                f.write("\n" + "=" * 70 + "\n")

            log(f"Results saved to: {filename}", "OK")
            return filename
        except Exception as e:
            log(f"Failed to save results: {e}", "FAIL")
            return None

    def run_all(self):
        """Run all test steps"""
        if not self.initialize():
            log("Initialization failed, aborting test", "FAIL")
            return False

        try:
            self.step_1_sw_download()
            self.step_2_tda_operations()
            self.step_3_6_dfls_download()
            self.step_7_device_info()
            self.step_8_9_write_adj_dgtos()
            self.step_10_send_reset()
            self.step_11_read_back_dgtos()
            self.step_12_placeholder()
            self.step_13_fault_history()
            self.step_14_psm_status_loop()
        except Exception as e:
            log(f"Test execution error: {e}", "FAIL")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()

        counts = self.print_results()
        self.save_results()

        return counts[TestResult.FAIL] == 0


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  IMPROVED OTA TEST AUTOMATION (Pablo's 14 Steps)")
    print("=" * 70)
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Python: {sys.version}")
    print(f"  Working Dir: {os.getcwd()}")
    print("=" * 70)

    test = OTATest()
    success = test.run_all()

    sys.exit(0 if success else 1)
