#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from command_selector import FuzzySelector
from receiver import Receiver

class Plugin(Receiver):
    def __init__(self, ip, port):
        Receiver.__init__(self, ip, port)
        self.__selector__ = FuzzySelector()
        self.__function__ = {}
        self.__command__  = {}

    def __build__(self, name, rebuild):
        self.__selector__.__build__(name, self.__command__, rebuild)

    def __receive__(self):
        conn, addr = self.__sock__.accept()
        while True:
            data = conn.recv(128)
            if not data:
                break
            
            fields = data.split("::")
            name = fields[0]
            hyp  = fields[1]

            self.__process__(name, hyp)
        self.__sock__.close()
            
    def __process__(self, name, hyp):
        raise NotImplementedError('subclasses must override __process__()!')
