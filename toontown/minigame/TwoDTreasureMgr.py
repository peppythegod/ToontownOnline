from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject
from toontown.minigame import ToonBlitzGlobals
from toontown.minigame import TwoDTreasure
import random


class TwoDTreasureMgr(DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('TwoDTreasureMgr')

    def __init__(self, section, treasureList, enemyList):
        self.section = section
        self.treasureList = treasureList
        self.enemyList = enemyList
        self.load()

    def destroy(self):
        while len(self.treasures):
            treasure = self.treasures[0]
            treasure.destroy()
            self.treasures.remove(treasure)
        self.treasures = None
        self.section = None

    def load(self):
        if len(self.treasureList):
            self.treasuresNP = NodePath('Treasures')
            self.treasuresNP.reparentTo(self.section.sectionNP)

        self.treasures = []
        for index in xrange(len(self.treasureList)):
            treasureAttribs = self.treasureList[index][0]
            treasureValue = self.treasureList[index][1]
            self.createNewTreasure(treasureAttribs, treasureValue)

        self.enemyTreasures = []
        numPlayers = self.section.sectionMgr.game.numPlayers
        pos = Point3(-1, -1, -1)
        for index in xrange(len(self.enemyList)):
            self.createNewTreasure([pos], numPlayers, isEnemyGenerated=True)

    def createNewTreasure(self,
                          attrib,
                          value,
                          isEnemyGenerated=False,
                          model=None):
        treasureId = self.section.getSectionizedId(len(self.treasures))
        if model is None:
            model = self.getModel(
                value, self.section.sectionMgr.game.assetMgr.treasureModelList)

        newTreasure = TwoDTreasure.TwoDTreasure(self, treasureId, attrib[0],
                                                value, isEnemyGenerated, model)
        newTreasure.model.reparentTo(self.treasuresNP)
        self.treasures.append(newTreasure)
        if isEnemyGenerated:
            self.enemyTreasures.append(newTreasure)

    def getModel(self, value, modelList):
        value -= 1
        model = modelList[value]
        if value == 0:
            model.setColor(1, 0.80000000000000004, 0.80000000000000004, 1)
        elif value == 1:
            model.setColor(0.80000000000000004, 1, 0.80000000000000004, 1)
        elif value == 2:
            model.setColor(0.90000000000000002, 0.90000000000000002, 1, 1)
        elif value == 3:
            model.setColor(1, 1, 0.59999999999999998, 1)

        return model
