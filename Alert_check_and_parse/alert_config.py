import logger

"""
This file contains all the function with regards to the configuration file in the server
the configuration file has the location data of the user - city, area and square
the config file is organized as "key=value"
"""

# Function goal - tries to open the configuration file, adds error and quits if cant open it
# Returns - returns a file reference object
def get_configuration_file():
    try:
        cfg_file = open("cfg.txt","r")
        logger.add_to_log("Opening cfg file")
    except Exception:
        logger.add_to_log("Could not open cfg.txt file!...quitting")
        quit(0)
    return cfg_file

# Function goal - gets data from the configuration file
# Receives - reference to the file, and the data type we are looking for
# Returns - the value after the '=' sign of the data we were looking for
def get_data_from_cfg_file(cfg_file,data):
    for line in cfg_file:
        line = line.split('=')
        if line[0] == None:
            logger.add_to_log("Configuration file corrupted!...quitting")
            quit(0)
        if line[0] == data:
            logger.add_to_log("Found " + data +" - "+line[1])
            if line[1] == None:
                logger.add_to_log("Missing details of configuration file!...quitting")
                quit(0)
            return line[1].rstrip()

# Function goal - checks if all the personal location data has been filled
def check_all_data_filled(CITY,AREA,SQUARE):
    if CITY == '' or CITY == None or AREA == '' or AREA == None  or SQUARE == '' or SQUARE == None:
        logger.add_to_log("Could not get all data from configuration file!...quitting")
        quit(0)

# Function goal - closes the configuration file
def close_cfg_file(cfg_file):
    logger.add_to_log("Closing cfg file")
    cfg_file.close()