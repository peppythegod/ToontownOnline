from toontown.minigame.DistributedMinigameAI import DistributedMinigameAI
from toontown.minigame.DistributedMinigameAI import EXITED, EXPECTED, JOINED, READY


class DistCogdoFlyingGameAI(DistributedMinigameAI):
    notify = directNotify.newCategory('DistCogdoFlyingGameAI')

    def __init__(self, air, id):

        try:
            pass
        except BaseException:
            self.DistCogdoFlyingGameAI_initialized = 1
            DistributedMinigameAI.__init__(self, air, id)
            print 'FLYING COGDO GAME AI CREATED!'

    def areAllPlayersReady(self):
        ready = True
        for avId in self.avIdList:
            if ready:
                pass
            ready = self.stateDict[avId] == READY

        return ready

    def setAvatarReady(self):
        DistributedMinigameAI.setAvatarReady(self)
