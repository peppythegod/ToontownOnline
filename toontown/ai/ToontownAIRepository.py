from direct.distributed.PyDatagram import *
from pandac.PandaModules import *
from toontown.ai.MessageTypes import *
from otp.ai.AIZoneData import AIZoneDataStore
from otp.ai.TimeManagerAI import TimeManagerAI
from otp.distributed.OtpDoGlobals import *
from toontown.tutorial.TutorialManagerAI import TutorialManagerAI
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.distributed.ToontownDistrictAI import ToontownDistrictAI
from toontown.distributed.ToontownDistrictStatsAI import ToontownDistrictStatsAI
from toontown.distributed.ToontownInternalRepository import ToontownInternalRepository
from toontown.toonbase import ToontownGlobals
from toontown.ai.QuestManagerAI import QuestManagerAI
from toontown.safezone.SafeZoneManagerAI import SafeZoneManagerAI
from toontown.toon import NPCToons
from toontown.hood import TTHoodDataAI, DDHoodDataAI, OZHoodDataAI, GZHoodDataAI, DGHoodDataAI,\
    MMHoodDataAI, BRHoodDataAI, DLHoodDataAI, CSHoodDataAI, CashbotHQDataAI, LawbotHQDataAI, BossbotHQDataAI, GSHoodDataAI
from toontown.hood import ZoneUtil
from toontown.dna.DNAParser import *
from toontown.building.DistributedTrophyMgrAI import DistributedTrophyMgrAI
from toontown.ai.HolidayManagerAI import HolidayManagerAI
from toontown.coghq import FactoryManagerAI
from toontown.suit.SuitInvasionManagerAI import SuitInvasionManagerAI
from toontown.ai import CogSuitManagerAI
from toontown.ai import PromotionManagerAI
from toontown.ai import CogPageManagerAI
from toontown.coghq import MintManagerAI
from toontown.coghq import StageManagerAI
from toontown.coghq import CountryClubManagerAI
from toontown.ai.FishManagerAI import FishManagerAI
from toontown.fishing.DistributedFishingPondAI import DistributedFishingPondAI
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from toontown.uberdog.DistributedPartyManagerAI import DistributedPartyManagerAI
from toontown.racing.DistributedRacePadAI import DistributedRacePadAI
from toontown.racing.DistributedViewPadAI import DistributedViewPadAI
from toontown.racing.DistributedStartingBlockAI import DistributedStartingBlockAI, DistributedViewingBlockAI
from toontown.racing.DistributedLeaderBoardAI import DistributedLeaderBoardAI
from toontown.racing import RaceGlobals


