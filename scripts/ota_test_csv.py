"""
================================================================================
TASK 3: COMPLETE OTA TEST AUTOMATION (Pablo's 14 Steps) - CSV VERSION
================================================================================
This version uses the original CSV file for DGTO lookups instead of Excel.
================================================================================
"""

import time
import os
import re
from datetime import datetime
from pymtstestlib.api import API
from pymtstestlib.shared.error_defs import EErrors
from pymtstestlib.shared.export_defs import SMapDGTO
from pymtstestlib.shared.utils import SWAP

# =============================================================================
# CONFIGURATION
# =============================================================================

# Project files
FWPRJ_FILE = r"C:\Alireza\Alireza\TDM4_Test\TDM4_RX130_ATG485_70_26_05.fwprj"
CSV_FILE = r"C:\Alireza\Alireza\TDM4_Test\TDM4_RX130_ATG485_70_26_05.csv"

# DFLS file paths to check
DFLS_OPTIONS = [
    r"C:\Alireza\Alireza\TDM4_Test\sources\0x0048_PCM5_ver00.02.00-SAT.dfls",
    r"C:\Alireza\Alireza\TDM4_Test\0x0048_PCM5_ver00.02.00-SAT.dfls",
]

# Communication settings
COM_PORT = "//./COM5"
BAUDRATE = 38400

# Test values from Pablo's email
TDA_TEST_VALUE = "121212121212"
FACTORY_CODE = "0101010101010101010101010101"

# Timing settings
POST_STARTUP_DELAY = 5  # Wait time after system startup
MAX_ATTEMPTS = 30
DGTO_READ_DELAY = 0.2
PSM_READING_COUNT = 10

# =============================================================================
# CSV-BASED DGTO LOOKUP CLASS
# =============================================================================

class DGTOLookup:
    """
    DGTO lookup class that reads from CSV file.
    Provides name-to-code conversion similar to TestLib.

    Expected CSV format (semicolon-separated):
    DGTO_CODE;HEX_CODE;NAME;DESCRIPTION
    Example: 0-1-0-9;0x0109;TDM Electric Heater 1;
    """

    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.dgto_map = {}  # Maps name -> (hex_val, dgto_code)
        self.code_map = {}  # Maps dgto_code -> (hex_val, name)
        self._load_csv()

    def _load_csv(self):
        """Load the CSV file and build lookup maps."""
        if not os.path.exists(self.csv_path):
            print(f"    WARNING: CSV file not found: {self.csv_path}")
            return False

        try:
            # Read as semicolon-separated file with no header
            # Format: DGTO_CODE;HEX_CODE;NAME;DESCRIPTION
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

            # Split by semicolon
            parts = line.split(';')
            if len(parts) >= 3:
                dgto_code = parts[0].strip()  # e.g., "0-1-0-9"
                hex_str = parts[1].strip()     # e.g., "0x0109"
                name = parts[2].strip()        # e.g., "TDM Electric Heater 1"

                # Parse hex value
                try:
                    if hex_str.startswith('0x') or hex_str.startswith('0X'):
                        hex_val = int(hex_str, 16)
                    else:
                        hex_val = int(hex_str, 16)
                except:
                    hex_val = self._dgto_to_hex(dgto_code)

                # Build lookup maps
                if name:
                    # Normalize name for lookup (uppercase, no spaces)
                    name_key = name.upper().replace(' ', '_')
                    self.dgto_map[name_key] = (hex_val, dgto_code, name)
                    # Also store original name
                    self.dgto_map[name.upper()] = (hex_val, dgto_code, name)

                if dgto_code:
                    self.code_map[dgto_code] = (hex_val, name)

                count += 1

        print(f"    CSV loaded: {count} DGTO entries")
        return True

    def search_dgto(self, dgto_name):
        """
        Search for a DGTO by name or code.
        Returns: (hex_value, name, code) or (0, None, None) if not found
        """
        # Try by name (case-insensitive)
        name_upper = dgto_name.upper()
        if name_upper in self.dgto_map:
            hex_val, dgto_code, orig_name = self.dgto_map[name_upper]
            return hex_val, orig_name, dgto_code

        # Try with underscores replaced by spaces
        name_normalized = name_upper.replace('_', ' ')
        if name_normalized in self.dgto_map:
            hex_val, dgto_code, orig_name = self.dgto_map[name_normalized]
            return hex_val, orig_name, dgto_code

        # Try by DGTO code (e.g., "2-3-0-28")
        if dgto_name in self.code_map:
            hex_val, name = self.code_map[dgto_name]
            return hex_val, name, dgto_name

        # Partial name match
        for key, (hex_val, dgto_code, orig_name) in self.dgto_map.items():
            if name_upper in key or key in name_upper:
                return hex_val, orig_name, dgto_code

        # If not found, try to parse as D-G-T-O format
        return self._convert_code_string(dgto_name)

    def _convert_code_string(self, dgto_str):
        """Convert D-G-T-O string format to hex value."""
        if re.match(r"^[0-9]+-[0-9]+-[0-9]+-[0-9]+$", dgto_str):
            hex_val = self._dgto_to_hex(dgto_str)
            return hex_val, None, dgto_str
        return 0, None, None

    def _dgto_to_hex(self, dgto_code):
        """Convert D-G-T-O string to hex value using SWAP(SMapDGTO)."""
        try:
            return SWAP(SMapDGTO(dgto_code).dgto)
        except:
            # Manual conversion if library fails
            parts = dgto_code.split('-')
            if len(parts) == 4:
                d, g, t, o = [int(p) for p in parts]
                # Standard DGTO packing: Device(4) | Group(4) | Type(8) | Occurrence(8)
                return (d << 20) | (g << 16) | (t << 8) | o
        return 0

    def get_dgto_code(self, dgto_name):
        """Get the SWAP'd DGTO code for API calls."""
        hex_val, name, code = self.search_dgto(dgto_name)
        return hex_val

    def list_available(self, filter_text=None):
        """List available DGTOs (for debugging)."""
        print("\n    Available DGTOs:")
        for dgto_code, (hex_val, name) in self.code_map.items():
            if filter_text is None or filter_text.upper() in (name or '').upper():
                print(f"      {dgto_code} | 0x{hex_val:04X} | {name}")

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def dgto_direct(code):
    """Convert D-G-T-O string to SWAP'd value for direct API use."""
    return SWAP(SMapDGTO(code).dgto)

