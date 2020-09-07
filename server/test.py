import socket
import sys
from MaigCards.server.server import *
import threading

def testServer():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 2336))
    sock.listen()

    while True:
        conn, addr = sock.accept()
        print(conn, addr)
        while True:
            data = conn.recv(1024)
            print(data)
            print(Server.unserialize(data))


class ReceiveThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    

    def run(self):
        testServer()



if __name__ == '__main__':
    thread1 = ReceiveThread()
    thread1.start()

    thread1.join()



