# VDE-Runner

<h3> Introduction </h3>

VDE-Runner helps you to setup a <a href="http://wiki.virtualsquare.org/wiki/index.php/VDE_Basic_Networking">VDE network</a> and enable the <a href="http://wiki.v2.cs.unibo.it/wiki/index.php/Fast_Spanning_Tree_Protocol">Fast Spanning Tree Protocol<a> on each switch. The topology information is read from a configuration file. An example is given out for the right format.

<h3> Link Failure</h3>
To generate a link failure, find out the <i>vde_plug</i> process id of the either switch and kill it. 

<h3> Capture an Analyze Traffic </h3>
To support traffic capture, <i>--enable-experimental</i> flag is needed when compile VDE from source. The taffic of each switch is saved in /tmp/fifo+<swithName>. To anaylize it, each wireshark or tshark is needed. 

