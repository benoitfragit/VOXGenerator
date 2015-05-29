#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

from xlib_utils import XlibUtils
        
class AbstractActivation:
    def __init__(self):
        self.__display__ = XlibUtils()
        
        self.__types__     = self.__enum__("Invalid", "Window", "Keyword", "Mouse")
        self.__functions__ = {self.__types__.Window : self.__windowactivation__,
                              self.__types__.Keyword : self.__keywordactivation__,
                              self.__types__.Mouse : self.__mouseactivation__}

        self.__type__ = self.__types__.Invalid

    def __enum__(self, *args):
        enum = dict(zip(args, range(len(args))))
        return type('Enum', (), enum)

    def __keywordactivation__(self, *a):
        raise NotImplementedError('subclasses must override !')
    
    def __windowactivation__(self, *a):
        raise NotImplementedError('subclasses must override !')     

    def __mouseactivation__(self, *a):
        raise NotImplementedError('subclasses must override !')

    def __isactive__(self, *a):
        state = self.__functions__[self.__type__](a) 
        return state

class WindowActivation(AbstractActivation):
    def __init__(self, window):
        AbstractActivation.__init__(self)
        self.__type__ = self.__types__.Window
        self.__window__ = window
        
    def __windowactivation__(self, *a):
        win = self.__display__.__compute_active_window__()
        return win is self.__window__

class KeywordActivation(AbstractActivation):
    def __init__(self, keyword):
        AbstractActivation.__init__(self)
        self.__type__    = self.__types__.Keyword   
        self.__keyword__ = keyword
    
    def __keywordactivation__(self,  *a):
        return a[0][0] is self.__keyword__

class MouseActivation(AbstractActivation):
    def __init__(self, area):
        AbstractActivation.__init__(self)
        self.__type__ = self.__types__.Mouse
        self.__area__ = area
    
    def __mouseactivation__(self, *a):
        x, y = self.__display__.__compute_mouse_position__()
        return self.__area__[0] <= x and x <= self.__area__[1] and self.__area__[2] <= y and y <= self.__area__[3]
