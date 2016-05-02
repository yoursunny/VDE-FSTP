import sys
import time
from vde_runner import VDE_Runner

if len(sys.argv) < 2:
    print "Error : input configuration file"
else:
    vde_runner = VDE_Runner(sys.argv[1])
    vde_runner.runVDE()
    vde_runner.printFSTP()
    vde_runner.enableFSTP()

    time.sleep(60*21)

    print "test done."

