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

# zoom frame at coordinates with zoom multiplier
def zoom_at(frame, zoom, coord=None):
    # get height and width
    height, width, _ = [ zoom * i for i in frame.shape ]
    
    # zoom from center or coordinates tuple (coord=(x, y))
    if coord is None: # zoom from center coordinates
        centerx, centery = width / 2, height / 2
    else: 
        centerx, centery = [ zoom * c for c in coord ]
    
    frame = cv.resize(frame, (0, 0), fx=zoom, fy=zoom)

    # crop frame
    frame = frame[ 
        int(round(centery - height / zoom * 0.5)) : int(round(centery + height / zoom * 0.5)),
        int(round(centerx - width / zoom * 0.5)) : int(round(centerx + width / zoom * 0.5)),
        : ]
    
    return frame

def main():
    # flag to disable printing
    noprint = False

    # set MIDI CC numbers (can be overwritten with args)
    # BGR
    midicc_bmean = 1
    midicc_gmean = 2
    midicc_rmean = 3
    midicc_bmax = 4
    midicc_bmin = 5
    midicc_gmax = 6
    midicc_gmin = 7
    midicc_rmax = 8
    midicc_rmin = 9

    # HSV
    midicc_hmean = 10
    midicc_smean = 11
    midicc_vmean = 12
    midicc_hmax = 13
    midicc_hmin = 14
    midicc_smax = 15
    midicc_smin = 16
    midicc_vmax = 17
    midicc_vmin = 18

    # MEDIAN
    midicc_bmedian = 19
    midicc_gmedian = 20
    midicc_rmedian = 21
    midicc_hmedian = 22
    midicc_smedian = 23
    midicc_vmedian = 24

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
                # BGR
                midicc_bmean = int(args[i + 1])
                midicc_gmean = int(args[i + 2])
                midicc_rmean = int(args[i + 3])
                midicc_bmax = int(args[i + 4])
                midicc_bmin = int(args[i + 5])
                midicc_gmax = int(args[i + 6])
                midicc_gmin = int(args[i + 7])
                midicc_rmax = int(args[i + 8])
                midicc_rmin = int(args[i + 9])

                # HSV
                midicc_hmean = int(args[i + 10])
                midicc_smean = int(args[i + 11])
                midicc_vmean = int(args[i + 12])
                midicc_hmax = int(args[i + 13])
                midicc_hmin = int(args[i + 14])
                midicc_smax = int(args[i + 15])
                midicc_smin = int(args[i + 16])
                midicc_vmax = int(args[i + 17])
                midicc_vmin = int(args[i + 18])
            except:
                raise ValueError("For manual CC # setting, use the --cc argument followed by the desired 18 CC numbers. See README file for order of CC numbers.")

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
                # get image size
                height, width, channels = frame.shape
                
                # apply zoom if needed 
                frame = zoom_at(frame, 3)

                # show frame
                cv.imshow('CAMERAMIDI', frame)
                cv.waitKey(1)

                # get BGR values for each pixel of frame
                b_values, g_values, r_values = cv.split(frame)

                # TODO: BGR median
                b_median = np.median(b_values)
                g_median = np.median(g_values)
                r_median = np.median(r_values)

                # compute BGR values for frame
                b_mean = np.mean(b_values)
                g_mean = np.mean(g_values)
                r_mean = np.mean(r_values)
                b_max = np.max(b_values)
                b_min = np.min(b_values)
                g_max = np.max(g_values)
                g_min = np.min(g_values)
                r_max = np.max(r_values)
                r_min = np.min(r_values)

                if not noprint:
                    print("BGR MEANS :", int(b_mean), int(g_mean), int(r_mean))
                    print("BGR MEDIANS :", int(b_median), int(g_median), int(r_median))
                    print("B MAX MIN :", int(b_max), int(b_min))
                    print("G MAX MIN :", int(g_max), int(g_min))
                    print("R MAX MIN :", int(r_max), int(r_min))

                # normalize BGR values to MIDI
                bmean_midi = normalize_to_midi(b_mean, 0, 255)
                gmean_midi = normalize_to_midi(g_mean, 0, 255)
                rmean_midi = normalize_to_midi(r_mean, 0, 255)
                bmax_midi = normalize_to_midi(b_max, 0, 255)
                bmin_midi = normalize_to_midi(b_min, 0, 255)
                gmax_midi = normalize_to_midi(g_max, 0, 255)
                gmin_midi = normalize_to_midi(g_min, 0, 255)
                rmax_midi = normalize_to_midi(r_max, 0, 255)
                rmin_midi = normalize_to_midi(r_min, 0, 255)

                bmedian_midi = normalize_to_midi(b_median, 0, 255)
                gmedian_midi = normalize_to_midi(g_median, 0, 255)
                rmedian_midi = normalize_to_midi(r_median, 0, 255)

                if not noprint: 
                    print("BGR MEANS MIDI :", bmean_midi, gmean_midi, rmean_midi)
                    print("BGR MEDIAN MIDI :", bmedian_midi, gmedian_midi, rmedian_midi)
                    print("B MAX MIN MIDI :", bmax_midi, bmin_midi)
                    print("G MAX MIN MIDI :", gmax_midi, gmin_midi)
                    print("R MAX MIN MIDI :", rmax_midi, rmin_midi)

                # convert frame to HSV color space, get hue/saturation/value arrays
                hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
                h_values, s_values, v_values = cv.split(hsv_frame)

                # TODO: HSV median
                h_median = np.median(h_values)
                s_median = np.median(s_values)
                v_median = np.median(v_values)

                # compite HSV values for frame
                h_mean = np.mean(h_values)
                s_mean = np.mean(s_values)
                v_mean = np.mean(v_values)
                h_max = np.max(h_values)
                h_min = np.min(h_values)
                s_max = np.max(s_values)
                s_min = np.min(s_values)
                v_max = np.max(v_values)
                v_min = np.min(v_values)


                if not noprint: 
                    print("HSV MEANS :", int(h_mean), int(s_mean), int(v_mean))
                    print("HSV MEANS :", int(h_median), int(s_median), int(v_median))
                    print("H MAX MIN :", int(h_max), int(h_min))
                    print("S MAX MIN :", int(s_max), int(s_min))
                    print("V MAX MIN :", int(v_max), int(v_min))

                # normalize HSV values to MIDI
                hmean_midi = normalize_to_midi(h_mean, 0, 179) # hue max is 179
                smean_midi = normalize_to_midi(s_mean, 0, 255)
                vmean_midi = normalize_to_midi(v_mean, 0, 255)
                hmax_midi = normalize_to_midi(h_max, 0, 179)
                hmin_midi = normalize_to_midi(h_min, 0, 179)
                smax_midi = normalize_to_midi(s_max, 0, 255)
                smin_midi = normalize_to_midi(s_min, 0, 255)
                vmax_midi = normalize_to_midi(v_max, 0, 255)
                vmin_midi = normalize_to_midi(v_min, 0, 255)

                hmedian_midi = normalize_to_midi(h_median, 0, 179)
                smedian_midi = normalize_to_midi(s_median, 0, 255)
                vmedian_midi = normalize_to_midi(v_median, 0, 255)

                if not noprint:
                    print("HSV MEANS MIDI :", hmean_midi, smean_midi, vmean_midi)
                    print("HSV MEDIANS MIDI :", hmedian_midi, smedian_midi, vmedian_midi)
                    print("H MAX MIN MIDI :", hmax_midi, hmin_midi)
                    print("S MAX MIN MIDI :", smax_midi, smin_midi)
                    print("V MAX MIN MIDI :", vmax_midi, vmin_midi)

                # build MIDI CC messages
                control_bmean = [0xB0, midicc_bmean, bmean_midi]
                control_gmean = [0xB0, midicc_gmean, gmean_midi]
                control_rmean = [0xB0, midicc_rmean, rmean_midi]
                control_bmax = [0xB0, midicc_bmax, bmax_midi]
                control_bmin = [0xB0, midicc_bmin, bmin_midi]
                control_gmax = [0xB0, midicc_gmax, gmax_midi]
                control_gmin = [0xB0, midicc_gmin, gmin_midi]
                control_rmax = [0xB0, midicc_rmax, rmax_midi]
                control_rmin = [0xB0, midicc_rmin, rmin_midi]

                control_hmean = [0xB0, midicc_hmean, hmean_midi]
                control_smean = [0xB0, midicc_smean, smean_midi]
                control_vmean = [0xB0, midicc_vmean, vmean_midi]
                control_hmax = [0xB0, midicc_hmax, hmax_midi]
                control_hmin = [0xB0, midicc_hmin, hmin_midi]
                control_smax = [0xB0, midicc_smax, smax_midi]
                control_smin = [0xB0, midicc_smin, smin_midi]
                control_vmax = [0xB0, midicc_vmax, vmax_midi]
                control_vmin = [0xB0, midicc_vmin, vmin_midi]

                control_bmedian = [0xB0, midicc_bmedian, bmedian_midi]
                control_gmedian = [0xB0, midicc_gmedian, gmedian_midi]
                control_rmedian = [0xB0, midicc_rmedian, rmedian_midi]
                control_hmedian = [0xB0, midicc_hmedian, hmedian_midi]
                control_smedian = [0xB0, midicc_smedian, smedian_midi]
                control_vmedian = [0xB0, midicc_vmedian, vmedian_midi]

                # send MIDI CC messages
                midi_out.send_message(control_bmean)
                midi_out.send_message(control_gmean)
                midi_out.send_message(control_rmean)
                midi_out.send_message(control_bmax)
                midi_out.send_message(control_bmin)
                midi_out.send_message(control_gmax)
                midi_out.send_message(control_gmin)
                midi_out.send_message(control_rmax)
                midi_out.send_message(control_rmin)

                midi_out.send_message(control_hmean)
                midi_out.send_message(control_smean)
                midi_out.send_message(control_vmean)
                midi_out.send_message(control_hmax)
                midi_out.send_message(control_hmin)
                midi_out.send_message(control_smax)
                midi_out.send_message(control_smin)
                midi_out.send_message(control_vmax)
                midi_out.send_message(control_vmin)

                midi_out.send_message(control_bmedian)
                midi_out.send_message(control_gmedian)
                midi_out.send_message(control_rmedian)
                midi_out.send_message(control_hmedian)
                midi_out.send_message(control_smedian)
                midi_out.send_message(control_vmedian)

                # mini sleep to not spam too much
                time.sleep(0.005)

if __name__ == '__main__':
    main()