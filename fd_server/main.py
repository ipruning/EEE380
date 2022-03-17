import json
import random
import threading

from decouple import config
import flask
import telegram
from telegram.ext import CommandHandler

import requests

"""
Name: fatigue_monitoring_bot
Description: A Telegram bot that monitors the fatigue of a user.
About: A Telegram bot that monitors the fatigue of a user.
Botpic: 🖼 has a botpic
"""

"""
help - Get Help
start - Start the bot
start_m - Start monitoring
stop_m - Stop monitoring
"""


def callback_start(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(rf"Hi {user.mention_markdown_v2()}\!")


def callback_help(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
    update.message.reply_text("Help!")


def callback_alarm(context: telegram.ext.CallbackContext) -> None:
    url = "http://127.0.0.1:5000/api/v1/get_sensor_data"
    resp = requests.get(url=url)
    sensor_data = resp.json()
    print(sensor_data)
    my_message = f"Fatigue Value: {str(sensor_data[0])}"
    context.bot.send_message(chat_id=context.job.context, text=my_message)


def callback_start_m(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
    context.bot.send_message(chat_id=update.message.chat_id, text="Setting a timer!")
    context.job_queue.run_repeating(callback_alarm, 1, context=update.message.chat_id)


def callback_stop_m(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
    context.bot.send_message(chat_id=update.message.chat_id, text="Stopping the timer!")
    context.job_queue.stop()


app = flask.Flask(__name__)


@app.route("/api/v1/get_sensor_data", methods=["GET", "POST"])
def draw_stone():
    d_hum, d_temp = round(random.uniform(0, 1), 4), round(random.uniform(0, 1), 4)
    data = [d_temp, d_hum]
    return flask.Response(json.dumps(data), mimetype="application/json")


@app.route("/")
def staff_page():
    return app.send_static_file("index.html")


class FlaskThread(threading.Thread):
    def run(self) -> None:
        app.run(host="0.0.0.0", port=5000)

    def run_debug(self) -> None:
        app.run(host="0.0.0.0", port=5000, debug=True)


def run_bot() -> None:
    u = telegram.ext.Updater(config("BOT_API_KEY"), use_context=True)
    # j = u.job_queue
    u.dispatcher.add_handler(CommandHandler("help", callback_help))
    u.dispatcher.add_handler(CommandHandler("start", callback_start))
    u.dispatcher.add_handler(CommandHandler("start_m", callback_start_m))
    u.dispatcher.add_handler(CommandHandler("stop_m", callback_stop_m))
    u.start_polling()
    u.idle()


if __name__ == "__main__":
    flask_thread = FlaskThread()
    flask_thread.start()
    run_bot()
