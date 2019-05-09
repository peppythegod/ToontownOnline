from DistributedMinigameAI import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.actor import Actor
import DivingGameGlobals
import random
import random
import types


class DistributedDivingGameAI(DistributedMinigameAI):
    fishProportions = []
    for i in range(6):
        fishProportions.append([])

    n = 100
    fishProportions[0]
    fishProportions[0].append(
        ([0, 0.80000000000000004], [0.80000000000000004, 0.90000000000000002],
         [0.90000000000000002, 1], [n, n], [n, n], [n, n]))
    fishProportions[0].append(
        ([0, 0.80000000000000004], [0.80000000000000004, 1], [n, n], [n, n],
         [n, n], [n, n]))
    fishProportions[0].append(
        ([0, 0.69999999999999996], [0.69999999999999996, 1], [n, n], [n, n],
         [n, n], [n, n]))
    fishProportions[0].append(
        ([0, 0.69999999999999996], [0.69999999999999996, 0.90000000000000002],
         [0.90000000000000002, 1], [n, n], [n, n], [n, n]))
    fishProportions[0].append(([0, 0.5], [0.5, 1], [n, n], [n, n], [n, n],
                               [n, n]))
    fishProportions[0].append(([n, 0.5], [0.5, 1], [n, n], [n, n], [n, n],
                               [n, n]))
    fishProportions[1]
    fishProportions[1].append(
        ([0, 0.80000000000000004], [0.80000000000000004, 0.90000000000000002],
         [0.90000000000000002, 1], [n, n], [n, n], [n, n]))
    fishProportions[1].append(
        ([0, 0.80000000000000004], [0.80000000000000004, 1], [n, n], [n, n],
         [n, n], [n, n]))
    fishProportions[1].append(
        ([0, 0.69999999999999996], [0.69999999999999996, 1], [n, n], [n, n],
         [n, n], [n, n]))
    fishProportions[1].append(
        ([0, 0.69999999999999996], [0.69999999999999996, 0.90000000000000002],
         [n, n], [n, n], [n, n], [0.90000000000000002, 1]))
    fishProportions[1].append(
        ([0, 0.40000000000000002], [0.40000000000000002, 0.80000000000000004],
         [n, n], [n, n], [n, n], [0.80000000000000004, 1]))
    fishProportions[1].append(
        ([n, 0.29999999999999999], [0.29999999999999999, 0.59999999999999998],
         [n, n], [n, n], [n, n], [0.59999999999999998, 1]))
    fishProportions[2]
    fishProportions[2].append(
        ([0, 0.69999999999999996], [0.69999999999999996, 0.90000000000000002],
         [0.90000000000000002, 1], [n, n], [n, n], [n, n]))
    fishProportions[2].append(
        ([0, 0.59999999999999998], [0.59999999999999998, 1], [n, n], [n, n],
         [n, n], [n, n]))
    fishProportions[2].append(
        ([0, 0.59999999999999998], [0.59999999999999998, 0.80000000000000004],
         [n, n], [0.80000000000000004, 1], [n, n], [n, n]))
    fishProportions[2].append(([0, 0.5], [0.5, 0.69999999999999996], [n, n],
                               [0.69999999999999996, 0.90000000000000002],
                               [n, n], [0.90000000000000002, 1]))
    fishProportions[2].append(
        ([0, 0.20000000000000001], [0.20000000000000001, 0.40000000000000002],
         [n, n], [0.40000000000000002, 0.75], [n, n], [0.75, 1]))
    fishProportions[2].append(
        ([n, 0.20000000000000001], [0.20000000000000001, 0.59999999999999998],
         [n, n], [0.59999999999999998,
                  0.80000000000000004], [n, n], [0.80000000000000004, 1]))
    fishProportions[3]
    fishProportions[3].append(
        ([0, 0.69999999999999996], [0.69999999999999996, 0.90000000000000002],
         [0.90000000000000002, 1], [n, n], [n, n], [n, n]))
    fishProportions[3].append(
        ([0, 0.59999999999999998], [0.59999999999999998, 1], [n, n], [n, n],
         [n, n], [n, n]))
    fishProportions[3].append(
        ([0, 0.59999999999999998], [0.59999999999999998, 0.80000000000000004],
         [n, n], [0.94999999999999996, 1], [n, n], [n, n]))
    fishProportions[3].append(([0, 0.5], [0.5, 0.69999999999999996], [n, n], [
        0.69999999999999996, 0.84999999999999998
    ], [0.90000000000000002, 0.94999999999999996], [0.94999999999999996, 1]))
    fishProportions[3].append(
        ([0, 0.20000000000000001], [0.20000000000000001, 0.40000000000000002],
         [n, n], [0.40000000000000002, 0.75], [0.75, 0.84999999999999998],
         [0.84999999999999998, 1]))
    fishProportions[3].append(
        ([n, 0.20000000000000001], [0.20000000000000001, 0.59999999999999998],
         [n, n], [0.59999999999999998,
                  0.80000000000000004], [n, n], [0.80000000000000004, 1]))
    fishProportions[4]
    fishProportions[4].append(
        ([0, 0.69999999999999996], [0.69999999999999996, 0.90000000000000002],
         [0.90000000000000002, 1], [n, n], [n, n], [n, n]))
    fishProportions[4].append(
        ([0, 0.45000000000000001], [0.45000000000000001, 0.90000000000000002],
         [n, n], [0.90000000000000002, 1], [n, n], [n, n]))
    fishProportions[4].append(
        ([0, 0.20000000000000001], [0.20000000000000001, 0.5], [n, n],
         [0.5, 0.94999999999999996], [0.94999999999999996, 1], [n, n]))
    fishProportions[4].append(
        ([0, 0.10000000000000001], [0.10000000000000001, 0.29999999999999999],
         [n, n], [0.29999999999999999, 0.75], [0.75, 0.80000000000000004],
         [0.80000000000000004, 1]))
    fishProportions[4].append(([n, n], [0, 0.14999999999999999], [n, n],
                               [0.14999999999999999, 0.40000000000000002],
                               [n, n], [0.40000000000000002, 1]))
    fishProportions[4].append(
        ([n, n], [n, n], [n, n], [0, 0.40000000000000002], [n, n],
         [0.59999999999999998, 1]))
    fishProportions[5]
    fishProportions[5].append(
        ([0, 0.69999999999999996], [0.69999999999999996, 0.90000000000000002],
         [0.90000000000000002, 1], [n, n], [n, n], [n, n]))
    fishProportions[5].append(
        ([0, 0.45000000000000001], [0.45000000000000001, 0.90000000000000002],
         [n, n], [0.90000000000000002, 1], [n, n], [n, n]))
    fishProportions[5].append(
        ([0, 0.20000000000000001], [0.20000000000000001, 0.5], [n, n],
         [0.5, 0.94999999999999996], [0.94999999999999996, 1], [n, n]))
    fishProportions[5].append(
        ([0, 0.10000000000000001], [0.10000000000000001, 0.29999999999999999],
         [n, n], [0.29999999999999999, 0.75], [0.75, 0.80000000000000004],
         [0.80000000000000004, 1]))
    fishProportions[5].append(([n, n], [0, 0.14999999999999999], [n, n],
                               [0.14999999999999999, 0.40000000000000002],
                               [n, n], [0.40000000000000002, 1]))
    fishProportions[5].append(
        ([n, n], [n, n], [n, n], [0, 0.40000000000000002], [n, n],
         [0.59999999999999998, 1]))
    difficultyPatternsAI = {
        ToontownGlobals.ToontownCentral: [3.5, fishProportions[0], 1.5],
        ToontownGlobals.DonaldsDock: [3.0, fishProportions[1], 1.8],
        ToontownGlobals.DaisyGardens:
        [2.5, fishProportions[2], 2.1000000000000001],
        ToontownGlobals.MinniesMelodyland:
        [2.0, fishProportions[3], 2.3999999999999999],
        ToontownGlobals.TheBrrrgh:
        [2.0, fishProportions[4], 2.7000000000000002],
        ToontownGlobals.DonaldsDreamland: [1.5, fishProportions[5], 3.0]
    }

    def __init__(self, air, minigameId):
        self.DistributedDivingGameAI_initialized = 1
        DistributedMinigameAI.__init__(self, air, minigameId)
        self.gameFSM = ClassicFSM.ClassicFSM('DistributedDivingGameAI', [
            State.State('inactive', self.enterInactive, self.exitInactive,
                        ['swimming']),
            State.State('swimming', self.enterSwimming, self.exitSwimming,
                        ['cleanup']),
            State.State('cleanup', self.enterCleanup, self.exitCleanup,
                        ['inactive'])
        ], 'inactive', 'inactive')
        self.addChildGameFSM(self.gameFSM)
        self._DistributedDivingGameAI__timeBase = globalClockDelta.localToNetworkTime(
            globalClock.getRealTime())

    def delete(self):
        self.notify.debug('delete')
        del self.gameFSM
        DistributedMinigameAI.delete(self)

    def setGameReady(self):
        self.notify.debug('setGameReady')
        self.sendUpdate('setTrolleyZone', [self.trolleyZone])
        for avId in self.scoreDict.keys():
            self.scoreDict[avId] = 0

        self.SPAWNTIME = self.difficultyPatternsAI[self.getSafezoneId()][0]
        self.proportion = self.difficultyPatternsAI[self.getSafezoneId()][1]
        self.REWARDMOD = self.difficultyPatternsAI[self.getSafezoneId()][2]
        DistributedMinigameAI.setGameReady(self)
        self.spawnings = []
        for i in range(DivingGameGlobals.NUM_SPAWNERS):
            self.spawnings.append(
                Sequence(
                    Func(self.spawnFish, i),
                    Wait(self.SPAWNTIME + random.random()),
                    Func(self.spawnFish, i),
                    Wait((self.SPAWNTIME - 0.5) + random.random())))
            self.spawnings[i].loop()

    def setGameStart(self, timestamp):
        self.notify.debug('setGameStart')
        DistributedMinigameAI.setGameStart(self, timestamp)
        self.gameFSM.request('swimming')
        self.scoreTracking = {}
        for avId in self.scoreDict.keys():
            self.scoreTracking[avId] = [0, 0, 0, 0, 0]

    def getCrabMoving(self, crabId, crabX, dir):
        timestamp = globalClockDelta.getFrameNetworkTime()
        rand1 = int(random.random() * 10)
        rand2 = int(random.random() * 10)
        self.sendUpdate('setCrabMoving',
                        [crabId, timestamp, rand1, rand2, crabX, dir])

    def treasureRecovered(self):
        if not hasattr(self, 'scoreTracking'):
            return None

        avId = self.air.getAvatarIdFromSender()
        if avId not in self.avIdList:
            self.air.writeServerEvent(
                'suspicious', avId,
                'DivingGameAI.treasureRecovered: invalid avId')
            return None

        timestamp = globalClockDelta.getFrameNetworkTime()
        newSpot = int(random.random() * 30)
        self.scoreTracking[avId][4] += 1
        for someAvId in self.scoreDict.keys():
            if someAvId == avId:
                self.scoreDict[avId] += 10 * self.REWARDMOD * 0.25

            self.scoreDict[someAvId] += 10 * \
                (self.REWARDMOD * 0.75 / float(len(self.scoreDict.keys())))

        self.sendUpdate('incrementScore', [avId, newSpot, timestamp])

    def hasScoreMult(self):
        return 0

    def setGameAbort(self):
        self.notify.debug('setGameAbort')
        taskMgr.remove(self.taskName('gameTimer'))
        if self.gameFSM.getCurrentState():
            self.gameFSM.request('cleanup')

        DistributedMinigameAI.setGameAbort(self)

    def gameOver(self):
        self.notify.debug('gameOver')
        self.gameFSM.request('cleanup')
        DistributedMinigameAI.gameOver(self)
        trackingString = 'MiniGame Stats : Diving Game'
        trackingString += '\nDistrict:%s' % self.getSafezoneId()
        for avId in self.scoreTracking.keys():
            trackingString = trackingString + '\navId:%s fishHits:%s crabHits:%s treasureCatches:%s treasureDrops:%s treasureRecoveries:%s Score: %s' % (
                avId, self.scoreTracking[avId][0], self.scoreTracking[avId][1],
                self.scoreTracking[avId][2], self.scoreTracking[avId][3],
                self.scoreTracking[avId][4], self.scoreDict[avId])

        self.air.writeServerEvent('MiniGame Stats', None, trackingString)

    def enterInactive(self):
        self.notify.debug('enterInactive')

    def exitInactive(self):
        pass

    def getTimeBase(self):
        return self._DistributedDivingGameAI__timeBase

    def enterSwimming(self):
        self.notify.debug('enterSwimming')
        duration = 65.0
        taskMgr.doMethodLater(duration, self.timerExpired,
                              self.taskName('gameTimer'))

    def timerExpired(self, task):
        self.notify.debug('timer expired')
        for avId in self.scoreDict.keys():
            if self.scoreDict[avId] < 5:
                self.scoreDict[avId] = 5
                continue

        self.gameOver()
        return Task.done

    def exitSwimming(self):
        for i in range(DivingGameGlobals.NUM_SPAWNERS):
            self.spawnings[i].pause()

    def enterCleanup(self):
        self.notify.debug('enterCleanup')
        for i in range(DivingGameGlobals.NUM_SPAWNERS):
            self.spawnings[i].finish()

        del self.spawnings
        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass

    def pickupTreasure(self, chestId):
        if not hasattr(self, 'scoreTracking'):
            return None

        timestamp = globalClockDelta.getFrameNetworkTime()
        avId = self.air.getAvatarIdFromSender()
        if avId not in self.avIdList:
            self.air.writeServerEvent(
                'suspicious', avId,
                'DivingGameAI.pickupTreasure: invalid avId')
            return None

        self.scoreTracking[avId][2] += 1
        self.sendUpdate('setTreasureGrabbed', [avId, chestId])

    def spawnFish(self, spawnerId):
        timestamp = globalClockDelta.getFrameNetworkTime()
        props = self.proportion[spawnerId]
        num = random.random()
        for i in range(len(props)):
            prop = props[i]
            low = prop[0]
            high = prop[1]
            if num > low and num <= high:
                offset = int(10 * random.random())
                self.sendUpdate('fishSpawn', [timestamp, i, spawnerId, offset])
                return None
                continue

    def handleCrabCollision(self, avId, status):
        if avId not in self.avIdList:
            self.air.writeServerEvent(
                'suspicious', avId,
                'DivingGameAI.handleCrabCollision: invalid avId')
            return None

        timestamp = globalClockDelta.getFrameNetworkTime()
        self.sendUpdate('setTreasureDropped', [avId, timestamp])
        self.scoreTracking[avId][1] += 1
        if status == 'normal' or status == 'treasure':
            timestamp = globalClockDelta.getFrameNetworkTime()
            self.sendUpdate('performCrabCollision', [avId, timestamp])
            if status == 'treasure':
                self.scoreTracking[avId][3] += 1

    def handleFishCollision(self, avId, spawnId, spawnerId, status):
        if avId not in self.avIdList:
            self.air.writeServerEvent(
                'suspicious', avId,
                'DivingGameAI.handleFishCollision: invalid avId')
            return None

        timestamp = globalClockDelta.getFrameNetworkTime()
        self.sendUpdate('setTreasureDropped', [avId, timestamp])
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.scoreTracking[avId][0] += 1
        if status == 'treasure':
            self.scoreTracking[avId][3] += 1

        self.sendUpdate('performFishCollision',
                        [avId, spawnId, spawnerId, timestamp])
