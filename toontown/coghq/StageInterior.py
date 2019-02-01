from direct.directnotify import DirectNotifyGlobal
from toontown.battle import BattlePlace
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.showbase import BulletinBoardWatcher
from pandac.PandaModules import *
from toontown.toon import Toon
from toontown.toonbase import ToontownGlobals
from toontown.hood import ZoneUtil
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TTDialog
from toontown.toonbase import ToontownBattleGlobals
from toontown.coghq import DistributedStage
from toontown.building import Elevator


class StageInterior(BattlePlace.BattlePlace):
    notify = DirectNotifyGlobal.directNotify.newCategory('StageInterior')

    def __init__(self, loader, parentFSM, doneEvent):
        BattlePlace.BattlePlace.__init__(self, loader, doneEvent)
        self.parentFSM = parentFSM
        self.zoneId = loader.stageId
        self.elevatorDoneEvent = 'elevatorDone'
        self.fsm = ClassicFSM.ClassicFSM('StageInterior', [
            State.State('start', self.enterStart, self.exitStart, [
                'walk',
                'teleportIn',
                'fallDown']),
            State.State('walk', self.enterWalk, self.exitWalk, [
                'push',
                'sit',
                'stickerBook',
                'WaitForBattle',
                'battle',
                'died',
                'teleportOut',
                'squished',
                'DFA',
                'fallDown',
                'elevator']),
            State.State('sit', self.enterSit, self.exitSit, [
                'walk',
                'died',
                'teleportOut']),
            State.State('push', self.enterPush, self.exitPush, [
                'walk',
                'died',
                'teleportOut']),
            State.State('stickerBook', self.enterStickerBook, self.exitStickerBook, [
                'walk',
                'battle',
                'DFA',
                'WaitForBattle',
                'died',
                'teleportOut']),
            State.State('WaitForBattle', self.enterWaitForBattle, self.exitWaitForBattle, [
                'battle',
                'walk',
                'died',
                'teleportOut']),
            State.State('battle', self.enterBattle, self.exitBattle, [
                'walk',
                'teleportOut',
                'died']),
            State.State('fallDown', self.enterFallDown, self.exitFallDown, [
                'walk',
                'died',
                'teleportOut']),
            State.State('squished', self.enterSquished, self.exitSquished, [
                'walk',
                'died',
                'teleportOut']),
            State.State('teleportIn', self.enterTeleportIn, self.exitTeleportIn, [
                'walk',
                'teleportOut',
                'quietZone',
                'died']),
            State.State('teleportOut', self.enterTeleportOut, self.exitTeleportOut, [
                'teleportIn',
                'FLA',
                'quietZone',
                'WaitForBattle']),
            State.State('DFA', self.enterDFA, self.exitDFA, [
                'DFAReject',
                'teleportOut']),
            State.State('DFAReject', self.enterDFAReject, self.exitDFAReject, [
                'walkteleportOut']),
            State.State('died', self.enterDied, self.exitDied, [
                'teleportOut']),
            State.State('FLA', self.enterFLA, self.exitFLA, [
                'quietZone']),
            State.State('quietZone', self.enterQuietZone, self.exitQuietZone, [
                'teleportIn']),
            State.State('elevator', self.enterElevator, self.exitElevator, [
                'walk']),
            State.State('final', self.enterFinal, self.exitFinal, [
                'start'])], 'start', 'final')

    def load(self):
        self.parentFSM.getStateNamed('stageInterior').addChild(self.fsm)
        BattlePlace.BattlePlace.load(self)
        self.music = base.loadMusic('phase_9/audio/bgm/CHQ_FACT_bg.mid')

    def unload(self):
        self.parentFSM.getStateNamed('stageInterior').removeChild(self.fsm)
        del self.music
        del self.fsm
        del self.parentFSM
        BattlePlace.BattlePlace.unload(self)

    def enter(self, requestStatus):
        self.fsm.enterInitialState()
        base.transitions.fadeOut(t=0)
        base.localAvatar.inventory.setRespectInvasions(0)
        base.cr.forbidCheesyEffects(1)

        def commence(self=self):
            NametagGlobals.setMasterArrowsOn(1)
            self.fsm.request(requestStatus['how'], [
                requestStatus])
            base.playMusic(self.music, looping=1, volume=0.80000000000000004)
            base.transitions.irisIn()
            stage = bboard.get(DistributedStage.DistributedStage.ReadyPost)
            self.loader.hood.spawnTitleText(stage.stageId)

        self.stageReadyWatcher = BulletinBoardWatcher.BulletinBoardWatcher(
    'StageReady', DistributedStage.DistributedStage.ReadyPost, commence)
        self.stageDefeated = 0
        self.acceptOnce(
    DistributedStage.DistributedStage.WinEvent,
     self.handleStageWinEvent)
        if __debug__ and 0:
            self.accept(
    'f10', lambda: messenger.send(
        DistributedStage.DistributedStage.WinEvent))

        self.confrontedBoss = 0

        def handleConfrontedBoss(self=self):
            self.confrontedBoss = 1

        self.acceptOnce('localToonConfrontedStageBoss', handleConfrontedBoss)

    def exit(self):
        NametagGlobals.setMasterArrowsOn(0)
        bboard.remove(DistributedStage.DistributedStage.ReadyPost)
        base.cr.forbidCheesyEffects(0)
        base.localAvatar.inventory.setRespectInvasions(1)
        self.fsm.requestFinalState()
        self.loader.music.stop()
        self.music.stop()
        self.ignoreAll()
        del self.stageReadyWatcher

    def enterWalk(self, teleportIn=0):
        BattlePlace.BattlePlace.enterWalk(self, teleportIn)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterPush(self):
        BattlePlace.BattlePlace.enterPush(self)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterWaitForBattle(self):
        StageInterior.notify.debug('enterWaitForBattle')
        BattlePlace.BattlePlace.enterWaitForBattle(self)
        if base.localAvatar.getParent() != render:
            base.localAvatar.wrtReparentTo(render)
            base.localAvatar.b_setParent(ToontownGlobals.SPRender)

    def exitWaitForBattle(self):
        StageInterior.notify.debug('exitWaitForBattle')
        BattlePlace.BattlePlace.exitWaitForBattle(self)

    def enterBattle(self, event):
        StageInterior.notify.debug('enterBattle')
        self.music.stop()
        BattlePlace.BattlePlace.enterBattle(self, event)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterTownBattle(self, event):
        mult = ToontownBattleGlobals.getStageCreditMultiplier(
            bboard.get(DistributedStage.DistributedStage.FloorNum))
        base.localAvatar.inventory.setBattleCreditMultiplier(mult)
        self.loader.townBattle.enter(
    event,
    self.fsm.getStateNamed('battle'),
    bldg=1,
     creditMultiplier=mult)

    def exitBattle(self):
        StageInterior.notify.debug('exitBattle')
        BattlePlace.BattlePlace.exitBattle(self)
        self.loader.music.stop()
        base.playMusic(self.music, looping=1, volume=0.80000000000000004)

    def enterStickerBook(self, page=None):
        BattlePlace.BattlePlace.enterStickerBook(self, page)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterSit(self):
        BattlePlace.BattlePlace.enterSit(self)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterZone(self, zoneId):
        pass

    def enterTeleportOut(self, requestStatus):
        StageInterior.notify.debug('enterTeleportOut()'
