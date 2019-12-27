from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI


class DistributedRaceAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedRaceAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.zoneId = 0
        self.trackId = 0
        self.raceType = 0
        self.circuitLoop = []
        self.avatars = []
        self.startingPlaces = []
        self.lapCount = 0
        self.avatarKarts = []

    def setZoneId(self, zoneId):
        self.zoneId = zoneId
        
    def getZoneId(self):
        return self.zoneId

    def setTrackId(self, trackId):
        self.trackId = trackId
        
    def getTrackId(self):
        return self.trackId

    def setRaceType(self, raceType):
        self.raceType = raceType
        
    def getRaceType(self):
        return self.raceType

    def setCircuitLoop(self, circuitLoop):
        self.circuitLoop = circuitLoop
        
    def getCircuitLoop(self):
        return self.circuitLoop

    def setAvatars(self, avatars):
        self.avatars = avatars
        
    def getAvatars(self):
        return self.avatars

    def setStartingPlaces(self, startingPlaces):
        self.startingPlaces = startingPlaces
        
    def getStartingPlaces(self):
        return self.startingPlaces

    def setLapCount(self, lapCount):
        self.lapCount = lapCount
        
    def getLapCount(self):
        return self.lapCount

    def waitingForJoin(self):
        self.beginBarrier('waitingForJoin', self.avatars, 60, self.b_prepForRace)
        
    def prepForRace(self):
        pass
        
    def d_prepForRace(self):
        self.sendUpdate('prepForRace', [])

    def b_prepForRace(self, avatars):
        self.prepForRace()
        self.d_prepForRace()

    def d_setEnteredRacers(self, racers):
        self.sendUpdate('setEnteredRacers', [racers])

    def startTutorial(self):
        self.beginBarrier('readRules', self.avatars, 60, self.raceStart)

    def d_startTutorial(self):
        self.sendUpdate('startTutorial', [])

    def b_startTutorial(self, avatars):
        self.startTutorial()
        self.d_startTutorial()

    def startRace(self, todo0):
        pass

    def goToSpeedway(self, todo0, todo1):
        pass

    def genGag(self, todo0, todo1, todo2):
        pass

    def dropAnvilOn(self, todo0, todo1, todo2):
        pass

    def shootPiejectile(self, todo0, todo1, todo2):
        pass

    def racerDisconnected(self, todo0):
        pass

    def setPlace(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6, todo7,
                 todo8, todo9):
        pass

    def setCircuitPlace(self, todo0, todo1, todo2, todo3, todo4, todo5):
        pass

    def endCircuitRace(self):
        pass

    def setRaceZone(self, todo0, todo1):
        pass

    def hasGag(self, todo0, todo1, todo2):
        pass

    def racerLeft(self, todo0):
        pass

    def heresMyT(self, todo0, todo1, todo2, todo3):
        pass

    def requestThrow(self, todo0, todo1, todo2):
        pass

    def requestKart(self):
        pass
