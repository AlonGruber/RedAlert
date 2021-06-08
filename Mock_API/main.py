from flask import Flask
import random
import xml_files

"""
This is a mock server imitating the pikud haoref server
upon receiving a get request sends back one of the 4 example xml files 
"""

app = Flask(__name__)
@app.route("/xmlsender")
def index():
    fileToSend = random.randint(1,4)
    if fileToSend == 1:
        return xml_files.xml_1
    if fileToSend== 2:
        return xml_files.xml_2
    if fileToSend== 3:
        return xml_files.xml_3
    if fileToSend== 4:
        return xml_files.xml_4



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)