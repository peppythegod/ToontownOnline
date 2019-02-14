from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toontowngui import TTDialog
from otp.otpbase import OTPLocalizer
from toontown.toontowngui import ToonHeadDialog
from direct.gui.DirectGui import DGG
from otp.otpbase import OTPGlobals
from toontown.toonbase import TTLocalizer


class BoardingGroupInviterPanels:
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'BoardingGroupInviterPanels')

    def __init__(self):
        self._BoardingGroupInviterPanels__invitingPanel = None
        self._BoardingGroupInviterPanels__invitationRejectedPanel = None

    def cleanup(self):
        self.destroyInvitingPanel()
        self.destroyInvitationRejectedPanel()

    def createInvitingPanel(self, boardingParty, inviteeId, **kw):
        self.destroyInvitingPanel()
        self.destroyInvitationRejectedPanel()
        self.notify.debug('Creating Inviting Panel.')
        self._BoardingGroupInviterPanels__invitingPanel = BoardingGroupInvitingPanel(
            boardingParty, inviteeId, **None)

    def createInvitationRejectedPanel(self, boardingParty, inviteeId, **kw):
        self.destroyInvitingPanel()
        self.destroyInvitationRejectedPanel()
        self.notify.debug('Creating Invititation Rejected Panel.')
        self._BoardingGroupInviterPanels__invitationRejectedPanel = BoardingGroupInvitationRejectedPanel(
            boardingParty, inviteeId, **None)

    def destroyInvitingPanel(self):
        if self.isInvitingPanelUp():
            self._BoardingGroupInviterPanels__invitingPanel.cleanup()
            self._BoardingGroupInviterPanels__invitingPanel = None

    def destroyInvitationRejectedPanel(self):
        if self.isInvitationRejectedPanelUp():
            self._BoardingGroupInviterPanels__invitationRejectedPanel.cleanup()
            self._BoardingGroupInviterPanels__invitationRejectedPanel = None

    def isInvitingPanelIdCorrect(self, inviteeId):
        if self.isInvitingPanelUp():
            if inviteeId == self._BoardingGroupInviterPanels__invitingPanel.avId:
                return True
            else:
                self.notify.warning(
                    'Got a response back from an invitee, but a different invitee panel was open. Maybe lag?'
                )

        return False

    def isInvitingPanelUp(self):
        if self._BoardingGroupInviterPanels__invitingPanel:
            if not self._BoardingGroupInviterPanels__invitingPanel.isEmpty():
                return True

            self._BoardingGroupInviterPanels__invitingPanel = None

        return False

    def isInvitationRejectedPanelUp(self):
        if self._BoardingGroupInviterPanels__invitationRejectedPanel:
            if not self._BoardingGroupInviterPanels__invitationRejectedPanel.isEmpty(
            ):
                return True

            self._BoardingGroupInviterPanels__invitationRejectedPanel = None

        return False

    def forceCleanup(self):
        if self.isInvitingPanelUp():
            self._BoardingGroupInviterPanels__invitingPanel.forceCleanup()
            self._BoardingGroupInviterPanels__invitingPanel = None

        if self.isInvitationRejectedPanelUp():
            self._BoardingGroupInviterPanels__invitationRejectedPanel.forceCleanup(
            )
            self._BoardingGroupInviterPanels__invitationRejectedPanel = None


class BoardingGroupInviterPanelBase(ToonHeadDialog.ToonHeadDialog):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'BoardingGroupInviterPanelBase')

    def __init__(self, boardingParty, inviteeId, **kw):
        self.boardingParty = boardingParty
        self.avId = inviteeId
        avatar = base.cr.doId2do.get(self.avId)
        self.avatarName = ''
        if avatar:
            self.avatar = avatar
            self.avatarName = avatar.getName()
            avatarDNA = avatar.getStyle()

        self.defineParams()
        command = self.handleButton
        optiondefs = (('dialogName', self.dialogName,
                       None), ('text', self.inviterText,
                               None), ('style', self.panelStyle, None),
                      ('buttonTextList', self.buttonTextList,
                       None), ('command', command, None),
                      ('image_color', (1.0, 0.89000000000000001,
                                       0.77000000000000002, 1.0),
                       None), ('geom_scale', 0.20000000000000001,
                               None), ('geom_pos', (-0.10000000000000001, 0,
                                                    -0.025000000000000001),
                                       None), ('pad', (0.074999999999999997,
                                                       0.074999999999999997),
                                               None), ('topPad', 0, None),
                      ('midPad', 0, None), ('pos', (0.45000000000000001, 0,
                                                    0.75), None), ('scale',
                                                                   0.75, None))
        self.defineoptions(kw, optiondefs)
        ToonHeadDialog.ToonHeadDialog.__init__(self, avatarDNA)
        self.show()

    def defineParams(self):
        self.notify.error(
            'setupParams: This method should not be called from the base class. Derived class should override this method'
        )

    def cleanup(self):
        self.notify.debug('Destroying Panel.')
        ToonHeadDialog.ToonHeadDialog.cleanup(self)

    def forceCleanup(self):
        self.handleButton(0)

    def handleButton(self, value):
        self.cleanup()


class BoardingGroupInvitingPanel(BoardingGroupInviterPanelBase):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'BoardingGroupInvitingPanel')

    def __init__(self, boardingParty, inviteeId, **kw):
        BoardingGroupInviterPanelBase.__init__(self, boardingParty, inviteeId,
                                               **None)
        self.initialiseoptions(BoardingGroupInvitingPanel)
        self.setupUnexpectedExitHooks()

    def defineParams(self):
        self.dialogName = 'BoardingGroupInvitingPanel'
        self.inviterText = TTLocalizer.BoardingInvitingMessage % self.avatarName
        self.panelStyle = TTDialog.CancelOnly
        self.buttonTextList = [OTPLocalizer.GuildInviterCancel]

    def handleButton(self, value):
        self.boardingParty.requestCancelInvite(self.avId)
        BoardingGroupInviterPanelBase.cleanup(self)

    def setupUnexpectedExitHooks(self):
        if base.cr.doId2do.has_key(self.avId):
            toon = base.cr.doId2do[self.avId]
            self.unexpectedExitEventName = toon.uniqueName('disable')
            self.accept(self.unexpectedExitEventName, self.forceCleanup)

    def forceCleanup(self):
        self.ignore(self.unexpectedExitEventName)
        BoardingGroupInviterPanelBase.forceCleanup(self)


class BoardingGroupInvitationRejectedPanel(BoardingGroupInviterPanelBase):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'BoardingGroupInvitationRejectedPanel')

    def __init__(self, boardingParty, inviteeId, **kw):
        BoardingGroupInviterPanelBase.__init__(self, boardingParty, inviteeId,
                                               **None)
        self.initialiseoptions(BoardingGroupInvitationRejectedPanel)

    def defineParams(self):
        self.dialogName = 'BoardingGroupInvitationRejectedPanel'
        self.inviterText = TTLocalizer.BoardingInvitationRejected % self.avatarName
        self.panelStyle = TTDialog.Acknowledge
        self.buttonTextList = [OTPLocalizer.GuildInviterOK]
