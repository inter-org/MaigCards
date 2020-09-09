import socket
import threading
from mserver.server import Server

def testServer():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 2345))
    sock.listen()

    while True:
        conn, addr = sock.accept()
        print(conn, addr)
        while True:
            data = conn.recv(1024)
            print(Server.unserialize(data))
    print("server end")


class ReceiveThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('localhost', 2555))
        sock.listen()

        conn, addr = sock.accept()
        while True:
            data = conn.recv(1024)
            if not data:
                break

            print(Server.unserialize(data))


if __name__ == '__main__':
    thread1 = ReceiveThread()
    thread1.start()

    thread1.join()
