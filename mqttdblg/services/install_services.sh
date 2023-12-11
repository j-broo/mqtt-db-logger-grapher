#!/bin/bash

echo "Installing MQTT DB Logger service..."
sudo cp mqttdblogger.service /etc/systemd/system/
sudo systemctl enable mqttdblogger.service

echo "Installing MQTT DB Grapher service..."
sudo cp mqttdbgrapher.service /etc/systemd/system/
sudo systemctl enable mqttdbgrapher.service
