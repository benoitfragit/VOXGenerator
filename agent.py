#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from sender import Sender
from receiver import Receiver

class AbstractAgent(Sender, Receiver):
    def __init__(self, id1, port1, id2, port2):
        Receiver.__init__(self, id1, port1)
        Sender.__init__(self, id2, port2)
        
        self.__types__   = self.__enum__("Invalid", "Manager", "Pipeline", "Plugin")
        self.__actions__ = self.__enum__("Invalid", "Register", "Result", "Pause", "Stop", "Resume")
       
        self.__type__    = self.__types__.Invalid
        self.__action__  = self.__actions__.Invalid
        self.__functions__ = {}
        
    def __enum__(self, *args):
        enum = dict(zip(args, range(len(args))))
        return type('Enum', (), enum)

class ManagerAgent(AbstractAgent):
    def __init__(self, id1, port1, id2, port2):
        AbstractAgent.__init__(self, id1, port1, id2, port2)
        self.__agents__ = {}
        
        self.__type__ = self.__types__.Manager

        self.__functions__ = {self.__actions__.Register:self.__register__,
                              self.__actions__.Pause:self.__pause__,
                              self.__actions__.Stop:self.__stop__,
                              self.__actions__.Resume:self.__resume__}
        
    def __register__(self, pid, name):
        self.__agents__[name] = pid  

    def __pause__(self, pid, name):
        if self.__agents__.haskey(name):
            pid = self.__agents__[name]
            os.kill(pid, signal.SIGSTOP)
    
    def __resume__(self, pid, name):
        if self.__agents__.haskey(name):
            pid = self.__agents__[name]
            os.kill(pid, signal.SIGCONG)
    
    def __stop__(self, pid, name):
        if self.__agents__.has_key(name):
            pid = self.__agents__[name]
            os.kill(pid, signal.SIGKILL)
    
    def __receive__(self):
        while True:
            data, addr = self.__sock__.recvfrom(1024)
            fields = int(data.split("::")[0])
            action = fields[0]
            pid    = fields[1]
            name   = fields[2]
            
            if self.__functions__.has_key(action):
                self.__functions__(pid, name)

class PipelineAgent(AbstractAgent):
    def __init__(self, id1, port1, id2, port2):
        AbstractAgent.__init__(self, id1, port1, id2, port2)
        self.__type__   = self.__types__.Pipeline
        self.__action__ = self.__actions__.Result
        
        self.__functions__ = {self.__actions__.Result:self.__result__}
        
    def __result__(self, name, hyp):
        msg = int(self.__actions__.Result) + "::" + name + "::" + hyp
        self.__send__(msg)

class PluginAgent(AbstractAgent):
    def __init__(self, id1, port1, id2, port2):
        AbstractAgent.__init__(self, id1, port1, id2, port2)
        self.__type__   = self.__types__.Plugin
        self.__action__ = self.__actions__.Result

        self.__functions__ = {self.__actions__.Result:self.__result__}
    
    def __result__(self, name, hyp)
        raise NotImplementedError('subclasses must override __result__()!')

    def __receive__(self)::
        while True:
            data, addr = self.__sock__.recvfrom(1024)
            fields = data.split("::")
            action = fields[0]
            name = fields[1]
            hyp = fields[2]
            
            if action == self.__action__:
                self.__result__(name, hyp)
