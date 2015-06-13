WHAT ARE PLUGINS ?
=================

How to write plugin ?
------------------------

You should write in an xml file. This xml is going to be use by the pipeline.
Here I will show you how to write plugin.

``` XML
	<plugin id="0" name="Desktop" reload="False" ip="127.0.0.1" port="5100">
		<package name="time" module="localtime"/>
		<command name="home"      transcription="ouvre mon dossier personnel" type="system" exec="xdg-open /home/benoit"/>
		<command name="documents" transcription="ouvre mes documents"         type="system" exec="xdg-open /home/benoit/Documents"/>
        <command name="musiques"  transcription="ouvre ma musique"            type="system" exec="xdg-open /home/benoit/Musique"/>
		<command name="images"    transcription="ouvre mes images"            type="system" exec="xdg-open /home/benoit/Images"/>
        <command name="projets"   transcription="ouvre mes projets"           type="system" exec="xdg-open /home/benoit/Projet"/> 
        <command name="heure"     transcription="quelle heure est t-il"       type="custom"/>
    </plugin>
    
    <plugin id="1" name="Action" reload="False" ip="127.0.0.1" port="6000">
		<command name="copier" transcription="copier ceci" type="system" exec="xdotool key ctrl+c"/>
		<command name="coller" transcription="coller ici"  type="system" exec="xdotool key ctrl+v"/>
		<command name="couper" transcription="couper ceci" type="system" exec="xdotool key ctrl+x"/>
	</plugin>
```

To define a new plugin should add a new node plugin int the xml file. This plugin should have an uniq id, name. Then you have to specify the ip adress and the port your are going to use for this plugin. They are important ! Because they make you able to deploy your plugins on distant platforms.

Then you can add all command, each of them should have a name, a transcription (the sentence you are going to pronounce to start thist command), a type. If this type is system then you can specify the system command you want to use else you will have to overwrite this command by heriting from this plugin. I will show you an example in a few lines.

Before I need to comment the speciaf flag reload that you can see for every plugin. this flag determine whether or not we should rebuild the tf-idf model used to find the good command to use when the plugin receive text.

When the generator is going to read the example file, it will create two Python plugin:


The first one !
``` Python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, logging    
from voxgenerator import Plugin
class Desktop(Plugin):
    def __init__(self):
        Plugin.__init__(self, '127.0.0.1', 5100)
        self.__id__ = 0
        self.__name__ = 'Desktop'

        self.__logger__ = logging.getLogger('voxgenerator.Desktop')
        self.__function__[0] = self.home
        self.__function__[1] = self.documents
        self.__function__[2] = self.musiques
        self.__function__[3] = self.images
        self.__function__[4] = self.projets
        self.__function__[5] = self.heure
        
        self.__command__[0] = 'ouvre mon dossier personnel'
        self.__command__[1] = 'ouvre mes documents'
        self.__command__[2] = 'ouvre ma musique'
        self.__command__[3] = 'ouvre mes images'
        self.__command__[4] = 'ouvre mes projets'
        self.__command__[5] = 'quelle heure est t-il'
        
        self.__build__('Desktop', False)
        self.__receive__()
    
    def home(self):
        os.system('xdg-open /home/benoit')
    
    def documents(self):
        os.system('xdg-open /home/benoit/Documents')
    
    def musiques(self):
        os.system('xdg-open /home/benoit/Musique')
    
    def images(self):
        os.system('xdg-open /home/benoit/Images')
    
    def projets(self):
        os.system('xdg-open /home/benoit/Projet')
    
    def heure(self):
        raise NotImplementedError('subclasses must override heure()!')

if __name__ == '__main__':
    p = Desktop()

```

and the second one
``` Python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, logging    
from voxgenerator import Plugin
class Action(Plugin):
    def __init__(self):
        Plugin.__init__(self, '127.0.0.1', 6000)
        self.__id__ = 1
        self.__name__ = 'Action'

        self.__logger__ = logging.getLogger('voxgenerator.Action')
        self.__function__[0] = self.copier
        self.__function__[1] = self.coller
        self.__function__[2] = self.couper
        
        self.__command__[0] = 'copier ceci'
        self.__command__[1] = 'coller ici'
        self.__command__[2] = 'couper ceci'
        
        self.__build__('Action', False)
        self.__receive__()
    
    def copier(self):
        os.system('xdotool key ctrl+c')
    
    def coller(self):
        os.system('xdotool key ctrl+v')
    
    def couper(self):
        os.system('xdotool key ctrl+x')

if __name__ == '__main__':
    p = Action()

```

You can see in the plugin Desktop that a method should be overwritten. So I'v written a python script that heritate from this plugin:

``` Python
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

```

As you can see the heure method is overwritten to speak the current time.

Ok now you know every thins about plugins ! 