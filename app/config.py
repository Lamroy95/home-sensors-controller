from os import environ
from dotenv import load_dotenv

load_dotenv()


POLLING_INTERVAL = 5

DEVICE_TOKEN = environ["DEVICE_TOKEN"]
DEVICE_IP_ADDR = environ["DEVICE_IP_ADDR"]
ALLOWED_MEASUREMENTS = ['temp_dec', 'humidity', 'aqi']
PLACE = environ.get("PLACE", default="home")

MQTT_HOST = environ["MQTT_HOST"]
MQTT_PORT = int(environ["MQTT_PORT"])
MQTT_USER = environ["MQTT_USER"]
MQTT_PWD = environ["MQTT_PWD"]
MQTT_CLIENT_ID = environ.get("MQTT_CLIENT_ID", default="home-raspi-python")
