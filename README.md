# VDE-Runner

<h3> Introduction </h3>

VDE-Runner helps you to setup a <a href="http://wiki.virtualsquare.org/wiki/index.php/VDE_Basic_Networking">VDE network</a> and enable the <a href="http://wiki.v2.cs.unibo.it/wiki/index.php/Fast_Spanning_Tree_Protocol">Fast Spanning Tree Protocol<a> on each switch. The topology information is read from a configuration file. A topology example is given out for format specification.

<h3> Simulate A Link Failure</h3>
To simulate a link failure, find out the <i>vde_plug</i> process id of the switch on either end and kill it. 

<h3> Capture and Analyze Traffic </h3>
To support traffic capture, <i>--enable-experimental</i> flag needs to be parsed when compiling VDE from source. The traffic of each switch is saved in /tmp/fifo+[switchName]. To anaylize it, either wireshark or tshark is useful. 

