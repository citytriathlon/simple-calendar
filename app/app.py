# app.py
from flask import Flask, render_template
from threading import Thread
import asyncio
from calendar_data import CalendarData

app = Flask(__name__)
calendar_data = CalendarData()


def start_async_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(calendar_data.start())


@app.route("/")
def mainpage():
    context = calendar_data.get_recent_events()
    return render_template("index.html", data=context)

if __name__ == "__main__":
    Thread(target=start_async_loop, daemon=True).start()
    app.run(debug=True, host='0.0.0.0', port=5000)
