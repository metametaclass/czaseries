#!/usr/bin/env python3

import os
import argparse
import fileinput
import matplotlib.pyplot as plt
import json
import pandas as pd

def init_figure_settings(width=12, height=5):
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
    parser.add_argument("-p", "--plot", action="store_true", help="show plots")
    parser.add_argument("-s", "--stream", action="store_true", help="stream handling")
    parser.add_argument("files", nargs="*", help="files to process")
    return parser.parse_args()

def _process_file(fn, show_plot):
    print("process", fn)
    name_prefix,ext = os.path.splitext(fn)
    name_prefix = os.path.basename(name_prefix)

    #data = pd.read_csv(fn, sep=';', decimal='.', encoding='cp1251') #, parse_dates=['MSR_DT']
    with open(fn) as f:
        data = pd.read_json(f, lines=True)
        sensors = pd.crosstab(data.time, data.id, data.temperature_F, aggfunc=min)
        # sensors = pd.pivot_table(data, index=["time", "id"])
        # print(data)
        # print(sensors)
        print(data.keys())
        print(sensors.keys())

        if show_plot:
            fig = plt.figure()
            ax = fig.add_subplot(1,1,1)
            ax.plot(sensors)
            plt.savefig(name_prefix+"_sensors.png")


def _handle_stream(f):
    
    for line in f:
        line = line.rstrip()
        data = json.loads(line)
        print(data)
    # data = pd.read_json(f, lines=True)
    # print(data)


if __name__ == "__main__":
    args = _parse_arguments()
    if args.plots:
        init_figure_settings()
    if args.stream:
        _handle_stream(fileinput.input(args.files))
    else:
        for file in args.files:
            _process_file(file, args.plot)
    if args.plot:
        # plt.get_current_fig_manager().full_screen_toggle()
        plt.show()
