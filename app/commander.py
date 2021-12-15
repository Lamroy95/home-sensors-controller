import paho.mqtt.client as mqtt

from app import loggers
from app.deivces.base import Device
from app.models.commands import Command


class Commander:
    def __init__(
            self,
            topic: str,
            client: mqtt.Client,
            device: Device,
    ):
        self.topic = topic
        self.client = client
        self.device = device

        self._setup_handlers()

    def _setup_handlers(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe

    def on_connect(self, client: mqtt.Client, userdata, flags, rc):
        loggers.commander.info("Connected to MQTT broker")
        self.subscribe(self.topic)

    def on_disconnect(self, client: mqtt.Client, userdata, rc):
        loggers.commander.info("Disconnected from MQTT broker")

    def on_subscribe(self, client: mqtt.Client, userdata, mid, granted_qos):
        loggers.commander.info(f"Subscribed")

    def on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        param = msg.payload.decode('utf-8')
        _, command_name = msg.topic.strip("/").rsplit("/", maxsplit=1)
        loggers.commander.info(f"Recieved command `{command_name}` with param `{param}`")
        cmd = Command(command_name, param)
        self.execute_command(cmd, param)

    def subscribe(self, topic: str):
        self.client.subscribe(topic)

    def start(self):
        self.subscribe(self.topic)

    def stop(self):
        self.client.disconnect()

    def execute_command(self, command: Command, param):
        method = getattr(self.device, command.method.name)
        method(command.param)
        loggers.commander.info(f"Executed method `{command.method.name}` with param `{param}`")
