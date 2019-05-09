from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed.DistributedObjectAI import DistributedObjectAI


class DistributedTrophyMgrAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedTrophyMgrAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def requestTrophyScore(self):
        pass

    def addTrophy(self, avId, name, numFloors):
        pass

    def removeTrophy(self, avId, numFloors):
        pass

    def updateTrophyScore(self, avId, trophyScore):
        pass

    def reorganize(self):
        pass

    def getLeaderInfo(self):
        return ([], [], [])