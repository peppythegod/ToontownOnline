from pandac.PandaModules import *
import ShtikerPage
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toon import NPCToons
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer


class TIPPage(ShtikerPage.ShtikerPage):
    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.textRolloverColor = Vec4(1, 1, 0, 1)
        self.textDownColor = Vec4(0.5, 0.90000000000000002, 1, 1)
        self.textDisabledColor = Vec4(0.40000000000000002, 0.80000000000000004,
                                      0.40000000000000002, 1)

    def load(self):
        self.title = DirectLabel(
            parent=self,
            relief=None,
            text=TTLocalizer.TIPPageTitle,
            text_scale=0.12,
            textMayChange=0,
            pos=(0, 0, 0.59999999999999998))

    def unload(self):
        del self.title
        loader.unloadModel('phase_3.5/models/gui/stickerbook_gui')
        ShtikerPage.ShtikerPage.unload(self)

    def updatePage(self):
        pass

    def enter(self):
        self.updatePage()
        ShtikerPage.ShtikerPage.enter(self)

    def exit(self):
        ShtikerPage.ShtikerPage.exit(self)
