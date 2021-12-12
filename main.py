import logging

import paho.mqtt.client as mqtt

from app.updater import Updater
from app.deivces.air_purifier import AirPurifier
from app import config

logging.basicConfig(level=logging.INFO)


def get_mqtt_connection() -> mqtt.Client:
    client = mqtt.Client(client_id=config.MQTT_CLIENT_ID, clean_session=False)
    client.username_pw_set(config.MQTT_USER, config.MQTT_PWD)

    rc = client.connect(host=config.MQTT_HOST, port=config.MQTT_PORT)
    if rc == 0:
        logging.info(f"Connected to mqtt broker {config.MQTT_HOST}:{config.MQTT_PORT}")
    else:
        message = f"Connection to mqtt broker {config.MQTT_HOST}:{config.MQTT_PORT} failed with return code {rc}"
        logging.error(message)
        raise ConnectionError(message)
    return client


def main():
    mqtt_client = get_mqtt_connection()
    device = AirPurifier(place=config.PLACE, ip=config.DEVICE_IP_ADDR, token=config.DEVICE_TOKEN)
    updater = Updater(device, mqtt_client, config.ALLOWED_MEASUREMENTS)

    updater.start_polling(interval=config.POLLING_INTERVAL)


if __name__ == '__main__':
    main()
