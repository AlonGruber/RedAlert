import red_alert
import bulb_discovery
import threading
from AlarmCountdownThread import AlarmCountdownThread
from PowerStatusCheckerThread import PowerStatusCheckerThread
from flask import Flask

#timers for all alarms and countdowns
timer_countdown = 3
check_power_interval = 300

#flask app
app = Flask(__name__)

#run a test on all lights
red_alert.red_light_check_for_list(bulb_discovery.try_get_bulb_list())

#get list of all bulb objects
bulb_obj_list = bulb_discovery.get_bulbs()

#create semaphore for the 2 thread types
semaphore = threading.Semaphore()

#get current power status for bulbs
current_power_status_list = []
red_alert.update_power_status(bulb_obj_list, current_power_status_list,semaphore)

#raise thread for alarm countdown
timer = AlarmCountdownThread(timer_countdown, red_alert.revert_power_status_to_all, [bulb_obj_list, current_power_status_list,semaphore])

#raise thread to check power status and start it
power_status_checker = PowerStatusCheckerThread(check_power_interval,timer,red_alert.update_power_status,[bulb_obj_list,current_power_status_list,semaphore])
power_status_checker.start()

#flask web service
#when called, an alarm notification is received to start the alarm
@app.route("/alert")
def ring_alarm():
    global timer
    #runs alert on all bulbs
    red_alert.red_alert_for_list(bulb_obj_list)
    #checks how to behave with timer
    if timer.is_alive():
        timer.reset(timer_countdown)
        return "alarm restarted"
    else:
        try:
            timer.start()
        except RuntimeError:
            timer = AlarmCountdownThread(timer_countdown, red_alert.revert_power_status_to_all, [bulb_obj_list, current_power_status_list,semaphore])
            timer.start()
    return "alarm started"

#runs flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8079, debug=True)
