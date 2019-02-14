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


class GroupInvitee(ToonHeadDialog.ToonHeadDialog):
    notify = DirectNotifyGlobal.directNotify.newCategory('GroupInvitee')

    def __init__(self):
        pass

    def make(self, party, toon, leaderId, **kw):
        self.leaderId = leaderId
        self.avName = toon.getName()
        self.av = toon
        self.avId = toon.doId
        self.avDNA = toon.getStyle()
        self.party = party
        text = TTLocalizer.BoardingInviteeMessage % self.avName
        style = TTDialog.TwoChoice
        buttonTextList = [
            OTPLocalizer.FriendInviteeOK, OTPLocalizer.FriendInviteeNo
        ]
        command = self._GroupInvitee__handleButton
        optiondefs = (('dialogName', 'GroupInvitee',
                       None), ('text', text, None), ('style', style, None),
                      ('buttonTextList', buttonTextList,
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
        ToonHeadDialog.ToonHeadDialog.__init__(self, self.avDNA)
        self.initialiseoptions(GroupInvitee)
        self.show()

    def cleanup(self):
        ToonHeadDialog.ToonHeadDialog.cleanup(self)

    def forceCleanup(self):
        self.party.requestRejectInvite(self.leaderId, self.avId)
        self.cleanup()

    def _GroupInvitee__handleButton(self, value):
        place = base.cr.playGame.getPlace()
        if value == DGG.DIALOG_OK and place and not (
                place.getState() == 'elevator'):
            self.party.requestAcceptInvite(self.leaderId, self.avId)
        else:
            self.party.requestRejectInvite(self.leaderId, self.avId)
        self.cleanup()
