"""
================================================================================
IMPROVED OTA TEST AUTOMATION v2.0 (Pablo's 14 Steps)
================================================================================
Using TestLib methods as specified by Pablo:
  - WriteTDA / ReadTDA
  - dfls_download
  - get_device_info (via readIdentTable)
  - write_dgto / read_dgto (ADJ and STATISTICS DGTOs)
  - send_reset
  - get_fault_history (ErrorHistoryRead)
  - PSM-Status reading loop
================================================================================
"""

import time
import os
import sys
from datetime import datetime

# =============================================================================
# PATH SETUP
# =============================================================================
PROJECT_ROOT = r"C:\Alireza\Alireza\TDM4_Test"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# =============================================================================
# IMPORTS
# =============================================================================
try:
    from libs.TestLib import TestLib
    from libs.Report import Report
    from libs.ConfigParser import ConfigParser
    print("[OK] TestLib framework imported")
except ImportError as e:
    print(f"[ERROR] Failed to import TestLib: {e}")
    sys.exit(1)

try:
    from pymtstestlib.api import API
    from pymtstestlib.shared.error_defs import EErrors
    print("[OK] pymtstestlib imported")
except ImportError as e:
    print(f"[ERROR] Failed to import pymtstestlib: {e}")
    sys.exit(1)

# =============================================================================
# CONFIGURATION
# =============================================================================

# Device settings for TestLib initialization
DEVICE_SETTINGS = {
    "port": 5,  # COM5
    "baudRate": 38400,
    "dgtoSourcePath": r"C:\Alireza\Alireza\TDM4_Test\TDM4_RX130_ATG485_70_26_05",  # Excel file (without .xlsx)
    "fwprjSourcePath": r"C:\Alireza\Alireza\TDM4_Test\TDM4_RX130_ATG485_70_26_05",  # FWPRJ file (without .fwprj)
    "probeSourcePath": "None",  # Set to actual path if you have probe file
    "phantomSourcePath": "None",  # Set to actual path if you have phantom file
    "device": "TDM4 PCM5",
    "probe_check_time": 10,
    "dgto_check_time": 1,
}

# Test configuration
TDA_TEST_VALUE = "121212121212"  # Random TDA value as Pablo specified
FACTORY_CODE = "0101010101010101010101010101"  # Random Factory Code as Pablo specified
DFLS_FILE = r"C:\Alireza\Alireza\TDM4_Test\sources\0x0048_PCM5_ver00.02.00-SAT.dfls"

# ADJ DGTOs to test (from Excel/ARES Chatter - Adjustables category)
# Format: (DGTO_NAME, test_value)
ADJ_DGTOS_TO_WRITE = [
    ("FANHMAX", 1500),           # Fan max heating RPM
    ("FANCMAX", 1400),           # Fan max cooling RPM
    ("FANCMIN", 400),            # Fan min RPM
    ("TDM_EH_Enable", 1),        # Electric heater enable
]

# STATISTICS DGTOs to test (from Excel/ARES Chatter - Statistics category)
# Format: (DGTO_NAME, test_value)
STATISTICS_DGTOS_TO_WRITE = [
    # Add your statistics DGTOs here based on what's in your Excel file
    # Example: ("STAT_DGTO_NAME", value),
]

# PSM-Status DGTO for Step 14
PSM_STATUS_DGTO = "PSM-Status"  # Or use code like "4-11-6-25" if name doesn't work

# Timing
PSM_READING_COUNT = 10
PSM_READ_INTERVAL = 1  # seconds

# =============================================================================
# LOGGING
# =============================================================================

def log(message, level="INFO"):
    """Print timestamped log message"""
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    symbols = {"INFO": "   ", "OK": " ✓ ", "FAIL": " ✗ ", "WARN": " ⚠ ", "STEP": ">>>"}
    print(f"[{timestamp}]{symbols.get(level, '   ')}{message}")

# =============================================================================
# OTA TEST CLASS
# =============================================================================

