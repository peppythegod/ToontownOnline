from direct.distributed.PyDatagram import *
from pandac.PandaModules import *
from toontown.ai.MessageTypes import *
from otp.distributed.OtpDoGlobals import *
from toontown.distributed.ToontownInternalRepository import ToontownInternalRepository
from toontown.toonbase import ToontownGlobals

from otp.distributed.DistributedDirectoryAI import DistributedDirectoryAI
from otp.uberdog import DistributedChatManagerUD
from otp.friends import AvatarFriendsManagerUD
from toontown.friends import TTPlayerFriendsManagerUD
from toontown.uberdog import TTSpeedchatRelayUD
from toontown.uberdog import DistributedDeliveryManagerUD
from toontown.coderedemption import TTCodeRedemptionMgrUD


class ToontownUDRepository(ToontownInternalRepository):

    def __init__(self, baseChannel, stateServerChannel):
        ToontownInternalRepository.__init__(
            self, baseChannel, stateServerChannel, dcSuffix='UD')

        self.notify.setInfo(True)
        
    def createGlobals(self):
        self.chatManager = DistributedChatManagerUD.DistributedChatManagerUD(self)
        self.chatManager.generateWithRequiredAndId(OTP_DO_ID_CHAT_MANAGER, 0, 0)
        self.avatarFriendsManager = AvatarFriendsManagerUD.AvatarFriendsManagerUD(self) # TODO
        self.avatarFriendsManager.generateWithRequiredAndId(OTP_DO_ID_AVATAR_FRIENDS_MANAGER, 0, 0)
        self.playerFriendsManager = TTPlayerFriendsManagerUD.TTPlayerFriendsManagerUD(self) # TODO
        self.playerFriendsManager.generateWithRequiredAndId(OTP_DO_ID_PLAYER_FRIENDS_MANAGER, 0, 0)
        self.speedchatRelay = TTSpeedchatRelayUD.TTSpeedchatRelayUD(self) # TODO
        self.speedchatRelay.generateWithRequiredAndId(OTP_DO_ID_TOONTOWN_SPEEDCHAT_RELAY, 0, 0)
        self.deliveryManager = DistributedDeliveryManagerUD.DistributedDeliveryManagerUD(self) # TODO
        self.deliveryManager.generateWithRequiredAndId(OTP_DO_ID_TOONTOWN_DELIVERY_MANAGER, 0, 0)
        self.codeRedemptionManager = TTCodeRedemptionMgrUD.TTCodeRedemptionMgrUD(self) #TODO
        self.codeRedemptionManager.generateWithRequiredAndId(OTP_DO_ID_TOONTOWN_CODE_REDEMPTION_MANAGER, 0, 0)

    def handleConnected(self):
        rootObj = DistributedDirectoryAI(self)
        rootObj.generateWithRequiredAndId(self.getGameDoId(), 0, 0)         

        self.notify.info('Creating globals...')
        self.createGlobals()

        self.notify.info('Done.')