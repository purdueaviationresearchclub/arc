"""
quick demo script for calculating altitude, airspeed, and vertical speed
from two pressure transducers connected to labjack t7
voltage based with moving average
"""

# this lib must be installed!
# use `pip install labjack-ljm` in terminal to install
from labjack import ljm
# collections and time and math are built-in libs
from collections import deque
import math
import time

# from regression
PSI_PER_VOLT = 25.0
PSI_OFFSET = -11.45
PA_PER_PSI = 6894.757

# input channels on t7
STATIC_CHANNEL = 0  # side of aircraft
PITOT_CHANNEL = 1   # front of aircraft

# air constants
AIR_TEMP_K = 288.15  # assumed air temp
R_AIR = 287.058      # J/(kg*K)

# moving average window
WINDOW_SIZE = 50
static_readings = deque(maxlen=WINDOW_SIZE)
static_sum = 0.0
pitot_readings = deque(maxlen=WINDOW_SIZE)
pitot_sum = 0.0

# (time, altitude) readings used for vertical speed
alt_readings = deque(maxlen=WINDOW_SIZE)

# pressure on the ground, set once the first window is full
ref_pressure = None

handle = ljm.openS("T7", "ANY", "ANY")
info = ljm.getHandleInfo(handle)
print(f"Connected to ({info[2]})")

try:
    while True:
        static_volts, pitot_volts = ljm.eReadNames(
            handle, 2, [f"AIN{STATIC_CHANNEL}", f"AIN{PITOT_CHANNEL}"]
        )
        static_pa = (static_volts * PSI_PER_VOLT + PSI_OFFSET) * PA_PER_PSI
        pitot_pa = (pitot_volts * PSI_PER_VOLT + PSI_OFFSET) * PA_PER_PSI

        # If deques are full, remove the oldest value from running sums
        if len(static_readings) == WINDOW_SIZE:
            static_sum -= static_readings[0]
            pitot_sum -= pitot_readings[0]

        # Add new readings
        static_readings.append(static_pa)
        pitot_readings.append(pitot_pa)
        static_sum += static_pa
        pitot_sum += pitot_pa

        # Calculate moving averages
        static_avg = static_sum / len(static_readings)
        pitot_avg = pitot_sum / len(pitot_readings)

        # Save reference pressure once the window is full
        if ref_pressure is None:
            if len(static_readings) == WINDOW_SIZE:
                ref_pressure = static_avg
            continue

        # Altitude (m) from static pressure
        altitude = 44330.77 * (1 - (static_avg / ref_pressure) ** 0.190263)

        # Airspeed (m/s) from dynamic pressure and density
        dynamic_pa = max(pitot_avg - static_avg, 0.0)
        density = static_avg / (R_AIR * AIR_TEMP_K)  # kg/m^3
        airspeed = math.sqrt(2 * dynamic_pa / density)

        # Vertical speed (m/s) = dH/dt over the window
        now = time.time()
        alt_readings.append((now, altitude))
        old_time, old_altitude = alt_readings[0]
        if now > old_time:
            vertical_speed = (altitude - old_altitude) / (now - old_time)
        else:
            vertical_speed = 0.0

        print(f"\r{altitude:.1f}m {airspeed:.2f}m/s {vertical_speed:+.2f}m/s vert", end="", flush=True)
except KeyboardInterrupt:
    print("\nStopped.")
finally:
    ljm.close(handle)
