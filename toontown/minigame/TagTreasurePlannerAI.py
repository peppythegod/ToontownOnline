from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase.ToontownGlobals import *
from toontown.safezone import RegenTreasurePlannerAI
import DistributedTagTreasureAI


class TagTreasurePlannerAI(RegenTreasurePlannerAI.RegenTreasurePlannerAI):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'TagTreasurePlannerAI')

    def __init__(self, zoneId, callback):
        self.numPlayers = 0
        RegenTreasurePlannerAI.RegenTreasurePlannerAI.__init__(
            self, zoneId, DistributedTagTreasureAI.DistributedTagTreasureAI,
            'TagTreasurePlanner-' + str(zoneId), 3, 4, callback)

    def initSpawnPoints(self):
        self.spawnPoints = [(0, 0, 0.10000000000000001),
                            (5, 20, 0.10000000000000001),
                            (0, 40, 0.10000000000000001),
                            (-5, -20, 0.10000000000000001),
                            (0, -40, 0.10000000000000001),
                            (20, 0, 0.10000000000000001),
                            (40, 5, 0.10000000000000001),
                            (-20, -5, 0.10000000000000001),
                            (-40, 0, 0.10000000000000001),
                            (22, 20, 0.10000000000000001),
                            (-20, 22, 0.10000000000000001),
                            (20, -20, 0.10000000000000001),
                            (-25, -20, 0.10000000000000001),
                            (20, 40, 0.10000000000000001),
                            (20, -44, 0.10000000000000001),
                            (-24, 40, 0.10000000000000001),
                            (-20, -40, 0.10000000000000001)]
        return self.spawnPoints
