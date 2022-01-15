import json
import random

import flask

app = flask.Flask(__name__)


@app.route("/api/get_sensor_data", methods=["GET", "POST"])
def draw_stone():
    d_hum, d_temp = round(random.uniform(0, 1), 4), round(random.uniform(0, 1), 4)
    data = [d_temp, d_hum]
    return flask.Response(json.dumps(data), mimetype="application/json")


@app.route("/")
def staff_page():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run("0.0.0.0", port=5005)
