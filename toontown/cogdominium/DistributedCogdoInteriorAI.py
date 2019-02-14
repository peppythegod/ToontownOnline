from toontown.toonbase.ToontownBattleGlobals import *
from otp.ai.AIBaseGlobal import *
from direct.distributed.ClockDelta import *
from toontown.building.ElevatorConstants import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.distributed import DistributedObjectAI
from direct.fsm import State
from toontown.battle import DistributedBattleBldgAI
from toontown.battle import BattleBase
from direct.task import Timer
from toontown.cogdominium.DistributedCogdoElevatorIntAI import DistributedCogdoElevatorIntAI
from toontown.cogdominium.CogdoLayout import CogdoLayout
import copy
from toontown.cogdominium.DistCogdoCraneGameAI import DistCogdoCraneGameAI


class DistributedCogdoInteriorAI(DistributedObjectAI.DistributedObjectAI):
    def __init__(self, air, elevator):
        self.air = air
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        (self.extZoneId,
         self.zoneId) = elevator.bldg.getExteriorAndInteriorZoneId()
        self._numFloors = elevator.bldg.planner.numFloors
        self.layout = elevator.bldg._cogdoLayout
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
        self.bldg = elevator.bldg
        self.elevator = elevator
        self._game = None
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
                self._DistributedCogdoInteriorAI__addToon(toonId)
                continue

        self.savedByMap = {}
        self.fsm = ClassicFSM.ClassicFSM(
            'DistributedCogdoInteriorAI', [
                State.State('WaitForAllToonsInside',
                            self.enterWaitForAllToonsInside,
                            self.exitWaitForAllToonsInside, ['Elevator']),
                State.State('Elevator', self.enterElevator, self.exitElevator,
                            ['Game']),
                State.State('Game', self.enterGame, self.exitGame, ['Battle']),
                State.State('Battle', self.enterBattle, self.exitBattle,
                            ['ReservesJoining', 'BattleDone']),
                State.State('ReservesJoining', self.enterReservesJoining,
                            self.exitReservesJoining, ['Battle']),
                State.State('BattleDone', self.enterBattleDone,
                            self.exitBattleDone, ['Resting', 'Reward']),
                State.State('Resting', self.enterResting, self.exitResting,
                            ['Elevator']),
                State.State('Reward', self.enterReward, self.exitReward,
                            ['Off']),
                State.State('Off', self.enterOff, self.exitOff,
                            ['WaitForAllToonsInside'])
            ],
            'Off',
            'Off',
            onUndefTransition=ClassicFSM.ClassicFSM.ALLOW)
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
        self._cogdoLayout = None
        self._DistributedCogdoInteriorAI__cleanupFloorBattle()
        taskName = self.taskName('deleteInterior')
        taskMgr.remove(taskName)
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def requestDelete(self):
        if self._game:
            self._game.requestDelete()

        DistributedObjectAI.DistributedObjectAI.requestDelete(self)

    def addGameFSM(self, gameFSM):
        self.fsm.getStateNamed('Game').addChild(gameFSM)

    def removeGameFSM(self, gameFSM):
        self.fsm.getStateNamed('Game').removeChild(gameFSM)

    def _DistributedCogdoInteriorAI__handleUnexpectedExit(self, toonId):
        self.notify.warning('toon: %d exited unexpectedly' % toonId)
        if self._game:
            self._game.handleToonDisconnected(toonId)

        self._DistributedCogdoInteriorAI__removeToon(toonId)
        if len(self.toons) == 0:
            self.timer.stop()
            if self.fsm.getCurrentState().getName() == 'Resting':
                pass
            elif self.battle is None:
                self.bldg.deleteCogdoInterior()

    def _handleToonWentSad(self, toonId):
        self.notify.info('toon: %d went sad' % toonId)
        toon = self.air.getDo(toonId)
        if toon:
            self.ignore(toon.getGoneSadMessage())

        if self._game:
            self._game.handleToonWentSad(toonId)

        self._DistributedCogdoInteriorAI__removeToon(toonId)
        if len(self.toons) == 0:
            self.timer.stop()
            if self.fsm.getCurrentState().getName() == 'Resting':
                pass
            elif self.battle is None:
                self._sadCleanupTask = taskMgr.doMethodLater(
                    20, self._cleanupAfterLastToonWentSad,
                    self.uniqueName('sadcleanup'))

    def _cleanupAfterLastToonWentSad(self, task):
        self._sadCleanupTask = None
        self.bldg.deleteCogdoInterior()
        return task.done

    def _DistributedCogdoInteriorAI__addToon(self, toonId):
        if toonId not in self.air.doId2do:
            self.notify.warning('addToon() - no toon for doId: %d' % toonId)
            return None

        event = self.air.getAvatarExitEvent(toonId)
        self.avatarExitEvents.append(event)
        self.accept(
            event,
            self._DistributedCogdoInteriorAI__handleUnexpectedExit,
            extraArgs=[toonId])
        self.toons.append(toonId)
        self.responses[toonId] = 0

    def _DistributedCogdoInteriorAI__removeToon(self, toonId):
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

    def _DistributedCogdoInteriorAI__resetResponses(self):
        self.responses = {}
        for toon in self.toons:
            self.responses[toon] = 0

        self.ignoreResponses = 0

    def _DistributedCogdoInteriorAI__allToonsResponded(self):
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
        return self._numFloors

    def d_setToons(self):
        self.sendUpdate('setToons', self.getToons())

    def getToons(self):
        sendIds = []
        for toonId in self.toonIds:
            if toonId is None:
                sendIds.append(0)
                continue
            sendIds.append(toonId)

        return [sendIds, 0]

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

        return [suitIds, reserveIds, values]

    def b_setState(self, state):
        self.d_setState(state)
        self.setState(state)

    def d_setState(self, state):
        stime = globalClock.getRealTime() + BattleBase.SERVER_BUFFER_TIME
        self.sendUpdate(
            'setState',
            [state, globalClockDelta.localToNetworkTime(stime)])

    def setState(self, state):
        self.fsm.request(state)

    def getState(self):
        return [
            self.fsm.getCurrentState().getName(),
            globalClockDelta.getRealNetworkTime()
        ]

    def setAvatarJoined(self):
        avId = self.air.getAvatarIdFromSender()
        if self.toons.count(avId) == 0:
            self.air.writeServerEvent(
                'suspicious', avId,
                'DistributedCogdoInteriorAI.setAvatarJoined from toon not in %s.'
                % self.toons)
            self.notify.warning(
                'setAvatarJoined() - av: %d not in list' % avId)
            return None

        avatar = self.air.doId2do.get(avId)
        if avatar is not None:
            self.savedByMap[avId] = (avatar.getName(), avatar.dna.asTuple())

        self.responses[avId] += 1
        if self._DistributedCogdoInteriorAI__allToonsResponded():
            self.fsm.request('Elevator')

    def elevatorDone(self):
        toonId = self.air.getAvatarIdFromSender()
        if self.ignoreResponses == 1:
            return None
        elif self.fsm.getCurrentState().getName() != 'Elevator':
            self.notify.warning('elevatorDone() - in state: %s' %
                                self.fsm.getCurrentState().getName())
            return None
        elif self.toons.count(toonId) == 0:
            self.notify.warning(
                'elevatorDone() - toon not in toon list: %d' % toonId)
            return None

        self.responses[toonId] += 1
        if self._DistributedCogdoInteriorAI__allToonsResponded(
        ) and self.ignoreElevatorDone == 0:
            self.b_setState('Game')

    def reserveJoinDone(self):
        toonId = self.air.getAvatarIdFromSender()
        if self.ignoreResponses == 1:
            return None
        elif self.fsm.getCurrentState().getName() != 'ReservesJoining':
            self.notify.warning('reserveJoinDone() - in state: %s' %
                                self.fsm.getCurrentState().getName())
            return None
        elif self.toons.count(toonId) == 0:
            self.notify.warning(
                'reserveJoinDone() - toon not in list: %d' % toonId)
            return None

        self.responses[toonId] += 1
        if self._DistributedCogdoInteriorAI__allToonsResponded(
        ) and self.ignoreReserveJoinDone == 0:
            self.b_setState('Battle')

    def isBossFloor(self, floorNum):
        if self.layout.hasBossBattle():
            if self.layout.getBossBattleFloor() == floorNum:
                return True

        return False

    def isTopFloor(self, floorNum):
        return self.layout.getNumFloors() - 1 == floorNum

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterWaitForAllToonsInside(self):
        self._DistributedCogdoInteriorAI__resetResponses()

    def exitWaitForAllToonsInside(self):
        self._DistributedCogdoInteriorAI__resetResponses()

    def enterElevator(self):
        if self.isBossFloor(self.currentFloor):
            self._populateFloorSuits()
        else:
            self.d_setToons()
        self._DistributedCogdoInteriorAI__resetResponses()
        self._game = self._createGame()
        self.d_setState('Elevator')
        self.timer.startCallback(
            BattleBase.ELEVATOR_T + ElevatorData[ELEVATOR_NORMAL]['openTime'] +
            BattleBase.SERVER_BUFFER_TIME,
            self._DistributedCogdoInteriorAI__serverElevatorDone)

    def _createGame(self):
        game = None
        if not self.isBossFloor(self.currentFloor):
            for toonId in self.toonIds:
                if toonId:
                    toon = self.air.getDo(toonId)
                    if toon:
                        self.accept(toon.getGoneSadMessage(),
                                    Functor(self._handleToonWentSad, toonId))

            game = DistCogdoCraneGameAI(self.air, self)
            game.generateWithRequired(self.zoneId)

        return game

    def _DistributedCogdoInteriorAI__serverElevatorDone(self):
        self.ignoreElevatorDone = 1
        self.b_setState('Game')

    def exitElevator(self):
        self.timer.stop()
        self._DistributedCogdoInteriorAI__resetResponses()

    def enterGame(self):
        self.d_setState('Game')
        self.elevator.d_setFloor(self.currentFloor)
        if self._game:
            self._game.start()
        else:
            self._gameDone()

    def _populateFloorSuits(self):
        suitHandles = self.bldg.planner.genFloorSuits(self.currentFloor)
        self.suits = suitHandles['activeSuits']
        self.activeSuits = []
        for suit in self.suits:
            self.activeSuits.append(suit)

        self.reserveSuits = suitHandles['reserveSuits']
        self.d_setToons()
        self.d_setSuits()

    def _gameDone(self):
        if len(self.toons) == 0:
            return None

        if not self.isBossFloor(self.currentFloor):
            self._populateFloorSuits()

        self.b_setState('Battle')
        if self._game:
            self._game.requestDelete()
            self._game = None
            for toonId in self.toonIds:
                if toonId:
                    toon = self.air.getDo(toonId)
                    if toon:
                        self.ignore(toon.getGoneSadMessage())

    def exitGame(self):
        pass

    def _DistributedCogdoInteriorAI__createFloorBattle(self):
        if self.isBossFloor(self.currentFloor):
            bossBattle = 1
        else:
            bossBattle = 0
        self.battle = DistributedBattleBldgAI.DistributedBattleBldgAI(
            self.air,
            self.zoneId,
            self._DistributedCogdoInteriorAI__handleRoundDone,
            self._DistributedCogdoInteriorAI__handleBattleDone,
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

    def _DistributedCogdoInteriorAI__cleanupFloorBattle(self):
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

    def _DistributedCogdoInteriorAI__handleRoundDone(self, toonIds, totalHp,
                                                     deadSuits):
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
            self.fsm.request('BattleDone', [toonIds])
        else:
            self.battle.resume()

    def _DistributedCogdoInteriorAI__handleBattleDone(self, zoneId, toonIds):
        if len(toonIds) == 0:
            taskName = self.taskName('deleteInterior')
            taskMgr.doMethodLater(
                10, self._DistributedCogdoInteriorAI__doDeleteInterior,
                taskName)
        elif self.isTopFloor(self.currentFloor):
            self.setState('Reward')
        else:
            self.b_setState('Resting')

    def _DistributedCogdoInteriorAI__doDeleteInterior(self, task):
        self.bldg.deleteCogdoInterior()

    def enterBattle(self):
        if self.battle is None:
            self._DistributedCogdoInteriorAI__createFloorBattle()

    def exitBattle(self):
        pass

    def enterReservesJoining(self):
        self._DistributedCogdoInteriorAI__resetResponses()
        self.timer.startCallback(
            ElevatorData[ELEVATOR_NORMAL]['openTime'] + SUIT_HOLD_ELEVATOR_TIME
            + BattleBase.SERVER_BUFFER_TIME,
            self._DistributedCogdoInteriorAI__serverReserveJoinDone)

    def _DistributedCogdoInteriorAI__serverReserveJoinDone(self):
        self.ignoreReserveJoinDone = 1
        self.b_setState('Battle')

    def exitReservesJoining(self):
        self.timer.stop()
        self._DistributedCogdoInteriorAI__resetResponses()
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
                self._DistributedCogdoInteriorAI__removeToon(toon)

        self.d_setToons()
        if len(self.toons) == 0:
            self.bldg.deleteCogdoInterior()
        elif self.isTopFloor(self.currentFloor):
            self.battle.resume(self.currentFloor, topFloor=1)
        else:
            self.battle.resume(self.currentFloor, topFloor=0)

    def exitBattleDone(self):
        self._DistributedCogdoInteriorAI__cleanupFloorBattle()
        self.d_setSuits()

    def _DistributedCogdoInteriorAI__handleEnterElevator(self):
        self.fsm.request('Elevator')

    def enterResting(self):
        self.intElevator = DistributedCogdoElevatorIntAI(
            self.air, self, self.toons)
        self.intElevator.generateWithRequired(self.zoneId)

    def handleAllAboard(self, seats):
        if not hasattr(self, 'fsm'):
            return None

        numOfEmptySeats = seats.count(None)
        if numOfEmptySeats == 4:
            self.bldg.deleteCogdoInterior()
            return None
        elif numOfEmptySeats >= 0 and numOfEmptySeats <= 3:
            pass
        else:
            self.error('Bad number of empty seats: %s' % numOfEmptySeats)
        for toon in self.toons:
            if seats.count(toon) == 0:
                self._DistributedCogdoInteriorAI__removeToon(toon)
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
                savedBy.append([v, tuple[0], tuple[1]])
                continue

        self.bldg.fsm.request('waitForVictorsFromCogdo', [victors, savedBy])
        self.d_setState('Reward')

    def exitReward(self):
        pass
