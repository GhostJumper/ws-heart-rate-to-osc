import os
import json
import time
import threading
from collections import deque
from pythonosc import udp_client
from websocket import create_connection

# Global variables
VRCHAT_OSC_IP = os.environ.get('VRCHAT_OSC_IP', "127.0.0.1")
VRCHAT_OSC_PORT = int(os.environ.get('VRCHAT_OSC_PORT', 9000))

WEBSOCKET_IP = os.environ.get('WEBSOCKET_IP', "127.0.0.1")
WEBSOCKET_PORT = int(os.environ.get('WEBSOCKET_PORT', 8080))
DEVICE_ID = int(os.environ.get('DEVICE_ID', 19635))
PROFILE = os.environ.get('PROFILE', 'HR')

OSC_HEART_RATE_PARAMETER = os.environ.get('OSC_HEART_RATE_PARAMETER', '/avatar/parameters/Hologram')

MIN_HR = int(os.environ.get('MIN_HR', 60))
MAX_HR = int(os.environ.get('MAX_HR', 120))

MIN_PARAM_VALUE = float(os.environ.get('MIN_PARAM_VALUE', 0.1))
MAX_PARAM_VALUE = float(os.environ.get('MAX_PARAM_VALUE', 0.74))

data_buffer = deque(maxlen=5)
average_heart_rate = None
lock = threading.Lock()

# WebSocket thread
def websocket_thread():
    global data_buffer, average_heart_rate
    ws = create_connection(f'ws://{WEBSOCKET_IP}:{WEBSOCKET_PORT}')

    while True:
        data = ws.recv()
        try:
            data_json = json.loads(data)
            profile = data_json.get('profile')
            device_id = data_json.get('deviceID')
            heart_rate = data_json.get('heartRate')
            

            if (heart_rate and isinstance(heart_rate, int) and profile == PROFILE and device_id == DEVICE_ID):
                with lock:
                    print(f"Received heart rate: {heart_rate}")
                    data_buffer.append(heart_rate)
                    average_heart_rate = sum(data_buffer) / len(data_buffer)
        except json.JSONDecodeError:
            pass

# OSC thread
def osc_thread():
    global average_heart_rate
    osc_client = udp_client.SimpleUDPClient(VRCHAT_OSC_IP, VRCHAT_OSC_PORT)  # Replace with your OSC server IP and port

    last_sent_average = None

    while True:
        with lock:
            if average_heart_rate is not None and average_heart_rate != last_sent_average:
                osc_client.send_message(OSC_HEART_RATE_PARAMETER, map_heart_rate_to_float(average_heart_rate))
                print(f"Sending OSC message: {OSC_HEART_RATE_PARAMETER}={map_heart_rate_to_float(average_heart_rate)}")
                last_sent_average = average_heart_rate
        time.sleep(0.1)

def map_heart_rate_to_float(heart_rate):
    if heart_rate < MIN_HR:
        heart_rate = MIN_HR
    elif heart_rate > MAX_HR:
        heart_rate = MAX_HR
    normalized_hr = (heart_rate - MIN_HR) / (MAX_HR - MIN_HR) * (MAX_PARAM_VALUE - MIN_PARAM_VALUE) + MIN_PARAM_VALUE
    return round(normalized_hr, 2)

# Start threads
websocket_t = threading.Thread(target=websocket_thread)
osc_t = threading.Thread(target=osc_thread)

websocket_t.start()
osc_t.start()

websocket_t.join()
osc_t.join()