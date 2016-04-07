import subprocess
import sys
import time

class Node(object):
    def __init__(self, name):
        self.name = name
        self.nPorts = 0
        self.portNode = {}

    def addLink(self, node):
        self.nPorts += 1
        self.portNode[self.nPorts] = node

    def getPort(self, node):
        for i in range(1, self.nPorts+1):
            if self.portNode[i] == node:
                return i

    def __str__(self):
        return self.name

class VDE_Runner(object):
    def __init__(self, configureFileName):
        self.nodes = []
        self.links = []
        self.rootNode = object()

        #Node,Port
        self.rootPaths = []

        #construct the topology via conf file     
        configureFile = open(configureFileName,"r")
        for eachLine in configureFile:
            print eachLine
            if len(eachLine) < 2:
                break

            if "nodes" in  eachLine:
                isReadingNodes = True
                isReadingLinks = False
                continue
            elif "links" in eachLine:
                isReadingLinks = True
                isReadingNodes = False
                continue

            if isReadingNodes:
                eachLineList = eachLine.split(":")
                newNode = Node(eachLineList[0])
                self.nodes.append(newNode)
                if "root" in eachLineList[1]:
                    self.rootNode = newNode

            if isReadingLinks:
                
                #sourceNode = eachLineList[0].split["-"][0]
                #destinationNode = eachLineList[0].split["-"][1]
                eachLine = eachLine[:-1]
                eachLineList = eachLine.split(":")

                firtPart = eachLineList[0]
                sourceNode = self.findNode(firtPart.split("-")[0])
                destNode = self.findNode(firtPart.split("-")[1])
                self.links.append((sourceNode,destNode))

                sourceNode.addLink(destNode)
                destNode.addLink(sourceNode)

                if "root" in eachLineList[1]:
                    self.rootPaths.append((sourceNode,destNode))

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
                subprocess.call(["vde_switch","-d","-s","/tmp/switch-"+eachNode.name, "-M", "/tmp/mgmt-"+eachNode.name])

            #subprocess.call(["mkfifo","/tmp/myfifo-"+eachNode.name])

            subprocess.call("echo 'plugin/add /usr/local/lib/vde2/plugins/pdump.so' |nc -U /tmp/mgmt-"+eachNode.name, shell=True)
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
        command = "dpipe -d vde_plug /tmp/switch-"+str(sourceName)+" = vde_plug /tmp/switch-"+(destName)
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
        vde_runner = VDE_Runner(sys.argv[1])
        vde_runner.runVDE()
        vde_runner.printFSTP()
        vde_runner.enableFSTP()
        time.sleep(30)
        #vde_runner.deleteLink(6,9)
        vde_runner.deleteLink(2, 3)
        time.sleep(32)
        exit(0)

#from vde_runner import Node, VDE_Runner
#v = VDE_Runner("4*3grid.conf")