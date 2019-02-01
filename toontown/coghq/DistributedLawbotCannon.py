from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from direct.task.Task import Task
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import CollisionSphere, CollisionNode
from toontown.toonbase import ToontownGlobals
from toontown.estate import DistributedCannon
from toontown.estate import CannonGlobals
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toon import NPCToons
from toontown.toon import ToonHead
from toontown.toonbase import TTLocalizer
from toontown.minigame import Trajectory
from toontown.effects import DustCloud
GROUND_PLANE_MIN = -15
CANNON_ROTATION_MIN = -55
CANNON_ROTATION_MAX = 50
CANNON_ROTATION_VEL = 15.0
CANNON_ANGLE_MIN = 10
CANNON_ANGLE_MAX = 85
CANNON_ANGLE_VEL = 15.0
INITIAL_VELOCITY = 80
CANNON_MOVE_UPDATE_FREQ = 0.5
CAMERA_PULLBACK_MIN = 20
CAMERA_PULLBACK_MAX = 40


class DistributedLawbotCannon(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedLawbotCannon')
    LOCAL_CANNON_MOVE_TASK = 'localCannonMoveTask'
    FIRE_KEY = 'control'
    UP_KEY = 'arrow_up'
    DOWN_KEY = 'arrow_down'
    LEFT_KEY = 'arrow_left'
    RIGHT_KEY = 'arrow_right'
    HIT_GROUND = 0

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.index = None
        self.avId = 0
        self.av = None
        self.localToonShooting = 0
        self.cannonsActive = 0
        self.cannonLocation = None
        self.cannonPostion = None
        self.cannon = None
        self.madeGui = 0
        self.jurorToon = None
        self.toonModel = None
        self.toonHead = None
        self.toonScale = None
        self.dustCloud = None
        self.hitBumper = 0
        self.hitTarget = 0
        self.lastPos = Vec3(0, 0, 0)
        self.lastVel = Vec3(0, 0, 0)
        self.vel = Vec3(0, 0, 0)
        self.landingPos = Vec3(0, 0, 0)
        self.t = 0
        self.lastT = 0
        self.deltaT = 0
        self.hitTrack = None
        self.flyColNode = None
        self.flyColNodePath = None
        self.localAvId = base.localAvatar.doId
        self.model_Created = 0

    def disable(self):
        taskMgr.remove(self.uniqueName('fireCannon'))
        taskMgr.remove(self.uniqueName('shootTask'))
        self._DistributedLawbotCannon__stopFlyTask(self.avId)
        taskMgr.remove(self.uniqueName('flyTask'))
        self.ignoreAll()
        self.setMovie(CannonGlobals.CANNON_MOVIE_CLEAR, 0, 0)
        self.nodePath.detachNode()
        self._DistributedLawbotCannon__unmakeGui()
        if self.hitTrack:
            self.hitTrack.finish()
            del self.hitTrack
            self.hitTrack = None

        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        self.offstage()
        self.unload()
        DistributedObject.DistributedObject.delete(self)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.boss.cannons[self.index] = self

    def generateInit(self):
        DistributedObject.DistributedObject.generateInit(self)
        self.nodePath = NodePath(self.uniqueName('Cannon'))
        self.load()
        self.activateCannons()

    def setPosHpr(self, x, y, z, h, p, r):
        self.nodePath.setPosHpr(x, y, z, h, p, r)

    def setBossCogId(self, bossCogId):
        self.bossCogId = bossCogId
        self.boss = base.cr.doId2do[bossCogId]

    def getSphereRadius(self):
        return 1.5

    def getParentNodePath(self):
        return render

    def setIndex(self, index):
        self.index = index

    def load(self):
        self.cannon = loader.loadModel('phase_4/models/minigames/toon_cannon')
        self.collSphere = CollisionSphere(0, 0, 0, self.getSphereRadius())
        self.dustCloud = DustCloud.DustCloud(render)
        self.dustCloud.setBillboardPointEye()
        self.collSphere.setTangible(1)
        self.collNode = CollisionNode(self.uniqueName('CannonSphere'))
        self.collNode.setCollideMask(ToontownGlobals.WallBitmask)
        self.collNode.addSolid(self.collSphere)
        self.collNodePath = self.nodePath.attachNewNode(self.collNode)
        self.cannon.reparentTo(self.nodePath)
        self.kartColNode = CollisionNode(self.uniqueName('KartColNode'))
        self.kartNode = self.nodePath.attachNewNode(self.kartColNode)
        self.sndCannonMove = base.loadSfx(
            'phase_4/audio/sfx/MG_cannon_adjust.mp3')
        self.sndCannonFire = base.loadSfx(
            'phase_4/audio/sfx/MG_cannon_fire_alt.mp3')
        self.sndHitGround = base.loadSfx(
            'phase_4/audio/sfx/MG_cannon_hit_dirt.mp3')
        self.sndHitChair = base.loadSfx('phase_11/audio/sfx/LB_toon_jury.mp3')
        self.cannon.hide()
        self.flashingLabel = None

    def unload(self):
        if self.cannon:
            self.cannon.removeNode()
            del self.cannon

        if self.dustCloud is not None:
            self.dustCloud.destroy()
            del self.dustCloud

        del self.sndCannonMove
        del self.sndCannonFire
        del self.sndHitGround
        del self.sndHitChair
        if self.av:
            self._DistributedLawbotCannon__resetToon(self.av)
            self.av.loop('neutral')
            self.av.setPlayRate(1.0, 'run')

        if self.toonHead is not None:
            self.toonHead.stopBlink()
            self.toonHead.stopLookAroundNow()
            self.toonHead.delete()
            del self.toonHead

        if self.toonModel is not None:
            self.toonModel.removeNode()
            del self.toonModel

        if self.jurorToon is not None:
            self.jurorToon.delete()
            del self.jurorToon

        del self.toonScale

    def activateCannons(self):
        if not self.cannonsActive:
            self.cannonsActive = 1
            self.onstage()
            self.nodePath.reparentTo(self.getParentNodePath())
            self.accept(
                self.uniqueName('enterCannonSphere'),
                self._DistributedLawbotCannon__handleEnterSphere)

    def onstage(self):
        self._DistributedLawbotCannon__createCannon()
        self.cannon.reparentTo(self.nodePath)
        self.dustCloud.reparentTo(render)

    def offstage(self):
        if self.cannon:
            self.cannon.reparentTo(hidden)

        if self.dustCloud:
            self.dustCloud.reparentTo(hidden)
            self.dustCloud.stop()

    def _DistributedLawbotCannon__createCannon(self):
        self.barrel = self.cannon.find('**/cannon')
        self.cannonLocation = Point3(0, 0, 0.025000000000000001)
        self.cannonPosition = [
            0,
            CANNON_ANGLE_MIN]
        self.cannon.setPos(self.cannonLocation)
        self._DistributedLawbotCannon__updateCannonPosition(self.avId)

    def updateCannonPosition(self, avId, zRot, angle):
        if avId != self.localAvId:
            self.cannonPosition = [
                zRot,
                angle]
            self._DistributedLawbotCannon__updateCannonPosition(avId)

    def _DistributedLawbotCannon__updateCannonPosition(self, avId):
        self.cannon.setHpr(self.cannonPosition[0], 0.0, 0.0)
        self.barrel.setHpr(0.0, self.cannonPosition[1], 0.0)
        maxP = 90
        newP = self.barrel.getP()
        yScale = 1 - 0.5 * float(newP) / maxP
        shadow = self.cannon.find('**/square_drop_shadow')
        shadow.setScale(1, yScale, 1)

    def _DistributedLawbotCannon__handleEnterSphere(self, collEntry):
        self.d_requestEnter()

    def d_requestEnter(self):
        self.sendUpdate('requestEnter', [])

    def setMovie(self, mode, avId, extraInfo):
        wasLocalToon = self.localToonShooting
        self.avId = avId
        if mode == CannonGlobals.CANNON_MOVIE_CLEAR:
            self.setLanded()
        elif mode == CannonGlobals.CANNON_MOVIE_LANDED:
            self.setLanded()
        elif mode == CannonGlobals.CANNON_MOVIE_FORCE_EXIT:
            self.exitCannon(self.avId)
            self.setLanded()
        elif mode == CannonGlobals.CANNON_MOVIE_LOAD:
            if self.avId == base.localAvatar.doId:
                self.cannonBallsLeft = extraInfo
                base.cr.playGame.getPlace().setState('crane')
                base.localAvatar.setTeleportAvailable(0)
                self.localToonShooting = 1
                self._DistributedLawbotCannon__makeGui()
                camera.reparentTo(self.barrel)
                camera.setPos(0.5, -2, 2.5)
                camera.setHpr(0, 0, 0)
                self.boss.toonEnteredCannon(self.avId, self.index)

            if self.avId in self.cr.doId2do:
                self.av = self.cr.doId2do[self.avId]
                self.acceptOnce(
                    self.av.uniqueName('disable'),
                    self._DistributedLawbotCannon__avatarGone)
                self.av.loop('neutral')
                self.av.stopSmooth()
                self._DistributedLawbotCannon__destroyToonModels()
                self._DistributedLawbotCannon__createToonModels()
                self.av.setPosHpr(3, 0, 0, 90, 0, 0)
                self.av.reparentTo(self.cannon)
            else:
                self.notify.warning(
                    'Unknown avatar %d in cannon %d' %
                    (self.avId, self.doId))
        else:
            self.notify.warning('unhandled case, mode = %d' % mode)

    def _DistributedLawbotCannon__avatarGone(self):
        self.setMovie(CannonGlobals.CANNON_MOVIE_CLEAR, 0, 0)

    def _DistributedLawbotCannon__makeGui(self):
        if self.madeGui:
            return None

        NametagGlobals.setMasterArrowsOn(0)
        guiModel = 'phase_4/models/gui/cannon_game_gui'
        cannonGui = loader.loadModel(guiModel)
        self.aimPad = DirectFrame(
            image=cannonGui.find('**/CannonFire_PAD'),
            relief=None,
            pos=(
                0.69999999999999996,
                0,
                -0.55333299999999996),
            scale=0.80000000000000004)
        cannonGui.removeNode()
        self.fireButton = DirectButton(
            parent=self.aimPad,
            image=(
                (guiModel,
                 '**/Fire_Btn_UP'),
                (guiModel,
                 '**/Fire_Btn_DN'),
                (guiModel,
                 '**/Fire_Btn_RLVR')),
            relief=None,
            pos=(
                0.0115741,
                0,
                0.0050505100000000002),
            scale=1.0,
            command=self._DistributedLawbotCannon__firePressed)
        self.upButton = DirectButton(
            parent=self.aimPad,
            image=(
                (guiModel,
                 '**/Cannon_Arrow_UP'),
                (guiModel,
                 '**/Cannon_Arrow_DN'),
                (guiModel,
                 '**/Cannon_Arrow_RLVR')),
            relief=None,
            pos=(
                0.0115741,
                0,
                0.221717))
        self.downButton = DirectButton(
            parent=self.aimPad,
            image=(
                (guiModel,
                 '**/Cannon_Arrow_UP'),
                (guiModel,
                 '**/Cannon_Arrow_DN'),
                (guiModel,
                 '**/Cannon_Arrow_RLVR')),
            relief=None,
            pos=(
                0.0136112,
                0,
                -0.21010100000000001),
            image_hpr=(
                0,
                0,
                180))
        self.leftButton = DirectButton(
            parent=self.aimPad,
            image=(
                (guiModel,
                 '**/Cannon_Arrow_UP'),
                (guiModel,
                 '**/Cannon_Arrow_DN'),
                (guiModel,
                 '**/Cannon_Arrow_RLVR')),
            relief=None,
            pos=(
                -0.199352,
                0,
                -0.00050526900000000003),
            image_hpr=(
                0,
                0,
                -90))
        self.rightButton = DirectButton(
            parent=self.aimPad,
            image=(
                (guiModel,
                 '**/Cannon_Arrow_UP'),
                (guiModel,
                 '**/Cannon_Arrow_DN'),
                (guiModel,
                 '**/Cannon_Arrow_RLVR')),
            relief=None,
            pos=(
                0.219167,
                0,
                -0.0010102399999999999),
            image_hpr=(
                0,
                0,
                90))
        guiClose = loader.loadModel('phase_3.5/models/gui/avatar_panel_gui')
        cannonBallText = '%d/%d' % (self.cannonBallsLeft,
                                    ToontownGlobals.LawbotBossCannonBallMax)
        self.cannonBallLabel = DirectLabel(
            parent=self.aimPad, text=cannonBallText, text_fg=VBase4(
                1, 1, 1, 1), text_align=TextNode.ACenter, relief=None, pos=(
                0.47499999999999998, 0.0, -0.34999999999999998), scale=0.25)
        if self.cannonBallsLeft < 5:
            if self.flashingLabel:
                self.flashingLabel.stop()

            flashingTrack = Sequence()
            for i in range(10):
                flashingTrack.append(
                    LerpColorScaleInterval(
                        self.cannonBallLabel, 0.5, VBase4(
                            1, 0, 0, 1)))
                flashingTrack.append(
                    LerpColorScaleInterval(
                        self.cannonBallLabel, 0.5, VBase4(
                            1, 1, 1, 1)))

            self.flashingLabel = flashingTrack
            self.flashingLabel.start()

        self.aimPad.setColor(1, 1, 1, 0.90000000000000002)

        def bindButton(button, upHandler, downHandler):
            button.bind(DGG.B1PRESS, lambda x, handler=upHandler: handler())
            button.bind(
                DGG.B1RELEASE,
                lambda x,
                handler=downHandler: handler())

        bindButton(
            self.upButton,
            self._DistributedLawbotCannon__upPressed,
            self._DistributedLawbotCannon__upReleased)
        bindButton(
            self.downButton,
            self._DistributedLawbotCannon__downPressed,
            self._DistributedLawbotCannon__downReleased)
        bindButton(
            self.leftButton,
            self._DistributedLawbotCannon__leftPressed,
            self._DistributedLawbotCannon__leftReleased)
        bindButton(
            self.rightButton,
            self._DistributedLawbotCannon__rightPressed,
            self._DistributedLawbotCannon__rightReleased)
        self._DistributedLawbotCannon__enableAimInterface()
        self.madeGui = 1

    def _DistributedLawbotCannon__unmakeGui(self):
        self.notify.debug('__unmakeGui')
        if not self.madeGui:
            return None

        if self.flashingLabel:
            self.flashingLabel.finish()
            self.flashingLabel = None

        NametagGlobals.setMasterArrowsOn(1)
        self._DistributedLawbotCannon__disableAimInterface()
        self.upButton.unbind(DGG.B1PRESS)
        self.upButton.unbind(DGG.B1RELEASE)
        self.downButton.unbind(DGG.B1PRESS)
        self.downButton.unbind(DGG.B1RELEASE)
        self.leftButton.unbind(DGG.B1PRESS)
        self.leftButton.unbind(DGG.B1RELEASE)
        self.rightButton.unbind(DGG.B1PRESS)
        self.rightButton.unbind(DGG.B1RELEASE)
        self.aimPad.destroy()
        del self.aimPad
        del self.fireButton
        del self.upButton
        del self.downButton
        del self.leftButton
        del self.rightButton
        self.madeGui = 0

    def _DistributedLawbotCannon__enableAimInterface(self):
        self.aimPad.show()
        self.accept(
            self.FIRE_KEY,
            self._DistributedLawbotCannon__fireKeyPressed)
        self.accept(self.UP_KEY, self._DistributedLawbotCannon__upKeyPressed)
        self.accept(
            self.DOWN_KEY,
            self._DistributedLawbotCannon__downKeyPressed)
        self.accept(
            self.LEFT_KEY,
            self._DistributedLawbotCannon__leftKeyPressed)
        self.accept(
            self.RIGHT_KEY,
            self._DistributedLawbotCannon__rightKeyPressed)
        self._DistributedLawbotCannon__spawnLocalCannonMoveTask()

    def _DistributedLawbotCannon__disableAimInterface(self):
        self.aimPad.hide()
        self.ignore(self.FIRE_KEY)
        self.ignore(self.UP_KEY)
        self.ignore(self.DOWN_KEY)
        self.ignore(self.LEFT_KEY)
        self.ignore(self.RIGHT_KEY)
        self.ignore(self.FIRE_KEY + '-up')
        self.ignore(self.UP_KEY + '-up')
        self.ignore(self.DOWN_KEY + '-up')
        self.ignore(self.LEFT_KEY + '-up')
        self.ignore(self.RIGHT_KEY + '-up')
        self._DistributedLawbotCannon__killLocalCannonMoveTask()

    def _DistributedLawbotCannon__fireKeyPressed(self):
        self.ignore(self.FIRE_KEY)
        self.accept(
            self.FIRE_KEY + '-up',
            self._DistributedLawbotCannon__fireKeyReleased)
        self._DistributedLawbotCannon__firePressed()

    def _DistributedLawbotCannon__upKeyPressed(self):
        self.ignore(self.UP_KEY)
        self.accept(
            self.UP_KEY + '-up',
            self._DistributedLawbotCannon__upKeyReleased)
        self._DistributedLawbotCannon__upPressed()

    def _DistributedLawbotCannon__downKeyPressed(self):
        self.ignore(self.DOWN_KEY)
        self.accept(
            self.DOWN_KEY + '-up',
            self._DistributedLawbotCannon__downKeyReleased)
        self._DistributedLawbotCannon__downPressed()

    def _DistributedLawbotCannon__leftKeyPressed(self):
        self.ignore(self.LEFT_KEY)
        self.accept(
            self.LEFT_KEY + '-up',
            self._DistributedLawbotCannon__leftKeyReleased)
        self._DistributedLawbotCannon__leftPressed()

    def _DistributedLawbotCannon__rightKeyPressed(self):
        self.ignore(self.RIGHT_KEY)
        self.accept(
            self.RIGHT_KEY + '-up',
            self._DistributedLawbotCannon__rightKeyReleased)
        self._DistributedLawbotCannon__rightPressed()

    def _DistributedLawbotCannon__fireKeyReleased(self):
        self.ignore(self.FIRE_KEY + '-up')
        self.accept(
            self.FIRE_KEY,
            self._DistributedLawbotCannon__fireKeyPressed)

    def _DistributedLawbotCannon__leftKeyReleased(self):
        self.ignore(self.LEFT_KEY + '-up')
        self.accept(
            self.LEFT_KEY,
            self._DistributedLawbotCannon__leftKeyPressed)
        self._DistributedLawbotCannon__leftReleased()

    def _DistributedLawbotCannon__rightKeyReleased(self):
        self.ignore(self.RIGHT_KEY + '-up')
        self.accept(
            self.RIGHT_KEY,
            self._DistributedLawbotCannon__rightKeyPressed)
        self._DistributedLawbotCannon__rightReleased()

    def _DistributedLawbotCannon__upKeyReleased(self):
        self.ignore(self.UP_KEY + '-up')
        self.accept(self.UP_KEY, self._DistributedLawbotCannon__upKeyPressed)
        self._DistributedLawbotCannon__upReleased()

    def _DistributedLawbotCannon__downKeyReleased(self):
        self.ignore(self.DOWN_KEY + '-up')
        self.accept(
            self.DOWN_KEY,
            self._DistributedLawbotCannon__downKeyPressed)
        self._DistributedLawbotCannon__downReleased()

    def _DistributedLawbotCannon__leaveCannon(self):
        self.notify.debug('__leaveCannon')
        self.sendUpdate('requestLeave')

    def _DistributedLawbotCannon__firePressed(self):
        self.notify.debug('fire pressed')
        if not self.boss.state == 'BattleTwo':
            self.notify.debug(
                'boss is in state=%s, not firing' %
                self.boss.state)
            return None

        self._DistributedLawbotCannon__broadcastLocalCannonPosition()
        self._DistributedLawbotCannon__unmakeGui()
        self.sendUpdate('setCannonLit', [
            self.cannonPosition[0],
            self.cannonPosition[1]])

    def _DistributedLawbotCannon__upPressed(self):
        self.notify.debug('up pressed')
        self.upPressed = self._DistributedLawbotCannon__enterControlActive(
            self.upPressed)

    def _DistributedLawbotCannon__downPressed(self):
        self.notify.debug('down pressed')
        self.downPressed = self._DistributedLawbotCannon__enterControlActive(
            self.downPressed)

    def _DistributedLawbotCannon__leftPressed(self):
        self.notify.debug('left pressed')
        self.leftPressed = self._DistributedLawbotCannon__enterControlActive(
            self.leftPressed)

    def _DistributedLawbotCannon__rightPressed(self):
        self.notify.debug('right pressed')
        self.rightPressed = self._DistributedLawbotCannon__enterControlActive(
            self.rightPressed)

    def _DistributedLawbotCannon__upReleased(self):
        self.notify.debug('up released')
        self.upPressed = self._DistributedLawbotCannon__exitControlActive(
            self.upPressed)

    def _DistributedLawbotCannon__downReleased(self):
        self.notify.debug('down released')
        self.downPressed = self._DistributedLawbotCannon__exitControlActive(
            self.downPressed)

    def _DistributedLawbotCannon__leftReleased(self):
        self.notify.debug('left released')
        self.leftPressed = self._DistributedLawbotCannon__exitControlActive(
            self.leftPressed)

    def _DistributedLawbotCannon__rightReleased(self):
        self.notify.debug('right released')
        self.rightPressed = self._DistributedLawbotCannon__exitControlActive(
            self.rightPressed)

    def _DistributedLawbotCannon__enterControlActive(self, control):
        return control + 1

    def _DistributedLawbotCannon__exitControlActive(self, control):
        return max(0, control - 1)

    def _DistributedLawbotCannon__spawnLocalCannonMoveTask(self):
        self.leftPressed = 0
        self.rightPressed = 0
        self.upPressed = 0
        self.downPressed = 0
        self.cannonMoving = 0
        task = Task(self._DistributedLawbotCannon__localCannonMoveTask)
        task.lastPositionBroadcastTime = 0.0
        taskMgr.add(task, self.LOCAL_CANNON_MOVE_TASK)

    def _DistributedLawbotCannon__killLocalCannonMoveTask(self):
        taskMgr.remove(self.LOCAL_CANNON_MOVE_TASK)
        if self.cannonMoving:
            self.sndCannonMove.stop()

    def _DistributedLawbotCannon__localCannonMoveTask(self, task):
        pos = self.cannonPosition
        oldRot = pos[0]
        oldAng = pos[1]
        rotVel = 0
        if self.leftPressed:
            rotVel += CANNON_ROTATION_VEL

        if self.rightPressed:
            rotVel -= CANNON_ROTATION_VEL

        pos[0] += rotVel * globalClock.getDt()
        if pos[0] < CANNON_ROTATION_MIN:
            pos[0] = CANNON_ROTATION_MIN
        elif pos[0] > CANNON_ROTATION_MAX:
            pos[0] = CANNON_ROTATION_MAX

        angVel = 0
        if self.upPressed:
            angVel += CANNON_ANGLE_VEL

        if self.downPressed:
            angVel -= CANNON_ANGLE_VEL

        pos[1] += angVel * globalClock.getDt()
        if pos[1] < CANNON_ANGLE_MIN:
            pos[1] = CANNON_ANGLE_MIN
        elif pos[1] > CANNON_ANGLE_MAX:
            pos[1] = CANNON_ANGLE_MAX

        if oldRot != pos[0] or oldAng != pos[1]:
            if self.cannonMoving == 0:
                self.cannonMoving = 1
                base.playSfx(self.sndCannonMove, looping=1)

            self._DistributedLawbotCannon__updateCannonPosition(self.localAvId)
            if task.time - task.lastPositionBroadcastTime > CANNON_MOVE_UPDATE_FREQ:
                task.lastPositionBroadcastTime = task.time
                self._DistributedLawbotCannon__broadcastLocalCannonPosition()

        elif self.cannonMoving:
            self.cannonMoving = 0
            self.sndCannonMove.stop()
            self._DistributedLawbotCannon__broadcastLocalCannonPosition()

        return Task.cont

    def _DistributedLawbotCannon__broadcastLocalCannonPosition(self):
        self.sendUpdate('setCannonPosition', [
            self.cannonPosition[0],
            self.cannonPosition[1]])

    def _DistributedLawbotCannon__updateCannonPosition(self, avId):
        self.cannon.setHpr(self.cannonPosition[0], 0.0, 0.0)
        self.barrel.setHpr(0.0, self.cannonPosition[1], 0.0)
        maxP = 90
        newP = self.barrel.getP()
        yScale = 1 - 0.5 * float(newP) / maxP
        shadow = self.cannon.find('**/square_drop_shadow')
        shadow.setScale(1, yScale, 1)

    def _DistributedLawbotCannon__createToonModels(self):
        self.model_Created = 1
        self.jurorToon = NPCToons.createLocalNPC(
            ToontownGlobals.LawbotBossBaseJurorNpcId + self.index)
        self.toonScale = self.jurorToon.getScale()
        jurorToonParent = render.attachNewNode('toonOriginChange')
        self.jurorToon.wrtReparentTo(jurorToonParent)
        self.jurorToon.setPosHpr(
            0, 0, -(self.jurorToon.getHeight() / 2.0), 0, -90, 0)
        self.toonModel = jurorToonParent
        self.toonHead = ToonHead.ToonHead()
        self.toonHead.setupHead(self.jurorToon.style)
        self.toonHead.reparentTo(hidden)
        self._DistributedLawbotCannon__loadToonInCannon()

    def _DistributedLawbotCannon__destroyToonModels(self):
        if 0:
            self.av.dropShadow.show()
            if self.dropShadow is not None:
                self.dropShadow.removeNode()
                self.dropShadow = None

            self.hitBumper = 0
            self.hitTarget = 0
            self.angularVel = 0
            self.vel = Vec3(0, 0, 0)
            self.lastVel = Vec3(0, 0, 0)
            self.lastPos = Vec3(0, 0, 0)
            self.landingPos = Vec3(0, 0, 0)
            self.t = 0
            self.lastT = 0
            self.deltaT = 0
            self.av = None
            self.lastWakeTime = 0
            self.localToonShooting = 0

        if self.toonHead is not None:
            self.toonHead.reparentTo(hidden)
            self.toonHead.stopBlink()
            self.toonHead.stopLookAroundNow()
            self.toonHead = None

        if self.toonModel is not None:
            self.toonModel.removeNode()
            self.toonModel = None

        if self.jurorToon is not None:
            self.jurorToon.delete()
            self.jurorToon = None

        self.model_Created = 0

    def _DistributedLawbotCannon__loadToonInCannon(self):
        self.toonModel.reparentTo(hidden)
        self.toonHead.startBlink()
        self.toonHead.startLookAround()
        self.toonHead.reparentTo(self.barrel)
        self.toonHead.setPosHpr(0, 6, 0, 0, -45, 0)
        sc = self.toonScale
        self.toonHead.setScale(render, sc[0], sc[1], sc[2])

    def exitCannon(self, avId):
        self._DistributedLawbotCannon__unmakeGui()
        if self.avId == avId:
            self.av.reparentTo(render)
            self._DistributedLawbotCannon__resetToonToCannon(self.av)

    def _DistributedLawbotCannon__resetToonToCannon(self, avatar):
        pos = None
        if not avatar:
            if self.avId:
                avatar = base.cr.doId2do.get(self.avId, None)

        if avatar:
            if hasattr(self, 'cannon') and self.cannon:
                avatar.reparentTo(self.cannon)
                avatar.setPosHpr(3, 0, 0, 90, 0, 0)
                avatar.wrtReparentTo(render)

            self._DistributedLawbotCannon__resetToon(avatar)

    def _DistributedLawbotCannon__resetToon(self, avatar, pos=None):
        if avatar:
            self._DistributedLawbotCannon__stopCollisionHandler(avatar)
            self._DistributedLawbotCannon__setToonUpright(avatar, pos)
            if self.localToonShooting:
                self.notify.debug('toon setting position to %s' % pos)
                if pos:
                    base.localAvatar.setPos(pos)

                camera.reparentTo(avatar)
                camera.setPos(self.av.cameraPositions[0][0])
                place = base.cr.playGame.getPlace()
                if place:
                    place.setState('finalBattle')

            self.b_setLanded()

    def _DistributedLawbotCannon__stopCollisionHandler(self, avatar):
        if avatar:
            avatar.loop('neutral')
            if self.flyColNode:
                self.flyColNode = None

            if avatar == base.localAvatar:
                avatar.collisionsOn()

            self.flyColSphere = None
            if self.flyColNodePath:
                base.cTrav.removeCollider(self.flyColNodePath)
                self.flyColNodePath.removeNode()
                self.flyColNodePath = None

            self.handler = None

    def _DistributedLawbotCannon__setToonUpright(self, avatar, pos=None):
        if avatar:
            if not pos:
                pos = avatar.getPos(render)

            avatar.setPos(render, pos)
            avatar.loop('neutral')

    def b_setLanded(self):
        self.d_setLanded()

    def d_setLanded(self):
        if self.localToonShooting:
            self.sendUpdate('setLanded', [])

    def setLanded(self):
        self.removeAvFromCannon()

    def removeAvFromCannon(self):
        if self.av is not None:
            self._DistributedLawbotCannon__stopCollisionHandler(self.av)
            self.av.resetLOD()
            place = base.cr.playGame.getPlace()
            if self.av == base.localAvatar:
                if place:
                    place.setState('finalBattle')

            self.av.loop('neutral')
            self.av.setPlayRate(1.0, 'run')
            if self.av.getParent().getName() == 'toonOriginChange':
                self.av.wrtReparentTo(render)
                self._DistributedLawbotCannon__setToonUpright(self.av)

            if self.av == base.localAvatar:
                self.av.startPosHprBroadcast()

            self.av.startSmooth()
            self.av.setScale(1, 1, 1)
            self.ignore(self.av.uniqueName('disable'))
            self._DistributedLawbotCannon__destroyToonModels()

    def setCannonWillFire(self, avId, fireTime, zRot, angle, timestamp):
        self.notify.debug('setCannonWillFire: ' + str(avId) + ': zRot=' + \
                          str(zRot) + ', angle=' + str(angle) + ', time=' + str(fireTime))
        if not self.model_Created:
            self.notify.warning(
                "We walked into the zone mid-flight, so we won't see it")
            return None

        self.cannonPosition[0] = zRot
        self.cannonPosition[1] = angle
        self._DistributedLawbotCannon__updateCannonPosition(avId)
        task = Task(self._DistributedLawbotCannon__fireCannonTask)
        task.avId = avId
        ts = globalClockDelta.localElapsedTime(timestamp)
        task.fireTime = fireTime - ts
        if task.fireTime < 0.0:
            task.fireTime = 0.0

        taskMgr.add(task, self.taskName('fireCannon'))

    def _DistributedLawbotCannon__fireCannonTask(self, task):
        launchTime = task.fireTime
        avId = task.avId
        if self.toonHead is None or not (self.boss.state == 'BattleTwo'):
            return Task.done

        flightResults = self._DistributedLawbotCannon__calcFlightResults(
            avId, launchTime)
        if not isClient():
            print 'EXECWARNING DistributedLawbotCannon: %s' % flightResults
            printStack()

        for key in flightResults:
            exec "%s = flightResults['%s']" % (key, key)

        self.notify.debug('start position: ' + str(startPos))
        self.notify.debug('start velocity: ' + str(startVel))
        self.notify.debug('time of launch: ' + str(launchTime))
        self.notify.debug('time of impact: ' + str(timeOfImpact))
        self.notify.debug('location of impact: ' +
                          str(trajectory.getPos(timeOfImpact)))
        head = self.toonHead
        head.stopBlink()
        head.stopLookAroundNow()
        head.reparentTo(hidden)
        juror = self.toonModel
        juror.reparentTo(render)
        juror.setPos(startPos)
        barrelHpr = self.barrel.getHpr(render)
        juror.setHpr(startHpr)
        self.jurorToon.loop('swim')
        self.jurorToon.setPosHpr(
            0, 0, -(self.jurorToon.getHeight() / 2.0), 0, 0, 0)
        info = {}
        info['avId'] = avId
        info['trajectory'] = trajectory
        info['launchTime'] = launchTime
        info['timeOfImpact'] = timeOfImpact
        info['hitWhat'] = hitWhat
        info['toon'] = self.toonModel
        info['hRot'] = self.cannonPosition[0]
        info['haveWhistled'] = 0
        info['maxCamPullback'] = CAMERA_PULLBACK_MIN
        if self.localToonShooting:
            camera.reparentTo(juror)
            camera.setP(45.0)
            camera.setZ(-10.0)

        self.flyColSphere = CollisionSphere(
            0, 0, self.av.getHeight() / 2.0, 1.0)
        self.flyColNode = CollisionNode(self.uniqueName('flySphere'))
        self.flyColNode.setCollideMask(
            ToontownGlobals.WallBitmask | ToontownGlobals.FloorBitmask | ToontownGlobals.PieBitmask)
        self.flyColNode.addSolid(self.flyColSphere)
        self.flyColNodePath = self.jurorToon.attachNewNode(self.flyColNode)
        self.flyColNodePath.setColor(1, 0, 0, 1)
        self.handler = CollisionHandlerEvent()
        self.handler.setInPattern(self.uniqueName('cannonHit'))
        base.cTrav.addCollider(self.flyColNodePath, self.handler)
        self.accept(self.uniqueName('cannonHit'),
                    self._DistributedLawbotCannon__handleCannonHit)
        shootTask = Task(
            self._DistributedLawbotCannon__shootTask,
            self.taskName('shootTask'))
        flyTask = Task(
            self._DistributedLawbotCannon__flyTask,
            self.taskName('flyTask'))
        shootTask.info = info
        flyTask.info = info
        seqTask = Task.sequence(shootTask, flyTask)
        taskMgr.add(seqTask, self.taskName('flyingToon') + '-' + str(avId))
        self.acceptOnce(
            self.uniqueName('stopFlyTask'),
            self._DistributedLawbotCannon__stopFlyTask)
        return Task.done

    def _DistributedLawbotCannon__toRadians(self, angle):
        return angle * 2.0 * math.pi / 360.0

    def _DistributedLawbotCannon__toDegrees(self, angle):
        return angle * 360.0 / 2.0 * math.pi

    def _DistributedLawbotCannon__calcFlightResults(self, avId, launchTime):
        head = self.toonHead
        startPos = head.getPos(render)
        startHpr = head.getHpr(render)
        hpr = self.barrel.getHpr(render)
        rotation = self._DistributedLawbotCannon__toRadians(hpr[0])
        angle = self._DistributedLawbotCannon__toRadians(hpr[1])
        horizVel = INITIAL_VELOCITY * math.cos(angle)
        xVel = horizVel * -math.sin(rotation)
        yVel = horizVel * math.cos(rotation)
        zVel = INITIAL_VELOCITY * math.sin(angle)
        startVel = Vec3(xVel, yVel, zVel)
        trajectory = Trajectory.Trajectory(launchTime, startPos, startVel)
        self.trajectory = trajectory
        (timeOfImpact, hitWhat) = self._DistributedLawbotCannon__calcToonImpact(trajectory)
        return {
            'startPos': startPos,
            'startHpr': startHpr,
            'startVel': startVel,
            'trajectory': trajectory,
            'timeOfImpact': 3 * timeOfImpact,
            'hitWhat': hitWhat}

    def _DistributedLawbotCannon__calcToonImpact(self, trajectory):
        t_groundImpact = trajectory.checkCollisionWithGround(GROUND_PLANE_MIN)
        if t_groundImpact >= trajectory.getStartTime():
            return (t_groundImpact, self.HIT_GROUND)
        else:
            self.notify.error('__calcToonImpact: toon never impacts ground?')
            return (0.0, self.HIT_GROUND)

    def _DistributedLawbotCannon__handleCannonHit(self, collisionEntry):
        if self.av is None or self.flyColNode is None:
            return None

        interPt = collisionEntry.getSurfacePoint(render)
        hitNode = collisionEntry.getIntoNode().getName()
        fromNodePath = collisionEntry.getFromNodePath()
        intoNodePath = collisionEntry.getIntoNodePath()
        ignoredHits = [
            'NearBoss']
        for nodeName in ignoredHits:
            if hitNode == nodeName:
                return None
                continue

        self._DistributedLawbotCannon__stopFlyTask(self.avId)
        self._DistributedLawbotCannon__stopCollisionHandler(self.jurorToon)
        if self.localToonShooting:
            camera.wrtReparentTo(render)

        pos = interPt
        hpr = self.jurorToon.getHpr()
        track = Sequence()
        if self.localToonShooting:
            pass
        1
        chairlist = [
            'trigger-chair']
        for index in range(len(ToontownGlobals.LawbotBossChairPosHprs)):
            chairlist.append('Chair-%s' % index)

        if hitNode in chairlist:
            track.append(
                Func(
                    self._DistributedLawbotCannon__hitChair,
                    self.jurorToon,
                    pos))
            track.append(Wait(1.0))
            track.append(
                Func(
                    self._DistributedLawbotCannon__setToonUpright,
                    self.av))
            if self.av == base.localAvatar:
                strs = hitNode.split('-')
                chairNum = int(strs[1])
                self.boss.sendUpdate('hitChair', [
                    chairNum,
                    self.index])

        else:
            track.append(
                Func(
                    self._DistributedLawbotCannon__hitGround,
                    self.jurorToon,
                    pos))
            track.append(Wait(1.0))
            track.append(
                Func(
                    self._DistributedLawbotCannon__setToonUpright,
                    self.av))
        track.append(Func(self.b_setLanded))
        if self.localToonShooting:
            pass
        1
        if self.hitTrack:
            self.hitTrack.finish()

        self.hitTrack = track
        self.hitTrack.start()

    def enterCannonHit(self, collisionEntry):
        pass

    def _DistributedLawbotCannon__shootTask(self, task):
        base.playSfx(self.sndCannonFire)
        return Task.done

    def _DistributedLawbotCannon__flyTask(self, task):
        toon = task.info['toon']
        if toon.isEmpty():
            self._DistributedLawbotCannon__resetToonToCannon(self.av)
            return Task.done

        curTime = task.time + task.info['launchTime']
        t = min(curTime, task.info['timeOfImpact'])
        self.lastT = self.t
        self.t = t
        deltaT = self.t - self.lastT
        self.deltaT = deltaT
        if t >= task.info['timeOfImpact']:
            self._DistributedLawbotCannon__resetToonToCannon(self.av)
            return Task.done

        pos = task.info['trajectory'].getPos(t)
        toon.setFluidPos(pos)
        vel = task.info['trajectory'].getVel(t)
        run = math.sqrt(vel[0] * vel[0] + vel[1] * vel[1])
        rise = vel[2]
        theta = self._DistributedLawbotCannon__toDegrees(math.atan(rise / run))
        toon.setHpr(self.cannon.getH(render), -90 + theta, 0)
        view = 2
        lookAt = task.info['toon'].getPos(render)
        hpr = task.info['toon'].getHpr(render)
        if self.localToonShooting:
            if view == 0:
                camera.wrtReparentTo(render)
                camera.lookAt(lookAt)
            elif view == 1:
                camera.reparentTo(render)
                camera.setPos(render, 100, 100, 35.25)
                camera.lookAt(render, lookAt)
            elif view == 2:
                if hpr[1] > -90:
                    camera.setPos(0, 0, -30)
                    if camera.getZ() < lookAt[2]:
                        camera.setZ(render, lookAt[2] + 10)

                    camera.lookAt(Point3(0, 0, 0))

        return Task.cont

    def _DistributedLawbotCannon__stopFlyTask(self, avId):
        taskMgr.remove(self.taskName('flyingToon') + '-' + str(avId))

    def _DistributedLawbotCannon__hitGround(self, avatar, pos, extraArgs=[]):
        hitP = avatar.getPos(render)
        h = self.barrel.getH(render)
        avatar.setPos(pos[0], pos[1], pos[2] + avatar.getHeight() / 3.0)
        avatar.setHpr(h, -135, 0)
        self.dustCloud.setPos(
            render,
            pos[0],
            pos[1],
            pos[2] +
            avatar.getHeight() /
            3.0)
        self.dustCloud.setScale(0.34999999999999998)
        self.dustCloud.play()
        base.playSfx(self.sndHitGround)
        avatar.hide()

    def _DistributedLawbotCannon__hitChair(self, avatar, pos, extraArgs=[]):
        hitP = avatar.getPos(render)
        h = self.barrel.getH(render)
        avatar.setPos(pos[0], pos[1], pos[2] + avatar.getHeight() / 3.0)
        avatar.setHpr(h, -135, 0)
        self.dustCloud.setPos(
            render,
            pos[0],
            pos[1],
            pos[2] +
            avatar.getHeight() /
            3.0)
        self.dustCloud.setScale(0.34999999999999998)
        self.dustCloud.play()
        base.playSfx(self.sndHitGround)
        base.playSfx(self.sndHitChair)
        avatar.hide()

    def generateCannonAppearTrack(self, avatar):
        self.cannon.setScale(0.10000000000000001)
        self.cannon.show()
        kartTrack = Parallel(
            Sequence(
                ActorInterval(
                    avatar, 'feedPet'), Func(
                    avatar.loop, 'neutral')), Sequence(
                Func(
                    self.cannon.reparentTo, avatar.rightHand), Wait(2.1000000000000001), Func(
                    self.cannon.wrtReparentTo, render), Func(
                    self.cannon.setShear, 0, 0, 0), Parallel(
                    LerpHprInterval(
                        self.cannon, hpr=self.nodePath.getHpr(render), duration=1.2), ProjectileInterval(
                        self.cannon, endPos=self.nodePath.getPos(render), duration=1.2, gravityMult=0.45000000000000001)), Wait(0.20000000000000001), Sequence(
                    LerpScaleInterval(
                        self.cannon, scale=Point3(
                            1.1000000000000001, 1.1000000000000001, 0.10000000000000001), duration=0.20000000000000001), LerpScaleInterval(
                        self.cannon, scale=Point3(
                            0.90000000000000002, 0.90000000000000002, 0.10000000000000001), duration=0.10000000000000001), LerpScaleInterval(
                        self.cannon, scale=Point3(
                            1.0, 1.0, 0.10000000000000001), duration=0.10000000000000001), LerpScaleInterval(
                        self.cannon, scale=Point3(
                            1.0, 1.0, 1.1000000000000001), duration=0.20000000000000001), LerpScaleInterval(
                        self.cannon, scale=Point3(
                            1.0, 1.0, 0.90000000000000002), duration=0.10000000000000001), LerpScaleInterval(
                        self.cannon, scale=Point3(
                            1.0, 1.0, 1.0), duration=0.10000000000000001), Func(
                        self.cannon.wrtReparentTo, self.nodePath))))
        return kartTrack
