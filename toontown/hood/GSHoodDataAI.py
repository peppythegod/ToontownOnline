from direct.directnotify import DirectNotifyGlobal
import HoodDataAI
import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.racing import DistributedStartingBlockAI
from pandac.PandaModules import *
from toontown.racing.RaceGlobals import *
from toontown.classicchars import DistributedGoofySpeedwayAI
from toontown.dna.DNAParser import DNAData
if __debug__:
    import pdb


class GSHoodDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('GSHoodDataAI')

    def __init__(self, air, zoneId=None):
        hoodId = ToontownGlobals.GoofySpeedway
        if zoneId is None:
            zoneId = hoodId

        HoodDataAI.HoodDataAI.__init__(self, air, zoneId, hoodId)

    def startup(self):
        HoodDataAI.HoodDataAI.startup(self)
        #self.createStartingBlocks()
        self.cycleDuration = 10
        #self.createLeaderBoards()
        #self._GSHoodDataAI__cycleLeaderBoards()
        self.classicChar = DistributedGoofySpeedwayAI.DistributedGoofySpeedwayAI(
            self.air)
        self.classicChar.generateWithRequired(self.zoneId)
        self.classicChar.start()
        self.addDistObj(self.classicChar)
        messenger.send('GSHoodSpawned', [self])

    def shutdown(self):
        self.notify.debug('shutting down GSHoodDataAI: %s' % self.zoneId)
        messenger.send('GSHoodDestroyed', [self])
        HoodDataAI.HoodDataAI.shutdown(self)

    def cleanup(self):
        self.notify.debug('cleaning up GSHoodDataAI: %s' % self.zoneId)
        taskMgr.removeTasksMatching(str(self) + '_leaderBoardSwitch')
        for board in self.leaderBoards:
            board.delete()

        del self.leaderBoards

    def createLeaderBoards(self):
        self.leaderBoards = []
        dnaStore = DNAStorage()
        dnaData = simbase.air.loadDNAFileAI(
            dnaStore, simbase.air.genDNAFileName(self.zoneId))
        if isinstance(dnaData, DNAData):
            pass #TODO
            #self.leaderBoards = self.air.findLeaderBoards(dnaData, self.zoneId)

        for distObj in self.leaderBoards:
            if distObj:
                if distObj.getName().count('city'):
                    type = 'city'
                elif distObj.getName().count('stadium'):
                    type = 'stadium'
                elif distObj.getName().count('country'):
                    type = 'country'

                for subscription in LBSubscription[type]:
                    distObj.subscribeTo(subscription)

                self.addDistObj(distObj)
                continue

    def _GSHoodDataAI__cycleLeaderBoards(self, task=None):
        messenger.send('GS_LeaderBoardSwap' + str(self.zoneId))
        taskMgr.doMethodLater(self.cycleDuration,
                              self._GSHoodDataAI__cycleLeaderBoards,
                              str(self) + '_leaderBoardSwitch')

    def createStartingBlocks(self):
        self.racingPads = []
        self.viewingPads = []
        self.viewingBlocks = []
        self.startingBlocks = []
        self.foundRacingPadGroups = []
        self.foundViewingPadGroups = []
        for zone in self.air.zoneTable[self.canonicalHoodId]:
            zoneId = ZoneUtil.getTrueZoneId(zone[0], self.zoneId)
            dnaData = self.air.dnaDataMap.get(zone[0], None)
            if isinstance(dnaData, DNAData):
                area = ZoneUtil.getCanonicalZoneId(zoneId)
                (foundRacingPads,
                 foundRacingPadGroups) = self.air.findRacingPads(
                     dnaData, zoneId, area)
                (foundViewingPads,
                 foundViewingPadGroups) = self.air.findRacingPads(
                     dnaData, zoneId, area, type='viewing_pad')
                self.racingPads += foundRacingPads
                self.foundRacingPadGroups += foundRacingPadGroups
                self.viewingPads += foundViewingPads
                self.foundViewingPadGroups += foundViewingPadGroups
                continue

        self.startingBlocks = []
        for (dnaGroup, distRacePad) in zip(self.foundRacingPadGroups,
                                           self.racingPads):
            startingBlocks = self.air.findStartingBlocks(dnaGroup, distRacePad)
            self.startingBlocks += startingBlocks
            for startingBlock in startingBlocks:
                distRacePad.addStartingBlock(startingBlock)

        for distObj in self.startingBlocks:
            self.addDistObj(distObj)

        for (dnaGroup, distViewPad) in zip(self.foundViewingPadGroups,
                                           self.viewingPads):
            viewingBlocks = self.air.findStartingBlocks(dnaGroup, distViewPad)
            self.viewingBlocks += viewingBlocks
            for viewingBlock in viewingBlocks:
                distViewPad.addStartingBlock(viewingBlock)

        for distObj in self.viewingBlocks:
            self.addDistObj(distObj)

        for viewPad in self.viewingPads:
            self.addDistObj(viewPad)

        for racePad in self.racingPads:
            racePad.request('WaitEmpty')
            self.addDistObj(racePad)
