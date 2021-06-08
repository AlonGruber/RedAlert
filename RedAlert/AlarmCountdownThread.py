from threading import Event,Thread
import logger

"""
this class extends thread,
it implements a timer thread with a reset ability
used to count down on how much time has passed since last alarm received,
so we can return the bulbs to their previous state before the alarm,
the thread runs a function to return to the previous bulb state when timer is finished
"""

# alarm_countdown class
# Parameters -
#          timer_duration - the amount of time the countdown is set to
#          function_to_run - function set to run once the timer is finished
#          args - the arguments the function_to_run gets once it runs
#          finished_event - Event() type object
#          resetBool - boolean value used to check if timer has been reset

# Inherits from Thread
# sets all values received in init, creates new event object and sets the resetBool to true for now
class AlarmCountdownThread(Thread):
    def __init__(self, timer_duration, function_to_run, args=[]):
        Thread.__init__(self)
        logger.add_to_log("New alarm countdown thread created!")
        self.function_to_run = function_to_run
        self.timer_duration = timer_duration
        self.args = args
        self.finished_event = Event()
        self.resetBool = True

# called once the thread starts running
# since reset bool is set to true, the thread goes into the while loop,
# it then sets the bool to false, and it will stay false as long as the reset function has not been called
# the thread then waits on the event object, if the wait is finished without interruption, it exists the while loop,
# since the reset bool is set to false, and if the finished is not set to true, it runs the function
# if no reset has been made the set value is false the entire time
    def run(self):
        logger.add_to_log("Alarm countdown thread running! thread id -" + str(self.ident))
        while self.resetBool:
            self.resetBool = False
            self.finished_event.wait(self.timer_duration)
        if not self.finished_event.isSet():
            self.function_to_run(*self.args)

# function used to reset the timer
# once function is called, first the timer is reset to the new value
# then the reset bool is set to true, and right after the event is set
# once the event is set, the thread is awakened from its wait state in the run function
# since the reset bool is now true, the while loop will repeat itself with the new value
# the event is then cleared and returned to false
    def reset(self, timer_duration):
        logger.add_to_log("Resetting timer for alarm countdown thread! thread id -" + str(self.ident))
        self.timer_duration = timer_duration
        self.resetBool = True
        self.finished_event.set()
        self.finished_event.clear()
