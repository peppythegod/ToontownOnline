from toontown.toonbase.ToontownGlobals import *
import RegenTreasurePlannerAI
import DistributedBRTreasureAI


class BRTreasurePlannerAI(RegenTreasurePlannerAI.RegenTreasurePlannerAI):

    def __init__(self, zoneId):
        self.healAmount = 12
        RegenTreasurePlannerAI.RegenTreasurePlannerAI.__init__(
            self,
            zoneId,
            DistributedBRTreasureAI.DistributedBRTreasureAI,
            'BRTreasurePlanner',
            20,
            2)

    def initSpawnPoints(self):
        self.spawnPoints = [
            (-108, 46, 6.2000000000000002),
            (-111, 74, 6.2000000000000002),
            (-126, 81, 6.2000000000000002),
            (-74, -75, 3.0),
            (-136, -51, 3.0),
            (-20, 35, 6.2000000000000002),
            (-55, 109, 6.2000000000000002),
            (58, -57, 6.2000000000000002),
            (-42, -134, 6.2000000000000002),
            (-68, -148, 6.2000000000000002),
            (-1, -62, 6.2000000000000002),
            (25, 2, 6.2000000000000002),
            (-133, 53, 6.2000000000000002),
            (-99, 86, 6.2000000000000002),
            (30, 63, 6.2000000000000002),
            (-147, 3, 6.2000000000000002),
            (-135, -102, 6.2000000000000002),
            (35, -98, 6.2000000000000002)]
        return self.spawnPoints
