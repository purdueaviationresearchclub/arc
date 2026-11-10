"""
Main file for ARC ADIRU

read pitot + static voltage from ADS1115
convert to PSI (PitotStaticInputSignals:pitotPressure / staticPressure)
convert PSI to Pa (AirDataComputerInputProcessing, LLR-004/005)
pressureData (carries both PSI and Pa)

IAS in m/s from Pa values (LLR-006)
altitude in feet from PSI value (LLR-001, uses P0=14.6959 Psi)
vertical speed in ft/s from dH/dt of altitude
AirData

convert IAS m/s to knots (LLR-007)
altitude already in feet (LLR-002)
convert VS ft/s to fpm
dict for PFD.set()

PFD.set(**dict), render, flip
"""

import logging
import time

import config
from adiru.air_data_computer.data_types import PressureData, AirData
from adiru.air_data_computer.input_processing import PressureReader
from adiru.air_data_computer.compute.airspeed import compute_ias_meters_per_sec
from adiru.air_data_computer.compute.altitude import compute_altitude_ft
from adiru.air_data_computer.compute.vertical_speed import VerticalSpeedComputer
from adiru.air_data_computer.output_processing import format_for_pfd
from pfd.pfd_main import PrimaryFlightDisplay

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class ADIRUController:
    def __init__(self):
        self.pitot_reader = PressureReader(
            adc_channel=config.PITOT_ADC_CHANNEL,
            psi_per_volt=config.PITOT_PSI_PER_VOLT,
            psi_offset=config.PITOT_PSI_OFFSET,
            gain=config.ADC_GAIN,
        )
        self.static_reader = PressureReader(
            adc_channel=config.STATIC_ADC_CHANNEL,
            psi_per_volt=config.STATIC_PSI_PER_VOLT,
            psi_offset=config.STATIC_PSI_OFFSET,
            gain=config.ADC_GAIN,
        )

        self.vs_computer = VerticalSpeedComputer(window_size=config.VS_WINDOW_SIZE)

    def connect_hardware(self) -> None:
        logger.info("connecting")
        self.pitot_reader.connect()
        self.static_reader.connect()
        logger.info("connected")

    def disconnect_hardware(self) -> None:
        self.pitot_reader.disconnect()
        self.static_reader.disconnect()
        logger.info("disconnected")

    def _read_pressures(self) -> PressureData:
        """
        returns PressureData with both PSI (raw signal) and Pa (input-processed) values
        """
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
        """
        runs computations on pressure data
        """
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
            logger.error("Pipeline error: %s", e)
            return {}


def main():
    controller = ADIRUController()

    try:
        controller.connect_hardware()

        pfd = PrimaryFlightDisplay()
        pfd.run(dummy=False, data_provider=controller.data_provider)

    except KeyboardInterrupt:
        logger.info("Shutdown requested by user (Ctrl+C).")
    except Exception as e:
        logger.error("Fatal error: %s", e)
    finally:
        controller.disconnect_hardware()
        logger.info("ADIRU shutdown complete.")


if __name__ == "__main__":
    main()
