# CoilSystemPython

A Python3-based program for the coil system

## Usage

open terminal and cd to the target directory

python3 main.py

## Program Structure

main
|
---callbacks.py
	|
	--------fieldManager.py-------s826.py
	|
	--------vision.py
	|	|
	|	-------------filterlib.py
	|	|
	|	-------------objectDetection.py
	|
	|
	--------subthread.py
	
.
+-- _config.yml
+-- _drafts
|   +-- begin-with-the-crazy-ideas.textile
|   +-- on-simplicity-in-technology.markdown
+-- _includes
|   +-- footer.html
|   +-- header.html
+-- _layouts
|   +-- default.html
|   +-- post.html
+-- _posts
|   +-- 2007-10-29-why-every-programmer-should-play-nethack.textile
|   +-- 2009-04-26-barcamp-boston-4-roundup.textile
+-- _data
|   +-- members.yml
+-- _site
+-- index.html

## Dependencies

1. opencv

pip3 install opencv-python

pip3 install opencv-contrib-python

2. pyqt5

pip3 install pyqt5

3. pydc1394

https://github.com/jordens/pydc1394

## GUI Designer

qt-designer is used.

sudo apt-get install qt4-designer

## USB camera or Firewire Camera

Can specify the camera in vision.py
