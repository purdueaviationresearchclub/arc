"""
mock version of pressure_reader.py
implements values as defined by test_config.py
"""

import logging
from config import PSI_TO_PASCAL
import test_config

logger = logging.getLogger(__name__)


class MockPressureReader:
    def __init__(self, adc_channel: int = 0, psi_per_volt: float = 25.0,
                 psi_offset: float = -11.45, gain: int = 1):
        self.adc_channel = adc_channel
        if adc_channel == 0:
            self._value_func = test_config.make_pitot_value_func()
        else:
            self._value_func = test_config.make_static_value_func()
        self._connected = False

    def connect(self) -> None:
        self._connected = True
        mode = test_config.MODE
        logger.info(f"connected on channel {self.adc_channel} "
                    f"(mode={mode})")

    def read_psi(self) -> float:
        if not self._connected:
            raise ConnectionError("not connected")
        return self._value_func()

    def read_pascals(self) -> float:
        psi = self.read_psi()
        return psi * PSI_TO_PASCAL

    def disconnect(self) -> None:
        self._connected = False
        logger.info(f"channel {self.adc_channel} disconnected")
