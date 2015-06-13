#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Xlib import display

class Display:
    def __init__(self):
        self.__display__ = display.Display()
        
    def __compute_active_window__(self):
        window = self.__display__.get_input_focus().focus
        wmname = window.get_wm_name()
        wmclass = window.get_wm_class()
        if wmclass is None and wmname is None:
            window = window.query_tree().parent
            return window.get_wm_name()

        return wname
        
    def __compute_mouse_position__(self):
        data = self.__display__.screen().root.query_pointer()._data
        return data["root_x"], data["root_y"]
        
if __name__ == '__main__':
    x = Display()
    
    print x.__compute_active_window__()
    print x.__compute_mouse_position__()
