"""
LLR-001: Altitude Computation
h = 145366.45 * (1 - (P_static / P_0) ^ 0.19026)
"""

import logging
from config import P0_PSI, ALT_SCALE_FT, ALT_EXPONENT

logger = logging.getLogger(__name__)


def compute_altitude_ft(static_pressure_psi: float) -> float:
    """
    altitude in feet
    static_pressure_psi: static pressure in PSI.
    """
    if static_pressure_psi <= 0:
        logger.warning("invalid static pressure: %.4f PSI", static_pressure_psi)
        return 0.0

    if P0_PSI <= 0:
        logger.error("invalid P0_PSI constant: %.4f", P0_PSI)
        return 0.0

    altitude_ft = ALT_SCALE_FT * (1 - (static_pressure_psi / P0_PSI) ** ALT_EXPONENT)
    return altitude_ft
