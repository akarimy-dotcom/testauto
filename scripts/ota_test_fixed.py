"""
================================================================================
OTA TEST AUTOMATION - FIXED VERSION
================================================================================
Fixes:
  - E_IDENT error: Proper device initialization before TDA operations
  - DFLS path: Correct file path
  - Added device ping/verification before operations
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
from pymtstestlib.api import API
from pymtstestlib.shared.error_defs import EErrors
from pymtstestlib.shared.export_defs import SMapDGTO
from pymtstestlib.shared.utils import SWAP

print("[OK] pymtstestlib imported")

# =============================================================================
# CONFIGURATION - FIXED PATHS
# =============================================================================

# Communication
COM_PORT = "//./COM5"
BAUDRATE = 38400

# Files - CORRECTED PATHS
FWPRJ_FILE = r"C:\Alireza\Alireza\TDM4_Test\TDM4_RX130_ATG485_70_26_05.fwprj"
DFLS_FILE = r"C:\Alireza\Alireza\TDM4_Test\sources\0x0048_PCM5_ver00.02.00-SAT.dfls"

# Test values
TDA_TEST_VALUE = "121212121212"  # As Pablo specified
FACTORY_CODE = "0101010101010101010101010101"

# Timing
MAX_ATTEMPTS = 30
POST_STARTUP_DELAY = 5  # Wait after startup
POST_RESET_DELAY = 10

# DGTO Helper
def dgto(code):
    """Convert D-G-T-O string to address"""
    return SWAP(SMapDGTO(code).dgto)

# Key DGTOs
DGTO_TDM_STATUS = dgto("10-0-6-22")
DGTO_FAULT_CODE = dgto("5-1-2-3")
DGTO_PSM_STATUS = dgto("4-11-6-25")

# ADJ DGTOs for Steps 8-9
ADJ_DGTOS = [
    ("FANHMAX", dgto("10-0-2-24"), 1500),
    ("FANCMAX", dgto("10-0-2-26"), 1400),
    ("FANCMIN", dgto("10-0-2-27"), 400),
]

# =============================================================================
# LOGGING
# =============================================================================

def log(msg, level="INFO"):
    ts = datetime.now().strftime('%H:%M:%S')
    sym = {"INFO": "   ", "OK": " ✓ ", "FAIL": " ✗ ", "WARN": " ⚠ ", "STEP": ">>>"}
    print(f"[{ts}]{sym.get(level, '   ')}{msg}")

# =============================================================================
# MAIN TEST
# =============================================================================

print("=" * 70)
print("  OTA TEST - FIXED VERSION")
print("=" * 70)
print(f"  Time: {datetime.now()}")
print(f"  COM: {COM_PORT}")
print(f"  FWPRJ: {FWPRJ_FILE}")
print(f"  DFLS: {DFLS_FILE}")
print("=" * 70)

# Check files exist
if not os.path.exists(FWPRJ_FILE):
    print(f"[ERROR] FWPRJ file not found: {FWPRJ_FILE}")
    sys.exit(1)
else:
    print(f"[OK] FWPRJ file exists")

if os.path.exists(DFLS_FILE):
    print(f"[OK] DFLS file exists")
else:
    print(f"[WARN] DFLS file not found: {DFLS_FILE}")

results = {}

# =============================================================================
# INITIALIZE API
# =============================================================================
log("INITIALIZING COMMUNICATION", "STEP")
log("-" * 50)

api = API()

# Step 1: Open COM port
log(f"Opening COM port: {COM_PORT}")
try:
    api.CommOpen(COM_PORT, BAUDRATE)
    log("COM port opened", "OK")
except Exception as e:
    log(f"COM port error: {e}", "FAIL")
    sys.exit(1)

time.sleep(2)

# Step 2: System startup with FWPRJ (CRITICAL - fixes E_IDENT error)
log(f"System startup from FWPRJ...")
try:
    api.system_startup_from_file(FWPRJ_FILE)
    log("System startup complete", "OK")
except Exception as e:
    log(f"System startup error: {e}", "FAIL")
    api.CommClose()
    sys.exit(1)

# Wait for device to be ready
log(f"Waiting {POST_STARTUP_DELAY}s for device to be ready...")
time.sleep(POST_STARTUP_DELAY)

# Step 3: Verify communication by reading a DGTO
log("Verifying device communication...")
device_ready = False
for i in range(MAX_ATTEMPTS):
    s, v = api.ReadDGTO(DGTO_TDM_STATUS)
    if s == EErrors.E_OK and v is not None:
        log(f"Device ready! TDM_STATUS = {v}", "OK")
        device_ready = True
        break
    time.sleep(0.3)

if not device_ready:
    log("Device not responding!", "FAIL")
    log("Check: Is device powered? Is COM port correct?", "WARN")
    api.CommClose()
    sys.exit(1)

# =============================================================================
# STEP 1: SW Download (Skip - no method)
# =============================================================================
log("STEP 1: SW Download", "STEP")
log("-" * 50)
log("SKIPPED - No method available")
results["step_1"] = ("SKIP", "No method")

# =============================================================================
# STEP 2: Write TDA and Read TDA
# =============================================================================
log("STEP 2: Write TDA and Verify", "STEP")
log("-" * 50)

write_ok = False
read_ok = False
tda_read = None

# Write TDA
log(f"Writing TDA: {TDA_TEST_VALUE}")
for attempt in range(MAX_ATTEMPTS):
    try:
        s = api.TDAWriteInfo(TDA_TEST_VALUE, "")
        if s == EErrors.E_OK:
            log("TDAWriteInfo: OK", "OK")
            # Register the TDA
            api.TDARegisterTest(1)
            write_ok = True
            break
        elif s == EErrors.E_IDENT:
            log(f"TDAWriteInfo attempt {attempt+1}: E_IDENT (device not ready)", "WARN")
            time.sleep(1)
        else:
            log(f"TDAWriteInfo attempt {attempt+1}: {s}", "WARN")
            time.sleep(0.5)
    except Exception as e:
        log(f"TDAWriteInfo exception: {e}", "FAIL")
        time.sleep(0.5)

if not write_ok:
    log("TDAWriteInfo failed after all attempts", "FAIL")

time.sleep(2)

# Read TDA
log("Reading TDA...")
for attempt in range(MAX_ATTEMPTS):
    try:
        result = api.TDAReadInfo()

        if isinstance(result, tuple) and len(result) >= 2:
            s, info = result[0], result[1]
            if s == EErrors.E_OK and info is not None:
                # Extract TDA code
                if hasattr(info, 'code'):
                    try:
                        tda_read = info.code.hex() if isinstance(info.code, bytes) else str(info.code)
                    except:
                        tda_read = str(info.code)
                else:
                    tda_read = str(info)

                log(f"TDAReadInfo: {tda_read}", "OK")
                read_ok = True

                # Verify
                if TDA_TEST_VALUE.lower() in tda_read.lower():
                    log("TDA VERIFIED - Match!", "OK")
                else:
                    log(f"TDA MISMATCH: expected '{TDA_TEST_VALUE}'", "WARN")
                break
            elif s == EErrors.E_IDENT:
                log(f"TDAReadInfo attempt {attempt+1}: E_IDENT", "WARN")
                time.sleep(1)
            else:
                log(f"TDAReadInfo attempt {attempt+1}: {s}", "WARN")
                time.sleep(0.5)
        else:
            # Single return value
            if result == EErrors.E_OK:
                log("TDAReadInfo: OK (no data)", "OK")
                read_ok = True
                break
            else:
                log(f"TDAReadInfo attempt {attempt+1}: {result}", "WARN")
                time.sleep(0.5)
    except Exception as e:
        log(f"TDAReadInfo exception: {e}", "FAIL")
        time.sleep(0.5)

results["step_2_write"] = ("OK" if write_ok else "FAIL", TDA_TEST_VALUE)
results["step_2_read"] = ("OK" if read_ok else "FAIL", tda_read or "Failed")

# =============================================================================
# STEPS 3-6: Download DFLS
# =============================================================================
log("STEPS 3-6: Download DFLS", "STEP")
log("-" * 50)

if not os.path.exists(DFLS_FILE):
    log(f"DFLS file not found: {DFLS_FILE}", "WARN")
    log("Checking alternative locations...")

    # Try alternative paths
    alt_paths = [
        r"C:\Alireza\Alireza\TDM4_Test\0x0048_PCM5_ver00.02.00-SAT.dfls",
        r"C:\Alireza\Alireza\TDM4_Test\sources\0x0048_PCM5_ver00.02.00-SAT.dfls",
        os.path.join(PROJECT_ROOT, "0x0048_PCM5_ver00.02.00-SAT.dfls"),
        os.path.join(PROJECT_ROOT, "sources", "0x0048_PCM5_ver00.02.00-SAT.dfls"),
    ]

    for path in alt_paths:
        if os.path.exists(path):
            DFLS_FILE = path
            log(f"Found DFLS at: {path}", "OK")
            break
    else:
        # List what files ARE in the sources folder
        sources_dir = os.path.join(PROJECT_ROOT, "sources")
        if os.path.exists(sources_dir):
            log(f"Files in {sources_dir}:")
            for f in os.listdir(sources_dir):
                log(f"  - {f}")

        results["step_3_6"] = ("SKIP", "DFLS file not found")

if os.path.exists(DFLS_FILE):
    log(f"DFLS File: {DFLS_FILE}")
    log(f"Factory Code: {FACTORY_CODE}")

    try:
        success = api.DflsMapDownload(DFLS_FILE, FACTORY_CODE)
        if success:
            log("DflsMapDownload started", "OK")

            # Wait for download to complete
            for i in range(150):  # 5 minutes max
                try:
                    result = api.GetDownloadInfo()
                    if isinstance(result, tuple):
                        s, info = result
                        if hasattr(info, 'progress'):
                            log(f"Progress: {info.progress}%")
                        if hasattr(info, 'status'):
                            if info.status == 3:
                                log("DFLS Download COMPLETE", "OK")
                                results["step_3_6"] = ("OK", "Downloaded")
                                break
                            elif info.status == 4:
                                log(f"DFLS Download ERROR: status={info.status}", "FAIL")
                                results["step_3_6"] = ("FAIL", "Download error")
                                break
                except Exception as e:
                    pass
                time.sleep(2)
            else:
                log("DFLS Download timeout", "WARN")
                results["step_3_6"] = ("PARTIAL", "Timeout")
        else:
            log("DflsMapDownload failed to start", "FAIL")
            results["step_3_6"] = ("FAIL", "Failed to start")
    except Exception as e:
        log(f"DFLS error: {e}", "FAIL")
        results["step_3_6"] = ("FAIL", str(e))

# =============================================================================
# STEP 7: Get Device Info
# =============================================================================
log("STEP 7: Get Device Info", "STEP")
log("-" * 50)

device_info = {}

# Read TDM Status
s, v = api.ReadDGTO(DGTO_TDM_STATUS)
if s == EErrors.E_OK:
    device_info["TDM_STATUS"] = v
    log(f"TDM_STATUS: {v}", "OK")

# Read Fault Code
s, v = api.ReadDGTO(DGTO_FAULT_CODE)
if s == EErrors.E_OK:
    device_info["Fault_Code"] = v
    log(f"Fault_Code: {v}", "OK")

# Try ReadPSoleFwAttr
try:
    result = api.ReadPSoleFwAttr()
    if isinstance(result, tuple) and len(result) >= 4:
        s, desc, prod_id, ares_ver = result
        if s:
            device_info["Description"] = desc
            device_info["ProductID"] = prod_id
            device_info["ARES_Ver"] = ares_ver
            log(f"Description: {desc}", "OK")
            log(f"Product ID: {prod_id}", "OK")
except:
    pass

if device_info:
    results["step_7"] = ("OK", str(device_info))
else:
    results["step_7"] = ("FAIL", "No info obtained")

# =============================================================================
# STEPS 8-9: Write ADJ DGTOs
# =============================================================================
log("STEPS 8-9: Write ADJ DGTOs", "STEP")
log("-" * 50)

written_dgtos = []
for name, addr, value in ADJ_DGTOS:
    log(f"Writing {name} = {value}...")
    success = False

    for attempt in range(MAX_ATTEMPTS):
        s = api.WriteDGTO(addr, value)
        if s == EErrors.E_OK:
            log(f"  {name}: OK", "OK")
            written_dgtos.append((name, addr, value, True))
            success = True
            break
        time.sleep(0.2)

    if not success:
        log(f"  {name}: FAIL", "FAIL")
        written_dgtos.append((name, addr, value, False))

    time.sleep(0.3)

ok_count = sum(1 for d in written_dgtos if d[3])
results["step_8_9"] = ("OK" if ok_count == len(ADJ_DGTOS) else "PARTIAL",
                       f"{ok_count}/{len(ADJ_DGTOS)}")

# =============================================================================
# STEP 10: Send Reset
# =============================================================================
log("STEP 10: Send Reset", "STEP")
log("-" * 50)

reset_ok = False
for attempt in range(MAX_ATTEMPTS):
    s = api.ErrorHistoryReset()
    if s == EErrors.E_OK:
        log("ErrorHistoryReset: OK", "OK")
        reset_ok = True
        break
    time.sleep(0.2)

if reset_ok:
    log(f"Waiting {POST_RESET_DELAY}s for device to stabilize...")
    time.sleep(POST_RESET_DELAY)
    results["step_10"] = ("OK", "Reset sent")
else:
    log("ErrorHistoryReset failed", "FAIL")
    results["step_10"] = ("FAIL", "Failed")

# =============================================================================
# STEP 11: Read Back DGTOs
# =============================================================================
log("STEP 11: Read Back DGTOs", "STEP")
log("-" * 50)

match_count = 0
for name, addr, expected, was_written in written_dgtos:
    if not was_written:
        log(f"  {name}: Skipped (write failed)")
        continue

    s, actual = api.ReadDGTO(addr)
    if s == EErrors.E_OK and actual is not None:
        if actual == expected:
            log(f"  {name}: {actual} == {expected} [MATCH]", "OK")
            match_count += 1
        else:
            log(f"  {name}: {actual} != {expected} [MISMATCH]", "WARN")
    else:
        log(f"  {name}: Read failed", "FAIL")

total_written = sum(1 for d in written_dgtos if d[3])
results["step_11"] = ("OK" if match_count == total_written else "PARTIAL",
                      f"{match_count}/{total_written}")

# =============================================================================
# STEP 12: Skip
# =============================================================================
log("STEP 12: (Skipped - Method Missing)", "STEP")
results["step_12"] = ("SKIP", "Method missing")

# =============================================================================
# STEP 13: Fault History
# =============================================================================
log("STEP 13: Fault History", "STEP")
log("-" * 50)

fault_ok = False
try:
    result = api.ErrorHistoryRead(0, 10)
    if isinstance(result, tuple) and len(result) >= 2:
        s, faults = result
        if s == EErrors.E_OK and faults:
            log(f"ErrorHistoryRead: {len(faults)} entries", "OK")
            for i, f in enumerate(faults[:3]):
                log(f"  Fault[{i}]: {f}")
            results["step_13"] = ("OK", f"{len(faults)} faults")
            fault_ok = True
except Exception as e:
    log(f"ErrorHistoryRead error: {e}", "WARN")

if not fault_ok:
    # Fallback
    s, v = api.ReadDGTO(DGTO_FAULT_CODE)
    if s == EErrors.E_OK:
        log(f"Fault_Code: {v}", "OK")
        results["step_13"] = ("OK", f"Fault_Code={v}")
    else:
        results["step_13"] = ("FAIL", "Could not read")

# =============================================================================
# STEP 14: PSM-Status Loop
# =============================================================================
log("STEP 14: Read PSM-Status (10 readings)", "STEP")
log("-" * 50)

psm_readings = []
for i in range(10):
    ts = datetime.now().strftime('%H:%M:%S')

    s, v = api.ReadDGTO(DGTO_PSM_STATUS)
    if s == EErrors.E_OK and v is not None:
        psm_readings.append(v)
        log(f"[{ts}] PSM-Status = {v}")
    else:
        psm_readings.append("FAIL")
        log(f"[{ts}] PSM-Status = FAIL", "WARN")

    if i < 9:
        time.sleep(1)

ok_readings = sum(1 for v in psm_readings if v != "FAIL")
results["step_14"] = ("OK" if ok_readings == 10 else "PARTIAL",
                      f"{ok_readings}/10")

# =============================================================================
# CLEANUP
# =============================================================================
api.CommClose()
log("COM port closed", "OK")

# =============================================================================
# FINAL RESULTS
# =============================================================================
print("\n" + "=" * 70)
print("  FINAL RESULTS")
print("=" * 70)

step_names = [
    ("step_1", "SW Download"),
    ("step_2_write", "WriteTDA"),
    ("step_2_read", "ReadTDA"),
    ("step_3_6", "DFLS Download"),
    ("step_7", "Device Info"),
    ("step_8_9", "Write DGTOs"),
    ("step_10", "Reset"),
    ("step_11", "Read DGTOs"),
    ("step_12", "Step 12"),
    ("step_13", "Fault History"),
    ("step_14", "PSM-Status"),
]

print(f"{'Step':<15} | {'Status':<10} | {'Details':<40}")
print("-" * 70)

counts = {"OK": 0, "FAIL": 0, "PARTIAL": 0, "SKIP": 0}
for key, name in step_names:
    status, details = results.get(key, ("FAIL", "Not run"))
    counts[status] = counts.get(status, 0) + 1
    sym = {"OK": "✓", "FAIL": "✗", "PARTIAL": "~", "SKIP": "-"}[status]
    print(f"{name:<15} | {sym} {status:<7} | {str(details)[:38]:<40}")

print("-" * 70)
print(f"TOTAL: {counts['OK']} OK | {counts['FAIL']} FAIL | {counts['PARTIAL']} PARTIAL | {counts['SKIP']} SKIP")
print("=" * 70)

# Save results
filename = f"ota_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
with open(os.path.join(PROJECT_ROOT, filename), 'w') as f:
    f.write(f"OTA Test Results - {datetime.now()}\n")
    f.write("=" * 70 + "\n")
    for key, (status, details) in results.items():
        f.write(f"{key}: {status} - {details}\n")
print(f"\nResults saved to: {filename}")
