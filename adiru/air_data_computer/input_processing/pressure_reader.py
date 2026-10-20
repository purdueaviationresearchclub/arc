"""
reads raw voltage from a pressure transducer and converts to psi
"""

import logging
import busio
import board
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

logger = logging.getLogger(__name__)

PSI_TO_PASCAL = 6894.76

class PressureReader:    
    def __init__(
        self,
        adc_channel: int = 0, # ADS1115 channel
        psi_per_volt: float = 25.0, # slope
        psi_offset: float = -11.45, # y-intercept
        gain: int = 1 # gain amplifier
    ):
        self.adc_channel = adc_channel
        self.psi_per_volt = psi_per_volt
        self.psi_offset = psi_offset
        self.gain = gain
        self._adc = None
        self._channel = None

    def connect(self) -> None:
        i2c = busio.I2C(board.SCL, board.SDA)
        self._adc = ADS1115(i2c, gain=self.gain)
        self._channel = AnalogIn(self._adc, self.adc_channel)
        logger.info("connected")

    def read_psi(self) -> float:
        if self._channel is None:
            raise ConnectionError("not initialized")

        volts = self._channel.voltage
        psi = (volts * self.psi_per_volt) + self.psi_offset
        return psi

    def read_pascals(self) -> float:
        psi = self.read_psi()
        return psi * PSI_TO_PASCAL

    def disconnect(self) -> None:
        self._channel = None
        self._adc = None
        logger.info("connection closed")