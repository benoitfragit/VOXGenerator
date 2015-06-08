#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket

class Receiver:
    def __init__(self, ip, port):
        self.__ip__   = ip
        self.__port__ = port
        self.__sock__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
        self.__sock__.bind((self.__ip__, self.__port__))
        self.__sock__.listen(1)

    def __receive__(self):
        raise NotImplementedError('subclasses must override __receive__()!')

if __name__ == '__main__':
    receiver = Receiver("127.0.0.1", 5005)
