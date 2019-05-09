from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.coghq import DistributedCashbotBossCraneAI
from toontown.coghq import DistributedCashbotBossSafeAI
from toontown.suit import DistributedCashbotBossGoonAI
from toontown.coghq import DistributedCashbotBossTreasureAI
from toontown.battle import BattleExperienceAI
from toontown.chat import ResistanceChat
from direct.fsm import FSM
import DistributedBossCogAI
import SuitDNA
import random
import math


class DistributedCashbotBossAI(DistributedBossCogAI.DistributedBossCogAI,
                               FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedCashbotBossAI')
    maxGoons = 8

    def __init__(self, air):
        DistributedBossCogAI.DistributedBossCogAI.__init__(self, air, 'm')
        FSM.FSM.__init__(self, 'DistributedCashbotBossAI')
        self.cranes = None
        self.safes = None
        self.goons = None
        self.treasures = {}
        self.grabbingTreasures = {}
        self.recycledTreasures = []
        self.healAmount = 0
        self.rewardId = ResistanceChat.getRandomId()
        self.rewardedToons = []
        self.scene = NodePath('scene')
        self.reparentTo(self.scene)
        cn = CollisionNode('walls')
        cs = CollisionSphere(0, 0, 0, 13)
        cn.addSolid(cs)
        cs = CollisionInvSphere(0, 0, 0, 42)
        cn.addSolid(cs)
        self.attachNewNode(cn)
        self.heldObject = None
        self.waitingForHelmet = 0
        self.avatarHelmets = {}
        self.bossMaxDamage = ToontownGlobals.CashbotBossMaxDamage

    def generate(self):
        DistributedBossCogAI.DistributedBossCogAI.generate(self)
        if __dev__:
            self.scene.reparentTo(self.getRender())

    def getHoodId(self):
        return ToontownGlobals.CashbotHQ

    def formatReward(self):
        return str(self.rewardId)

    def makeBattleOneBattles(self):
        self.postBattleState = 'PrepareBattleThree'
        self.initializeBattles(1, ToontownGlobals.CashbotBossBattleOnePosHpr)

    def generateSuits(self, battleNumber):
        cogs = self.invokeSuitPlanner(11, 0)
        skelecogs = self.invokeSuitPlanner(12, 1)
        activeSuits = cogs['activeSuits'] + skelecogs['activeSuits']
        reserveSuits = cogs['reserveSuits'] + skelecogs['reserveSuits']
        random.shuffle(activeSuits)
        while len(activeSuits) > 4:
            suit = activeSuits.pop()
            reserveSuits.append((suit, 100))

        def compareJoinChance(a, b):
            return cmp(a[1], b[1])

        reserveSuits.sort(compareJoinChance)
        return {'activeSuits': activeSuits, 'reserveSuits': reserveSuits}

    def removeToon(self, avId):
        if self.cranes is not None:
            for crane in self.cranes:
                crane.removeToon(avId)

        if self.safes is not None:
            for safe in self.safes:
                safe.removeToon(avId)

        if self.goons is not None:
            for goon in self.goons:
                goon.removeToon(avId)

        DistributedBossCogAI.DistributedBossCogAI.removeToon(self, avId)

    def _DistributedCashbotBossAI__makeBattleThreeObjects(self):
        if self.cranes is None:
            self.cranes = []
            for index in range(len(ToontownGlobals.CashbotBossCranePosHprs)):
                crane = DistributedCashbotBossCraneAI.DistributedCashbotBossCraneAI(
                    self.air, self, index)
                crane.generateWithRequired(self.zoneId)
                print "crane id %d" %crane.doId
                self.cranes.append(crane)

        if self.safes is None:
            self.safes = []
            for index in range(len(ToontownGlobals.CashbotBossSafePosHprs)):
                safe = DistributedCashbotBossSafeAI.DistributedCashbotBossSafeAI(
                    self.air, self, index)
                safe.generateWithRequired(self.zoneId)
                self.safes.append(safe)

        if self.goons is None:
            self.goons = []

    def _DistributedCashbotBossAI__resetBattleThreeObjects(self):
        if self.cranes is not None:
            for crane in self.cranes:
                crane.request('Free')

        if self.safes is not None:
            for safe in self.safes:
                safe.request('Initial')

    def _DistributedCashbotBossAI__deleteBattleThreeObjects(self):
        if self.cranes is not None:
            for crane in self.cranes:
                crane.request('Off')
                crane.requestDelete()

            self.cranes = None

        if self.safes is not None:
            for safe in self.safes:
                safe.request('Off')
                safe.requestDelete()

            self.safes = None

        if self.goons is not None:
            for goon in self.goons:
                goon.request('Off')
                goon.requestDelete()

            self.goons = None

    def doNextAttack(self, task):
        self._DistributedCashbotBossAI__doDirectedAttack()
        if self.heldObject is None and not (self.waitingForHelmet):
            self.waitForNextHelmet()

    def _DistributedCashbotBossAI__doDirectedAttack(self):
        if self.toonsToAttack:
            toonId = self.toonsToAttack.pop(0)
            while toonId not in self.involvedToons:
                if not self.toonsToAttack:
                    self.b_setAttackCode(ToontownGlobals.BossCogNoAttack)
                    return None

                toonId = self.toonsToAttack.pop(0)
            self.toonsToAttack.append(toonId)
            self.b_setAttackCode(ToontownGlobals.BossCogSlowDirectedAttack,
                                 toonId)

    def reprieveToon(self, avId):
        if avId in self.toonsToAttack:
            i = self.toonsToAttack.index(avId)
            del self.toonsToAttack[i]
            self.toonsToAttack.append(avId)

    def makeTreasure(self, goon):
        if self.state != 'BattleThree':
            return None

        pos = goon.getPos(self)
        v = Vec3(pos[0], pos[1], 0.0)
        if not v.normalize():
            v = Vec3(1, 0, 0)

        v = v * 27
        angle = random.uniform(0.0, 2.0 * math.pi)
        radius = 10
        dx = radius * math.cos(angle)
        dy = radius * math.sin(angle)
        fpos = self.scene.getRelativePoint(self, Point3(
            v[0] + dx, v[1] + dy, 0))
        if goon.strength <= 10:
            style = ToontownGlobals.ToontownCentral
            healAmount = 3
        elif goon.strength <= 15:
            style = random.choice([
                ToontownGlobals.DonaldsDock, ToontownGlobals.DaisyGardens,
                ToontownGlobals.MinniesMelodyland
            ])
            healAmount = 10
        else:
            style = random.choice(
                [ToontownGlobals.TheBrrrgh, ToontownGlobals.DonaldsDreamland])
            healAmount = 12
        if self.recycledTreasures:
            treasure = self.recycledTreasures.pop(0)
            treasure.d_setGrab(0)
            treasure.b_setGoonId(goon.doId)
            treasure.b_setStyle(style)
            treasure.b_setPosition(pos[0], pos[1], 0)
            treasure.b_setFinalPosition(fpos[0], fpos[1], 0)
        else:
            treasure = DistributedCashbotBossTreasureAI.DistributedCashbotBossTreasureAI(
                self.air, self, goon, style, fpos[0], fpos[1], 0)
            treasure.generateWithRequired(self.zoneId)
        treasure.healAmount = healAmount
        self.treasures[treasure.doId] = treasure

    def grabAttempt(self, avId, treasureId):
        av = self.air.doId2do.get(avId)
        if not av:
            return None

        treasure = self.treasures.get(treasureId)
        if treasure:
            if treasure.validAvatar(av):
                del self.treasures[treasureId]
                treasure.d_setGrab(avId)
                self.grabbingTreasures[treasureId] = treasure
                taskMgr.doMethodLater(
                    5,
                    self._DistributedCashbotBossAI__recycleTreasure,
                    treasure.uniqueName('recycleTreasure'),
                    extraArgs=[treasure])
            else:
                treasure.d_setReject()

    def _DistributedCashbotBossAI__recycleTreasure(self, treasure):
        if treasure.doId in self.grabbingTreasures:
            del self.grabbingTreasures[treasure.doId]
            self.recycledTreasures.append(treasure)

    def deleteAllTreasures(self):
        for treasure in self.treasures.values():
            treasure.requestDelete()

        self.treasures = {}
        for treasure in self.grabbingTreasures.values():
            taskMgr.remove(treasure.uniqueName('recycleTreasure'))
            treasure.requestDelete()

        self.grabbingTreasures = {}
        for treasure in self.recycledTreasures:
            treasure.requestDelete()

        self.recycledTreasures = []

    def getMaxGoons(self):
        t = self.getBattleThreeTime()
        if t <= 1.0:
            return self.maxGoons
        elif t <= 1.1000000000000001:
            return self.maxGoons + 1
        elif t <= 1.2:
            return self.maxGoons + 2
        elif t <= 1.3:
            return self.maxGoons + 3
        elif t <= 1.3999999999999999:
            return self.maxGoons + 4
        else:
            return self.maxGoons + 8

    def makeGoon(self, side=None):
        if side is None:
            side = random.choice(['EmergeA', 'EmergeB'])

        goon = self._DistributedCashbotBossAI__chooseOldGoon()
        if goon is None:
            if len(self.goons) >= self.getMaxGoons():
                return None

            goon = DistributedCashbotBossGoonAI.DistributedCashbotBossGoonAI(
                self.air, self)
            goon.generateWithRequired(self.zoneId)
            self.goons.append(goon)

        if self.getBattleThreeTime() > 1.0:
            goon.STUN_TIME = 4
            goon.b_setupGoon(
                velocity=8, hFov=90, attackRadius=20, strength=30, scale=1.8)
        else:
            goon.STUN_TIME = self.progressValue(30, 8)
            goon.b_setupGoon(
                velocity=self.progressRandomValue(3, 7),
                hFov=self.progressRandomValue(70, 80),
                attackRadius=self.progressRandomValue(6, 15),
                strength=int(self.progressRandomValue(5, 25)),
                scale=self.progressRandomValue(0.5, 1.5))
        goon.request(side)

    def _DistributedCashbotBossAI__chooseOldGoon(self):
        for goon in self.goons:
            if goon.state == 'Off':
                return goon
                continue

    def waitForNextGoon(self, delayTime):
        currState = self.getCurrentOrNextState()
        if currState == 'BattleThree':
            taskName = self.uniqueName('NextGoon')
            taskMgr.remove(taskName)
            taskMgr.doMethodLater(delayTime, self.doNextGoon, taskName)

    def stopGoons(self):
        taskName = self.uniqueName('NextGoon')
        taskMgr.remove(taskName)

    def doNextGoon(self, task):
        if self.attackCode != ToontownGlobals.BossCogDizzy:
            self.makeGoon()

        delayTime = self.progressValue(10, 2)
        self.waitForNextGoon(delayTime)

    def waitForNextHelmet(self):
        currState = self.getCurrentOrNextState()
        if currState == 'BattleThree':
            taskName = self.uniqueName('NextHelmet')
            taskMgr.remove(taskName)
            delayTime = self.progressValue(45, 15)
            taskMgr.doMethodLater(
                delayTime, self._DistributedCashbotBossAI__donHelmet, taskName)
            self.waitingForHelmet = 1

    def _DistributedCashbotBossAI__donHelmet(self, task):
        self.waitingForHelmet = 0
        if self.heldObject is None:
            safe = self.safes[0]
            safe.request('Grabbed', self.doId, self.doId)
            self.heldObject = safe

    def stopHelmets(self):
        self.waitingForHelmet = 0
        taskName = self.uniqueName('NextHelmet')
        taskMgr.remove(taskName)

    def acceptHelmetFrom(self, avId):
        now = globalClock.getFrameTime()
        then = self.avatarHelmets.get(avId, None)
        if then is None or now - then > 300:
            self.avatarHelmets[avId] = now
            return 1

        return 0

    def magicWordHit(self, damage, avId):
        if self.heldObject:
            self.heldObject.demand('Dropped', avId, self.doId)
            self.heldObject.avoidHelmet = 1
            self.heldObject = None
            self.waitForNextHelmet()
        else:
            self.recordHit(damage)

    def magicWordReset(self):
        if self.state == 'BattleThree':
            self._DistributedCashbotBossAI__resetBattleThreeObjects()

    def magicWordResetGoons(self):
        if self.state == 'BattleThree':
            if self.goons is not None:
                for goon in self.goons:
                    goon.request('Off')
                    goon.requestDelete()

                self.goons = None

            self._DistributedCashbotBossAI__makeBattleThreeObjects()

    def recordHit(self, damage):
        avId = self.air.getAvatarIdFromSender()
        if not self.validate(avId, avId in self.involvedToons,
                             'recordHit from unknown avatar'):
            return None

        if self.state != 'BattleThree':
            return None

        self.b_setBossDamage(self.bossDamage + damage)
        if self.bossDamage >= self.bossMaxDamage:
            self.b_setState('Victory')
        elif self.attackCode != ToontownGlobals.BossCogDizzy:
            if damage >= ToontownGlobals.CashbotBossKnockoutDamage:
                self.b_setAttackCode(ToontownGlobals.BossCogDizzy)
                self.stopHelmets()
            else:
                self.b_setAttackCode(ToontownGlobals.BossCogNoAttack)
                self.stopHelmets()
                self.waitForNextHelmet()

    def b_setBossDamage(self, bossDamage):
        self.d_setBossDamage(bossDamage)
        self.setBossDamage(bossDamage)

    def setBossDamage(self, bossDamage):
        self.reportToonHealth()
        self.bossDamage = bossDamage

    def d_setBossDamage(self, bossDamage):
        self.sendUpdate('setBossDamage', [bossDamage])

    def d_setRewardId(self, rewardId):
        self.sendUpdate('setRewardId', [rewardId])

    def applyReward(self):
        avId = self.air.getAvatarIdFromSender()
        if avId in self.involvedToons and avId not in self.rewardedToons:
            self.rewardedToons.append(avId)
            toon = self.air.doId2do.get(avId)
            if toon:
                toon.doResistanceEffect(self.rewardId)

    def enterOff(self):
        DistributedBossCogAI.DistributedBossCogAI.enterOff(self)
        self.rewardedToons = []

    def exitOff(self):
        DistributedBossCogAI.DistributedBossCogAI.exitOff(self)

    def enterIntroduction(self):
        DistributedBossCogAI.DistributedBossCogAI.enterIntroduction(self)
        self._DistributedCashbotBossAI__makeBattleThreeObjects()
        self._DistributedCashbotBossAI__resetBattleThreeObjects()

    def exitIntroduction(self):
        DistributedBossCogAI.DistributedBossCogAI.exitIntroduction(self)
        self._DistributedCashbotBossAI__deleteBattleThreeObjects()

    def enterPrepareBattleThree(self):
        self.resetBattles()
        self._DistributedCashbotBossAI__makeBattleThreeObjects()
        self._DistributedCashbotBossAI__resetBattleThreeObjects()
        self.barrier = self.beginBarrier(
            'PrepareBattleThree', self.involvedToons, 55,
            self._DistributedCashbotBossAI__donePrepareBattleThree)

    def _DistributedCashbotBossAI__donePrepareBattleThree(self, avIds):
        self.b_setState('BattleThree')

    def exitPrepareBattleThree(self):
        if self.newState != 'BattleThree':
            self._DistributedCashbotBossAI__deleteBattleThreeObjects()

        self.ignoreBarrier(self.barrier)

    def enterBattleThree(self):
        self.setPosHpr(*ToontownGlobals.CashbotBossBattleThreePosHpr)
        self._DistributedCashbotBossAI__makeBattleThreeObjects()
        self._DistributedCashbotBossAI__resetBattleThreeObjects()
        self.reportToonHealth()
        self.toonsToAttack = self.involvedToons[:]
        random.shuffle(self.toonsToAttack)
        self.b_setBossDamage(0)
        self.battleThreeStart = globalClock.getFrameTime()
        self.resetBattles()
        self.waitForNextAttack(15)
        self.waitForNextHelmet()
        self.makeGoon(side='EmergeA')
        self.makeGoon(side='EmergeB')
        taskName = self.uniqueName('NextGoon')
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(
            2, self._DistributedCashbotBossAI__doInitialGoons, taskName)

    def _DistributedCashbotBossAI__doInitialGoons(self, task):
        self.makeGoon(side='EmergeA')
        self.makeGoon(side='EmergeB')
        self.waitForNextGoon(10)

    def exitBattleThree(self):
        helmetName = self.uniqueName('helmet')
        taskMgr.remove(helmetName)
        if self.newState != 'Victory':
            self._DistributedCashbotBossAI__deleteBattleThreeObjects()

        self.deleteAllTreasures()
        self.stopAttacks()
        self.stopGoons()
        self.stopHelmets()
        self.heldObject = None

    def enterVictory(self):
        self.resetBattles()
        self.suitsKilled.append({
            'type': None,
            'level': None,
            'track': self.dna.dept,
            'isSkelecog': 0,
            'isForeman': 0,
            'isVP': 0,
            'isCFO': 1,
            'isSupervisor': 0,
            'isVirtual': 0,
            'activeToons': self.involvedToons[:]
        })
        self.barrier = self.beginBarrier(
            'Victory', self.involvedToons, 30,
            self._DistributedCashbotBossAI__doneVictory)

    def _DistributedCashbotBossAI__doneVictory(self, avIds):
        self.d_setBattleExperience()
        self.b_setState('Reward')
        BattleExperienceAI.assignRewards(
            self.involvedToons, self.toonSkillPtsGained, self.suitsKilled,
            ToontownGlobals.dept2cogHQ(self.dept), self.helpfulToons)
        for toonId in self.involvedToons:
            toon = self.air.doId2do.get(toonId)
            if toon:
                toon.addResistanceMessage(self.rewardId)
                toon.b_promote(self.deptIndex)
                continue

    def exitVictory(self):
        self._DistributedCashbotBossAI__deleteBattleThreeObjects()

    def enterEpilogue(self):
        DistributedBossCogAI.DistributedBossCogAI.enterEpilogue(self)
        self.d_setRewardId(self.rewardId)
