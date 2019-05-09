from panda3d.core import BamFile, NodePath, StringStream, Vec4, TextNode
import DNANode, DNAError
import math

class DNASignBaseline(DNANode.DNANode):
    COMPONENT_CODE = 6

    def __init__(self):
        DNANode.DNANode.__init__(self, '')
        self.text = ''
        self.code = ''
        self.color = Vec4(0, 0, 0, 0)
        self.flags = ''
        self.indent = 0
        self.kern = 0
        self.wiggle = 0
        self.stumble = 0
        self.stomp = 0
        self.width = 0
        self.height = 0

    def makeFromDGI(self, dgi):
        DNANode.DNANode.makeFromDGI(self, dgi)
        self.text = dgi.getString()
        self.code = dgi.getString()
        self.color = Vec4(dgi.getUint8() / 255.,
                            dgi.getUint8() / 255.,
                            dgi.getUint8() / 255.,
                            dgi.getUint8() / 255.,)
        self.flags = dgi.getString()
        self.indent = dgi.getFloat32()
        self.kern = dgi.getFloat32()
        self.wiggle = dgi.getFloat32()
        self.stumble = dgi.getFloat32()
        self.stomp = dgi.getFloat32()
        self.width = dgi.getFloat32()
        self.height = dgi.getFloat32()

    def traverse(self, nodePath, dnaStorage):
        return
        """
        node = nodePath.attachNewNode('baseline', 0)
        node.setPosHpr(self.pos, self.hpr)
        node.setPos(node, 0, -0.1, 0)
        if self.data:
            bf = BamFile()
            ss = StringStream()
            ss.setData(self.data)
            bf.openRead(ss)
            signText = NodePath(bf.readNode())
            signText.reparentTo(node)
        node.flattenStrong()
        for child in self.children:
            child.traverse(nodePath, dnaStorage)
        """
        tn = TextNode("text")
        root = NodePath("signroot")
        x = 0
        for i in range(len(self.text)):
            tn.setText(self.text[0:i + 1])
            tn.setTextColor(self.color)
            
            font = dnaStorage.findFont(self.code)
            if not font:
                raise DNAError.DNAError('Font code %s not found.' %self.code)
                return
                
            tn.setFont(font)
            if i == 0 and self.flags.find('b') != -1:
                tn.setTextScale(1.5)
            else:
                tn.setTextScale(1.0)
            
            np = nodePath.attachNewNode(tn.generate())
            np.setScale(self.scale)
            np.setDepthWrite(0)
            if i & 1:
                np.setPos(x + self.stumble, 0, self.stomp)
                np.setR(-self.wiggle)
            else:
                np.setPos(x - self.stumble, 0, self.stomp)
                np.setR(self.wiggle)
                
            x += tn.getWidth() * np.getSx() + self.kern
            
        for child in root.getChildren():
            child.setX(child.getX() - x / 2.)
            
        if self.width != 0 and self.height != 0:
            for node in root.getChildren():
                a = node.getX() / (self.height / 2.)
                b = self.indent * math.pi / 180.
                theta = a + b
                d = node.getY()
                x = math.sin(theta) * (self.width / 2.)
                y = (math.cos(theta) - 1) * (self.height / 2.)
                radius = math.hypot(x, y)
                if radius != 0:
                    j = (radius + d) / radius
                    x *= j
                    y *= j
                node.setPos(x, 0, y)
                node.setR(node, theta * 180. / math.pi)
                
        _np = nodePath.attachNewNode(root.node())
        _np.setPosHpr(self.pos, self.hpr)
        _np.setDepthOffset(50)
        
        for child in self.children:
            child.traverse(_np, dnaStorage)
        
        _np.flattenStrong()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            