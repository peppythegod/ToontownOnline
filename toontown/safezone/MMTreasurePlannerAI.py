from toontown.toonbase.ToontownGlobals import *
import RegenTreasurePlannerAI
import DistributedMMTreasureAI


class MMTreasurePlannerAI(RegenTreasurePlannerAI.RegenTreasurePlannerAI):
    def __init__(self, zoneId):
        self.healAmount = 10
        RegenTreasurePlannerAI.RegenTreasurePlannerAI.__init__(
            self, zoneId, DistributedMMTreasureAI.DistributedMMTreasureAI,
            'MMTreasurePlanner', 20, 2)

    def initSpawnPoints(self):
        self.spawnPoints = [(118, -39, 3.2999999999999998),
                            (118, 1, 3.2999999999999998),
                            (112, -22, 0.80000000000000004), (108, -74, -4.5),
                            (110, -65, -4.5), (102, 23.5, -4.5), (60, -115,
                                                                  6.5),
                            (-5, -115, 6.5), (-64, -77, 6.5), (-77, -44, 6.5),
                            (-76, 3, 6.5), (44, 76, 6.5), (136, -96, -13.5),
                            (85, -6.7000000000000002, -13.5), (60, -95, -14.5),
                            (72, 60, -13.5), (-55, -23, -14.5), (-21, 47,
                                                                 -14.5),
                            (-24, -75, -14.5)]
        return self.spawnPoints
