"""
data types for the ADIRU
"""

from dataclasses import dataclass


@dataclass
class PressureData:
    """
    LLR-001 (altitude) uses raw PSI directly
    LLR-006 (airspeed) uses converted Pascals

    LLR-004 and LLR-005 (deprecated?)
    PSI values correspond to PitotStaticInputSignals:pitotPressure / staticPressure.
    Pa values correspond to AirDataComputerInputProcessing:pitotPressurePa / staticPressurePa
    """
    pitot_pressure_psi: float
    static_pressure_psi: float
    pitot_pressure_pa: float
    static_pressure_pa: float


@dataclass
class AirData:
    """
    ias_mps: meters per second (LLR-006: AirDataComputer:airspeedMetersPerSec)
    altitude_ft: feet (LLR-001: AirDataComputer:altitude)
    vertical_speed_fps: feet per second (from dH/dt of altitude)
    """
    ias_mps: float = 0.0
    altitude_ft: float = 0.0
    vertical_speed_fps: float = 0.0
