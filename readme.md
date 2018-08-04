# CoilSystemPython

A Python3-based program for the coil system. Ported from C code.

## Features
* Control the electromagnetic coils via s826 PCI I/O board.
* Realtime vision feedback from firewire/USB cameras.
* Filtering and pre-processing of the images.
* Object detection algorithm.
* Qt5-based GUI, which allows easy customization.
* Multithreading module for controlling multiple agents according to the feedback data from the cameras.
* Preview window (60 Hz) for the X, Y, and Z magnetic field.
* Controlling the magnetic field with a Joystick controller.
            
Contents
--------------------

<!-- TOC orderedList:true -->


1. [Usage](#usage)
    1. [Installation](#installation)
    2. [How to run](#how-to-run)
    3. [Utilities](#utilities)
2. [Structure](#structure)
3. [Vision](#vision)
    1. [Camera](#camera)
    2. [Filters](#filters)
    3. [Object Detection](#object-detection)
4. [New Features](#new-features)
    1. [Joystick support - Mar 15, 2018](#joystick)
    2. [Signal Generator - Mar 22, 2018](#signal-generator)
    3. [Field Preview Window - Mar 24, 2018](#preview-window)
    4. [Drawing feature - Jun 14, 2018](#drawing)
    5. [Video recording and snapshot feature - Aug 4, 2018](#recording)

5. [Known Issues](#known-issues)

<!-- /TOC -->


## Usage

### Installation

New(Apr 6, 2018): Updated "autoInstall.sh" that helps install all packages automatically. Many thanks to Omidy. The file can be found in "utilities". 

```
1. Download "autoInstall.sh" to your local folder.

2. Download "s826 linux driver" (http://www.sensoray.com/PCI_Express_digital_output_826.htm) and "pydc139" (https://github.com/jordens/pydc1394). 

3. Name the extracted folders as "s826" and "pydc1394". Put them in the same directory as "autoInstall.sh".

4. Open terminal in the current directory and run command "sudo bash ./autoInstall.sh".
```

This bash file installs all the following dependencies:

1. opencv

```
pip3 install opencv-python

pip3 install opencv-contrib-python
```

2. pyqt5

```
pip3 install pyqt5
```

3. pydc1394

https://github.com/jordens/pydc1394

4. s826Driver

Download "Linux Software Development Kit" and follow the instructions in Readme.

http://www.sensoray.com/products/826.htm

5. General python packages such as matplotlib and numpy

6. "qt-designer" is used for designing the GUI of the program.

```
sudo apt-get install qttools5-dev-tools
```

### How to run

open terminal and cd to the target directory and run

```
python3 main.py
```

### Utilities

#### Screen Recording

SimpleScreenRecorder doesn't work property in Ubuntu 17 because it rolls back to GNOME (it used Unity in previous versions).

As a substitute, you can use green-recorder https://github.com/foss-project/green-recorder

You might have some trouble dealing with the .webm format of the video though. :P

#### Listing all available firewire cameras

There is a sample program in Utilities folder that lists up the guid of all available firewire cameras.

## Structure

To have a better understanding of the program, I would recommend you first have a look at "fieldManager.py".

After that, open the GUI and "callbacks.py" to follow the signal flow and event handler (pyqtSlot).

Go through "vision.py" to see how images are processed, and "objectDetection.py" to see how objects are detected and stored in instances of Agent class.

Read "subthread.py" in the end because it uses all the above-mentioned classes to do some complex stuff. E.g. Apply a rotational field with time-varying frequency/magnitude based on the position of the object detected.

![Layout](https://github.com/atelier-ritz/CoilSystemPython/blob/master/documentation/layout.png)

```
main.py

callbacks.py
│
└───mathfx.py [some macros for maths] 
└───syntax.py [highlight the keywords in GUI editor_vision]
|
└───fieldManager.py [send commands to s826; store XYZ field strength]
│   	|   s826.py [control s826 I/O]
│  
│
└───visoin.py [capture frames; apply filters; detect objects]
│       │   filterlib.py [define filters]
│       │   objectDetection.py [define object detection algorithms]
|       |   drawing.py [allow users to draw line etc. in a subthread]
│
│
└───subthread.py [run multithreading tasks]
│
└───realTimePlot.py [plot a real-time preview window of the magnetic field]
│
└───PS3Controller.py [enable joystick/controllers]

```
## Vision

### Camera

#### Important (If you are using firewire cameras)

![Camera error](https://github.com/atelier-ritz/CoilSystemPython/blob/master/documentation/camera_seting_error.png)

Important: The program freezes if you have a wrong camera setting.

Run the firewire camera manager in coriander:

```
coriander
```

Please select "Y8 mono 8pp, 30fps" for both cameras.

If you want to have a higher fps, you need to increase the buffersize when initializing the instance of Camera class in "callbacks.py".

#### Supported Cameras

Both USB camera (including the webcam on your laptop) and Firewire cameras are supported.

You can enable/disable the second camera by commenting out the following line in "callbacks.py": 

```
vision2 = Vision(index=2,type='firewire',guid=2672909588927744,buffersize=10)
```

Note: In this example program, all the filters and object detection algorithms apply to the 1st camera only.

If you want to use a USB camera instead, change it to 

```
vision2 = Vision(index=2,type='usb',guid=XXXX,buffersize=XX)
```

"guid" and "buffersize" can be anything because they will not be used in USB camera mode.

### Filters

Go to filterlib.py and define your filter. E.g. myfilter(param1,param2,...)

Then you can directly use it in the GUI by typing "myfilter(param1, param2,...)"

### Object Detection

![Object Detection](https://github.com/atelier-ritz/CoilSystemPython/blob/master/documentation/object_detection.png)

Go to GUI and add the name of your algorithm in algorithm combobox.

Go to vision.py __init__() function. Add a class attribute of the object to be detected. For example, self.gripper = Agent(), self.cargo = Agent()

Define your algorithm in objectDetection.py. Refer to algorithmA() as an Example.

Go to processObjectDetection() and pass your "agents" (instances of Agent Class) to the algorithm you just created.

The parameters (x, y, and orientation, if applicable) are updated at 60 Hz (defined in setupTimer() in callbacks.py).

These values can be accessed in the subthread.py by using self.vision.<nameOfYourAgent>.x, self.vision.<nameOfYourAgent>.y, and self.vision.<nameOfYourAgent>.orientation.

## New Features

In order to make the code neat and clean, I have three versions of the code in my repository.

master: basic modules only

with-Joystick: basic modules + joystick support

### Joystick

pygame needs to be installed to use the joystick module. To enable it, uncomment the following lines in callbacks.py.

```
from PS3Controller import DualShock
joystick = DualShock()
```

Although we only tested a PS3 Dualshock controller connected via USB, you should be able to work with any controller. (Try using "lsusb" command and "dmesg" command in the terminal to see if the controller is detected.) 

The available input for a PS3 controllers are 6 axis input and 16 button inputs.

Run the follwing command in the directory to test the controller input.

```
python3 PS3Controller.py
```

Refer to the sample code in *tianqiGripper()* in subThread.py.

### signal-generator

Added oscBetween() function that can be used in "subthread.py".

This function generates an oscillating value between a lowerbound and an upperbound.

The following oscillation waveforms are available: sin, saw, square, triangle.

Please refer to "exampleOscBetween" in "subthread.py" and the "oscBetween()" function defined in "mathfx.py".

### Preview Window

Added a window for real time preview of magnetic fields.

Also added some examples in subthread.py.

![Preview Window](https://github.com/atelier-ritz/CoilSystemPython/blob/master/documentation/previewwindow.gif)

### Drawing

In the old version, users can apply filters to the image, or highlight the object detected.

However, it didn't allow users to draw lines and circles directly on the frames captured.

This is necessary when, for example, users want to draw a vector pointing from the current robot position to the goal position.

Please refer to the "swimmerPathFollowing" example and "drawing" example in subThread.py.

### Recording

To take a snapshot, click the snapshot button in the GUI.

To record a video in a subThread, use the following commands):

```
self.vision.startRecording('YOUR_FILE_NAME.avi')
self.vision.stopRecording()
```

Please refer to the *drawing()* in subThread.py.

## Known Issues

1. The program always crashes on the first time after system startup.

2. If a game controller is used, segmentation fault occurs when exiting the program. 

3. Segmentation fault occurs when the user tries to record the videos of multiple cameras simultaneously. (When *self.vision.stopRecording()* is executed)
