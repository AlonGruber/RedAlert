import xml_parsing
import requests
import alert_config
import logger
import time

#addresses for the pikud haoref api and the alert server
xmlURL = "http://localhost:8080/xmlsender"
alarmURL = "http://localhost:8079/alert"
location = ""

#check pikud haoref api every x seconds
check_interval = 5

#Load all data from the config file
cfg_file = alert_config.get_configuration_file()
my_city = alert_config.get_data_from_cfg_file(cfg_file, 'CITY')
my_area = alert_config.get_data_from_cfg_file(cfg_file, 'AREA')
my_square = alert_config.get_data_from_cfg_file(cfg_file, 'SQUARE')
alert_config.check_all_data_filled(my_city, my_area, my_square)
alert_config.close_cfg_file(cfg_file)

#main, runs in loop
def main():
    while True:
        try:
            #try to get data from pikud haoref API
            data = requests.get(xmlURL, location)
        except:
            logger.add_to_log("could not connect to to pikud haoref API!")
        #parse the xml we received
        root = xml_parsing.get_xml(data.text)
        #and get all needed information from it
        status,areaDesc_text, area_value_text = xml_parsing.get_all_relevant_data(root)
        #first we check if the alarm is real according to its status
        if xml_parsing.is_alarm_real(status):
            #then we check if we are in the area the alarm was meant for
            if xml_parsing.check_match(areaDesc_text, area_value_text, my_city, my_area, my_square):
                try:
                    #if it is we send a signal to the alarm to start
                    send_alarm = requests.get(alarmURL,location)
                    logger.add_to_log("sent alarm! " + send_alarm)
                except:
                    logger.add_to_log("could not send alarm to red alert server!")
        # time to sleep between requests
        time.sleep(check_interval)


if __name__ == "__main__":
    main()
