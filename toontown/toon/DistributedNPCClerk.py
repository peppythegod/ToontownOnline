from pandac.PandaModules import *
from DistributedNPCToonBase import *
from toontown.minigame import ClerkPurchase
from toontown.shtiker.PurchaseManagerConstants import *
import NPCToons
from direct.task.Task import Task
from toontown.toonbase import TTLocalizer
from toontown.hood import ZoneUtil
from toontown.toontowngui import TeaserPanel


class DistributedNPCClerk(DistributedNPCToonBase):
    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.purchase = None
        self.isLocalToon = 0
        self.av = None
        self.purchaseDoneEvent = 'purchaseDone'

    def disable(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupPurchaseGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.purchase:
            self.purchase.exit()
            self.purchase.unload()
            self.purchase = None

        self.av = None
        base.localAvatar.posCamera(0, 0)
        DistributedNPCToonBase.disable(self)

    def allowedToEnter(self):
        if hasattr(base,
                   'ttAccess') and base.ttAccess and base.ttAccess.canAccess():
            return True

        return False

    def handleOkTeaser(self):
        self.dialog.destroy()
        del self.dialog
        place = base.cr.playGame.getPlace()
        if place:
            place.fsm.request('walk')

    def handleCollisionSphereEnter(self, collEntry):
        if self.allowedToEnter():
            base.cr.playGame.getPlace().fsm.request('purchase')
            self.sendUpdate('avatarEnter', [])
        else:
            place = base.cr.playGame.getPlace()
            if place:
                place.fsm.request('stopped')

            self.dialog = TeaserPanel.TeaserPanel(
                pageName='otherGags', doneFunc=self.handleOkTeaser)

    def _DistributedNPCClerk__handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')
        self.av = None

    def resetClerk(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupPurchaseGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.purchase:
            self.purchase.exit()
            self.purchase.unload()
            self.purchase = None

        self.clearMat()
        self.startLookAround()
        self.detectAvatars()
        if self.isLocalToon:
            self.freeAvatar()

        return Task.done

    def setMovie(self, mode, npcId, avId, timestamp):
        timeStamp = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        self.remain = NPCToons.CLERK_COUNTDOWN_TIME - timeStamp
        self.isLocalToon = avId == base.localAvatar.doId
        if mode == NPCToons.PURCHASE_MOVIE_CLEAR:
            return None

        if mode == NPCToons.PURCHASE_MOVIE_TIMEOUT:
            taskMgr.remove(self.uniqueName('popupPurchaseGUI'))
            taskMgr.remove(self.uniqueName('lerpCamera'))
            if self.isLocalToon:
                self.ignore(self.purchaseDoneEvent)

            if self.purchase:
                self._DistributedNPCClerk__handlePurchaseDone()

            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG,
                                 CFSpeech | CFTimeout)
            self.resetClerk()
        elif mode == NPCToons.PURCHASE_MOVIE_START:
            self.av = base.cr.doId2do.get(avId)
            if self.av is None:
                self.notify.warning('Avatar %d not found in doId' % avId)
                return None
            else:
                self.accept(
                    self.av.uniqueName('disable'),
                    self._DistributedNPCClerk__handleUnexpectedExit)
            self.setupAvatars(self.av)
            if self.isLocalToon:
                camera.wrtReparentTo(render)
                seq = Sequence((camera.posQuatInterval(1, Vec3(-5, 9, self.getHeight() - 0.5), Vec3(-150, -2, 0), other=self, blendType='easeOut', name=self.uniqueName('lerpCamera'))))
                seq.start()

            self.setChatAbsolute(TTLocalizer.STOREOWNER_GREETING,
                                 CFSpeech | CFTimeout)
            if self.isLocalToon:
                taskMgr.doMethodLater(1.0, self.popupPurchaseGUI,
                                      self.uniqueName('popupPurchaseGUI'))

        elif mode == NPCToons.PURCHASE_MOVIE_COMPLETE:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GOODBYE,
                                 CFSpeech | CFTimeout)
            self.resetClerk()
        elif mode == NPCToons.PURCHASE_MOVIE_NO_MONEY:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_NEEDJELLYBEANS,
                                 CFSpeech | CFTimeout)
            self.resetClerk()

    def popupPurchaseGUI(self, task):
        self.setChatAbsolute('', CFSpeech)
        self.acceptOnce(self.purchaseDoneEvent,
                        self._DistributedNPCClerk__handlePurchaseDone)
        self.accept('boughtGag', self._DistributedNPCClerk__handleBoughtGag)
        self.purchase = ClerkPurchase.ClerkPurchase(
            base.localAvatar, self.remain, self.purchaseDoneEvent)
        self.purchase.load()
        self.purchase.enter()
        return Task.done

    def _DistributedNPCClerk__handleBoughtGag(self):
        self.d_setInventory(base.localAvatar.inventory.makeNetString(),
                            base.localAvatar.getMoney(), 0)

    def _DistributedNPCClerk__handlePurchaseDone(self):
        self.ignore('boughtGag')
        self.d_setInventory(base.localAvatar.inventory.makeNetString(),
                            base.localAvatar.getMoney(), 1)
        self.purchase.exit()
        self.purchase.unload()
        self.purchase = None

    def d_setInventory(self, invString, money, done):
        self.sendUpdate('setInventory', [invString, money, done])
