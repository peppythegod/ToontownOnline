from otp.friends.FriendSecret import unloadFriendSecret
from otp.friends.FriendSecret import hideFriendSecret
from otp.friends.FriendSecret import showFriendSecret
import otp.friends.FriendSecret
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from toontown.toonbase import TTLocalizer
from otp.friends.FriendSecret import AccountSecret
from otp.friends.FriendSecret import AvatarSecret
from otp.friends.FriendSecret import BothSecrets
from otp.friends import FriendSecret
globalFriendSecret = globalFriendSecret


def openFriendSecret(secretType):
    global globalFriendSecret
    if globalFriendSecret is not None:
        globalFriendSecret.unload()

    globalFriendSecret = ToontownFriendSecret(secretType)
    globalFriendSecret.enter()


FriendSecret.openFriendSecret = openFriendSecret


class ToontownFriendSecret(FriendSecret.FriendSecret):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'ToontownFriendSecret')

    def __init__(self, secretType):
        FriendSecret.FriendSecret.__init__(self, secretType)
        self.initialiseoptions(ToontownFriendSecret)

    def makeFriendTypeButtons(self):
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        self.avatarButton = DirectButton(
            parent=self,
            image=(buttons.find('**/ChtBx_OKBtn_UP'),
                   buttons.find('**/ChtBx_OKBtn_DN'),
                   buttons.find('**/ChtBx_OKBtn_Rllvr')),
            relief=None,
            text=TTLocalizer.FriendInviterToon,
            text_scale=0.070000000000000007,
            text_pos=(0.0, -0.10000000000000001),
            pos=(-0.34999999999999998, 0.0, -0.050000000000000003),
            command=self._FriendSecret__handleAvatar)
        avatarText = DirectLabel(
            parent=self,
            relief=None,
            pos=Vec3(0.34999999999999998, 0, -0.29999999999999999),
            text=TTLocalizer.FriendInviterToonFriendInfo,
            text_fg=(0, 0, 0, 1),
            text_pos=(0, 0),
            text_scale=0.055,
            text_align=TextNode.ACenter)
        avatarText.reparentTo(self.avatarButton.stateNodePath[2])
        self.avatarButton.hide()
        self.accountButton = DirectButton(
            parent=self,
            image=(buttons.find('**/ChtBx_OKBtn_UP'),
                   buttons.find('**/ChtBx_OKBtn_DN'),
                   buttons.find('**/ChtBx_OKBtn_Rllvr')),
            relief=None,
            text=TTLocalizer.FriendInviterPlayer,
            text_scale=0.070000000000000007,
            text_pos=(0.0, -0.10000000000000001),
            pos=(0.34999999999999998, 0.0, -0.050000000000000003),
            command=self._FriendSecret__handleAccount)
        accountText = DirectLabel(
            parent=self,
            relief=None,
            pos=Vec3(-0.34999999999999998, 0, -0.29999999999999999),
            text=TTLocalizer.FriendInviterPlayerFriendInfo,
            text_fg=(0, 0, 0, 1),
            text_pos=(0, 0),
            text_scale=0.055,
            text_align=TextNode.ACenter)
        accountText.reparentTo(self.accountButton.stateNodePath[2])
        self.accountButton.hide()
        buttons.removeNode()

    def _ToontownFriendSecret__determineSecret(self):
        if self.secretType == BothSecrets:
            self._FriendSecret__cleanupFirstPage()
            self.ok1.hide()
            self.changeOptions.hide()
            self.nextText['text'] = TTLocalizer.FriendInviterBegin
            self.nextText.setPos(0, 0, 0.29999999999999999)
            self.nextText.show()
            self.avatarButton.show()
            self.accountButton.show()
            self.cancel.show()
        else:
            self._FriendSecret__getSecret()
