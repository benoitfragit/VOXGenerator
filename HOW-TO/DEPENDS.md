INSTALL DEPENDANCIES
====================

Voice Recognition dependancies
------------------------------------

We are going to install all dependancies to run Pocketsphinx. Let' go, open a terminal and type the following lines:

``` Bash
mkdir sphinx
cd sphinx
git clone git://github.com/cmusphinx/sphinxbase.git
cd sphinxbase
./autogen.sh
make
sudo make install
cd ..
git clone git://github.com/cmusphinx/pocketsphinx.git
cd pocketsphinx
./autogen.sh
make 
sudo make install
```

Follow this [tutorial](http://cmusphinx.sourceforge.net/wiki/cmuclmtkdevelopment) to install cmuclmtk suite.

Install all other dependancies
-----------------------------------

``` Bash
sudo apt-get install libgirepository-1.0.1 libgirepository1.0-dev libgstreamer-plugins-base0.10-0 libgstreamer-plugins-bad0.10-0 gir1.2-gstreamer-0.10 libgstreamer-plugins-base0.10-dev libgstreamer0.10-dev libgstreamer0.10-0 gstreamer0.10-alsa python-dev python-pip bison python-time python-espeak python-xlib
``` 

Grab all required files for your langage
-------------------------------------------

You can go to this [page](http://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/) to find an acoustic model, a dictionnary and a langage model for your voice.

