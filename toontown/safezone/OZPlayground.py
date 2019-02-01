from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
import Playground
from toontown.launcher import DownloadForceAcknowledge
from toontown.building import Elevator
from toontown.toontowngui import TTDialog
from toontown.toonbase import TTLocalizer
from toontown.racing import RaceGlobals
from direct.fsm import State
from toontown.safezone import PicnicBasket
from toontown.safezone import GolfKart
from direct.task.Task import Task


class OZPlayground(Playground.Playground):
    waterLevel = -0.53000000000000003

    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)
        self.parentFSM = parentFSM
        self.picnicBasketBlockDoneEvent = 'picnicBasketBlockDone'
        self.cameraSubmerged = -1
        self.toonSubmerged = -1
        self.fsm.addState(
            State.State(
                'picnicBasketBlock',
                self.enterPicnicBasketBlock,
                self.exitPicnicBasketBlock,
                ['walk']))
        state = self.fsm.getStateNamed('walk')
        state.addTransition('picnicBasketBlock')
        self.picnicBasketDoneEvent = 'picnicBasketDone'

    def load(self):
        Playground.Playground.load(self)

    def unload(self):
        Playground.Playground.unload(self)

    def enter(self, requestStatus):
        Playground.Playground.enter(self, requestStatus)

    def exit(self):
        Playground.Playground.exit(self)
        taskMgr.remove('oz-check-toon-underwater')
        taskMgr.remove('oz-check-cam-underwater')
        self.loader.hood.setNoFog()

    def doRequestLeave(self, requestStatus):
        self.fsm.request('trialerFA', [
            requestStatus])

    def enterDFA(self, requestStatus):
        doneEvent = 'dfaDoneEvent'
        self.accept(doneEvent, self.enterDFACallback, [
            requestStatus])
        self.dfa = DownloadForceAcknowledge.DownloadForceAcknowledge(doneEvent)
        if requestStatus['hoodId'] == ToontownGlobals.MyEstate:
            self.dfa.enter(
                base.cr.hoodMgr.getPhaseFromHood(
                    ToontownGlobals.MyEstate))
        else:
            self.dfa.enter(5)

    def enterStart(self):
        self.cameraSubmerged = 0
        self.toonSubmerged = 0
        taskMgr.add(
            self._OZPlayground__checkToonUnderwater,
            'oz-check-toon-underwater')
        taskMgr.add(
            self._OZPlayground__checkCameraUnderwater,
            'oz-check-cam-underwater')

    def _OZPlayground__checkCameraUnderwater(self, task):
        if camera.getZ(render) < self.waterLevel:
            self._OZPlayground__submergeCamera()
        else:
            self._OZPlayground__emergeCamera()
        return Task.cont

    def _OZPlayground__checkToonUnderwater(self, task):
        if base.localAvatar.getZ() < -4.0:
            self._OZPlayground__submergeToon()
        else:
            self._OZPlayground__emergeToon()
        return Task.cont

    def _OZPlayground__submergeCamera(self):
        if self.cameraSubmerged == 1:
            return None

        self.loader.hood.setUnderwaterFog()
        base.playSfx(
            self.loader.underwaterSound,
            looping=1,
            volume=0.80000000000000004)
        self.cameraSubmerged = 1
        self.walkStateData.setSwimSoundAudible(1)

    def _OZPlayground__emergeCamera(self):
        if self.cameraSubmerged == 0:
            return None

        self.loader.hood.setNoFog()
        self.loader.underwaterSound.stop()
        self.cameraSubmerged = 0
        self.walkStateData.setSwimSoundAudible(0)

    def _OZPlayground__submergeToon(self):
        if self.toonSubmerged == 1:
            return None

        base.playSfx(self.loader.submergeSound)
        if base.config.GetBool('disable-flying-glitch') == 0:
            self.fsm.request('walk')

        self.walkStateData.fsm.request('swimming', [
            self.loader.swimSound])
        pos = base.localAvatar.getPos(render)
        base.localAvatar.d_playSplashEffect(pos[0], pos[1], self.waterLevel)
        self.toonSubmerged = 1

    def _OZPlayground__emergeToon(self):
        if self.toonSubmerged == 0:
            return None

        self.walkStateData.fsm.request('walking')
        self.toonSubmerged = 0

    def enterTeleportIn(self, requestStatus):
        reason = requestStatus.get('reason')
        if reason == RaceGlobals.Exit_Barrier:
            requestStatus['nextState'] = 'popup'
            self.dialog = TTDialog.TTDialog(
                text=TTLocalizer.KartRace_RaceTimeout,
                command=self._OZPlayground__cleanupDialog,
                style=TTDialog.Acknowledge)
        elif reason == RaceGlobals.Exit_Slow:
            requestStatus['nextState'] = 'popup'
            self.dialog = TTDialog.TTDialog(
                text=TTLocalizer.KartRace_RacerTooSlow,
                command=self._OZPlayground__cleanupDialog,
                style=TTDialog.Acknowledge)
        elif reason == RaceGlobals.Exit_BarrierNoRefund:
            requestStatus['nextState'] = 'popup'
            self.dialog = TTDialog.TTDialog(
                text=TTLocalizer.KartRace_RaceTimeoutNoRefund,
                command=self._OZPlayground__cleanupDialog,
                style=TTDialog.Acknowledge)

        self.toonSubmerged = -1
        taskMgr.remove('oz-check-toon-underwater')
        Playground.Playground.enterTeleportIn(self, requestStatus)

    def teleportInDone(self):
        self.toonSubmerged = -1
        taskMgr.add(
            self._OZPlayground__checkToonUnderwater,
            'oz-check-toon-underwater')
        Playground.Playground.teleportInDone(self)

    def _OZPlayground__cleanupDialog(self, value):
        if self.dialog:
            self.dialog.cleanup()
            self.dialog = None

        if hasattr(self, 'fsm'):
            self.fsm.request('walk', [
                1])

    def enterPicnicBasketBlock(self, picnicBasket):
        base.localAvatar.laffMeter.start()
        base.localAvatar.b_setAnimState('off', 1)
        base.localAvatar.cantLeaveGame = 1
        self.accept(self.picnicBasketDoneEvent, self.handlePicnicBasketDone)
        self.trolley = PicnicBasket.PicnicBasket(
            self,
            self.fsm,
            self.picnicBasketDoneEvent,
            picnicBasket.getDoId(),
            picnicBasket.seatNumber)
        self.trolley.load()
        self.trolley.enter()

    def exitPicnicBasketBlock(self):
        base.localAvatar.laffMeter.stop()
        base.localAvatar.cantLeaveGame = 0
        self.ignore(self.trolleyDoneEvent)
        self.trolley.unload()
        self.trolley.exit()
        del self.trolley

    def detectedPicnicTableSphereCollision(self, picnicBasket):
        self.fsm.request('picnicBasketBlock', [
            picnicBasket])

    def handleStartingBlockDone(self, doneStatus):
        self.notify.debug('handling StartingBlock done event')
        where = doneStatus['where']
        if where == 'reject':
            self.fsm.request('walk')
        elif where == 'exit':
            self.fsm.request('walk')
        elif where == 'racetrack':
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)
        else:
            self.notify.error(
                'Unknown mode: ' +
                where +
                ' in handleStartingBlockDone')

    def handlePicnicBasketDone(self, doneStatus):
        self.notify.debug('handling picnic basket done event')
        mode = doneStatus['mode']
        if mode == 'reject':
            self.fsm.request('walk')
        elif mode == 'exit':
            self.fsm.request('walk')
        else:
            self.notify.error(
                'Unknown mode: ' +
                mode +
                ' in handlePicnicBasketDone')

    def showPaths(self):
        CCharPaths = CCharPaths
        import toontown.classicchars
        TTLocalizer = TTLocalizer
        import toontown.toonbase
        self.showPathPoints(CCharPaths.getPaths(TTLocalizer.Chip))
