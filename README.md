# RedAlert
The projects consists of 3 services

1 - RedAlert - this process triggers the alarm,
It is configured once upon running first, and saves all discoverd yeelight bulbs
It waits for http get requests using a simple flask function, once a notification has been received it rings the alarm

Alert Parser - this process priodically requests the pikud haoref server for alarm data,
once received, it parses the data, and checks if the alarm is relevant to the current area the parser is configured to 
if so, it signals the RedAlert to alarm

Mock API server - contains 4 examle XML files provided for the hackathon, 
Upon getting a request for alarm data, returns one of them 
