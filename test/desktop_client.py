#!/usr/bin/env python
# -*- coding: utf-8 -*-

from desktop import Desktop
from voxgenerator import Speaker 
from time import localtime

class DesktopClient(Desktop, Speaker):
    def __init__(self):
        Speaker.__init__(self, "fr", 1)
        Desktop.__init__(self)
    
    def heure(self):
        sentence = "il est " + str(localtime().tm_hour) + " heure et " + str(localtime().tm_min) + " minutes"
        self.__say__(sentence)

if __name__ == '__main__':
    p = DesktopClient()
