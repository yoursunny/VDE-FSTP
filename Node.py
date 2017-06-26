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
