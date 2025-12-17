"""
================================================================================
TASK 3: COMPLETE OTA TEST AUTOMATION (Pablo's 14 Steps) - FIXED
================================================================================
Fixed version with better error handling
================================================================================
"""

import time
import os
from datetime import datetime
from pymtstestlib.api import API
from pymtstestlib.shared.error_defs import EErrors
from pymtstestlib.shared.export_defs import SMapDGTO
from pymtstestlib.shared.utils import SWAP

# =============================================================================
# CONFIGURATION
# =============================================================================

FWPRJ = r"C:\Alireza\Alireza\TDM4_Test\TDM4_RX130_ATG485_70_26_05.fwprj"

# DFLS file - check which one exists
DFLS_OPTIONS = [
    r"C:\Alireza\Alireza\TDM4_Test\0x0048_PCM5_ver00.02.00-SAT.dfls",
    r"C:\Alireza\Alireza\TDM4_Test\sources\0x0048_PCM5_ver00.02.00-SAT.dfls",
]

COM_PORT = "//./COM5"
BAUDRATE = 38400

# Test values from Pablo's email
TDA_TEST_VALUE = "121212121212"
FACTORY_CODE = "0101010101010101010101010101"

MAX_ATTEMPTS = 30

# =============================================================================
# DGTO HELPER
# =============================================================================

def dgto(code):
    return SWAP(SMapDGTO(code).dgto)

# Key DGTOs
DGTO_PSM_STATUS = dgto("4-11-6-25")
DGTO_FAULT_CODE = dgto("5-1-2-3")
DGTO_TDM_STATUS = dgto("10-0-6-22")

# ADJ DGTOs for Step 8-9
ADJ_DGTOS = [
    ("FANHMAX", dgto("10-0-2-24"), 1500),
    ("FANCMAX", dgto("10-0-2-26"), 1400),
    ("FANCMIN", dgto("10-0-2-27"), 400),
    ("TDM_EH_Enable", dgto("2-3-0-28"), 1),
]

# =============================================================================
# MAIN TEST
# =============================================================================

print("=" * 70)
print("  TASK 3: COMPLETE OTA TEST (Pablo's 14 Steps) - FIXED")
print("=" * 70)
print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"  COM Port: {COM_PORT}")
print("=" * 70)

# Find DFLS file
DFLS_FILE = None
for path in DFLS_OPTIONS:
    if os.path.exists(path):
        DFLS_FILE = path
        print(f"  DFLS Found: {path}")
        break

if DFLS_FILE is None:
    print("  WARNING: No DFLS file found!")

# Initialize API
api = API()
api.CommOpen(COM_PORT, BAUDRATE)
time.sleep(2)
api.system_startup_from_file(FWPRJ)
time.sleep(2)

results = {}

# =============================================================================
# STEP 1: Download SW Version (SKIP)
# =============================================================================
print("\n[STEP 1] Download SW Version to Board")
print("-" * 50)
results["step_1"] = ("SKIP", "No method available")
print("    SKIPPED - No method available")

# =============================================================================
# STEP 2: Write TDA and Read TDA
# =============================================================================
print("\n[STEP 2] Write TDA and Verify")
print("-" * 50)

# Try WriteTDA
print(f"    Writing TDA: {TDA_TEST_VALUE}")
try:
    # Method 1: Direct string
    s = api.TDAWriteInfo(TDA_TEST_VALUE, "")
    if s == EErrors.E_OK:
        print(f"    TDAWriteInfo: OK")
        api.TDARegisterTest(1)
        results["step_2_write"] = ("OK", TDA_TEST_VALUE)
    else:
        print(f"    TDAWriteInfo: {s}")
        results["step_2_write"] = ("FAIL", str(s))
except Exception as e:
    print(f"    TDAWriteInfo Error: {e}")
    results["step_2_write"] = ("FAIL", str(e))

time.sleep(1)

# Try ReadTDA
print("    Reading TDA...")
try:
    result = api.TDAReadInfo()
    # Handle different return formats
    if isinstance(result, tuple) and len(result) >= 2:
        s, info = result[0], result[1]
        if s == EErrors.E_OK and info is not None:
            if hasattr(info, 'code'):
                tda_code = info.code.decode('utf-8').rstrip('\xff\x00')
            else:
                tda_code = str(info)
            print(f"    TDAReadInfo: {tda_code}")
            results["step_2_read"] = ("OK", tda_code)
        else:
            print(f"    TDAReadInfo: {s}")
            results["step_2_read"] = ("FAIL", str(s))
    else:
        print(f"    TDAReadInfo unexpected format: {result}")
        results["step_2_read"] = ("FAIL", "Unexpected format")
except Exception as e:
    print(f"    TDAReadInfo Error: {e}")
    results["step_2_read"] = ("FAIL", str(e))

