# VDE-FSTP

VDE-FSTP emulates [Fast Spanning Tree Protocol](http://wiki.v2.cs.unibo.it/wiki/index.php/Fast_Spanning_Tree_Protocol) using [Virtual Distributed Ethernet](http://wiki.virtualsquare.org/wiki/index.php/VDE_Basic_Networking).

## Installation

Ubuntu 14.04

`sudo apt-get install vde2 tshark`

## Usage

The topology information is read from a configuration file. An example is given in `topology-example.conf`.

To simulate a link failure, find the PID of `vde_plug` process and kill it.

Traffic trace is saved in `/tmp/myfifo-<switch-name>`, and can be analyzed with Wireshark.
`analyzer.py` collects statistics about how many packets are transmitted per second.
