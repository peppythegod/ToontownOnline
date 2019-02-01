from toontown.toonbase.ToontownBattleGlobals import *
from otp.ai.AIBaseGlobal import *
from direct.distributed.ClockDelta import *
from ElevatorConstants import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.distributed import DistributedObjectAI
from direct.fsm import State
from toontown.battle import DistributedBattleBldgAI
from toontown.battle import BattleBase
from direct.task import Timer
import DistributedElevatorIntAI
import copy


class DistributedSuitInteriorAI(DistributedObjectAI.DistributedObjectAI):

    def __init__(self, air, elevator):
        self.air = air
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        (self.extZoneId, self.zoneId) = elevator.bldg.getExteriorAndInteriorZoneId()
        self.numFloors = elevator.bldg.planner.numFloors
        self.avatarExitEvents = []
        self.toons = []
        self.toonSkillPtsGained = {}
        self.toonExp = {}
        self.toonOrigQuests = {}
        self.toonItems = {}
        self.toonOrigMerits = {}
        self.toonMerits = {}
        self.toonParts = {}
        self.helpfulToons = []
        self.currentFloor = 0
        self.topFloor = self.numFloors - 1
        self.bldg = elevator.bldg
        self.elevator = elevator
        self.suits = []
        self.activeSuits = []
        self.reserveSuits = []
        self.joinedReserves = []
        self.suitsKilled = []
        self.suitsKilledPerFloor = []
        self.battle = None
        self.timer = Timer.Timer()
        self.responses = {}
        self.ignoreResponses = 0
        self.ignoreElevatorDone = 0
        self.ignoreReserveJoinDone = 0
        self.toonIds = copy.copy(elevator.seats)
        for toonId in self.toonIds:
            if toonId is not None:
                self._DistributedSuitInteriorAI__addToon(toonId)
                continue

        self.savedByMap = {}
        self.fsm = ClassicFSM.ClassicFSM('DistributedSuitInteriorAI', [
            State.State('WaitForAllToonsInside', self.enterWaitForAllToonsInside, self.exitWaitForAllToonsInside, [
                'Elevator']),
            State.State('Elevator', self.enterElevator, self.exitElevator, [
                'Battle']),
            State.State('Battle', self.enterBattle, self.exitBattle, [
                'ReservesJoining',
                'BattleDone']),
            State.State('ReservesJoining', self.enterReservesJoining, self.exitReservesJoining, [
                'Battle']),
            State.State('BattleDone', self.enterBattleDone, self.exitBattleDone, [
                'Resting',
                'Reward']),
            State.State('Resting', self.enterResting, self.exitResting, [
                'Elevator']),
            State.State('Reward', self.enterReward, self.exitReward, [
                'Off']),
            State.State('Off', self.enterOff, self.exitOff, [
                'WaitForAllToonsInside'])], 'Off', 'Off', onUndefTransition=ClassicFSM.ClassicFSM.ALLOW)
        self.fsm.enterInitialState()

    def delete(self):
        self.ignoreAll()
        self.toons = []
        self.toonIds = []
        self.fsm.requestFinalState()
        del self.fsm
        del self.bldg
        del self.elevator
        self.timer.stop()
        del self.timer
        self._DistributedSuitInteriorAI__cleanupFloorBattle()
        taskName = self.taskName('deleteInterior')
        taskMgr.remove(taskName)
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def _DistributedSuitInteriorAI__handleUnexpectedExit(self, toonId):
        self.notify.warning('toon: %d exited unexpectedly' % toonId)
        self._DistributedSuitInteriorAI__removeToon(toonId)
        if len(self.toons) == 0:
            self.timer.stop()
            if self.fsm.getCurrentState().getName() == 'Resting':
                pass
            elif self.battle is None:
                self.bldg.deleteSuitInterior()

    def _DistributedSuitInteriorAI__addToon(self, toonId):
        if toonId not in self.air.doId2do:
            self.notify.warning('addToon() - no toon for doId: %d' % toonId)
            return None

        event = self.air.getAvatarExitEvent(toonId)
        self.avatarExitEvents.append(event)
        self.accept(
            event,
            self._DistributedSuitInteriorAI__handleUnexpectedExit,
            extraArgs=[toonId])
        self.toons.append(toonId)
        self.responses[toonId] = 0

    def _DistributedSuitInteriorAI__removeToon(self, toonId):
        if self.toons.count(toonId):
            self.toons.remove(toonId)

        if self.toonIds.count(toonId):
            self.toonIds[self.toonIds.index(toonId)] = None

        if toonId in self.responses:
            del self.responses[toonId]

        event = self.air.getAvatarExitEvent(toonId)
        if self.avatarExitEvents.count(event):
            self.avatarExitEvents.remove(event)

        self.ignore(event)

    def _DistributedSuitInteriorAI__resetResponses(self):
        self.responses = {}
        for toon in self.toons:
            self.responses[toon] = 0

        self.ignoreResponses = 0

    def _DistributedSuitInteriorAI__allToonsResponded(self):
        for toon in self.toons:
            if self.responses[toon] == 0:
                return 0
                continue

        self.ignoreResponses = 1
        return 1

    def getZoneId(self):
        return self.zoneId

    def getExtZoneId(self):
        return self.extZoneId

    def getDistBldgDoId(self):
        return self.bldg.getDoId()

    def getNumFloors(self):
        return self.numFloors

    def d_setToons(self):
        self.sendUpdate('setToons', self.getToons())

    def getToons(self):
        sendIds = []
        for toonId in self.toonIds:
            if toonId is None:
                sendIds.append(0)
                continue
            sendIds.append(toonId)

        return [
            sendIds,
            0]

    def d_setSuits(self):
        self.sendUpdate('setSuits', self.getSuits())

    def getSuits(self):
        suitIds = []
        for suit in self.activeSuits:
            suitIds.append(suit.doId)

        reserveIds = []
        values = []
        for info in self.reserveSuits:
            reserveIds.append(info[0].doId)
            values.append(info[1])

        return [
            suitIds,
            reserveIds,
            values]

    def b_setState(self, state):
        self.d_setState(state)
        self.setState(state)

    def d_setState(self, state):
        stime = globalClock.getRealTime() + BattleBase.SERVER_BUFFER_TIME
        self.sendUpdate('setState', [
            state,
            globalClockDelta.localToNetworkTime(stime)])

    def setState(self, state):
        self.fsm.request(state)

    def getState(self):
        return [
            self.fsm.getCurrentState().getName(),
            globalClockDelta.getRealNetworkTime()]

    def setAvatarJoined(self):
        avId = self.air.getAvatarIdFromSender()
        if self.toons.count(avId) == 0:
            self.air.writeServerEvent(
                'suspicious',
                avId,
                'DistributedSuitInteriorAI.setAvatarJoined from toon not in %s.' %
                self.toons)
            self.notify.warning(
                'setAvatarJoined() - av: %d not in list' %
                avId)
            return None

        avatar = self.air.doId2do.get(avId)
        if avatar is not None:
            self.savedByMap[avId] = (avatar.getName(), avatar.dna.asTuple())

        self.responses[avId] += 1
        if self._DistributedSuitInteriorAI__allToonsResponded():
            self.fsm.request('Elevator')

    def elevatorDone(self):
        toonId = self.air.getAvatarIdFromSender()
        if self.ignoreResponses == 1:
            return None
        elif self.fsm.getCurrentState().getName() != 'Elevator':
            self.notify.warning(
                'elevatorDone() - in state: %s' %
                self.fsm.getCurrentState().getName())
            return None
        elif self.toons.count(toonId) == 0:
            self.notify.warning(
                'elevatorDone() - toon not in toon list: %d' %
                toonId)
            return None

        self.responses[toonId] += 1
        if self._DistributedSuitInteriorAI__allToonsResponded(
        ) and self.ignoreElevatorDone == 0:
            self.b_setState('Battle')

    def reserveJoinDone(self):
        toonId = self.air.getAvatarIdFromSender()
        if self.ignoreResponses == 1:
            return None
        elif self.fsm.getCurrentState().getName() != 'ReservesJoining':
            self.notify.warning(
                'reserveJoinDone() - in state: %s' %
                self.fsm.getCurrentState().getName())
            return None
        elif self.toons.count(toonId) == 0:
            self.notify.warning(
                'reserveJoinDone() - toon not in list: %d' %
                toonId)
            return None

        self.responses[toonId] += 1
        if self._DistributedSuitInteriorAI__allToonsResponded(
        ) and self.ignoreReserveJoinDone == 0:
            self.b_setState('Battle')

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterWaitForAllToonsInside(self):
        self._DistributedSuitInteriorAI__resetResponses()

    def exitWaitForAllToonsInside(self):
        self._DistributedSuitInteriorAI__resetResponses()

    def enterElevator(self):
        suitHandles = self.bldg.planner.genFloorSuits(self.currentFloor)
        self.suits = suitHandles['activeSuits']
        self.activeSuits = []
        for suit in self.suits:
            self.activeSuits.append(suit)

        self.reserveSuits = suitHandles['reserveSuits']
        self.d_setToons()
        self.d_setSuits()
        self._DistributedSuitInteriorAI__resetResponses()
        self.d_setState('Elevator')
        self.timer.startCallback(
            BattleBase.ELEVATOR_T +
            ElevatorData[ELEVATOR_NORMAL]['openTime'] +
            BattleBase.SERVER_BUFFER_TIME,
            self._DistributedSuitInteriorAI__serverElevatorDone)

    def _DistributedSuitInteriorAI__serverElevatorDone(self):
        self.ignoreElevatorDone = 1
        self.b_setState('Battle')

    def exitElevator(self):
        self.timer.stop()
        self._DistributedSuitInteriorAI__resetResponses()

    def _DistributedSuitInteriorAI__createFloorBattle(self):
        if self.currentFloor == self.topFloor:
            bossBattle = 1
        else:
            bossBattle = 0
        self.battle = DistributedBattleBldgAI.DistributedBattleBldgAI(
            self.air,
            self.zoneId,
            self._DistributedSuitInteriorAI__handleRoundDone,
            self._DistributedSuitInteriorAI__handleBattleDone,
            bossBattle=bossBattle)
        self.battle.suitsKilled = self.suitsKilled
        self.battle.suitsKilledPerFloor = self.suitsKilledPerFloor
        self.battle.battleCalc.toonSkillPtsGained = self.toonSkillPtsGained
        self.battle.toonExp = self.toonExp
        self.battle.toonOrigQuests = self.toonOrigQuests
        self.battle.toonItems = self.toonItems
        self.battle.toonOrigMerits = self.toonOrigMerits
        self.battle.toonMerits = self.toonMerits
        self.battle.toonParts = self.toonParts
        self.battle.helpfulToons = self.helpfulToons
        self.battle.setInitialMembers(self.toons, self.suits)
        self.battle.generateWithRequired(self.zoneId)
        mult = getCreditMultiplier(self.currentFloor)
        if self.air.suitInvasionManager.getInvading():
            mult *= getInvasionMultiplier()

        self.battle.battleCalc.setSkillCreditMultiplier(mult)

    def _DistributedSuitInteriorAI__cleanupFloorBattle(self):
        for suit in self.suits:
            self.notify.debug('cleaning up floor suit: %d' % suit.doId)
            if suit.isDeleted():
                self.notify.debug('whoops, suit %d is deleted.' % suit.doId)
                continue
            suit.requestDelete()

        self.suits = []
        self.reserveSuits = []
        self.activeSuits = []
        if self.battle is not None:
            self.battle.requestDelete()

        self.battle = None

    def _DistributedSuitInteriorAI__handleRoundDone(
            self, toonIds, totalHp, deadSuits):
        totalMaxHp = 0
        for suit in self.suits:
            totalMaxHp += suit.maxHP

        for suit in deadSuits:
            self.activeSuits.remove(suit)

        if len(self.reserveSuits) > 0 and len(self.activeSuits) < 4:
            self.joinedReserves = []
            hpPercent = 100 - (totalHp / totalMaxHp) * 100.0
            for info in self.reserveSuits:
                if info[1] <= hpPercent and len(self.activeSuits) < 4:
                    self.suits.append(info[0])
                    self.activeSuits.append(info[0])
                    self.joinedReserves.append(info)
                    continue

            for info in self.joinedReserves:
                self.reserveSuits.remove(info)

            if len(self.joinedReserves) > 0:
                self.fsm.request('ReservesJoining')
                self.d_setSuits()
                return None

        if len(self.activeSuits) == 0:
            self.fsm.request('BattleDone', [
                toonIds])
        else:
            self.battle.resume()

    def _DistributedSuitInteriorAI__handleBattleDone(self, zoneId, toonIds):
        if len(toonIds) == 0:
            taskName = self.taskName('deleteInterior')
            taskMgr.doMethodLater(
                10, self._DistributedSuitInteriorAI__doDeleteInterior, taskName)
        elif self.currentFloor == self.topFloor:
            self.setState('Reward')
        else:
            self.b_setState('Resting')

    def _DistributedSuitInteriorAI__doDeleteInterior(self, task):
        self.bldg.deleteSuitInterior()

    def enterBattle(self):
        if self.battle is None:
            self._DistributedSuitInteriorAI__createFloorBattle()
            self.elevator.d_setFloor(self.currentFloor)

    def exitBattle(self):
        pass

    def enterReservesJoining(self):
        self._DistributedSuitInteriorAI__resetResponses()
        self.timer.startCallback(
            ElevatorData[ELEVATOR_NORMAL]['openTime'] +
            SUIT_HOLD_ELEVATOR_TIME +
            BattleBase.SERVER_BUFFER_TIME,
            self._DistributedSuitInteriorAI__serverReserveJoinDone)

    def _DistributedSuitInteriorAI__serverReserveJoinDone(self):
        self.ignoreReserveJoinDone = 1
        self.b_setState('Battle')

    def exitReservesJoining(self):
        self.timer.stop()
        self._DistributedSuitInteriorAI__resetResponses()
        for info in self.joinedReserves:
            self.battle.suitRequestJoin(info[0])

        self.battle.resume()
        self.joinedReserves = []

    def enterBattleDone(self, toonIds):
        if len(toonIds) != len(self.toons):
            deadToons = []
            for toon in self.toons:
                if toonIds.count(toon) == 0:
                    deadToons.append(toon)
                    continue

            for toon in deadToons:
                self._DistributedSuitInteriorAI__removeToon(toon)

        self.d_setToons()
        if len(self.toons) == 0:
            self.bldg.deleteSuitInterior()
        elif self.currentFloor == self.topFloor:
            self.battle.resume(self.currentFloor, topFloor=1)
        else:
            self.battle.resume(self.currentFloor, topFloor=0)

    def exitBattleDone(self):
        self._DistributedSuitInteriorAI__cleanupFloorBattle()

    def _DistributedSuitInteriorAI__handleEnterElevator(self):
        self.fsm.request('Elevator')

    def enterResting(self):
        self.intElevator = DistributedElevatorIntAI.DistributedElevatorIntAI(
            self.air, self, self.toons)
        self.intElevator.generateWithRequired(self.zoneId)

    def handleAllAboard(self, seats):
        if not hasattr(self, 'fsm'):
            return None

        numOfEmptySeats = seats.count(None)
        if numOfEmptySeats == 4:
            self.bldg.deleteSuitInterior()
            return None
        elif numOfEmptySeats >= 0 and numOfEmptySeats <= 3:
            pass
        else:
            self.error('Bad number of empty seats: %s' % numOfEmptySeats)
        for toon in self.toons:
            if seats.count(toon) == 0:
                self._DistributedSuitInteriorAI__removeToon(toon)
                continue

        self.toonIds = copy.copy(seats)
        self.toons = []
        for toonId in self.toonIds:
            if toonId is not None:
                self.toons.append(toonId)
                continue

        self.d_setToons()
        self.currentFloor += 1
        self.fsm.request('Elevator')

    def exitResting(self):
        self.intElevator.requestDelete()
        del self.intElevator

    def enterReward(self):
        victors = self.toonIds[:]
        savedBy = []
        for v in victors:
            tuple = self.savedByMap.get(v)
            if tuple:
                savedBy.append([
                    v,
                    tuple[0],
                    tuple[1]])
                continue

        self.bldg.fsm.request('waitForVictors', [
            victors,
            savedBy])
        self.d_setState('Reward')

    def exitReward(self):
        pass
