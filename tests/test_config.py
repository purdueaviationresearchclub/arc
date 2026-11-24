"""
basic config for mockup
only static or dynamic
"""

import math
import time

# 'static' or 'dynamic' refers to pressure value type
# this does not refer to read type, only input variability
MODE = "dynamic"

STATIC_SCENARIOS = {
    "sea_level_zero_airspeed": {
        "pitot_psi": 14.6959,
        "static_psi": 14.6959,
    },
    "sea_level_100kts": {
        "pitot_psi": 14.931,
        "static_psi": 14.6959,
    },
    "sea_level_150kts": {
        "pitot_psi": 15.225,
        "static_psi": 14.6959,
    },

    "altitude_5000ft_120kts": {
        "pitot_psi": 12.55,
        "static_psi": 12.23,
    },
    # example on how to create custom
    "custom": {
        "pitot_psi": 14.8,
        "static_psi": 14.6959,
    },
}

ACTIVE_SCENARIO = "sea_level_150kts"

DYNAMIC_CONFIG = {
    "static_psi_base": 14.6959,
    "static_psi_amplitude": 0.8,
    "static_psi_frequency_hz": 0.05,

    "pitot_psi_base": 15.0,
    "pitot_psi_amplitude": 0.4,
    "pitot_psi_frequency_hz": 0.1,
}

PSI_PER_VOLT = 25.0
PSI_OFFSET = -11.45


def volts_to_psi(volts: float) -> float:
    return (volts * PSI_PER_VOLT) + PSI_OFFSET

def make_static_value_func():
    if MODE == "static":
        scenario = STATIC_SCENARIOS[ACTIVE_SCENARIO]
        value = scenario["static_psi"]
        return lambda: value
    else:
        cfg = DYNAMIC_CONFIG
        base = cfg["static_psi_base"]
        amp = cfg["static_psi_amplitude"]
        freq = cfg["static_psi_frequency_hz"]
        start = time.time()
        return lambda: base + amp * math.sin(2 * math.pi * freq * (time.time() - start))


def make_pitot_value_func():
    if MODE == "static":
        scenario = STATIC_SCENARIOS[ACTIVE_SCENARIO]
        value = scenario["pitot_psi"]
        return lambda: value
    else:
        cfg = DYNAMIC_CONFIG
        base = cfg["pitot_psi_base"]
        amp = cfg["pitot_psi_amplitude"]
        freq = cfg["pitot_psi_frequency_hz"]
        start = time.time()
        return lambda: base + amp * math.sin(2 * math.pi * freq * (time.time() - start))
