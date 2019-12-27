from DistributedNPCToonBase import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
import NPCToons
from direct.task.Task import Task
from toontown.toonbase import TTLocalizer
from toontown.racing.KartShopGui import *
from toontown.racing.KartShopGlobals import *


class DistributedNPCKartClerk(DistributedNPCToonBase):
    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.isLocalToon = 0
        self.av = None
        self.button = None
        self.popupInfo = None
        self.kartShopGui = None

    def disable(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupKartShopGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.popupInfo:
            self.popupInfo.destroy()
            self.popupInfo = None

        if self.kartShopGui:
            self.kartShopGui.destroy()
            self.kartShopGui = None

        self.av = None
        if self.isLocalToon:
            base.localAvatar.posCamera(0, 0)

        DistributedNPCToonBase.disable(self)

    def generate(self):
        DistributedNPCToonBase.generate(self)

    def getCollSphereRadius(self):
        return 2.25

    def handleCollisionSphereEnter(self, collEntry):
        base.cr.playGame.getPlace().fsm.request('purchase')
        self.sendUpdate('avatarEnter', [])

    def _DistributedNPCKartClerk__handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')
        self.av = None

    def resetKartShopClerk(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupKartShopGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.kartShopGui:
            self.kartShopGui.destroy()
            self.kartShopGui = None

        self.show()
        self.startLookAround()
        self.detectAvatars()
        self.clearMat()
        if self.isLocalToon:
            self.freeAvatar()

        return Task.done

    def ignoreEventDict(self):
        for event in KartShopGlobals.EVENTDICT:
            self.ignore(event)

    def setMovie(self, mode, npcId, avId, extraArgs, timestamp):
        timeStamp = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        self.remain = NPCToons.CLERK_COUNTDOWN_TIME - timeStamp
        self.npcId = npcId
        self.isLocalToon = avId == base.localAvatar.doId
        if mode == NPCToons.SELL_MOVIE_CLEAR:
            return None

        if mode == NPCToons.SELL_MOVIE_TIMEOUT:
            taskMgr.remove(self.uniqueName('lerpCamera'))
            if self.isLocalToon:
                self.ignoreEventDict()
                if self.popupInfo:
                    self.popupInfo.reparentTo(hidden)

                if self.kartShopGui:
                    self.kartShopGui.destroy()
                    self.kartShopGui = None

            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG,
                                 CFSpeech | CFTimeout)
            self.resetKartShopClerk()
        elif mode == NPCToons.SELL_MOVIE_START:
            self.av = base.cr.doId2do.get(avId)
            if self.av is None:
                self.notify.warning('Avatar %d not found in doId' % avId)
                return None
            else:
                self.accept(
                    self.av.uniqueName('disable'),
                    self._DistributedNPCKartClerk__handleUnexpectedExit)
            self.setupAvatars(self.av)
            if self.isLocalToon:
                camera.wrtReparentTo(render)
                quat = Quat()
                quat.setHpr((-150, -2, 0))
                camera.posQuatInterval(1, Point3(-5, 9, base.localAvatar.getHeight() - 0.5), quat, other=self, blendType='easeOut').start()
                taskMgr.doMethodLater(1.0, self.popupKartShopGUI,
                                      self.uniqueName('popupKartShopGUI'))

        elif mode == NPCToons.SELL_MOVIE_COMPLETE:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GOODBYE,
                                 CFSpeech | CFTimeout)
            self.resetKartShopClerk()
        elif mode == NPCToons.SELL_MOVIE_PETCANCELED:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GOODBYE,
                                 CFSpeech | CFTimeout)
            self.resetKartShopClerk()
        elif mode == NPCToons.SELL_MOVIE_NO_MONEY:
            self.notify.warning('SELL_MOVIE_NO_MONEY should not be called')
            self.resetKartShopClerk()

    def _DistributedNPCKartClerk__handleBuyKart(self, kartID):
        self.sendUpdate('buyKart', [kartID])

    def _DistributedNPCKartClerk__handleBuyAccessory(self, accID):
        self.sendUpdate('buyAccessory', [accID])

    def _DistributedNPCKartClerk__handleGuiDone(self, bTimedOut=False):
        self.ignoreAll()
        if hasattr(self, 'kartShopGui') and self.kartShopGui != None:
            self.kartShopGui.destroy()
            self.kartShopGui = None

        if not bTimedOut:
            self.sendUpdate('transactionDone')

    def popupKartShopGUI(self, task):
        self.setChatAbsolute('', CFSpeech)
        self.accept(KartShopGlobals.EVENTDICT['buyAccessory'],
                    self._DistributedNPCKartClerk__handleBuyAccessory)
        self.accept(KartShopGlobals.EVENTDICT['buyKart'],
                    self._DistributedNPCKartClerk__handleBuyKart)
        self.acceptOnce(KartShopGlobals.EVENTDICT['guiDone'],
                        self._DistributedNPCKartClerk__handleGuiDone)
        self.kartShopGui = KartShopGuiMgr(KartShopGlobals.EVENTDICT)
