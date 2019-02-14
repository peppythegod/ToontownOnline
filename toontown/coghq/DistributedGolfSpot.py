import math
from pandac.PandaModules import Point3, CollisionSphere, CollisionNode, CollisionHandlerEvent, TextNode, VBase4, SmoothMover, NodePath, BitMask32
from direct.fsm import FSM
from direct.distributed import DistributedObject
from direct.distributed.ClockDelta import globalClockDelta
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import DGG, DirectButton, DirectLabel, DirectWaitBar
from direct.interval.IntervalGlobal import Sequence, Wait, ActorInterval, Parallel, Func, LerpPosInterval, LerpHprInterval, ProjectileInterval, LerpScaleInterval, SoundInterval
from direct.showbase import PythonUtil
from direct.task import Task
from toontown.golf import GolfGlobals
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer


class DistributedGolfSpot(DistributedObject.DistributedObject, FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGolfSpot')
    positions = ((-45, 100, GolfGlobals.GOLF_BALL_RADIUS),
                 (-15, 100, GolfGlobals.GOLF_BALL_RADIUS),
                 (15, 100, GolfGlobals.GOLF_BALL_RADIUS),
                 (45, 100, GolfGlobals.GOLF_BALL_RADIUS))
    toonGolfOffsetPos = Point3(-2, 0, -(GolfGlobals.GOLF_BALL_RADIUS))
    toonGolfOffsetHpr = Point3(-90, 0, 0)
    rotateSpeed = 20
    golfPowerSpeed = base.config.GetDouble('golf-power-speed', 3)
    golfPowerExponent = base.config.GetDouble('golf-power-exponent', 0.75)

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        FSM.FSM.__init__(self, 'DistributedGolfSpot')
        self.boss = None
        self.index = None
        self.avId = 0
        self.toon = None
        self.golfSpotSmoother = SmoothMover()
        self.golfSpotSmoother.setSmoothMode(SmoothMover.SMOn)
        self.smoothStarted = 0
        self._DistributedGolfSpot__broadcastPeriod = 0.20000000000000001
        if self.index > len(self.positions):
            self.notify.error('Invalid index %d' % index)

        self.fadeTrack = None
        self.setupPowerBar()
        self.aimStart = None
        self.golfSpotAdviceLabel = None
        self.changeSeq = 0
        self.lastChangeSeq = 0
        self.controlKeyAllowed = False
        self.flyBallTracks = {}
        self.splatTracks = {}
        self._DistributedGolfSpot__flyBallBubble = None
        self.flyBallHandler = None
        self._DistributedGolfSpot__flyBallSequenceNum = 0
        self.swingInterval = None
        self.lastHitSequenceNum = -1
        self.goingToReward = False
        self.gotHitByBoss = False
        self.releaseTrack = None
        self.grabTrack = None
        self.restoreScaleTrack = None

    def setBossCogId(self, bossCogId):
        self.bossCogId = bossCogId
        self.boss = base.cr.doId2do[bossCogId]
        self.boss.setGolfSpot(self, self.index)

    def setIndex(self, index):
        self.index = index

    def disable(self):
        DistributedObject.DistributedObject.disable(self)
        self.ignoreAll()

    def delete(self):
        DistributedObject.DistributedObject.delete(self)
        self.ignoreAll()
        self.boss = None

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.triggerName = self.uniqueName('trigger')
        self.triggerEvent = 'enter%s' % self.triggerName
        self.smoothName = self.uniqueName('golfSpotSmooth')
        self.golfSpotAdviceName = self.uniqueName('golfSpotAdvice')
        self.posHprBroadcastName = self.uniqueName('golfSpotBroadcast')
        self.ballPowerTaskName = self.uniqueName('updateGolfPower')
        self.adjustClubTaskName = self.uniqueName('adjustClub')
        self.loadAssets()
        self.accept('flyBallHit-%d' % self.index,
                    self._DistributedGolfSpot__flyBallHit)

    def loadAssets(self):
        self.root = render.attachNewNode('golfSpot-%d' % self.index)
        self.root.setPos(*self.positions[self.index])
        self.ballModel = loader.loadModel('phase_6/models/golf/golf_ball')
        self.ballColor = VBase4(1, 1, 1, 1)
        if self.index < len(GolfGlobals.PlayerColors):
            self.ballColor = VBase4(*GolfGlobals.PlayerColors[self.index])
            self.ballModel.setColorScale(self.ballColor)

        self.ballModel.reparentTo(self.root)
        self.club = loader.loadModel('phase_6/models/golf/putter')
        self.clubLookatSpot = self.root.attachNewNode('clubLookat')
        self.clubLookatSpot.setY(
            -(GolfGlobals.GOLF_BALL_RADIUS + 0.10000000000000001))
        cs = CollisionSphere(0, 0, 0, 1)
        cs.setTangible(0)
        cn = CollisionNode(self.triggerName)
        cn.addSolid(cs)
        cn.setIntoCollideMask(ToontownGlobals.WallBitmask)
        self.trigger = self.root.attachNewNode(cn)
        self.trigger.stash()
        self.hitBallSfx = loader.loadSfx('phase_6/audio/sfx/Golf_Hit_Ball.mp3')

    def cleanup(self):
        if self.swingInterval:
            self.swingInterval.finish()
            self.swingInterval = None

        if self.releaseTrack:
            self.releaseTrack.finish()
            self.releaseTrack = None

        flyTracks = self.flyBallTracks.values()
        for track in flyTracks:
            track.finish()

        if self.fadeTrack:
            self.fadeTrack.finish()
            self.fadeTrack = None

        if self.restoreScaleTrack:
            self.restoreScaleTrack.finish()
            self.restoreScaleTrack = None

        self.root.removeNode()
        self.ballModel.removeNode()
        self.club.removeNode()
        if self.powerBar:
            self.powerBar.destroy()
            self.powerBar = None

        taskMgr.remove(self.triggerName)
        self.boss = None

    def setState(self, state, avId, extraInfo):
        if not self.isDisabled():
            self.gotHitByBoss = extraInfo
            if state == 'C':
                self.demand('Controlled', avId)
            elif state == 'F':
                self.demand('Free')
            elif state == 'O':
                self.demand('Off')
            else:
                self.notify.error('Invalid state from AI: %s' % state)

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterFree(self):
        if self.fadeTrack:
            self.fadeTrack.finish()
            self.fadeTrack = None

        self.restoreScaleTrack = Sequence(
            Wait(6), self.getRestoreScaleInterval(), name='restoreScaleTrack')
        self.restoreScaleTrack.start()
        if self.avId == localAvatar.doId:
            if not self.isDisabled():
                self.ballModel.setAlphaScale(0.29999999999999999)
                self.ballModel.setTransparency(1)
                taskMgr.doMethodLater(5,
                                      self._DistributedGolfSpot__allowDetect,
                                      self.triggerName)
                self.fadeTrack = Sequence(
                    Func(self.ballModel.setTransparency, 1),
                    self.ballModel.colorScaleInterval(
                        0.20000000000000001,
                        VBase4(1, 1, 1, 0.29999999999999999)),
                    name='fadeTrack-enterFree')
                self.fadeTrack.start()

        else:
            self.trigger.unstash()
            self.accept(self.triggerEvent,
                        self._DistributedGolfSpot__hitTrigger)
        self.avId = 0

    def exitFree(self):
        if self.fadeTrack:
            self.fadeTrack.finish()
            self.fadeTrack = None

        self.restoreScaleTrack.finish()
        self.restoreScaleTrack = None
        taskMgr.remove(self.triggerName)
        self.ballModel.clearTransparency()
        self.trigger.stash()
        self.ignore(self.triggerEvent)

    def enterControlled(self, avId):
        self.avId = avId
        toon = base.cr.doId2do.get(avId)
        if not toon:
            return None

        self.enableControlKey()
        self.toon = toon
        self.grabTrack = self.makeToonGrabInterval(toon)
        if avId == localAvatar.doId:
            self.boss.toCraneMode()
            camera.reparentTo(self.root)
            camera.setPosHpr(0, -10, 3, 0, 0, 0)
            localAvatar.setPos(self.root, self.toonGolfOffsetPos)
            localAvatar.setHpr(self.root, self.toonGolfOffsetHpr)
            localAvatar.sendCurrentPosition()
            self._DistributedGolfSpot__enableControlInterface()
            self.startPosHprBroadcast()
            self.accept('exitCrane', self.gotBossZapped)

        self.grabTrack.start()

    def exitControlled(self):
        self.grabTrack.finish()
        del self.grabTrack
        if self.swingInterval:
            self.swingInterval.finish()
            self.swingInterval = None

        if not self.ballModel.isEmpty():
            if self.ballModel.isHidden():
                self.notify.debug(
                    'ball is hidden scale =%s' % self.ballModel.getScale())
            else:
                self.notify.debug(
                    'ball is showing scale=%s' % self.ballModel.getScale())

        if self.toon and not self.toon.isDisabled():
            self.toon.startSmooth()

        self.releaseTrack = self.makeToonReleaseInterval(self.toon)
        self.stopPosHprBroadcast()
        self.stopSmooth()
        if self.avId == localAvatar.doId:
            self._DistributedGolfSpot__disableControlInterface()
            if not self.goingToReward:
                camera.reparentTo(base.localAvatar)
                camera.setPos(base.localAvatar.cameraPositions[0][0])
                camera.setHpr(0, 0, 0)

        self.stopAdjustClubTask()
        self.releaseTrack.start()
        self.enableControlKey()

    def _DistributedGolfSpot__allowDetect(self, task):
        if self.fadeTrack:
            self.fadeTrack.finish()

        self.fadeTrack = Sequence(
            self.ballModel.colorScaleInterval(0.20000000000000001,
                                              self.ballColor),
            Func(self.ballModel.clearTransparency),
            name='fadeTrack-allowDetect')
        self.fadeTrack.start()
        self.trigger.unstash()
        self.accept(self.triggerEvent, self._DistributedGolfSpot__hitTrigger)

    def _DistributedGolfSpot__hitTrigger(self, event):
        self.d_requestControl()

    def getRestoreScaleInterval(self):
        return Sequence()

    def d_requestControl(self):
        self.sendUpdate('requestControl')

    def d_requestFree(self, gotHitByBoss):
        self.sendUpdate('requestFree', [gotHitByBoss])

    def makeToonGrabInterval(self, toon):
        origPos = toon.getPos(self.root)
        origHpr = toon.getHpr(self.root)
        a = self.accomodateToon(toon)
        newPos = toon.getPos()
        newHpr = toon.getHpr()
        origHpr.setX(PythonUtil.fitSrcAngle2Dest(origHpr[0], newHpr[0]))
        self.notify.debug('toon.setPosHpr %s %s' % (origPos, origHpr))
        toon.setPosHpr(origPos, origHpr)
        walkTime = 0.20000000000000001
        reach = Sequence()
        if reach.getDuration() < walkTime:
            reach = Sequence(
                ActorInterval(
                    toon,
                    'walk',
                    loop=1,
                    duration=walkTime - reach.getDuration()), reach)

        i = Sequence(
            Parallel(
                toon.posInterval(walkTime, newPos, origPos),
                toon.hprInterval(walkTime, newHpr, origHpr), reach),
            Func(toon.stopLookAround))
        if toon == base.localAvatar:
            i.append(Func(self.switchToAnimState, 'GolfPuttLoop'))

        i.append(Func(self.startAdjustClubTask))
        i = Parallel(i, a)
        return i

    def accomodateToon(self, toon):
        toon.wrtReparentTo(self.root)
        toon.setPos(self.toonGolfOffsetPos)
        toon.setHpr(self.toonGolfOffsetHpr)
        return Sequence()

    def switchToAnimState(self, animStateName, forced=False):
        curAnimState = base.localAvatar.animFSM.getCurrentState()
        curAnimStateName = ''
        if curAnimState:
            curAnimStateName = curAnimState.getName()

        if curAnimStateName != animStateName or forced:
            base.localAvatar.b_setAnimState(animStateName)

    def _DistributedGolfSpot__enableControlInterface(self):
        gui = loader.loadModel('phase_3.5/models/gui/avatar_panel_gui')
        self.closeButton = DirectButton(
            image=(gui.find('**/CloseBtn_UP'), gui.find('**/CloseBtn_DN'),
                   gui.find('**/CloseBtn_Rllvr'), gui.find('**/CloseBtn_UP')),
            relief=None,
            scale=2,
            text=TTLocalizer.BossbotGolfSpotLeave,
            text_scale=0.040000000000000001,
            text_pos=(0, -0.070000000000000007),
            text_fg=VBase4(1, 1, 1, 1),
            pos=(1.05, 0, -0.81999999999999995),
            command=self._DistributedGolfSpot__exitGolfSpot)
        self.accept('escape', self._DistributedGolfSpot__exitGolfSpot)
        self.accept('control', self._DistributedGolfSpot__controlPressed)
        self.accept('control-up', self._DistributedGolfSpot__controlReleased)
        self.accept('InputState-forward', self._DistributedGolfSpot__upArrow)
        self.accept('InputState-reverse', self._DistributedGolfSpot__downArrow)
        self.accept('InputState-turnLeft',
                    self._DistributedGolfSpot__leftArrow)
        self.accept('InputState-turnRight',
                    self._DistributedGolfSpot__rightArrow)
        taskMgr.add(self._DistributedGolfSpot__watchControls,
                    'watchGolfSpotControls')
        taskMgr.doMethodLater(5,
                              self._DistributedGolfSpot__displayGolfSpotAdvice,
                              self.golfSpotAdviceName)
        self.arrowVert = 0
        self.arrowHorz = 0
        if self.powerBar:
            self.powerBar.show()

    def _DistributedGolfSpot__disableControlInterface(self):
        if self.closeButton:
            self.closeButton.destroy()
            self.closeButton = None

        self._DistributedGolfSpot__cleanupGolfSpotAdvice()
        self.ignore('escape')
        self.ignore('control')
        self.ignore('control-up')
        self.ignore('InputState-forward')
        self.ignore('InputState-reverse')
        self.ignore('InputState-turnLeft')
        self.ignore('InputState-turnRight')
        self.arrowVert = 0
        self.arrowHorz = 0
        taskMgr.remove('watchGolfSpotControls')
        if self.powerBar:
            self.powerBar.hide()
        else:
            self.notify.debug('self.powerBar is none')

    def setupPowerBar(self):
        self.powerBar = DirectWaitBar(
            pos=(0.0, 0, -0.93999999999999995),
            relief=DGG.SUNKEN,
            frameSize=(-2.0, 2.0, -0.20000000000000001, 0.20000000000000001),
            borderWidth=(0.02, 0.02),
            scale=0.25,
            range=100,
            sortOrder=50,
            frameColor=(0.5, 0.5, 0.5, 0.5),
            barColor=(1.0, 0.0, 0.0, 1.0),
            text='',
            text_scale=0.26000000000000001,
            text_fg=(1, 1, 1, 1),
            text_align=TextNode.ACenter,
            text_pos=(0, -0.050000000000000003))
        self.power = 0
        self.powerBar['value'] = self.power
        self.powerBar.hide()

    def resetPowerBar(self):
        self.power = 0
        self.powerBar['value'] = self.power
        self.powerBar['text'] = ''

    def _DistributedGolfSpot__displayGolfSpotAdvice(self, task):
        if self.golfSpotAdviceLabel is None:
            self.golfSpotAdviceLabel = DirectLabel(
                text=TTLocalizer.BossbotGolfSpotAdvice,
                text_fg=VBase4(1, 1, 1, 1),
                text_align=TextNode.ACenter,
                relief=None,
                pos=(0, 0, 0.68999999999999995),
                scale=0.10000000000000001)

    def _DistributedGolfSpot__cleanupGolfSpotAdvice(self):
        if self.golfSpotAdviceLabel:
            self.golfSpotAdviceLabel.destroy()
            self.golfSpotAdviceLabel = None

        taskMgr.remove(self.golfSpotAdviceName)

    def showExiting(self):
        if self.closeButton:
            self.closeButton.destroy()
            self.closeButton = DirectLabel(
                relief=None,
                text=TTLocalizer.BossbotGolfSpotLeaving,
                pos=(1.05, 0, -0.88),
                text_pos=(0, 0),
                text_scale=0.059999999999999998,
                text_fg=VBase4(1, 1, 1, 1))

        self._DistributedGolfSpot__cleanupGolfSpotAdvice()

    def _DistributedGolfSpot__exitGolfSpot(self):
        self.d_requestFree(False)

    def _DistributedGolfSpot__controlPressed(self):
        if self.controlKeyAllowed:
            self._DistributedGolfSpot__beginFireBall()

    def _DistributedGolfSpot__controlReleased(self):
        if self.controlKeyAllowed:
            self._DistributedGolfSpot__endFireBall()

    def _DistributedGolfSpot__upArrow(self, pressed):
        self._DistributedGolfSpot__incrementChangeSeq()
        self._DistributedGolfSpot__cleanupGolfSpotAdvice()
        if pressed:
            self.arrowVert = 1
        elif self.arrowVert > 0:
            self.arrowVert = 0

    def _DistributedGolfSpot__downArrow(self, pressed):
        self._DistributedGolfSpot__incrementChangeSeq()
        self._DistributedGolfSpot__cleanupGolfSpotAdvice()
        if pressed:
            self.arrowVert = -1
        elif self.arrowVert < 0:
            self.arrowVert = 0

    def _DistributedGolfSpot__rightArrow(self, pressed):
        self._DistributedGolfSpot__incrementChangeSeq()
        self._DistributedGolfSpot__cleanupGolfSpotAdvice()
        if pressed:
            self.arrowHorz = 1
            self.switchToAnimState('GolfRotateLeft')
        elif self.arrowHorz > 0:
            self.arrowHorz = 0
            self.switchToAnimState('GolfPuttLoop')

    def _DistributedGolfSpot__leftArrow(self, pressed):
        self._DistributedGolfSpot__incrementChangeSeq()
        self._DistributedGolfSpot__cleanupGolfSpotAdvice()
        if pressed:
            self.arrowHorz = -1
            self.switchToAnimState('GolfRotateRight')
        elif self.arrowHorz < 0:
            self.arrowHorz = 0
            self.switchToAnimState('GolfPuttLoop')

    def _DistributedGolfSpot__watchControls(self, task):
        if self.arrowHorz:
            self._DistributedGolfSpot__moveGolfSpot(self.arrowHorz)

        return Task.cont

    def _DistributedGolfSpot__moveGolfSpot(self, xd):
        dt = globalClock.getDt()
        h = self.root.getH() - xd * self.rotateSpeed * dt
        h %= 360
        limitH = h
        self.root.setH(limitH)

    def _DistributedGolfSpot__incrementChangeSeq(self):
        self.changeSeq = self.changeSeq + 1 & 255

    def _DistributedGolfSpot__beginFireBall(self):
        if self.aimStart is not None:
            return None

        if not self.state == 'Controlled':
            return None

        if not self.avId == localAvatar.doId:
            return None

        time = globalClock.getFrameTime()
        self.aimStart = time
        messenger.send('wakeup')
        taskMgr.add(self._DistributedGolfSpot__updateBallPower,
                    self.ballPowerTaskName)

    def _DistributedGolfSpot__endFireBall(self):
        if self.aimStart is None:
            return None

        if not self.state == 'Controlled':
            return None

        if not self.avId == localAvatar.doId:
            return None

        taskMgr.remove(self.ballPowerTaskName)
        self.disableControlKey()
        messenger.send('wakeup')
        self.aimStart = None
        power = self.power
        angle = self.root.getH()
        self.notify.debug('incrementing self.__flyBallSequenceNum')
        self._DistributedGolfSpot__flyBallSequenceNum = (
            self._DistributedGolfSpot__flyBallSequenceNum + 1) % 255
        self.sendSwingInfo(power, angle,
                           self._DistributedGolfSpot__flyBallSequenceNum)
        self.setSwingInfo(power, angle,
                          self._DistributedGolfSpot__flyBallSequenceNum)
        self.resetPowerBar()

    def _DistributedGolfSpot__updateBallPower(self, task):
        if not self.powerBar:
            print '### no power bar!!!'
            return task.done

        newPower = self._DistributedGolfSpot__getBallPower(
            globalClock.getFrameTime())
        self.power = newPower
        self.powerBar['value'] = newPower
        return task.cont

    def _DistributedGolfSpot__getBallPower(self, time):
        elapsed = max(time - self.aimStart, 0.0)
        t = elapsed / self.golfPowerSpeed
        t = math.pow(t, self.golfPowerExponent)
        power = int(t * 100) % 200
        if power > 100:
            power = 200 - power

        return power

    def stopPosHprBroadcast(self):
        taskName = self.posHprBroadcastName
        taskMgr.remove(taskName)

    def startPosHprBroadcast(self):
        taskName = self.posHprBroadcastName
        self.b_clearSmoothing()
        self.d_sendGolfSpotPos()
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(self._DistributedGolfSpot__broadcastPeriod,
                              self._DistributedGolfSpot__posHprBroadcast,
                              taskName)

    def _DistributedGolfSpot__posHprBroadcast(self, task):
        self.d_sendGolfSpotPos()
        taskName = self.posHprBroadcastName
        taskMgr.doMethodLater(self._DistributedGolfSpot__broadcastPeriod,
                              self._DistributedGolfSpot__posHprBroadcast,
                              taskName)
        return Task.done

    def d_sendGolfSpotPos(self):
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.sendUpdate(
            'setGolfSpotPos',
            [self.changeSeq, self.root.getH(), timestamp])

    def setGolfSpotPos(self, changeSeq, h, timestamp):
        self.changeSeq = changeSeq
        if self.smoothStarted:
            now = globalClock.getFrameTime()
            local = globalClockDelta.networkToLocalTime(timestamp, now)
            self.golfSpotSmoother.setH(h)
            self.golfSpotSmoother.setTimestamp(local)
            self.golfSpotSmoother.markPosition()
        else:
            self.root.setH(h)

    def b_clearSmoothing(self):
        self.d_clearSmoothing()
        self.clearSmoothing()

    def d_clearSmoothing(self):
        self.sendUpdate('clearSmoothing', [0])

    def clearSmoothing(self, bogus=None):
        self.golfSpotSmoother.clearPositions(1)

    def doSmoothTask(self, task):
        self.golfSpotSmoother.computeAndApplySmoothHpr(self.root)
        return Task.cont

    def startSmooth(self):
        if not self.smoothStarted:
            taskName = self.smoothName
            taskMgr.remove(taskName)
            self.reloadPosition()
            taskMgr.add(self.doSmoothTask, taskName)
            self.smoothStarted = 1

    def stopSmooth(self):
        if self.smoothStarted:
            taskName = self.smoothName
            taskMgr.remove(taskName)
            self.forceToTruePosition()
            self.smoothStarted = 0

    def makeToonReleaseInterval(self, toon):
        def getSlideToPos(toon=toon):
            return render.getRelativePoint(toon, Point3(0, -5, 0))

        if self.gotHitByBoss:
            grabIval = Sequence(
                Func(self.detachClub),
                name='makeToonReleaseInterval-gotHitByBoss')
            if not toon.isEmpty():
                toonIval = Sequence(
                    Func(toon.wrtReparentTo, render),
                    Parallel(
                        ActorInterval(toon, 'slip-backward'),
                        toon.posInterval(0.5, getSlideToPos, fluid=1)),
                    name='makeToonReleaseInterval-toonIval')
                grabIval.append(toonIval)

        else:
            grabIval = Sequence(Func(self.detachClub))
            if not toon.isEmpty():
                toonIval = Sequence(
                    Parallel(
                        ActorInterval(
                            toon, 'walk', duration=1.0, playRate=-1.0),
                        LerpPosInterval(
                            toon, duration=1.0, pos=Point3(-10, 0, 0))),
                    Func(toon.wrtReparentTo, render))
                grabIval.append(toonIval)

        if localAvatar.doId == toon.doId:
            if not (self.goingToReward) and toon.hp > 0:
                grabIval.append(Func(self.goToFinalBattle))
                grabIval.append(
                    Func(self.notify.debug, 'goingToFinalBattlemode'))
                grabIval.append(Func(self.safeBossToFinalBattleMode))

        return grabIval

    def safeBossToFinalBattleMode(self):
        if self.boss:
            self.boss.toFinalBattleMode()

    def goToFinalBattle(self):
        if self.cr:
            place = self.cr.playGame.getPlace()
            if place and hasattr(place, 'fsm'):
                curState = place.fsm.getCurrentState().getName()
                if place.fsm.getCurrentState().getName() == 'crane':
                    place.setState('finalBattle')
                else:
                    self.notify.debug(
                        'NOT going to final battle, state=%s' % curState)

    def attachClub(self, avId, pointToBall=False):
        club = self.club
        if club:
            av = base.cr.doId2do.get(avId)
            if av:
                av.useLOD(1000)
                lHand = av.getLeftHands()[0]
                club.setPos(0, 0, 0)
                club.reparentTo(lHand)
                netScale = club.getNetTransform().getScale()[1]
                counterActToonScale = lHand.find('**/counteractToonScale')
                if counterActToonScale.isEmpty():
                    counterActToonScale = lHand.attachNewNode(
                        'counteractToonScale')
                    counterActToonScale.setScale(1 / netScale)
                    self.notify.debug(
                        'creating counterActToonScale for %s' % av.getName())

                club.reparentTo(counterActToonScale)
                club.setX(-0.25 * netScale)
                if pointToBall:
                    club.lookAt(self.clubLookatSpot)

    def detachClub(self):
        if not self.club.isEmpty():
            self.club.reparentTo(self.root)
            self.club.setZ(-20)
            self.club.setScale(1)

    def adjustClub(self):
        club = self.club
        if club:
            distance = club.getDistance(self.clubLookatSpot)
            scaleFactor = distance / 2.0579999999999998
            club.setScale(1, scaleFactor, 1)

    def startAdjustClubTask(self):
        taskMgr.add(self.adjustClubTask, self.adjustClubTaskName)

    def stopAdjustClubTask(self):
        taskMgr.remove(self.adjustClubTaskName)

    def adjustClubTask(self, task):
        self.attachClub(self.avId, True)
        self.adjustClub()
        return task.cont

    def enableControlKey(self):
        self.controlKeyAllowed = True

    def disableControlKey(self):
        self.controlKeyAllowed = False

    def sendSwingInfo(self, power, angle, sequenceNum):
        self.sendUpdate('setSwingInfo', [power, angle, sequenceNum])

    def startBallPlayback(self, power, angle, sequenceNum):
        flyBall = self.ballModel.copyTo(NodePath())
        flyBall.setScale(1.0)
        flyBallBubble = self.getFlyBallBubble().instanceTo(NodePath())
        flyBallBubble.reparentTo(flyBall)
        flyBall.setTag('pieSequence', str(sequenceNum))
        flyBall.setTag('throwerId', str(self.avId))
        t = power / 100.0
        t = 1.0 - t
        dist = 300 - 200 * t
        time = 1.5 + 0.5 * t
        proj = ProjectileInterval(
            None,
            startPos=Point3(0, 0, 0),
            endPos=Point3(0, dist, 0),
            duration=time)
        relVel = proj.startVel

        def getVelocity(root=self.root, relVel=relVel):
            return render.getRelativeVector(root, relVel)

        fly = Sequence(
            Func(flyBall.reparentTo, render),
            Func(flyBall.setPosHpr, self.root, 0, 0, 0, 0, 0, 0),
            Func(base.cTrav.addCollider, flyBallBubble, self.flyBallHandler),
            ProjectileInterval(flyBall, startVel=getVelocity, duration=3),
            Func(flyBall.detachNode),
            Func(base.cTrav.removeCollider, flyBallBubble),
            Func(self.notify.debug, 'removed collider'),
            Func(self.flyBallFinishedFlying, sequenceNum))
        flyWithSound = Parallel(
            fly,
            SoundInterval(self.hitBallSfx, node=self.root),
            name='flyWithSound')
        self.notify.debug('starting flyball track')
        flyWithSound.start()
        self.flyBallTracks[sequenceNum] = flyWithSound

    def setSwingInfo(self, power, angle, sequenceNum):
        av = base.cr.doId2do.get(self.avId)
        self.swingInterval = Sequence()
        if av:
            self.stopAdjustClubTask()
            self.swingInterval = Sequence(
                ActorInterval(
                    av,
                    'swing-putt',
                    startFrame=0,
                    endFrame=GolfGlobals.BALL_CONTACT_FRAME),
                Func(self.startBallPlayback, power, angle, sequenceNum),
                Func(self.ballModel.hide),
                ActorInterval(
                    av,
                    'swing-putt',
                    startFrame=GolfGlobals.BALL_CONTACT_FRAME,
                    endFrame=24),
                Func(self.ballModel.setScale, 0.10000000000000001),
                Func(self.ballModel.show),
                LerpScaleInterval(self.ballModel, 1.0, Point3(1, 1, 1)),
                Func(self.enableControlKey))
            if av == localAvatar:
                self.swingInterval.append(
                    Func(self.switchToAnimState, 'GolfPuttLoop', True))

        self.swingInterval.start()

    def getFlyBallBubble(self):
        if self._DistributedGolfSpot__flyBallBubble is None:
            bubble = CollisionSphere(0, 0, 0, GolfGlobals.GOLF_BALL_RADIUS)
            node = CollisionNode('flyBallBubble')
            node.addSolid(bubble)
            node.setFromCollideMask(ToontownGlobals.PieBitmask
                                    | ToontownGlobals.CameraBitmask
                                    | ToontownGlobals.FloorBitmask)
            node.setIntoCollideMask(BitMask32.allOff())
            self._DistributedGolfSpot__flyBallBubble = NodePath(node)
            self.flyBallHandler = CollisionHandlerEvent()
            self.flyBallHandler.addInPattern('flyBallHit-%d' % self.index)

        return self._DistributedGolfSpot__flyBallBubble

    def _DistributedGolfSpot__flyBallHit(self, entry):
        print entry

    def flyBallFinishedFlying(self, sequence):
        if sequence in self.flyBallTracks:
            del self.flyBallTracks[sequence]

    def _DistributedGolfSpot__finishFlyBallTrack(self, sequence):
        if sequence in self.flyBallTracks:
            flyBallTrack = self.flyBallTracks[sequence]
            del self.flyBallTracks[sequence]
            flyBallTrack.finish()

    def flyBallFinishedSplatting(self, sequence):
        if sequence in self.splatTracks:
            del self.splatTracks[sequence]

    def _DistributedGolfSpot__flyBallHit(self, entry):
        if not entry.hasSurfacePoint() or not entry.hasInto():
            return None

        if not entry.getInto().isTangible():
            return None

        sequence = int(entry.getFromNodePath().getNetTag('pieSequence'))
        self._DistributedGolfSpot__finishFlyBallTrack(sequence)
        if sequence in self.splatTracks:
            splatTrack = self.splatTracks[sequence]
            del self.splatTracks[sequence]
            splatTrack.finish()

        flyBallCode = 0
        flyBallCodeStr = entry.getIntoNodePath().getNetTag('pieCode')
        if flyBallCodeStr:
            flyBallCode = int(flyBallCodeStr)

        pos = entry.getSurfacePoint(render)
        timestamp32 = globalClockDelta.getFrameNetworkTime(bits=32)
        throwerId = int(entry.getFromNodePath().getNetTag('throwerId'))
        splat = self.getFlyBallSplatInterval(pos[0], pos[1], pos[2],
                                             flyBallCode, throwerId)
        splat = Sequence(splat, Func(self.flyBallFinishedSplatting, sequence))
        self.splatTracks[sequence] = splat
        splat.start()
        self.notify.debug(
            'doId=%d into=%s flyBallCode=%d, throwerId=%d' %
            (self.doId, entry.getIntoNodePath(), flyBallCode, throwerId))
        if flyBallCode == ToontownGlobals.PieCodeBossCog and self.avId == localAvatar.doId and self.lastHitSequenceNum != self._DistributedGolfSpot__flyBallSequenceNum:
            self.lastHitSequenceNum = self._DistributedGolfSpot__flyBallSequenceNum
            self.boss.d_ballHitBoss(1)
        elif flyBallCode == ToontownGlobals.PieCodeToon and self.avId == localAvatar.doId and self.lastHitSequenceNum != self._DistributedGolfSpot__flyBallSequenceNum:
            self.lastHitSequenceNum = self._DistributedGolfSpot__flyBallSequenceNum
            avatarDoId = entry.getIntoNodePath().getNetTag('avatarDoId')
            if avatarDoId == '':
                self.notify.warning('Toon %s has no avatarDoId tag.' % repr(
                    entry.getIntoNodePath()))
                return None

            doId = int(avatarDoId)
            if doId != localAvatar.doId:
                pass

    def getFlyBallSplatInterval(self, x, y, z, flyBallCode, throwerId):
        ToontownBattleGlobals = ToontownBattleGlobals
        import toontown.toonbase
        BattleProps = BattleProps
        import toontown.battle
        splatName = 'dust'
        splat = BattleProps.globalPropPool.getProp(splatName)
        splat.setBillboardPointWorld(2)
        color = ToontownGlobals.PieCodeColors.get(flyBallCode)
        if color:
            splat.setColor(*color)

        if flyBallCode == ToontownGlobals.PieCodeBossCog:
            self.notify.debug('changing color to %s' % self.ballColor)
            splat.setColor(self.ballColor)

        sound = loader.loadSfx('phase_11/audio/sfx/LB_evidence_miss.mp3')
        vol = 1.0
        if flyBallCode == ToontownGlobals.PieCodeBossCog:
            sound = loader.loadSfx('phase_4/audio/sfx/Golf_Hit_Barrier_1.mp3')

        soundIval = SoundInterval(sound, node=splat, volume=vol)
        if flyBallCode == ToontownGlobals.PieCodeBossCog and localAvatar.doId == throwerId:
            vol = 1.0
            soundIval = SoundInterval(sound, node=localAvatar, volume=vol)

        ival = Parallel(
            Func(splat.reparentTo, render), Func(splat.setPos, x, y, z),
            soundIval,
            Sequence(ActorInterval(splat, splatName), Func(splat.detachNode)))
        return ival

    def setGoingToReward(self):
        self.goingToReward = True

    def gotBossZapped(self):
        self.showExiting()
        self.d_requestFree(True)
