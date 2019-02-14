from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.showbase import DirectObject
from otp.avatar import AvatarPanel
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TTDialog
from otp.distributed import CentralLogger
IGNORE_SCALE = 0.059999999999999998
STOP_IGNORE_SCALE = 0.040000000000000001


class AvatarPanelBase(AvatarPanel.AvatarPanel):
    def __init__(self, avatar, FriendsListPanel=None):
        self.dialog = None
        self.category = None
        AvatarPanel.AvatarPanel.__init__(self, avatar, FriendsListPanel)

    def getIgnoreButtonInfo(self):
        if base.cr.avatarFriendsManager.checkIgnored(self.avId):
            return (TTLocalizer.AvatarPanelStopIgnoring,
                    self.handleStopIgnoring, STOP_IGNORE_SCALE)
        else:
            return (TTLocalizer.AvatarPanelIgnore, self.handleIgnore,
                    IGNORE_SCALE)

    def handleIgnore(self):
        isAvatarFriend = base.cr.isFriend(self.avatar.doId)
        isPlayerFriend = base.cr.playerFriendsManager.isAvatarOwnerPlayerFriend(
            self.avatar.doId)
        if not isAvatarFriend:
            pass
        isFriend = isPlayerFriend
        if isFriend:
            self.dialog = TTDialog.TTGlobalDialog(
                style=TTDialog.CancelOnly,
                text=TTLocalizer.IgnorePanelAddFriendAvatar % self.avName,
                text_wordwrap=18.5,
                text_scale=0.059999999999999998,
                cancelButtonText=TTLocalizer.lCancel,
                doneEvent='IgnoreBlocked',
                command=self.freeLocalAvatar)
        else:
            self.dialog = TTDialog.TTGlobalDialog(
                style=TTDialog.TwoChoice,
                text=TTLocalizer.IgnorePanelAddIgnore % self.avName,
                text_wordwrap=18.5,
                text_scale=TTLocalizer.APBdialog,
                okButtonText=TTLocalizer.AvatarPanelIgnore,
                cancelButtonText=TTLocalizer.lCancel,
                doneEvent='IgnoreConfirm',
                command=self.handleIgnoreConfirm)
        DirectLabel(
            parent=self.dialog,
            relief=None,
            pos=(0, TTLocalizer.APBdirectLabelPosY, 0.125),
            text=TTLocalizer.IgnorePanelTitle,
            textMayChange=0,
            text_scale=0.080000000000000002)
        self.dialog.show()
        self._AvatarPanelBase__acceptStoppedStateMsg()
        self.requestStopped()

    def handleStopIgnoring(self):
        self.dialog = TTDialog.TTGlobalDialog(
            style=TTDialog.TwoChoice,
            text=TTLocalizer.IgnorePanelRemoveIgnore % self.avName,
            text_wordwrap=18.5,
            text_scale=0.059999999999999998,
            okButtonText=TTLocalizer.AvatarPanelStopIgnoring,
            cancelButtonText=TTLocalizer.lCancel,
            buttonPadSF=4.0,
            doneEvent='StopIgnoringConfirm',
            command=self.handleStopIgnoringConfirm)
        DirectLabel(
            parent=self.dialog,
            relief=None,
            pos=(0, TTLocalizer.APBdirectLabelPosY, 0.14999999999999999),
            text=TTLocalizer.IgnorePanelTitle,
            textMayChange=0,
            text_scale=0.080000000000000002)
        self.dialog.show()
        self._AvatarPanelBase__acceptStoppedStateMsg()
        self.requestStopped()

    def handleIgnoreConfirm(self, value):
        if value == -1:
            self.freeLocalAvatar()
            return None

        base.cr.avatarFriendsManager.addIgnore(self.avId)
        self.dialog = TTDialog.TTGlobalDialog(
            style=TTDialog.Acknowledge,
            text=TTLocalizer.IgnorePanelIgnore % self.avName,
            text_wordwrap=18.5,
            text_scale=0.059999999999999998,
            topPad=0.10000000000000001,
            doneEvent='IgnoreComplete',
            command=self.handleDoneIgnoring)
        DirectLabel(
            parent=self.dialog,
            relief=None,
            pos=(0, TTLocalizer.APBdirectLabelPosY, 0.14999999999999999),
            text=TTLocalizer.IgnorePanelTitle,
            textMayChange=0,
            text_scale=0.080000000000000002)
        self.dialog.show()
        self._AvatarPanelBase__acceptStoppedStateMsg()
        self.requestStopped()

    def handleStopIgnoringConfirm(self, value):
        if value == -1:
            self.freeLocalAvatar()
            return None

        base.cr.avatarFriendsManager.removeIgnore(self.avId)
        self.dialog = TTDialog.TTGlobalDialog(
            style=TTDialog.Acknowledge,
            text=TTLocalizer.IgnorePanelEndIgnore % self.avName,
            text_wordwrap=18.5,
            text_scale=0.059999999999999998,
            topPad=0.10000000000000001,
            doneEvent='StopIgnoringComplete',
            command=self.handleDoneIgnoring)
        DirectLabel(
            parent=self.dialog,
            relief=None,
            pos=(0, TTLocalizer.APBdirectLabelPosY, 0.14999999999999999),
            text=TTLocalizer.IgnorePanelTitle,
            textMayChange=0,
            text_scale=0.080000000000000002)
        self.dialog.show()
        self._AvatarPanelBase__acceptStoppedStateMsg()
        self.requestStopped()

    def handleDoneIgnoring(self, value):
        self.freeLocalAvatar()

    def handleReport(self):
        if base.cr.centralLogger.hasReportedPlayer(self.playerId, self.avId):
            self.alreadyReported()
        else:
            self.confirmReport()

    def confirmReport(self):
        if base.cr.isFriend(
                self.avId) or base.cr.playerFriendsManager.isPlayerFriend(
                    self.avId):
            string = TTLocalizer.ReportPanelBodyFriends
            titlePos = 0.40999999999999998
        else:
            string = TTLocalizer.ReportPanelBody
            titlePos = 0.34999999999999998
        self.dialog = TTDialog.TTGlobalDialog(
            style=TTDialog.TwoChoice,
            text=string % self.avName,
            text_wordwrap=18.5,
            text_scale=0.059999999999999998,
            okButtonText=TTLocalizer.AvatarPanelReport,
            cancelButtonText=TTLocalizer.lCancel,
            doneEvent='ReportConfirm',
            command=self.handleReportConfirm)
        DirectLabel(
            parent=self.dialog,
            relief=None,
            pos=(0, 0, titlePos),
            text=TTLocalizer.ReportPanelTitle,
            textMayChange=0,
            text_scale=0.080000000000000002)
        self.dialog.show()
        self._AvatarPanelBase__acceptStoppedStateMsg()
        self.requestStopped()

    def handleReportConfirm(self, value):
        self.cleanupDialog()
        if value == 1:
            self.chooseReportCategory()
        else:
            self.requestWalk()

    def alreadyReported(self):
        self.dialog = TTDialog.TTGlobalDialog(
            style=TTDialog.Acknowledge,
            text=TTLocalizer.ReportPanelAlreadyReported % self.avName,
            text_wordwrap=18.5,
            text_scale=0.059999999999999998,
            topPad=0.10000000000000001,
            doneEvent='AlreadyReported',
            command=self.handleAlreadyReported)
        DirectLabel(
            parent=self.dialog,
            relief=None,
            pos=(0, 0, 0.20000000000000001),
            text=TTLocalizer.ReportPanelTitle,
            textMayChange=0,
            text_scale=0.080000000000000002)
        self.dialog.show()
        self._AvatarPanelBase__acceptStoppedStateMsg()
        self.requestStopped()

    def handleAlreadyReported(self, value):
        self.freeLocalAvatar()

    def chooseReportCategory(self):
        self.dialog = TTDialog.TTGlobalDialog(
            pos=(0, 0, 0.40000000000000002),
            style=TTDialog.CancelOnly,
            text=TTLocalizer.ReportPanelCategoryBody % (self.avName,
                                                        self.avName),
            text_wordwrap=18.5,
            text_scale=0.059999999999999998,
            topPad=0.050000000000000003,
            midPad=0.75,
            cancelButtonText=TTLocalizer.lCancel,
            doneEvent='ReportCategory',
            command=self.handleReportCategory)
        DirectLabel(
            parent=self.dialog,
            relief=None,
            pos=(0, 0, 0.22500000000000001),
            text=TTLocalizer.ReportPanelTitle,
            textMayChange=0,
            text_scale=0.080000000000000002)
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        DirectButton(
            parent=self.dialog,
            relief=None,
            image=(guiButton.find('**/QuitBtn_UP'),
                   guiButton.find('**/QuitBtn_DN'),
                   guiButton.find('**/QuitBtn_RLVR')),
            image_scale=(2.125, 1.0, 1.0),
            text=TTLocalizer.ReportPanelCategoryLanguage,
            text_scale=0.059999999999999998,
            text_pos=(0, -0.0124),
            pos=(0, 0, -0.29999999999999999),
            command=self.handleReportCategory,
            extraArgs=[0])
        DirectButton(
            parent=self.dialog,
            relief=None,
            image=(guiButton.find('**/QuitBtn_UP'),
                   guiButton.find('**/QuitBtn_DN'),
                   guiButton.find('**/QuitBtn_RLVR')),
            image_scale=(2.1499999999999999, 1.0, 1.0),
            text=TTLocalizer.ReportPanelCategoryPii,
            text_scale=0.059999999999999998,
            text_pos=(0, -0.012500000000000001),
            pos=(0, 0, -0.42499999999999999),
            command=self.handleReportCategory,
            extraArgs=[1])
        DirectButton(
            parent=self.dialog,
            relief=None,
            image=(guiButton.find('**/QuitBtn_UP'),
                   guiButton.find('**/QuitBtn_DN'),
                   guiButton.find('**/QuitBtn_RLVR')),
            image_scale=(2.125, 1.0, 1.0),
            text=TTLocalizer.ReportPanelCategoryRude,
            text_scale=0.059999999999999998,
            text_pos=(0, -0.012500000000000001),
            pos=(0, 0, -0.55000000000000004),
            command=self.handleReportCategory,
            extraArgs=[2])
        DirectButton(
            parent=self.dialog,
            relief=None,
            image=(guiButton.find('**/QuitBtn_UP'),
                   guiButton.find('**/QuitBtn_DN'),
                   guiButton.find('**/QuitBtn_RLVR')),
            image_scale=(2.125, 1.0, 1.0),
            text=TTLocalizer.ReportPanelCategoryName,
            text_scale=0.059999999999999998,
            text_pos=(0, -0.012500000000000001),
            pos=(0, 0, -0.67500000000000004),
            command=self.handleReportCategory,
            extraArgs=[3])
        DirectButton(
            parent=self.dialog,
            relief=None,
            image=(guiButton.find('**/QuitBtn_UP'),
                   guiButton.find('**/QuitBtn_DN'),
                   guiButton.find('**/QuitBtn_RLVR')),
            image_scale=(2.125, 1.0, 1.0),
            text=TTLocalizer.ReportPanelCategoryHacking,
            text_scale=0.059999999999999998,
            text_pos=(0, -0.012500000000000001),
            pos=(0, 0, -0.80000000000000004),
            command=self.handleReportCategory,
            extraArgs=[4])
        guiButton.removeNode()
        self.dialog.show()
        self._AvatarPanelBase__acceptStoppedStateMsg()
        self.requestStopped()

    def handleReportCategory(self, value):
        self.cleanupDialog()
        if value >= 0:
            cat = [
                CentralLogger.ReportFoulLanguage,
                CentralLogger.ReportPersonalInfo,
                CentralLogger.ReportRudeBehavior, CentralLogger.ReportBadName,
                CentralLogger.ReportHacking
            ]
            self.category = cat[value]
            self.confirmReportCategory(value)
        else:
            self.requestWalk()

    def confirmReportCategory(self, category):
        string = TTLocalizer.ReportPanelConfirmations[category]
        string += '\n\n' + TTLocalizer.ReportPanelWarning
        self.dialog = TTDialog.TTGlobalDialog(
            style=TTDialog.TwoChoice,
            text=string % self.avName,
            text_wordwrap=18.5,
            text_scale=0.059999999999999998,
            topPad=0.10000000000000001,
            okButtonText=TTLocalizer.AvatarPanelReport,
            cancelButtonText=TTLocalizer.lCancel,
            doneEvent='ReportConfirmCategory',
            command=self.handleReportCategoryConfirm)
        DirectLabel(
            parent=self.dialog,
            relief=None,
            pos=(0, 0, 0.5),
            text=TTLocalizer.ReportPanelTitle,
            textMayChange=0,
            text_scale=0.080000000000000002)
        self.dialog.show()
        self._AvatarPanelBase__acceptStoppedStateMsg()

    def handleReportCategoryConfirm(self, value):
        self.cleanupDialog()
        removed = 0
        isPlayer = 0
        if value > 0:
            if self.category == CentralLogger.ReportHacking:
                base.cr.centralLogger.reportPlayer(self.category,
                                                   self.playerId, self.avId)
                self.category = CentralLogger.ReportRudeBehavior

            base.cr.centralLogger.reportPlayer(self.category, self.playerId,
                                               self.avId)
            if base.cr.isFriend(self.avId):
                base.cr.removeFriend(self.avId)
                removed = 1

            if base.cr.playerFriendsManager.isPlayerFriend(self.playerId):
                if self.playerId:
                    base.cr.playerFriendsManager.sendRequestRemove(
                        self.playerId)
                    removed = 1
                    isPlayer = 1

            self.reportComplete(removed, isPlayer)
        else:
            self.requestWalk()

    def reportComplete(self, removed, isPlayer):
        string = TTLocalizer.ReportPanelThanks
        titlePos = 0.25
        if removed:
            if isPlayer:
                string += ' ' + TTLocalizer.ReportPanelRemovedPlayerFriend % self.playerId
            else:
                string += ' ' + TTLocalizer.ReportPanelRemovedFriend % self.avName
            titlePos = 0.29999999999999999

        self.dialog = TTDialog.TTGlobalDialog(
            style=TTDialog.Acknowledge,
            text=string,
            text_wordwrap=18.5,
            text_scale=0.059999999999999998,
            topPad=0.10000000000000001,
            doneEvent='ReportComplete',
            command=self.handleReportComplete)
        DirectLabel(
            parent=self.dialog,
            relief=None,
            pos=(0, 0, titlePos),
            text=TTLocalizer.ReportPanelTitle,
            textMayChange=0,
            text_scale=0.080000000000000002)
        self.dialog.show()
        self._AvatarPanelBase__acceptStoppedStateMsg()

    def handleReportComplete(self, value):
        self.freeLocalAvatar()

    def freeLocalAvatar(self, value=None):
        self.cleanupDialog()
        self.requestWalk()

    def cleanupDialog(self):
        if self.dialog:
            self.dialog.ignore('exitingStoppedState')
            self.dialog.cleanup()
            self.dialog = None

    def requestStopped(self):
        if not base.cr.playGame.getPlace().fsm.getCurrentState().getName(
        ) == 'stickerBook':
            if base.cr.playGame.getPlace().fsm.hasStateNamed('stopped'):
                base.cr.playGame.getPlace().fsm.request('stopped')
            else:
                self.notify.warning('skipping request to stopped in %s' %
                                    base.cr.playGame.getPlace())
        else:
            self.cleanup()

    def requestWalk(self):
        if base.cr.playGame.getPlace().fsm.hasStateNamed('finalBattle'):
            base.cr.playGame.getPlace().fsm.request('finalBattle')
        elif base.cr.playGame.getPlace().fsm.hasStateNamed('walk'):
            if base.cr.playGame.getPlace().getState() == 'stopped':
                base.cr.playGame.getPlace().fsm.request('walk')

        else:
            self.notify.warning(
                'skipping request to walk in %s' % base.cr.playGame.getPlace())

    def _AvatarPanelBase__acceptStoppedStateMsg(self):
        self.dialog.ignore('exitingStoppedState')
        self.dialog.accept('exitingStoppedState', self.cleanupDialog)
