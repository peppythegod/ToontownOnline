from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from direct.task import Task
import FlowerBase
import FlowerPicker


class FlowerSellGUI(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('FlowerGui')

    def __init__(self, doneEvent):
        DirectFrame.__init__(self,
                             relief=None,
                             state='normal',
                             geom=DGG.getDefaultDialogGeom(),
                             geom_color=ToontownGlobals.GlobalDialogColor,
                             geom_scale=(2.0,
                                         1,
                                         1.5),
                             frameSize=(-1,
                                        1,
                                        -1,
                                        1),
                             pos=(0,
                                  0,
                                  0),
                             text='',
                             text_wordwrap=26,
                             text_scale=TTLocalizer.FSGUIdirectFrame,
                             text_pos=(0,
                                       0.65000000000000002))
        self.initialiseoptions(FlowerSellGUI)
        self.doneEvent = doneEvent
        self.picker = FlowerPicker.FlowerPicker(self)
        self.picker.load()
        self.picker.setPos(-0.58999999999999997, 0, 0.029999999999999999)
        self.picker.setScale(0.93000000000000005)
        newBasketFlower = base.localAvatar.flowerBasket.getFlower()
        self.picker.update(newBasketFlower)
        self.picker.show()
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        okImageList = (
            buttons.find('**/ChtBx_OKBtn_UP'),
            buttons.find('**/ChtBx_OKBtn_DN'),
            buttons.find('**/ChtBx_OKBtn_Rllvr'))
        cancelImageList = (
            buttons.find('**/CloseBtn_UP'),
            buttons.find('**/CloseBtn_DN'),
            buttons.find('**/CloseBtn_Rllvr'))
        self.cancelButton = DirectButton(
            parent=self,
            relief=None,
            image=cancelImageList,
            pos=(
                0.29999999999999999,
                0,
                -0.57999999999999996),
            text=TTLocalizer.FlowerGuiCancel,
            text_scale=TTLocalizer.FSGUIcancelButton,
            text_pos=(
                0,
                -0.10000000000000001),
            command=self._FlowerSellGUI__cancel)
        self.okButton = DirectButton(
            parent=self,
            relief=None,
            image=okImageList,
            pos=(
                0.59999999999999998,
                0,
                -0.57999999999999996),
            text=TTLocalizer.FlowerGuiOk,
            text_scale=TTLocalizer.FSGUIokButton,
            text_pos=(
                0,
                -0.10000000000000001),
            command=self._FlowerSellGUI__sellFlower)
        buttons.removeNode()
        self._FlowerSellGUI__updateFlowerValue()
        base.cr.playGame.getPlace().detectedFlowerSellUse()

    def destroy(self):
        DirectFrame.destroy(self)
        base.cr.playGame.getPlace().detectedFlowerSellDone()

    def _FlowerSellGUI__cancel(self):
        messenger.send(self.doneEvent, [
            0])

    def _FlowerSellGUI__sellFlower(self):
        messenger.send(self.doneEvent, [
            1])

    def _FlowerSellGUI__updateFlowerValue(self):
        flowerBasket = base.localAvatar.getFlowerBasket()
        num = len(flowerBasket)
        value = flowerBasket.getTotalValue()
        self['text'] = TTLocalizer.FlowerBasketValue % {
            'name': base.localAvatar.getName(),
            'num': num,
            'value': value}
        self.setText()
