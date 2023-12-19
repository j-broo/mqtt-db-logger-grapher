import configparser
import paho.mqtt.client as mqtt
import sqlite3
from random import randint
import os
from os import system
from time import time
import json
import logging
from datetime import datetime

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini', 'UTF-8')

mqtt_host = config.get('config', 'MQTT_HOST')
mqtt_port = int(config.get('config', 'MQTT_PORT'))
mqtt_client_id = config.get('config', 'MQTT_CLIENT_ID') + ' ' + str(randint(0, 100))
mqtt_user = config.get('config', 'MQTT_USER')
mqtt_password = config.get('config', 'MQTT_PASSWORD')
topic = config.get('config', 'ROOT_TOPIC') + '/' + config.get('config', 'SUB_TOPIC')
qos = int(config.get('config', 'QOS'))
age_limit = int(config.get('config', 'AGE_LIMIT'))*86400
database_file = config.get('config', 'DATABASE_FILE')
startup_vacuum = bool(config.get('config', 'STARTUP_VACUUM'))
log_file = config.get('config', 'LOG_FILE')

logging.basicConfig(filename=log_file, filemode='a', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%F %T')

def on_connect(mqtt_client, user_data, flags, conn_result):
    try:
        mqtt_client.subscribe(topic, qos=qos)
        logging.info("Connected to "+  mqtt_host + " on " + str(mqtt_port) + ". Subscribed to " + topic + ".")
    except Exception as e:
        logging.error("Failed to connect!", exc_info=True)

def on_message(mqtt_client, user_data, message):
    payload = message.payload.decode('utf-8')
    timestamp = int(time())
    db_conn = user_data['db_conn']
    log_message = 'INSERT INTO mqtt_log (timestamp, topic, payload) VALUES (?, ?, ?)'
    cleanup = 'DELETE FROM mqtt_log WHERE timestamp < ?'
    cursor = db_conn.cursor()

    try:
        cursor.execute(log_message, (timestamp, message.topic, payload))
        cursor.execute(cleanup, [timestamp-age_limit])
        db_conn.commit()
    except Exception as e:
         logging.error("Error saving data!", exc_info=True)

    cursor.close()

def getdbsize():
    return str(round(os.path.getsize(database_file)/1048576,2))

def main():
    db_conn = sqlite3.connect(database_file)

    createtable = '''
    PRAGMA journal_mode=WAL;
    CREATE TABLE IF NOT EXISTS mqtt_log (
    timestamp INTEGER NOT NULL,
    topic TEXT NOT NULL,
    payload TEXT NOT NULL,
    PRIMARY KEY (timestamp, topic));
    CREATE INDEX IF NOT EXISTS mqtt_log_idx ON mqtt_log(topic, timestamp ASC, payload);
    '''

    cursor = db_conn.cursor()
    cursor.executescript(createtable)

    if startup_vacuum:
       logging.info("Started vacuuming database. Database size before: " + getdbsize() + " MiB.")
       cursor.execute('PRAGMA VACUUM')
       logging.info("Finished vacuuming database. Database size after: " + getdbsize() + " MiB.")

    cursor.close()

    mqtt_client = mqtt.Client(mqtt_client_id)
    mqtt_client.username_pw_set(mqtt_user, mqtt_password)
    mqtt_client.user_data_set({'db_conn': db_conn})

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(mqtt_host, mqtt_port)
    mqtt_client.loop_forever()

main()
