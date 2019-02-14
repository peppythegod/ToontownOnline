from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
import FlowerPanel


class FlowerPicker(DirectScrolledList):
    notify = DirectNotifyGlobal.directNotify.newCategory('FlowerPicker')

    def __init__(self, parent=aspect2d, **kw):
        self.flowerList = []
        self.parent = parent
        self.shown = 0
        gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        optiondefs = (('parent', self.parent, None), ('relief', None, None),
                      ('incButton_image',
                       (gui.find('**/FndsLst_ScrollUp'),
                        gui.find('**/FndsLst_ScrollDN'),
                        gui.find('**/FndsLst_ScrollUp_Rllvr'),
                        gui.find('**/FndsLst_ScrollUp')),
                       None), ('incButton_relief', None,
                               None), ('incButton_scale',
                                       (1.6000000000000001, 1.6000000000000001,
                                        -1.6000000000000001), None),
                      ('incButton_pos', (0.16, 0, -0.46999999999999997),
                       None), ('incButton_image3_color',
                               Vec4(0.69999999999999996, 0.69999999999999996,
                                    0.69999999999999996, 0.75),
                               None), ('decButton_image',
                                       (gui.find('**/FndsLst_ScrollUp'),
                                        gui.find('**/FndsLst_ScrollDN'),
                                        gui.find('**/FndsLst_ScrollUp_Rllvr'),
                                        gui.find('**/FndsLst_ScrollUp')),
                                       None), ('decButton_relief', None, None),
                      ('decButton_scale',
                       (1.6000000000000001, 1.6000000000000001,
                        1.6000000000000001),
                       None), ('decButton_pos', (0.16, 0,
                                                 0.089999999999999997), None),
                      ('decButton_image3_color',
                       Vec4(0.69999999999999996, 0.69999999999999996,
                            0.69999999999999996, 0.75),
                       None), ('itemFrame_pos', (-0.025000000000000001, 0, 0),
                               None), ('itemFrame_scale', 0.54000000000000004,
                                       None), ('itemFrame_relief', None, None),
                      ('itemFrame_frameSize', (-0.050000000000000003, 0.75,
                                               -0.75, 0.050000000000000003),
                       None), ('numItemsVisible', 10, None), ('items', [],
                                                              None))
        self.defineoptions(kw, optiondefs)
        DirectScrolledList.__init__(self, parent)
        self.initialiseoptions(FlowerPicker)
        self.flowerGui = loader.loadModel(
            'phase_3.5/models/gui/fishingBook').find('**/bucket')
        self.flowerGui.find('**/fram1').removeNode()
        self.flowerGui.find('**/bubble').removeNode()
        self.flowerGui.find('**/bucket').removeNode()
        self.flowerGui.reparentTo(self, -1)
        self.flowerGui.setPos(0.63, 0.10000000000000001, -0.10000000000000001)
        self.flowerGui.setScale(0.035000000000000003)
        self.basketGui = loader.loadModel(
            'phase_5.5/models/estate/flowerBasket')
        self.basketGui.reparentTo(self, -2)
        self.basketGui.setPos(0.17000000000000001, 0.10000000000000001, 0.0)
        self.basketGui.setScale(1.25)
        self.info = DirectLabel(
            parent=self,
            relief=None,
            text='',
            text_scale=TTLocalizer.FPinfo,
            pos=(0.17999999999999999, 0, -0.67000000000000004))
        self.flowerPanel = FlowerPanel.FlowerPanel(parent=self)
        self.flowerPanel.setSwimBounds(-0.29999999999999999,
                                       0.29999999999999999,
                                       -0.23499999999999999, 0.25)
        self.flowerPanel.setSwimColor(1.0, 1.0, 0.74900999999999995, 1.0)
        gui.removeNode()

    def destroy(self):
        DirectScrolledList.destroy(self)
        self.parent = None
        self.flowerList = []
        self.flowerPanel = None

    def hideFlowerPanel(self):
        self.flowerPanel.hide()

    def hide(self):
        if not hasattr(self, 'loaded'):
            return None

        self.hideFlowerPanel()
        DirectScrolledList.hide(self)
        self.shown = 0

    def show(self):
        if not hasattr(self, 'loaded'):
            self.load()

        self.updatePanel()
        DirectScrolledList.show(self)
        self.shown = 1

    def load(self):
        self.loaded = 1
        self.flowerPanel.load()
        self.flowerPanel.setPos(1.05, 0, 0.10000000000000001)
        self.flowerPanel.setScale(0.90000000000000002)

    def update(self, newFloweres):
        for (flower, flowerButton) in self.flowerList[:]:
            self.removeItem(flowerButton)
            flowerButton.destroy()
            self.flowerList.remove([flower, flowerButton])

        for flower in newFloweres:
            flowerButton = self.makeFlowerButton(flower)
            self.addItem(flowerButton)
            self.flowerList.append([flower, flowerButton])

        value = 0
        for flower in newFloweres:
            value += flower.getValue()

        maxFlower = base.localAvatar.getMaxFlowerBasket()
        self.info['text'] = TTLocalizer.FlowerPickerTotalValue % (
            len(newFloweres), maxFlower, value)
        if self.shown:
            self.updatePanel()

    def updatePanel(self):
        if len(self.flowerList) >= 1:
            self.showFlowerPanel(self.flowerList[0][0])
        else:
            self.hideFlowerPanel()

    def makeFlowerButton(self, flower):
        return DirectScrolledListItem(
            parent=self,
            relief=None,
            text=flower.getFullName(),
            text_scale=0.070000000000000007,
            text_align=TextNode.ALeft,
            text1_fg=Vec4(1, 1, 0, 1),
            text2_fg=Vec4(0.5, 0.90000000000000002, 1, 1),
            text3_fg=Vec4(0.40000000000000002, 0.80000000000000004,
                          0.40000000000000002, 1),
            command=self.showFlowerPanel,
            extraArgs=[flower])

    def showFlowerPanel(self, flower):
        self.flowerPanel.update(flower)
        self.flowerPanel.show()
        messenger.send('wakeup')