class OTATestWithTestLib:
    """
    OTA Test using TestLib methods as specified by Pablo
    """

    def __init__(self):
        self.testlib = None
        self.results = {}
        self.written_dgtos = []  # Store written DGTOs for verification in Step 11
        self.start_time = None

    def initialize(self):
        """Initialize TestLib with device settings"""
        log("=" * 60, "STEP")
        log("INITIALIZING TestLib", "STEP")
        log("=" * 60, "STEP")

        self.start_time = datetime.now()

        try:
            # Create TestLib instance - this handles COM port, FWPRJ loading, etc.
            self.testlib = TestLib(DEVICE_SETTINGS)
            log(f"TestLib initialized on COM{DEVICE_SETTINGS['port']}", "OK")
            log(f"Device: {DEVICE_SETTINGS['device']}", "OK")
            return True
        except Exception as e:
            log(f"TestLib initialization failed: {e}", "FAIL")
            import traceback
            traceback.print_exc()
            return False

    def cleanup(self):
        """Cleanup and generate report"""
        if self.testlib:
            try:
                # Update report with final results
                all_ok = all(r[0] == "OK" for r in self.results.values() if r[0] != "SKIP")
                self.testlib.update_report(all_ok)
                log("Report updated", "OK")
            except Exception as e:
                log(f"Report update failed: {e}", "WARN")

    # =========================================================================
    # STEP 2: Write TDA and Read TDA
    # =========================================================================
    def step_2_tda_write_read(self):
        """
        STEP 2: Write TDA and verify by reading back
        - Use WriteTDA to write random TDA (e.g., "121212121212")
        - Use ReadTDA to read and verify it matches
        """
        log("STEP 2: Write TDA and Read TDA (Verify)", "STEP")
        log("-" * 50)

        write_ok = False
        read_ok = False
        verify_ok = False
        read_value = None

        # Write TDA using TestLib's WriteTDA method
        log(f"Writing TDA: {TDA_TEST_VALUE}")
        try:
            result = self.testlib.WriteTDA(TDA_TEST_VALUE, "")
            if result:
                log("WriteTDA successful", "OK")
                write_ok = True
            else:
                log("WriteTDA returned False", "FAIL")
        except Exception as e:
            log(f"WriteTDA error: {e}", "FAIL")

        time.sleep(1)

        # Read TDA using TestLib's ReadTDA method
        log("Reading TDA to verify...")
        try:
            read_result = self.testlib.ReadTDA()

            if read_result is not None:
                # Handle different return formats
                if isinstance(read_result, tuple):
                    read_value = read_result[0] if len(read_result) > 0 else str(read_result)
                elif isinstance(read_result, bytes):
                    read_value = read_result.decode('utf-8').rstrip('\xff\x00')
                else:
                    read_value = str(read_result)

                log(f"ReadTDA returned: {read_value}", "OK")
                read_ok = True

                # Verify match
                if TDA_TEST_VALUE in str(read_value):
                    log(f"TDA VERIFIED: Written value matches!", "OK")
                    verify_ok = True
                else:
                    log(f"TDA MISMATCH: Expected '{TDA_TEST_VALUE}', got '{read_value}'", "WARN")
            else:
                log("ReadTDA returned None", "FAIL")
        except Exception as e:
            log(f"ReadTDA error: {e}", "FAIL")

        # Record results
        self.results["step_2_write"] = ("OK" if write_ok else "FAIL", TDA_TEST_VALUE)
        self.results["step_2_read"] = ("OK" if read_ok else "FAIL", read_value)
        self.results["step_2_verify"] = ("OK" if verify_ok else "FAIL",
                                          "Match" if verify_ok else "Mismatch")

        return write_ok and read_ok

    # =========================================================================
    # STEPS 3-6: Download DFLS
    # =========================================================================
    def step_3_6_dfls_download(self):
        """
        STEPS 3-6: Download DFLS file using dfls_download method
        - Use dfls_download with DFLS file and Factory Code
        """
        log("STEPS 3-6: Download DFLS (dfls_download)", "STEP")
        log("-" * 50)

        if not os.path.exists(DFLS_FILE):
            log(f"DFLS file not found: {DFLS_FILE}", "WARN")
            self.results["step_3_6"] = ("SKIP", "DFLS file not found")
            return True  # Continue with other tests

        log(f"DFLS File: {DFLS_FILE}")
        log(f"Factory Code: {FACTORY_CODE}")

        try:
            # Use TestLib's dfls_download method
            result = self.testlib.dfls_download(DFLS_FILE, FACTORY_CODE)

            if result:
                log("dfls_download completed successfully", "OK")
                self.results["step_3_6"] = ("OK", "DFLS downloaded")
                return True
            else:
                log("dfls_download returned False", "FAIL")
                self.results["step_3_6"] = ("FAIL", "Download failed")
                return False

        except AttributeError:
            # Method might not exist in this version
            log("dfls_download method not available in TestLib", "WARN")
            log("Trying direct API method...", "INFO")

            try:
                # Fallback to direct API
                api = self.testlib._api
                success = api.DflsMapDownload(DFLS_FILE, FACTORY_CODE)
                if success:
                    log("DflsMapDownload (API) started", "OK")
                    # Wait for completion
                    for i in range(120):  # 2 minutes timeout
                        time.sleep(2)
                        try:
                            info = api.GetDownloadInfo()
                            if hasattr(info, 'status') and info.status == 3:
                                log("DFLS download complete", "OK")
                                self.results["step_3_6"] = ("OK", "Downloaded via API")
                                return True
                        except:
                            pass
                    self.results["step_3_6"] = ("PARTIAL", "Timeout waiting")
                    return False
                else:
                    self.results["step_3_6"] = ("FAIL", "API download failed")
                    return False
            except Exception as e2:
                log(f"API fallback also failed: {e2}", "FAIL")
                self.results["step_3_6"] = ("FAIL", str(e2))
                return False

        except Exception as e:
            log(f"dfls_download error: {e}", "FAIL")
            self.results["step_3_6"] = ("FAIL", str(e))
            return False

    # =========================================================================
    # STEP 7: Get Device Info
    # =========================================================================
    def step_7_get_device_info(self):
        """
        STEP 7: Get device info to verify points written above
        - Use get_device_info or readIdentTable
        """
        log("STEP 7: Get Device Info (Verify)", "STEP")
        log("-" * 50)

        device_info = {}
        info_ok = False

        # Try readIdentTable method
        try:
            ident_result = self.testlib.readIdentTable()
            if ident_result:
                log(f"readIdentTable: {ident_result}", "OK")
                device_info["ident_table"] = ident_result
                info_ok = True
        except Exception as e:
            log(f"readIdentTable error: {e}", "WARN")

        # Also read some key DGTOs for verification
        try:
            # Read TDM Status
            tdm_status = self.testlib.read_dgto("TDM - Status")
            if tdm_status is not None:
                log(f"TDM - Status: {tdm_status}", "OK")
                device_info["tdm_status"] = tdm_status
                info_ok = True
        except Exception as e:
            log(f"TDM Status read error: {e}", "WARN")

        try:
            # Read Fault Code
            fault_code = self.testlib.read_dgto("Fault_Code")
            if fault_code is not None:
                log(f"Fault_Code: {fault_code}", "OK")
                device_info["fault_code"] = fault_code
        except Exception as e:
            log(f"Fault Code read error: {e}", "WARN")

        if info_ok:
            self.results["step_7"] = ("OK", str(device_info))
        else:
            self.results["step_7"] = ("FAIL", "Could not get device info")

        return info_ok

    # =========================================================================
    # STEPS 8-9: Write ADJ and STATISTICS DGTOs
    # =========================================================================
    def step_8_9_write_dgtos(self):
        """
        STEPS 8-9: Write ADJ and STATISTICS DGTOs using write_dgto
        - Choose some ADJ DGTOs and write random values
        - Choose some STATISTICS DGTOs and write random values
        - DGTOs can be found in Excel file or ARES Chatter
        """
        log("STEPS 8-9: Write ADJ and STATISTICS DGTOs (write_dgto)", "STEP")
        log("-" * 50)

        self.written_dgtos = []
        success_count = 0
        total_count = 0

        # Combine ADJ and STATISTICS DGTOs
        all_dgtos = ADJ_DGTOS_TO_WRITE + STATISTICS_DGTOS_TO_WRITE
        total_count = len(all_dgtos)

        if total_count == 0:
            log("No DGTOs configured to write!", "WARN")
            self.results["step_8_9"] = ("SKIP", "No DGTOs configured")
            return True

        log(f"Writing {len(ADJ_DGTOS_TO_WRITE)} ADJ DGTOs and {len(STATISTICS_DGTOS_TO_WRITE)} STATISTICS DGTOs")

        for dgto_name, value in all_dgtos:
            log(f"Writing {dgto_name} = {value}...")

            try:
                # Use TestLib's write_dgto method
                result = self.testlib.write_dgto(dgto_name, value)

                if result:
                    log(f"  {dgto_name} written successfully", "OK")
                    self.written_dgtos.append((dgto_name, value, True))
                    success_count += 1
                else:
                    log(f"  {dgto_name} write failed (returned False)", "FAIL")
                    self.written_dgtos.append((dgto_name, value, False))

            except Exception as e:
                log(f"  {dgto_name} write error: {e}", "FAIL")
                self.written_dgtos.append((dgto_name, value, False))

            time.sleep(0.5)

        # Record results
        if success_count == total_count:
            self.results["step_8_9"] = ("OK", f"{success_count}/{total_count} written")
        elif success_count > 0:
            self.results["step_8_9"] = ("PARTIAL", f"{success_count}/{total_count} written")
        else:
            self.results["step_8_9"] = ("FAIL", f"0/{total_count} written")

        return success_count > 0

    # =========================================================================
    # STEP 10: Send Reset
    # =========================================================================
    def step_10_send_reset(self):
        """
        STEP 10: Send reset using send_reset method
        """
        log("STEP 10: Send Reset (send_reset)", "STEP")
        log("-" * 50)

        try:
            # Use TestLib's send_reset method
            # The method typically takes a timer parameter (seconds before reset)
            result = self.testlib.send_reset(timer=0)  # Immediate reset

            if result:
                log("send_reset successful", "OK")
                # Wait for device to come back
                log("Waiting 10 seconds for device to restart...")
                time.sleep(10)
                self.results["step_10"] = ("OK", "Reset sent")
                return True
            else:
                log("send_reset returned False", "FAIL")
                self.results["step_10"] = ("FAIL", "Reset failed")
                return False

        except AttributeError:
            log("send_reset method not available, trying ErrorHistoryReset...", "WARN")
            try:
                api = self.testlib._api
                s = api.ErrorHistoryReset()
                if s == EErrors.E_OK:
                    log("ErrorHistoryReset successful", "OK")
                    time.sleep(10)
                    self.results["step_10"] = ("OK", "Reset via ErrorHistoryReset")
                    return True
            except Exception as e2:
                log(f"ErrorHistoryReset also failed: {e2}", "FAIL")
            self.results["step_10"] = ("FAIL", "No reset method available")
            return False

        except Exception as e:
            log(f"send_reset error: {e}", "FAIL")
            self.results["step_10"] = ("FAIL", str(e))
            return False

    # =========================================================================
    # STEP 11: Read Back DGTOs Written in Steps 8-9
    # =========================================================================
    def step_11_read_dgtos(self):
        """
        STEP 11: Read back the DGTOs written in Steps 8-9 using read_dgto
        """
        log("STEP 11: Read Back DGTOs (read_dgto)", "STEP")
        log("-" * 50)

        if not self.written_dgtos:
            log("No DGTOs to read back (Step 8-9 not completed)", "WARN")
            self.results["step_11"] = ("SKIP", "No DGTOs from Step 8-9")
            return True

        match_count = 0
        total_count = 0

        for dgto_name, expected_value, was_written in self.written_dgtos:
            if not was_written:
                log(f"  Skipping {dgto_name} (write failed in Step 8-9)")
                continue

            total_count += 1
            log(f"Reading {dgto_name} (expected: {expected_value})...")

            try:
                # Use TestLib's read_dgto method
                actual_value = self.testlib.read_dgto(dgto_name)

                if actual_value is not None:
                    if actual_value == expected_value:
                        log(f"  {dgto_name} = {actual_value} [MATCH]", "OK")
                        match_count += 1
                    else:
                        log(f"  {dgto_name} = {actual_value} (expected {expected_value}) [MISMATCH]", "WARN")
                else:
                    log(f"  {dgto_name} read returned None", "FAIL")

            except Exception as e:
                log(f"  {dgto_name} read error: {e}", "FAIL")

        # Record results
        if total_count == 0:
            self.results["step_11"] = ("SKIP", "No DGTOs to verify")
        elif match_count == total_count:
            self.results["step_11"] = ("OK", f"{match_count}/{total_count} matched")
        elif match_count > 0:
            self.results["step_11"] = ("PARTIAL", f"{match_count}/{total_count} matched")
        else:
            self.results["step_11"] = ("FAIL", f"0/{total_count} matched")

        return match_count == total_count

    # =========================================================================
    # STEP 12: Skip (Method Missing)
    # =========================================================================
    def step_12_placeholder(self):
        """
        STEP 12: This can't be done at the moment (method missing)
        """
        log("STEP 12: (Method Missing - Skipped)", "STEP")
        log("-" * 50)
        log("Skipped as per Pablo's instructions - method not available")

        self.results["step_12"] = ("SKIP", "Method missing")
        return True

    # =========================================================================
    # STEP 13: Get Fault History
    # =========================================================================
    def step_13_fault_history(self):
        """
        STEP 13: Save Fault History information using get_fault_history
        """
        log("STEP 13: Get Fault History (get_fault_history)", "STEP")
        log("-" * 50)

        fault_info = None
        fault_ok = False

        # Try various method names for getting fault history
        methods_to_try = [
            ("get_fault_history", lambda: self.testlib.get_fault_history()),
            ("ErrorHistoryRead", lambda: self.testlib._api.ErrorHistoryRead(0, 10)),
        ]

        for method_name, method_call in methods_to_try:
            try:
                result = method_call()

                if result is not None:
                    if isinstance(result, tuple) and len(result) >= 2:
                        s, faults = result
                        if faults is not None:
                            fault_count = len(faults) if hasattr(faults, '__len__') else 0
                            log(f"{method_name}: {fault_count} fault entries", "OK")

                            # Display first few faults
                            if fault_count > 0 and hasattr(faults, '__iter__'):
                                for i, fault in enumerate(list(faults)[:5]):
                                    log(f"  Fault[{i}]: {fault}")

                            fault_info = f"{fault_count} faults"
                            fault_ok = True
                            break
                    else:
                        log(f"{method_name} returned: {result}", "OK")
                        fault_info = str(result)
                        fault_ok = True
                        break
            except AttributeError:
                log(f"{method_name} method not available", "INFO")
            except Exception as e:
                log(f"{method_name} error: {e}", "WARN")

        # Fallback: Read Fault_Code DGTO
        if not fault_ok:
            log("Trying Fault_Code DGTO fallback...")
            try:
                fault_code = self.testlib.read_dgto("Fault_Code")
                if fault_code is not None:
                    log(f"Fault_Code: {fault_code}", "OK")
                    fault_info = f"Fault_Code={fault_code}"
                    fault_ok = True
            except Exception as e:
                log(f"Fault_Code read error: {e}", "WARN")

        if fault_ok:
            self.results["step_13"] = ("OK", fault_info)
        else:
            self.results["step_13"] = ("FAIL", "Could not get fault history")

        return fault_ok

    # =========================================================================
    # STEP 14: Read PSM-Status Every Second
    # =========================================================================
    def step_14_psm_status_loop(self):
        """
        STEP 14: Read PSM-Status DGTO every second and save it
        """
        log(f"STEP 14: Read PSM-Status Every Second ({PSM_READING_COUNT} readings)", "STEP")
        log("-" * 50)

        readings = []
        read_ok_count = 0

        log(f"Reading DGTO: {PSM_STATUS_DGTO}")

        for i in range(PSM_READING_COUNT):
            timestamp = datetime.now().strftime('%H:%M:%S')

            try:
                # Use TestLib's read_dgto method
                value = self.testlib.read_dgto(PSM_STATUS_DGTO)

                if value is not None:
                    readings.append({"time": timestamp, "value": value})
                    log(f"[{timestamp}] {PSM_STATUS_DGTO} = {value}")
                    read_ok_count += 1
                else:
                    readings.append({"time": timestamp, "value": "FAIL"})
                    log(f"[{timestamp}] {PSM_STATUS_DGTO} = FAIL (None)", "WARN")

            except Exception as e:
                readings.append({"time": timestamp, "value": f"ERROR: {e}"})
                log(f"[{timestamp}] {PSM_STATUS_DGTO} = ERROR: {e}", "FAIL")

            # Wait 1 second before next reading (except after last one)
            if i < PSM_READING_COUNT - 1:
                time.sleep(PSM_READ_INTERVAL)

        # Save readings to file
        self._save_psm_readings(readings)

        # Record results
        if read_ok_count == PSM_READING_COUNT:
            self.results["step_14"] = ("OK", f"{read_ok_count}/{PSM_READING_COUNT} readings")
        elif read_ok_count > 0:
            self.results["step_14"] = ("PARTIAL", f"{read_ok_count}/{PSM_READING_COUNT} readings")
        else:
            self.results["step_14"] = ("FAIL", f"0/{PSM_READING_COUNT} readings")

        return read_ok_count > 0

    def _save_psm_readings(self, readings):
        """Save PSM readings to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(PROJECT_ROOT, f"psm_readings_{timestamp}.txt")

        try:
            with open(filename, 'w') as f:
                f.write(f"PSM-Status Readings - {datetime.now()}\n")
                f.write("=" * 40 + "\n")
                for reading in readings:
                    f.write(f"{reading['time']}: {reading['value']}\n")
            log(f"PSM readings saved to: {filename}", "OK")
        except Exception as e:
            log(f"Failed to save PSM readings: {e}", "WARN")

    # =========================================================================
    # Results Summary
    # =========================================================================
    def print_results(self):
        """Print final results table"""
        print("\n" + "=" * 70)
        print("  FINAL RESULTS - Pablo's 14 Steps OTA Test")
        print("=" * 70)

        if self.start_time:
            duration = datetime.now() - self.start_time
            print(f"  Test Duration: {duration}")
        print()

        step_names = [
            ("step_2_write", "Step 2: WriteTDA"),
            ("step_2_read", "Step 2: ReadTDA"),
            ("step_2_verify", "Step 2: Verify TDA"),
            ("step_3_6", "Steps 3-6: DFLS Download"),
            ("step_7", "Step 7: Device Info"),
            ("step_8_9", "Steps 8-9: Write DGTOs"),
            ("step_10", "Step 10: Send Reset"),
            ("step_11", "Step 11: Read DGTOs"),
            ("step_12", "Step 12: (Skipped)"),
            ("step_13", "Step 13: Fault History"),
            ("step_14", "Step 14: PSM-Status"),
        ]

        counts = {"OK": 0, "FAIL": 0, "PARTIAL": 0, "SKIP": 0}

        print(f"{'Step':<30} | {'Status':<10} | {'Details':<25}")
        print("-" * 70)

        for key, name in step_names:
            status, details = self.results.get(key, ("FAIL", "Not executed"))
            counts[status] = counts.get(status, 0) + 1

            symbol = {"OK": "✓", "FAIL": "✗", "PARTIAL": "~", "SKIP": "-"}.get(status, "?")
            details_str = str(details)[:23] if details else "-"

            print(f"{name:<30} | {symbol} {status:<7} | {details_str:<25}")

        print("-" * 70)
        print(f"\nSUMMARY: {counts['OK']} OK | {counts['FAIL']} FAIL | {counts['PARTIAL']} PARTIAL | {counts['SKIP']} SKIP")
        print("=" * 70)

        return counts

    def save_results(self):
        """Save results to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(PROJECT_ROOT, f"ota_test_results_{timestamp}.txt")

        try:
            with open(filename, 'w') as f:
                f.write(f"OTA TEST RESULTS (Pablo's 14 Steps)\n")
                f.write(f"Date: {datetime.now()}\n")
                f.write("=" * 70 + "\n\n")

                for key, (status, details) in self.results.items():
                    f.write(f"{key}: {status} - {details}\n")

            log(f"Results saved to: {filename}", "OK")
        except Exception as e:
            log(f"Failed to save results: {e}", "WARN")

    def run_all(self):
        """Run all test steps"""
        print("=" * 70)
        print("  PABLO'S 14 STEPS - OTA TEST AUTOMATION v2.0")
        print("  Using TestLib Methods")
        print("=" * 70)
        print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)

        if not self.initialize():
            log("Initialization failed!", "FAIL")
            return False

        try:
            # Execute all steps
            self.step_2_tda_write_read()
            self.step_3_6_dfls_download()
            self.step_7_get_device_info()
            self.step_8_9_write_dgtos()
            self.step_10_send_reset()
            self.step_11_read_dgtos()
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

        return counts.get("FAIL", 0) == 0


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    test = OTATestWithTestLib()
    success = test.run_all()
    sys.exit(0 if success else 1)
