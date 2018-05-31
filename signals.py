from blinker import Namespace
import time
from send_request import Uptime

from flask import Flask, current_app

app = Flask(__name__)

my_signals = Namespace()

uptime = Uptime()

def check(app, **extra):
    uptime.monitor_uptime()

trigger = my_signals.signal('trigger')


trigger.connect(check, app)

def every_min():
    count = 0
    while count < 1:
        time.sleep(1)
        print("It's been a minute")
        count += 1
        print(count)
        with app.app_context():
            trigger.send(current_app._get_current_object())



if __name__ == "__main__":
    every_min()

