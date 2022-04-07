import socket
from time import sleep
from coords_receiver import get_address

address = get_address()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

while True:
    send_data = '{"type": "PAYLOAD_SUMMARY", "callsign": "SQ3TLE-8-V2", "latitude": 50.070594787597656, "longitude": 19.90592384338379, "altitude": 283, "speed": 1, "heading": -1, "time": "17:33:39", "comment": "HorusDemodLib", "temp": -1, "sats": 5, "batt_voltage": 2.8823529411764706, "snr": 1.9}'
    s.sendto(send_data.encode('utf-8'), address)
    print("Mock Sent : ", send_data)
    sleep(2)

s.close()