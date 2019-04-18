from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal


class DistributedFishingSpotAI(DistributedObjectAI.DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedFishingSpotAI')

    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)

    def requestEnter(self):
        pass
        
    def requestExit(self):
        pass
        
    def doCast(self, a, b):
        pass
    
    def sellFish(self):
        pass