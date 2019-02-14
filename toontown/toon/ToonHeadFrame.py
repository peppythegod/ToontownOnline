from direct.gui.DirectGui import *
from pandac.PandaModules import *
import ToonHead
from toontown.distributed import DelayDelete
from toontown.toonbase import ToontownGlobals


class ToonHeadFrame(DirectFrame):
    def __init__(self,
                 av,
                 color=ToontownGlobals.GlobalDialogColor,
                 g=DGG.getDefaultDialogGeom()):
        DirectFrame.__init__(
            self,
            relief=None,
            geom=g,
            geom_color=color,
            geom_scale=(1, 1, 0.5),
            pos=(0, 0, 0))
        self.initialiseoptions(ToonHeadFrame)
        self.av = av
        self.avKeep = DelayDelete.DelayDelete(av, 'ToonHeadFrame.avKeep')
        self.head = self.stateNodePath[0].attachNewNode('head', 20)
        self.head.setPosHprScale(
            -0.27000000000000002, 10.0, -0.089999999999999997, 180.0, 0.0, 0.0,
            0.20000000000000001, 0.20000000000000001, 0.20000000000000001)
        self.headModel = ToonHead.ToonHead()
        self.headModel.startBlink()
        self.headModel.setupHead(self.av.style, forGui=1)
        self.headModel.reparentTo(self.head)
        self.tag1Node = NametagFloat2d()
        self.tag1Node.setContents(Nametag.CSpeech | Nametag.CThought)
        self.av.nametag.addNametag(self.tag1Node)
        self.tag1 = self.attachNewNode(self.tag1Node.upcastToPandaNode())
        self.tag1.setPosHprScale(-0.16, 0, -0.089999999999999997, 0, 0, 0,
                                 0.055, 0.055, 0.055)
        self.tag2Node = NametagFloat2d()
        self.tag2Node.setContents(Nametag.CName)
        self.av.nametag.addNametag(self.tag2Node)
        self.tag2 = self.attachNewNode(self.tag2Node.upcastToPandaNode())
        self.tag2.setPosHprScale(-0.27000000000000002, 10.0, 0.16, 0, 0, 0,
                                 0.050000000000000003, 0.050000000000000003,
                                 0.050000000000000003)
        self.extraData = DirectLabel(
            parent=self,
            relief=None,
            pos=(0.0, 0.0, 0.059999999999999998),
            scale=1.0,
            text='',
            text0_fg=(0.29999999999999999, 0.20000000000000001, 1, 1),
            text_scale=(0.14000000000000001, 0.059999999999999998),
            text_pos=(0, -0.01))
        self.extraData.hide()

    def destroy(self):
        DirectFrame.destroy(self)
        self.headModel.delete()
        del self.headModel
        self.head.removeNode()
        del self.head
        if not self.av.isEmpty():
            self.av.nametag.removeNametag(self.tag1Node)
            self.av.nametag.removeNametag(self.tag2Node)

        self.tag1.removeNode()
        self.tag2.removeNode()
        del self.tag1
        del self.tag2
        del self.tag1Node
        del self.tag2Node
        del self.av
        if self.avKeep:
            self.avKeep.destroy()
            del self.avKeep

        self.extraData.removeNode()
        del self.extraData

    def removeAvKeep(self):
        if hasattr(self, 'avKeep') and self.avKeep:
            self.avKeep.destroy()
            self.avKeep = None
