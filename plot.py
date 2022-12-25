#!/usr/bin/env python3

import os
import argparse
import fileinput
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import json
import pandas as pd

def init_figure_settings(width=24, height=10):
    plt.rcParams["figure.figsize"] = [width, height]
    plt.rcParams['font.size'] = 14
    plt.rcParams['image.cmap'] = 'plasma'
    plt.rcParams['axes.linewidth'] = 2
    # Set the default colour cycle (in case someone changes it...)
    from cycler import cycler
    cols = plt.get_cmap('tab10').colors
    plt.rcParams['axes.prop_cycle'] = cycler(color=cols)


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gui", action="store_true", help="show gui plots")
    parser.add_argument("-s", "--stream", action="store_true", help="stream handling")
    parser.add_argument("files", nargs="*", help="files to process")
    return parser.parse_args()

def _process_file(fn):
    print("process", fn)
    name_prefix,ext = os.path.splitext(fn)
    name_prefix = os.path.basename(name_prefix)

    #data = pd.read_csv(fn, sep=';', decimal='.', encoding='cp1251') #, parse_dates=['MSR_DT']
    with open(fn) as f:
        data = pd.read_json(f, lines=True, convert_dates=["time"])
        # print(data.shape)
        # print(data.dtypes)
        # print(data.keys())
        sensors_tf = pd.crosstab(data.time, data.id, data.temperature_F, aggfunc=min)
        sensors_tc = sensors_tf.copy()
        sensors_h = pd.crosstab(data.time, data.id, data.humidity, aggfunc=min)

        #print(data.keys())
        # print(sensors_tc.keys())
        #print(sensors_tc)

        counter = 1
        for k in sensors_tc.keys():
            temperature = (sensors_tc[k] - 32)*5/9
            humidity = sensors_h[k]
            time = sensors_tc.index
            print(time.dtype)
            fig = plt.figure()
            ax = fig.add_subplot(2,1,1)
            ax.set_title(f"temperature {k}")
            ax.plot(time, temperature, "r-")
            # ax.xaxis.set_major_locator(dates.HourLocator())

            ax = fig.add_subplot(2,1,2)
            ax.set_title(f"humidity {k}")
            ax.plot(time, humidity, "g-")
            # ax.xaxis.set_major_locator(dates.HourLocator())

            plt.savefig(name_prefix+f"_sensor_f{k}.png")


        # fig = plt.figure()
        # ax = fig.add_subplot(2,1,1)
        # sensors_tc.plot(ax=ax)
        # #ax.plot(sensors_tc.time, sensors_tc)
        # ax = fig.add_subplot(2,1,2)
        # sensors_h.plot(ax=ax)
        # #ax.plot(sensors_h.time, sensors_h)
        # plt.savefig(name_prefix+"_sensors.png")


def _handle_stream(f):
    
    for line in f:
        line = line.rstrip()
        data = json.loads(line)
        print(data)
    # data = pd.read_json(f, lines=True)
    # print(data)


if __name__ == "__main__":
    args = _parse_arguments()
    init_figure_settings()
    if args.stream:
        _handle_stream(fileinput.input(args.files))
    else:
        for file in args.files:
            _process_file(file)
    if args.gui:
        # plt.get_current_fig_manager().full_screen_toggle()
        plt.show()
