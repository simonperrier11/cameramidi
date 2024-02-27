# cameramidi
```cameramidi.py``` is a Python script that computes the means of the BGR and HSV values for each frame of a video capture in real-time, then outputs these values as MIDI CC messages. This allows a video capture to be used in a creative way, such as controlling the parameters of a software synthesizer, etc.

## Requirements
You will need Python 3.X, as well as a video capture device connected to your computer. 

If no MIDI out device is detected, a virtual one will be created by the script.

_Please note that this script was developped and tested using Python 3.12, on a M2 MacOS 14.3 system only._

## Installation
Download the script, then install the dependencies using ```pip3``` or your preferred package manager.

## Usage
Open a terminal in the location of the script, then run :

```python3 cameramidi.py```

You might need to give camera access permission, depending on your operating system configuration.

To quit the script, simply type ```CTRL+C``` in your terminal.

By default, the script will print each value (means, MIDI values) in your terminal in real-time. The script will also output the MIDI CC messages as CC1, CC2, CC3, CC4, CC5 and CC6.

## Arguments

```--noprint``` : Use this argument if you want the script to not print values in your terminal.

```--cc``` : Use this argument, followed by 6 numbers, to define which MIDI CC numbers to use. Example, if you want to use CC numbers 20-25 instead of 1-6 : 

```python3 cameramidi.py --cc 20 21 22 23 24 25```

## Known limitations
- The script currently only supports one capture device.
- The script currently only outputs on MIDI channel 1.
