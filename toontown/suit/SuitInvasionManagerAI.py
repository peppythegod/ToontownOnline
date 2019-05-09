import time

from toontown.battle import SuitBattleGlobals
from toontown.suit import SuitDNA
from toontown.toonbase import ToontownGlobals


class SuitInvasionManagerAI:
    def __init__(self, air):
        self.air = air

        self.invading = False
        self.start = 0
        self.remaining = 0
        self.total = 0
        self.suitDeptIndex = None
        self.suitTypeIndex = None
        self.flags = 0

    def getInvading(self):
        return self.invading
        
    def getInvadingCog(self):
        return (None, False)