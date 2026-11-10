"""
PFD Formatter

LLR-007: airspeedKnots = airspeedMetersPerSec * 1.94384
LLR-008: write airspeedKnots to the PFD
LLR-002: write altitude to the PFD
"""

import logging
from config import MPS_TO_KNOTS, FPS_TO_FPM
from adiru.air_data_computer.data_types import AirData

logger = logging.getLogger(__name__)


def convert_ias_mps_to_knots(ias_mps: float) -> float:
    """
    converts indicated airspeed from m/s to knots
    IAS_knots = IAS_m/s * 1.94384
    result as AirDataComputerOutputProcessing:airspeedKnots
    """
    return ias_mps * MPS_TO_KNOTS


def convert_vs_fps_to_fpm(vs_fps: float) -> float:
    """ft/s to ft/min for PFD"""
    return vs_fps * FPS_TO_FPM


def format_for_pfd(air_data: AirData) -> dict:
    """
    converts AirData into a keyword dict for PFD.set()

    air_data: The AirData object produced by the Compute layer.

    returns dict for passing to PrimaryFlightDisplay.set(**result).
    """
    return {
        "airspeed_kts": convert_ias_mps_to_knots(air_data.ias_mps),
        "altitude_ft": air_data.altitude_ft,
        "vsi_fpm": convert_vs_fps_to_fpm(air_data.vertical_speed_fps),
    }
