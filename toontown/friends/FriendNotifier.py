from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toontowngui import TTDialog
from otp.otpbase import OTPLocalizer
from toontown.toontowngui import ToonHeadDialog
from direct.gui.DirectGui import DGG
from otp.otpbase import OTPGlobals


class FriendNotifier(ToonHeadDialog.ToonHeadDialog):
    notify = DirectNotifyGlobal.directNotify.newCategory('FriendNotifier')

    def __init__(self, avId, avName, avDNA, context, **kw):
        self.avId = avId
        self.avName = avName
        self.avDNA = avDNA
        self.context = context
        text = OTPLocalizer.FriendNotifictation % self.avName
        style = TTDialog.Acknowledge
        buttonText = [
            OTPLocalizer.FriendInviteeOK, OTPLocalizer.FriendInviteeOK
        ]
        command = self._FriendNotifier__handleButton
        optiondefs = (('dialogName', 'FriendInvitee',
                       None), ('text', text, None), ('style', style, None),
                      ('buttonText', buttonText, None), ('command', command,
                                                         None),
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
        self.initialiseoptions(FriendNotifier)
        self.show()

    def cleanup(self):
        print 'cleanup calling!'
        ToonHeadDialog.ToonHeadDialog.cleanup(self)

    def _FriendNotifier__handleButton(self, value):
        if value == DGG.DIALOG_OK:
            pass
        1
        self.context = None
        self.cleanup()

    def _FriendNotifier__handleOhWell(self, value):
        self.cleanup()

    def _FriendNotifier__handleCancelFromAbove(self, context=None):
        if context is None or context == self.context:
            self.context = None
            self.cleanup()
