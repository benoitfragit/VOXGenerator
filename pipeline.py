#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gobject
import pygst
pygst.require('0.10')
gobject.threads_init()
import gst

class Pipeline:
    def __init__(self, id, hmm, dic, lm):
        self.__id__ = id
        self.__pipeline__ = gst.parse_launch('gsettingsaudiosrc ! audioconvert ! audioresample '
                                        + '! vader name=vad auto_threshold=true '
                                        + '! pocketsphinx name=asr ! fakesink')
                                        
        self.__hmm__ = hmm
        self.__dic__ = dic
        self.__lm__ = lm
        self.__loop__ = gobject.MainLoop()
        
        asr = self.__pipeline__.get_by_name('asr')
        asr.set_property('hmm', hmm)
        asr.set_property('dict', dic)
        asr.set_property('lm', lm)
        asr.connect('result', self.__onresult__)
        
        bus = self.__pipeline__.get_bus()
        bus.add_signal_watch()
        bus.connect('message::application', self.__onmessage__)
                
    def __play__(self):
        self.__pipeline__.set_state(gst.STATE_PLAYING)
        self.__loop__.run()

    def __pause__(self):
        self.__pipeline__.set_state(gst.STATE_PAUSED)       

    def __onresult__(self, asr, text, uttid):
        struct = gst.Structure('result')
        struct.set_value('hyp', text)
        struct.set_value('uttid', uttid)
        asr.post_message(gst.message_new_application(asr, struct))

    def __onmessage__(self, bus, msg):
        if msgtype == 'result':
            self.__onfinalresult__(msg.structure['hyp'], msg.structure['uttid'])

    def __onfinalresult__(self, hyp, uttid):
        self.__process__(hyp, uttid)

	def __process__(self, hyp, uttid):
		raise NotImplementedError('subclasses must override __process__()!')

	def __send_text__(self, hyp, uttid):
		print hyp + " is going to be sent to the manager/n"

if __name__ == '__main__':
    p = Pipeline(0, 'sphinx/hmm', 'sphinx/dictionnary.dic', 'sphinx/model.lm.dmp')
    p.__play__()
