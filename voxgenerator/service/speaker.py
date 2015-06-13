#!/usr/bin/env python
# -*- coding: utf-8 -*-

from espeak import espeak

class Speaker :
    def __init__(self, voice, gender):
        espeak.set_voice(voice, '', gender, 0, 0)
    
    def __say__(self, txt):
        espeak.synth(txt)    
