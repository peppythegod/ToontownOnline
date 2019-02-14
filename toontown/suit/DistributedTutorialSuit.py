from pandac.PandaModules import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.directnotify import DirectNotifyGlobal
from toontown.distributed.DelayDeletable import DelayDeletable
import DistributedSuitBase


class DistributedTutorialSuit(DistributedSuitBase.DistributedSuitBase,
                              DelayDeletable):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedTutorialSuit')

    def __init__(self, cr):

        try:
            pass
        except BaseException:
            self.DistributedSuit_initialized = 1
            DistributedSuitBase.DistributedSuitBase.__init__(self, cr)
            self.fsm = ClassicFSM.ClassicFSM('DistributedSuit', [
                State.State('Off', self.enterOff, self.exitOff,
                            ['Walk', 'Battle']),
                State.State('Walk', self.enterWalk, self.exitWalk,
                            ['WaitForBattle', 'Battle']),
                State.State('Battle', self.enterBattle, self.exitBattle, []),
                State.State('WaitForBattle', self.enterWaitForBattle,
                            self.exitWaitForBattle, ['Battle'])
            ], 'Off', 'Off')
            self.fsm.enterInitialState()

    def generate(self):
        DistributedSuitBase.DistributedSuitBase.generate(self)

    def announceGenerate(self):
        DistributedSuitBase.DistributedSuitBase.announceGenerate(self)
        self.setState('Walk')

    def disable(self):
        self.notify.debug('DistributedSuit %d: disabling' % self.getDoId())
        self.setState('Off')
        DistributedSuitBase.DistributedSuitBase.disable(self)

    def delete(self):

        try:
            pass
        except BaseException:
            self.DistributedSuit_deleted = 1
            self.notify.debug('DistributedSuit %d: deleting' % self.getDoId())
            del self.fsm
            DistributedSuitBase.DistributedSuitBase.delete(self)

    def d_requestBattle(self, pos, hpr):
        self.cr.playGame.getPlace().setState('WaitForBattle')
        self.sendUpdate('requestBattle',
                        [pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2]])

    def _DistributedTutorialSuit__handleToonCollision(self, collEntry):
        toonId = base.localAvatar.getDoId()
        self.notify.debug('Distributed suit: requesting a Battle with ' +
                          'toon: %d' % toonId)
        self.d_requestBattle(self.getPos(), self.getHpr())
        self.setState('WaitForBattle')

    def enterWalk(self):
        self.enableBattleDetect(
            'walk', self._DistributedTutorialSuit__handleToonCollision)
        self.loop('walk', 0)
        pathPoints = [
            Vec3(55, 15, -0.5),
            Vec3(55, 25, -0.5),
            Vec3(25, 25, -0.5),
            Vec3(25, 15, -0.5),
            Vec3(55, 15, -0.5)
        ]
        self.tutWalkTrack = self.makePathTrack(self, pathPoints, 4.5,
                                               'tutFlunkyWalk')
        self.tutWalkTrack.loop()

    def exitWalk(self):
        self.disableBattleDetect()
        self.tutWalkTrack.pause()
        self.tutWalkTrack = None
