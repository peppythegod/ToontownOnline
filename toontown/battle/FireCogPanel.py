from toontown.toonbase.ToontownBattleGlobals import *
from toontown.toonbase import ToontownGlobals
from direct.fsm import StateData
from direct.directnotify import DirectNotifyGlobal
from toontown.battle import BattleBase
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer


class FireCogPanel(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('ChooseAvatarPanel')

    def __init__(self, doneEvent):
        self.notify.debug('Init choose panel...')
        StateData.StateData.__init__(self, doneEvent)
        self.numAvatars = 0
        self.chosenAvatar = 0
        self.toon = 0
        self.loaded = 0

    def load(self):
        gui = loader.loadModel('phase_3.5/models/gui/battle_gui')
        self.frame = DirectFrame(
            relief=None,
            image=gui.find('**/BtlPick_TAB'),
            image_color=Vec4(1, 0.20000000000000001, 0.20000000000000001, 1))
        self.frame.hide()
        self.statusFrame = DirectFrame(
            parent=self.frame,
            relief=None,
            image=gui.find('**/ToonBtl_Status_BG'),
            image_color=Vec4(0.5, 0.90000000000000002, 0.5, 1),
            pos=(0.61099999999999999, 0, 0))
        self.textFrame = DirectFrame(
            parent=self.frame,
            relief=None,
            image=gui.find('**/PckMn_Select_Tab'),
            image_color=Vec4(1, 1, 0, 1),
            image_scale=(1.0, 1.0, 2.0),
            text='',
            text_fg=Vec4(0, 0, 0, 1),
            text_pos=(0, 0.02, 0),
            text_scale=TTLocalizer.FCPtextFrame,
            pos=(-0.012999999999999999, 0, 0.012999999999999999))
        self.textFrame[
            'text'] = TTLocalizer.FireCogTitle % localAvatar.getPinkSlips()
        self.avatarButtons = []
        for i in range(4):
            button = DirectButton(
                parent=self.frame,
                relief=None,
                text='',
                text_fg=Vec4(0, 0, 0, 1),
                text_scale=0.067000000000000004,
                text_pos=(0, -0.014999999999999999, 0),
                textMayChange=1,
                image_scale=(1.0, 1.0, 1.0),
                image=(gui.find('**/PckMn_Arrow_Up'),
                       gui.find('**/PckMn_Arrow_Dn'),
                       gui.find('**/PckMn_Arrow_Rlvr')),
                command=self._FireCogPanel__handleAvatar,
                extraArgs=[i])
            button.setScale(1, 1, 1)
            button.setPos(0, 0, 0.20000000000000001)
            self.avatarButtons.append(button)

        self.backButton = DirectButton(
            parent=self.frame,
            relief=None,
            image=(gui.find('**/PckMn_BackBtn'),
                   gui.find('**/PckMn_BackBtn_Dn'),
                   gui.find('**/PckMn_BackBtn_Rlvr')),
            pos=(-0.64700000000000002, 0, 0.0060000000000000001),
            scale=1.05,
            text=TTLocalizer.TownBattleChooseAvatarBack,
            text_scale=0.050000000000000003,
            text_pos=(0.01, -0.012),
            text_fg=Vec4(0, 0, 0.80000000000000004, 1),
            command=self._FireCogPanel__handleBack)
        gui.removeNode()
        self.loaded = 1

    def unload(self):
        if self.loaded:
            self.frame.destroy()
            del self.frame
            del self.statusFrame
            del self.textFrame
            del self.avatarButtons
            del self.backButton

        self.loaded = 0

    def enter(self,
              numAvatars,
              localNum=None,
              luredIndices=None,
              trappedIndices=None,
              track=None,
              fireCosts=None):
        if not self.loaded:
            self.load()

        self.frame.show()
        invalidTargets = []
        if not self.toon:
            if len(luredIndices) > 0:
                if track == BattleBase.TRAP or track == BattleBase.LURE:
                    invalidTargets += luredIndices

            if len(trappedIndices) > 0:
                if track == BattleBase.TRAP:
                    invalidTargets += trappedIndices

        self._FireCogPanel__placeButtons(numAvatars, invalidTargets, localNum,
                                         fireCosts)

    def exit(self):
        self.frame.hide()

    def _FireCogPanel__handleBack(self):
        doneStatus = {'mode': 'Back'}
        messenger.send(self.doneEvent, [doneStatus])

    def _FireCogPanel__handleAvatar(self, avatar):
        doneStatus = {'mode': 'Avatar', 'avatar': avatar}
        messenger.send(self.doneEvent, [doneStatus])

    def adjustCogs(self, numAvatars, luredIndices, trappedIndices, track):
        invalidTargets = []
        if len(luredIndices) > 0:
            if track == BattleBase.TRAP or track == BattleBase.LURE:
                invalidTargets += luredIndices

        if len(trappedIndices) > 0:
            if track == BattleBase.TRAP:
                invalidTargets += trappedIndices

        self._FireCogPanel__placeButtons(numAvatars, invalidTargets, None)

    def adjustToons(self, numToons, localNum):
        self._FireCogPanel__placeButtons(numToons, [], localNum)

    def _FireCogPanel__placeButtons(self, numAvatars, invalidTargets, localNum,
                                    fireCosts):
        canfire = 0
        for i in range(4):
            if numAvatars > i and i not in invalidTargets and i != localNum:
                self.avatarButtons[i].show()
                self.avatarButtons[i]['text'] = ''
                if fireCosts[i] <= localAvatar.getPinkSlips():
                    self.avatarButtons[i]['state'] = DGG.NORMAL
                    self.avatarButtons[i]['text_fg'] = (0, 0, 0, 1)
                    canfire = 1
                else:
                    self.avatarButtons[i]['state'] = DGG.DISABLED
                    self.avatarButtons[i]['text_fg'] = (1.0, 0, 0, 1)
            fireCosts[i] <= localAvatar.getPinkSlips()
            self.avatarButtons[i].hide()

        if canfire:
            self.textFrame[
                'text'] = TTLocalizer.FireCogTitle % localAvatar.getPinkSlips(
                )
        else:
            self.textFrame[
                'text'] = TTLocalizer.FireCogLowTitle % localAvatar.getPinkSlips(
                )
        if numAvatars == 1:
            self.avatarButtons[0].setX(0)
        elif numAvatars == 2:
            self.avatarButtons[0].setX(0.20000000000000001)
            self.avatarButtons[1].setX(-0.20000000000000001)
        elif numAvatars == 3:
            self.avatarButtons[0].setX(0.40000000000000002)
            self.avatarButtons[1].setX(0.0)
            self.avatarButtons[2].setX(-0.40000000000000002)
        elif numAvatars == 4:
            self.avatarButtons[0].setX(0.59999999999999998)
            self.avatarButtons[1].setX(0.20000000000000001)
            self.avatarButtons[2].setX(-0.20000000000000001)
            self.avatarButtons[3].setX(-0.59999999999999998)
        else:
            self.notify.error('Invalid number of avatars: %s' % numAvatars)
