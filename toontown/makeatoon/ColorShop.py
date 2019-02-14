from pandac.PandaModules import *
from toontown.toon import ToonDNA
from direct.fsm import StateData
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from MakeAToonGlobals import *
from toontown.toonbase import TTLocalizer
import ShuffleButton
import random
from direct.directnotify import DirectNotifyGlobal


class ColorShop(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('ColorShop')

    def __init__(self, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        self.toon = None
        self.colorAll = 1

    def getGenderColorList(self, dna):
        if self.dna.getGender() == 'm':
            return ToonDNA.defaultBoyColorList
        else:
            return ToonDNA.defaultGirlColorList

    def enter(self, toon, shopsVisited=[]):
        base.disableMouse()
        self.toon = toon
        self.dna = toon.getStyle()
        colorList = self.getGenderColorList(self.dna)

        try:
            self.headChoice = colorList.index(self.dna.headColor)
            self.armChoice = colorList.index(self.dna.armColor)
            self.legChoice = colorList.index(self.dna.legColor)
        except BaseException:
            self.headChoice = random.choice(colorList)
            self.armChoice = self.headChoice
            self.legChoice = self.headChoice
            self._ColorShop__swapHeadColor(0)
            self._ColorShop__swapArmColor(0)
            self._ColorShop__swapLegColor(0)

        self.startColor = 0
        self.acceptOnce('last', self._ColorShop__handleBackward)
        self.acceptOnce('next', self._ColorShop__handleForward)
        choicePool = [
            self.getGenderColorList(self.dna),
            self.getGenderColorList(self.dna),
            self.getGenderColorList(self.dna)
        ]
        self.shuffleButton.setChoicePool(choicePool)
        self.accept(self.shuffleFetchMsg, self.changeColor)
        self.acceptOnce('MAT-newToonCreated', self.shuffleButton.cleanHistory)

    def showButtons(self):
        self.parentFrame.show()

    def hideButtons(self):
        self.parentFrame.hide()

    def exit(self):
        self.ignore('last')
        self.ignore('next')
        self.ignore('enter')
        self.ignore(self.shuffleFetchMsg)

        try:
            del self.toon
        except BaseException:
            print 'ColorShop: toon not found'

        self.hideButtons()

    def load(self):
        self.gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui')
        guiRArrowUp = self.gui.find('**/tt_t_gui_mat_arrowUp')
        guiRArrowRollover = self.gui.find('**/tt_t_gui_mat_arrowUp')
        guiRArrowDown = self.gui.find('**/tt_t_gui_mat_arrowDown')
        guiRArrowDisabled = self.gui.find('**/tt_t_gui_mat_arrowDisabled')
        shuffleFrame = self.gui.find('**/tt_t_gui_mat_shuffleFrame')
        shuffleArrowUp = self.gui.find('**/tt_t_gui_mat_shuffleArrowUp')
        shuffleArrowDown = self.gui.find('**/tt_t_gui_mat_shuffleArrowDown')
        shuffleArrowRollover = self.gui.find('**/tt_t_gui_mat_shuffleArrowUp')
        shuffleArrowDisabled = self.gui.find(
            '**/tt_t_gui_mat_shuffleArrowDisabled')
        self.parentFrame = DirectFrame(
            relief=DGG.RAISED,
            pos=(0.97999999999999998, 0, 0.41599999999999998),
            frameColor=(1, 0, 0, 0))
        self.toonFrame = DirectFrame(
            parent=self.parentFrame,
            image=shuffleFrame,
            image_scale=halfButtonInvertScale,
            relief=None,
            pos=(0, 0, -0.072999999999999995),
            hpr=(0, 0, 0),
            scale=1.3,
            frameColor=(1, 1, 1, 1),
            text=TTLocalizer.ColorShopToon,
            text_scale=TTLocalizer.CStoonFrame,
            text_pos=(-0.001, -0.014999999999999999),
            text_fg=(1, 1, 1, 1))
        self.allLButton = DirectButton(
            parent=self.toonFrame,
            relief=None,
            image=(shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover,
                   shuffleArrowDisabled),
            image_scale=halfButtonScale,
            image1_scale=halfButtonHoverScale,
            image2_scale=halfButtonHoverScale,
            pos=(-0.20000000000000001, 0, 0),
            command=self._ColorShop__swapAllColor,
            extraArgs=[-1])
        self.allRButton = DirectButton(
            parent=self.toonFrame,
            relief=None,
            image=(shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover,
                   shuffleArrowDisabled),
            image_scale=halfButtonInvertScale,
            image1_scale=halfButtonInvertHoverScale,
            image2_scale=halfButtonInvertHoverScale,
            pos=(0.20000000000000001, 0, 0),
            command=self._ColorShop__swapAllColor,
            extraArgs=[1])
        self.headFrame = DirectFrame(
            parent=self.parentFrame,
            image=shuffleFrame,
            image_scale=halfButtonInvertScale,
            relief=None,
            pos=(0, 0, -0.29999999999999999),
            hpr=(0, 0, 2),
            scale=0.90000000000000002,
            frameColor=(1, 1, 1, 1),
            text=TTLocalizer.ColorShopHead,
            text_scale=0.0625,
            text_pos=(-0.001, -0.014999999999999999),
            text_fg=(1, 1, 1, 1))
        self.headLButton = DirectButton(
            parent=self.headFrame,
            relief=None,
            image=(shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover,
                   shuffleArrowDisabled),
            image_scale=halfButtonScale,
            image1_scale=halfButtonHoverScale,
            image2_scale=halfButtonHoverScale,
            pos=(-0.20000000000000001, 0, 0),
            command=self._ColorShop__swapHeadColor,
            extraArgs=[-1])
        self.headRButton = DirectButton(
            parent=self.headFrame,
            relief=None,
            image=(shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover,
                   shuffleArrowDisabled),
            image_scale=halfButtonInvertScale,
            image1_scale=halfButtonInvertHoverScale,
            image2_scale=halfButtonInvertHoverScale,
            pos=(0.20000000000000001, 0, 0),
            command=self._ColorShop__swapHeadColor,
            extraArgs=[1])
        self.bodyFrame = DirectFrame(
            parent=self.parentFrame,
            image=shuffleFrame,
            image_scale=halfButtonScale,
            relief=None,
            pos=(0, 0, -0.5),
            hpr=(0, 0, -2),
            scale=0.90000000000000002,
            frameColor=(1, 1, 1, 1),
            text=TTLocalizer.ColorShopBody,
            text_scale=0.0625,
            text_pos=(-0.001, -0.014999999999999999),
            text_fg=(1, 1, 1, 1))
        self.armLButton = DirectButton(
            parent=self.bodyFrame,
            relief=None,
            image=(shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover,
                   shuffleArrowDisabled),
            image_scale=halfButtonScale,
            image1_scale=halfButtonHoverScale,
            image2_scale=halfButtonHoverScale,
            pos=(-0.20000000000000001, 0, 0),
            command=self._ColorShop__swapArmColor,
            extraArgs=[-1])
        self.armRButton = DirectButton(
            parent=self.bodyFrame,
            relief=None,
            image=(shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover,
                   shuffleArrowDisabled),
            image_scale=halfButtonInvertScale,
            image1_scale=halfButtonInvertHoverScale,
            image2_scale=halfButtonInvertHoverScale,
            pos=(0.20000000000000001, 0, 0),
            command=self._ColorShop__swapArmColor,
            extraArgs=[1])
        self.legsFrame = DirectFrame(
            parent=self.parentFrame,
            image=shuffleFrame,
            image_scale=halfButtonInvertScale,
            relief=None,
            pos=(0, 0, -0.69999999999999996),
            hpr=(0, 0, 3),
            scale=0.90000000000000002,
            frameColor=(1, 1, 1, 1),
            text=TTLocalizer.ColorShopLegs,
            text_scale=0.0625,
            text_pos=(-0.001, -0.014999999999999999),
            text_fg=(1, 1, 1, 1))
        self.legLButton = DirectButton(
            parent=self.legsFrame,
            relief=None,
            image=(shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover,
                   shuffleArrowDisabled),
            image_scale=halfButtonScale,
            image1_scale=halfButtonHoverScale,
            image2_scale=halfButtonHoverScale,
            pos=(-0.20000000000000001, 0, 0),
            command=self._ColorShop__swapLegColor,
            extraArgs=[-1])
        self.legRButton = DirectButton(
            parent=self.legsFrame,
            relief=None,
            image=(shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover,
                   shuffleArrowDisabled),
            image_scale=halfButtonInvertScale,
            image1_scale=halfButtonInvertHoverScale,
            image2_scale=halfButtonInvertHoverScale,
            pos=(0.20000000000000001, 0, 0),
            command=self._ColorShop__swapLegColor,
            extraArgs=[1])
        self.parentFrame.hide()
        self.shuffleFetchMsg = 'ColorShopShuffle'
        self.shuffleButton = ShuffleButton.ShuffleButton(
            self, self.shuffleFetchMsg)

    def unload(self):
        self.gui.removeNode()
        del self.gui
        self.parentFrame.destroy()
        self.toonFrame.destroy()
        self.headFrame.destroy()
        self.bodyFrame.destroy()
        self.legsFrame.destroy()
        self.headLButton.destroy()
        self.headRButton.destroy()
        self.armLButton.destroy()
        self.armRButton.destroy()
        self.legLButton.destroy()
        self.legRButton.destroy()
        self.allLButton.destroy()
        self.allRButton.destroy()
        del self.parentFrame
        del self.toonFrame
        del self.headFrame
        del self.bodyFrame
        del self.legsFrame
        del self.headLButton
        del self.headRButton
        del self.armLButton
        del self.armRButton
        del self.legLButton
        del self.legRButton
        del self.allLButton
        del self.allRButton
        self.shuffleButton.unload()
        self.ignore('MAT-newToonCreated')

    def _ColorShop__swapAllColor(self, offset):
        colorList = self.getGenderColorList(self.dna)
        length = len(colorList)
        choice = (self.headChoice + offset) % length
        self._ColorShop__updateScrollButtons(choice, length, self.allLButton,
                                             self.allRButton)
        self._ColorShop__swapHeadColor(offset)
        oldArmColorIndex = colorList.index(self.toon.style.armColor)
        oldLegColorIndex = colorList.index(self.toon.style.legColor)
        self._ColorShop__swapArmColor(choice - oldArmColorIndex)
        self._ColorShop__swapLegColor(choice - oldLegColorIndex)

    def _ColorShop__swapHeadColor(self, offset):
        colorList = self.getGenderColorList(self.dna)
        length = len(colorList)
        self.headChoice = (self.headChoice + offset) % length
        self._ColorShop__updateScrollButtons(
            self.headChoice, length, self.headLButton, self.headRButton)
        newColor = colorList[self.headChoice]
        self.dna.headColor = newColor
        self.toon.swapToonColor(self.dna)

    def _ColorShop__swapArmColor(self, offset):
        colorList = self.getGenderColorList(self.dna)
        length = len(colorList)
        self.armChoice = (self.armChoice + offset) % length
        self._ColorShop__updateScrollButtons(self.armChoice, length,
                                             self.armLButton, self.armRButton)
        newColor = colorList[self.armChoice]
        self.dna.armColor = newColor
        self.toon.swapToonColor(self.dna)

    def _ColorShop__swapLegColor(self, offset):
        colorList = self.getGenderColorList(self.dna)
        length = len(colorList)
        self.legChoice = (self.legChoice + offset) % length
        self._ColorShop__updateScrollButtons(self.legChoice, length,
                                             self.legLButton, self.legRButton)
        newColor = colorList[self.legChoice]
        self.dna.legColor = newColor
        self.toon.swapToonColor(self.dna)

    def _ColorShop__updateScrollButtons(self, choice, length, lButton,
                                        rButton):
        if choice == (self.startColor - 1) % length:
            rButton['state'] = DGG.DISABLED
        else:
            rButton['state'] = DGG.NORMAL
        if choice == self.startColor % length:
            lButton['state'] = DGG.DISABLED
        else:
            lButton['state'] = DGG.NORMAL

    def _ColorShop__handleForward(self):
        self.doneStatus = 'next'
        messenger.send(self.doneEvent)

    def _ColorShop__handleBackward(self):
        self.doneStatus = 'last'
        messenger.send(self.doneEvent)

    def changeColor(self):
        self.notify.debug('Entering changeColor')
        colorList = self.getGenderColorList(self.dna)
        newChoice = self.shuffleButton.getCurrChoice()
        newHeadColorIndex = colorList.index(newChoice[0])
        newArmColorIndex = colorList.index(newChoice[1])
        newLegColorIndex = colorList.index(newChoice[2])
        oldHeadColorIndex = colorList.index(self.toon.style.headColor)
        oldArmColorIndex = colorList.index(self.toon.style.armColor)
        oldLegColorIndex = colorList.index(self.toon.style.legColor)
        self._ColorShop__swapHeadColor(newHeadColorIndex - oldHeadColorIndex)
        if self.colorAll:
            self._ColorShop__swapArmColor(newHeadColorIndex - oldArmColorIndex)
            self._ColorShop__swapLegColor(newHeadColorIndex - oldLegColorIndex)
        else:
            self._ColorShop__swapArmColor(newArmColorIndex - oldArmColorIndex)
            self._ColorShop__swapLegColor(newLegColorIndex - oldLegColorIndex)

    def getCurrToonSetting(self):
        return [self.dna.headColor, self.dna.armColor, self.dna.legColor]
