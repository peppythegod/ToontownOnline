

from direct.showbase.ShowBaseGlobal import *
from toontown.toonbase.ToontownGlobals import *
from direct.gui.DirectGui import *
from toontown.toon import LaffMeter
from toontown.toonbase import TTLocalizer


class TreasureScorePanel(DirectFrame):

    def __init__(self):
        DirectFrame.__init__(
            self, relief=None, image_color=GlobalDialogColor, image_scale=(
                0.23999999999999999, 1.0, 0.23999999999999999), image_pos=(
                0.0, 0.10000000000000001, 0.0))
        self.score = 0
        self.scoreText = DirectLabel(
            self, relief=None, text=str(
                self.score), text_scale=0.080000000000000002, pos=(
                0.0, 0.0, -0.089999999999999997))
        self.nameText = DirectLabel(
            self,
            relief=None,
            text=TTLocalizer.DivingGameTreasuresRetrieved,
            text_scale=0.050000000000000003,
            text_pos=(
                0.0,
                0.059999999999999998),
            text_wordwrap=7.5,
            text_shadow=(
                1,
                1,
                1,
                1))
        self.show()

    def cleanup(self):
        del self.scoreText
        del self.nameText
        self.destroy()

    def incrScore(self):
        self.score += 1
        self.scoreText['text'] = str(self.score)

    def makeTransparent(self, alpha):
        self.setTransparency(1)
        self.setColorScale(1, 1, 1, alpha)
