"""
quick demo script for displaying psi of a transducer connected to labjack t7
voltage based
"""

# this lib must be installed! 
# use `pip install labjack-ljm` in terminal to install
from labjack import ljm

# from regression
PSI_PER_VOLT = 25.0
PSI_OFFSET = -11.45

# input channel on t7
CHANNEL = 0

handle = ljm.openS("T7", "ANY", "ANY")
info = ljm.getHandleInfo(handle)
print(f"Connected to ({info[2]})")

try:
    while True:
        volts = ljm.eReadName(handle, f"AIN{CHANNEL}")
        psi = (volts * PSI_PER_VOLT) + PSI_OFFSET
        print(f"\r{volts:.4f}V {psi:.2f}psi   ", end="", flush=True)
except KeyboardInterrupt:
    print("\nStopped.")
finally:
    ljm.close(handle)
