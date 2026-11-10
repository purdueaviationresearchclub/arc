"""
LLR-010: Vertical Speed Computation
VS = dH / dt

consideration
LLR-011 (dp/dh = -rho(h) * g)
LLR-013 (VS = -(dp/dt) / (rho * g))
"""

import logging
import time
from collections import deque
from config import VS_WINDOW_SIZE, FPS_TO_FPM

logger = logging.getLogger(__name__)


class VerticalSpeedComputer:
    """
    rolling window of (timestamp, altitude) pairs and computes vertical speed as dH/dt over that window
    stateful computer
    """

    def __init__(self, window_size: int = VS_WINDOW_SIZE):
        """
        window_size: number of altitude samples to keep
        """
        self._readings: deque = deque(maxlen=window_size)

    def update(self, altitude_ft: float, timestamp: float = None) -> float:
        """
        new altitude reading

        altitude_ft: Current altitude in feet (from LLR-001).
        timestamp: Optional timestamp in seconds. If None, uses time.time().

        returns vertical speed or 0 if difference is invalid or 0
        """
        if timestamp is None:
            timestamp = time.time()

        self._readings.append((timestamp, altitude_ft))

        if len(self._readings) < 2:
            return 0.0

        old_time, old_altitude = self._readings[0]
        now_time, now_altitude = self._readings[-1]

        dt = now_time - old_time
        if dt <= 0:
            return 0.0

        vs_fps = (now_altitude - old_altitude) / dt
        return vs_fps

    def reset(self) -> None:
        self._readings.clear()


def fps_to_fpm(vs_fps: float) -> float:
    """ft/s to ft/min for PFD"""
    return vs_fps * FPS_TO_FPM
