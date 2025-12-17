from libs.TestLib import TestLib
from configs.Config import device_config

com = TestLib(device_config)

data_ids = [0x00510700, "2-4360-2", "2-4361-0", "2-4362-0"]

values = com.read_DataIdListFromCZO(data_ids, 0x005e0001)  # MultiRead of 4 DataID

if values is not None:
    print("MultiRead command OK")


for i in range(len(values)):
    values[i] = values[i] + 2

res = com.write_DataIdListToCZO(data_ids, 0x005e0001, values)   # MultiWrite of 4 DataID

if res:
    print("Write command OK")

val_read = com.read_DataIdFromCZO("2-4362-0", 0x005e0001)  # Single Read of DataID standard

if val_read is not None:
    print("Read on STANDARD DataType command OK")

res = com.write_DataIdToCZO("2-4362-0", 0x005e0001, val_read + 3)  # Single Write of DataID standard

if res:
    print("Write on STANDARD DataType command OK")

vals_read = com.read_DataIdFromCZO("22-1-2", 0x00640001)  # Read of DataID Array

if vals_read is not None:
    print("Read on ARRAY DataType command OK")

for i in range(len(vals_read)):
    if vals_read[i] > 1:
        vals_read[i] = vals_read[i] - 1
    else:
        vals_read[i] = vals_read[i] + 1

res = com.write_DataIdToCZO("22-1-2", 0x00640001, vals_read)  # Write of DataID Array

if res:
    print("Write on ARRAY DataType command OK")

com.update_report(True)
exit(0)
