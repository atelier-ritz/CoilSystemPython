# CoilSystemPython

A Python3-based program for the coil system

## Usage

open terminal and cd to the target directory and run

```
python3 main.py
```

## Program Structure
To have a better understanding of the program, I would recommend you first have a look at "fieldManager.py".

After that, open the GUI and "callbacks.py" to follow the signal flow and event handler (pyqtSlot).

Go through "vision.py" to see how images are processed, and "objectDetection.py" to see how objects are detected and stored in instances of Agent class.

Read "subthread.py" in the end because it uses all the above-mentioned classes to do some complex stuff. E.g. Apply a rotational field with time-varying frequency/magnitude based on the position of the object detected.

```
main.py

callbacks.py
│
│   
└───syntax.py [highlight the keywords in GUI editor_vision]
|
└───fieldManager.py [send commands to s826; store XYZ field strength]
│   	|   s826.py [control s826 I/O]
│  
│
└───visoin.py [capture frames; apply filters; detect objects]
│       │   filterlib.py [define filters]
│       │   objectDetection.py [define object detection algorithms]
│
│
└───subthread.py [run multithreading tasks]

```
## To enable/disable 2nd camera; Switch to USB camera

Go to callbacks.py and comment out line 19 

```
vision2 = Vision(index=2,type='firewire',guid=2672909588927744,buffersize=10)
```
Note: In this example program, all the filters and object detection algorithms apply to the 1st camera only.

If you want to use a USB camera instead, change it to 

```
vision2 = Vision(index=2,type='usb',guid=XXXX,buffersize=XX)
```

"guid" and "buffersize" can be anything because they will not be used in USB camera mode.

## To create a new filter

Go to filterlib.py and define your filter. E.g. myfilter(param1,param2,...)

Then you can directly use it in the GUI by typing "myfilter(param1, param2,...)"

## To create a new object detection algorithm

Go to GUI and add the name of your algorithm in algorithm combobox.

Go to vision.py __init__() function. Add a class attribute of the object to be detected. For example, self.gripper = Agent(), self.cargo = Agent()

Define your algorithm in objectDetection.py. Refer to algorithmA() as an Example.

Go to processObjectDetection() and pass your "agents" (instances of Agent Class) to the algorithm you just created.

The parameters (x, y, and orientation, if applicable) are updated at 60 Hz (defined in setupTimer() in callbacks.py).

These values can be accessed in the subthread.py by using self.vision.gripper.x, self.vision.gripper.y, and self.vision.gripper.orientation.

## Dependencies

1. opencv

pip3 install opencv-python

pip3 install opencv-contrib-python

2. pyqt5

pip3 install pyqt5

3. pydc1394

https://github.com/jordens/pydc1394

4. s826Driver

Download "Linux Software Development Kit" and follow the instructions in Readme.

http://www.sensoray.com/products/826.htm

## GUI Designer

qt-designer is used.

sudo apt-get install qttools5-dev-tools

## USB camera or Firewire Camera

Can specify the camera in vision.py

## Screen Recording

 == I suggest using Ubuntu 16 rather than Ubuntu 17 for now ==

Simplescreenrecorder doesn't work property because Ubuntu 17.10 rolles back to GNOME (it used Unity in previous versions).

As a substitue, you can use green-recorder https://github.com/foss-project/green-recorder

You might have some trouble dealing with the .webm format of the video. :P

## Joystick Controller (Mar 15, 2018, under testing)

In the "With-Joystick" branch of this repository, we added a new module that enables the control of the magnetic field with a joystick controller. 

Although We only tested a PS3 Dualshock controller connected via USB, you should be able to work with any controller. (Try using "lsusb" command and "dmesg" command in the terminal to see if the controller is detected.) 

The available input for a PS3 controllers are 6 axis input (ranges from -1 to +1. L/R joyStick and L2/R2 buttons) and 16 on/off inputs (L1 R1 Start Select Square Circle Triangle Cross) Some changes are made to the code as follows:
```
Callbacks.py 
     * Added an instance of "DualShock" class
     * This instance is passed to the subthread module
     * In "update()" the input from the controller is updated. This means the input is updated at 60 Hz.
Subthread.py
     * In a subthread, the input can be obtained via functions defined in "PS3Controller.py". See the comments in the file.
```

## oscBetween function (Mar 22, 2018)

Added oscBetween() function that can be used in "subthread.py".

This function generates an oscillating value between a lowerbound and an upperbound.

The following oscillation waveforms are available: sin, saw, sqaure, triangle.

Please refer to "exampleOscBetween" in "subthread.py" and the "oscBetween()" function defined in "mathfx.py".

## added real-time field preview window (Mar 23, 2018)

Added a window for real time filed preview.

Avaialble in the "With-PlotWindow" branch.

Also added some examples in subthread.py.
