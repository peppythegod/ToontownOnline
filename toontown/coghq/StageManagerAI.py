from direct.directnotify import DirectNotifyGlobal
import DistributedStageAI
from toontown.toonbase import ToontownGlobals
from toontown.coghq import StageLayout
from direct.showbase import DirectObject
import random

StageId2Layouts = {
    ToontownGlobals.LawbotStageIntA: (0, 1, 2),
    ToontownGlobals.LawbotStageIntB: (3, 4, 5),
    ToontownGlobals.LawbotStageIntC: (6, 7, 8),
    ToontownGlobals.LawbotStageIntD: (9, 10, 11)
}


class StageManagerAI(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('StageManagerAI')
    stageId = None

    def __init__(self, air):
        DirectObject.DirectObject.__init__(self)
        self.air = air

    def getDoId(self):
        return 0
        
    def createStage(self, stageId, entranceId, players):
        for avId in players:
            if bboard.has('stageId-%s' % avId):
                stageId = bboard.get('stageId-%s' % avId)
                break
                
        floor = 0
        layoutIndex = None
        for avId in players:
            if bboard.has('stageRoom-%s' % avId):
                roomId = bboard.get('stageRoom-%s' % avId)
                for lt in StageId2Layouts[stageId]:
                    for i in xrange(StageLayout.getNumFloors(lt)):
                        layout = StageLayout.StageLayout(stageId, i, stageLayout = lt)
                        if roomId in layout.getRoomIds():
                            layoutIndex = lt
                            floor = i
                else:
                    import StageRoomSpecs
                    roomName = StageRoomSpecs.CashbotStageRoomId2RoomName[roomId]
                    self.notify.warning('room %s (%s) not found in any floor of Stage %s' % (roomId, roomName, stageId))
        
        stageZone = self.air.allocateZone()
        
        if layoutIndex is None:
            layoutIndex = random.choice(StageId2Layouts[stageId])
            
        stage = DistributedStageAI.DistributedStageAI(self.air, stageId, stageZone, floor, players, layoutIndex)
        stage.generateWithRequired(stageZone)
        return stageZone 

    def createStageOld(self, stageId, players):
        for avId in players:
            if bboard.has('stageId-%s' % avId):
                stageId = bboard.get('stageId-%s' % avId)
                break

        numFloors = StageLayout.getNumFloors(stageId)
        floor = random.randrange(numFloors)
        for avId in players:
            if bboard.has('stageFloor-%s' % avId):
                floor = bboard.get('stageFloor-%s' % avId)
                floor = max(0, floor)
                floor = min(floor, numFloors - 1)
                break

        for avId in players:
            if bboard.has('stageRoom-%s' % avId):
                roomId = bboard.get('stageRoom-%s' % avId)
                for i in xrange(numFloors):
                    layout = StageLayout.StageLayout(stageId, i)
                    if roomId in layout.getRoomIds():
                        floor = i
                        continue
                else:
                    StageRoomSpecs = StageRoomSpecs
                    roomName = StageRoomSpecs.CashbotStageRoomId2RoomName[
                        roomId]
                    StageManagerAI.notify.warning(
                        'room %s (%s) not found in any floor of stage %s' %
                        (roomId, roomName, stageId))

        stageZone = self.air.allocateZone()
        stage = DistributedStageAI.DistributedStageAI(
            self.air, stageId, stageZone, floor, players)
        stage.generateWithRequired(stageZone)
        return stageZone
        
    def createLawOffice(self, stageId, entranceId, players):
        return self.createStage(stageId , entranceId, players)