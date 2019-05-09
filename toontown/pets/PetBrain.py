from pandac.PandaModules import *
from direct.showbase.PythonUtil import weightedChoice, randFloat, Functor
from direct.showbase.PythonUtil import list2dict
from direct.showbase import DirectObject
from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from direct.fsm import FSM
from toontown.toon import DistributedToonAI
from toontown.pets import PetConstants, PetObserve, PetGoal, PetGoalMgr
from toontown.pets import PetTricks, PetLookerAI
from libotp.CPetBrain import CPetBrain
import random
import types


class PetBrain(DirectObject.DirectObject, CPetBrain):
    notify = DirectNotifyGlobal.directNotify.newCategory('PetBrain')

    def __init__(self, pet):
        CPetBrain.__init__(self)
        self.pet = pet
        self.focus = None
        self.started = 0
        self.inMovie = 0
        self.chaseNode = self.pet.getRender().attachNewNode('PetChaseNode')
        self.goalMgr = PetGoalMgr.PetGoalMgr(self.pet)
        self.doId2goals = {}
        self.nearbyAvs = {}
        self.avAwareness = {}
        self.lastInteractTime = {}
        self.nextAwarenessIndex = 0
        if __dev__:
            self.pscPrior = PStatCollector(
                'App:Show code:petThink:UpdatePriorities')
            self.pscAware = PStatCollector(
                'App:Show code:petThink:ShuffleAwareness')
            self.pscResc = PStatCollector('App:Show code:petThink:Reschedule')

    def destroy(self):
        taskMgr.remove(self.getTeleportTaskName())
        if __dev__:
            del self.pscPrior
            del self.pscAware
            del self.pscResc

        self.stop()
        self.goalMgr.destroy()
        self.chaseNode.removeNode()
        del self.chaseNode
        del self.focus
        del self.pet
        if self.doId2goals:
            self.notify.warning('destroy(): self.doId2goals is not empty: %s' %
                                self.doId2goals.keys())
            for goalList in self.doId2goals.values():
                for goal in goalList:
                    goal.destroy()

        del self.doId2goals
        del self.avAwareness

    def getThinkTaskName(self):
        return 'petThink-%s' % self.pet.doId

    def getTeleportTaskName(self):
        return 'petTeleport-%s' % self.pet.doId

    def getObserveEventAttendedByAvStart(self, otherDoId):
        return 'petObserveAttendedByAvStart-%s-%s' % (self.pet.doId, otherDoId)

    def getObserveEventAttendedByAvStop(self, otherDoId):
        return 'petObserveAttendedByAvStop-%s-%s' % (self.pet.doId, otherDoId)

    def getObserveEventAttendingAvStart(self, otherDoId):
        return 'petObserveAttendingAvStart-%s-%s' % (self.pet.doId, otherDoId)

    def getObserveEventAttendingAvStop(self, otherDoId):
        return 'petObserveAttendingAvStop-%s-%s' % (self.pet.doId, otherDoId)

    def start(self):
        PetBrain.notify.debug('start: %s' % self.pet.doId)
        self.lookers = {}
        self.lookees = {}
        self.accept(
            PetLookerAI.getStartLookedAtByOtherEvent(self.pet.doId),
            self._handleLookedAtByOtherStart)
        self.accept(
            PetLookerAI.getStopLookedAtByOtherEvent(self.pet.doId),
            self._handleLookedAtByOtherStop)
        self.accept(
            PetLookerAI.getStartLookingAtOtherEvent(self.pet.doId),
            self._handleLookingAtOtherStart)
        self.accept(
            PetLookerAI.getStopLookingAtOtherEvent(self.pet.doId),
            self._handleLookingAtOtherStop)
        self.globalGoals = [PetGoal.Wander()]
        for goal in self.globalGoals:
            self.goalMgr.addGoal(goal)

        for doId in self.pet._getNearbyAvatarDict():
            self._handleAvatarArrive(doId)

        self.tLastLonelinessUpdate = globalClock.getFrameTime()
        taskMgr.doMethodLater(simbase.petThinkPeriod * random.random(),
                              self._think, self.getThinkTaskName())
        self.started = 1

    def stop(self):
        PetBrain.notify.debug('stop: %s' % self.pet.doId)
        if not self.started:
            return None

        self.started = 0
        del self.lookers
        del self.lookees
        for doId in self.pet._getNearbyAvatarDict():
            self._handleAvatarLeave(doId)

        for goal in self.globalGoals:
            self.goalMgr.removeGoal(goal)
            goal.destroy()

        del self.globalGoals
        self.clearFocus()
        taskMgr.remove(self.getThinkTaskName())
        self.ignore(PetLookerAI.getStartLookedAtByOtherEvent(self.pet.doId))
        self.ignore(PetLookerAI.getStopLookedAtByOtherEvent(self.pet.doId))
        self.ignore(PetLookerAI.getStartLookingAtOtherEvent(self.pet.doId))
        self.ignore(PetLookerAI.getStopLookingAtOtherEvent(self.pet.doId))

    def observe(self, petObserve):
        if petObserve.isForgettable():
            if random.random(
            ) < 0.050000000000000003 * self.pet.traits.forgetfulness:
                return None

        petObserve._influence(self)

    def updateLastInteractTime(self, avId):
        if avId in self.lastInteractTime:
            self.lastInteractTime[avId] = globalClock.getFrameTime()

    def _think(self, task=None):
        if not self.inMovie:
            if __dev__:
                self.pscPrior.start()

            self._updatePriorities()
            if __dev__:
                self.pscPrior.stop()

            if __dev__:
                self.pscAware.start()

            if len(self.nearbyAvs) > PetConstants.MaxAvatarAwareness:
                self.nextAwarenessIndex %= len(self.nearbyAvs)
                self._considerBecomeAwareOf(
                    self.nearbyAvs.keys()[self.nextAwarenessIndex])
                self.nextAwarenessIndex += 1

            if __dev__:
                self.pscAware.stop()

            curT = globalClock.getFrameTime()
            tSinceLastLonelinessUpdate = curT - self.tLastLonelinessUpdate
            if tSinceLastLonelinessUpdate >= PetConstants.LonelinessUpdatePeriod:
                self.tLastLonelinessUpdate = curT
                numLookers = len(self.lookers)
                if numLookers:
                    dt = tSinceLastLonelinessUpdate
                    self.pet.lerpMood(
                        'loneliness',
                        max(-1.0, dt * -0.0030000000000000001 * numLookers))
                    if numLookers > 5:
                        self.pet.lerpMood('excitement',
                                          min(1.0, dt * 0.001 * numLookers))

        if __dev__:
            self.pscResc.start()

        taskMgr.doMethodLater(simbase.petThinkPeriod, self._think,
                              self.getThinkTaskName())
        if __dev__:
            self.pscResc.stop()

        return Task.done

    def _updatePriorities(self):
        self.goalMgr.updatePriorities()

    def _handleLookingAtOtherStart(self, avId):
        if avId in self.lookees:
            PetBrain.notify.warning(
                '%s: already looking at av %s' % (self.pet.doId, avId))
            return None

        self.lookees[avId] = avId
        self.observe(
            PetObserve.PetActionObserve(PetObserve.Actions.ATTENDING_START,
                                        avId))

    def _handleLookingAtOtherStop(self, avId):
        if avId not in self.lookees:
            PetBrain.notify.warning(
                '%s: not looking at av %s' % (self.pet.doId, avId))
            return None

        del self.lookees[avId]
        self.observe(
            PetObserve.PetActionObserve(PetObserve.Actions.ATTENDING_STOP,
                                        avId))

    def _handleLookedAtByOtherStart(self, avId):
        if avId in self.lookers:
            PetBrain.notify.warning(
                '%s: av %s already looking at me' % (self.pet.doId, avId))
            return None

        self.lookers[avId] = avId
        self.observe(
            PetObserve.PetActionObserve(PetObserve.Actions.ATTENDED_START,
                                        avId))

    def _handleLookedAtByOtherStop(self, avId):
        if avId not in self.lookers:
            PetBrain.notify.warning(
                '%s: av %s not looking at me' % (self.pet.doId, avId))
            return None

        del self.lookers[avId]
        self.observe(
            PetObserve.PetActionObserve(PetObserve.Actions.ATTENDED_STOP,
                                        avId))

    def lookedAtBy(self, avId):
        return avId in self.lookers

    def lookingAt(self, avId):
        return avId in self.lookees

    def getAvIdsLookingAtUs(self):
        return self.lookers

    def getAvIdsWeAreLookingAt(self):
        return self.lookees

    def setFocus(self, object):
        if isinstance(self.focus, DistributedObjectAI.DistributedObjectAI):
            self.ignore(self.focus.getDeleteEvent())
            self.lastInteractTime.setdefault(self.focus.doId, 0)

        PetBrain.notify.debug('setFocus: %s' % object)
        self.focus = object
        if isinstance(self.focus, DistributedObjectAI.DistributedObjectAI):
            self.accept(self.focus.getDeleteEvent(), self._handleFocusHasLeft)

    def getFocus(self):
        return self.focus

    def clearFocus(self):
        self.setFocus(None)

    def _handleFocusHasLeft(self):
        if self.focus.isEmpty():
            self.chaseNode.setPos(self.pet, 0, 0, 0)
        else:
            self.chaseNode.setPos(self.focus, 0, 0, 0)
        self._inspectSpot(self.chaseNode)

    def _chase(self, target):
        if callable(target):
            target = target()

        if target is None:
            return 0

        self.setFocus(target)
        self.pet.actionFSM.request('Chase', target)
        return 1

    def _wander(self):
        self.clearFocus()
        self.pet.actionFSM.request('Wander')
        return 1

    def _unstick(self):
        self.clearFocus()
        self.pet.actionFSM.request('Unstick')
        return 1

    def _flee(self, chaser):
        if callable(chaser):
            chaser = chaser()

        if chaser is None:
            return 0

        self.setFocus(chaser)
        self.pet.actionFSM.request('Flee', chaser)
        return 1

    def _inspectSpot(self, spot=None):
        if spot is None:
            spot = NodePath('randomSpot')
            spot.setPos(randFloat(-20, 20), randFloat(-20, 20), 0)

        self.setFocus(spot)
        self.pet.actionFSM.request('InspectSpot', spot)
        return 1

    def _stay(self, avatar):
        self.setFocus(avatar)
        self.pet.actionFSM.request('Stay', avatar)
        return 1

    def _doTrick(self, trickId, avatar):
        self.setFocus(avatar)
        self.pet.actionFSM.request('Trick', avatar, trickId)
        return 1

    def _heal(self, avatar):
        if callable(avatar):
            avatar = avatar()

        if avatar is None:
            return 0

        self.setFocus(avatar)
        self.pet.actionFSM.request('Heal', avatar)
        return 1

    def _startMovie(self):
        self.setFocus(None)
        self.pet.actionFSM.request('Movie')
        self.inMovie = 1

    def _endMovie(self):
        self.inMovie = 0

    def _handleGenericObserve(self, observe):
        pass

    def _handleActionObserve(self, observe):
        action = observe.getAction()
        avId = observe.getAvId()
        OA = PetObserve.Actions
        dbg = PetBrain.notify.debug
        if action == OA.ATTENDED_START:
            dbg('avatar %s is looking at me' % avId)
            self.pet.lerpMoods({
                'boredom': -0.10000000000000001,
                'excitement': 0.050000000000000003,
                'loneliness': -0.050000000000000003
            })
            messenger.send(self.getObserveEventAttendedByAvStart(avId))
        elif action == OA.ATTENDED_STOP:
            dbg('avatar %s is no longer looking at me' % avId)
            messenger.send(self.getObserveEventAttendedByAvStop(avId))
        elif action == OA.ATTENDING_START:
            dbg('I am looking at avatar %s' % avId)
            messenger.send(self.getObserveEventAttendingAvStart(avId))
        elif action == OA.ATTENDING_STOP:
            dbg('I am no longer looking at avatar %s' % avId)
            messenger.send(self.getObserveEventAttendingAvStop(avId))
        elif action == OA.CHANGE_ZONE:
            if avId != self.pet.doId:
                (oldZoneId, newZoneId) = observe.getData()
                PetBrain.notify.debug(
                    '%s.CHANGE_ZONE: %s, %s->%s' % (self.pet.doId, avId,
                                                    oldZoneId, newZoneId))
                myZoneId = self.pet.zoneId
                if newZoneId != oldZoneId:
                    if newZoneId == myZoneId:
                        self._handleAvatarArrive(avId)
                    elif oldZoneId == myZoneId:
                        self._handleAvatarLeave(avId)

                if self.pet.inEstate:
                    if avId in (self.pet.ownerId, self.pet.estateOwnerId):
                        if oldZoneId in self.pet.estateZones and newZoneId not in self.pet.estateZones:
                            if avId == self.pet.ownerId:
                                self._handleOwnerLeave()
                            else:
                                self._handleEstateOwnerLeave()

        elif action == OA.LOGOUT:
            if avId == self.pet.ownerId:
                self._handleOwnerLeave()
            elif avId == self.pet.estateOwnerId:
                self._handleEstateOwnerLeave()

        elif action == OA.FEED:
            dbg('avatar %s is feeding me' % avId)
            self.pet.lerpMoods({
                'affection': 0.34999999999999998,
                'anger': -0.070000000000000007,
                'boredom': -0.5,
                'excitement': 0.5,
                'fatigue': -0.20000000000000001,
                'hunger': -0.5,
                'loneliness': -0.080000000000000002,
                'playfulness': 0.10000000000000001,
                'restlessness': -0.050000000000000003,
                'sadness': -0.20000000000000001
            })
            self.updateLastInteractTime(avId)
            avatar = simbase.air.doId2do.get(avId)
            if avatar is not None:
                avatar.setHatePets(0)

        elif action == OA.SCRATCH:
            dbg('avatar %s is scratching me' % avId)
            self.pet.lerpMoods({
                'affection': 0.45000000000000001,
                'anger': -0.10000000000000001,
                'boredom': -0.80000000000000004,
                'excitement': 0.5,
                'fatigue': -0.25,
                'loneliness': -0.20000000000000001,
                'playfulness': 0.10000000000000001,
                'restlessness': -0.20000000000000001,
                'sadness': -0.20000000000000001
            })
            self.updateLastInteractTime(avId)
            avatar = simbase.air.doId2do.get(avId)
            if avatar is not None:
                avatar.setHatePets(0)

        elif action == OA.GARDEN:
            dbg('avatar %s is gardening' % avId)
            avatar = simbase.air.doId2do.get(avId)
            if avatar is not None:
                if self.getFocus() == avatar:
                    self._wander()

    def _handlePhraseObserve(self, observe):
        def _handleGettingFriendlyAttention(avId, self=self):
            self.pet.lerpMoods({
                'boredom': -0.84999999999999998,
                'restlessness': -0.10000000000000001,
                'playfulness': 0.20000000000000001,
                'loneliness': -0.40000000000000002,
                'sadness': -0.10000000000000001,
                'fatigue': -0.050000000000000003,
                'excitement': 0.050000000000000003,
                'anger': -0.050000000000000003
            })
            self.updateLastInteractTime(avId)

        def _handleComeHere(avId, self=self):
            avatar = simbase.air.doId2do.get(avId)
            if avatar:
                self._chase(avatar)
                avatar.setHatePets(0)

        def _handleFollowMe(avId, self=self):
            avatar = simbase.air.doId2do.get(avId)
            if avatar:
                self._chase(avatar)
                avatar.setHatePets(0)

        def _handleStay(avId, self=self):
            avatar = simbase.air.doId2do.get(avId)
            if avatar:
                self._stay(avatar)

        def _handleCriticism(avId, self=self):
            ownerFactor = 0.5
            if avId == self.pet.ownerId:
                ownerFactor = 1.0

            self.pet.lerpMoods({
                'affection': -0.40000000000000002,
                'anger': 0.40000000000000002,
                'boredom': -0.29999999999999999,
                'confusion': 0.050000000000000003,
                'fatigue': 0.20000000000000001,
                'playfulness': -0.10000000000000001,
                'sadness': 0.5 * ownerFactor
            })

        def _handleGoAway(avId, self=self):
            avatar = simbase.air.doId2do.get(avId)
            if avatar is not None:
                if self.getFocus() == avatar:
                    self._wander()

        def _handleDoTrick(trickId, avId, self=self):
            avatar = simbase.air.doId2do.get(avId)
            if avatar:
                if self.lookedAtBy(avatar.doId):
                    if not self.goalMgr.hasTrickGoal():
                        if not self.pet._willDoTrick(trickId):
                            self.pet.trickFailLogger.addEvent(trickId)
                            trickId = PetTricks.Tricks.BALK

                        trickGoal = PetGoal.DoTrick(avatar, trickId)
                        self.goalMgr.addGoal(trickGoal)

        phrase = observe.getPetPhrase()
        avId = observe.getAvId()
        OP = PetObserve.Phrases
        if phrase in list2dict([
                OP.COME, OP.FOLLOW_ME, OP.STAY, OP.NEED_LAFF, OP.NEED_GAGS,
                OP.NEED_JB, OP.HI, OP.SOOTHE, OP.PRAISE, OP.HAPPY, OP.QUESTION,
                OP.FRIENDLY, OP.LETS_PLAY, OP.DO_TRICK
        ]):
            _handleGettingFriendlyAttention(avId)

        if phrase == OP.COME:
            _handleComeHere(avId)

        if phrase == OP.FOLLOW_ME:
            _handleFollowMe(avId)

        if phrase == OP.STAY:
            _handleStay(avId)

        if phrase == OP.CRITICISM:
            _handleCriticism(avId)

        if phrase == OP.GO_AWAY:
            _handleGoAway(avId)

        if phrase == OP.DO_TRICK:
            _handleDoTrick(observe.getTrickId(), avId)

    def _addGoalsReAvatar(self, avId):
        av = self.pet.air.doId2do.get(avId)
        if av is None:
            PetBrain.notify.warning('%s._addGoalsReAvatar: %s not in doId2do' %
                                    (self.pet.doId, avId))
            return None

        if avId not in self.doId2goals:
            goals = [PetGoal.ChaseAvatar(av), PetGoal.FleeFromAvatar(av)]
            self.doId2goals[avId] = goals
            self.lastInteractTime.setdefault(avId, 0)

        for goal in self.doId2goals[avId]:
            self.goalMgr.addGoal(goal)

    def _removeGoalsReAvatar(self, avId):
        if avId not in self.doId2goals:
            PetBrain.notify.warning('no goals re av %s to remove' % avId)
            return None

        for goal in self.doId2goals[avId]:
            self.goalMgr.removeGoal(goal)
            goal.destroy()

        del self.doId2goals[avId]

    def _considerBecomeAwareOf(self, avId):
        av = simbase.air.doId2do.get(avId)
        if av is None:
            PetBrain.notify.warning(
                '_considerBecomeAwareOf: av %s does not exist' % avId)
            return None

        if avId in self.avAwareness:
            return None

        def becomeAwareOf(avId, self=self):
            self.avAwareness[avId] = None
            self._addGoalsReAvatar(avId)

        if len(self.avAwareness) < PetConstants.MaxAvatarAwareness:
            becomeAwareOf(avId)
            return None

        def calcInterest(avId, self=self):
            if avId == self.pet.ownerId:
                return 100.0

            return random.random()

        avInterest = calcInterest(avId)
        minInterest = avInterest
        minInterestAvId = avId
        for awAvId in self.avAwareness:
            i = calcInterest(awAvId)
            if i < minInterest:
                minInterest = i
                minInterestAvId = awAvId
                break
                continue

        if minInterestAvId != avId:
            self._removeAwarenessOf(minInterestAvId)
            becomeAwareOf(avId)

    def _removeAwarenessOf(self, avId):
        if avId in self.avAwareness:
            self._removeGoalsReAvatar(avId)
            del self.avAwareness[avId]

    def _handleAvatarArrive(self, avId):
        PetBrain.notify.debug(
            '%s._handleAvatarArrive: %s' % (self.pet.doId, avId))
        if avId in self.nearbyAvs:
            PetBrain.notify.warning('%s already in self.nearbyAvs' % avId)
            return None

        self.nearbyAvs[avId] = None
        excitement = 0.29999999999999999
        if avId == self.pet.ownerId:
            excitement = 0.69999999999999996

        self.pet.lerpMoods({
            'excitement': 0.69999999999999996,
            'loneliness': -0.40000000000000002
        })
        self._considerBecomeAwareOf(avId)

    def _handleAvatarLeave(self, avId):
        PetBrain.notify.debug(
            '%s._handleAvatarLeave: %s' % (self.pet.doId, avId))
        if avId not in self.nearbyAvs:
            PetBrain.notify.warning('av %s not in self.nearbyAvs' % avId)
            return None

        del self.nearbyAvs[avId]
        self.pet.lerpMoods({'loneliness': 0.10000000000000001})
        self._removeAwarenessOf(avId)

    def _handleOwnerLeave(self):
        self.pet.teleportOut()
        taskMgr.doMethodLater(
            PetConstants.TELEPORT_OUT_DURATION, self.pet.requestDelete,
            self.getTeleportTaskName())

    def _handleEstateOwnerLeave(self):
        self.pet.teleportOut()
        taskMgr.doMethodLater(
            PetConstants.TELEPORT_OUT_DURATION, self.pet.requestDelete,
            self.getTeleportTaskName())
