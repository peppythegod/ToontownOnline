from panda3d.core import Vec4, Vec3, DecalEffect
import DNAGroup
import DNAError
import DNAUtil

class DNACornice(DNAGroup.DNAGroup):
    COMPONENT_CODE = 12

    def __init__(self, name):
        DNAGroup.DNAGroup.__init__(self, name)
        self.code = ''
        self.color = Vec4(1, 1, 1, 1)

    def setCode(self, code):
        self.code = code

    def getCode(self):
        return self.code

    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def makeFromDGI(self, dgi):
        DNAGroup.DNAGroup.makeFromDGI(self, dgi)
        self.code = DNAUtil.dgiExtractString8(dgi)
        self.color = DNAUtil.dgiExtractColor(dgi)

    def traverse(self, nodePath, dnaStorage):
        pParentXScale = nodePath.getParent().getScale().getX()
        parentZScale = nodePath.getScale().getZ()
        node = dnaStorage.findNode(self.code)
        if node is None:
            raise DNAError.DNAError('DNACornice code %d not found in DNAStorage' % self.code)
        nodePathA = nodePath.attachNewNode('cornice-internal', 0)
        node = node.find('**/*_d')
        np = node.copyTo(nodePathA, 0)
        np.setPosHprScale(
            Vec3(0, 0, 0),
            Vec3(0, 0, 0),
            Vec3(1, pParentXScale/parentZScale,
                      pParentXScale/parentZScale))
        np.setEffect(DecalEffect.make())
        np.flattenStrong()
        node = node.getParent().find('**/*_nd')
        np = node.copyTo(nodePathA, 1)
        np.setPosHprScale(
            Vec3(0, 0, 0),
            Vec3(0, 0, 0),
            Vec3(1, pParentXScale/parentZScale,
                      pParentXScale/parentZScale))
        np.flattenStrong()
        nodePathA.setPosHprScale(
            Vec3(0, 0, node.getScale().getZ()),
            Vec3(0, 0, 0),
            Vec3(1, 1, 1))
        nodePathA.setColor(self.color)
        nodePathA.flattenStrong()