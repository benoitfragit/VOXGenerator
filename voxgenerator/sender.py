#!/usr/bin/env python   
# -*- coding: utf-8 -*-

import sys
import socket

class Sender:
    def __init__(self, ip, port):
        self.__ip__   = ip
        self.__port__ = port
        self.__sock__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.__connected__ = False

    def __send__(self, msg):
        if self.__connected__ == False:
            self.__sock__.connect((self.__ip__, self.__port__))
            self.__connected__ = True
        
        self.__sock__.send(msg)
    
if __name__ == '__main__':
    sender = Sender("127.0.0.1", 5005)