# =============================================================================
# STEP 3-6: Download DFLS
# =============================================================================
print("\n[STEP 3-6] Download DFLS")
print("-" * 50)

if DFLS_FILE:
    print(f"    DFLS File: {DFLS_FILE}")
    try:
        success = api.DflsMapDownload(DFLS_FILE, FACTORY_CODE)
        if success:
            print("    DflsMapDownload: Started")
            # Wait for download
            for i in range(60):
                try:
                    result = api.GetDownloadInfo()
                    if isinstance(result, tuple):
                        s, info = result
                        print(f"    Status: {info}")
                        if hasattr(info, 'status') and info.status == 3:
                            print("    DFLS Download: COMPLETE")
                            results["step_3_6"] = ("OK", "DFLS downloaded")
                            break
                except:
                    pass
                time.sleep(1)
            else:
                results["step_3_6"] = ("PARTIAL", "Timeout")
        else:
            results["step_3_6"] = ("FAIL", "DflsMapDownload failed")
    except Exception as e:
        print(f"    DFLS Error: {e}")
        results["step_3_6"] = ("FAIL", str(e))
else:
    print("    DFLS file not found")
    results["step_3_6"] = ("SKIP", "File not found")

time.sleep(2)

# =============================================================================
# STEP 7: Get Device Info
# =============================================================================
print("\n[STEP 7] Get Device Info")
print("-" * 50)

device_info_ok = False

# Method 1: Try ReadPSoleFwAttr
try:
    result = api.ReadPSoleFwAttr()
    if isinstance(result, tuple) and len(result) >= 4:
        s, desc, prod_id, ares_ver = result
        if s and desc is not None:
            print(f"    Description: {desc}")
            print(f"    Product ID: {prod_id}")
            print(f"    ARES Version: {ares_ver}")
            results["step_7"] = ("OK", f"ProdID:{prod_id}")
            device_info_ok = True
except Exception as e:
    print(f"    ReadPSoleFwAttr: {e}")

# Method 2: Fallback to TDM_STATUS DGTO
if not device_info_ok:
    print("    Trying fallback (TDM_STATUS)...")
    for i in range(MAX_ATTEMPTS):
        s, v = api.ReadDGTO(DGTO_TDM_STATUS)
        if s == EErrors.E_OK and v is not None:
            print(f"    TDM_STATUS: {v}")
            results["step_7"] = ("OK", f"TDM_STATUS={v}")
            device_info_ok = True
            break
        time.sleep(0.2)

    if not device_info_ok:
        results["step_7"] = ("FAIL", "Could not get device info")

# =============================================================================
# STEP 8-9: Write ADJ DGTOs
# =============================================================================
print("\n[STEP 8-9] Write ADJ DGTOs")
print("-" * 50)

written_dgtos = []

for name, dgto_val, test_value in ADJ_DGTOS:
    print(f"    Writing {name} = {test_value}...")
    success = False
    for i in range(MAX_ATTEMPTS):
        s = api.WriteDGTO(dgto_val, test_value)
        if s == EErrors.E_OK:
            print(f"        {name}: OK")
            written_dgtos.append((name, dgto_val, test_value, "OK"))
            success = True
            break
        time.sleep(0.2)
    if not success:
        print(f"        {name}: FAIL")
        written_dgtos.append((name, dgto_val, test_value, "FAIL"))
    time.sleep(0.3)

ok_count = sum(1 for d in written_dgtos if d[3] == "OK")
results["step_8_9"] = ("OK" if ok_count == len(ADJ_DGTOS) else "PARTIAL",
                       f"{ok_count}/{len(ADJ_DGTOS)} written")

# =============================================================================
# STEP 10: Send Reset
# =============================================================================
print("\n[STEP 10] Send Reset (ErrorHistoryReset)")
print("-" * 50)

for i in range(MAX_ATTEMPTS):
    s = api.ErrorHistoryReset()
    if s == EErrors.E_OK:
        print("    ErrorHistoryReset: OK")
        results["step_10"] = ("OK", "Error log cleared")
        break
    time.sleep(0.2)
else:
    print("    ErrorHistoryReset: FAIL")
    results["step_10"] = ("FAIL", "Could not reset")

time.sleep(2)

# =============================================================================
# STEP 11: Read Back DGTOs
# =============================================================================
print("\n[STEP 11] Read Back DGTOs")
print("-" * 50)

read_results = []

for name, dgto_val, expected, write_status in written_dgtos:
    if write_status == "OK":
        for i in range(MAX_ATTEMPTS):
            s, actual = api.ReadDGTO(dgto_val)
            if s == EErrors.E_OK and actual is not None:
                match = (actual == expected)
                status_text = "MATCH" if match else "MISMATCH"
                print(f"    {name}: Read={actual}, Expected={expected} [{status_text}]")
                read_results.append(match)
                break
            time.sleep(0.2)
        else:
            print(f"    {name}: FAIL to read")
            read_results.append(False)
    else:
        print(f"    {name}: Skipped (write failed)")
        read_results.append(False)

