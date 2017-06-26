#!/usr/bin/python2

import sys, time
from VdeRunner import VdeRunner

def parseCommandLine():
    import argparse

    parser = argparse.ArgumentParser(description='Run VDE-FSTP experiment.')
    parser.add_argument('--topo', required=True,
                        help='topology file')
    parser.add_argument('--duration', type=int, default=60,
                        help='duration of emulation')
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = parseCommandLine()
    vr = VdeRunner(args.topo)
    vr.runVDE()
    vr.printFSTP()
    vr.enableFSTP()
    time.sleep(args.duration)
    vr.stop()
