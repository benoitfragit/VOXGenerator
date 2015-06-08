#!/usr/bin/env python   
# -*- coding: utf-8 -*-

import sys
import socket
from select import select

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
    
    def __receive__(self):
        readable, writable, exceptional = select([self.__sock__], [], [], 0)
        if readable:
            try:
                data = self.__sock__.recv(128)
                if data is not None:
                    print data
            except:
                print "not connected !"
        
if __name__ == '__main__':
    sender = Sender("127.0.0.1", 5005)