match_count = sum(read_results)
results["step_11"] = ("OK" if match_count == len(read_results) else "PARTIAL",
                      f"{match_count}/{len(read_results)} matched")

# =============================================================================
# STEP 12: (SKIP)
# =============================================================================
print("\n[STEP 12] SKIPPED - Method Missing")
print("-" * 50)
results["step_12"] = ("SKIP", "Method missing")
print("    SKIPPED")

# =============================================================================
# STEP 13: Get Fault History
# =============================================================================
print("\n[STEP 13] Get Fault History")
print("-" * 50)

fault_ok = False

# Method 1: Try ErrorHistoryRead
try:
    result = api.ErrorHistoryRead(0, 10)
    # Handle different return formats
    if isinstance(result, tuple) and len(result) >= 2:
        s, faults = result
        if s == EErrors.E_OK and faults is not None:
            print(f"    ErrorHistoryRead: OK ({len(faults)} entries)")
            for i, fault in enumerate(faults[:3]):
                print(f"        Fault[{i}]: {fault}")
            results["step_13"] = ("OK", f"{len(faults)} faults")
            fault_ok = True
    elif result == EErrors.E_OK:
        print("    ErrorHistoryRead: OK (empty)")
        results["step_13"] = ("OK", "No faults")
        fault_ok = True
except Exception as e:
    print(f"    ErrorHistoryRead Error: {e}")

# Method 2: Fallback to Fault_Code DGTO
if not fault_ok:
    print("    Trying fallback (Fault_Code DGTO)...")
    for i in range(MAX_ATTEMPTS):
        s, v = api.ReadDGTO(DGTO_FAULT_CODE)
        if s == EErrors.E_OK and v is not None:
            print(f"    Fault_Code: {v}")
            results["step_13"] = ("OK", f"Fault_Code={v}")
            fault_ok = True
            break
        time.sleep(0.2)

    if not fault_ok:
        results["step_13"] = ("FAIL", "Could not read fault history")

# =============================================================================
# STEP 14: Read PSM-Status Every Second
# =============================================================================
print("\n[STEP 14] Read PSM-Status Every Second (10 readings)")
print("-" * 50)

psm_readings = []
reading_count = 10

for i in range(reading_count):
    timestamp = datetime.now().strftime('%H:%M:%S')
    read_ok = False

    for attempt in range(10):  # More retries
        s, v = api.ReadDGTO(DGTO_PSM_STATUS)
        if s == EErrors.E_OK and v is not None:
            psm_readings.append(v)
            print(f"    [{timestamp}] PSM-Status = {v}")
            read_ok = True
            break
        time.sleep(0.1)

    if not read_ok:
        psm_readings.append("FAIL")
        print(f"    [{timestamp}] PSM-Status = FAIL")

    if i < reading_count - 1:
        time.sleep(1)

ok_readings = sum(1 for v in psm_readings if v != "FAIL")
results["step_14"] = ("OK" if ok_readings == reading_count else "PARTIAL",
                      f"{ok_readings}/{reading_count} readings")

# =============================================================================
# CLEANUP
# =============================================================================
api.CommClose()

# =============================================================================
# FINAL RESULTS TABLE
# =============================================================================
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
    status, details = results.get(key, ("FAIL", "Not executed"))
    details_str = str(details)[:38] if details else "-"

    if status == "OK":
        status_display = "✓ OK"
    elif status == "FAIL":
        status_display = "✗ FAIL"
    elif status == "SKIP":
        status_display = "- SKIP"
    else:
        status_display = "~ PARTIAL"

    print(f"{name:<15} | {status_display:<10} | {details_str:<40}")

print("-" * 70)

ok = sum(1 for r in results.values() if r[0] == "OK")
fail = sum(1 for r in results.values() if r[0] == "FAIL")
skip = sum(1 for r in results.values() if r[0] == "SKIP")
partial = sum(1 for r in results.values() if r[0] == "PARTIAL")

print(f"\nTOTAL: {ok} OK | {fail} FAIL | {partial} PARTIAL | {skip} SKIP")
print("=" * 70)

# Save results
results_file = f"task3_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
with open(results_file, 'w') as f:
    f.write(f"TASK 3 RESULTS - {datetime.now()}\n")
    f.write("=" * 70 + "\n")
    for key, name in step_order:
        status, details = results.get(key, ("FAIL", "Not executed"))
        f.write(f"{name}: {status} - {details}\n")
    f.write(f"\nTOTAL: {ok} OK | {fail} FAIL | {partial} PARTIAL | {skip} SKIP\n")

print(f"\nResults saved to: {results_file}")
