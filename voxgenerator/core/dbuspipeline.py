#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dbus.service
import dbus

from dbussessionplugin  import DbusSessionPlugin

class DbusPipeline(DbusSessionPlugin):
    def __init__(self, name):
        DbusSessionPlugin.__init__(self, name)
        self.__hyp__ = ""

    @dbus.service.signal(dbus_interface='org.freedesktop.Voxgenerator',
                         signature='')
    def dbus_pipeline_restart(self):
        self.__logger__.info("dbus: Request to restart the pipeline")

    @dbus.service.signal(dbus_interface='org.freedesktop.Voxgenerator',
                         signature='')
    def dbus_pipeline_stop(self):
        self.__logger__.info("dbus: Request to stop the pipeline")

    @dbus.service.signal(dbus_interface='org.freedesktop.Voxgenerator',
                         signature='')
    def dbus_pipeline_pause(self):
        self.__logger__.info("dbus: Request to pause the pipeline")

    @dbus.service.signal(dbus_interface='org.freedesktop.Voxgenerator',
                         signature='')
    def dbus_pipeline_play(self):
        self.__logger__.info("dbus: Request to put the pipeline ine play")

    @dbus.service.signal(dbus_interface='org.freedesktop.Voxgenerator',
                         signature='ss')
    def dbus_pipeline_transcription(self, lm, s):
        self.__logger__.info("dbus: Sending: " + s + " to the plugin: " + lm)
        self.__hyp__ = s

    @dbus.service.method(dbus_interface='org.freedesktop.Voxgenerator',
                        in_signature='', out_signature='s')
    def dbus_get_transcription(self):
        return self.__hyp__
