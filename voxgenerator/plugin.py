#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, logging
from activation import *
from command_selector import FuzzySelector
from receiver import Receiver

class Plugin(Receiver):
    def __init__(self, ip, port):
        Receiver.__init__(self, ip, port)
        
        logging.basicConfig(level=logging.DEBUG)
        
        self.__selector__ = FuzzySelector()
        self.__function__ = {}
        self.__command__  = {}

    def __build__(self, name, rebuild):
        self.__selector__.__build__(name.lower(), self.__command__, rebuild)

    def __receive__(self):
        conn, addr = self.__sock__.accept()
        try:
            while True:
                data = conn.recv(128)
                if not data:
                    break
            
                fields = data.split("::")
                name = fields[0]
                hyp  = fields[1]

                self.__process__(name, hyp)
        finally:
            self.__sock__.close()
            
    def __process__(self, name, hyp):
        if self.__name__ == name:
            self.__logger__.info(name + ' receive : ' + hyp)
            idx = self.__selector__.__query__(hyp)
            if self.__function__.has_key(idx):
                try:
                    self.__function__[idx]()
                except :
                    self.__logger__.critical(name + ' should overwrite method process')
