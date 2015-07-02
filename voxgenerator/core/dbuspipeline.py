#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dbus.service
import dbus

from dbussessionplugin  import DbusSessionPlugin

class DbusPipeline(DbusSessionPlugin):
    def __init__(self, name):
        DbusSessionPlugin.__init__(self, name)
        self.__hyp__ = ""
        self.__playing__ = False

    @dbus.service.signal(dbus_interface='org.freedesktop.Voxgenerator',
                         signature='')
    def dbus_pipeline_pause(self):
        self.__playing__ = False
        self.__logger__.info("dbus: Request to pause the pipeline")

    @dbus.service.signal(dbus_interface='org.freedesktop.Voxgenerator',
                         signature='b')
    def dbus_pipeline_play(self, status):
        self.__playing__ = status
        self.__logger__.info("dbus: Request to put the pipeline in play")

    @dbus.service.signal(dbus_interface='org.freedesktop.Voxgenerator',
                         signature='ss')
    def dbus_pipeline_transcription(self, lm, s):
        self.__logger__.info("dbus: Sending: " + s + " to the plugin: " + lm)
        self.__hyp__ = s

    @dbus.service.method(dbus_interface='org.freedesktop.Voxgenerator',
                        in_signature='', out_signature='s')
    def dbus_get_transcription(self):
        return self.__hyp__

    @dbus.service.method(dbus_interface='org.freedesktop.Voxgenerator',
                        in_signature='', out_signature='b')
    def dbus_pipeline_request_status(self):
        return self.__playing__

    @dbus.service.method(dbus_interface='org.freedesktop.Voxgenerator',
                        in_signature='', out_signature='b')
    def dbus_pipeline_request_stop(self):
        self.__loop__.quit()
        try:
            self.__stop__()
        except:
            self.__logger__.critical("You overwrite method __stop__")

    @dbus.service.method(dbus_interface='org.freedesktop.Voxgenerator',
                        in_signature='', out_signature='s')
    def dbus_pipeline_request_description(self):
        return self.__getdescription__()

    def __getdescription__(self):
        raise NotImplementedError('subclasses must override !')

    def __stop__(self):
         raise NotImplementedError('subclasses must override !')
