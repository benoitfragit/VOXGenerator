#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dbus.service
import dbu

from dbussessionplugin import DbusSessionPlugin

class DbusPlugin(DbusSessionPlugin):
    def __init__(self, name):
        DbusSessionPlugin.__init__(self, name)
        
        self.__bus__.add_signal_receiver(dbus_on_transcription, dbus_interface = 'org.freedesktop.Voxgenerator', signal_name = "DbusPipelineTranscription")

    def dbus_on_transcription(self, name):
        if self.__name__ == name:
            pipeline = self.__bus__.get_object(self.__dbus_signature__, self.__dbus_path__)
            hyp = pipeline.dbus_get_transcription()
            try:
                self.__dbus_process_hyp__(hyp)
            except:
                self.__logger__.info("you should overwrite method __dbus_process_hyp__!")

    def __dbus_process_hyp__(self, hyp):
        raise NotImplementedError('subclasses must override __dbus_process_hyp_()!')
