from otp.ai.AIBase import *
from direct.distributed.ClockDelta import *
from BattleBase import *
from BattleCalculatorAI import *
from toontown.toonbase.ToontownBattleGlobals import *
from SuitBattleGlobals import *
from pandac.PandaModules import *
import BattleExperienceAI
from direct.distributed import DistributedObjectAI
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
from direct.directnotify import DirectNotifyGlobal
from toontown.ai import DatabaseObject
from toontown.toon import DistributedToonAI
from toontown.toon import InventoryBase
from toontown.toonbase import ToontownGlobals
import random
from toontown.toon import NPCToons


class DistributedBattleBaseAI(DistributedObjectAI.DistributedObjectAI,
                              BattleBase):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedBattleBaseAI')

    def __init__(self,
                 air,
                 zoneId,
                 finishCallback=None,
                 maxSuits=4,
                 bossBattle=0,
                 tutorialFlag=0,
                 interactivePropTrackBonus=-1):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.serialNum = 0
        self.zoneId = zoneId
        self.maxSuits = maxSuits
        self.setBossBattle(bossBattle)
        self.tutorialFlag = tutorialFlag
        self.interactivePropTrackBonus = interactivePropTrackBonus
        self.finishCallback = finishCallback
        self.avatarExitEvents = []
        self.responses = {}
        self.adjustingResponses = {}
        self.joinResponses = {}
        self.adjustingSuits = []
        self.adjustingToons = []
        self.numSuitsEver = 0
        BattleBase.__init__(self)
        self.streetBattle = 1
        self.pos = Point3(0, 0, 0)
        self.initialSuitPos = Point3(0, 0, 0)
        self.toonExp = {}
        self.toonOrigQuests = {}
        self.toonItems = {}
        self.toonOrigMerits = {}
        self.toonMerits = {}
        self.toonParts = {}
        self.battleCalc = BattleCalculatorAI(self, tutorialFlag)
        if self.air.suitInvasionManager.getInvading():
            mult = getInvasionMultiplier()
            self.battleCalc.setSkillCreditMultiplier(mult)

        if self.air.holidayManager.isMoreXpHolidayRunning():
            mult = getMoreXpHolidayMultiplier()
            self.battleCalc.setSkillCreditMultiplier(mult)

        self.fsm = None
        self.clearAttacks()
        self.ignoreFaceOffDone = 0
        self.needAdjust = 0
        self.movieHasBeenMade = 0
        self.movieHasPlayed = 0
        self.rewardHasPlayed = 0
        self.movieRequested = 0
        self.ignoreResponses = 0
        self.ignoreAdjustingResponses = 0
        self.taskNames = []
        self.exitedToons = []
        self.suitsKilled = []
        self.suitsKilledThisBattle = []
        self.suitsKilledPerFloor = []
        self.suitsEncountered = []
        self.newToons = []
        self.newSuits = []
        self.numNPCAttacks = 0
        self.npcAttacks = {}
        self.pets = {}
        self.fsm = ClassicFSM.ClassicFSM('DistributedBattleAI', [
            State.State('FaceOff', self.enterFaceOff, self.exitFaceOff,
                        ['WaitForInput', 'Resume']),
            State.State('WaitForJoin', self.enterWaitForJoin,
                        self.exitWaitForJoin, ['WaitForInput', 'Resume']),
            State.State('WaitForInput', self.enterWaitForInput,
                        self.exitWaitForInput, ['MakeMovie', 'Resume']),
            State.State('MakeMovie', self.enterMakeMovie, self.exitMakeMovie,
                        ['PlayMovie', 'Resume']),
            State.State('PlayMovie', self.enterPlayMovie, self.exitPlayMovie,
                        ['WaitForJoin', 'Reward', 'Resume']),
            State.State('Reward', self.enterReward, self.exitReward,
                        ['Resume']),
            State.State('Resume', self.enterResume, self.exitResume, []),
            State.State('Off', self.enterOff, self.exitOff,
                        ['FaceOff', 'WaitForJoin'])
        ], 'Off', 'Off')
        self.joinableFsm = ClassicFSM.ClassicFSM('Joinable', [
            State.State('Joinable', self.enterJoinable, self.exitJoinable,
                        ['Unjoinable']),
            State.State('Unjoinable', self.enterUnjoinable,
                        self.exitUnjoinable, ['Joinable'])
        ], 'Unjoinable', 'Unjoinable')
        self.joinableFsm.enterInitialState()
        self.runableFsm = ClassicFSM.ClassicFSM('Runable', [
            State.State('Runable', self.enterRunable, self.exitRunable,
                        ['Unrunable']),
            State.State('Unrunable', self.enterUnrunable, self.exitUnrunable,
                        ['Runable'])
        ], 'Unrunable', 'Unrunable')
        self.runableFsm.enterInitialState()
        self.adjustFsm = ClassicFSM.ClassicFSM('Adjust', [
            State.State('Adjusting', self.enterAdjusting, self.exitAdjusting,
                        ['NotAdjusting', 'Adjusting']),
            State.State('NotAdjusting', self.enterNotAdjusting,
                        self.exitNotAdjusting, ['Adjusting'])
        ], 'NotAdjusting', 'NotAdjusting')
        self.adjustFsm.enterInitialState()
        self.fsm.enterInitialState()
        self.startTime = globalClock.getRealTime()
        self.adjustingTimer = Timer()

    def clearAttacks(self):
        self.toonAttacks = {}
        self.suitAttacks = getDefaultSuitAttacks()

    def requestDelete(self):
        if hasattr(self, 'fsm'):
            self.fsm.request('Off')

        self._DistributedBattleBaseAI__removeTaskName(
            self.uniqueName('make-movie'))
        DistributedObjectAI.DistributedObjectAI.requestDelete(self)

    def delete(self):
        self.notify.debug('deleting battle')
        self.fsm.request('Off')
        self.ignoreAll()
        self._DistributedBattleBaseAI__removeAllTasks()
        del self.fsm
        del self.joinableFsm
        del self.runableFsm
        del self.adjustFsm
        self._DistributedBattleBaseAI__cleanupJoinResponses()
        self.timer.stop()
        del self.timer
        self.adjustingTimer.stop()
        del self.adjustingTimer
        self.battleCalc.cleanup()
        del self.battleCalc
        for suit in self.suits:
            del suit.battleTrap

        del self.finishCallback
        for petProxy in self.pets.values():
            petProxy.requestDelete()

        DistributedObjectAI.DistributedObjectAI.delete(self)

    def pause(self):
        self.timer.stop()
        self.adjustingTimer.stop()

    def unpause(self):
        self.timer.resume()
        self.adjustingTimer.resume()

    def abortBattle(self):
        self.notify.debug('%s.abortBattle() called.' % self.doId)
        toonsCopy = self.toons[:]
        for toonId in toonsCopy:
            self._DistributedBattleBaseAI__removeToon(toonId)
            if self.fsm.getCurrentState().getName(
            ) == 'PlayMovie' or self.fsm.getCurrentState().getName(
            ) == 'MakeMovie':
                self.exitedToons.append(toonId)
                continue

        self.d_setMembers()
        self.b_setState('Resume')
        self._DistributedBattleBaseAI__removeAllTasks()
        self.timer.stop()
        self.adjustingTimer.stop()

    def _DistributedBattleBaseAI__removeSuit(self, suit):
        self.notify.debug('__removeSuit(%d)' % suit.doId)
        self.suits.remove(suit)
        self.activeSuits.remove(suit)
        if self.luredSuits.count(suit) == 1:
            self.luredSuits.remove(suit)

        self.suitGone = 1
        del suit.battleTrap

    def findSuit(self, id):
        for s in self.suits:
            if s.doId == id:
                return s
                continue

    def _DistributedBattleBaseAI__removeTaskName(self, name):
        if self.taskNames.count(name):
            self.taskNames.remove(name)
            self.notify.debug('removeTaskName() - %s' % name)
            taskMgr.remove(name)

    def _DistributedBattleBaseAI__removeAllTasks(self):
        for n in self.taskNames:
            self.notify.debug('removeAllTasks() - %s' % n)
            taskMgr.remove(n)

        self.taskNames = []

    def _DistributedBattleBaseAI__removeToonTasks(self, toonId):
        name = self.taskName('running-toon-%d' % toonId)
        self._DistributedBattleBaseAI__removeTaskName(name)
        name = self.taskName('to-pending-av-%d' % toonId)
        self._DistributedBattleBaseAI__removeTaskName(name)

    def getLevelDoId(self):
        return 0

    def getBattleCellId(self):
        return 0

    def getPosition(self):
        self.notify.debug('getPosition() - %s' % self.pos)
        return [self.pos[0], self.pos[1], self.pos[2]]

    def getInitialSuitPos(self):
        p = []
        p.append(self.initialSuitPos[0])
        p.append(self.initialSuitPos[1])
        p.append(self.initialSuitPos[2])
        return p

    def setBossBattle(self, bossBattle):
        self.bossBattle = bossBattle

    def getBossBattle(self):
        return self.bossBattle

    def b_setState(self, state):
        self.notify.debug('network:setState(%s)' % state)
        stime = globalClock.getRealTime() + SERVER_BUFFER_TIME
        self.sendUpdate(
            'setState',
            [state, globalClockDelta.localToNetworkTime(stime)])
        self.setState(state)

    def setState(self, state):
        self.fsm.request(state)

    def getState(self):
        return [
            self.fsm.getCurrentState().getName(),
            globalClockDelta.getRealNetworkTime()
        ]

    def d_setMembers(self):
        self.notify.debug('network:setMembers()')
        self.sendUpdate('setMembers', self.getMembers())

    def getMembers(self):
        suits = []
        for s in self.suits:
            suits.append(s.doId)

        joiningSuits = ''
        for s in self.joiningSuits:
            joiningSuits += str(suits.index(s.doId))

        pendingSuits = ''
        for s in self.pendingSuits:
            pendingSuits += str(suits.index(s.doId))

        activeSuits = ''
        for s in self.activeSuits:
            activeSuits += str(suits.index(s.doId))

        luredSuits = ''
        for s in self.luredSuits:
            luredSuits += str(suits.index(s.doId))

        suitTraps = ''
        for s in self.suits:
            if s.battleTrap == NO_TRAP:
                suitTraps += '9'
                continue
            if s.battleTrap == BattleCalculatorAI.TRAP_CONFLICT:
                suitTraps += '9'
                continue
            suitTraps += str(s.battleTrap)

        toons = []
        for t in self.toons:
            toons.append(t)

        joiningToons = ''
        for t in self.joiningToons:
            joiningToons += str(toons.index(t))

        pendingToons = ''
        for t in self.pendingToons:
            pendingToons += str(toons.index(t))

        activeToons = ''
        for t in self.activeToons:
            activeToons += str(toons.index(t))

        runningToons = ''
        for t in self.runningToons:
            runningToons += str(toons.index(t))

        self.notify.debug(
            'getMembers() - suits: %s joiningSuits: %s pendingSuits: %s activeSuits: %s luredSuits: %s suitTraps: %s toons: %s joiningToons: %s pendingToons: %s activeToons: %s runningToons: %s'
            % (suits, joiningSuits, pendingSuits, activeSuits, luredSuits,
               suitTraps, toons, joiningToons, pendingToons, activeToons,
               runningToons))
        return [
            suits, joiningSuits, pendingSuits, activeSuits, luredSuits,
            suitTraps, toons, joiningToons, pendingToons, activeToons,
            runningToons,
            globalClockDelta.getRealNetworkTime()
        ]

    def d_adjust(self):
        self.notify.debug('network:adjust()')
        self.sendUpdate('adjust', [globalClockDelta.getRealNetworkTime()])

    def getInteractivePropTrackBonus(self):
        return self.interactivePropTrackBonus

    def getZoneId(self):
        return self.zoneId

    def getTaskZoneId(self):
        return self.zoneId

    def d_setMovie(self):
        self.notify.debug('network:setMovie()')
        self.sendUpdate('setMovie', self.getMovie())
        self._DistributedBattleBaseAI__updateEncounteredCogs()

    def getMovie(self):
        suitIds = []
        for s in self.activeSuits:
            suitIds.append(s.doId)

        p = [self.movieHasBeenMade]
        p.append(self.activeToons)
        p.append(suitIds)
        for t in self.activeToons:
            if t in self.toonAttacks:
                ta = self.toonAttacks[t]
                index = -1
                id = ta[TOON_ID_COL]
                if id != -1:
                    index = self.activeToons.index(id)

                track = ta[TOON_TRACK_COL]
                if (track == NO_ATTACK
                        or attackAffectsGroup(track, ta[TOON_LVL_COL])
                    ) and track != NPCSOS and track != PETSOS:
                    target = -1
                    if track == HEAL:
                        if ta[TOON_LVL_COL] == 1:
                            ta[TOON_HPBONUS_COL] = random.randint(0, 10000)

                elif track == SOS and track == NPCSOS or track == PETSOS:
                    target = ta[TOON_TGT_COL]
                elif track == HEAL:
                    if self.activeToons.count(ta[TOON_TGT_COL]) != 0:
                        target = self.activeToons.index(ta[TOON_TGT_COL])
                    else:
                        target = -1
                elif suitIds.count(ta[TOON_TGT_COL]) != 0:
                    target = suitIds.index(ta[TOON_TGT_COL])
                else:
                    target = -1
                p = p + [index, track, ta[TOON_LVL_COL], target]
                p = p + ta[4:]
                continue
            index = self.activeToons.index(t)
            attack = getToonAttack(index)
            p = p + attack

        for i in range(4 - len(self.activeToons)):
            p = p + getToonAttack(-1)

        for sa in self.suitAttacks:
            index = -1
            id = sa[SUIT_ID_COL]
            if id != -1:
                index = suitIds.index(id)

            if sa[SUIT_ATK_COL] == -1:
                targetIndex = -1
            else:
                targetIndex = sa[SUIT_TGT_COL]
                if targetIndex == -1:
                    self.notify.debug(
                        'suit attack: %d must be group' % sa[SUIT_ATK_COL])
                else:
                    toonId = self.activeToons[targetIndex]
            p = p + [index, sa[SUIT_ATK_COL], targetIndex]
            sa[SUIT_TAUNT_COL] = 0
            if sa[SUIT_ATK_COL] != -1:
                suit = self.findSuit(id)
                sa[SUIT_TAUNT_COL] = getAttackTauntIndexFromIndex(
                    suit, sa[SUIT_ATK_COL])

            p = p + sa[3:]

        return p

    def d_setChosenToonAttacks(self):
        self.notify.debug('network:setChosenToonAttacks()')
        self.sendUpdate('setChosenToonAttacks', self.getChosenToonAttacks())

    def getChosenToonAttacks(self):
        ids = []
        tracks = []
        levels = []
        targets = []
        for t in self.activeToons:
            if t in self.toonAttacks:
                ta = self.toonAttacks[t]
            else:
                ta = getToonAttack(t)
            ids.append(t)
            tracks.append(ta[TOON_TRACK_COL])
            levels.append(ta[TOON_LVL_COL])
            targets.append(ta[TOON_TGT_COL])

        return [ids, tracks, levels, targets]

    def d_setBattleExperience(self):
        self.notify.debug('network:setBattleExperience()')
        self.sendUpdate('setBattleExperience', self.getBattleExperience())

    def getBattleExperience(self):
        returnValue = BattleExperienceAI.getBattleExperience(
            4, self.activeToons, self.toonExp,
            self.battleCalc.toonSkillPtsGained, self.toonOrigQuests,
            self.toonItems, self.toonOrigMerits, self.toonMerits,
            self.toonParts, self.suitsKilled, self.helpfulToons)
        return returnValue

    def getToonUberStatus(self):
        fieldList = []
        uberIndex = LAST_REGULAR_GAG_LEVEL + 1
        for toon in self.activeToons:
            toonList = []
            for trackIndex in range(MAX_TRACK_INDEX):
                toonList.append(toon.inventory.numItem(track, uberIndex))

            fieldList.append(encodeUber(toonList))

        return fieldList

    def addSuit(self, suit):
        self.notify.debug('addSuit(%d)' % suit.doId)
        self.newSuits.append(suit)
        self.suits.append(suit)
        suit.battleTrap = NO_TRAP
        self.numSuitsEver += 1

    def _DistributedBattleBaseAI__joinSuit(self, suit):
        self.joiningSuits.append(suit)
        toPendingTime = MAX_JOIN_T + SERVER_BUFFER_TIME
        taskName = self.taskName('to-pending-av-%d' % suit.doId)
        self._DistributedBattleBaseAI__addJoinResponse(suit.doId, taskName)
        self.taskNames.append(taskName)
        taskMgr.doMethodLater(
            toPendingTime,
            self._DistributedBattleBaseAI__serverJoinDone,
            taskName,
            extraArgs=(suit.doId, taskName))

    def _DistributedBattleBaseAI__serverJoinDone(self, avId, taskName):
        self.notify.debug('join for av: %d timed out on server' % avId)
        self._DistributedBattleBaseAI__removeTaskName(taskName)
        self._DistributedBattleBaseAI__makeAvPending(avId)
        return Task.done

    def _DistributedBattleBaseAI__makeAvPending(self, avId):
        self.notify.debug('__makeAvPending(%d)' % avId)
        self._DistributedBattleBaseAI__removeJoinResponse(avId)
        self._DistributedBattleBaseAI__removeTaskName(
            self.taskName('to-pending-av-%d' % avId))
        if self.toons.count(avId) > 0:
            self.joiningToons.remove(avId)
            self.pendingToons.append(avId)
        else:
            suit = self.findSuit(avId)
            if suit is not None:
                if not suit.isEmpty():
                    if not self.joiningSuits.count(suit) == 1:
                        self.notify.warning('__makeAvPending(%d) in zone: %d' %
                                            (avId, self.zoneId))
                        self.notify.warning('toons: %s' % self.toons)
                        self.notify.warning(
                            'joining toons: %s' % self.joiningToons)
                        self.notify.warning(
                            'pending toons: %s' % self.pendingToons)
                        self.notify.warning('suits: %s' % self.suits)
                        self.notify.warning(
                            'joining suits: %s' % self.joiningSuits)
                        self.notify.warning(
                            'pending suits: %s' % self.pendingSuits)

                    self.joiningSuits.remove(suit)
                    self.pendingSuits.append(suit)

            else:
                self.notify.warning(
                    'makeAvPending() %d not in toons or suits' % avId)
                return None
        self.d_setMembers()
        self.needAdjust = 1
        self._DistributedBattleBaseAI__requestAdjust()

    def suitRequestJoin(self, suit):
        self.notify.debug('suitRequestJoin(%d)' % suit.getDoId())
        if self.suitCanJoin():
            self.addSuit(suit)
            self._DistributedBattleBaseAI__joinSuit(suit)
            self.d_setMembers()
            suit.prepareToJoinBattle()
            return 1
        else:
            self.notify.warning(
                'suitRequestJoin() - not joinable - joinable state: %s max suits: %d'
                % (self.joinableFsm.getCurrentState().getName(),
                   self.maxSuits))
            return 0

    def addToon(self, avId):
        print 'DBB-addToon %s' % avId
        self.notify.debug('addToon(%d)' % avId)
        toon = self.getToon(avId)
        if toon is None:
            return 0

        toon.stopToonUp()
        event = simbase.air.getAvatarExitEvent(avId)
        self.avatarExitEvents.append(event)
        self.accept(
            event,
            self._DistributedBattleBaseAI__handleUnexpectedExit,
            extraArgs=[avId])
        event = 'inSafezone-%s' % avId
        self.avatarExitEvents.append(event)
        self.accept(
            event,
            self._DistributedBattleBaseAI__handleSuddenExit,
            extraArgs=[avId, 0])
        self.newToons.append(avId)
        self.toons.append(avId)
        toon = simbase.air.doId2do.get(avId)
        if toon:
            if hasattr(self, 'doId'):
                toon.b_setBattleId(self.doId)
            else:
                toon.b_setBattleId(-1)
            messageToonAdded = 'Battle adding toon %s' % avId
            messenger.send(messageToonAdded, [avId])

        if self.fsm is not None and self.fsm.getCurrentState().getName(
        ) == 'PlayMovie':
            self.responses[avId] = 1
        else:
            self.responses[avId] = 0
        self.adjustingResponses[avId] = 0
        if avId not in self.toonExp:
            p = []
            for t in Tracks:
                p.append(toon.experience.getExp(t))

            self.toonExp[avId] = p

        if avId not in self.toonOrigMerits:
            self.toonOrigMerits[avId] = toon.cogMerits[:]

        if avId not in self.toonMerits:
            self.toonMerits[avId] = [0, 0, 0, 0]

        if avId not in self.toonOrigQuests:
            flattenedQuests = []
            for quest in toon.quests:
                flattenedQuests.extend(quest)

            self.toonOrigQuests[avId] = flattenedQuests

        if avId not in self.toonItems:
            self.toonItems[avId] = ([], [])

        return 1

    def _DistributedBattleBaseAI__joinToon(self, avId, pos):
        self.joiningToons.append(avId)
        toPendingTime = MAX_JOIN_T + SERVER_BUFFER_TIME
        taskName = self.taskName('to-pending-av-%d' % avId)
        self._DistributedBattleBaseAI__addJoinResponse(avId, taskName, toon=1)
        taskMgr.doMethodLater(
            toPendingTime,
            self._DistributedBattleBaseAI__serverJoinDone,
            taskName,
            extraArgs=(avId, taskName))
        self.taskNames.append(taskName)

    def _DistributedBattleBaseAI__updateEncounteredCogs(self):
        for toon in self.activeToons:
            if toon in self.newToons:
                for suit in self.activeSuits:
                    if hasattr(suit, 'dna'):
                        self.suitsEncountered.append({
                            'type':
                            suit.dna.name,
                            'activeToons':
                            self.activeToons[:]
                        })
                        continue
                    self.notify.warning(
                        'Suit has no DNA in zone %s: toons involved = %s' %
                        (self.zoneId, self.activeToons))
                    return None

                self.newToons.remove(toon)
                continue

        for suit in self.activeSuits:
            if suit in self.newSuits:
                if hasattr(suit, 'dna'):
                    self.suitsEncountered.append({
                        'type':
                        suit.dna.name,
                        'activeToons':
                        self.activeToons[:]
                    })
                else:
                    self.notify.warning(
                        'Suit has no DNA in zone %s: toons involved = %s' %
                        (self.zoneId, self.activeToons))
                    return None
                self.newSuits.remove(suit)
                continue

    def _DistributedBattleBaseAI__makeToonRun(self, toonId, updateAttacks):
        self.activeToons.remove(toonId)
        self.toonGone = 1
        self.runningToons.append(toonId)
        taskName = self.taskName('running-toon-%d' % toonId)
        taskMgr.doMethodLater(
            TOON_RUN_T,
            self._DistributedBattleBaseAI__serverRunDone,
            taskName,
            extraArgs=(toonId, updateAttacks, taskName))
        self.taskNames.append(taskName)

    def _DistributedBattleBaseAI__serverRunDone(self, toonId, updateAttacks,
                                                taskName):
        self.notify.debug('run for toon: %d timed out on server' % toonId)
        self._DistributedBattleBaseAI__removeTaskName(taskName)
        self._DistributedBattleBaseAI__removeToon(toonId)
        self.d_setMembers()
        if len(self.toons) == 0:
            self.notify.debug('last toon is gone - battle is finished')
            self.b_setState('Resume')
        elif updateAttacks == 1:
            self.d_setChosenToonAttacks()

        self.needAdjust = 1
        self._DistributedBattleBaseAI__requestAdjust()
        return Task.done

    def _DistributedBattleBaseAI__requestAdjust(self):
        if not self.fsm:
            return None

        cstate = self.fsm.getCurrentState().getName()
        if cstate == 'WaitForInput' or cstate == 'WaitForJoin':
            if self.adjustFsm.getCurrentState().getName() == 'NotAdjusting':
                if self.needAdjust == 1:
                    self.d_adjust()
                    self.adjustingSuits = []
                    for s in self.pendingSuits:
                        self.adjustingSuits.append(s)

                    self.adjustingToons = []
                    for t in self.pendingToons:
                        self.adjustingToons.append(t)

                    self.adjustFsm.request('Adjusting')
                else:
                    self.notify.debug('requestAdjust() - dont need to')
            else:
                self.notify.debug('requestAdjust() - already adjusting')
        else:
            self.notify.debug('requestAdjust() - in state: %s' % cstate)

    def _DistributedBattleBaseAI__handleUnexpectedExit(self, avId):
        disconnectCode = self.air.getAvatarDisconnectReason(avId)
        self.notify.warning(
            'toon: %d exited unexpectedly, reason %d' % (avId, disconnectCode))
        userAborted = disconnectCode == ToontownGlobals.DisconnectCloseWindow
        self._DistributedBattleBaseAI__handleSuddenExit(avId, userAborted)

    def _DistributedBattleBaseAI__handleSuddenExit(self, avId, userAborted):
        self._DistributedBattleBaseAI__removeToon(
            avId, userAborted=userAborted)
        if self.fsm.getCurrentState().getName(
        ) == 'PlayMovie' or self.fsm.getCurrentState().getName(
        ) == 'MakeMovie':
            self.exitedToons.append(avId)

        self.d_setMembers()
        if len(self.toons) == 0:
            self.notify.debug('last toon is gone - battle is finished')
            self._DistributedBattleBaseAI__removeAllTasks()
            self.timer.stop()
            self.adjustingTimer.stop()
            self.b_setState('Resume')
        else:
            self.needAdjust = 1
            self._DistributedBattleBaseAI__requestAdjust()

    def _DistributedBattleBaseAI__removeSuit(self, suit):
        self.notify.debug('__removeSuit(%d)' % suit.doId)
        self.suits.remove(suit)
        self.activeSuits.remove(suit)
        if self.luredSuits.count(suit) == 1:
            self.luredSuits.remove(suit)

        self.suitGone = 1
        del suit.battleTrap

    def _DistributedBattleBaseAI__removeToon(self, toonId, userAborted=0):
        self.notify.debug('__removeToon(%d)' % toonId)
        if self.toons.count(toonId) == 0:
            return None

        self.battleCalc.toonLeftBattle(toonId)
        self._DistributedBattleBaseAI__removeToonTasks(toonId)
        self.toons.remove(toonId)
        if self.joiningToons.count(toonId) == 1:
            self.joiningToons.remove(toonId)

        if self.pendingToons.count(toonId) == 1:
            self.pendingToons.remove(toonId)

        if self.activeToons.count(toonId) == 1:
            activeToonIdx = self.activeToons.index(toonId)
            self.notify.debug(
                'removing activeToons[%d], updating suitAttacks SUIT_HP_COL to match'
                % activeToonIdx)
            for i in range(len(self.suitAttacks)):
                if activeToonIdx < len(self.suitAttacks[i][SUIT_HP_COL]):
                    del self.suitAttacks[i][SUIT_HP_COL][activeToonIdx]
                    continue
                self.notify.warning(
                    "suitAttacks %d doesn't have an HP column for active toon index %d"
                    % (i, activeToonIdx))

            self.activeToons.remove(toonId)

        if self.runningToons.count(toonId) == 1:
            self.runningToons.remove(toonId)

        if self.adjustingToons.count(toonId) == 1:
            self.notify.warning(
                'removeToon() - toon: %d was adjusting!' % toonId)
            self.adjustingToons.remove(toonId)

        self.toonGone = 1
        if toonId in self.pets:
            self.pets[toonId].requestDelete()
            del self.pets[toonId]

        self._DistributedBattleBaseAI__removeResponse(toonId)
        self._DistributedBattleBaseAI__removeAdjustingResponse(toonId)
        self._DistributedBattleBaseAI__removeJoinResponses(toonId)
        event = simbase.air.getAvatarExitEvent(toonId)
        self.avatarExitEvents.remove(event)
        self.ignore(event)
        event = 'inSafezone-%s' % toonId
        self.avatarExitEvents.remove(event)
        self.ignore(event)
        toon = simbase.air.doId2do.get(toonId)
        if toon:
            toon.b_setBattleId(0)
            messageToonReleased = 'Battle releasing toon %s' % toon.doId
            messenger.send(messageToonReleased, [toon.doId])

        if not userAborted:
            toon = self.getToon(toonId)
            if toon is not None:
                toon.hpOwnedByBattle = 0
                toon.d_setHp(toon.hp)
                toon.d_setInventory(toon.inventory.makeNetString())
                self.air.cogPageManager.toonEncounteredCogs(
                    toon, self.suitsEncountered, self.getTaskZoneId())

        elif len(self.suits) > 0 and not (self.streetBattle):
            self.notify.info(
                'toon %d aborted non-street battle; clearing inventory and hp.'
                % toonId)
            toon = DistributedToonAI.DistributedToonAI(self.air)
            toon.doId = toonId
            empty = InventoryBase.InventoryBase(toon)
            toon.b_setInventory(empty.makeNetString())
            toon.b_setHp(0)
            db = DatabaseObject.DatabaseObject(self.air, toonId)
            db.storeObject(toon, ['setInventory', 'setHp'])
            self.notify.info(
                'killing mem leak from temporary DistributedToonAI %d' %
                toonId)
            toon.deleteDummy()

    def getToon(self, toonId):
        if toonId in self.air.doId2do:
            return self.air.doId2do[toonId]
        else:
            self.notify.warning(
                'getToon() - toon: %d not in repository!' % toonId)

    def toonRequestRun(self):
        toonId = self.air.getAvatarIdFromSender()
        if self.ignoreResponses == 1:
            self.notify.debug('ignoring response from toon: %d' % toonId)
            return None

        self.notify.debug('toonRequestRun(%d)' % toonId)
        if not self.isRunable():
            self.notify.warning('toonRequestRun() - not runable')
            return None

        updateAttacks = 0
        if self.activeToons.count(toonId) == 0:
            self.notify.warning(
                'toon tried to run, but not found in activeToons: %d' % toonId)
            return None

        for toon in self.activeToons:
            if toon in self.toonAttacks:
                ta = self.toonAttacks[toon]
                track = ta[TOON_TRACK_COL]
                level = ta[TOON_LVL_COL]
                if (ta[TOON_TGT_COL] == toonId
                        or track == HEAL) and attackAffectsGroup(
                            track, level) and len(self.activeToons) <= 2:
                    healerId = ta[TOON_ID_COL]
                    self.notify.debug('resetting toon: %ds attack' % healerId)
                    self.toonAttacks[toon] = getToonAttack(
                        toon, track=UN_ATTACK)
                    self.responses[healerId] = 0
                    updateAttacks = 1

            len(self.activeToons) <= 2

        self._DistributedBattleBaseAI__makeToonRun(toonId, updateAttacks)
        self.d_setMembers()
        self.needAdjust = 1
        self._DistributedBattleBaseAI__requestAdjust()

    def toonRequestJoin(self, x, y, z):
        toonId = self.air.getAvatarIdFromSender()
        self.notify.debug('toonRequestJoin(%d)' % toonId)
        self.signupToon(toonId, x, y, z)

    def toonDied(self):
        toonId = self.air.getAvatarIdFromSender()
        self.notify.debug('toonDied(%d)' % toonId)
        if toonId in self.toons:
            toon = self.getToon(toonId)
            if toon:
                toon.hp = -1
                toon.inventory.zeroInv(1)
                self._DistributedBattleBaseAI__handleSuddenExit(toonId, 0)

    def signupToon(self, toonId, x, y, z):
        if self.toons.count(toonId):
            return None

        if self.toonCanJoin():
            if self.addToon(toonId):
                self._DistributedBattleBaseAI__joinToon(
                    toonId, Point3(x, y, z))
                self.d_setMembers()

        else:
            self.notify.warning('toonRequestJoin() - not joinable')
            self.d_denyLocalToonJoin(toonId)

    def d_denyLocalToonJoin(self, toonId):
        self.notify.debug('network: denyLocalToonJoin(%d)' % toonId)
        self.sendUpdateToAvatarId(toonId, 'denyLocalToonJoin', [])

    def resetResponses(self):
        self.responses = {}
        for t in self.toons:
            self.responses[t] = 0

        self.ignoreResponses = 0

    def allToonsResponded(self):
        for t in self.toons:
            if self.responses[t] == 0:
                return 0
                continue

        self.ignoreResponses = 1
        return 1

    def _DistributedBattleBaseAI__allPendingActiveToonsResponded(self):
        for t in self.pendingToons + self.activeToons:
            if self.responses[t] == 0:
                return 0
                continue

        self.ignoreResponses = 1
        return 1

    def _DistributedBattleBaseAI__allActiveToonsResponded(self):
        for t in self.activeToons:
            if self.responses[t] == 0:
                return 0
                continue

        self.ignoreResponses = 1
        return 1

    def _DistributedBattleBaseAI__removeResponse(self, toonId):
        del self.responses[toonId]
        if self.ignoreResponses == 0 and len(self.toons) > 0:
            currStateName = self.fsm.getCurrentState().getName()
            if currStateName == 'WaitForInput':
                if self._DistributedBattleBaseAI__allActiveToonsResponded():
                    self.notify.debug('removeResponse() - dont wait for movie')
                    self._DistributedBattleBaseAI__requestMovie()

            elif currStateName == 'PlayMovie':
                if self._DistributedBattleBaseAI__allPendingActiveToonsResponded(
                ):
                    self.notify.debug('removeResponse() - surprise movie done')
                    self._DistributedBattleBaseAI__movieDone()

            elif currStateName == 'Reward' or currStateName == 'BuildingReward':
                if self._DistributedBattleBaseAI__allActiveToonsResponded():
                    self.notify.debug(
                        'removeResponse() - surprise reward done')
                    self.handleRewardDone()

    def _DistributedBattleBaseAI__resetAdjustingResponses(self):
        self.adjustingResponses = {}
        for t in self.toons:
            self.adjustingResponses[t] = 0

        self.ignoreAdjustingResponses = 0

    def _DistributedBattleBaseAI__allAdjustingToonsResponded(self):
        for t in self.toons:
            if self.adjustingResponses[t] == 0:
                return 0
                continue

        self.ignoreAdjustingResponses = 1
        return 1

    def _DistributedBattleBaseAI__removeAdjustingResponse(self, toonId):
        if toonId in self.adjustingResponses:
            del self.adjustingResponses[toonId]
            if self.ignoreAdjustingResponses == 0 and len(self.toons) > 0:
                if self._DistributedBattleBaseAI__allAdjustingToonsResponded():
                    self._DistributedBattleBaseAI__adjustDone()

    def _DistributedBattleBaseAI__addJoinResponse(self, avId, taskName,
                                                  toon=0):
        if toon == 1:
            for jr in self.joinResponses.values():
                jr[avId] = 0

        self.joinResponses[avId] = {}
        for t in self.toons:
            self.joinResponses[avId][t] = 0

        self.joinResponses[avId]['taskName'] = taskName

    def _DistributedBattleBaseAI__removeJoinResponses(self, avId):
        self._DistributedBattleBaseAI__removeJoinResponse(avId)
        removedOne = 0
        for j in self.joinResponses.values():
            if avId in j:
                del j[avId]
                removedOne = 1
                continue

        if removedOne == 1:
            for t in self.joiningToons:
                if self._DistributedBattleBaseAI__allToonsRespondedJoin(t):
                    self._DistributedBattleBaseAI__makeAvPending(t)
                    continue

    def _DistributedBattleBaseAI__removeJoinResponse(self, avId):
        if avId in self.joinResponses:
            taskMgr.remove(self.joinResponses[avId]['taskName'])
            del self.joinResponses[avId]

    def _DistributedBattleBaseAI__allToonsRespondedJoin(self, avId):
        jr = self.joinResponses[avId]
        for t in self.toons:
            if jr[t] == 0:
                return 0
                continue

        return 1

    def _DistributedBattleBaseAI__cleanupJoinResponses(self):
        for jr in self.joinResponses.values():
            taskMgr.remove(jr['taskName'])
            del jr

    def adjustDone(self):
        toonId = self.air.getAvatarIdFromSender()
        if self.ignoreAdjustingResponses == 1:
            self.notify.debug('adjustDone() - ignoring toon: %d' % toonId)
            return None
        elif self.adjustFsm.getCurrentState().getName() != 'Adjusting':
            self.notify.warning('adjustDone() - in state %s' %
                                self.fsm.getCurrentState().getName())
            return None
        elif self.toons.count(toonId) == 0:
            self.notify.warning(
                'adjustDone() - toon: %d not in toon list' % toonId)
            return None

        self.adjustingResponses[toonId] += 1
        self.notify.debug('toon: %d done adjusting' % toonId)
        if self._DistributedBattleBaseAI__allAdjustingToonsResponded():
            self._DistributedBattleBaseAI__adjustDone()

    def timeout(self):
        toonId = self.air.getAvatarIdFromSender()
        if self.ignoreResponses == 1:
            self.notify.debug('timeout() - ignoring toon: %d' % toonId)
            return None
        elif self.fsm.getCurrentState().getName() != 'WaitForInput':
            self.notify.warning('timeout() - in state: %s' %
                                self.fsm.getCurrentState().getName())
            return None
        elif self.toons.count(toonId) == 0:
            self.notify.warning(
                'timeout() - toon: %d not in toon list' % toonId)
            return None

        self.toonAttacks[toonId] = getToonAttack(toonId)
        self.d_setChosenToonAttacks()
        self.responses[toonId] += 1
        self.notify.debug('toon: %d timed out' % toonId)
        if self._DistributedBattleBaseAI__allActiveToonsResponded():
            self._DistributedBattleBaseAI__requestMovie(timeout=1)

    def movieDone(self):
        toonId = self.air.getAvatarIdFromSender()
        if self.ignoreResponses == 1:
            self.notify.debug('movieDone() - ignoring toon: %d' % toonId)
            return None
        elif self.fsm.getCurrentState().getName() != 'PlayMovie':
            self.notify.warning('movieDone() - in state %s' %
                                self.fsm.getCurrentState().getName())
            return None
        elif self.toons.count(toonId) == 0:
            self.notify.warning(
                'movieDone() - toon: %d not in toon list' % toonId)
            return None

        self.responses[toonId] += 1
        self.notify.debug('toon: %d done with movie' % toonId)
        if self._DistributedBattleBaseAI__allPendingActiveToonsResponded():
            self._DistributedBattleBaseAI__movieDone()
        else:
            self.timer.stop()
            self.timer.startCallback(
                TIMEOUT_PER_USER,
                self._DistributedBattleBaseAI__serverMovieDone)

    def rewardDone(self):
        toonId = self.air.getAvatarIdFromSender()
        stateName = self.fsm.getCurrentState().getName()
        if self.ignoreResponses == 1:
            self.notify.debug('rewardDone() - ignoring toon: %d' % toonId)
            return None
        elif stateName not in ('Reward', 'BuildingReward', 'FactoryReward',
                               'MintReward', 'StageReward',
                               'CountryClubReward'):
            self.notify.warning('rewardDone() - in state %s' % stateName)
            return None
        elif self.toons.count(toonId) == 0:
            self.notify.warning(
                'rewardDone() - toon: %d not in toon list' % toonId)
            return None

        self.responses[toonId] += 1
        self.notify.debug('toon: %d done with reward' % toonId)
        if self._DistributedBattleBaseAI__allActiveToonsResponded():
            self.handleRewardDone()
        else:
            self.timer.stop()
            self.timer.startCallback(TIMEOUT_PER_USER, self.serverRewardDone)

    def assignRewards(self):
        if self.rewardHasPlayed == 1:
            self.notify.debug('handleRewardDone() - reward has already played')
            return None

        self.rewardHasPlayed = 1
        BattleExperienceAI.assignRewards(
            self.activeToons, self.battleCalc.toonSkillPtsGained,
            self.suitsKilled, self.getTaskZoneId(), self.helpfulToons)

    def joinDone(self, avId):
        toonId = self.air.getAvatarIdFromSender()
        if self.toons.count(toonId) == 0:
            self.notify.warning(
                'joinDone() - toon: %d not in toon list' % toonId)
            return None

        if avId not in self.joinResponses:
            self.notify.debug('joinDone() - no entry for: %d - ignoring: %d' %
                              (avId, toonId))
            return None

        jr = self.joinResponses[avId]
        if toonId in jr:
            jr[toonId] += 1

        self.notify.debug(
            'client with localToon: %d done joining av: %d' % (toonId, avId))
        if self._DistributedBattleBaseAI__allToonsRespondedJoin(avId):
            self._DistributedBattleBaseAI__makeAvPending(avId)

    def requestAttack(self, track, level, av):
        toonId = self.air.getAvatarIdFromSender()
        if self.ignoreResponses == 1:
            self.notify.debug('requestAttack() - ignoring toon: %d' % toonId)
            return None
        elif self.fsm.getCurrentState().getName() != 'WaitForInput':
            self.notify.warning('requestAttack() - in state: %s' %
                                self.fsm.getCurrentState().getName())
            return None
        elif self.activeToons.count(toonId) == 0:
            self.notify.warning(
                'requestAttack() - toon: %d not in toon list' % toonId)
            return None

        self.notify.debug(
            'requestAttack(%d, %d, %d, %d)' % (toonId, track, level, av))
        toon = self.getToon(toonId)
        if toon is None:
            self.notify.warning('requestAttack() - no toon: %d' % toonId)
            return None

        validResponse = 1
        if track == SOS:
            self.notify.debug('toon: %d calls for help' % toonId)
            self.air.writeServerEvent('friendSOS', toonId, '%s' % av)
            self.toonAttacks[toonId] = getToonAttack(
                toonId, track=SOS, target=av)
        elif track == NPCSOS:
            self.notify.debug('toon: %d calls for help' % toonId)
            self.air.writeServerEvent('NPCSOS', toonId, '%s' % av)
            toon = self.getToon(toonId)
            if toon is None:
                return None

            if av in toon.NPCFriendsDict:
                npcCollision = 0
                if av in self.npcAttacks:
                    callingToon = self.npcAttacks[av]
                    if self.activeToons.count(callingToon) == 1:
                        self.toonAttacks[toonId] = getToonAttack(
                            toonId, track=PASS)
                        npcCollision = 1

                if npcCollision == 0:
                    self.toonAttacks[toonId] = getToonAttack(
                        toonId, track=NPCSOS, level=5, target=av)
                    self.numNPCAttacks += 1
                    self.npcAttacks[av] = toonId

        elif track == PETSOS:
            self.notify.debug('toon: %d calls for pet: %d' % (toonId, av))
            self.air.writeServerEvent('PETSOS', toonId, '%s' % av)
            toon = self.getToon(toonId)
            if toon is None:
                return None

            if not self.validate(
                    toonId, level in toon.petTrickPhrases,
                    'requestAttack: invalid pet trickId: %s' % level):
                return None

            self.toonAttacks[toonId] = getToonAttack(
                toonId, track=PETSOS, level=level, target=av)
        elif track == UN_ATTACK:
            self.notify.debug('toon: %d changed its mind' % toonId)
            self.toonAttacks[toonId] = getToonAttack(toonId, track=UN_ATTACK)
            if toonId in self.responses:
                self.responses[toonId] = 0

            validResponse = 0
        elif track == PASS:
            self.toonAttacks[toonId] = getToonAttack(toonId, track=PASS)
        elif track == FIRE:
            self.toonAttacks[toonId] = getToonAttack(
                toonId, track=FIRE, target=av)
        elif track >= 0:
            pass
        if not self.validate(toonId, track <= MAX_TRACK_INDEX,
                             'requestAttack: invalid track %s' % track):
            return None

        if level >= 0:
            pass
        if not self.validate(toonId, level <= MAX_LEVEL_INDEX,
                             'requestAttack: invalid level %s' % level):
            return None

        if toon.inventory.numItem(track, level) == 0:
            self.notify.warning(
                'requestAttack() - toon has no item track:                     %d level: %d'
                % (track, level))
            self.toonAttacks[toonId] = getToonAttack(toonId)
            return None

        if track == HEAL:
            if (self.runningToons.count(av) == 1 or attackAffectsGroup(
                    track, level)) and len(self.activeToons) < 2:
                self.toonAttacks[toonId] = getToonAttack(
                    toonId, track=UN_ATTACK)
                validResponse = 0
            else:
                self.toonAttacks[toonId] = getToonAttack(
                    toonId, track=track, level=level, target=av)
        else:
            self.toonAttacks[toonId] = getToonAttack(
                toonId, track=track, level=level, target=av)
            if av == -1 and not attackAffectsGroup(track, level):
                validResponse = 0

        self.d_setChosenToonAttacks()
        if validResponse == 1:
            self.responses[toonId] += 1

        self.notify.debug('toon: %d chose an attack' % toonId)
        if self._DistributedBattleBaseAI__allActiveToonsResponded():
            self._DistributedBattleBaseAI__requestMovie()

    def requestPetProxy(self, av):
        toonId = self.air.getAvatarIdFromSender()
        if self.ignoreResponses == 1:
            self.notify.debug('requestPetProxy() - ignoring toon: %d' % toonId)
            return None
        elif self.fsm.getCurrentState().getName() != 'WaitForInput':
            self.notify.warning('requestPetProxy() - in state: %s' %
                                self.fsm.getCurrentState().getName())
            return None
        elif self.activeToons.count(toonId) == 0:
            self.notify.warning(
                'requestPetProxy() - toon: %d not in toon list' % toonId)
            return None

        self.notify.debug('requestPetProxy(%s, %s)' % (toonId, av))
        toon = self.getToon(toonId)
        if toon is None:
            self.notify.warning('requestPetProxy() - no toon: %d' % toonId)
            return None

        petId = toon.getPetId()
        zoneId = self.zoneId
        if petId == av:
            if toonId not in self.pets:

                def handleGetPetProxy(success,
                                      petProxy,
                                      petId=petId,
                                      zoneId=zoneId,
                                      toonId=toonId):
                    if success:
                        if petId not in simbase.air.doId2do:
                            simbase.air.requestDeleteDoId(petId)
                        else:
                            petDO = simbase.air.doId2do[petId]
                            petDO.requestDelete()
                            simbase.air.deleteDistObject(petDO)
                        petProxy.dbObject = 1
                        petProxy.generateWithRequiredAndId(
                            petId, self.air.districtId, zoneId)
                        petProxy.broadcastDominantMood()
                        self.pets[toonId] = petProxy
                    else:
                        self.notify.warning(
                            'error generating petProxy: %s' % petId)

                self.getPetProxyObject(petId, handleGetPetProxy)

    def suitCanJoin(self):
        if len(self.suits) < self.maxSuits:
            pass
        return self.isJoinable()

    def toonCanJoin(self):
        if len(self.toons) < 4:
            pass
        return self.isJoinable()

    def _DistributedBattleBaseAI__requestMovie(self, timeout=0):
        if self.adjustFsm.getCurrentState().getName() == 'Adjusting':
            self.notify.debug('__requestMovie() - in Adjusting')
            self.movieRequested = 1
        else:
            movieDelay = 0
            if len(self.activeToons) == 0:
                self.notify.warning(
                    'only pending toons left in battle %s, toons = %s' %
                    (self.doId, self.toons))
            elif len(self.activeSuits) == 0:
                self.notify.warning(
                    'only pending suits left in battle %s, suits = %s' %
                    (self.doId, self.suits))
            elif len(self.activeToons) > 1 and not timeout:
                movieDelay = 1

            self.fsm.request('MakeMovie')
            if movieDelay:
                taskMgr.doMethodLater(0.80000000000000004,
                                      self._DistributedBattleBaseAI__makeMovie,
                                      self.uniqueName('make-movie'))
                self.taskNames.append(self.uniqueName('make-movie'))
            else:
                self._DistributedBattleBaseAI__makeMovie()

    def _DistributedBattleBaseAI__makeMovie(self, task=None):
        self.notify.debug('makeMovie()')
        if self._DOAI_requestedDelete:
            self.notify.warning(
                'battle %s requested delete, then __makeMovie was called!' %
                self.doId)
            if hasattr(self, 'levelDoId'):
                self.notify.warning(
                    'battle %s in level %s' % (self.doId, self.levelDoId))

            return None

        self._DistributedBattleBaseAI__removeTaskName(
            self.uniqueName('make-movie'))
        if self.movieHasBeenMade == 1:
            self.notify.debug('__makeMovie() - movie has already been made')
            return None

        self.movieRequested = 0
        self.movieHasBeenMade = 1
        self.movieHasPlayed = 0
        self.rewardHasPlayed = 0
        for t in self.activeToons:
            if t not in self.toonAttacks:
                self.toonAttacks[t] = getToonAttack(t)

            attack = self.toonAttacks[t]
            if attack[TOON_TRACK_COL] == PASS or attack[
                    TOON_TRACK_COL] == UN_ATTACK:
                self.toonAttacks[t] = getToonAttack(t)

            if self.toonAttacks[t][TOON_TRACK_COL] != NO_ATTACK:
                self.addHelpfulToon(t)
                continue

        self.battleCalc.calculateRound()
        for t in self.activeToons:
            self.sendEarnedExperience(t)
            toon = self.getToon(t)
            if toon is not None:
                toon.hpOwnedByBattle = 1
                if toon.immortalMode:
                    toon.toonUp(toon.maxHp)

        self.d_setMovie()
        self.b_setState('PlayMovie')
        return Task.done

    def sendEarnedExperience(self, toonId):
        toon = self.getToon(toonId)
        if toon is not None:
            expList = self.battleCalc.toonSkillPtsGained.get(toonId, None)
            if expList is None:
                toon.d_setEarnedExperience([])
            else:
                roundList = []
                for exp in expList:
                    roundList.append(int(exp + 0.5))

                toon.d_setEarnedExperience(roundList)

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterFaceOff(self):
        pass

    def exitFaceOff(self):
        pass

    def enterWaitForJoin(self):
        self.notify.debug('enterWaitForJoin()')
        if len(self.activeSuits) > 0:
            self.b_setState('WaitForInput')
        else:
            self.notify.debug('enterWaitForJoin() - no active suits')
            self.runableFsm.request('Runable')
            self.resetResponses()
            self._DistributedBattleBaseAI__requestAdjust()

    def exitWaitForJoin(self):
        pass

    def enterWaitForInput(self):
        self.notify.debug('enterWaitForInput()')
        self.joinableFsm.request('Joinable')
        self.runableFsm.request('Runable')
        self.resetResponses()
        self._DistributedBattleBaseAI__requestAdjust()
        if not self.tutorialFlag:
            self.timer.startCallback(
                SERVER_INPUT_TIMEOUT,
                self._DistributedBattleBaseAI__serverTimedOut)

        self.npcAttacks = {}
        for toonId in self.toons:
            if bboard.get('autoRestock-%s' % toonId, False):
                toon = self.air.doId2do.get(toonId)
                if toon is not None:
                    toon.doRestock(0)

            toon is not None

    def exitWaitForInput(self):
        self.npcAttacks = {}
        self.timer.stop()

    def _DistributedBattleBaseAI__serverTimedOut(self):
        self.notify.debug('wait for input timed out on server')
        self.ignoreResponses = 1
        self._DistributedBattleBaseAI__requestMovie(timeout=1)

    def enterMakeMovie(self):
        self.notify.debug('enterMakeMovie()')
        self.runableFsm.request('Unrunable')
        self.resetResponses()

    def exitMakeMovie(self):
        pass

    def enterPlayMovie(self):
        self.notify.debug('enterPlayMovie()')
        self.joinableFsm.request('Joinable')
        self.runableFsm.request('Unrunable')
        self.resetResponses()
        movieTime = TOON_ATTACK_TIME * (len(self.activeToons) + self.numNPCAttacks) + \
            SUIT_ATTACK_TIME * len(self.activeSuits) + SERVER_BUFFER_TIME
        self.numNPCAttacks = 0
        self.notify.debug(
            'estimated upper bound of movie time: %f' % movieTime)
        self.timer.startCallback(
            movieTime, self._DistributedBattleBaseAI__serverMovieDone)

    def _DistributedBattleBaseAI__serverMovieDone(self):
        self.notify.debug('movie timed out on server')
        self.ignoreResponses = 1
        self._DistributedBattleBaseAI__movieDone()

    def serverRewardDone(self):
        self.notify.debug('reward timed out on server')
        self.ignoreResponses = 1
        self.handleRewardDone()

    def handleRewardDone(self):
        self.b_setState('Resume')

    def exitPlayMovie(self):
        self.timer.stop()

    def _DistributedBattleBaseAI__movieDone(self):
        self.notify.debug('__movieDone() - movie is finished')
        if self.movieHasPlayed == 1:
            self.notify.debug('__movieDone() - movie had already finished')
            return None

        self.movieHasBeenMade = 0
        self.movieHasPlayed = 1
        self.ignoreResponses = 1
        needUpdate = 0
        toonHpDict = {}
        for toon in self.activeToons:
            toonHpDict[toon] = [0, 0, 0]
            actualToon = self.getToon(toon)
            self.notify.debug(
                'BEFORE ROUND: toon: %d hp: %d' % (toon, actualToon.hp))

        deadSuits = []
        trapDict = {}
        suitsLuredOntoTraps = []
        npcTrapAttacks = []
        for activeToon in self.activeToons + self.exitedToons:
            if activeToon in self.toonAttacks:
                attack = self.toonAttacks[activeToon]
                track = attack[TOON_TRACK_COL]
                npc_level = None
                if track == NPCSOS:
                    (track, npc_level, npc_hp) = NPCToons.getNPCTrackLevelHp(
                        attack[TOON_TGT_COL])
                    if track is None:
                        track = NPCSOS
                    elif track == TRAP:
                        npcTrapAttacks.append(attack)
                        toon = self.getToon(attack[TOON_ID_COL])
                        av = attack[TOON_TGT_COL]
                        if toon is not None and av in toon.NPCFriendsDict:
                            toon.NPCFriendsDict[av] -= 1
                            if toon.NPCFriendsDict[av] <= 0:
                                del toon.NPCFriendsDict[av]

                            toon.d_setNPCFriendsDict(toon.NPCFriendsDict)
                            continue
                        continue

                if track != NO_ATTACK:
                    toonId = attack[TOON_ID_COL]
                    level = attack[TOON_LVL_COL]
                    if npc_level is not None:
                        level = npc_level

                    if attack[TOON_TRACK_COL] == NPCSOS:
                        toon = self.getToon(toonId)
                        av = attack[TOON_TGT_COL]
                        if toon is not None and av in toon.NPCFriendsDict:
                            toon.NPCFriendsDict[av] -= 1
                            if toon.NPCFriendsDict[av] <= 0:
                                del toon.NPCFriendsDict[av]

                            toon.d_setNPCFriendsDict(toon.NPCFriendsDict)

                    elif track == PETSOS:
                        pass
                    elif track == FIRE:
                        pass
                    elif track != SOS:
                        toon = self.getToon(toonId)
                        if toon is not None:
                            check = toon.inventory.useItem(track, level)
                            if check == -1:
                                self.air.writeServerEvent(
                                    'suspicious', toonId,
                                    'Toon generating movie for non-existant gag track %s level %s'
                                    % (track, level))
                                self.notify.warning(
                                    'generating movie for non-existant gag track %s level %s! avId: %s'
                                    % (track, level, toonId))

                            toon.d_setInventory(toon.inventory.makeNetString())

                    hps = attack[TOON_HP_COL]
                    if track == SOS:
                        self.notify.debug('toon: %d called for help' % toonId)
                    elif track == NPCSOS:
                        self.notify.debug('toon: %d called for help' % toonId)
                    elif track == PETSOS:
                        self.notify.debug('toon: %d called for pet' % toonId)
                        for i in range(len(self.activeToons)):
                            toon = self.getToon(self.activeToons[i])
                            if toon is not None:
                                if i < len(hps):
                                    hp = hps[i]
                                    if hp > 0:
                                        toonHpDict[toon.doId][0] += hp

                                    self.notify.debug(
                                        'pet heal: toon: %d healed for hp: %d'
                                        % (toon.doId, hp))
                                else:
                                    self.notify.warning(
                                        'Invalid targetIndex %s in hps %s.' %
                                        (i, hps))
                            i < len(hps)

                    elif track == NPC_RESTOCK_GAGS:
                        for at in self.activeToons:
                            toon = self.getToon(at)
                            if toon is not None:
                                toon.inventory.NPCMaxOutInv(npc_level)
                                toon.d_setInventory(
                                    toon.inventory.makeNetString())
                                continue

                    elif track == HEAL:
                        if levelAffectsGroup(HEAL, level):
                            for i in range(len(self.activeToons)):
                                at = self.activeToons[i]
                                if at != toonId or attack[
                                        TOON_TRACK_COL] == NPCSOS:
                                    toon = self.getToon(at)
                                    if toon is not None:
                                        if i < len(hps):
                                            hp = hps[i]
                                        else:
                                            self.notify.warning(
                                                'Invalid targetIndex %s in hps %s.'
                                                % (i, hps))
                                            hp = 0
                                        toonHpDict[toon.doId][0] += hp
                                        self.notify.debug(
                                            'HEAL: toon: %d healed for hp: %d'
                                            % (toon.doId, hp))

                                toon is not None

                        else:
                            targetId = attack[TOON_TGT_COL]
                            toon = self.getToon(targetId)
                            if toon is not None and targetId in self.activeToons:
                                targetIndex = self.activeToons.index(targetId)
                                if targetIndex < len(hps):
                                    hp = hps[targetIndex]
                                else:
                                    self.notify.warning(
                                        'Invalid targetIndex %s in hps %s.' %
                                        (targetIndex, hps))
                                    hp = 0
                                toonHpDict[toon.doId][0] += hp

                    elif attackAffectsGroup(track, level,
                                            attack[TOON_TRACK_COL]):
                        for suit in self.activeSuits:
                            targetIndex = self.activeSuits.index(suit)
                            if targetIndex < 0 or targetIndex >= len(hps):
                                self.notify.warning(
                                    'Got attack (%s, %s) on target suit %s, but hps has only %s entries: %s'
                                    % (track, level, targetIndex, len(hps),
                                       hps))
                                continue
                            hp = hps[targetIndex]
                            if hp > 0 and track == LURE:
                                if suit.battleTrap == UBER_GAG_LEVEL_INDEX:
                                    pass
                                1
                                suit.battleTrap = NO_TRAP
                                needUpdate = 1
                                if suit.doId in trapDict:
                                    del trapDict[suit.doId]

                                if suitsLuredOntoTraps.count(suit) == 0:
                                    suitsLuredOntoTraps.append(suit)

                            if track == TRAP:
                                targetId = suit.doId
                                if targetId in trapDict:
                                    trapDict[targetId].append(attack)
                                else:
                                    trapDict[targetId] = [attack]
                                needUpdate = 1

                            died = attack[SUIT_DIED_COL] & 1 << targetIndex
                            if died != 0:
                                if deadSuits.count(suit) == 0:
                                    deadSuits.append(suit)

                            deadSuits.count(suit) == 0

                    else:
                        targetId = attack[TOON_TGT_COL]
                        target = self.findSuit(targetId)
                        if target is not None:
                            targetIndex = self.activeSuits.index(target)
                            if targetIndex < 0 or targetIndex >= len(hps):
                                self.notify.warning(
                                    'Got attack (%s, %s) on target suit %s, but hps has only %s entries: %s'
                                    % (track, level, targetIndex, len(hps),
                                       hps))
                            else:
                                hp = hps[targetIndex]
                                if track == TRAP:
                                    if targetId in trapDict:
                                        trapDict[targetId].append(attack)
                                    else:
                                        trapDict[targetId] = [attack]

                                if hp > 0 and track == LURE:
                                    oldBattleTrap = target.battleTrap
                                    if oldBattleTrap == UBER_GAG_LEVEL_INDEX:
                                        pass
                                    1
                                    target.battleTrap = NO_TRAP
                                    needUpdate = 1
                                    if target.doId in trapDict:
                                        del trapDict[target.doId]

                                    if suitsLuredOntoTraps.count(target) == 0:
                                        suitsLuredOntoTraps.append(target)

                                    if oldBattleTrap == UBER_GAG_LEVEL_INDEX:
                                        for otherSuit in self.activeSuits:
                                            if not otherSuit == target:
                                                otherSuit.battleTrap = NO_TRAP
                                                if otherSuit.doId in trapDict:
                                                    del trapDict[
                                                        otherSuit.doId]

                                            otherSuit.doId in trapDict

                                died = attack[SUIT_DIED_COL] & 1 << targetIndex
                                if died != 0:
                                    if deadSuits.count(target) == 0:
                                        deadSuits.append(target)

            track != NO_ATTACK

        self.exitedToons = []
        for suitKey in trapDict.keys():
            attackList = trapDict[suitKey]
            attack = attackList[0]
            target = self.findSuit(attack[TOON_TGT_COL])
            if attack[TOON_LVL_COL] == UBER_GAG_LEVEL_INDEX:
                targetId = suitKey
                target = self.findSuit(targetId)

            if len(attackList) == 1:
                if suitsLuredOntoTraps.count(target) == 0:
                    self.notify.debug('movieDone() - trap set')
                    target.battleTrap = attack[TOON_LVL_COL]
                    needUpdate = 1
                else:
                    target.battleTrap = NO_TRAP
            suitsLuredOntoTraps.count(target) == 0
            self.notify.debug('movieDone() - traps collided')
            if target is not None:
                target.battleTrap = NO_TRAP
                continue

        if self.battleCalc.trainTrapTriggered:
            self.notify.debug('Train trap triggered, clearing all traps')
            for otherSuit in self.activeSuits:
                self.notify.debug('suit =%d, oldBattleTrap=%d' %
                                  (otherSuit.doId, otherSuit.battleTrap))
                otherSuit.battleTrap = NO_TRAP

        currLuredSuits = self.battleCalc.getLuredSuits()
        if len(self.luredSuits) == len(currLuredSuits):
            for suit in self.luredSuits:
                if currLuredSuits.count(suit.doId) == 0:
                    needUpdate = 1
                    break
                    continue

        else:
            needUpdate = 1
        self.luredSuits = []
        for i in currLuredSuits:
            suit = self.air.doId2do[i]
            self.luredSuits.append(suit)
            self.notify.debug('movieDone() - suit: %d is lured' % i)

        for attack in npcTrapAttacks:
            (track, level,
             hp) = NPCToons.getNPCTrackLevelHp(attack[TOON_TGT_COL])
            for suit in self.activeSuits:
                if self.luredSuits.count(
                        suit) == 0 and suit.battleTrap == NO_TRAP:
                    suit.battleTrap = level
                    continue

            needUpdate = 1

        for suit in deadSuits:
            self.notify.debug('removing dead suit: %d' % suit.doId)
            if suit.isDeleted():
                self.notify.debug('whoops, suit %d is deleted.' % suit.doId)
            else:
                self.notify.debug(
                    'suit had revives? %d' % suit.getMaxSkeleRevives())
                encounter = {
                    'type': suit.dna.name,
                    'level': suit.getActualLevel(),
                    'track': suit.dna.dept,
                    'isSkelecog': suit.getSkelecog(),
                    'isForeman': suit.isForeman(),
                    'isVP': 0,
                    'isCFO': 0,
                    'isSupervisor': suit.isSupervisor(),
                    'isVirtual': suit.isVirtual(),
                    'hasRevives': suit.getMaxSkeleRevives(),
                    'activeToons': self.activeToons[:]
                }
                self.suitsKilled.append(encounter)
                self.suitsKilledThisBattle.append(encounter)
            self._DistributedBattleBaseAI__removeSuit(suit)
            needUpdate = 1
            suit.resume()

        lastActiveSuitDied = 0
        if len(self.activeSuits) == 0 and len(self.pendingSuits) == 0:
            lastActiveSuitDied = 1

        for i in range(4):
            attack = self.suitAttacks[i][SUIT_ATK_COL]
            if attack != NO_ATTACK:
                suitId = self.suitAttacks[i][SUIT_ID_COL]
                suit = self.findSuit(suitId)
                if suit is None:
                    self.notify.warning(
                        'movieDone() - suit: %d is gone!' % suitId)
                    continue

                if not hasattr(suit, 'dna') and suit.dna:
                    toonId = self.air.getAvatarIdFromSender()
                    self.notify.warning(
                        '_movieDone avoiding crash, sender=%s but suit has no dna'
                        % toonId)
                    self.air.writeServerEvent(
                        'suspicious', toonId,
                        '_movieDone avoiding crash, suit has no dna')
                    continue

                adict = getSuitAttack(suit.getStyleName(), suit.getLevel(),
                                      attack)
                hps = self.suitAttacks[i][SUIT_HP_COL]
                if adict['group'] == ATK_TGT_GROUP:
                    for activeToon in self.activeToons:
                        toon = self.getToon(activeToon)
                        if toon is not None:
                            targetIndex = self.activeToons.index(activeToon)
                            toonDied = self.suitAttacks[i][
                                TOON_DIED_COL] & 1 << targetIndex
                            if targetIndex >= len(hps):
                                self.notify.warning(
                                    'DAMAGE: toon %s is no longer in battle!' %
                                    activeToon)
                            else:
                                hp = hps[targetIndex]
                                if hp > 0:
                                    self.notify.debug(
                                        'DAMAGE: toon: %d hit for dmg: %d' %
                                        (activeToon, hp))
                                    if toonDied != 0:
                                        toonHpDict[toon.doId][2] = 1

                                    toonHpDict[toon.doId][1] += hp

                        hp > 0

                elif adict['group'] == ATK_TGT_SINGLE:
                    targetIndex = self.suitAttacks[i][SUIT_TGT_COL]
                    if targetIndex >= len(self.activeToons):
                        self.notify.warning(
                            'movieDone() - toon: %d gone!' % targetIndex)
                        break

                    toonId = self.activeToons[targetIndex]
                    toon = self.getToon(toonId)
                    toonDied = self.suitAttacks[i][
                        TOON_DIED_COL] & 1 << targetIndex
                    if targetIndex >= len(hps):
                        self.notify.warning(
                            'DAMAGE: toon %s is no longer in battle!' % toonId)
                    else:
                        hp = hps[targetIndex]
                        if hp > 0:
                            self.notify.debug(
                                'DAMAGE: toon: %d hit for dmg: %d' % (toonId,
                                                                      hp))
                            if toonDied != 0:
                                toonHpDict[toon.doId][2] = 1

                            toonHpDict[toon.doId][1] += hp

            adict['group'] == ATK_TGT_GROUP

        deadToons = []
        for activeToon in self.activeToons:
            hp = toonHpDict[activeToon]
            toon = self.getToon(activeToon)
            if toon is not None:
                self.notify.debug(
                    'AFTER ROUND: currtoonHP: %d toonMAX: %d hheal: %d damage: %d'
                    % (toon.hp, toon.maxHp, hp[0], hp[1]))
                toon.hpOwnedByBattle = 0
                hpDelta = hp[0] - hp[1]
                if hpDelta >= 0:
                    toon.toonUp(hpDelta, quietly=1)
                else:
                    toon.takeDamage(-hpDelta, quietly=1)
                if toon.hp <= 0:
                    self.notify.debug(
                        'movieDone() - toon: %d was killed' % activeToon)
                    toon.inventory.zeroInv(1)
                    deadToons.append(activeToon)

                self.notify.debug(
                    'AFTER ROUND: toon: %d setHp: %d' % (toon.doId, toon.hp))
                continue

        for deadToon in deadToons:
            self._DistributedBattleBaseAI__removeToon(deadToon)
            needUpdate = 1

        self.clearAttacks()
        self.d_setMovie()
        self.d_setChosenToonAttacks()
        self.localMovieDone(needUpdate, deadToons, deadSuits,
                            lastActiveSuitDied)

    def enterResume(self):
        for suit in self.suits:
            self.notify.info('battle done, resuming suit: %d' % suit.doId)
            if suit.isDeleted():
                self.notify.info('whoops, suit %d is deleted.' % suit.doId)
                continue
            suit.resume()

        self.suits = []
        self.joiningSuits = []
        self.pendingSuits = []
        self.adjustingSuits = []
        self.activeSuits = []
        self.luredSuits = []
        for toonId in self.toons:
            toon = simbase.air.doId2do.get(toonId)
            if toon:
                toon.b_setBattleId(0)
                messageToonReleased = 'Battle releasing toon %s' % toon.doId
                messenger.send(messageToonReleased, [toon.doId])
                continue

        for exitEvent in self.avatarExitEvents:
            self.ignore(exitEvent)

        eventMsg = {}
        for encounter in self.suitsKilledThisBattle:
            cog = encounter['type']
            level = encounter['level']
            msgName = '%s%s' % (cog, level)
            if encounter['isSkelecog']:
                msgName += '+'

            if msgName in eventMsg:
                eventMsg[msgName] += 1
                continue
            eventMsg[msgName] = 1

        msgText = ''
        for (msgName, count) in eventMsg.items():
            if msgText != '':
                msgText += ','

            msgText += '%s%s' % (count, msgName)

        self.air.writeServerEvent('battleCogsDefeated', self.doId,
                                  '%s|%s' % (msgText, self.getTaskZoneId()))

    def exitResume(self):
        pass

    def isJoinable(self):
        return self.joinableFsm.getCurrentState().getName() == 'Joinable'

    def enterJoinable(self):
        self.notify.debug('enterJoinable()')

    def exitJoinable(self):
        pass

    def enterUnjoinable(self):
        self.notify.debug('enterUnjoinable()')

    def exitUnjoinable(self):
        pass

    def isRunable(self):
        return self.runableFsm.getCurrentState().getName() == 'Runable'

    def enterRunable(self):
        self.notify.debug('enterRunable()')

    def exitRunable(self):
        pass

    def enterUnrunable(self):
        self.notify.debug('enterUnrunable()')

    def exitUnrunable(self):
        pass

    def _DistributedBattleBaseAI__estimateAdjustTime(self):
        self.needAdjust = 0
        adjustTime = 0
        if len(self.pendingSuits) > 0 or self.suitGone == 1:
            self.suitGone = 0
            pos0 = self.suitPendingPoints[0][0]
            pos1 = self.suitPoints[0][0][0]
            adjustTime = self.calcSuitMoveTime(pos0, pos1)

        if len(self.pendingToons) > 0 or self.toonGone == 1:
            self.toonGone = 0
            if adjustTime == 0:
                pos0 = self.toonPendingPoints[0][0]
                pos1 = self.toonPoints[0][0][0]
                adjustTime = self.calcToonMoveTime(pos0, pos1)

        return adjustTime

    def enterAdjusting(self):
        self.notify.debug('enterAdjusting()')
        self.timer.stop()
        self._DistributedBattleBaseAI__resetAdjustingResponses()
        self.adjustingTimer.startCallback(
            self._DistributedBattleBaseAI__estimateAdjustTime() +
            SERVER_BUFFER_TIME,
            self._DistributedBattleBaseAI__serverAdjustingDone)

    def _DistributedBattleBaseAI__serverAdjustingDone(self):
        if self.needAdjust == 1:
            self.adjustFsm.request('NotAdjusting')
            self._DistributedBattleBaseAI__requestAdjust()
        else:
            self.notify.debug('adjusting timed out on the server')
            self.ignoreAdjustingResponses = 1
            self._DistributedBattleBaseAI__adjustDone()

    def exitAdjusting(self):
        currStateName = self.fsm.getCurrentState().getName()
        if currStateName == 'WaitForInput':
            self.timer.restart()
        elif currStateName == 'WaitForJoin':
            self.b_setState('WaitForInput')

        self.adjustingTimer.stop()

    def _DistributedBattleBaseAI__addTrainTrapForNewSuits(self):
        hasTrainTrap = False
        trapInfo = None
        for otherSuit in self.activeSuits:
            if otherSuit.battleTrap == UBER_GAG_LEVEL_INDEX:
                hasTrainTrap = True
                continue

        if hasTrainTrap:
            for curSuit in self.activeSuits:
                if not curSuit.battleTrap == UBER_GAG_LEVEL_INDEX:
                    oldBattleTrap = curSuit.battleTrap
                    curSuit.battleTrap = UBER_GAG_LEVEL_INDEX
                    self.battleCalc.addTrainTrapForJoiningSuit(curSuit.doId)
                    self.notify.debug(
                        'setting traintrack trap for joining suit %d oldTrap=%s'
                        % (curSuit.doId, oldBattleTrap))
                    continue

    def _DistributedBattleBaseAI__adjustDone(self):
        for s in self.adjustingSuits:
            self.pendingSuits.remove(s)
            self.activeSuits.append(s)

        self.adjustingSuits = []
        for toon in self.adjustingToons:
            if self.pendingToons.count(toon) == 1:
                self.pendingToons.remove(toon)
            else:
                self.notify.warning(
                    'adjustDone() - toon: %d not pending!' % toon.doId)
            if self.activeToons.count(toon) == 0:
                self.activeToons.append(toon)
                self.ignoreResponses = 0
                self.sendEarnedExperience(toon)
                continue
            self.notify.warning(
                'adjustDone() - toon: %d already active!' % toon.doId)

        self.adjustingToons = []
        self._DistributedBattleBaseAI__addTrainTrapForNewSuits()
        self.d_setMembers()
        self.adjustFsm.request('NotAdjusting')
        if self.needAdjust == 1:
            self.notify.debug('__adjustDone() - need to adjust again')
            self._DistributedBattleBaseAI__requestAdjust()

    def enterNotAdjusting(self):
        self.notify.debug('enterNotAdjusting()')
        if self.movieRequested == 1:
            if len(
                    self.activeToons
            ) > 0 and self._DistributedBattleBaseAI__allActiveToonsResponded():
                self._DistributedBattleBaseAI__requestMovie()

    def exitNotAdjusting(self):
        pass

    def getPetProxyObject(self, petId, callback):
        doneEvent = 'readPet-%s' % self._getNextSerialNum()
        dbo = DatabaseObject.DatabaseObject(
            self.air, petId, doneEvent=doneEvent)
        pet = dbo.readPetProxy()

        def handlePetProxyRead(dbo, retCode, callback=callback, pet=pet):
            success = retCode == 0
            if not success:
                self.notify.warning('pet DB read failed')
                pet = None

            callback(success, pet)

        self.acceptOnce(doneEvent, handlePetProxyRead)

    def _getNextSerialNum(self):
        num = self.serialNum
        self.serialNum += 1
        return num
