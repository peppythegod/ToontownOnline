from pandac.PandaModules import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
import DistributedDoorEntityBase
from direct.fsm import FourState
from direct.fsm import ClassicFSM
from otp.level import DistributedEntity
from toontown.toonbase import TTLocalizer
from otp.level import BasicEntities
from direct.fsm import State
from otp.level import VisibilityBlocker


class DistributedDoorEntityLock(
        DistributedDoorEntityBase.LockBase,
        FourState.FourState):
    slideLeft = Vec3(-7.5, 0.0, 0.0)
    slideRight = Vec3(7.5, 0.0, 0.0)

    def __init__(
            self,
            door,
            lockIndex,
            lockedNodePath,
            leftNodePath,
            rightNodePath,
            stateIndex):
        self.door = door
        self.lockIndex = lockIndex
        self.lockedNodePath = lockedNodePath
        self.leftNodePath = leftNodePath
        self.rightNodePath = rightNodePath
        self.initialStateIndex = stateIndex
        FourState.FourState.__init__(
            self, self.stateNames, self.stateDurations)

    def delete(self):
        self.takedown()
        del self.door

    def setup(self):
        self.setLockState(self.initialStateIndex)
        del self.initialStateIndex

    def takedown(self):
        if self.track is not None:
            self.track.pause()
            self.track = None

        for i in self.states.keys():
            del self.states[i]

        self.states = []
        self.fsm = None

    def setLockState(self, stateIndex):
        if self.stateIndex != stateIndex:
            state = self.states.get(stateIndex)
            if state is not None:
                self.fsm.request(state)

    def isUnlocked(self):
        return self.isOn()

    def enterState1(self):
        FourState.FourState.enterState1(self)
        beat = self.duration * 0.050000000000000003
        slideSfx = base.loadSfx(
            'phase_9/audio/sfx/CHQ_FACT_arms_retracting.mp3')
        self.setTrack(
            Sequence(
                Wait(
                    beat * 2.0),
                Parallel(
                    SoundInterval(
                        slideSfx,
                        node=self.door.node,
                        volume=0.80000000000000004),
                    Sequence(
                        ShowInterval(
                            self.leftNodePath),
                        ShowInterval(
                            self.rightNodePath),
                        Parallel(
                            LerpPosInterval(
                                nodePath=self.leftNodePath,
                                other=self.lockedNodePath,
                                duration=beat * 16.0,
                                pos=Vec3(0.0),
                                blendType='easeIn'),
                            LerpPosInterval(
                                nodePath=self.rightNodePath,
                                other=self.lockedNodePath,
                                duration=beat * 16.0,
                                pos=Vec3(0.0),
                                blendType='easeIn')),
                        HideInterval(
                            self.leftNodePath),
                        HideInterval(
                            self.rightNodePath),
                        ShowInterval(
                            self.lockedNodePath)))))

    def enterState2(self):
        FourState.FourState.enterState2(self)
        self.setTrack(None)
        self.leftNodePath.setPos(self.lockedNodePath, Vec3(0.0))
        self.rightNodePath.setPos(self.lockedNodePath, Vec3(0.0))
        self.leftNodePath.hide()
        self.rightNodePath.hide()
        self.lockedNodePath.show()

    def enterState3(self):
        FourState.FourState.enterState3(self)
        unlockSfx = base.loadSfx('phase_9/audio/sfx/CHQ_FACT_door_unlock.mp3')
        slideSfx = base.loadSfx(
            'phase_9/audio/sfx/CHQ_FACT_arms_retracting.mp3')
        beat = self.duration * 0.050000000000000003
        self.setTrack(
            Sequence(
                Wait(
                    beat * 2),
                Parallel(
                    SoundInterval(
                        unlockSfx,
                        node=self.door.node,
                        volume=0.80000000000000004),
                    SoundInterval(
                        slideSfx,
                        node=self.door.node,
                        volume=0.80000000000000004),
                    Sequence(
                        HideInterval(
                            self.lockedNodePath),
                        ShowInterval(
                            self.leftNodePath),
                        ShowInterval(
                            self.rightNodePath),
                        Parallel(
                            LerpPosInterval(
                                nodePath=self.leftNodePath,
                                other=self.lockedNodePath,
                                duration=beat * 16,
                                pos=self.slideLeft,
                                blendType='easeOut'),
                            LerpPosInterval(
                                nodePath=self.rightNodePath,
                                other=self.lockedNodePath,
                                duration=beat * 16,
                                pos=self.slideRight,
                                blendType='easeOut')),
                        HideInterval(
                            self.leftNodePath),
                        HideInterval(
                            self.rightNodePath)))))

    def enterState4(self):
        FourState.FourState.enterState4(self)
        self.setTrack(None)
        self.leftNodePath.setPos(self.lockedNodePath, self.slideLeft)
        self.rightNodePath.setPos(self.lockedNodePath, self.slideRight)
        self.leftNodePath.hide()
        self.rightNodePath.hide()
        self.lockedNodePath.hide()


