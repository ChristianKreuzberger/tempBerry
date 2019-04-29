"""Example how to handle codes received by the pilight-daemon.
A running pilight-daemon is neededed.
"""

import time
import traceback
import sys
import requests
from datetime import datetime
from pilight import pilight


def post_temperature_data(data):
    """
    Post temperature data to tempberry api
    :param data:
    :return:
    """

    with requests.Session() as s:
        try:
            r = s.post("https://tempberry.chkr.at/api/temperatures/", data)
            return r
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print(datetime.now(), "post_data(): An error occured")
            print(''.join('!! ' + line for line in lines))

    return None


def post_binary_data(data):
    """
    Post binary sensor data to tempberry api
    :param data:
    :return:
    """

    with requests.Session() as s:
        try:
            r = s.post("https://tempberry.chkr.at/api/binary_sensors/", data)
            return r
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print(datetime.now(), "post_data(): An error occured")
            print(''.join('!! ' + line for line in lines))

    return None


last_temperature_message = None
last_binary_sensor_message = None


def handle_code(code):  # Simply  print received data from pilight
    """
    Handle messages coming from pilight
    :param code:
    :return:
    """
    global last_temperature_message, last_binary_sensor_message

    # handle message based on protocol
    if code['protocol'] == 'teknihall':
        # teknihall = temperature data

        # ignore this message if it is the same as last time (e.g., repeats from the sensor)
        if last_temperature_message == code['message']:
            print('Skipped duplicate message')
            return

        print(code)

        # ignore if sensor id is 0 (most likely a wrong sensor reading)
        if code['message']['id'] == 0:
            print(datetime.now(), "Skipping sensor id 0")
            return

        print(datetime.now(), code['protocol'], "Id: %(id)s Temp: %(temperature)s %(humidity)s" % code['message'])

        # Post data to REST API
        post_temperature_data(
            {
                'sensor_id': code['message']['id'], 'temperature': code['message']['temperature'],
                'humidity': code['message']['humidity'], 'battery': code['message']['battery'], 'source': 'raspberry'
            }
        )

        # store last_code so we can compare and skip certain messages
        last_temperature_message = code['message']
    elif code['protocol'] == 'cpu_temp':
        print(datetime.now(), code['protocol'], "Cpu Temp %(temperature)s" % code['message'])
    elif code['protocol'] == 'openweathermap':
        return  # ignore open weather map updates
    elif code['protocol'] == 'arctech_contact':
        # handle contact sensors via binary protocol

        # {'uuid': '0000-b8-27-eb-774f8b', 'protocol': 'arctech_contact', 'repeats': 3, 'message': {'state': 'closed', 'unit': 1, 'id': 15707136}, 'origin': 'receiver'}
        # binary sensor data from contact sensors

        # ignore this message if it is the same as last time (e.g., repeats from the sensor)
        if last_binary_sensor_message == code['message']:
            # print('Skipped duplicate message')
            return

        print(code)

        # ignore if sensor id is 0 (most likely a wrong sensor reading)
        if code['message']['id'] == 0:
            print(datetime.now(), "Skipping sensor id 0")
            return

        state = code['message']['state']
        sensor_id = code['message']['id']

        binary_state = -1

        if state in ['on', 'open', 'opened', 'up']:
            binary_state = 1
        elif state in ['off', 'down', 'close', 'closed']:
            binary_state = 0

        # Post data to REST API
        post_temperature_data(
            {
                'sensor_id': sensor_id,
                'binary_state': binary_state,
                'source': 'raspberry'
            }
        )

        last_binary_sensor_message = code['message']
    elif 'arctech' in code['protocol']:
        # ignore all other arctech entries (they are the same as artec_contact)
        pass
    else:
        print("--- !!!! Unknown protocl --- ")
        print(datetime.now(), code['protocol'], code)


# pylint: disable=C0103
if __name__ == '__main__':
    # Create new pilight connection that runs on localhost with port 5000
    pilight_client = pilight.Client(host='127.0.0.1', port=5000, veto_repeats=False)

    # Set a data handle that is called on received data
    pilight_client.set_callback(handle_code)
    pilight_client.start()  # Start the receiver

    # You have 10 seconds to print all the data the pilight-daemon receives
    time.sleep(100000000)
    pilight_client.stop()  # Stop the receiver


