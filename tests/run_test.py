"""
copy of main.py that uses mock pressure reader instead
configuration in test_config.py
"""

import logging
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
import test_config
from mock_pressure_reader import MockPressureReader
from data_types import PressureData, AirData
from adiru.air_data_computer.compute.airspeed import compute_ias_meters_per_sec
from adiru.air_data_computer.compute.altitude import compute_altitude_ft
from adiru.air_data_computer.compute.vertical_speed import VerticalSpeedComputer
from adiru.air_data_computer.output_processing import format_for_pfd
from pfd.pfd_main import PrimaryFlightDisplay

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s   %(name)s   %(levelname)s   %(message)s",
)
logger = logging.getLogger(__name__)


class TestController:
    def __init__(self):
        self.pitot_reader = MockPressureReader(
            adc_channel=config.PITOT_ADC_CHANNEL,
        )
        self.static_reader = MockPressureReader(
            adc_channel=config.STATIC_ADC_CHANNEL,
        )

        self.vs_computer = VerticalSpeedComputer(window_size=config.VS_WINDOW_SIZE)

        if test_config.MODE == "static":
            scenario = test_config.STATIC_SCENARIOS[test_config.ACTIVE_SCENARIO]
            logger.info(f"dynamic: {test_config.ACTIVE_SCENARIO}")
            logger.info(f"  Pitot:  {scenario['pitot_psi']:.4f} PSI")
            logger.info(f"  Static: {scenario['static_psi']:.4f} PSI")
        else:
            cfg = test_config.DYNAMIC_CONFIG
            logger.info("dynamic:")
            logger.info(f"  static: {cfg['static_psi_base']} +/- {cfg['static_psi_amplitude']} PSI "
                        f"at {cfg['static_psi_frequency_hz']} Hz")
            logger.info(f"  pitot:  {cfg['pitot_psi_base']} +/- {cfg['pitot_psi_amplitude']} PSI "
                        f"at {cfg['pitot_psi_frequency_hz']} Hz")

    def connect_hardware(self) -> None:
        self.pitot_reader.connect()
        self.static_reader.connect()
        logger.info("readers connected")

    def disconnect_hardware(self) -> None:
        self.pitot_reader.disconnect()
        self.static_reader.disconnect()
        logger.info("readers disconnected")

    def _read_pressures(self) -> PressureData:
        pitot_psi = self.pitot_reader.read_psi()
        static_psi = self.static_reader.read_psi()

        pitot_pa = pitot_psi * config.PSI_TO_PASCAL
        static_pa = static_psi * config.PSI_TO_PASCAL

        return PressureData(
            pitot_pressure_psi=pitot_psi,
            static_pressure_psi=static_psi,
            pitot_pressure_pa=pitot_pa,
            static_pressure_pa=static_pa,
        )

    def _compute(self, pressures: PressureData) -> AirData:
        ias_mps = compute_ias_meters_per_sec(
            p_total_pa=pressures.pitot_pressure_pa,
            p_static_pa=pressures.static_pressure_pa,
        )
        altitude_ft = compute_altitude_ft(
            static_pressure_psi=pressures.static_pressure_psi,
        )
        now = time.time()
        vs_fps = self.vs_computer.update(altitude_ft, timestamp=now)

        return AirData(
            ias_mps=ias_mps,
            altitude_ft=altitude_ft,
            vertical_speed_fps=vs_fps,
        )

    def data_provider(self) -> dict:
        try:
            pressures = self._read_pressures()
            air_data = self._compute(pressures)
            return format_for_pfd(air_data)
        except Exception as e:
            logger.error("error: %s", e)
            return {}


def main():
    controller = TestController()

    try:
        controller.connect_hardware()

        pfd = PrimaryFlightDisplay()
        pfd.run(dummy=False, data_provider=controller.data_provider)

    except KeyboardInterrupt:
        logger.info("shutdown requested")
    except Exception as e:
        logger.error("error: %s", e)
    finally:
        controller.disconnect_hardware()
        logger.info("complete")


if __name__ == "__main__":
    main()
