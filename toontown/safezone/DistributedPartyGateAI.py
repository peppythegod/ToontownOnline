from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal


class DistributedPartyGate(DistributedObjectAI.DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedPartyGateAI')

    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)

    def getPartyList(self, avId):
        pass
        
    def partyChoiceRequest(self, avId, ds1, ds2):
        pass