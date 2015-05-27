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

class Pipeline(Selector):
    def __init__(self, xml):
        Selector.__init__(self, xml)
        
        pipeline_tree = etree.parse(xml)
        dics = pipeline_tree.xpath("/pipelines/dic")
        hmms = pipeline_tree.xpath("/pipelines/hmm")
    
        dic_file = ""
        for dic in dics:
            f = dic.get("file")
            if f is not None:
                dic_file = f

        hmm_file = ""
        for hmm in hmms:
            f = hmm.get("file")
            if f is not None:
                hmm_file = f
                
		print hmm_file, dic_file
    
        self.__pipeline__ = gst.parse_launch('gsettingsaudiosrc ! audioconvert ! audioresample '
                                        + '! vader name=vad auto_threshold=true '
                                        + '! pocketsphinx name=asr ! fakesink')
                                        
        self.__hmm__   = hmm_file
        self.__dic__   = dic_file
        self.__lm__    = self.__getactivatedlm__("")
        self.__lmctl__ = "lm/lmctl.txt"
        self.__loop__ = gobject.MainLoop()
        self.__previoushyp__ = ""
        
        asr = self.__pipeline__.get_by_name('asr')
        asr.set_property('hmm', hmm)
        asr.set_property('dict', dic)
        asr.set_property('lmctl', self.__lmctl__)
        asr.set_property("lmname", self.__lm__)
        asr.connect('result', self.__onresult__)
        
        bus = self.__pipeline__.get_bus()
        bus.add_signal_watch()
        bus.connect('message::application', self.__onmessage__)
                
    def __play__(self):
        self.__pipeline__.set_state(gst.STATE_PLAYING)
        context = self.__loop__.run()
        
        while True:
            """ use a selector to change the language model """
            lm = self.__getactivatedlm__(self.__previoushyp__)

            if lm is not self.__lm__:
                asr = self.__pipeline__.get_by_name('asr')
                asr.set_property('lmname', lm)  
            
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
        print hyp
        self.__previoushyp__ = hyp
        """self.__send_text__(hyp)"""

    def __send_text__(self, hyp):
        print hyp + " is going to be sent to the manager/n"

if __name__ == '__main__':
    p = Pipeline("pipeline.xml")
    p.__play__()
