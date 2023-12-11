import configparser
from flask import Flask, render_template, request
import sqlite3
import json

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini', 'UTF-8')

database_file = config.get('config', 'DATABASE_FILE')
root_topic = config.get('config', 'ROOT_TOPIC')
default_range = int(config.get('config', 'DEFAULT_RANGE'))
default_graph = config.get('config', 'DEFAULT_GRAPH')
graphed_topics = json.loads(config.get('config', 'GRAPHED_TOPICS'))

app = Flask(__name__)

@app.route("/<datasource>.json")
def load(datasource):
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    cursor.execute(f"SELECT (strftime('%s', DATETIME(timestamp, 'unixepoch', 'localtime')))*1000, CAST(payload AS DECIMAL) FROM mqtt_log WHERE topic = '{root_topic}/{datasource}' ORDER BY timestamp ASC")
    results = cursor.fetchall()
    return json.dumps(results)

@app.route("/graph")
def graph():
    return render_template('graph.html', default_range=default_range, default_graph=default_graph, graphed_topics=graphed_topics)

if __name__ == '__main__':
    app.run(
    debug=False,
    threaded=True,
    host='0.0.0.0'
)
