#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selector import Selector

import os
import gobject
import pygst
pygst.require('0.10')
gobject.threads_init()
import gst
import os, sys
from lxml import etree
from sender import Sender

class Pipeline(Selector):
    def __init__(self, xml):
        Selector.__init__(self, xml)
        self.__clients__ = {}

        pipeline_tree = etree.parse(xml)
        root = pipeline_tree.xpath("/pipelines")

        self.__loadclientadress__(root[0])
                
        self.__dic__ = root[0].find("dic").get("file")
        self.__hmm__ = root[0].find("hmm").get("file")

        self.__pipeline__ = gst.parse_launch('gsettingsaudiosrc ! audioconvert ! audioresample '
                                        + '! vader name=vad auto_threshold=true '
                                        + '! pocketsphinx name=asr ! fakesink')
            
        self.__lm__    = self.__getdefault__()
        self.__loop__ = gobject.MainLoop()
        self.__previoushyp__ = ""
                
        asr = self.__pipeline__.get_by_name('asr')
        asr.set_property('hmm',    self.__hmm__)
        asr.set_property('dict',   self.__dic__)
        asr.set_property('lmctl',  self.__lmctl__)
        asr.set_property("lmname", self.__lm__)
        asr.connect('result', self.__onresult__)
        
        bus = self.__pipeline__.get_bus()
        bus.add_signal_watch()
        bus.connect('message::application', self.__onmessage__)
                
    def __loadclientadress__(self, root):
        pipelines = root.findall("pipeline")
        for pipe in pipelines:
            name = pipe.get("plugin")
            ip   = pipe.get("ip")
            port = pipe.get("port")
            
            if self.__plugins__.has_key(name) and ip is not None and port is not None:
                self.__clients__[name] = Sender(ip, int(port))
    
    def __play__(self):
        self.__pipeline__.set_state(gst.STATE_PLAYING)
        context = self.__loop__.get_context()
        
        while True:                        
            """ use a selector to change the language model """
            lm = self.__getactivatedlm__(self.__previoushyp__)

            if lm is not self.__lm__:
                asr = self.__pipeline__.get_by_name('asr')
                asr.set_property('lmname', lm)  
                self.__lm__ = lm
            
            context.iteration(True)

    def __pause__(self):
        self.__pipeline__.set_state(gst.STATE_PAUSED)       

    def __onresult__(self, asr, text, uttid):        
        struct = gst.Structure('result')
        struct.set_value('hyp', text)
        struct.set_value('uttid', uttid)
        asr.post_message(gst.message_new_application(asr, struct))

    def __onmessage__(self, bus, msg):
        msgtype = msg.structure.get_name()
        if msgtype == 'result':
            self.__onfinalresult__(msg.structure['hyp'], msg.structure['uttid'])

    def __onfinalresult__(self, hyp, uttid):
        self.__process__(hyp, uttid)

    def __process__(self, hyp, uttid):
        print "client :" + self.__lm__ + " hyp: " + hyp + "\n"
        self.__previoushyp__ = hyp
        self.__clients__[self.__lm__].__send__(self.__lm__  + "::" + hyp)

if __name__ == '__main__':
    p = Pipeline("pipeline.xml")
    p.__play__()