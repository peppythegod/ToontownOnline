from DistributedMinigameAI import *
from direct.distributed.ClockDelta import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
import TargetGameGlobals
import random
import types


def checkPlace(placeX, placeY, fillSize, placeList):
    goodPlacement = 1
    for place in placeList:
        distance = math.sqrt((place[0] - placeX) * (place[0] - placeX) +
                             (place[1] - placeY) * (place[1] - placeY))
        distance = distance - fillSize + place[2]
        if distance <= 0.0:
            goodPlacement = 0
            break
            continue

    return goodPlacement


class DistributedTargetGameAI(DistributedMinigameAI):
    def __init__(self, air, minigameId):

        try:
            pass
        except BaseException:
            self.DistributedTargetGameAI_initialized = 1
            DistributedMinigameAI.__init__(self, air, minigameId)
            self.gameFSM = ClassicFSM.ClassicFSM('DistributedTargetGameAI', [
                State.State('inactive', self.enterInactive, self.exitInactive,
                            ['fly']),
                State.State('fly', self.enterFly, self.exitFly,
                            ['cleanup', 'resetRound']),
                State.State('resetRound', self.enterResetRound,
                            self.exitResetRound, ['cleanup', 'fly']),
                State.State('cleanup', self.enterCleanup, self.exitCleanup,
                            ['inactive'])
            ], 'inactive', 'inactive')
            self.addChildGameFSM(self.gameFSM)
            self._DistributedTargetGameAI__timeBase = globalClockDelta.localToNetworkTime(
                globalClock.getRealTime())
            self.round = 2
            self.barrierScore = None
            self.scoreTrack = []

    def delete(self):
        self.notify.debug('delete')
        del self.gameFSM
        del self.scoreTrack
        if hasattr(self, 'barrierScore'):
            if self.barrierScore:
                self.barrierScore.cleanup()
                del self.barrierScore

        DistributedMinigameAI.delete(self)

    def setGameReady(self):
        self.notify.debug('setGameReady')
        self.sendUpdate('setTrolleyZone', [self.trolleyZone])
        DistributedMinigameAI.setGameReady(self)
        import time as time
        random.seed(time.time())
        seed = int(random.random() * 4000.0)
        self.sendUpdate('setTargetSeed', [seed])
        random.seed(seed)
        self.setupTargets()

    def setupTargets(self):
        fieldWidth = TargetGameGlobals.ENVIRON_WIDTH * 3
        fieldLength = TargetGameGlobals.ENVIRON_LENGTH * 3.7000000000000002
        self.pattern = TargetGameGlobals.difficultyPatterns[
            self.getSafezoneId()]
        self.targetList = self.pattern[0]
        self.targetValue = self.pattern[1]
        self.targetSize = self.pattern[2]
        self.targetColors = self.pattern[3]
        self.targetSubParts = self.pattern[4]
        highestValue = 0
        for value in self.targetValue:
            if value > highestValue:
                highestValue = value
                continue

        self.placeValue = highestValue * 0.5
        self.targetsPlaced = []
        placeList = []
        for typeIndex in range(len(self.targetList)):
            for targetIndex in range(self.targetList[typeIndex]):
                goodPlacement = 0
                while not goodPlacement:
                    placeX = random.random() * fieldWidth * 0.59999999999999998 - \
                        fieldWidth * 0.59999999999999998 * 0.5
                    placeY = (random.random() * 0.59999999999999998 + 0.0 +
                              0.40000000000000002 *
                              (self.placeValue * 1.0 / highestValue * 1.0)
                              ) * fieldLength
                    fillSize = self.targetSize[typeIndex]
                    goodPlacement = checkPlace(placeX, placeY, fillSize,
                                               placeList)
                placeList.append((placeX, placeY, fillSize))
                subIndex = self.targetSubParts[typeIndex]
                while subIndex:
                    combinedIndex = typeIndex + subIndex - 1
                    self.targetsPlaced.append((placeX, placeY, combinedIndex))
                    subIndex -= 1

    def setGameStart(self, timestamp):
        self.notify.debug('setGameStart')
        for avId in self.scoreDict.keys():
            self.scoreDict[avId] = 0

        DistributedMinigameAI.setGameStart(self, timestamp)
        self.gameFSM.request('fly')

    def setScore(self, scoreX, scoreY, other=None):
        avId = self.air.getAvatarIdFromSender()
        if avId not in self.avIdList:
            self.air.writeServerEvent('suspicious', avId,
                                      'RingGameAI.setScore: invalid avId')
            return None

        topValue = 0
        hitTarget = None
        for target in self.targetsPlaced:
            radius = self.targetSize[target[2]]
            value = self.targetValue[target[2]]
            posX = target[0]
            posY = target[1]
            dx = posX - scoreX
            dy = posY - scoreY
            distance = math.sqrt(dx * dx + dy * dy)
            if distance < radius and topValue < value:
                topValue = value
                hitTarget = target
                hitX = posX
                hitY = posY
                continue

        if self.scoreDict[avId] < topValue:
            self.scoreDict[avId] = topValue
            self.sendUpdate('setSingleScore', [topValue, avId])

    def setGameAbort(self):
        self.notify.debug('setGameAbort')
        if self.gameFSM.getCurrentState():
            self.gameFSM.request('cleanup')

        DistributedMinigameAI.setGameAbort(self)

    def gameOver(self):
        self.notify.debug('gameOver')
        self.gameFSM.request('cleanup')
        DistributedMinigameAI.gameOver(self)

    def enterInactive(self):
        self.notify.debug('enterInactive')

    def exitInactive(self):
        pass

    def getTimeBase(self):
        return self._DistributedTargetGameAI__timeBase

    def enterFly(self):
        self.notify.debug('enterFly')
        self.barrierScore = ToonBarrier(
            'waitClientsScore', self.uniqueName('waitClientsScore'),
            self.avIdList, 120, self.allAvatarsScore, self.handleTimeout)

    def exitFly(self):
        pass

    def handleTimeout(self, other=None):
        pass

    def allAvatarsScore(self, other=None):
        if self.round == 0:
            self.gameOver()
        else:
            self.round -= 1
            self.gameFSM.request('resetRound')

    def getScoreList(self):
        scoreList = [0, 0, 0, 0]
        avList = [0, 0, 0, 0]
        scoreIndex = 0
        for avId in self.scoreDict.keys():
            scoreList[scoreIndex] = self.scoreDict[avId]
            avList[scoreIndex] = avId
            scoreIndex += 1

        return scoreList

    def enterResetRound(self):
        scoreList = self.getScoreList()
        self.scoreTrack.append(scoreList)
        self.sendUpdate('setRoundDone', [])
        self.barrierScore.cleanup()
        del self.barrierScore
        taskMgr.doMethodLater(0.10000000000000001, self.gotoFly,
                              self.taskName('roundReset'))

    def exitResetRound(self):
        pass

    def gotoFly(self, extra=None):
        if hasattr(self, 'gameFSM'):
            self.gameFSM.request('fly')

    def enterCleanup(self):
        self.notify.debug('enterCleanup')
        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass

    def setPlayerDone(self, other=None):
        if not hasattr(self, 'barrierScore') or self.barrierScore is None:
            return None

        avId = self.air.getAvatarIdFromSender()
        self.barrierScore.clear(avId)
        for avId in self.stateDict.keys():
            if self.stateDict[avId] == EXITED:
                self.barrierScore.clear(avId)
                continue

    def gameOver(self):
        self.notify.debug('gameOver')
        for entry in self.scoreDict:
            if self.scoreDict[entry] == 0:
                self.scoreDict[entry] = 1
                continue

        self.scoreTrack.append(self.getScoreList())
        statMessage = 'MiniGame Stats : Target Game' + '\nScores' + '%s' % self.scoreTrack + \
            '\nAvIds' + '%s' % self.scoreDict.keys() + '\nSafeZone' + '%s' % self.getSafezoneId()
        self.air.writeServerEvent('MiniGame Stats', None, statMessage)
        self.sendUpdate('setGameDone', [])
        self.gameFSM.request('cleanup')
        DistributedMinigameAI.gameOver(self)

    def hasScoreMult(self):
        return 0
