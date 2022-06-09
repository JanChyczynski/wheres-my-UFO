import json
import os
import queue
import sys
import threading
import socket

from coordinates import Coords


def get_address():
    default_ip = "127.0.0.1"
    default_port = 55672
    ip = input("Enter ip adrress, enter empty for default: ")
    port = input("Enter port number, enter empty for default: ")
    if len(ip) == 0:
        ip = default_ip
    ip = ip.strip()
    if len(port) == 0:
        port = default_port
    else:
        port = int(port)

    return ip, port


class CoordinatesReceiver:
    MAX_FRAME_SIZE = 2048

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.s.settimeout(1)
        # self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        ip, port = get_address()

        self.s.bind((ip, port))

        self.coords_que = queue.Queue()
        self.data_receiver_th = threading.Thread(target=self.data_receiver)
        self.data_receiver_th.start()
        self.loop()

    def loop(self):
        while True:
            coords = None
            try:
                coords = self.coords_que.get_nowait()
            except queue.Empty:
                pass
            except KeyboardInterrupt as ke:
                print("Keyboard int", ke)
                self.exit = True
                # sys.exit(0)
                os._exit(0)

            if coords is not None:
                print("Received", coords)

    def data_receiver(self):
        while True:
            data, address = self.s.recvfrom(CoordinatesReceiver.MAX_FRAME_SIZE)
            unjsoned = json.loads(data)
            self.coords_que.put(Coords.from_dict(unjsoned))


if __name__ == "__main__":
    appl = CoordinatesReceiver()
