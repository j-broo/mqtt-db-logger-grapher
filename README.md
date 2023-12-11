# MQTT DB Logger Grapher
MQTT Logger Grapher is a client side software for logging MQTT topics from a broker to a SQLite3 database, and displaying the data with [Highcharts](https://www.highcharts.com) in a web browser, using Python and Flask. Designed specifically to monitor power inverter data from [SolPipLog](https://github.com/njfaria/SolPipLog), but can be used for any MQTT data. The web interface is responsive, so it's suitable for desktop or mobile devices.

Intended for use on a Raspberry Pi or other Debian-based host. Successfully developed and tested on a Pi 1B+, so it does not need high level hardware.

![image](https://github.com/j-broo/mqtt-db-logger-grapher/assets/26300538/8f90f811-969d-4d23-aafc-ddfcce84e17e)
![image](https://github.com/j-broo/mqtt-db-logger-grapher/assets/26300538/fbadf2dd-130d-45d4-bd78-f609deb37242)


# Installation instructions
1. Download the release and unzip to "/etc" or another suitable folder (you may need to edit the config and service files if not using "/etc".
2. Edit "config.ini" to connect to your broker, choose your topics, and other settings.
3. Run "install_services.sh" in the "service" folder to install the python scripts as services.
4. Start services using "systemctl start mqttdblogger" or "systemctl start mqttdbgrapher".
5. Check the log file for a successful conection.
6. Access the web interface on "http://yourhost:5000/graph"

# Recommendations
1. Host the database on a FAST flash or external disk so save your SD card. You may need to check the speed of the disk first. Slow disks will lead to data logging dropouts (you'll see gaps in the graph).
2. Limit your data retention age - keeping weeks or moths worth of data will slow the graphs down, as all data for a topic is loaded every time. You can configure the data retention limit in the "config.ini" file. 
3. If you don't keep too much data and have RAM to spare, consider using a RAM disk for the database, such as Log2RAM, so it's cached in RAM and only written to disk periodically. Not recommended on older low RAM devices. Keep in mind data might be lost on power loss.

## Based on the following projects/snippets:

* [MQTT data to Sqlite DB](https://lindevs.com/save-mqtt-data-to-sqlite-database-using-python)
* [Sqlite to Highcharts](https://www.ronan.bzh/p/dynamic-charts-with-highcharts-sqlite-and-python/)
* [Python app as a service](https://levelup.gitconnected.com/from-python-to-daemon-how-to-turn-your-python-app-into-a-linux-service-controlled-by-systemd-d87b59adfe7a)
