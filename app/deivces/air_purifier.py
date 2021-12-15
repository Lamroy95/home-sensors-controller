from typing import List

from miio.airpurifier import AirPurifier as AirPurifierBase

from app.deivces.base import Device
from app.models.measurements import RawMeasurement


class AirPurifier(AirPurifierBase, Device):
    def __init__(self, place, *args, **kwargs):
        self.place = place
        super().__init__(*args, **kwargs)

    def get_measurements(self, measurement_names: List[str]) -> List[RawMeasurement]:
        raw_result = self.get_properties(measurement_names)
        return [RawMeasurement(name, value) for name, value in zip(measurement_names, raw_result) if value is not None]
