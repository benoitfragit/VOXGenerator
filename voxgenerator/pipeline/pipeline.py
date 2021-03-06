 #!/usr/bin/env python
# -*- coding: utf-8 -*-

from selector import Selector

import os
import gobject
import pygst
import threading
pygst.require('0.10')
gobject.threads_init()
import gst
import os, sys
from lxml import etree

from voxgenerator.core import DbusPipeline

class Pipeline(Selector, DbusPipeline):
    def __init__(self, xml):
        DbusPipeline.__init__(self, 'Pipeline')
        Selector.__init__(self, xml)

        pipeline_tree = etree.parse(xml)
        root = pipeline_tree.xpath("/pipelines")

        self.__description__ = xml
        self.__thread__ = None
        self.__stopthread__ = False
        self.__dic__ = root[0].find("dic").get("file")
        self.__hmm__ = root[0].find("hmm").get("file")

        self.__pipeline__ = gst.parse_launch('gsettingsaudiosrc ! audioconvert ! audioresample '
                                        + '! vader auto-threshold=true ! pocketsphinx name=asr ! fakesink')
        self.__lm__    = self.__getdefault__()
        self.__previoushyp__ = ""

        asr = self.__pipeline__.get_by_name('asr')
        asr.set_property('hmm',    self.__hmm__)
        asr.set_property('dict',   self.__dic__)
        asr.set_property('lmctl',  self.__lmctl__)
        asr.set_property("lmname", self.__lm__)
        asr.connect('result', self.__onresult__)

    def __run__(self):
        self.__thread__ = threading.Thread(target=self.__updateactivatedlm__)
        self.__thread__.start()
        self.__pipeline__.set_state(gst.STATE_PLAYING)
        self.dbus_pipeline_play(True)
        self.__loop__.run()

    def __updateactivatedlm__(self):
        """ use a selector to change the language model """
        while self.__stopthread__ != True:
            lm = self.__getactivatedlm__(self.__previoushyp__)

            if lm is not self.__lm__:
                asr = self.__pipeline__.get_by_name('asr')
                asr.set_property('lmname', lm)
                self.__lm__ = lm
                self.__logger__.info(lm + " is now active !")

    def __pause__(self):
        self.__pipeline__.set_state(gst.STATE_PAUSED)
        self.dbus_pipeline_pause()

    def __onresult__(self, asr, text, uttid):
        self.__previoushyp__ = text
        self.__logger__.info(self.__lm__ + " will receive " + text)

        try:
            self.dbus_pipeline_transcription(self.__lm__, text)
        except:
            self.__logger__.critical("Plugin " + self.__lm__ + " hasn't been started !")

    def __stop__(self):
        self.__stopthread__ = True
        self.__pipeline__.set_state(gst.STATE_NULL)
        self.dbus_pipeline_play(False)

    def __getdescription__(self):
        return self.__description__

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        pipelines_desriptions = sys.argv[1]

        if os.path.isfile(pipelines_description):
            p = Pipeline(pipelines_descriptions)
            p.__run__()
