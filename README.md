# MQTT DB Logger Grapher
MQTT Logger Grapher is a client side software for logging MQTT topics from a broker to a SQLite3 database, and displaying the data with [Highcharts](https://www.highcharts.com) in a web browser, using Python and Flask. Designed specifically to monitor power inverter data from [SolPipLog](https://github.com/njfaria/SolPipLog), but can be used for any MQTT data. The web interface is responsive, so it's suitable for desktop or mobile devices.

![image](https://github.com/j-broo/mqtt-db-logger-grapher/assets/26300538/8f90f811-969d-4d23-aafc-ddfcce84e17e)
![image](https://github.com/j-broo/mqtt-db-logger-grapher/assets/26300538/fbadf2dd-130d-45d4-bd78-f609deb37242)

## Based on the following projects/snippets:

* [MQTT data to Sqlite DB](https://lindevs.com/save-mqtt-data-to-sqlite-database-using-python)
* [Sqlite to Highcharts](https://www.ronan.bzh/p/dynamic-charts-with-highcharts-sqlite-and-python/)
* [Python app as a service](https://levelup.gitconnected.com/from-python-to-daemon-how-to-turn-your-python-app-into-a-linux-service-controlled-by-systemd-d87b59adfe7a)
