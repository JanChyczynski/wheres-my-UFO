import random
import socket
from time import sleep
from locationVisualizer.coordsReceiver import get_address

SENDING_INTERVAL = 2

address = get_address()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)


def calc_h(t):
    if t < 0:
        return 0
    if t <= 10.5:
        return -12 * t * (t - 21)
    else:
        return max(0, 1323 - (t - 10.5) * 20)


lat = 50.070594787597656
lon = 19.90592384338379
t = -3
while True:
    if calc_h(t) != 0:
        lat += random.uniform(0, 2e-2)
        lon += random.uniform(4e-2, 6e-2)

    send_data = '{"type": "PAYLOAD_SUMMARY", "callsign": "SQ3TLE-8-V2", "latitude": ' + str(
        lat) + ', "longitude": ' + str(
        lon) + ', "altitude": ' + str(calc_h(t)) + ', "speed": 1, "heading": -1, "time": "17:33:39",\
         "comment": "HorusDemodLib", "temp": -1, "sats": 5, "batt_voltage": 2.8823529411764706, "snr": 1.9}'
    s.sendto(send_data.encode('utf-8'), address)
    print("Mock Sent : ", send_data)
    sleep(SENDING_INTERVAL)
    t += SENDING_INTERVAL

s.close()
