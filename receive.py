"""Example how to handle codes received by the pilight-daemon.
A running pilight-daemon is neededed.
"""

import time
import requests
from datetime import datetime
from pilight import pilight


def post_data(data):
    r = requests.post("http://tempberry.chkr.at/api/temperatures/", data)
    return r


last_code = None

def handle_code(code):  # Simply  print received data from pilight
    global last_code
    """Handle to just prints the received code."""
    if code['protocol'] == 'teknihall':
        # ignore this message if the code is exactly the same
        print(code)
        if last_code == code['message']:
            return

        print(datetime.now(), code['protocol'], "Id: %(id)s Temp: %(temperature)s %(humidity)s" % code['message'])

        # Post data to REST API
        post_data(
            {
                'sensor_id': code['message']['id'], 'temperature': code['message']['temperature'],
                'humidity': code['message']['humidity'], 'battery': '0', 'source': 'raspberry'
            }
        )

        last_code = code['message']
    elif code['protocol'] == 'cpu_temp':
        print(datetime.now(), code['protocol'], "Cpu Temp %(temperature)s" % code['message'])
    elif code['protocol'] == 'openweathermap':
        return  # ignore open weather map updates
    else:
        print(datetime.now(), code['protocol'], code)


# pylint: disable=C0103
if __name__ == '__main__':
    # Create new pilight connection that runs on localhost with port 5000
    pilight_client = pilight.Client(host='127.0.0.1', port=5000, veto_repeats=False)

    # Set a data handle that is called on received data
    pilight_client.set_callback(handle_code)
    pilight_client.start()  # Start the receiver

    # You have 10 seconds to print all the data the pilight-daemon receives
    time.sleep(10000)
    pilight_client.stop()  # Stop the receiver

