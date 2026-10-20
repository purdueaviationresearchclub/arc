"""
reads raw voltage from a pressure transducer via LabJack T7 and applies formula to convert to psi
"""

import logging
from labjack import ljm

logger = logging.getLogger(__name__)

PSI_TO_PASCAL = 6894.76


class PressureReaderT7:
    def __init__(self, channel: int = 0, psi_per_volt: float = 25.0, psi_offset: float = -11.45):
        """
        inits reader
        channel: AIN channel number on T7
        psi_per_volt: slope from transducer curve
        psi_offset: y-intercept from transducer curve
        """
        self.channel = channel
        self.psi_per_volt = psi_per_volt
        self.psi_offset = psi_offset
        self.handle = None

    def connect(self) -> None:
        """opens connection to T7"""
        self.handle = ljm.openS("T7", "ANY", "ANY")
        info = ljm.getHandleInfo(self.handle)
        logger.info(f"connected to {info[2]}")

    def read_psi(self) -> float:
        """
        reads voltage and applies linear regression to output psi
        """
        if self.handle is None:
            raise ConnectionError("not connected")

        volts = ljm.eReadName(self.handle, f"AIN{self.channel}")
        psi = (volts * self.psi_per_volt) + self.psi_offset
        return psi

    def read_pascals(self) -> float:
        """reads psi and converts to pascals for use by ADIRU"""
        psi = self.read_psi()
        return psi * PSI_TO_PASCAL

    def disconnect(self) -> None:
        """closes the connection"""
        if self.handle is not None:
            ljm.close(self.handle)
            logger.info("connection closed")
            self.handle = None
