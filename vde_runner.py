import subprocess
import sys

class VDE_Runner(object):
    def __init__(self, configureFileName):
        self.nodes = []
        self.links = []
        self.rootNode = ""

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
                self.nodes.append(eachLineList[0])
                if "root" in eachLineList[1]:
                    self.rootNode = eachLineList[0]

            if isReadingLinks:
                #eachLineList = eachLine.split[":"]
                #sourceNode = eachLineList[0].split["-"][0]
                #destinationNode = eachLineList[0].split["-"][1]
                eachLine = eachLine[:-1]
                s = eachLine.split("-")[0]
                d = eachLine.split("-")[1]
                self.links.append((s,d))

        print self.nodes
        print self.links

    def runVDE(self):
    	print "-----------------------Start to setup all switchs with links-------------------------"
        subprocess.call(["killall","vde_switch"])
        subprocess.call(["killall","vde_plug"])

        for eachNode in self.nodes:
            

            if eachNode == self.rootNode:
                subprocess.call(["vde_switch","-d","-s","/tmp/switch-"+eachNode, "-M", "/tmp/mgmt-"+eachNode, "--macaddr", "00:00:00:00:00:01"])
            else:
                subprocess.call(["vde_switch","-d","-s","/tmp/switch-"+eachNode, "-M", "/tmp/mgmt-"+eachNode])

            subprocess.call(["mkfifo","/tmp/fifo-"+eachNode])

            subprocess.call("echo 'plugin/add /usr/local/lib/vde2/plugins/pdump.so' |nc -U /tmp/mgmt-"+eachNode, shell=True)
            command_dump = "echo 'pdump/filename /tmp/myfifo-"+eachNode+"' | nc -U /tmp/mgmt-"+eachNode
            subprocess.call(command_dump, shell=True)
            subprocess.call("echo 'pdump/buffered 0' |nc -U /tmp/mgmt-"+eachNode, shell=True)
            subprocess.call("echo 'pdump/active 1' |nc -U /tmp/mgmt-"+eachNode, shell=True)

        for eachLink in self.links:
            s = eachLink[0]
            d = eachLink[1]

            command = "dpipe -d vde_plug /tmp/switch-"+s+" = vde_plug /tmp/switch-"+d
            subprocess.call(command, shell=True)

    def printFSTP(self):
    	print "-----------------------FSTP/PRINT for all switchs-------------------------"
        for eachNode in self.nodes:
            command = "echo 'fstp/print' | nc -U  /tmp/mgmt-"+eachNode
            subprocess.call(command, shell=True)


    def enableFSTP(self):
    	print "-----------------------Enable FSTP for all switchs-------------------------"
    	for eachNode in self.nodes:
            command = "echo 'fstp/setfstp 1' | nc -U  /tmp/mgmt-"+eachNode
            subprocess.call(command, shell=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Error : input configuration file"
    else:
        vde_runner = VDE_Runner(sys.argv[1])
        vde_runner.runVDE()
        vde_runner.printFSTP()
        vde_runner.enableFSTP()