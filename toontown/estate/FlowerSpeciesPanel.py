from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
import GardenGlobals
import FlowerPhoto
from toontown.estate import BeanRecipeGui


class FlowerSpeciesPanel(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('FlowerSpeciesPanel')

    def __init__(self, species=None, itemIndex=0, *extraArgs):
        flowerGui = loader.loadModel('phase_3.5/models/gui/fishingBook')
        albumGui = flowerGui.find('**/photo_frame1')
        pictureGroup = albumGui.attachNewNode('PictureGroup')
        hideList = ['corner_backs', 'shadow', 'bg', 'corners', 'picture']
        for name in hideList:
            temp = flowerGui.find('**/%s' % name)
            if not temp.isEmpty():
                temp.wrtReparentTo(pictureGroup)
                continue

        pictureGroup.setPos(0, 0, 1.0)
        albumGui.find('**/arrows').removeNode()
        optiondefs = (('relief', None, None), ('state', DGG.NORMAL, None),
                      ('image', albumGui,
                       None), ('image_scale',
                               (0.025000000000000001, 0.025000000000000001,
                                0.025000000000000001),
                               None), ('image_pos', (0, 1, 0), None),
                      ('text', TTLocalizer.FlowerUnknown,
                       None), ('text_scale', 0.065000000000000002, None),
                      ('text_fg', (0.20000000000000001, 0.10000000000000001,
                                   0.0, 1),
                       None), ('text_pos', (-0.5, -0.34000000000000002),
                               None), ('text_font',
                                       ToontownGlobals.getInterfaceFont(),
                                       None), ('text_wordwrap', 13.5,
                                               None), ('text_align',
                                                       TextNode.ALeft, None))
        self.defineoptions({}, optiondefs)
        DirectFrame.__init__(self)
        self.initialiseoptions(FlowerSpeciesPanel)
        self.flowerPanel = None
        self.species = None
        self.variety = 0
        self.flowerCollection = extraArgs[0]
        self.setSpecies(int(species))
        self.setScale(1.2)
        albumGui.removeNode()
        self.beanRecipeGui = None

    def destroy(self):
        if self.flowerPanel:
            self.flowerPanel.destroy()
            del self.flowerPanel

        self.flowerCollection = None
        self.cleanupBeanRecipeGui()
        DirectFrame.destroy(self)

    def load(self):
        pass

    def setSpecies(self, species):
        if self.species == species:
            return None

        self.species = species
        if self.species is not None:
            if self.flowerPanel:
                self.flowerPanel.destroy()

            varietyToUse = self.flowerCollection.getInitialVariety(
                self.species)
            self.variety = varietyToUse
            self.flowerPanel = FlowerPhoto.FlowerPhoto(
                species=self.species, variety=varietyToUse, parent=self)
            zAdj = 0.013100000000000001
            xAdj = -0.002
            self.flowerPanel.setPos(-0.22900000000000001 + xAdj, 1,
                                    -0.01 + zAdj)
            self.flowerPanel.setSwimBounds(
                -0.24610000000000001, 0.23669999999999999,
                -0.20699999999999999 + zAdj, 0.26640000000000003 + zAdj)
            self.flowerPanel.setSwimColor(0.75, 0.75, 0.75, 1.0)
            varietyList = GardenGlobals.getFlowerVarieties(self.species)
            self.speciesLabels = []
            offset = 0.074999999999999997
            startPos = (len(varietyList) / 2) * offset
            if not len(varietyList) % 2:
                startPos -= offset / 2

            for variety in range(len(varietyList)):
                label = DirectButton(
                    parent=self,
                    frameSize=(0, 0.44500000000000001, -0.02,
                               0.040000000000000001),
                    relief=None,
                    state=DGG.DISABLED,
                    pos=(0.059999999999999998, 0, startPos - variety * offset),
                    text=TTLocalizer.FlowerUnknown,
                    text_fg=(0.20000000000000001, 0.10000000000000001, 0.0, 1),
                    text_scale=(0.044999999999999998, 0.044999999999999998,
                                0.45000000000000001),
                    text_align=TextNode.ALeft,
                    text_font=ToontownGlobals.getInterfaceFont(),
                    command=self.changeVariety,
                    extraArgs=[variety],
                    text1_bg=Vec4(1, 1, 0, 1),
                    text2_bg=Vec4(0.5, 0.90000000000000002, 1, 1),
                    text3_fg=Vec4(0.40000000000000002, 0.80000000000000004,
                                  0.40000000000000002, 1))
                self.speciesLabels.append(label)

    def show(self):
        self.update()
        DirectFrame.show(self)

    def hide(self):
        if self.flowerPanel is not None:
            self.flowerPanel.hide()

        if self.beanRecipeGui is not None:
            self.beanRecipeGui.hide()

        DirectFrame.hide(self)

    def showRecipe(self):
        if base.localAvatar.flowerCollection.hasSpecies(self.species):
            self['text'] = TTLocalizer.FlowerSpeciesNames[self.species]
            if base.localAvatar.flowerCollection.hasFlower(
                    self.species, self.variety):
                name = GardenGlobals.getFlowerVarietyName(
                    self.species, self.variety)
                recipeKey = GardenGlobals.PlantAttributes[
                    self.species]['varieties'][self.variety][0]
                self['text'] = name
                self.createBeanRecipeGui(
                    GardenGlobals.Recipes[recipeKey]['beans'])
            else:
                self.cleanupBeanRecipeGui()
        else:
            self['text'] = TTLocalizer.FlowerUnknown
            self.cleanupBeanRecipeGui()

    def update(self):
        if base.localAvatar.flowerCollection.hasSpecies(self.species):
            self.flowerPanel.show(showBackground=0)
            self['text'] = TTLocalizer.FlowerSpeciesNames[self.species]

        for variety in range(
                len(GardenGlobals.getFlowerVarieties(self.species))):
            if base.localAvatar.flowerCollection.hasFlower(
                    self.species, variety):
                name = GardenGlobals.getFlowerVarietyName(
                    self.species, variety)
                self.speciesLabels[variety]['text'] = name
                self.speciesLabels[variety]['state'] = DGG.NORMAL
                continue

        self.showRecipe()

    def changeVariety(self, variety):
        self.variety = variety
        self.flowerPanel.changeVariety(variety)
        self.flowerPanel.show()
        self.showRecipe()

    def createBeanRecipeGui(self, recipe):
        if self.beanRecipeGui:
            self.beanRecipeGui.destroy()

        pos1 = (-0.20000000000000001, 0, -0.36499999999999999)
        pos2 = (-0.46000000000000002, 0, 0.29999999999999999)
        pos3 = (-0.46000000000000002, 0, -0.29999999999999999)
        pos4 = (-0.59999999999999998, 0, -0.27000000000000002)
        self.beanRecipeGui = BeanRecipeGui.BeanRecipeGui(
            aspect2dp,
            recipe,
            pos=pos4,
            scale=1.3,
            frameColor=(0.80000000000000004, 0.80000000000000004,
                        0.80000000000000004, 1.0))

    def cleanupBeanRecipeGui(self):
        if self.beanRecipeGui:
            self.beanRecipeGui.destroy()
            self.beanRecipeGui = None
