from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI


class TimeManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("TimeManagerAI")

    def requestServerTime(self, todo0):
        pass

    def serverTime(self, todo0, todo1, todo2):
        pass

    def setDisconnectReason(self, todo0):
        pass

    def setExceptionInfo(self, todo0):
        pass

    def setSignature(self, todo0, todo1, todo2):
        pass

    def setFrameRate(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6,
                     todo7, todo8, todo9, todo10, todo11, todo12, todo13,
                     todo14, todo15, todo16, todo17):
        pass

    def setCpuInfo(self, todo0, todo1):
        pass

    def checkForGarbageLeaks(self, todo0):
        pass

    def setNumAIGarbageLeaks(self, todo0):
        pass

    def setClientGarbageLeak(self, todo0, todo1):
        pass

    def checkAvOnDistrict(self, todo0, todo1):
        pass

    def checkAvOnDistrictResult(self, todo0, todo1, todo2):
        pass
