from dataclasses import dataclass


@dataclass
class RawMeasurement:
    name: str
    value: int

    def __repr__(self):
        return f"{self.name}: {self.value}"


@dataclass
class Measurement(RawMeasurement):
    topic: str
    qos: int
    retain: bool
