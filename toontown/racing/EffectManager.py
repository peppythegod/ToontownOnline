from pandac.PandaModules import *
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *
from toontown.battle.BattleProps import *
from toontown.battle import MovieUtil


class EffectManager(DirectObject):
    def __init__(self):
        self.effectList = []

    def delete(self):
        for effect in effectList:
            self._EffectManager__removeEffect(effect)

    def addSplatEffect(self,
                       spawner,
                       splatName='splat-creampie',
                       time=1,
                       size=6,
                       parent=render):
        splat = globalPropPool.getProp(splatName)
        splatSeq = Sequence()
        splatType = globalPropPool.getPropType(splatName)
        splatShow = Func(self._EffectManager__showProp, splat, size, parent,
                         spawner.getPos(parent))
        splatAnim = ActorInterval(splat, splatName)
        splatHide = Func(MovieUtil.removeProp, splat)
        splatRemove = Func(self._EffectManager__removeEffect, splatSeq)
        splatSeq.append(splatShow)
        splatSeq.append(splatAnim)
        splatSeq.append(splatHide)
        splatSeq.append(splatRemove)
        splatSeq.start()
        self.effectList.append(splatSeq)

    def _EffectManager__showProp(self, prop, size, parent, pos):
        prop.reparentTo(parent)
        prop.setScale(size)
        prop.setBillboardPointEye()
        prop.setPos(pos + Vec3(0, 0, size / 2))

    def _EffectManager__removeEffect(self, effect):
        if effect.isPlaying():
            effect.finish()

        self.effectList.remove(effect)
        effect = None
