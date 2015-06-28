#!/usr/bin/env python
# -*- coding: utf-8 -*-

from controller import Controller
from Tkinter import *
import tkFileDialog

class View(Controller, Tk):
    def __init__(self, parent):
        Controller.__init__(self)
        Tk.__init__(self, parent);

        self.__parent__ = parent

        self.__serviceactivated__ = BooleanVar()
        self.__serviceactivated__.set(self.__isservicerunning__)

        self.__pipelinedescription__ = StringVar()
        self.__pipelinedescription__.set("Unknown")

        self.__pipelineactivated__ = BooleanVar()
        self.__pipelineactivated__.set(self.__pipelineplaying__)

        self.__initialize__()

    def __initialize__(self):
        """
        building global frame
        """
        frame_service = LabelFrame(self, text="Service")

        label_service = Label(frame_service, text="Service status", anchor="w", justify=LEFT)
        label_service.pack(side=LEFT, fill=X, expand=1, padx=5, pady=5)

        button_service_on  = Radiobutton(frame_service, text="On",  variable=self.__serviceactivated__, value=True,  command=self.__update_service_status__)
        button_service_on.pack(side=LEFT, padx=5, pady=5)

        button_service_off = Radiobutton(frame_service, text="Off", variable=self.__serviceactivated__, value=False, command=self.__update_service_status__)
        button_service_off.pack(side=LEFT, padx=5, pady=5)

        """
        building pipeline frame
        """
        frame_pipe = LabelFrame(self, text="ASR pipeline")

        frame_description = Frame(frame_pipe)
        label_pipe = Label(frame_description, textvariable=self.__pipelinedescription__, anchor="w", justify=LEFT)
        label_pipe.pack(side=LEFT, fill=X, expand=1, padx=5, pady=5)
        button_pipe = Button(frame_description, text="Choose", command=self.__choosedescription__)
        button_pipe.pack(side=LEFT, padx=5, pady=5)
        frame_description.pack(fill=X, padx=5, pady=5)

        frame_status = Frame(frame_pipe)
        label_pipe_status = Label(frame_status, text="Pipeline status", anchor="w", justify=LEFT)
        label_pipe_status.pack(side=LEFT, fill=X, expand=1)
        button_pipe_play  = Radiobutton(frame_status, text="Play",  variable=self.__pipelineactivated__, value=True,  command=self.__update_pipeline_status__)
        button_pipe_play.pack(side=LEFT, padx=5, pady=5)
        button_pipe_pause = Radiobutton(frame_status, text="Pause", variable=self.__pipelineactivated__, value=False, command=self.__update_pipeline_status__)
        button_pipe_pause.pack(side=LEFT, padx=5, pady=5)
        frame_status.pack(fill=X, padx=5, pady=5)

        frame_service.pack(fill=X, padx=5, pady=5)
        frame_pipe.pack(fill=X, padx=5, pady=5)

        """
        build the plugin frame
        """
        frame_plugins = LabelFrame(self, text="Plugins")

        listbox = Listbox(frame_plugins)

        for plugin in self.__plugins__:
            listbox.insert(END, plugin)

        listbox.pack(fill=BOTH, expand=1)
        frame_plugins.pack(fill=BOTH, padx=5, pady=5, expand=1)

        self.resizable(True, True)

    def __update_service_status__(self):
        var = self.__serviceactivated__.get()
        self.__applyservicestatus__(var)

    def __update_pipeline_status__(self):
        var = self.__pipelineactivated__.get()
        self.__applypipelinestatus__(var)

    def __choosedescription__(self):
        f = tkFileDialog.askopenfilename()
        self.__pipelinedescription__.set(f)
        self.__setnewdescription__(f)

if __name__ == '__main__':
    app = View(None)
    app.title('Voxgenerator control')
    app.mainloop()
