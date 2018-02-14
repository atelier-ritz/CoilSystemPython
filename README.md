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
|
└───fieldManager.py
│   	|   s826.py
│  
│
└───visoin.py
│       │   filterlib.py
│       │   objectDetection.py
│
│
└───subthread.py

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
