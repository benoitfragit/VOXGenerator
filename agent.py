#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, signal
from sender import Sender
from receiver import Receiver

class AbstractAgent():
    def __init__(self):
        self.__pid__     = os.getpid()        
        self.__types__   = self.__enum__("Invalid", "Manager", "Controller", "Pipeline", "Plugin")
        self.__actions__ = self.__enum__("Invalid", "Register", "Result", "Pause", "Stop", "Resume")
       
        self.__type__    = self.__types__.Invalid
        self.__action__  = self.__actions__.Invalid
        self.__functions__ = {}
        
    def __enum__(self, *args):
        enum = dict(zip(args, range(len(args))))
        return type('Enum', (), enum)

class ManagerAgent(Receiver,AbstractAgent):
    def __init__(self):
        AbstractAgent.__init__(self)
        Receiver.__init__(self, "127.0.0.1", 5005)
        
        self.__agents__ = {}
        self.__agents__["Manager"] = self.__pid__
        
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
            print "receive !"
            data, addr = self.__sock__.recvfrom(128)
            fields = data.split("::")
            action = int(fields[0])
            pid    = int(fields[1])
            name   = fields[2]
            
            print name, pid
            
            if action == self.__action__:
                self.__functions__[action](pid, name)
            
            
class ControllerAgent(Sender, AbstractAgent):
    def __init__(self):
        AbstractAgent.__init__(self)
        Sender.__init__(self, "127.0.0.1", 5005)
        
        self.__functions__ = {self.__actions__.Register:self.__register__,
                      self.__actions__.Pause:self.__pause__,
                      self.__actions__.Stop:self.__stop__,
                      self.__actions__.Resume:self.__resume__}
    
    def __register__(self, name):
        self.__send__(str(self.__actions__.Register) + "::" + str(self.__pid__) + "::" +  name)

    def __pause__(self, pid, name):
        self.__send__(str(self.__actions__.Pause) + "::" + str(pid) + "::" +  name)

    def __stop__(self, pid, name):
        self.__send__(str(self.__actions__.Stop) + "::" + str(pid) + "::" +  name)
    
    def __resume__(self, pid, name):
        self.__send__(str(self.__actions__.Resume) + "::" + str(pid) + "::" +  name)

class PipelineAgent(Sender,AbstractAgent):
    def __init__(self):
        AbstractAgent.__init__(self)
      
        Sender.__init__(self, "127.0.0.1", 4000)

        self.__type__   = self.__types__.Pipeline
        self.__action__ = self.__actions__.Result
        
        self.__functions__ = {self.__actions__.Result:self.__result__}
        
    def __result__(self, name, hyp):
        print "SENDING " + hyp + " TO " + name + "\n" 
        msg = str(self.__actions__.Result) + "::" + name + "::" + hyp
        self.__send__(msg)

class PluginAgent(Receiver, AbstractAgent):
    def __init__(self):
        AbstractAgent.__init__(self)
        Receiver.__init__(self, "127.0.0.1", 4005)
        self.__type__   = self.__types__.Plugin
        self.__action__ = self.__actions__.Result

        self.__functions__ = {self.__actions__.Result:self.__result__}
    
    def __result__(self, name, hyp):
        raise NotImplementedError('subclasses must override __result__()!')

    def __receive__(self):
        while True:
            data, addr = self.__sock__.recvfrom(128)
            fields = data.split("::")
            action = int(fields[0])
            name = fields[1]
            hyp = fields[2]
            
            if action == self.__action__:
                self.__result__(name, hyp)
