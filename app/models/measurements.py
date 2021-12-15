from dataclasses import dataclass
from typing import Union


@dataclass
class RawMeasurement:
    name: str
    value: Union[int, float, str]

    def __repr__(self):
        return f"{self.name}: {self.value}"


@dataclass
class Measurement(RawMeasurement):
    topic: str
    qos: int
    retain: bool
