from toontown.toonbase.ToontownGlobals import *
import RegenTreasurePlannerAI
import DistributedDLTreasureAI


class DLTreasurePlannerAI(RegenTreasurePlannerAI.RegenTreasurePlannerAI):
    def __init__(self, zoneId):
        self.healAmount = 12
        RegenTreasurePlannerAI.RegenTreasurePlannerAI.__init__(
            self, zoneId, DistributedDLTreasureAI.DistributedDLTreasureAI,
            'DLTreasurePlanner', 20, 2)

    def initSpawnPoints(self):
        self.spawnPoints = [(86, 69, -17.399999999999999),
                            (34, -48, -16.399999999999999), (87, -70, -17.5),
                            (-98, 99, 0.0), (51, 100, 0.0), (-45, -12, -15.0),
                            (9, 8, -15.0), (-24, 64, -17.199999999999999),
                            (-100, -99, 0.0), (21, -101, 0.0), (88, -17,
                                                                -15.0),
                            (32, 70, -17.399999999999999),
                            (53, 35, -15.800000000000001), (2, -30, -15.5),
                            (-40, -56, -16.800000000000001), (-28, 18, -15.0),
                            (-34, -88, 0.0)]
        return self.spawnPoints
