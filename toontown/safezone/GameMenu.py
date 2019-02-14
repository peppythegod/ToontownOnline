from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *
from TrolleyConstants import *
from direct.gui.DirectGui import *
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals


class GameMenu(DirectFrame):
    def __init__(self, picnicFunction, menuType):
        self.picnicFunction = picnicFunction
        DirectFrame.__init__(
            self,
            pos=(0.0, 0.0, 0.84999999999999998),
            image_color=ToontownGlobals.GlobalDialogColor,
            image_scale=(1.8, 0.90000000000000002, 0.13),
            text='',
            text_scale=0.050000000000000003)
        self['image'] = DGG.getDefaultDialogGeom()
        if menuType == 1:
            self.title = DirectLabel(
                self,
                relief=None,
                text=TTLocalizer.PicnicTableMenuTutorial,
                text_pos=(0.0, -0.037999999999999999),
                text_fg=(1, 0, 0, 1),
                text_scale=0.089999999999999997,
                text_font=ToontownGlobals.getSignFont(),
                text_shadow=(1, 1, 1, 1))
        elif menuType == 2:
            self.title = DirectLabel(
                self,
                relief=None,
                text=TTLocalizer.PicnicTableMenuSelect,
                text_pos=(0.0, -0.040000000000000001),
                text_fg=(1, 0, 0, 1),
                text_scale=0.089999999999999997,
                text_font=ToontownGlobals.getSignFont())

        self.selectionButtons = loader.loadModel(
            'phase_6/models/golf/picnic_game_menu.bam')
        btn1 = self.selectionButtons.find('**/Btn1')
        btn2 = self.selectionButtons.find('**/Btn2')
        btn3 = self.selectionButtons.find('**/Btn3')
        self.ChineseCheckers = DirectButton(
            self,
            image=(btn1.find('**/checkersBtnUp'),
                   btn1.find('**/checkersBtnDn'),
                   btn1.find('**/checkersBtnHi'),
                   btn1.find('**/checkersBtnUp')),
            scale=0.35999999999999999,
            relief=0,
            pos=(0, 0, -0.69999999999999996),
            command=self.checkersSelected)
        self.Checkers = DirectButton(
            self,
            image=(btn2.find('**/regular_checkersBtnUp'),
                   btn2.find('**/regular_checkersBtnDn'),
                   btn2.find('**/regular_checkersBtnHi'),
                   btn2.find('**/regular_checkersBtnUp')),
            scale=0.35999999999999999,
            relief=0,
            pos=(0.80000000000000004, 0, -0.69999999999999996),
            command=self.regCheckersSelected)
        self.FindFour = DirectButton(
            self,
            image=(btn3.find('**/findfourBtnUp'),
                   btn3.find('**/findfourBtnDn'),
                   btn3.find('**/findfourBtnHi'),
                   btn3.find('**/findfourBtnUp')),
            scale=0.35999999999999999,
            relief=0,
            pos=(-0.80000000000000004, 0, -0.69999999999999996),
            command=self.findFourSelected)
        if not base.config.GetBool('want-chinese', 0):
            self.ChineseCheckers['command'] = self.doNothing
            self.ChineseCheckers.setColor(
                0.69999999999999996, 0.69999999999999996, 0.69999999999999996,
                0.69999999999999996)

        if not base.config.GetBool('want-checkers', 0):
            self.Checkers['command'] = self.doNothing
            self.Checkers.setColor(0.69999999999999996, 0.69999999999999996,
                                   0.69999999999999996, 0.69999999999999996)

        if not base.config.GetBool('want-findfour', 0):
            self.FindFour['command'] = self.doNothing
            self.FindFour.setColor(0.69999999999999996, 0.69999999999999996,
                                   0.69999999999999996, 0.69999999999999996)

        self.chineseText = OnscreenText(
            text='Chinese Checkers',
            pos=(0, 0.56000000000000005, -0.80000000000000004),
            scale=0.14999999999999999,
            fg=Vec4(1, 1, 1, 1),
            align=TextNode.ACenter,
            font=ToontownGlobals.getMinnieFont(),
            wordwrap=7,
            shadow=(0, 0, 0, 0.80000000000000004),
            shadowOffset=(-0.10000000000000001, -0.10000000000000001),
            mayChange=True)
        self.chineseText.setR(-8)
        self.checkersText = OnscreenText(
            text='Checkers',
            pos=(0.81000000000000005, -0.10000000000000001,
                 -0.80000000000000004),
            scale=0.14999999999999999,
            fg=Vec4(1, 1, 1, 1),
            align=TextNode.ACenter,
            font=ToontownGlobals.getMinnieFont(),
            wordwrap=7,
            shadow=(0, 0, 0, 0.80000000000000004),
            shadowOffset=(0.10000000000000001, -0.10000000000000001),
            mayChange=True)
        self.findFourText = OnscreenText(
            text='Find Four',
            pos=(-0.81000000000000005, -0.080000000000000002,
                 -0.80000000000000004),
            scale=0.14999999999999999,
            fg=Vec4(1, 1, 1, 1),
            align=TextNode.ACenter,
            font=ToontownGlobals.getMinnieFont(),
            wordwrap=8,
            shadow=(0, 0, 0, 0.80000000000000004),
            shadowOffset=(-0.10000000000000001, -0.10000000000000001),
            mayChange=True)
        self.findFourText.setR(-8)
        self.checkersText.setR(8)

    def delete(self):
        self.removeButtons()

    def removeButtons(self):
        self.ChineseCheckers.destroy()
        self.Checkers.destroy()
        self.FindFour.destroy()
        self.chineseText.destroy()
        self.checkersText.destroy()
        self.findFourText.destroy()
        DirectFrame.destroy(self)

    def checkersSelected(self):
        self.picnicFunction(1)
        self.picnicFunction = None

    def regCheckersSelected(self):
        self.picnicFunction(2)
        self.picnicFunction = None

    def findFourSelected(self):
        self.picnicFunction(3)
        self.picnicFunction = None

    def doNothing(self):
        pass
