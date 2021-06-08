import xml.etree.ElementTree as ET

"""

"""

# All the tags found in the xmp files - used when going over the xml
tag_header = '{urn:oasis:names:tc:emergency:cap:1.2}'
xml_body_tag = '{http://www.w3.org/2003/05/soap-envelope}Body'
xml_alert_tag = tag_header + 'alert'
xml_identifier_tag = tag_header + 'identifier'
xml_status_tag = tag_header + 'status'
xml_sent_time_tag = tag_header + 'sent'
xml_info_tag = tag_header + 'info'
xml_expires_tag = tag_header + 'expires'
xml_parameter_tag = tag_header + 'parameter'
xml_area_tag = tag_header + 'area'
xml_areaDesc_tag = tag_header + 'areaDesc'
xml_geocode_tag = tag_header + 'geocode'
xml_value_tag = tag_header + 'value'

# Strings we find in the XML and want to check for
Actual_xml = 'Actual'
Exercise_xml = 'Exercise'
CITIES_xml = 'CITIES'
AREAS_xml = 'AREAS'
SQUARES_xml = 'SQUARES'
ALL_xml = 'ALL'

# Function goal - parses the string we get from the get request to an object of ElementTree
# Returns - root of tree
def get_xml(xml_string):
    root = ET.fromstring(xml_string)
    return root

# Function goal - we use this function to look for a child with a specific name
# Receives - the root and the target child name
# Returns - child node we were looking for
def get_child_in_root(root, target):
    for child in root:
        if child.tag == target:
            return child

# Function goal - we use this to get the text in the node
# Receives - a tree node
# Returns - the text in the tree node
def get_text_in_node(node):
    return node.text


# the geocode tag appears twice in the xml under the same child
# we need the second time it appears so we count appearances
# and return the second time we see it
def get_2nd_geocode_tag(root, target):
    i = 0
    for child in root:
        if child.tag == target:
            i += 1
            if i == 2:
                return child


# Function goal - we go inside the tree and extract all the data we need
# Receives - the tree root
# Returns - a list with the data
# Additional data - it is possible that we might need more data in the future so not every extract is used
def get_all_relevant_data(root):
    body_node = get_child_in_root(root, xml_body_tag)
    alert_node = get_child_in_root(body_node, xml_alert_tag)
    status_node = get_child_in_root(alert_node,xml_status_tag)
    status_text = get_text_in_node(status_node)
    info_node = get_child_in_root(alert_node, xml_info_tag)
    expire_time_node = get_child_in_root(info_node, xml_expires_tag)
    expire_time_text = get_text_in_node(expire_time_node)
    area_type_node = get_child_in_root(info_node, xml_area_tag)
    areaDesc_node = get_child_in_root(area_type_node, xml_areaDesc_tag)
    areaDesc_text = get_text_in_node(areaDesc_node)
    geocode_node = get_2nd_geocode_tag(area_type_node, xml_geocode_tag)
    area_value_node = get_child_in_root(geocode_node, xml_value_tag)
    area_value_text = get_text_in_node(area_value_node)
    return status_text,areaDesc_text,area_value_text


# Function goal - checks if the current xml is a real alarm or an exercise by checking the status tag
# Receives - string with actual or exercise
# Returns - true if its an actual alarm
def is_alarm_real(status):
    return True
    if status == Actual_xml:
        return True
    if status == Exercise_xml:
        return False
    else:
        return None

# Function goal - checks if the user is in the area list received
# Receives - the area list and my area code
# Returns - true if the user is in that list
def match_AREAS(xml_areas,my_area):
    area_list = xml_areas.split(',')
    for area in area_list:
        if area == my_area:
            return True
    return False

# Function goal - checks if the user is in the city list received
# Receives - the city list and my city code
# Returns - true if the user is in that list
def match_CITIES(xml_cities,my_city):
    city_list = xml_cities.split(',')
    for city in city_list:
        if city == my_city:
            return True
    return False

# Function goal - checks if a number is within a range provided in a string
# Receives - a string that looks like  - '1234 - 12347', and a number for my square
# Returns - true if the number is in the range
# Additional details - squares are sent in number ranges so we split them
def check_range(square_range,my_square):
    square_range_list = square_range.split('-')
    return square_range_list[0] <= my_square <= square_range_list[1]

# Function goal - checks if the user is in the square list received
# Receives - the city list and my square code
# Returns - true if the user is in that list
def match_SQUARES(xml_squares,my_square):
    square_list = xml_squares.split(',')
    for square_range in square_list:
        if check_range(square_range,my_square):
            return True
    return False

# Function goal - depending on the xml we received, we check the match by either city, area or square
# Receives - the type of area, its value, and the user's location data
# Returns - true or false if the alarm is directed at our location
# Additional details - if an all alert is sent, we return true always
def check_match(areaDesc_text,area_value_text,my_city,my_area,my_square):
    if areaDesc_text == CITIES_xml:
        return match_CITIES(area_value_text,my_city)
    if areaDesc_text == AREAS_xml:
        return match_AREAS(area_value_text,my_area)
    if areaDesc_text == SQUARES_xml:
        return match_SQUARES(area_value_text,my_square)
    if areaDesc_text == ALL_xml:
        return True
