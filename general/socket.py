#!/usr/bin/python
# -*- coding: UTF-8 -*-

from enum import IntEnum

import socket


class OperationEnum(IntEnum):
    PROCEED=0x00



class GamePacket:
    def __init__(self):
        self.index_number = 0
        self.operation_number = 0
