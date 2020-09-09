import threading
from queue import Queue


class ThreadVar:
    def __init__(self):
        self.send_packets = Queue()
        self.recv_packets = Queue()
        self.send_packets_lock = threading.Lock()
        self.recv_packets_lock = threading.Lock()
        self.terminate_flag_lock = threading.Lock()
        self.terminate_flag = False

        # @staticmethod

    def getSendTop(self):
        print("before queue.get()")
        self.send_packets_lock.acquire()
        qsize = self.send_packets.qsize()
        if qsize == 0:
            self.send_packets_lock.release()
            return None
        res = self.send_packets.get()
        self.send_packets_lock.release()
        print("after queue.get()")
        return res

    # @staticmethod
    def getRecvTop(self):
        self.recv_packets_lock.acquire()
        res = self.recv_packets.get()
        self.recv_packets_lock.release()
        return res

    # @staticmethod
    def putSendTop(self, x):
        print("before put")
        self.send_packets_lock.acquire()
        self.send_packets.put(x)
        self.send_packets_lock.release()
        print("after put")
        print(self.send_packets.qsize())

    # @staticmethod
    def putRecvTop(self, x):
        self.recv_packets_lock.acquire()
        self.recv_packets.put(x)
        self.recv_packets_lock.relase()

    # @staticmethod
    def readTermFlag(self):
        return self.terminate_flag

    # @staticmethod
    def writeTermFlag(self, x: bool):
        self.terminate_flag_lock.acquire()
        self.terminate_flag = x
        self.terminate_flag_lock.release()

    def getSendQsize(self):
        self.send_packets_lock.acquire()
        qsize = self.send_packets.qsize()
        self.send_packets_lock.release()
        return qsize


    def getRecvQsize(self):
        self.recv_packets_lock.acquire()
        qsize = self.recv_packets.qsize()
        self.recv_packets_lock.release()
        return qsize