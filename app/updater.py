import time
from typing import List, Optional

import paho.mqtt.client as mqtt

from app import loggers
from app.deivces.base import Device
from app.models.measurements import Measurement, RawMeasurement


class Updater:
    def __init__(
            self,
            device: Device,
            mqtt_client: mqtt.Client,
            allowed_measurements: list
    ):
        self.device = device
        self.mqtt_client = mqtt_client
        self.allowed_measurements = allowed_measurements

    def start_polling(self, interval: int = 10):
        """
        Start infinite polling with cleanup.
        :param interval: Polling interval.
        :return:
        """
        loggers.updater.info("Start polling")
        try:
            self.poll(interval=interval)
        finally:
            self.stop()
            loggers.updater.info("Polling stopped")

    def stop(self):
        self.mqtt_client.disconnect()

    def publish(self, measurements: List[Measurement], wait: Optional[bool] = True):
        queued = [self.mqtt_client.publish(m.topic, m.value, m.qos, m.retain) for m in measurements]

        if not wait:
            loggers.updater.info("Messages are queued")
            return

        for m, r in zip(measurements, queued):
            try:
                r.wait_for_publish()
            except ValueError:
                loggers.updater.error(f"{m.topic}: Message queue is full")
            except RuntimeError as e:
                loggers.updater.error(f"{e}")
                raise ConnectionError(f"{e}")
            else:
                loggers.updater.info(f"{m.topic}: value {m.value} published")

    def poll_once(self) -> List[RawMeasurement]:
        raw_measurements = self.device.get_measurements(self.allowed_measurements)
        loggers.updater.info(f"Recieved measurements: {raw_measurements}")
        return raw_measurements

    def format_output(self, raw_data: List[RawMeasurement]) -> List[Measurement]:
        result = list()
        for m in raw_data:
            result.append(Measurement(
                name=m.name,
                value=m.value,
                topic=f"/measurements/{self.device.place}/{m.name}",
                qos=0,
                retain=False
            ))
        return result

    def poll(self, interval: int):
        """
        Run infiite polling. Each iteration consists of gathering sensor
        measurements and publishing them into MQTT queue.
        :param interval: Polling interval in seconds.
        :return:
        """
        while True:
            start_time = time.time()

            raw_result = self.poll_once()
            result = self.format_output(raw_result)
            self.publish(result)

            delay = time.time() - start_time
            time.sleep(max(0, int(interval - delay)))
