# CoilSystemPython

A Python3-based program for the coil system

## Usage

open terminal and cd to the target directory

python3 main.py

## Program Structure
	
```
main.py

callbacks.py
│
│   
└───syntax.py [highlight the keywords in GUI editor_vision]
|
└───fieldManager.py [send commands to s826; store the current field strength]
│   	|   s826.py [control the s826 I/O]
│  
│
└───visoin.py [capture frames; apply filters; object detection]
│       │   filterlib.py [define filters]
│       │   objectDetection.py [define object detection algorithms]
│
│
└───subthread.py [finish multithreading tasks]

```
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
