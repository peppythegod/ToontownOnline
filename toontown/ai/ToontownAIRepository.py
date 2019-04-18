from direct.distributed.PyDatagram import *
from pandac.PandaModules import *
from toontown.ai.MessageTypes import *
"""
from otp.ai.AIZoneData import AIZoneDataStore
from otp.ai.MagicWordManagerAI import MagicWordManagerAI
from otp.ai.TimeManagerAI import TimeManagerAI
from otp.ai import BanManagerAI
from otp.distributed.OtpDoGlobals import *
from otp.friends.FriendManagerAI import FriendManagerAI
from toontown.ai import CogPageManagerAI
from toontown.ai import CogSuitManagerAI
from toontown.ai import PromotionManagerAI
from toontown.ai.AchievementsManagerAI import AchievementsManagerAI
from toontown.ai.FishManagerAI import  FishManagerAI
from toontown.ai.HolidayManagerAI import HolidayManagerAI
from toontown.ai.NewsManagerAI import NewsManagerAI
from toontown.ai.QuestManagerAI import QuestManagerAI
from toontown.ai import BankManagerAI
from toontown.building.DistributedTrophyMgrAI import DistributedTrophyMgrAI
from toontown.catalog.CatalogManagerAI import CatalogManagerAI
from toontown.catalog.PopularItemManagerAI import PopularItemManagerAI
from toontown.coghq import CountryClubManagerAI
from toontown.coghq import FactoryManagerAI
from toontown.coghq import LawOfficeManagerAI
from toontown.coghq import MintManagerAI
"""
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.distributed.ToontownDistrictAI import ToontownDistrictAI
from toontown.distributed.ToontownDistrictStatsAI import ToontownDistrictStatsAI
from toontown.distributed.ToontownInternalRepository import ToontownInternalRepository
from toontown.toonbase import ToontownGlobals
"""
from toontown.dna.DNAParser import loadDNAFileAI
from toontown.estate.EstateManagerAI import EstateManagerAI
from toontown.hood import BRHoodAI
from toontown.hood import BossbotHQAI
from toontown.hood import CashbotHQAI
from toontown.hood import DDHoodAI
from toontown.hood import DGHoodAI
from toontown.hood import DLHoodAI
from toontown.hood import GSHoodAI
from toontown.hood import GZHoodAI
from toontown.hood import LawbotHQAI
from toontown.hood import MMHoodAI
from toontown.hood import OZHoodAI
from toontown.hood import SellbotHQAI
from toontown.hood import TTHoodAI
from toontown.hood import ZoneUtil
from toontown.pets.PetManagerAI import PetManagerAI
from toontown.safezone.SafeZoneManagerAI import SafeZoneManagerAI
from toontown.suit.SuitInvasionManagerAI import SuitInvasionManagerAI
from toontown.toon import NPCToons
from toontown.tutorial.TutorialManagerAI import TutorialManagerAI
from toontown.uberdog.DistributedPartyManagerAI import DistributedPartyManagerAI
"""


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
        self.factoryMgr = None
        self.mintMgr = None
        self.lawOfficeMgr = None
        self.countryClubMgr = None

        self.zoneAllocator = UniqueIdAllocator(ToontownGlobals.DynamicZonesBegin,
            ToontownGlobals.DynamicZonesEnd)

        #self.zoneDataStore = AIZoneDataStore()

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
                                  
        self.rootObj = DistributedObjectAI(self)
        self.rootObj.generateWithRequiredAndId(self.districtId, 0, 0)
        

        """
        self.notify.info('Creating managers...')
        self.createManagers()

        if self.config.GetBool('want-safe-zones', True):
            self.notify.info('Creating safe zones...')
            self.createSafeZones()

        if self.config.GetBool('want-cog-headquarters', True):
            self.notify.info('Creating Cog headquarters...')
            self.createCogHeadquarters()
        """

        self.notify.info('Done.')