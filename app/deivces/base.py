from typing import List

from app.models.measurements import RawMeasurement


class Device:
    place: str

    def get_measurements(self, measurement_names: List[str]) -> List[RawMeasurement]:
        pass
