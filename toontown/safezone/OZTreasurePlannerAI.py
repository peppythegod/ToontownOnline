from toontown.toonbase.ToontownGlobals import *
import RegenTreasurePlannerAI
import DistributedOZTreasureAI


class OZTreasurePlannerAI(RegenTreasurePlannerAI.RegenTreasurePlannerAI):

    def __init__(self, zoneId):
        self.healAmount = 3
        RegenTreasurePlannerAI.RegenTreasurePlannerAI.__init__(
            self,
            zoneId,
            DistributedOZTreasureAI.DistributedOZTreasureAI,
            'OZTreasurePlanner',
            20,
            5)

    def initSpawnPoints(self):
        self.spawnPoints = [
            (-156.90000000000001, -118.90000000000001, 0.025000000000000001),
            (-35.600000000000001, 86.0, 1.25),
            (116.8, 10.800000000000001, 0.104),
            (-35, 145.69999999999999, 0.025000000000000001),
            (-198.80000000000001, -45.100000000000001, 0.025000000000000001),
            (-47.100000000000001, -25.5, 0.80900000000000005),
            (59.149999999999999, 34.799999999999997, 1.7669999999999999),
            (-81.019999999999996, -72.200000000000003, 0.025999999999999999),
            (-167.90000000000001, 124.5, 0.025000000000000001),
            (-226.69999999999999, -27.600000000000001, 0.025000000000000001),
            (-16.0, -108.90000000000001, 0.025000000000000001),
            (18.0, 58.5, 5.9189999999999996),
            (91.400000000000006, 127.8, 0.025000000000000001),
            (-86.5, -75.900000000000006, 0.025000000000000001),
            (-48.750999999999998, -32.299999999999997, 1.143)]
        return self.spawnPoints
