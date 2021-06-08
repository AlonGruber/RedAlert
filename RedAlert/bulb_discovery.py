from yeelight import *
import logger
import os.path

"""
This file referenced to the process of discovering all the bulbs in the network,
and to the different actions used to maintain the current list of bulbs in it 
"""


# Function goal - Getting the bulb list
# Returns - list of bulbs in strings if found, nothing if not found
# Additional details - We try to get the list of all the bulbs in the network by calling to discover_bulbs()
def try_get_bulb_list():
    bulb_list = discover_bulbs()
    if len(bulb_list) != 0:
        logger.add_to_log("I found " + str(len(bulb_list)) + " light bulbs!")
        return bulb_list
    else:
        logger.add_to_log("I could not find any light bulbs, please try again!")
        return None


# Function goal - Saves the bulb list to file bulbs.txt
# Receives - a list of bulbs as received from discover_bulbs()
# Additional details - Saves the list to a txt file called bulbs.txt
#                      saved as id + = + ip
def save_bulbs_to_file(bulb_list):
    try:
        bulb_file = open("bulbs.txt", "w")
    except:
        logger.add_to_log("could not create bulbs.txt file")
        raise Exception
    for i in range(len(bulb_list)):
        bulb_file.write(str(i) + '=' + bulb_list[i]['ip'])
        logger.add_to_log("adding to file bulb - " + bulb_list[i]['ip'])
        bulb_file.write('\n')


# Function goal - check if bulb discovery has already been made
# Additional details - check is done by checking if bulbs.txt file exists
# Returns - true or false - if file was found
def check_if_bulbs_file_exists():
    if os.path.exists('bulbs.txt'):
        logger.add_to_log("found bulbs file")
        return True
    else:
        logger.add_to_log("did not find bulbs file")
        return False


# Function goal - get the bulbs ip list from the bulbs.txt file
# Returns - list of ip addresses as found in bulbs file
# Additional details - bulbs file is constructed and read with '=' between id and ip
def get_bulb_data_from_list():
    try:
        bulb_file = open("bulbs.txt", "r")
    except:
        logger.add_to_log("could not open bulbs.txt file")
        raise Exception
    logger.add_to_log("reading bulbs from bulbs.txt")
    bulb_ip_list = []
    for line in map(str.strip, bulb_file.read().splitlines()):
        line = line.split('=')
        bulb_ip_list.append(line[1])
        logger.add_to_log("bulb id - " + line[0] + " bulb ip - " + line[1])
    return bulb_ip_list


# Function goal -
# Returns -
# Additional details -
def create_bulb_objects_from_list(bulb_ip_list):
    bulb_obj_list = []
    logger.add_to_log("creating bulb objects list from ip addresses")
    for bulb in bulb_ip_list:
        bulb_obj_list.append(Bulb(bulb))
    return bulb_obj_list


# Function goal - get bulbs list
# Returns - a list of bulb objects
# Additional details - This function uses the ones found above to return a list of ip addresses of the bulbs
def get_bulbs():
    if not check_if_bulbs_file_exists():
        bulb_list = try_get_bulb_list()
        if not bulb_list:
            quit(0)
        else:
            save_bulbs_to_file(bulb_list)
    else:
        bulb_list = get_bulb_data_from_list()
    return create_bulb_objects_from_list(bulb_list)
