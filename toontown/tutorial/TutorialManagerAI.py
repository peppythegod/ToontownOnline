from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.building.DistributedTutorialInteriorAI import DistributedTutorialInteriorAI
from toontown.toon import NPCToons
from toontown.building import DoorTypes
from toontown.building import DistributedDoorAI
from toontown.building.DistributedBuildingAI import DistributedBuildingAI
from toontown.suit.DistributedTutorialSuitAI import DistributedTutorialSuitAI
from toontown.toonbase import ToontownBattleGlobals
from toontown.building.HQBuildingAI import HQBuildingAI
from toontown.quest import Quests
from toontown.building import FADoorCodes
from direct.fsm.FSM import FSM

from toontown.toon import Experience

class TZoneStruct:
    branch = 0
    street = 0
    shop = 0
    hq = 0


class ToontorialBuildingAI:
    def __init__(self, air, street, interior, npcId):

        self.air = air

        self.interior = DistributedTutorialInteriorAI(self.air, interior, npcId)

        self.interior.generateWithRequired(interior)
        self.door0 = DistributedDoorAI.DistributedDoorAI(self.air, 2, DoorTypes.EXT_STANDARD, doorIndex=0)
        self.insideDoor0 = DistributedDoorAI.DistributedDoorAI(self.air, 0, DoorTypes.INT_STANDARD, doorIndex=0)
        self.door0.setOtherDoor(self.insideDoor0)
        self.insideDoor0.setOtherDoor(self.door0)
        self.door0.zoneId = street
        self.insideDoor0.zoneId = interior
        self.door0.generateWithRequired(street)
        self.door0.sendUpdate('setDoorIndex', [self.door0.getDoorIndex()])
        self.insideDoor0.generateWithRequired(interior)
        self.insideDoor0.sendUpdate('setDoorIndex', [self.insideDoor0.getDoorIndex()])

    def cleanup(self):
        self.door0.requestDelete()
        self.insideDoor0.requestDelete()
        self.interior.requestDelete()


class TutorialFSM(FSM):
    def __init__(self, air, zones, avId):
        FSM.__init__(self, 'TutorialFSM')
        self.avId = avId
        self.zones = zones
        self.air = air

        npcDesc = NPCToons.NPCToonDict.get(20000)
        self.tom = NPCToons.createNPC(self.air, 20000, npcDesc, self.zones.shop, 0)
        self.tom.setTutorial(1)
        
        self.building = ToontorialBuildingAI(self.air, zones.street, zones.shop, self.tom.getDoId())

        npcDesc = NPCToons.NPCToonDict.get(20002)
        self.harry = NPCToons.createNPC(self.air, 20002, npcDesc, self.zones.hq, 0)
        self.harry.setTutorial(1)

        self.hq = HQBuildingAI(self.air, zones.street, zones.hq, 1)

        self.forceTransition('Introduction')

    def enterIntroduction(self):
        self.building.insideDoor0.setDoorLock(FADoorCodes.TALK_TO_TOM)

    def exitIntroduction(self):
        self.building.insideDoor0.setDoorLock(FADoorCodes.UNLOCKED)

    def enterBattle(self):
        self.suit = DistributedTutorialSuitAI(self.air)
        self.suit.generateWithRequired(self.zones.street)
        self.building.door0.setDoorLock(FADoorCodes.DEFEAT_FLUNKY_TOM)
        self.hq.door0.setDoorLock(FADoorCodes.DEFEAT_FLUNKY_HQ)

    def exitBattle(self):
        if self.suit:
            self.suit.requestDelete()

    def enterHQ(self):
        self.building.door0.setDoorLock(FADoorCodes.TALK_TO_HQ_TOM)
        self.hq.door0.setDoorLock(FADoorCodes.UNLOCKED)
        self.hq.insideDoor0.setDoorLock(FADoorCodes.TALK_TO_HQ)
        self.hq.insideDoor1.setDoorLock(FADoorCodes.TALK_TO_HQ)

    def enterTunnel(self):
        npcDesc = NPCToons.NPCToonDict.get(20001)
        self.flippy = NPCToons.createNPC(self.air, 20001, npcDesc, self.zones.street, 0)

        self.hq.insideDoor1.setDoorLock(FADoorCodes.UNLOCKED)
        self.hq.door1.setDoorLock(FADoorCodes.GO_TO_PLAYGROUND)
        self.hq.insideDoor0.setDoorLock(FADoorCodes.WRONG_DOOR_HQ)

    def exitTunnel(self):
        self.flippy.requestDelete()

    def enterCleanUp(self):
        #deallocate all the zones
        self.building.cleanup()
        self.hq.cleanup()
        self.tom.requestDelete()
        self.harry.requestDelete()
        self.air.deallocateZone(self.zones.branch)
        self.air.deallocateZone(self.zones.street)
        self.air.deallocateZone(self.zones.shop)
        self.air.deallocateZone(self.zones.hq)
        del self.air.tutorialManager.avId2fsm[self.avId]

class TutorialManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("TutorialManagerAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.avId2fsm = {}
        self.avId2zones = {}

    def requestTutorial(self):
        #! Skip by default for now.
        self.requestSkipTutorial()
        return
        
        avId = self.air.getAvatarIdFromSender()

        zones = TZoneStruct()
        zones.branch = self.air.allocateZone()
        zones.street = self.air.allocateZone()
        zones.shop = self.air.allocateZone()
        zones.hq = self.air.allocateZone()
        self.avId2zones[avId] = zones

        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.unexpectedExit, extraArgs=[avId])

        self.d_enterTutorial(avId, zones.street, zones.street, zones.shop, zones.hq)

    def unexpectedExit(self, avId):
        fsm = self.avId2fsm.get(avId)
        if fsm:
            fsm.demand('CleanUp')

    def rejectTutorial(self): 
        pass

    def requestSkipTutorial(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av:
            av.b_setTutorialAck(1)
            av.b_setQuestHistory([110, 100])
            av.addQuest((110, Quests.getQuestFromNpcId(110), Quests.getQuestToNpcId(110), Quests.getQuestReward(110, av), 0), 0)
            self.air.questManager.toonRodeTrolleyFirstTime(av) 
            self.d_skipTutorialResponse(avId, 1)
            
            #
            av.b_setHp(150)
            av.b_setMaxHp(150)
            
            gagTracks = [1, 0, 1, 1, 1, 1, 1]
            av.b_setTrackAccess(gagTracks)
            av.b_setMaxCarry(80)

            experience = Experience.Experience(av.getExperience(), av)
            for i, track in enumerate(av.getTrackAccess()):
                if track:
                    experience.experience[i] = (
                        Experience.MaxSkill - Experience.UberSkill)
            av.b_setExperience(experience.makeNetString())

            av.b_setMoney(10000)
            av.b_setBankMoney(10000)
            av.b_setHoodsVisited([1000, 2000, 3000, 4000, 5000, 6000, 8000, 9000, 10000, 11000, 12000, 13000])
            av.b_setTeleportAccess([1000, 2000, 3000, 4000, 5000, 6000, 8000, 9000, 10000, 11000, 12000, 13000])
        else:
            self.d_skipTutorialResponse(avId, 0)

    def d_skipTutorialResponse(self, avId, allOk):
        self.sendUpdateToAvatarId(avId, 'skipTutorialResponse', [allOk])

    def d_enterTutorial(self, avId, branchZone, streetZone, shopZone, hqZone):
        self.sendUpdateToAvatarId(avId, 'enterTutorial', [branchZone, streetZone, shopZone, hqZone])

    def allDone(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av:
            av.b_setTutorialAck(1)
        self.ignore(self.air.getAvatarExitEvent(avId))
        fsm = self.avId2fsm.get(avId)
        if fsm:
            fsm.demand('CleanUp')
        else:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Attempted to exit a non-existent tutorial.')

    def toonArrived(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av:
            return
        if av.getTutorialAck():
            self.avId2fsm[avId].demand('CleanUp')
            self.air.writeServerEvent('suspicious', avId=avId, issue='Attempted to request Toontorial when it would be impossible to do so')
            return

        zones = self.avId2zones[avId]
        self.avId2fsm[avId] = TutorialFSM(self.air, zones, avId)

        # Reset Toon to be appropriate for the tutorial:
        av.b_setQuests([])
        av.b_setQuestHistory([])
        av.b_setRewardHistory(0, [])
        av.b_setHp(15)
        av.b_setMaxHp(15)

        av.inventory.zeroInv()
        if av.inventory.numItem(ToontownBattleGlobals.THROW_TRACK, 0) == 0:
            av.inventory.addItem(ToontownBattleGlobals.THROW_TRACK, 0)
        if av.inventory.numItem(ToontownBattleGlobals.SQUIRT_TRACK, 0) == 0:
            av.inventory.addItem(ToontownBattleGlobals.SQUIRT_TRACK, 0)
        av.d_setInventory(av.inventory.makeNetString())

        av.experience.zeroOutExp()
        av.d_setExperience(av.experience.makeNetString())