from Node import Node

class Topo:
    def __init__(self):
        self.nodes = {}
        self.links = []
        self.rootNode = None
        self.rootPaths = []

    def addNode(self, name, isRoot=False):
        node = Node(name)
        self.nodes[name] = node
        if isRoot:
            self.rootNode = node

    def addLink(self, src, dst, isRootPath=False):
        srcNode = self.nodes[src]
        dstNode = self.nodes[dst]
        srcNode.addLink(dstNode)
        dstNode.addLink(srcNode)

        self.links.append((srcNode, dstNode))
        if isRootPath:
            self.rootPaths.append((srcNode, dstNode))
