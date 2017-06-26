import subprocess
import sys
import time

from Node import Node

class VdeRunner(object):
    def __init__(self, configureFileName):
        from FileTopo import FileTopo
        topo = FileTopo(configureFileName)

        self.nodes = topo.nodes.values()
        self.links = topo.links
        self.rootNode = topo.rootNode
        self.rootPaths = topo.rootPaths

        print self.nodes
        print self.links
        print self.rootPaths

    def findNode(self,name):
        for eachNode in self.nodes:
            if eachNode.name == name:
                return eachNode

    def runVDE(self):
        print "-----------------------Start to setup all switchs with links-------------------------"
        subprocess.call(["killall","vde_switch"])
        subprocess.call(["killall","vde_plug"])
        subprocess.call("rm /tmp/fifo*",shell=True)
        subprocess.call("rm /tmp/myfifo*",shell=True)
        subprocess.call("rm -r /tmp/switch*",shell=True)
        

        #add nodes in VDE
        for eachNode in self.nodes:

            if eachNode == self.rootNode:
                subprocess.call(["vde_switch","-d","-s","/tmp/switch-"+eachNode.name, "-M", "/tmp/mgmt-"+eachNode.name, "--macaddr", "00:00:00:00:00:01"])
            else:
                cmd = "vde_switch -d -s /tmp/switch-"+eachNode.name+" -M /tmp/mgmt-"+eachNode.name
                print "@@@@Command : "+cmd
                subprocess.call(cmd, shell=True)

                #subprocess.call(["mkfifo","/tmp/myfifo-"+eachNode.name])

                subprocess.call("echo 'plugin/add /usr/lib/vde2/plugins/pdump.so' |nc -U /tmp/mgmt-"+eachNode.name, shell=True)
                command_dump = "echo 'pdump/filename /tmp/myfifo-"+eachNode.name+"' | nc -U /tmp/mgmt-"+eachNode.name
                subprocess.call(command_dump, shell=True)
                #subprocess.call("echo 'pdump/buffered 0' |nc -U /tmp/mgmt-"+eachNode.name, shell=True)
                subprocess.call("echo 'pdump/active 1' |nc -U /tmp/mgmt-"+eachNode.name, shell=True)

        #add links in VDE
        for eachLink in self.links:
            sourceNode = eachLink[0]
            destNode = eachLink[1]

            command = "dpipe -d vde_plug /tmp/switch-"+sourceNode.name+" = vde_plug /tmp/switch-"+destNode.name
            subprocess.call(command, shell=True)

        #add bonus ports in VDE
        print "-----------------------Start to setup bonus ports-------------------------"
        for eachLink in self.rootPaths:
            sourceNode = eachLink[0]
            destNode = eachLink[1]

            #!!destNode is the node that has multple choices
            destPort = destNode.getPort(sourceNode)

            command = "echo 'fstp/bonus 0 "+str(destPort)+" 10000000' |nc -U /tmp/mgmt-"+destNode.name
            print command
            subprocess.call(command, shell=True)


    def printFSTP(self):
        print "-----------------------FSTP/PRINT for all switchs-------------------------"
        for eachNode in self.nodes:
            command = "echo 'fstp/print' | nc -U  /tmp/mgmt-"+eachNode.name
            subprocess.call(command, shell=True)


    def enableFSTP(self):
        print "-----------------------Enable FSTP for all switchs-------------------------"
        for eachNode in self.nodes:
            command = "echo 'fstp/setfstp 1' | nc -U  /tmp/mgmt-"+eachNode.name
            subprocess.call(command, shell=True)

    def addLink(self,sourceName, destName):
        command = "dpipe -d vde_plug /tmp/switch-"+str(sourceName)+" = vde_plug /tmp/switch-"+str(destName)
        subprocess.call(command, shell=True)


    def deleteLink(self,sourceName,destName):
        #the same order as input
        print "-----------------------DELETE a link in VDE--------------------------"
        out = subprocess.check_output("ps -ef |grep 'vde_plug /tmp/switch-"+str(destName)+"'",shell=True)
        outList = out.split('\n')[:-3]
        for eachProcess in outList:
            processInfo = eachProcess.split(' ')
            while '' in processInfo:
                processInfo.remove('')
            if '1' in processInfo:
                continue
            else:
                print "##the process is deleted: ", processInfo
                processId = processInfo[2]
                subprocess.call("kill "+processId,shell=True)
                break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Error : input configuration file"
    else:
        vr = VdeRunner(sys.argv[1])
        vr.runVDE()
        vr.printFSTP()
        vr.enableFSTP()
        time.sleep(30)
        vr.deleteLink(6,9)
        #vr.deleteLink(2, 3)
        #vr.deleteLink(4, 5)
        #vr.deleteLink(9, 12)
        time.sleep(30)
        vr.addLink(6,9)
        time.sleep(32)
        exit(0)

#from VdeRunner import Node, VdeRunner
#v = VdeRunner("4*3grid.conf")
