from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.directnotify import DirectNotifyGlobal
import DistributedToon
from toontown.friends import FriendInviter
import ToonTeleportPanel
from toontown.toonbase import TTLocalizer
from toontown.hood import ZoneUtil
from toontown.toonbase.ToontownBattleGlobals import Tracks, Levels
globalAvatarDetail = None

def showPlayerDetail(avId, avName, playerId = None):
    global globalAvatarDetail
    if globalAvatarDetail != None:
        globalAvatarDetail.cleanup()
        globalAvatarDetail = None
    
    globalAvatarDetail = PlayerDetailPanel(avId, avName, playerId)


def hidePlayerDetail():
    global globalAvatarDetail
    if globalAvatarDetail != None:
        globalAvatarDetail.cleanup()
        globalAvatarDetail = None
    


def unloadPlayerDetail():
    global globalAvatarDetail
    if globalAvatarDetail != None:
        globalAvatarDetail.cleanup()
        globalAvatarDetail = None
    


class PlayerDetailPanel(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('ToonAvatarDetailPanel')
    
    def __init__(self, avId, avName, playerId = None, parent = aspect2dp, **kw):
        self.playerId = playerId
        self.isPlayer = 0
        self.playerInfo = None
        if playerId:
            self.isPlayer = 1
            if base.cr.playerFriendsManager.playerId2Info.has_key(playerId):
                self.playerInfo = base.cr.playerFriendsManager.playerId2Info[playerId]
                if not self.playerInfo.onlineYesNo:
                    avId = None
                
            else:
                avId = None
        
        self.avId = avId
        self.avName = avName
        self.avatar = None
        self.createdAvatar = None
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        gui = loader.loadModel('phase_3.5/models/gui/avatar_panel_gui')
        detailPanel = gui.find('**/avatarInfoPanel')
        textScale = 0.13200000000000001
        textWrap = 10.4
        if self.playerId:
            textScale = 0.10000000000000001
            textWrap = 18.0
        
        optiondefs = (('pos', (0.52500000000000002, 0.0, 0.52500000000000002), None), ('scale', 0.5, None), ('relief', None, None), ('image', detailPanel, None), ('image_color', GlobalDialogColor, None), ('text', '', None), ('text_wordwrap', textWrap, None), ('text_scale', textScale, None), ('text_pos', (-0.125, 0.75), None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        self.dataText = DirectLabel(self, text = '', text_scale = 0.085000000000000006, text_align = TextNode.ALeft, text_wordwrap = 15, relief = None, pos = (-0.84999999999999998, 0.0, 0.72499999999999998))
        if self.avId:
            self.avText = DirectLabel(self, text = TTLocalizer.PlayerToonName % {
                'toonname': self.avName }, text_scale = 0.089999999999999997, text_align = TextNode.ALeft, text_wordwrap = 15, relief = None, pos = (-0.84999999999999998, 0.0, 0.56000000000000005))
            guiButton = loader.loadModel('phase_3/models/gui/quit_button')
            self.gotoToonButton = DirectButton(parent = self, relief = None, image = (guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale = 1.1499999999999999, text = TTLocalizer.PlayerShowToon, text_scale = 0.080000000000000002, text_pos = (0.0, -0.02), textMayChange = 0, pos = (0.42999999999999999, 0, 0.41499999999999998), command = self._PlayerDetailPanel__showToon)
        
        ToonTeleportPanel.hideTeleportPanel()
        FriendInviter.hideFriendInviter()
        self.bCancel = DirectButton(self, image = (buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr')), relief = None, text = TTLocalizer.AvatarDetailPanelCancel, text_scale = 0.050000000000000003, text_pos = (0.12, -0.01), pos = (-0.86499999999999999, 0.0, -0.76500000000000001), scale = 2.0, command = self._PlayerDetailPanel__handleCancel)
        self.bCancel.show()
        self.initialiseoptions(PlayerDetailPanel)
        self._PlayerDetailPanel__showData()
        buttons.removeNode()
        gui.removeNode()

    
    def cleanup(self):
        if self.createdAvatar:
            self.avatar.delete()
            self.createdAvatar = None
        
        self.destroy()

    
    def _PlayerDetailPanel__handleCancel(self):
        unloadPlayerDetail()

    
    def _PlayerDetailPanel__showData(self):
        if self.isPlayer and self.playerInfo:
            if self.playerInfo.onlineYesNo:
                someworld = self.playerInfo.location
            else:
                someworld = TTLocalizer.OfflineLocation
            text = TTLocalizer.AvatarDetailPanelPlayer % {
                'player': self.playerInfo.playerName,
                'world': someworld }
        else:
            text = TTLocalizer.AvatarDetailPanelOffline
        self.dataText['text'] = text

    
    def _PlayerDetailPanel__showToon(self):
        messenger.send('wakeup')
        hasManager = hasattr(base.cr, 'playerFriendsManager')
        handle = base.cr.identifyFriend(self.avId)
        if not handle and hasManager:
            handle = base.cr.playerFriendsManager.getAvHandleFromId(self.avId)
        
        if handle != None:
            self.notify.info("Clicked on name in friend's list. doId = %s" % handle.doId)
            messenger.send('clickedNametagPlayer', [
                handle,
                self.playerId,
                0])
        


