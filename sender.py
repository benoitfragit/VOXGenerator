#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket

class Sender:
    def __init__(self, ip, port):
        self.__ip__   = ip
        self.__port__ = port
        self.__sock__ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    """ each pipeline should register itself at startup"""
    def __register__(self, id):
        self.__sock__.sendto( str(id) + ":register:", (self.__ip__, self.__port__))

    """ each pipeline should send its result """
    def __result__(self, id, hyp):
        self.__sock__.sendto(str(id) + ":result:" + hyp + ":" + str(prob), (self.__ip__, self.__port__))

    """ the manager publish the result to all plugins """
    def __publish__(self, id, hyp):
        self.__sock__.sendto(str(id) + ":publish:" + hyp, (self.__ip__, self.__port__)
    
    """ all plugins send an acknowledge with a score"""
    def __acknowledge__(self, id, hyp, score):
        self.__sock__.sendto(str(id) + ":acknowledge:" + hyp + ":" + str(score), (self.__ip__, self.__port__))
    
    """ the manager allow th good plugin to execute the command """
    def __execute__(self, id, hyp):
        self.__sock__.sendto(str(id) + ":execute:" + hyp, (self.__ip__, self.__port__))
    
if __name__ == '__main__':
    sender = Sender("127.0.0.1", 5005)
    sender.__register__(0)
