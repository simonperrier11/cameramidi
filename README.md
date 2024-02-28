# cameramidi
```cameramidi.py``` is a Python script that computes the mean, maximum and minimum values of the pixels' BGR and HSV values for each frame of a video capture in real-time, normalizes the results to the 0-127 range, then outputs these values as MIDI CC messages. This allows a video capture to be used in a creative way, such as controlling the parameters of a software synthesizer, etc.

## Requirements
You will need Python 3.X, as well as a video capture device connected to your computer. You might need to give camera access permission, depending on your operating system configuration.

If no MIDI out device is detected, a virtual one will be created by the script.

## Installation
Download the script, then install the dependencies using ```pip3``` or your preferred package manager.

## Usage
Open a terminal in the location of the script, then run :

```python3 cameramidi.py```

To quit the script, you must either terminate the terminal session, or simply type ```CTRL+C``` in your terminal.

By default, the script will analyze the feed of the first video capture device found (device index 0). It will print each computed value, with the corresponding MIDI-normalized value, in your terminal in real-time. The script will also output the MIDI CC messages as CC1-CC18. You can use the arguments in the section below to customize this behavior. 

## Values

Here is the order of the CC messages, and the value reprensented by each :
- CC1-3 : B mean, G mean, R mean
- CC4-5 : B max, B min
- CC6-7 : G max, G min
- CC8-9 : R max, R min
- CC10-12 : H mean, S mean, V mean
- CC13-14 : H max, H min
- CC15-16 : S max, S min
- CC17-18 : V max, V min

## Arguments

```--noprint``` : Use this argument if you want the script to not print values in your terminal.

```--deviceindex``` : Use this argument if you want to specify the capture device to use manually. For example, if you want to use your second camera instead of the first one (meaning, the capture device with index 1 instead of 0) :

```python3 cameramidi.py --deviceindex 1```

```--cc``` : Use this argument, followed by 18 CC numbers, to define which MIDI CC numbers to use for the values described in the section above. For example, if you want to use CC numbers 1-9 for BGR values, and then 20-28 for HSV values, instead of the default 1-18 range : 

```python3 cameramidi.py --cc 1 2 3 4 5 6 7 8 9 20 21 22 23 24 25 26 27 28```

## Known limitations
- The script currently only supports analysis of one capture device. However, if you wish to, you can start multiple instances of the script in different terminal windows, with different values for ```--deviceindex``` and ```--cc``` to allow the analysis of multiple capture devices separately.
- The script currently only outputs on one MIDI out device/port.
- The script currently only outputs on MIDI channel 1.

_Please note that this script was developped and tested using Python 3.12, on a M2 MacOS 14.3 system only._
