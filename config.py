"""
configuration for ADIRU
"""

PITOT_PSI_PER_VOLT = 25.0
PITOT_PSI_OFFSET = -11.45
STATIC_PSI_PER_VOLT = 25.0
STATIC_PSI_OFFSET = -11.45

# ADC settings
PITOT_ADC_CHANNEL = 0  # ADS1115 channel for pitot transducer
STATIC_ADC_CHANNEL = 1  # ADS1115 channel for static transducer
ADC_GAIN = 1  # 1 = +- 4.096V range

# units
PSI_TO_PASCAL = 6894.76  # Psi to Pascals (LLR-004, LLR-005)
MPS_TO_KNOTS = 1.94384  # m/s to knots (LLR-007)
FPS_TO_FPM = 60  # ft/s to ft/min (for PFD vsi_fpm)

# isa constant for airspeed compute
RHO_0 = 1.225  # kg/m^3, sea-level air density (LLR-006)

# barometric alttiude constants
# h = ALT_SCALE_FT * (1 - (P_static_psi / P0_PSI) ^ ALT_EXPONENT)
P0_PSI = 14.6959  # sea level standard atmospheric pressure (Psi)
ALT_SCALE_FT = 145366.45  # scale factor for altitude in feet
ALT_EXPONENT = 0.19026  # exponent per LLR-001

# vertical speed
VS_WINDOW_SIZE = 50  # number of samples in window

# display
PFD_FPS = 60  # PFD refresh rate
SENSOR_HZ = 50  # sensor read rate, max about 860
