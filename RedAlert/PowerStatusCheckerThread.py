from threading import Thread
import logger
import time

"""
this class extends thread,
since lights can go on and off, we check at a set time interval what their current status is,
and update the current power list
"""

# power_status class
# Parameters -
#          check_interval - decides how much time to wait between checks
#          function_to_run - function to run at each interval
#          args - the arguments the function_to_run gets once it runs
#          alarm_countdown_instance - the countdown thread used by main

# Inherits from Thread
# sets all values received in init, creates new event object and sets the resetBool to true for now
class PowerStatusCheckerThread(Thread):
    def __init__(self, check_interval,alarm_countdown_instance,function_to_run, args=[]):
        Thread.__init__(self)
        logger.add_to_log("New thread created!")
        self.check_interval = check_interval
        self.function_to_run = function_to_run
        self.alarm_countdown_instance = alarm_countdown_instance
        self.args = args

    def run(self):
        logger.add_to_log("Power status checker thread running! thread id - " + str(self.ident))
        while True:
            logger.add_to_log("Updating power status for bulbs! I am thread -"+str(self.ident))
            if not self.alarm_countdown_instance.is_alive():
                self.function_to_run(*self.args)
            time.sleep(self.check_interval)