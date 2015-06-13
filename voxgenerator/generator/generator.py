#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from lxml import etree
import os.path

class Generator:
    def __init__(self):
        self.__count_sep__ = 0
        self.__id__       = -1
        self.__name__     = ""
        self.__reload__   = False 

    def __right__(self):
        self.__count_sep__ += 4
            
    def __left__(self):
        if self.__count_sep__ >= 4:
            self.__count_sep__ -= 4
        else:
            self.__count_sep__ = 0
        
    def __sep__(self):
        sep = ""
        for space in range(self.__count_sep__):
            sep += " "
        return sep   
        
    def __generate_close__(self):
        self.__put__("")
        self.__put__("if __name__ == '__main__':")
        self.__right__()
        self.__put__("p = " + self.__name__ + "()")
        self.__left__()
        self.__f__.close()

    def __put__(self, line):
        self.__f__.write(self.__sep__() + line + "\n")
