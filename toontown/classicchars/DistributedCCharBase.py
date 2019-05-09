from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from otp.avatar import Avatar
from libotp import CFQuicktalker
from toontown.char import CharDNA
from toontown.char import DistributedChar
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.controls.ControlManager import CollisionHandlerRayStart
from toontown.toonbase import ToontownGlobals
from toontown.toonbase.TTLocalizer import Donald, DonaldDock, WesternPluto, Pluto
from toontown.effects import DustCloud
import CCharChatter
import CCharPaths
import string
import copy


class DistributedCCharBase(DistributedChar.DistributedChar):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedCCharBase')

    def __init__(self, cr, name, dnaName):
        self.DistributedCCharBase_initialized = 1

        DistributedChar.DistributedChar.__init__(self, cr)
        dna = CharDNA.CharDNA()
        dna.newChar(dnaName)
        self.setDNA(dna)
        self.setName(name)
        self.setTransparency(TransparencyAttrib.MDual, 1)
        fadeIn = self.colorScaleInterval(
            0.5,
            Vec4(1, 1, 1, 1),
            startColorScale=Vec4(1, 1, 1, 0),
            blendType='easeInOut')
        fadeIn.start()
        self.diffPath = None
        self.transitionToCostume = 0
        self._DistributedCCharBase__initCollisions()

    def _DistributedCCharBase__initCollisions(self):
        self.cSphere = CollisionSphere(0.0, 0.0, 0.0, 8.0)
        self.cSphere.setTangible(0)
        self.cSphereNode = CollisionNode(self.getName() + 'BlatherSphere')
        self.cSphereNode.addSolid(self.cSphere)
        self.cSphereNodePath = self.attachNewNode(self.cSphereNode)
        self.cSphereNodePath.hide()
        self.cSphereNode.setCollideMask(ToontownGlobals.WallBitmask)
        self.acceptOnce('enter' + self.cSphereNode.getName(),
                        self._DistributedCCharBase__handleCollisionSphereEnter)
        self.cRay = CollisionRay(0.0, 0.0, CollisionHandlerRayStart, 0.0, 0.0,
                                 -1.0)
        self.cRayNode = CollisionNode(self.getName() + 'cRay')
        self.cRayNode.addSolid(self.cRay)
        self.cRayNodePath = self.attachNewNode(self.cRayNode)
        self.cRayNodePath.hide()
        self.cRayBitMask = ToontownGlobals.FloorBitmask
        self.cRayNode.setFromCollideMask(self.cRayBitMask)
        self.cRayNode.setIntoCollideMask(BitMask32.allOff())
        self.lifter = CollisionHandlerFloor()
        self.lifter.setOffset(ToontownGlobals.FloorOffset)
        self.lifter.setReach(10.0)
        self.lifter.setMaxVelocity(0.0)
        self.lifter.addCollider(self.cRayNodePath, self)
        self.cTrav = base.localAvatar.cTrav

    def _DistributedCCharBase__deleteCollisions(self):
        del self.cSphere
        del self.cSphereNode
        self.cSphereNodePath.removeNode()
        del self.cSphereNodePath
        self.cRay = None
        self.cRayNode = None
        self.cRayNodePath = None
        self.lifter = None
        self.cTrav = None

    def disable(self):
        self.stopBlink()
        self.ignoreAll()
        self.chatTrack.finish()
        del self.chatTrack
        if self.chatterDialogue:
            self.chatterDialogue.stop()

        del self.chatterDialogue
        DistributedChar.DistributedChar.disable(self)
        self.stopEarTask()

    def delete(self):
        self.setParent(NodePath('Temp'))
        self.DistributedCCharBase_deleted = 1
        self._DistributedCCharBase__deleteCollisions()
        DistributedChar.DistributedChar.delete(self)

    def generate(self, diffPath=None):
        DistributedChar.DistributedChar.generate(self)
        if diffPath is None:
            self.setPos(
                CCharPaths.getNodePos(
                    CCharPaths.startNode,
                    CCharPaths.getPaths(self.getName(), self.getCCLocation())))
        else:
            self.setPos(
                CCharPaths.getNodePos(
                    CCharPaths.startNode,
                    CCharPaths.getPaths(diffPath, self.getCCLocation())))
        self.setHpr(0, 0, 0)
        self.setParent(ToontownGlobals.SPRender)
        self.startBlink()
        self.startEarTask()
        self.chatTrack = Sequence()
        self.chatterDialogue = None
        self.acceptOnce('enter' + self.cSphereNode.getName(),
                        self._DistributedCCharBase__handleCollisionSphereEnter)
        self.accept('exitSafeZone',
                    self._DistributedCCharBase__handleExitSafeZone)

    def _DistributedCCharBase__handleExitSafeZone(self):
        self._DistributedCCharBase__handleCollisionSphereExit(None)

    def _DistributedCCharBase__handleCollisionSphereEnter(self, collEntry):
        self.notify.debug('Entering collision sphere...')
        self.sendUpdate('avatarEnter', [])
        self.accept('chatUpdate', self._DistributedCCharBase__handleChatUpdate)
        self.accept('chatUpdateSC',
                    self._DistributedCCharBase__handleChatUpdateSC)
        self.accept('chatUpdateSCCustom',
                    self._DistributedCCharBase__handleChatUpdateSCCustom)
        self.accept('chatUpdateSCToontask',
                    self._DistributedCCharBase__handleChatUpdateSCToontask)
        self.nametag3d.setBin('transparent', 100)
        self.acceptOnce('exit' + self.cSphereNode.getName(),
                        self._DistributedCCharBase__handleCollisionSphereExit)

    def _DistributedCCharBase__handleCollisionSphereExit(self, collEntry):
        self.notify.debug('Exiting collision sphere...')
        self.sendUpdate('avatarExit', [])
        self.ignore('chatUpdate')
        self.ignore('chatUpdateSC')
        self.ignore('chatUpdateSCCustom')
        self.ignore('chatUpdateSCToontask')
        self.acceptOnce('enter' + self.cSphereNode.getName(),
                        self._DistributedCCharBase__handleCollisionSphereEnter)

    def _DistributedCCharBase__handleChatUpdate(self, msg, chatFlags):
        self.sendUpdate('setNearbyAvatarChat', [msg])

    def _DistributedCCharBase__handleChatUpdateSC(self, msgIndex):
        self.sendUpdate('setNearbyAvatarSC', [msgIndex])

    def _DistributedCCharBase__handleChatUpdateSCCustom(self, msgIndex):
        self.sendUpdate('setNearbyAvatarSCCustom', [msgIndex])

    def _DistributedCCharBase__handleChatUpdateSCToontask(
            self, taskId, toNpcId, toonProgress, msgIndex):
        self.sendUpdate('setNearbyAvatarSCToontask',
                        [taskId, toNpcId, toonProgress, msgIndex])

    def makeTurnToHeadingTrack(self, heading):
        curHpr = self.getHpr()
        destHpr = self.getHpr()
        destHpr.setX(heading)
        if destHpr[0] - curHpr[0] > 180.0:
            destHpr.setX(destHpr[0] - 360)
        elif destHpr[0] - curHpr[0] < -180.0:
            destHpr.setX(destHpr[0] + 360)

        turnSpeed = 180.0
        time = abs(destHpr[0] - curHpr[0]) / turnSpeed
        turnTracks = Parallel()
        if time > 0.20000000000000001:
            turnTracks.append(
                Sequence(
                    Func(self.loop, 'walk'), Wait(time),
                    Func(self.loop, 'neutral')))

        turnTracks.append(
            LerpHprInterval(
                self, time, destHpr, name='lerp' + self.getName() + 'Hpr'))
        return turnTracks

    def setChat(self, category, msg, avId):
        if avId in self.cr.doId2do:
            avatar = self.cr.doId2do[avId]
            chatter = CCharChatter.getChatter(self.getName(),
                                              self.getCCChatter())
            if category >= len(chatter):
                self.notify.debug("Chatter's changed")
                return None
            elif len(chatter[category]) <= msg:
                self.notify.debug("Chatter's changed")
                return None

            str = chatter[category][msg]
            if '%' in str:
                str = copy.deepcopy(str)
                avName = avatar.getName()
                str = string.replace(str, '%', avName)

            track = Sequence()
            if category != CCharChatter.GOODBYE:
                curHpr = self.getHpr()
                self.headsUp(avatar)
                destHpr = self.getHpr()
                self.setHpr(curHpr)
                track.append(self.makeTurnToHeadingTrack(destHpr[0]))

            if self.getName() == Donald and self.getName(
            ) == WesternPluto or self.getName() == Pluto:
                chatFlags = CFThought | CFTimeout
                if hasattr(base.cr, 'newsManager') and base.cr.newsManager:
                    holidayIds = base.cr.newsManager.getHolidayIdList()
                    if ToontownGlobals.APRIL_FOOLS_COSTUMES in holidayIds:
                        if self.getName() == Pluto:
                            chatFlags = CFTimeout | CFSpeech

            elif self.getName() == DonaldDock:
                chatFlags = CFTimeout | CFSpeech
                self.nametag3d.hide()
            else:
                chatFlags = CFTimeout | CFSpeech
            self.chatterDialogue = self.getChatterDialogue(category, msg)
            track.append(
                Func(self.setChatAbsolute, str, chatFlags,
                     self.chatterDialogue))
            self.chatTrack.finish()
            self.chatTrack = track
            self.chatTrack.start()

    def setWalk(self, srcNode, destNode, timestamp):
        pass

    def walkSpeed(self):
        return 0.10000000000000001

    def enableRaycast(self, enable=1):
        if not (self.cTrav) and not hasattr(self,
                                            'cRayNode') or not (self.cRayNode):
            self.notify.debug('raycast info not found for ' + self.getName())
            return None

        self.cTrav.removeCollider(self.cRayNodePath)
        if enable:
            if self.notify.getDebug():
                self.notify.debug('enabling raycast for ' + self.getName())

            self.cTrav.addCollider(self.cRayNodePath, self.lifter)
        elif self.notify.getDebug():
            self.notify.debug('disabling raycast for ' + self.getName())

    def getCCLocation(self):
        return 0

    def getCCChatter(self):
        self.handleHolidays()
        return self.CCChatter

    def handleHolidays(self):
        self.CCChatter = 0
        if hasattr(base.cr, 'newsManager') and base.cr.newsManager:
            holidayIds = base.cr.newsManager.getHolidayIdList()
            if ToontownGlobals.CRASHED_LEADERBOARD in holidayIds:
                self.CCChatter = ToontownGlobals.CRASHED_LEADERBOARD
            elif ToontownGlobals.CIRCUIT_RACING_EVENT in holidayIds:
                self.CCChatter = ToontownGlobals.CIRCUIT_RACING_EVENT
            elif ToontownGlobals.WINTER_CAROLING in holidayIds:
                self.CCChatter = ToontownGlobals.WINTER_CAROLING
            elif ToontownGlobals.WINTER_DECORATIONS in holidayIds:
                self.CCChatter = ToontownGlobals.WINTER_DECORATIONS
            elif ToontownGlobals.WACKY_WINTER_CAROLING in holidayIds:
                self.CCChatter = ToontownGlobals.WACKY_WINTER_CAROLING
            elif ToontownGlobals.WACKY_WINTER_DECORATIONS in holidayIds:
                self.CCChatter = ToontownGlobals.WACKY_WINTER_DECORATIONS
            elif ToontownGlobals.VALENTINES_DAY in holidayIds:
                self.CCChatter = ToontownGlobals.VALENTINES_DAY
            elif ToontownGlobals.APRIL_FOOLS_COSTUMES in holidayIds:
                self.CCChatter = ToontownGlobals.APRIL_FOOLS_COSTUMES
            elif ToontownGlobals.SILLY_CHATTER_ONE in holidayIds:
                self.CCChatter = ToontownGlobals.SILLY_CHATTER_ONE
            elif ToontownGlobals.SILLY_CHATTER_TWO in holidayIds:
                self.CCChatter = ToontownGlobals.SILLY_CHATTER_TWO
            elif ToontownGlobals.SILLY_CHATTER_THREE in holidayIds:
                self.CCChatter = ToontownGlobals.SILLY_CHATTER_THREE
            elif ToontownGlobals.SILLY_CHATTER_FOUR in holidayIds:
                self.CCChatter = ToontownGlobals.SILLY_CHATTER_FOUR
            elif ToontownGlobals.SILLY_CHATTER_FIVE in holidayIds:
                self.CCChatter = ToontownGlobals.SILLY_CHATTER_FOUR
            elif ToontownGlobals.HALLOWEEN_COSTUMES in holidayIds:
                self.CCChatter = ToontownGlobals.HALLOWEEN_COSTUMES
            elif ToontownGlobals.SPOOKY_COSTUMES in holidayIds:
                self.CCChatter = ToontownGlobals.SPOOKY_COSTUMES
            elif ToontownGlobals.SELLBOT_FIELD_OFFICE in holidayIds:
                self.CCChatter = ToontownGlobals.SELLBOT_FIELD_OFFICE

    def fadeAway(self):
        fadeOut = self.colorScaleInterval(
            0.5,
            Vec4(1, 1, 1, 0.5),
            startColorScale=Vec4(1, 1, 1, 1),
            blendType='easeInOut')
        fadeOut.start()
        self.loop('neutral')
        if self.fsm:
            self.fsm.addState(
                State.State('TransitionToCostume',
                            self.enterTransitionToCostume,
                            self.exitTransitionToCostume, ['Off']))
            self.fsm.request('TransitionToCostume', force=1)

        self.ignoreAll()

    def enterTransitionToCostume(self):
        def getDustCloudIval():
            dustCloud = DustCloud.DustCloud(fBillboard=0, wantSound=1)
            dustCloud.setBillboardAxis(2.0)
            dustCloud.setZ(4)
            dustCloud.setScale(0.59999999999999998)
            dustCloud.createTrack()
            return Sequence(
                Func(dustCloud.reparentTo, self),
                dustCloud.track,
                Func(dustCloud.destroy),
                name='dustCloadIval')

        dust = getDustCloudIval()
        dust.start()

    def exitTransitionToCostume(self):
        pass
