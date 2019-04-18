from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal


class SafeZoneManager(DistributedObjectAI.DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('SafeZoneManagerAI')
    neverDisable = 1

    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)

    def enterSafeZone(self):
        pass

    def exitSafeZone(self):
        pass
