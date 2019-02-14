from pandac.PandaModules import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase import DirectObject
from toontown.friends import FriendHandle
from otp.avatar import Avatar
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.friends import ToontownFriendSecret
import ToonAvatarDetailPanel
import AvatarPanelBase
import PlayerDetailPanel
from otp.otpbase import OTPGlobals
GAME_LOGO_NAMES = {
    'Default': 'GameLogo_Unknown',
    'Disney XD': 'GameLogo_XD',
    'Toontown': 'GameLogo_Toontown',
    'Pirates': 'GameLogo_Pirates'
}
GAME_LOGO_FILE = 'phase_3/models/misc/game_logo_card'


class PlayerInfoPanel(AvatarPanelBase.AvatarPanelBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('PlayerInfoPanel')

    def __init__(self, playerId):
        FriendsListPanel = FriendsListPanel
        import toontown.friends
        AvatarPanelBase.AvatarPanelBase.__init__(
            self, None, FriendsListPanel=FriendsListPanel)
        self.setup(playerId)
        self.avId = 0
        self.avName = None

    def setup(self, playerId):
        FriendsListPanel = FriendsListPanel
        import toontown.friends
        self.playerId = playerId
        self.playerInfo = base.cr.playerFriendsManager.playerId2Info.get(
            playerId)
        if not self.playerInfo:
            return None

        avId = None
        avatar = None
        if playerId:
            if self.playerInfo.onlineYesNo:
                avId = self.playerInfo.avatarId
                avatar = base.cr.playerFriendsManager.identifyFriend(avId)

        self.notify.debug('Opening player panel, %s' % self.playerInfo)
        self.avatar = avatar
        self.noAv = 0
        if not avatar:
            self.noAv = 1

        self.accountText = None
        self.listName = ' '
        world = self.playerInfo.location
        if self.playerInfo.onlineYesNo == 0:
            world = TTLocalizer.AvatarDetailPanelRealLife

        self.accountText = self.playerInfo.playerName
        if self.noAv:
            avButtonState = DGG.DISABLED
        else:
            avButtonState = DGG.NORMAL
        self.online = self.playerInfo.onlineYesNo
        if self.online:
            onlineButtonState = DGG.NORMAL
        else:
            onlineButtonState = DGG.DISABLED
        base.localAvatar.obscureFriendsListButton(1)
        gui = loader.loadModel('phase_3.5/models/gui/avatar_panel_gui')
        self.frame = DirectFrame(
            image=gui.find('**/avatar_panel'),
            relief=None,
            pos=(1.1000000000000001, 100, 0.52500000000000002))
        disabledImageColor = Vec4(1, 1, 1, 0.40000000000000002)
        text0Color = Vec4(1, 1, 1, 1)
        text1Color = Vec4(0.5, 1, 0.5, 1)
        text2Color = Vec4(1, 1, 0.5, 1)
        text3Color = Vec4(0.59999999999999998, 0.59999999999999998,
                          0.59999999999999998, 1)
        if self.playerInfo:
            logoImageName = GAME_LOGO_NAMES['Default']
            if not self.playerInfo.onlineYesNo:
                logoImageName = GAME_LOGO_NAMES['Default']
            elif GAME_LOGO_NAMES.has_key(self.playerInfo.location):
                logoImageName = GAME_LOGO_NAMES[self.playerInfo.location]

            model = loader.loadModel(GAME_LOGO_FILE)
            logoImage = model.find('**/' + logoImageName)
            del model
            self.outsideLogo = DirectLabel(
                parent=self.frame,
                relief=None,
                image=logoImage,
                pos=(0.012500000000000001, 0.0, 0.25),
                image_color=(1.0, 1.0, 1.0, 1),
                scale=(0.17499999999999999, 1, 0.17499999999999999))

        font = ToontownGlobals.getInterfaceFont()
        textScale = 0.047
        textWrap = 7.5
        textAlign = TextNode.ACenter
        textPos = (0, 0)
        self.nameLabel = DirectLabel(
            parent=self.frame,
            pos=(0.012500000000000001, 0, 0.38500000000000001),
            relief=None,
            text=self.listName,
            text_font=font,
            text_fg=Vec4(0, 0, 0, 1),
            text_pos=textPos,
            text_scale=textScale,
            text_wordwrap=textWrap,
            text_align=textAlign,
            text_shadow=(1, 1, 1, 1))
        if self.accountText:
            self.accountLabel = DirectLabel(
                parent=self.frame,
                pos=(0.012500000000000001, 0, 0.38500000000000001),
                text=self.accountText,
                relief=None,
                text_font=font,
                text_fg=Vec4(0, 0, 0, 1),
                text_pos=textPos,
                text_scale=textScale,
                text_wordwrap=textWrap,
                text_align=textAlign,
                text_shadow=(1, 1, 1, 1))
            self.accountLabel.show()

        self.closeButton = DirectButton(
            parent=self.frame,
            image=(gui.find('**/CloseBtn_UP'), gui.find('**/CloseBtn_DN'),
                   gui.find('**/CloseBtn_Rllvr'), gui.find('**/CloseBtn_UP')),
            relief=None,
            pos=(0.15764400000000001, 0, -0.37916699999999998),
            command=self._PlayerInfoPanel__handleClose)
        self.friendButton = DirectButton(
            parent=self.frame,
            image=(gui.find('**/Frnds_Btn_UP'), gui.find('**/Frnds_Btn_DN'),
                   gui.find('**/Frnds_Btn_RLVR'), gui.find('**/Frnds_Btn_UP')),
            image3_color=disabledImageColor,
            image_scale=0.90000000000000002,
            relief=None,
            text=TTLocalizer.AvatarPanelFriends,
            text_scale=0.059999999999999998,
            pos=(-0.10299999999999999, 0, 0.13300000000000001),
            text0_fg=text0Color,
            text1_fg=text1Color,
            text2_fg=text2Color,
            text3_fg=text3Color,
            text_pos=(0.059999999999999998, -0.02),
            text_align=TextNode.ALeft,
            state=avButtonState,
            command=self._PlayerInfoPanel__handleFriend)
        self.friendButton['state'] = DGG.DISABLED
        self.goToButton = DirectButton(
            parent=self.frame,
            image=(gui.find('**/Go2_Btn_UP'), gui.find('**/Go2_Btn_DN'),
                   gui.find('**/Go2_Btn_RLVR'), gui.find('**/Go2_Btn_UP')),
            image3_color=disabledImageColor,
            image_scale=0.90000000000000002,
            relief=None,
            pos=(-0.10299999999999999, 0, 0.044999999999999998),
            text=TTLocalizer.AvatarPanelGoTo,
            text0_fg=text0Color,
            text1_fg=text1Color,
            text2_fg=text2Color,
            text3_fg=text3Color,
            text_scale=0.059999999999999998,
            text_pos=(0.059999999999999998, -0.014999999999999999),
            text_align=TextNode.ALeft,
            state=avButtonState,
            command=self._PlayerInfoPanel__handleGoto)
        self.goToButton['state'] = DGG.DISABLED
        self.whisperButton = DirectButton(
            parent=self.frame,
            image=(gui.find('**/ChtBx_ChtBtn_UP'),
                   gui.find('**/ChtBx_ChtBtn_DN'),
                   gui.find('**/ChtBx_ChtBtn_RLVR'),
                   gui.find('**/ChtBx_ChtBtn_UP')),
            image3_color=disabledImageColor,
            relief=None,
            image_scale=0.90000000000000002,
            pos=(-0.10299999999999999, 0, -0.037499999999999999),
            text=TTLocalizer.AvatarPanelWhisper,
            text0_fg=text0Color,
            text1_fg=text1Color,
            text2_fg=text2Color,
            text3_fg=text3Color,
            text_scale=TTLocalizer.PIPwisperButton,
            text_pos=(0.059999999999999998, -0.012500000000000001),
            text_align=TextNode.ALeft,
            state=onlineButtonState,
            command=self._PlayerInfoPanel__handleWhisper)
        self.secretsButton = DirectButton(
            parent=self.frame,
            image=(gui.find('**/ChtBx_ChtBtn_UP'),
                   gui.find('**/ChtBx_ChtBtn_DN'),
                   gui.find('**/ChtBx_ChtBtn_RLVR'),
                   gui.find('**/ChtBx_ChtBtn_UP')),
            image3_color=disabledImageColor,
            image_scale=0.90000000000000002,
            relief=None,
            pos=(-0.10299999999999999, 0, -0.13),
            text=TTLocalizer.AvatarPanelSecrets,
            text0_fg=text0Color,
            text1_fg=text1Color,
            text2_fg=text2Color,
            text3_fg=text3Color,
            text_scale=TTLocalizer.PIPsecretsButton,
            text_pos=(0.055, -0.01),
            text_align=TextNode.ALeft,
            state=avButtonState,
            command=self._PlayerInfoPanel__handleSecrets)
        self.secretsButton['state'] = DGG.DISABLED
        if not base.localAvatar.isTeleportAllowed():
            self.goToButton['state'] = DGG.DISABLED

        (ignoreStr, ignoreCmd, ignoreSize) = self.getIgnoreButtonInfo()
        self.ignoreButton = DirectButton(
            parent=self.frame,
            image=(gui.find('**/Ignore_Btn_UP'), gui.find('**/Ignore_Btn_DN'),
                   gui.find('**/Ignore_Btn_RLVR'),
                   gui.find('**/Ignore_Btn_UP')),
            image3_color=disabledImageColor,
            image_scale=0.90000000000000002,
            relief=None,
            pos=(-0.103697, 0, -0.20999999999999999),
            text=ignoreStr,
            text0_fg=text0Color,
            text1_fg=text1Color,
            text2_fg=text2Color,
            text3_fg=text3Color,
            text_scale=ignoreSize,
            text_pos=(0.059999999999999998, -0.014999999999999999),
            text_align=TextNode.ALeft,
            state=avButtonState,
            command=ignoreCmd)
        if base.cr.productName not in ['JP', 'DE', 'BR', 'FR']:
            self.reportButton = DirectButton(
                parent=self.frame,
                image=(gui.find('**/report_BtnUP'),
                       gui.find('**/report_BtnDN'),
                       gui.find('**/report_BtnRLVR'),
                       gui.find('**/report_BtnUP')),
                image3_color=disabledImageColor,
                image_scale=0.65000000000000002,
                relief=None,
                pos=(-0.10299999999999999, 0, -0.29737999999999998),
                text=TTLocalizer.AvatarPanelReport,
                text0_fg=text0Color,
                text1_fg=text1Color,
                text2_fg=text2Color,
                text3_fg=text3Color,
                text_scale=0.059999999999999998,
                text_pos=(0.059999999999999998, -0.014999999999999999),
                text_align=TextNode.ALeft,
                command=self.handleReport)

        self.detailButton = DirectButton(
            parent=self.frame,
            image=(gui.find('**/ChtBx_BackBtn_UP'),
                   gui.find('**/ChtBx_BackBtn_DN'),
                   gui.find('**/ChtBx_BackBtn_Rllvr'),
                   gui.find('**/ChtBx_BackBtn_UP')),
            relief=None,
            text=('', TTLocalizer.PlayerPanelDetail,
                  TTLocalizer.PlayerPanelDetail, ''),
            text_fg=text2Color,
            text_shadow=(0, 0, 0, 1),
            text_scale=TTLocalizer.PIPdetailButton,
            text_pos=(0.085000000000000006, 0.055),
            text_align=TextNode.ACenter,
            pos=(-0.133773, 0, -0.38713199999999998),
            state=DGG.NORMAL,
            command=self._PlayerInfoPanel__handleDetails)
        gui.removeNode()
        menuX = -0.050000000000000003
        menuScale = 0.064000000000000001
        self.frame.show()
        messenger.send('avPanelDone')
        self.accept('playerOnline', self._PlayerInfoPanel__handlePlayerChanged)
        self.accept('playerOffline',
                    self._PlayerInfoPanel__handlePlayerChanged)
        self.accept(OTPGlobals.PlayerFriendUpdateEvent,
                    self._PlayerInfoPanel__handlePlayerChanged)
        self.accept(OTPGlobals.PlayerFriendRemoveEvent,
                    self._PlayerInfoPanel__handlePlayerUnfriend)

    def disableAll(self):
        self.detailButton['state'] = DGG.DISABLED
        self.ignoreButton['state'] = DGG.DISABLED
        if base.cr.productName not in ['JP', 'DE', 'BR', 'FR']:
            self.reportButton['state'] = DGG.DISABLED

        self.goToButton['state'] = DGG.DISABLED
        self.secretsButton['state'] = DGG.DISABLED
        self.whisperButton['state'] = DGG.DISABLED
        self.friendButton['state'] = DGG.DISABLED
        self.closeButton['state'] = DGG.DISABLED

    def cleanup(self):
        self.unsetup()
        self.ignore('playerOnline')
        self.ignore('playerOffline')
        self.ignore(OTPGlobals.PlayerFriendUpdateEvent)
        self.ignore(OTPGlobals.PlayerFriendRemoveEvent)
        AvatarPanelBase.AvatarPanelBase.cleanup(self)

    def unsetup(self):
        if not hasattr(self, 'frame') or self.frame == None:
            return None

        PlayerDetailPanel.unloadPlayerDetail()
        self.frame.destroy()
        del self.frame
        self.frame = None
        base.localAvatar.obscureFriendsListButton(-1)
        self.laffMeter = None
        self.ignore('updateLaffMeter')
        if hasattr(self.avatar, 'bFake') and self.avatar.bFake:
            self.avatar.delete()

    def _PlayerInfoPanel__handleGoto(self):
        if base.localAvatar.isTeleportAllowed():
            base.localAvatar.chatMgr.noWhisper()
            messenger.send('gotoAvatar',
                           [self.avId, self.avName, self.avDisableName])

    def _PlayerInfoPanel__handleWhisper(self):
        if self.noAv:
            base.localAvatar.chatMgr.whisperTo(self.listName, 0, self.playerId)
        else:
            base.localAvatar.chatMgr.whisperTo(self.avName, self.avId,
                                               self.playerId)

    def _PlayerInfoPanel__handleSecrets(self):
        base.localAvatar.chatMgr.noWhisper()
        ToontownFriendSecret.showFriendSecret(ToontownFriendSecret.BothSecrets)

    def _PlayerInfoPanel__handleFriend(self):
        base.localAvatar.chatMgr.noWhisper()
        self._PlayerInfoPanel__getAvInfo()
        messenger.send('friendAvatar',
                       [self.avId, self.avName, self.avDisableName])

    def _PlayerInfoPanel__getAvInfo(self):
        if self.playerId:
            self.avId = self.playerInfo.avatarId
            if self.avId:
                avatar = base.cr.playerFriendsManager.identifyFriend(self.avId)
                if avatar:
                    self.avName = avatar.getName()
                    if not self.avDisableName:
                        self.avDisableName = avatar.uniqueName('disable')

    def _PlayerInfoPanel__handleDetails(self):
        base.localAvatar.chatMgr.noWhisper()
        self._PlayerInfoPanel__getAvInfo()
        messenger.send('playerDetails',
                       [self.avId, self.avName, self.playerId])

    def handleDisableAvatar(self):
        pass

    def _PlayerInfoPanel__handlePlayerChanged(self, playerId, info=None):
        if playerId == self.playerId:
            self.unsetup()
            self.setup(playerId)

    def _PlayerInfoPanel__handlePlayerUnfriend(self, playerId):
        if playerId == self.playerId:
            self._PlayerInfoPanel__handleClose()

    def _PlayerInfoPanel__handleClose(self):
        self.cleanup()
        AvatarPanelBase.currentAvatarPanel = None
        if self.friendsListShown:
            self.FriendsListPanel.showFriendsList()

    def getAvId(self):
        if hasattr(self, 'avatar'):
            if self.avatar:
                return self.avatar.doId

    def getPlayerId(self):
        if hasattr(self, 'playerId'):
            return self.playerId

    def isHidden(self):
        if not hasattr(self, 'frame') or not (self.frame):
            return 1

        return self.frame.isHidden()

    def getType(self):
        return 'player'