class ToontownAIRepository(ToontownInternalRepository):

    def __init__(self, baseChannel, stateServerChannel, districtName):
        ToontownInternalRepository.__init__(
            self, baseChannel, stateServerChannel, dcSuffix='AI')

        self.districtName = districtName
        self.districtPopulation = 0

        self.notify.setInfo(True)
        self.hoods = []
        self.cogHeadquarters = []
        self.dnaStoreMap = {}
        self.dnaDataMap = {}
        self.suitPlanners = {}
        self.buildingManagers = {}

        self.zoneAllocator = UniqueIdAllocator(ToontownGlobals.DynamicZonesBegin,
            ToontownGlobals.DynamicZonesEnd)

        self.zoneDataStore = AIZoneDataStore()

        self.wantFishing = self.config.GetBool('want-fishing', True)
        self.wantHousing = self.config.GetBool('want-housing', True)
        self.wantPets = self.config.GetBool('want-pets', True)
        self.wantParties = self.config.GetBool('want-parties', True)
        self.wantCogbuildings = self.config.GetBool('want-cogbuildings', True)
        self.wantCogdominiums = self.config.GetBool('want-cogdominiums', True)
        self.doLiveUpdates = self.config.GetBool('want-live-updates', False)
        self.wantTrackClsends = self.config.GetBool('want-track-clsends', False)
        self.wantAchievements = self.config.GetBool('want-achievements', True)
        self.baseXpMultiplier = self.config.GetFloat('base-xp-multiplier', 1.0)
        self.wantHalloween = self.config.GetBool('want-halloween', False)
        self.wantChristmas = self.config.GetBool('want-christmas', False)

        self.cogSuitMessageSent = False
        
    def createManagers(self):
        self.timeManager = TimeManagerAI(self)
        self.timeManager.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)
        
        self.tutorialManager = TutorialManagerAI(self)
        self.tutorialManager.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)
        
        self.questManager = QuestManagerAI(self)
        
        self.safeZoneManager = SafeZoneManagerAI(self)
        self.safeZoneManager.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)
        
        self.trophyMgr = DistributedTrophyMgrAI(self)
        self.trophyMgr.generateWithRequired(OTP_ZONE_ID_OLD_QUIET_ZONE)
        
        self.holidayManager = HolidayManagerAI(self)
        self.suitInvasionManager = SuitInvasionManagerAI(self)
        self.cogSuitMgr = CogSuitManagerAI.CogSuitManagerAI(self)
        self.promotionMgr = PromotionManagerAI.PromotionManagerAI(self)
        self.cogPageManager = CogPageManagerAI.CogPageManagerAI()
        self.factoryMgr = FactoryManagerAI.FactoryManagerAI(self)
        self.mintMgr = MintManagerAI.MintManagerAI(self)
        self.lawMgr = StageManagerAI.StageManagerAI(self)
        self.countryClubMgr = CountryClubManagerAI.CountryClubManagerAI(self)
        
        self.fishManager = FishManagerAI()

        self.magicWordManager = None
        self.newsManager = None
        self.friendManager = None
        self.banManager = None
        self.achievementsManager = None
        self.bankManager = None
        if self.wantFishing:
            self.fishManager = None
        if self.wantHousing:
            self.estateManager = None
            
    def createZones(self):
        self.zoneTable = {
                          2000: ((2000, 1, 0), (2100, 1, 1), (2200, 1, 1), (2300, 1, 1)),
                          1000: ((1000, 1, 0), (1100, 1, 1), (1200, 1, 1), (1300, 1, 1)),
                          3000: ((3000, 1, 0), (3100, 1, 1), (3200, 1, 1), (3300, 1, 1)),
                          4000: ((4000, 1, 0), (4100, 1, 1), (4200, 1, 1), (4300, 1, 1)),
                          5000: ((5000, 1, 0), (5100, 1, 1), (5200, 1, 1), (5300, 1, 1)),
                          9000: ((9000, 1, 0), (9100, 1, 1), (9200, 1, 1)),
                          
                          6000: (),
                          8000: ((8000, 1, 0),),
                          17000: (),
                          
                          10000: (),
                          11000: (),
                          12000: (),
                          13000: ()
                         }
                         
        for x in self.zoneTable.values():
            for zone in x:
                if zone[1]:
                    self.getStorage(zone[0])
    
    def getStorage(self, zone):
        s = self.dnaStoreMap.get(zone)
        if not s:
            s = DNAStorage()
            loadDNAFileAI(s, self.genDNAFileName(zone), CSDefault)
            self.dnaStoreMap[zone] = s
        
        return s
        
    def loadDNAFileAI(self, a, b):
        return loadDNAFileAI(a, b, CSDefault)
        
    def genDNAFileName(self, zoneId):
        zoneId = ZoneUtil.getCanonicalZoneId(zoneId)
        hoodId = ZoneUtil.getCanonicalHoodId(zoneId)
        hood = ToontownGlobals.dnaMap[hoodId]
        if hoodId == zoneId:
            zoneId = 'sz'
            phase = ToontownGlobals.phaseMap[hoodId]
        else:
            phase = ToontownGlobals.streetPhaseMap[hoodId]

        return 'phase_%s/dna/%s_%s.dna' % (phase, hood, zoneId)
        
    def createHood(self, hoodCtr, zoneId):
        if zoneId != ToontownGlobals.BossbotHQ:
            self.dnaStoreMap[zoneId] = DNAStorage()
            self.dnaDataMap[zoneId] = self.loadDNAFileAI(self.dnaStoreMap[zoneId], self.genDNAFileName(zoneId))
            if zoneId in ToontownGlobals.HoodHierarchy:
                for streetId in ToontownGlobals.HoodHierarchy[zoneId]:
                    self.dnaStoreMap[streetId] = DNAStorage()
                    self.dnaDataMap[streetId] = self.loadDNAFileAI(self.dnaStoreMap[streetId], self.genDNAFileName(streetId))

        hood = hoodCtr(self, zoneId)
        hood.startup()
        self.hoods.append(hood)

    def createSafeZones(self):
        NPCToons.generateZone2NpcDict()

        self.createHood(TTHoodDataAI.TTHoodDataAI, ToontownGlobals.ToontownCentral)
        
        self.createHood(GSHoodDataAI.GSHoodDataAI, ToontownGlobals.GoofySpeedway)

        self.createHood(DDHoodDataAI.DDHoodDataAI, ToontownGlobals.DonaldsDock)

        self.createHood(DGHoodDataAI.DGHoodDataAI, ToontownGlobals.DaisyGardens)

        self.createHood(MMHoodDataAI.MMHoodDataAI, ToontownGlobals.MinniesMelodyland)

        self.createHood(BRHoodDataAI.BRHoodDataAI, ToontownGlobals.TheBrrrgh)

        self.createHood(DLHoodDataAI.DLHoodDataAI, ToontownGlobals.DonaldsDreamland)

    def createCogHeadquarters(self):
        self.createHood(CSHoodDataAI.CSHoodDataAI, ToontownGlobals.SellbotHQ)

        self.createHood(CashbotHQDataAI.CashbotHQDataAI, ToontownGlobals.CashbotHQ)

        self.createHood(LawbotHQDataAI.LawbotHQDataAI, ToontownGlobals.LawbotHQ)

        self.createHood(BossbotHQDataAI.BossbotHQDataAI, ToontownGlobals.BossbotHQ)

    def sendSetZone(self, obj, zoneId):
        obj.b_setLocation(obj.parentId, zoneId)

    def handleConnected(self):
        self.districtId = self.allocateChannel()

        # register the AI on the state server...
        dg = PyDatagram()
        dg.addServerHeader(self.serverId, self.ourChannel, STATESERVER_ADD_SHARD)
        dg.addUint32(self.districtId)
        dg.addString(self.districtName)
        dg.addUint32(self.districtPopulation)
        self.send(dg)

        # add a post remove to remove the shard from the state server
        # when we disconnect from the message director...
        dg = PyDatagram()
        dg.addServerHeader(self.serverId, self.ourChannel, STATESERVER_REMOVE_SHARD)
        self.addPostRemove(dg)               
                 
        self.distributedDistrict = ToontownDistrictAI(self)
        self.distributedDistrict.setName(self.districtName)
        self.distributedDistrict.generateWithRequiredAndId(self.districtId, self.getGameDoId(), 3)
        
        datagram = PyDatagram()
        datagram.addServerHeader(self.districtId, self.ourChannel, STATESERVER_OBJECT_SET_AI)
        datagram.addChannel(self.ourChannel)
        self.send(datagram)
        
        self.createZones()

        self.notify.info('Creating managers...')
        self.createManagers()
        
        if self.config.GetBool('want-safe-zones', True):
            self.notify.info('Creating safe zones...')
            self.createSafeZones()
            
        if self.config.GetBool('want-cog-headquarters', True):
            self.notify.info('Creating Cog headquarters...')
            self.createCogHeadquarters()
        
        self.distributedDistrict.b_setAvailable(1)

        self.notify.info('Done.')
        
    def sendShardInfo(self):
        dg = PyDatagram()
        dg.addServerHeader(self.serverId, self.ourChannel, STATESERVER_UPDATE_SHARD)
        dg.addString(self.districtName)
        dg.addUint32(self.districtPopulation)
        self.send(dg)
        
    def incrementPopulation(self):
        self.districtPopulation += 1
        self.sendShardInfo()

    def decrementPopulation(self):
        self.districtPopulation -= 1
        self.sendShardInfo()

    def allocateZone(self):
        return self.zoneAllocator.allocate()

    def deallocateZone(self, zone):
        self.zoneAllocator.free(zone)

    def getZoneDataStore(self):
        return self.zoneDataStore

    def getTrackClsends(self):
        return self.wantTrackClsends

    def getAvatarExitEvent(self, avId):
        return 'distObjDelete-%d' % avId

    def trueUniqueName(self, name):
        return self.uniqueName(name)

    def findFishingPonds(self, dnaData, zoneId, area):
        fishingPonds = []
        fishingPondGroups = []
        if isinstance(dnaData, DNAGroup) and 'fishing_pond' in dnaData.getName():
            fishingPondGroups.append(dnaData)
            fishingPond = DistributedFishingPondAI(simbase.air)
            fishingPond.setArea(area)
            fishingPond.generateWithRequired(zoneId)
            fishingPonds.append(fishingPond)
        else:
            if isinstance(dnaData, DNAVisGroup):
                zoneId = ZoneUtil.getTrueZoneId(int(dnaData.getName().split(':')[0]), zoneId)
        for i in xrange(dnaData.getNumChildren()):
            foundFishingPonds, foundFishingPondGroups = self.findFishingPonds(dnaData.at(i), zoneId, area)
            fishingPonds.extend(foundFishingPonds)
            fishingPondGroups.extend(foundFishingPondGroups)

        return (fishingPonds, fishingPondGroups)

    def findFishingSpots(self, dnaData, fishingPond):
        fishingSpots = []
        if isinstance(dnaData, DNAGroup) and dnaData.getName()[:13] == 'fishing_spot_':
            zoneId = fishingPond.zoneId
            doId = fishingPond.doId
            fishingSpot = DistributedFishingSpotAI(simbase.air)
            fishingSpot.setPondDoId(doId)
            x, y, z = dnaData.getPos()
            h, p, r = dnaData.getHpr()
            fishingSpot.setPosHpr(x, y, z, h, p, r)
            fishingSpot.generateWithRequired(zoneId)
            fishingSpots.append(fishingSpot)
        for i in xrange(dnaData.getNumChildren()):
            foundFishingSpots = self.findFishingSpots(dnaData.at(i), fishingPond)
            fishingSpots.extend(foundFishingSpots)

        return fishingSpots

    def findRacingPads(self, dnaData, zoneId, area, type = 'racing_pad', overrideDNAZone = False):
        racingPads, racingPadGroups = [], []
        if type in dnaData.getName():
            if type == 'racing_pad':
                nameSplit = dnaData.getName().split('_')
                racePad = DistributedRacePadAI(self)
                racePad.setArea(area)
                racePad.index = int(nameSplit[2])
                racePad.genre = nameSplit[3]
                trackInfo = RaceGlobals.getNextRaceInfo(-1, racePad.genre, racePad.index)
                racePad.setTrackInfo([trackInfo[0], trackInfo[1]])
                racePad.laps = trackInfo[2]
                racePad.generateWithRequired(zoneId)
                racingPads.append(racePad)
                racingPadGroups.append(dnaData)
            elif type == 'viewing_pad':
                viewPad = DistributedViewPadAI(self)
                viewPad.setArea(area)
                viewPad.generateWithRequired(zoneId)
                racingPads.append(viewPad)
                racingPadGroups.append(dnaData)
        for i in xrange(dnaData.getNumChildren()):
            foundRacingPads, foundRacingPadGroups = self.findRacingPads(dnaData.at(i), zoneId, area, type, overrideDNAZone)
            racingPads.extend(foundRacingPads)
            racingPadGroups.extend(foundRacingPadGroups)

        return (racingPads, racingPadGroups)

    def findStartingBlocks(self, dnaData, pad):
        startingBlocks = []
        for i in xrange(dnaData.getNumChildren()):
            groupName = dnaData.getName()
            blockName = dnaData.at(i).getName()
            if 'starting_block' in blockName:
                cls = DistributedStartingBlockAI if 'racing_pad' in groupName else DistributedViewingBlockAI
                x, y, z = dnaData.at(i).getPos()
                h, p, r = dnaData.at(i).getHpr()
                padLocationId = int(dnaData.at(i).getName()[(-1)])
                startingBlock = cls(self, pad, x, y, z, h, p, r, padLocationId)
                startingBlock.generateWithRequired(pad.zoneId)
                startingBlocks.append(startingBlock)

        return startingBlocks

    def findLeaderBoards(self, dnaData, zoneId):
        leaderboards = []
        if 'leaderBoard' in dnaData.getName():
            x, y, z = dnaData.getPos()
            h, p, r = dnaData.getHpr()
            leaderboard = DistributedLeaderBoardAI(self, dnaData.getName(), x, y, z, h, p, r)
            leaderboard.generateWithRequired(zoneId)
            leaderboards.append(leaderboard)
        for i in xrange(dnaData.getNumChildren()):
            foundLeaderBoards = self.findLeaderBoards(dnaData.at(i), zoneId)
            leaderboards.extend(foundLeaderBoards)

        return leaderboards

    def findPartyHats(self, dnaData, zoneId):
        return []