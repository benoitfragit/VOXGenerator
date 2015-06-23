#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, gi, sys

gi.require_version('Gst', '1.0')
from gi.repository import Gst
from gi.repository import GObject

GObject.threads_init()
Gst.init(None)

class Pipeline():
    def __init__(self): 
        """ some file to configure the pipe """               
        self.__dic__   = "/home/benoit/Bureau/Projet/VOXGenerator/test/sphinx/dictionnary.dic"
        self.__hmm__   = "/home/benoit/Bureau/Projet/VOXGenerator/test/sphinx/hmm"
        self.__lmctl__ = "/home/benoit/Bureau/Projet/VOXGenerator/test/lm/lmctl.txt"

        """ very simple pipe """
        self.__pipeline__ = Gst.parse_launch('alsasrc ! audioconvert ! audioresample ! pocketsphinx name=asr ! fakesink')
            
        """ the lmname """ 
        self.__lm__    = "Desktop"
        
        self.__loop__ = GObject.MainLoop()
        self.__previoushyp__ = ""
        
        """ grab the pocketsphinx element 
            without putting asr.set_property("configured", True) all other set_property have no effect on the pocketsphinx
            but calling asr.set_property("configured", True) lead to a segfault 
        """        
        asr = self.__pipeline__.get_by_name('asr')

        asr.set_property('lmctl',  self.__lmctl__)
        asr.set_property("lmname", self.__lm__)
        asr.connect('result', self.__onresult__)
    
                                
    def __run__(self):
        self.__pipeline__.set_state(Gst.State.PLAYING)
        self.__loop__.run()

    def __pause__(self):
        self.__pipeline__.set_state(Gst.State.PAUSED)       

    def __onresult__(self, asr, text):        
        print "result: " + text

if __name__ == '__main__':
    p = Pipeline()
    p.__run__()
