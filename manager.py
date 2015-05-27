#!/usr/bin/env python
# -*- coding: utf-8 -*-

from receiver import Receiver
from sender   import Sender

class Manager(Receiver, Sender):
    def __init__(self, out_ip, out_port, in_ip, in_port):
        Sender.__init__(self, out_ip, out_port)
        Receiver.__init__(self, in_ip, in_port)
    
        self.__registered__ = []
        self.__acknowledge__ = {}
        
    def __receive__(self):
        while True:
            data, addr = self.__sock__.recvfrom(1024)
            if data is not None:
                fields = data.split(':')
                id     = fields[0]
                action = fields[1]
                
                if   action == "register":
                    self.__registered__.append(id)
                    print "Id " + str(id) + " has been registered !"
                elif action == "result"
                    if id is in self.__registered__:
                        result = fields[2]
                        self.__publish__(id, hyp)
                elif action == "acknowledge":
                    if id is in self.__registered__:
                        score = fields[3]
                        self.__acknowledge__[id] = score
                    
                    acknowledged = True
                    for i in self.__registered__:
                        if not self.__acknowledge.haskey(i):
                            acknowledged = False
                            break 
                    
                    if acknowledged == True:
                        ss = [self.__acknowledge__[key] for key in self.__acknowledge__]
                        m = max(ss)
                        for key in self.__acknowledge__:
                            s = self.__acknowledge__[key]
                            if s == m:
                                self.__execute__(key, fields[2])
                                break
                                
                        self.__acknowledge__ = {}
