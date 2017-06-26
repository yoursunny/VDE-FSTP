import sys
import time
from VdeRunner import VdeRunner

if len(sys.argv) < 2:
    print "Error : input configuration file"
else:
    vr = VdeRunner(sys.argv[1])
    vr.runVDE()
    vr.printFSTP()
    vr.enableFSTP()

    time.sleep(60*1)

    print "test done."

