from otp.ai.AIBase import *
from toontown.toonbase.ToontownGlobals import *
from direct.distributed.ClockDelta import *
from direct.distributed import DistributedObjectAI
from direct.task import Task
PianoSpeeds = [
    1.0,
    2.0,
    3.0,
    4.0,
    5.0,
    6.0,
    8.0,
    10.0,
    12.0,
    14.0,
    16.0,
    18.0]
PianoMaxSpeed = PianoSpeeds[len(PianoSpeeds) - 1]
PianoSlowDownFactor = 0.69999999999999996
PianoSlowDownInterval = 10.0
PianoSlowDownMinimum = 0.10000000000000001


class DistributedMMPianoAI(DistributedObjectAI.DistributedObjectAI):

    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.spinStartTime = 0.0
        self.rpm = 0.0
        self.degreesPerSecond = (self.rpm / 60.0) * 360.0
        self.offset = 0.0
        self.direction = 1

    def delete(self):
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def requestSpeedUp(self):
        if self.rpm < PianoMaxSpeed:
            for speed in PianoSpeeds:
                if speed > self.rpm:
                    break
                    continue

            self.updateSpeed(speed, self.direction)

        self.d_playSpeedUp(self.air.getAvatarIdFromSender())
        self._DistributedMMPianoAI__slowDownLater()

    def requestChangeDirection(self):
        rpm = self.rpm
        if rpm == 0.0:
            rpm = PianoSpeeds[0]

        self.updateSpeed(rpm, -(self.direction))
        self._DistributedMMPianoAI__slowDownLater()
        self.d_playChangeDirection(self.air.getAvatarIdFromSender())

    def d_setSpeed(self, rpm, offset, startTime):
        self.sendUpdate('setSpeed', [
            rpm,
            offset,
            globalClockDelta.localToNetworkTime(startTime)])

    def d_playSpeedUp(self, avId):
        self.sendUpdate('playSpeedUp', [
            avId])

    def d_playChangeDirection(self, avId):
        self.sendUpdate('playChangeDirection', [
            avId])

    def updateSpeed(self, rpm, direction):
        now = globalClock.getRealTime()
        heading = self.degreesPerSecond * \
            (now - self.spinStartTime) + self.offset
        self.rpm = rpm
        self.direction = direction
        self.degreesPerSecond = (rpm / 60.0) * 360.0 * direction
        self.offset = heading % 360.0
        self.spinStartTime = now
        self.d_setSpeed(
            self.rpm *
            self.direction,
            self.offset,
            self.spinStartTime)

    def start(self):
        pass

    def _DistributedMMPianoAI__slowDownLater(self):
        taskName = self.uniqueName('slowDown')
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(
            PianoSlowDownInterval,
            self._DistributedMMPianoAI__slowDown,
            taskName)

    def _DistributedMMPianoAI__slowDown(self, task):
        rpm = self.rpm * PianoSlowDownFactor
        if rpm < PianoSlowDownMinimum:
            self.updateSpeed(0.0, self.direction)
        else:
            self.updateSpeed(rpm, self.direction)
            self._DistributedMMPianoAI__slowDownLater()
        return Task.done
