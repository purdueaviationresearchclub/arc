"""
LLR-006 Indicated Airspeed Meters Per Sec
"""

import math

# as defined in LLR-006
RHO_0 = 1.225 

def compute_ias_meters_per_sec(p_total_pa: float, p_static_pa: float) -> float:
    """
    IAS in meters per second
    
    p_total_pa: total (pitot) pressure in pascals.
    p_static_pa: static pressure in pascals.
    
    returns 0.0 if differential pressure is negative or zero
    """
    differential_pressure = p_total_pa - p_static_pa
    
    if differential_pressure <= 0:
        return 0.0
        
    ias = math.sqrt((2 * differential_pressure) / RHO_0)
    return ias