class DistributedDoorEntity(
        DistributedDoorEntityBase.DistributedDoorEntityBase,
        DistributedEntity.DistributedEntity,
        BasicEntities.NodePathAttribsProxy,
        FourState.FourState,
        VisibilityBlocker.VisibilityBlocker):

    def __init__(self, cr):
        self.innerDoorsTrack = None
        self.isVisReady = 0
        self.isOuterDoorOpen = 0
        DistributedEntity.DistributedEntity.__init__(self, cr)
        FourState.FourState.__init__(
            self, self.stateNames, self.stateDurations)
        VisibilityBlocker.VisibilityBlocker.__init__(self)
        self.locks = []

    def generate(self):
        DistributedEntity.DistributedEntity.generate(self)

    def announceGenerate(self):
        self.doorNode = hidden.attachNewNode('door-%s' % self.entId)
        DistributedEntity.DistributedEntity.announceGenerate(self)
        BasicEntities.NodePathAttribsProxy.initNodePathAttribs(self)
        self.setup()

    def disable(self):
        self.takedown()
        self.doorNode.removeNode()
        del self.doorNode
        DistributedEntity.DistributedEntity.disable(self)

    def delete(self):
        DistributedEntity.DistributedEntity.delete(self)

    def setup(self):
        self.setupDoor()
        for i in self.locks:
            i.setup()

        self.accept('exit%s' % (self.getName(),), self.exitTrigger)
        self.acceptAvatar()
        if __dev__:
            self.initWantDoors()

    def takedown(self):
        if __dev__:
            self.shutdownWantDoors()

        self.ignoreAll()
        if self.track is not None:
            self.track.finish()

        self.track = None
        if self.innerDoorsTrack is not None:
            self.innerDoorsTrack.finish()

        self.innerDoorsTrack = None
        for i in self.locks:
            i.takedown()

        self.locks = []
        self.fsm = None
        for i in self.states.keys():
            del self.states[i]

        self.states = []

    setUnlock0Event = DistributedDoorEntityBase.stubFunction
    setUnlock1Event = DistributedDoorEntityBase.stubFunction
    setUnlock2Event = DistributedDoorEntityBase.stubFunction
    setUnlock3Event = DistributedDoorEntityBase.stubFunction
    setIsOpenEvent = DistributedDoorEntityBase.stubFunction
    setIsLock0Unlocked = DistributedDoorEntityBase.stubFunction
    setIsLock1Unlocked = DistributedDoorEntityBase.stubFunction
    setIsLock2Unlocked = DistributedDoorEntityBase.stubFunction
    setIsLock3Unlocked = DistributedDoorEntityBase.stubFunction
    setIsOpen = DistributedDoorEntityBase.stubFunction
    setSecondsOpen = DistributedDoorEntityBase.stubFunction

    def acceptAvatar(self):
        self.accept('enter%s' % (self.getName(),), self.enterTrigger)

    def rejectInteract(self):
        DistributedEntity.DistributedEntity.rejectInteract(self)
        self.acceptAvatar()

    def avatarExit(self, avatarId):
        DistributedEntity.DistributedEntity.avatarExit(self, avatarId)
        self.acceptAvatar()

    def enterTrigger(self, args=None):
        messenger.send('DistributedInteractiveEntity_enterTrigger')
        self.sendUpdate('requestOpen')

    def exitTrigger(self, args=None):
        messenger.send('DistributedInteractiveEntity_exitTrigger')

    def okToUnblockVis(self):
        VisibilityBlocker.VisibilityBlocker.okToUnblockVis(self)
        self.isVisReady = 1
        self.openInnerDoors()

    def changedOnState(self, isOn):
        messenger.send(self.getOutputEventName(), [
            not isOn])

    def setLocksState(self, stateBits):
        lock0 = stateBits & 15
        lock1 = (stateBits & 240) >> 4
        lock2 = (stateBits & 3840) >> 8
        if self.isGenerated():
            s
