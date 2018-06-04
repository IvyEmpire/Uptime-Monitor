from blinker import Namespace
import time
from send_request import Uptime


from flask import Flask, current_app

app = Flask(__name__)

my_signals = Namespace()




uptime_for_auth0=Uptime ('auth0', 'https://empirelife-prod.auth0.com/testall',200)
uptime_for_advisor = Uptime('advisor', 'https://web9.empire.ca/AdvisorAPI/rest/advisorInfo/v1/', 405)

def check(app, **extra):

    uptime_for_auth0.monitor_uptime()
    uptime_for_advisor.monitor_uptime()

trigger = my_signals.signal('trigger')


trigger.connect(check, app)

def every_min():
    count = 0
    while count < 3:
        time.sleep(1)
        print("It's been a minute")
        count += 1
        print(count)
        with app.app_context():
            trigger.send(current_app._get_current_object())



if __name__ == "__main__":
    every_min()

