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
    MMHoodDataAI, BRHoodDataAI, DLHoodDataAI, CSHoodDataAI, CashbotHQDataAI, LawbotHQDataAI, BossbotHQDataAI
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
        self.wantYinYang = self.config.GetBool('want-yin-yang', False)
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
            loadDNAFileAI(s, self.genDNAFileName(zone))
            self.dnaStoreMap[zone] = s
        
        return s
        
    def genDNAFileName(self, zoneId):
        zoneId = ZoneUtil.getCanonicalZoneId(zoneId)
        hoodId = ZoneUtil.getCanonicalHoodId(zoneId)
        hood = ToontownGlobals.dnaMap[hoodId]
        if hoodId == zoneId:
            zoneId = 'sz'
            phase = ToontownGlobals.phaseMap[hoodId]
        else:
            phase = ToontownGlobals.streetPhaseMap[hoodId]

        return 'phase_%s/dna/%s_%s.pdna' % (phase, hood, zoneId)
        
    def createSafeZones(self):
        NPCToons.generateZone2NpcDict()
        tt_hood = TTHoodDataAI.TTHoodDataAI(self)
        tt_hood.startup()
        
        dd_hood = DDHoodDataAI.DDHoodDataAI(self)
        dd_hood.startup()
        
        oz_hood = OZHoodDataAI.OZHoodDataAI(self)
        oz_hood.startup()
        
        gz_hood = GZHoodDataAI.GZHoodDataAI(self)
        gz_hood.startup()
        
        dg_hood = DGHoodDataAI.DGHoodDataAI(self)
        dg_hood.startup()
        
        mm_hood = MMHoodDataAI.MMHoodDataAI(self)
        mm_hood.startup()
        
        br_hood = BRHoodDataAI.BRHoodDataAI(self)
        br_hood.startup()
        
        dl_hood = DLHoodDataAI.DLHoodDataAI(self)
        dl_hood.startup()
        
    def createCogHeadquarters(self):
        sb_hq = CSHoodDataAI.CSHoodDataAI(self)
        sb_hq.startup()
        
        cb_hq = CashbotHQDataAI.CashbotHQDataAI(self)
        cb_hq.startup()
        
        lb_hq = LawbotHQDataAI.LawbotHQDataAI(self)
        lb_hq.startup()
        
        bb_hq = BossbotHQDataAI.BossbotHQDataAI(self)
        bb_hq.startup()

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