from yeelight import *
import logger
import time
import threading

"""
In this file we reference to all the workings related to controlling the bulb
"""

# Relates to the alert color transmissions - 0.5 sec red 0.5 white, used globally since all alarms are the same
alert_transitions = [RGBTransition(1, 1, 1, duration=500), RGBTransition(255, 1, 1, duration=500)]
# alarm flow for 3 seconds
three_sec_alarm_flow = Flow(count=3, transitions=alert_transitions)
# alarm flow for 10 seconds
ten_sec_alarm_flow = Flow(count=10, transitions=alert_transitions)
# alarm flow for 5 minutes
five_min_alarm_flow = Flow(count=300, transitions=alert_transitions)


# Function goal - This function runs a check on all found light bulbs
# Receives - a list of ip addresses of all the found bulbs
# Test duration - each bulb will flash for 10 seconds, one by one
# Additional details -
#       since we are calling this function in the beginning of the run, we use ip strings and not the objects
#       we sleep on each bulb so that we can check the bulbs one by one, and see them ourselves
def red_light_check_for_all(bulb_ip_list):
    for bulb_ip in bulb_ip_list:
        bulb_obj = Bulb(bulb_ip)
        try:
            bulb_power = bulb_obj.get_properties()['power']
        except BulbException:
            logger.add_to_log("problem communicating with bulb - " + bulb_ip + ", continuing to next bulb")
            continue
        logger.add_to_log("current bulb power state is " + bulb_power)
        bulb_obj.turn_on()
        bulb_obj.set_brightness(100)
        logger.add_to_log("testing light bulb flashing, bulb ip - " + bulb_ip)
        bulb_obj.start_flow(ten_sec_alarm_flow)
        time.sleep(10)
        if bulb_power == 'off':
            bulb_obj.turn_off()


# Function goal - run an alert flow
# Receives - a bulb object on which the alarm will go off on
# Alarm duration - 5 minutes
# Additional details - triggered when an alarm is received

# TESTING PURPOSES - 3 SEC ALARM
def red_alert(bulb_obj):
    bulb_obj.turn_on()
    bulb_obj.set_brightness(100)
    # bulb_obj.start_flow(five_min_alarm_flow)
    bulb_obj.start_flow(three_sec_alarm_flow)


# Function goal - runs the red alert function on all bulbs in a bulb objects list
# Receives - a list of bulb objects
def red_alert_for_list(bulb_obj_list):
    logger.add_to_log("Alarm detected! running red alert on all bulbs")
    for bulb_obj in bulb_obj_list:
        red_alert(bulb_obj)

# Function goal - This function collects from all bulbs their current power state - on or off
# Receives - a list of bulb objects and a list of their current power
# Additional details - if we could not query the bulb for its state, we add it as disconnected
#                      this list corresponds its ids with the bulb object list's ids
def update_power_status(bulb_obj_list,power_list,sem):
    logger.add_to_log("getting power state for all bulbs")
    sem.acquire()
    power_list.clear()
    for i in range(len(bulb_obj_list)):
        try:
            cur_power_state = bulb_obj_list[i].get_properties()['power']
            logger.add_to_log("power state for bulb - " + str(i) + " is " + cur_power_state)
            power_list.append(cur_power_state)
        except BulbException:
            logger.add_to_log("could not get current power state for bulb id " + str(i))
            power_list.append('disconnected')
    sem.release()
    print(power_list)

# Function goal - reverts the previous power state to all bulbs
# Receives - a list of bulb objects, a list of the bulbs power state before the alarm
# Additional details - This function is called after an alarm is finished,
#                       and we want to return the bulbs to their previous state
def revert_power_status_to_all(bulb_obj_list, bulb_status_list,sem):
    logger.add_to_log("putting bulbs in previous state")
    sem.acquire()
    print(bulb_status_list)
    for i in range(len(bulb_obj_list)):
        if bulb_status_list[i] == 'off':
            logger.add_to_log("turning bulb id - " + str(i) + " off")
            bulb_obj_list[i].turn_off()
    sem.release()


