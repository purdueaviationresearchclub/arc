"""
tests to verify math
"""

import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from adiru.air_data_computer.compute.airspeed import compute_ias_meters_per_sec
from adiru.air_data_computer.compute.altitude import compute_altitude_ft
from adiru.air_data_computer.output_processing import convert_ias_mps_to_knots


def test_altitude_sea_level():
    result = compute_altitude_ft(config.P0_PSI)
    expected = 0.0
    status = "pass" if abs(result - expected) < 0.1 else "fail"
    print(f"[{status}] test_altitude_sea_level: "
          f"input={config.P0_PSI} PSI, got={result:.2f} ft, expected={expected:.2f} ft")


def test_altitude_5000ft():
    h_target = 5000.0
    p_expected = config.P0_PSI * (1 - h_target / config.ALT_SCALE_FT) ** (1.0 / config.ALT_EXPONENT)
    result = compute_altitude_ft(p_expected)
    status = "pass" if abs(result - h_target) < 100.0 else "fail"
    print(f"[{status}] test_altitude_5000ft: "
          f"input={p_expected:.4f} PSI, got={result:.1f} ft, expected={h_target:.0f} ft")


def test_altitude_invalid_pressure():
    result = compute_altitude_ft(0.0)
    status = "pass" if result == 0.0 else "fail"
    print(f"[{status}] test_altitude_invalid_pressure: "
          f"input=0.0 PSI, got={result:.2f} ft, expected=0.0 ft")


def test_airspeed_zero_differential():
    pressure_pa = 14.6959 * config.PSI_TO_PASCAL
    result = compute_ias_meters_per_sec(pressure_pa, pressure_pa)
    expected = 0.0
    status = "pass" if result == expected else "fail"
    print(f"[{status}] test_airspeed_zero_differential: "
          f"got={result:.2f} m/s, expected={expected:.2f} m/s")


def test_airspeed_known_value():
    static_pa = 101325.0
    target_mps = 100.0
    delta_p = 0.5 * config.RHO_0 * target_mps ** 2
    pitot_pa = static_pa + delta_p

    result = compute_ias_meters_per_sec(pitot_pa, static_pa)
    expected = target_mps
    status = "pass" if abs(result - expected) < 0.5 else "fail"
    print(f"[{status}] test_airspeed_known_value: "
          f"got={result:.2f} m/s, expected={expected:.2f} m/s")


def test_airspeed_negative_differential():
    result = compute_ias_meters_per_sec(100000.0, 101325.0)
    expected = 0.0
    status = "pass" if result == expected else "fail"
    print(f"[{status}] test_airspeed_negative_differential: "
          f"got={result:.2f} m/s, expected={expected:.2f} m/s")


def test_knots_conversion():
    result = convert_ias_mps_to_knots(100.0)
    expected = 194.384
    status = "pass" if abs(result - expected) < 0.01 else "fail"
    print(f"[{status}] test_knots_conversion: "
          f"input=100.0 m/s, got={result:.3f} kts, expected={expected:.3f} kts")


def test_knots_zero():
    result = convert_ias_mps_to_knots(0.0)
    expected = 0.0
    status = "pass" if result == expected else "fail"
    print(f"[{status}] test_knots_zero: "
          f"input=0.0 m/s, got={result:.3f} kts, expected={expected:.3f} kts")


def test_psi_to_pascals():
    result = 1.0 * config.PSI_TO_PASCAL
    expected = 6894.76
    status = "pass" if abs(result - expected) < 0.01 else "fail"
    print(f"[{status}] test_psi_to_pascals: "
          f"1 PSI = {result:.2f} Pa, expected={expected:.2f} Pa")


def test_sea_level_pressure():
    result = config.P0_PSI
    expected = 14.6959
    status = "pass" if abs(result - expected) < 0.0001 else "fail"
    print(f"[{status}] test_sea_level_pressure: "
          f"P0_PSI={result}, expected={expected}")


def main():
    test_sea_level_pressure()
    test_psi_to_pascals()
    test_altitude_sea_level()
    test_altitude_5000ft()
    test_altitude_invalid_pressure()
    test_airspeed_zero_differential()
    test_airspeed_known_value()
    test_airspeed_negative_differential()
    test_knots_conversion()
    test_knots_zero()
    print("tests complete")


if __name__ == "__main__":
    main()
