"""
quick demo script for displaying psi of a transducer connected to labjack t7
voltage based with moving average
"""

# this lib must be installed!
# use `pip install labjack-ljm` in terminal to install
from labjack import ljm
# collections is a built-in lib
from collections import deque

# from regression
PSI_PER_VOLT = 25.0
PSI_OFFSET = -11.45

# input channel on t7
CHANNEL = 0

# moving average window
WINDOW_SIZE = 50
readings = deque(maxlen=WINDOW_SIZE)
running_sum = 0.0

handle = ljm.openS("T7", "ANY", "ANY")
info = ljm.getHandleInfo(handle)
print(f"Connected to ({info[2]})")

try:
    while True:
        volts = ljm.eReadName(handle, f"AIN{CHANNEL}")
        psi = (volts * PSI_PER_VOLT) + PSI_OFFSET

        # If deque is full, remove the oldest value from running sum
        if len(readings) == WINDOW_SIZE:
            running_sum -= readings[0]

        # Add new reading
        readings.append(psi)
        running_sum += psi

        # Calculate moving average
        average_psi = running_sum / len(readings)
        print(f"\r{volts:.4f}V {average_psi:.2f}psi", end="", flush=True)
except KeyboardInterrupt:
    print("\nStopped.")
finally:
    ljm.close(handle)