def find_dfls_file():
    """Find the DFLS file from available paths."""
    for path in DFLS_OPTIONS:
        if os.path.exists(path):
            return path
    return None

def verify_device_ready(api, dgto_lookup, max_attempts=30):
    """Verify device is ready for communication."""
    # Try to read TDM_STATUS to verify communication
    dgto_code = dgto_lookup.get_dgto_code("TDM_STATUS")
    if dgto_code == 0:
        dgto_code = dgto_direct("10-0-6-22")  # Fallback

    for i in range(max_attempts):
        try:
            s, v = api.ReadDGTO(dgto_code)
            if s == EErrors.E_OK and v is not None:
                return True, v
        except:
            pass
        time.sleep(0.2)
    return False, None

# =============================================================================
# MAIN TEST CLASS
# =============================================================================

class OTATest:
    """
    OTA Test implementation following Pablo's 14 Steps.
    Uses CSV file for DGTO lookups.
    """

    def __init__(self):
        self.api = None
        self.dgto_lookup = None
        self.results = {}
        self.dfls_file = None

    def initialize(self):
        """Initialize API and load CSV file."""
        print("=" * 70)
        print("  TASK 3: COMPLETE OTA TEST (Pablo's 14 Steps) - CSV VERSION")
        print("=" * 70)
        print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  COM Port: {COM_PORT}")
        print(f"  CSV File: {CSV_FILE}")
        print("=" * 70)

        # Load CSV for DGTO lookups
        print("\n[INIT] Loading CSV file for DGTO lookups...")
        self.dgto_lookup = DGTOLookup(CSV_FILE)

        # Find DFLS file
        self.dfls_file = find_dfls_file()
        if self.dfls_file:
            print(f"    DFLS file found: {self.dfls_file}")
        else:
            print("    WARNING: DFLS file not found!")

        # Initialize API
        print("\n[INIT] Initializing API...")
        self.api = API()
        self.api.CommOpen(COM_PORT, BAUDRATE)
        print(f"    CommOpen: OK")
        time.sleep(2)

        # Load firmware project
        print(f"    Loading FWPRJ: {FWPRJ_FILE}")
        self.api.system_startup_from_file(FWPRJ_FILE)
        print(f"    system_startup_from_file: OK")

        # Wait for device to be ready
        print(f"    Waiting {POST_STARTUP_DELAY}s for device initialization...")
        time.sleep(POST_STARTUP_DELAY)

        # Verify device communication
        print("    Verifying device communication...")
        ready, value = verify_device_ready(self.api, self.dgto_lookup)
        if ready:
            print(f"    Device ready! TDM_STATUS = {value}")
            return True
        else:
            print("    WARNING: Could not verify device communication")
            return True  # Continue anyway

    def step_1_download_sw(self):
        """Step 1: Download SW Version to Board"""
        print("\n[STEP 1] Download SW Version to Board")
        print("-" * 50)
        # This step typically requires external programmer
        self.results["step_1"] = ("SKIP", "Requires external programmer")
        print("    SKIPPED - Requires external programmer")

    def step_2_write_read_tda(self):
        """Step 2: Write TDA and Read TDA"""
        print("\n[STEP 2] Write TDA and Verify")
        print("-" * 50)

        # Write TDA
        print(f"    Writing TDA: {TDA_TEST_VALUE}")
        try:
            s = self.api.TDAWriteInfo(TDA_TEST_VALUE, "")
            if s == EErrors.E_OK:
                print(f"    TDAWriteInfo: OK")
                self.api.TDARegisterTest(1)
                self.results["step_2_write"] = ("OK", TDA_TEST_VALUE)
            else:
                print(f"    TDAWriteInfo returned: {s}")
                self.results["step_2_write"] = ("FAIL", str(s))
        except Exception as e:
            print(f"    TDAWriteInfo Error: {e}")
            self.results["step_2_write"] = ("FAIL", str(e))

        time.sleep(1)

        # Read TDA
        print("    Reading TDA...")
        try:
            result = self.api.TDAReadInfo()
            if isinstance(result, tuple) and len(result) >= 2:
                s, info = result[0], result[1]
                if s == EErrors.E_OK and info is not None:
                    if hasattr(info, 'code'):
                        tda_code = info.code.decode('utf-8').rstrip('\xff\x00')
                    else:
                        tda_code = str(info)
                    print(f"    TDAReadInfo: {tda_code}")
                    self.results["step_2_read"] = ("OK", tda_code)
                else:
                    print(f"    TDAReadInfo returned: {s}")
                    self.results["step_2_read"] = ("FAIL", str(s))
            else:
                print(f"    TDAReadInfo unexpected format: {result}")
                self.results["step_2_read"] = ("FAIL", "Unexpected format")
        except Exception as e:
            print(f"    TDAReadInfo Error: {e}")
            self.results["step_2_read"] = ("FAIL", str(e))

    def step_3_6_download_dfls(self):
        """Steps 3-6: Download DFLS"""
        print("\n[STEP 3-6] Download DFLS")
        print("-" * 50)

        if not self.dfls_file:
            print("    DFLS file not found")
            self.results["step_3_6"] = ("SKIP", "File not found")
            return

        print(f"    DFLS File: {self.dfls_file}")
        print(f"    Factory Code: {FACTORY_CODE}")

        try:
            success = self.api.DflsMapDownload(self.dfls_file, FACTORY_CODE)
            if success:
                print("    DflsMapDownload: Started")
                # Wait for download to complete
                for i in range(60):
                    try:
                        result = self.api.GetDownloadInfo()
                        if isinstance(result, tuple):
                            s, info = result
                            if hasattr(info, 'status'):
                                print(f"    Status: {info.status} (progress: {getattr(info, 'progress', 'N/A')})")
                                if info.status == 3:  # Complete
                                    print("    DFLS Download: COMPLETE")
                                    self.results["step_3_6"] = ("OK", "DFLS downloaded")
                                    return
                    except Exception as e:
                        pass
                    time.sleep(1)

                self.results["step_3_6"] = ("PARTIAL", "Timeout waiting for completion")
            else:
                print("    DflsMapDownload: Failed to start")
                self.results["step_3_6"] = ("FAIL", "DflsMapDownload returned False")
        except Exception as e:
            print(f"    DFLS Error: {e}")
            self.results["step_3_6"] = ("FAIL", str(e))

        time.sleep(2)

    def step_7_get_device_info(self):
        """Step 7: Get Device Info"""
        print("\n[STEP 7] Get Device Info")
        print("-" * 50)

        # Method 1: Try ReadPSoleFwAttr
        try:
            result = self.api.ReadPSoleFwAttr()
            if isinstance(result, tuple) and len(result) >= 4:
                s, desc, prod_id, ares_ver = result
                if s and desc is not None:
                    print(f"    Description: {desc}")
                    print(f"    Product ID: {prod_id}")
                    print(f"    ARES Version: {ares_ver}")
                    self.results["step_7"] = ("OK", f"ProdID:{prod_id}")
                    return
        except Exception as e:
            print(f"    ReadPSoleFwAttr: {e}")

        # Method 2: Read TDM_STATUS via DGTO
        print("    Trying TDM_STATUS DGTO...")
        dgto_code = self.dgto_lookup.get_dgto_code("TDM_STATUS")
        if dgto_code == 0:
            dgto_code = dgto_direct("10-0-6-22")

        for i in range(MAX_ATTEMPTS):
            s, v = self.api.ReadDGTO(dgto_code)
            if s == EErrors.E_OK and v is not None:
                print(f"    TDM_STATUS: {v}")
                self.results["step_7"] = ("OK", f"TDM_STATUS={v}")
                return
            time.sleep(DGTO_READ_DELAY)

        self.results["step_7"] = ("FAIL", "Could not get device info")

    def step_8_9_write_adj_dgtos(self):
        """Steps 8-9: Write ADJ DGTOs"""
        print("\n[STEP 8-9] Write ADJ DGTOs")
        print("-" * 50)

        # ADJ DGTOs to write (name, fallback code, test value)
        # Names should match CSV entries or use DGTO codes directly
        adj_dgtos = [
            ("FANHMAX", "10-0-2-24", 1500),
            ("FANCMAX", "10-0-2-26", 1400),
            ("FANCMIN", "10-0-2-27", 400),
            ("TDM Electric Heater Enable", "2-3-0-28", 1),  # From CSV: 2-3-0-28;0x231C;TDM Electric Heater Enable
        ]

        self.written_dgtos = []

        for name, fallback_code, test_value in adj_dgtos:
            print(f"    Writing {name} = {test_value}...")

            # Get DGTO code (try CSV lookup first, then fallback)
            dgto_code = self.dgto_lookup.get_dgto_code(name)
            if dgto_code == 0:
                dgto_code = dgto_direct(fallback_code)
                print(f"        Using fallback code: {fallback_code}")

            success = False
            for i in range(MAX_ATTEMPTS):
                s = self.api.WriteDGTO(dgto_code, test_value)
                if s == EErrors.E_OK:
                    print(f"        {name}: OK")
                    self.written_dgtos.append((name, dgto_code, test_value, "OK"))
                    success = True
                    break
                time.sleep(DGTO_READ_DELAY)

            if not success:
                print(f"        {name}: FAIL")
                self.written_dgtos.append((name, dgto_code, test_value, "FAIL"))

            time.sleep(0.3)

        ok_count = sum(1 for d in self.written_dgtos if d[3] == "OK")
        self.results["step_8_9"] = (
            "OK" if ok_count == len(adj_dgtos) else "PARTIAL",
            f"{ok_count}/{len(adj_dgtos)} written"
        )

    def step_10_send_reset(self):
        """Step 10: Send Reset (ErrorHistoryReset)"""
        print("\n[STEP 10] Send Reset (ErrorHistoryReset)")
        print("-" * 50)

        for i in range(MAX_ATTEMPTS):
            s = self.api.ErrorHistoryReset()
            if s == EErrors.E_OK:
                print("    ErrorHistoryReset: OK")
                self.results["step_10"] = ("OK", "Error log cleared")
                time.sleep(2)
                return
            time.sleep(DGTO_READ_DELAY)

        print("    ErrorHistoryReset: FAIL")
        self.results["step_10"] = ("FAIL", "Could not reset")

    def step_11_read_back_dgtos(self):
        """Step 11: Read Back DGTOs and Verify"""
        print("\n[STEP 11] Read Back DGTOs")
        print("-" * 50)

        if not hasattr(self, 'written_dgtos') or not self.written_dgtos:
            print("    No DGTOs to verify")
            self.results["step_11"] = ("SKIP", "No DGTOs written")
            return

        read_results = []

        for name, dgto_code, expected, write_status in self.written_dgtos:
            if write_status != "OK":
                print(f"    {name}: Skipped (write failed)")
                read_results.append(False)
                continue

            read_success = False
            for i in range(MAX_ATTEMPTS):
                s, actual = self.api.ReadDGTO(dgto_code)
                if s == EErrors.E_OK and actual is not None:
                    match = (actual == expected)
                    status_text = "MATCH" if match else "MISMATCH"
                    print(f"    {name}: Read={actual}, Expected={expected} [{status_text}]")
                    read_results.append(match)
                    read_success = True
                    break
                time.sleep(DGTO_READ_DELAY)

            if not read_success:
                print(f"    {name}: FAIL to read")
                read_results.append(False)

        match_count = sum(read_results)
        self.results["step_11"] = (
            "OK" if match_count == len(read_results) else "PARTIAL",
            f"{match_count}/{len(read_results)} matched"
        )

    def step_12_skip(self):
        """Step 12: (Placeholder)"""
        print("\n[STEP 12] SKIPPED - Method Missing")
        print("-" * 50)
        self.results["step_12"] = ("SKIP", "Method not available")
        print("    SKIPPED")

    def step_13_get_fault_history(self):
        """Step 13: Get Fault History"""
        print("\n[STEP 13] Get Fault History")
        print("-" * 50)

        # Method 1: Try ErrorHistoryRead
        try:
            result = self.api.ErrorHistoryRead(0, 10)
            if isinstance(result, tuple) and len(result) >= 2:
                s, faults = result
                if s == EErrors.E_OK and faults is not None:
                    fault_count = len(faults) if hasattr(faults, '__len__') else 0
                    print(f"    ErrorHistoryRead: OK ({fault_count} entries)")
                    for i, fault in enumerate(list(faults)[:3]):
                        print(f"        Fault[{i}]: {fault}")
                    self.results["step_13"] = ("OK", f"{fault_count} faults")
                    return
            elif result == EErrors.E_OK:
                print("    ErrorHistoryRead: OK (empty)")
                self.results["step_13"] = ("OK", "No faults")
                return
        except Exception as e:
            print(f"    ErrorHistoryRead Error: {e}")

        # Method 2: Fallback to Fault_Code DGTO
        print("    Trying Fault_Code DGTO...")
        dgto_code = self.dgto_lookup.get_dgto_code("Fault_Code")
        if dgto_code == 0:
            dgto_code = dgto_direct("5-1-2-3")

        for i in range(MAX_ATTEMPTS):
            s, v = self.api.ReadDGTO(dgto_code)
            if s == EErrors.E_OK and v is not None:
                print(f"    Fault_Code: {v}")
                self.results["step_13"] = ("OK", f"Fault_Code={v}")
                return
            time.sleep(DGTO_READ_DELAY)

        self.results["step_13"] = ("FAIL", "Could not read fault history")

    def step_14_read_psm_status(self):
        """Step 14: Read PSM-Status Every Second"""
        print(f"\n[STEP 14] Read PSM-Status Every Second ({PSM_READING_COUNT} readings)")
        print("-" * 50)

        # Get PSM_Status DGTO code
        dgto_code = self.dgto_lookup.get_dgto_code("PSM_Status")
        if dgto_code == 0:
            dgto_code = self.dgto_lookup.get_dgto_code("PSM-Status")
        if dgto_code == 0:
            dgto_code = dgto_direct("4-11-6-25")

        psm_readings = []

        for i in range(PSM_READING_COUNT):
            timestamp = datetime.now().strftime('%H:%M:%S')
            read_ok = False

            for attempt in range(10):
                s, v = self.api.ReadDGTO(dgto_code)
                if s == EErrors.E_OK and v is not None:
                    psm_readings.append(v)
                    print(f"    [{timestamp}] PSM-Status = {v}")
                    read_ok = True
                    break
                time.sleep(0.1)

            if not read_ok:
                psm_readings.append("FAIL")
                print(f"    [{timestamp}] PSM-Status = FAIL")

            if i < PSM_READING_COUNT - 1:
                time.sleep(1)

        ok_readings = sum(1 for v in psm_readings if v != "FAIL")
        self.results["step_14"] = (
            "OK" if ok_readings == PSM_READING_COUNT else "PARTIAL",
            f"{ok_readings}/{PSM_READING_COUNT} readings"
        )

    def cleanup(self):
        """Close API connection."""
        if self.api:
            try:
                self.api.CommClose()
                print("\n[CLEANUP] CommClose: OK")
            except:
                pass

    def print_results(self):
        """Print final results table."""
        print("\n" + "=" * 70)
        print("  FINAL RESULTS TABLE")
        print("=" * 70)
        print(f"{'Step':<15} | {'Status':<10} | {'Details':<40}")
        print("-" * 70)

        step_order = [
            ("step_1", "SW Download"),
            ("step_2_write", "WriteTDA"),
            ("step_2_read", "ReadTDA"),
            ("step_3_6", "DFLS Download"),
            ("step_7", "Device Info"),
            ("step_8_9", "Write ADJ DGTOs"),
            ("step_10", "Send Reset"),
            ("step_11", "Read Back DGTOs"),
            ("step_12", "Step 12"),
            ("step_13", "Fault History"),
            ("step_14", "PSM-Status"),
        ]

        for key, name in step_order:
            status, details = self.results.get(key, ("FAIL", "Not executed"))
            details_str = str(details)[:38] if details else "-"

            if status == "OK":
                status_display = "OK"
            elif status == "FAIL":
                status_display = "FAIL"
            elif status == "SKIP":
                status_display = "SKIP"
            else:
                status_display = "PARTIAL"

            print(f"{name:<15} | {status_display:<10} | {details_str:<40}")

        print("-" * 70)

        ok = sum(1 for r in self.results.values() if r[0] == "OK")
        fail = sum(1 for r in self.results.values() if r[0] == "FAIL")
        skip = sum(1 for r in self.results.values() if r[0] == "SKIP")
        partial = sum(1 for r in self.results.values() if r[0] == "PARTIAL")

        print(f"\nTOTAL: {ok} OK | {fail} FAIL | {partial} PARTIAL | {skip} SKIP")
        print("=" * 70)

        return ok, fail, partial, skip

    def save_results(self):
        """Save results to file."""
        results_file = f"ota_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        step_order = [
            ("step_1", "SW Download"),
            ("step_2_write", "WriteTDA"),
            ("step_2_read", "ReadTDA"),
            ("step_3_6", "DFLS Download"),
            ("step_7", "Device Info"),
            ("step_8_9", "Write ADJ DGTOs"),
            ("step_10", "Send Reset"),
            ("step_11", "Read Back DGTOs"),
            ("step_12", "Step 12"),
            ("step_13", "Fault History"),
            ("step_14", "PSM-Status"),
        ]

        with open(results_file, 'w') as f:
            f.write(f"OTA TEST RESULTS (CSV Version) - {datetime.now()}\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Configuration:\n")
            f.write(f"  COM Port: {COM_PORT}\n")
            f.write(f"  CSV File: {CSV_FILE}\n")
            f.write(f"  FWPRJ: {FWPRJ_FILE}\n")
            f.write(f"  DFLS: {self.dfls_file}\n")
            f.write("\n" + "=" * 70 + "\n\n")

            for key, name in step_order:
                status, details = self.results.get(key, ("FAIL", "Not executed"))
                f.write(f"{name}: {status} - {details}\n")

            ok = sum(1 for r in self.results.values() if r[0] == "OK")
            fail = sum(1 for r in self.results.values() if r[0] == "FAIL")
            skip = sum(1 for r in self.results.values() if r[0] == "SKIP")
            partial = sum(1 for r in self.results.values() if r[0] == "PARTIAL")

            f.write(f"\nTOTAL: {ok} OK | {fail} FAIL | {partial} PARTIAL | {skip} SKIP\n")

        print(f"\nResults saved to: {results_file}")
        return results_file

    def run_all_steps(self):
        """Run all 14 steps."""
        try:
            self.step_1_download_sw()
            self.step_2_write_read_tda()
            self.step_3_6_download_dfls()
            self.step_7_get_device_info()
            self.step_8_9_write_adj_dgtos()
            self.step_10_send_reset()
            self.step_11_read_back_dgtos()
            self.step_12_skip()
            self.step_13_get_fault_history()
            self.step_14_read_psm_status()
        except Exception as e:
            print(f"\n[ERROR] Unexpected error: {e}")
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
    test = OTATest()

    if test.initialize():
        test.run_all_steps()
    else:
        print("\n[ERROR] Initialization failed!")
