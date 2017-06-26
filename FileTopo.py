from Node import Node
from Topo import Topo

SECTION_NODES = '[nodes]'
SECTION_LINKS = '[links]'

class FileTopo(Topo):
    """Topology created from file."""

    @staticmethod
    def parseAttributes(tokens):
        return dict([ kv for kv in [ token.split('=') for token in tokens ] if len(kv) == 2 ])

    def __init__(self, filename):
        """Build topology from file.
           filename: Mini-NDN style topology file."""
        Topo.__init__(self)

        currentSection = None
        with open(filename) as f:
            for line in f:
                line = line.strip()
                if line == SECTION_NODES or line == SECTION_LINKS:
                    currentSection = line
                elif currentSection == SECTION_NODES:
                    nodeName, attributes = line.split(': ')
                    attributes = self.parseAttributes(attributes.split(' ')[1:])
                    self.addNode(nodeName, isRoot=attributes.get('root', False))
                elif currentSection == SECTION_LINKS:
                    tokens = line.split(' ')
                    node1, node2 = tokens[0].split(':')
                    attributes = self.parseAttributes(tokens[1:])
                    self.addLink(node1, node2, isRootPath=attributes.get('root', False))
