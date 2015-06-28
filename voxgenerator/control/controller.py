#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
import tkFileDialog, dbus, dbus.service, os

class Controller:
    def __init__(self):
        self.__isservicerunning__ = False
        self.__pipelinedescriptionfile__ = None
        self.__pipelineplaying__ = False
        self.__plugins__ = ["oui", "non"]
        self.__initializecontroller__()

    def __initializecontroller__(self):
        """
        get service state
        """
        self.__bus__ = dbus.SessionBus()
        try:
            pipe = self.__bus__.get_object("org.freedesktop.Voxgenerator.Pipeline",
                                            "/org/freedesktop/Voxgenerator/Pipeline")

            self.__pipelineplaying__ = pipe.dbus_pipeline_request_status()
            self.__isservicerunning__ = True
        except:
            self.__isservicerunning__ = False
            self.__pipelineplaying__  = False

    def __applyservicestatus__(self, var):
        if  var == 1 or var == True:
            new_status = True
        else:
            new_status = False

        if self.__isservicerunning__ != new_status:
            self.__isservicerunning__ = new_status

            if new_status == False:
                try:
                    pipe = self.__bus__.get_object("org.freedesktop.Voxgenerator.Pipeline",
                                                   "/org/freedesktop/Voxgenerator/Pipeline")
                    pipe.dbus_pipeline_request_stop()
                except:
                    print "Unable to stop the pipeline !"
            else:
                try:
                    pipe = self.__bus__.get_object("org.freedesktop.Voxgenerator.Pipeline",
                                                   "/org/freedesktop/Voxgenerator/Pipeline")
                    pipe.dbus_pipeline_request_stop()
                except:
                    print "No need to stop the pipeline !"

                if self.__pipelinedescriptionfile__ is not None and os.path.isfile(self.__pipelinedescriptionfile__):
                    os.system("run_voxgenerator " + self.__pipelinedescriptionfile__ + " &")

    def __applypipelinestatus__(self, var):
        if var == 1 or var == True:
            new_status = True
        else:
            new_status = False

        if self.__pipelineplaying__ != new_status:
            self.__pipelineplaying__ = new_status
            print "pipeline playing " + str(new_status)

    def __setnewdescription__(self, f):
        self.__pipelinedescriptionfile__ = f
