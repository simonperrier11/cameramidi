# author : Simon Perrier
# description : Calculate mean of RGB and HSV values from a video capture
# in real time, normalize means to MIDI, output to MIDI out

import sys
import numpy as np
import cv2 as cv
import time
import rtmidi

# normalize x to MIDI 0-127 range
# formula : normalized_x = (b - a) * ((x - min(x)) / (max(x) - min(x))) + a
def normalize_to_midi(val, minval, maxval):
    return int(127 * ((val - minval) / (maxval - minval)))

def main():
    # flag to disable printing
    noprint = False

    # set MIDI CC numbers (can be overwritten with args)
    midicc_1 = 1
    midicc_2 = 2
    midicc_3 = 3
    midicc_4 = 4
    midicc_5 = 5
    midicc_6 = 6

    # set video capture device index (0 is first one listed)
    device_index = 0

    # parse script arguments, set flags and values accordingly
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg.lower() == "--noprint":
            noprint = True

        if arg.lower() == "--deviceindex":
            try:
                device_index = int(args[i + 1])
            except:
                raise ValueError("For manual capture device index setting, use the --deviceindex argument followed by the desired capture device index.")

        if arg.lower() == "--cc":
            try:
                midicc_1 = int(args[i + 1])
                midicc_2 = int(args[i + 2])
                midicc_3 = int(args[i + 3])
                midicc_4 = int(args[i + 4])
                midicc_5 = int(args[i + 5])
                midicc_6 = int(args[i + 6])
            except:
                raise ValueError("For manual CC # setting, use the --cc argument followed by the desired 6 CC numbers.")

    # get MIDI out ports, use first one found
    midi_out = rtmidi.MidiOut()
    available_ports = midi_out.get_ports()
    # print(available_ports)
    
    if available_ports:
        midi_out.open_port(0)
    else:
        midi_out.open_virtual_port("cameramidi Virtual MIDI Port")

    with midi_out:
        capture = cv.VideoCapture(device_index)

        while True:
            # read capture to get frame
            retval, frame = capture.read()

            if retval:
                # get BGR values for each pixel of frame
                # the 3rd dimension of the frame is the color channel
                b_values, g_values, r_values = cv.split(frame)

                # get BGR values mean for frame
                b_mean = np.mean(b_values)
                g_mean = np.mean(g_values)
                r_mean = np.mean(r_values)

                if not noprint: print("BGR MEAN :", int(b_mean), int(g_mean), int(r_mean))

                # normalize BGR means to MIDI
                b_midi = normalize_to_midi(b_mean, 0, 255)
                g_midi = normalize_to_midi(g_mean, 0, 255)
                r_midi = normalize_to_midi(r_mean, 0, 255)

                if not noprint: print("BGR MIDI :", b_midi, g_midi, r_midi)

                # convert frame to HSV color space, get hue/saturation/value arrays
                hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
                h_values, s_values, v_values = cv.split(hsv_frame)

                # get HSV values means for frame
                h_mean = np.mean(h_values)
                s_mean = np.mean(s_values)
                v_mean = np.mean(v_values)

                if not noprint: print("HSV MEAN :", int(h_mean), int(s_mean), int(v_mean))

                # normalize HSV means to MIDI
                h_midi = normalize_to_midi(h_mean, 0, 179) # hue max is 179
                s_midi = normalize_to_midi(s_mean, 0, 255)
                v_midi = normalize_to_midi(v_mean, 0, 255)

                if not noprint: print("HSV MIDI :", h_midi, s_midi, v_midi)

                # build MIDI CC messages
                control_r = [0xB0, midicc_1, b_midi]
                control_g = [0xB0, midicc_2, g_midi]
                control_b = [0xB0, midicc_3, r_midi]
                control_h = [0xB0, midicc_4, h_midi]
                control_s = [0xB0, midicc_5, s_midi]
                control_v = [0xB0, midicc_6, v_midi]

                # send MIDI CC messages
                midi_out.send_message(control_b)
                midi_out.send_message(control_g)
                midi_out.send_message(control_r)
                midi_out.send_message(control_h)
                midi_out.send_message(control_s)
                midi_out.send_message(control_v)

                # mini sleep to not spam too much
                time.sleep(0.005)

if __name__ == '__main__':
    main()