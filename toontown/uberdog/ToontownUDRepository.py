from direct.distributed.PyDatagram import *
from pandac.PandaModules import *
from toontown.ai.MessageTypes import *
from otp.distributed.OtpDoGlobals import *
from toontown.distributed.ToontownInternalRepository import ToontownInternalRepository
from toontown.toonbase import ToontownGlobals

from otp.distributed.DistributedDirectoryAI import DistributedDirectoryAI
from otp.uberdog import DistributedChatManagerUD


class ToontownUDRepository(ToontownInternalRepository):

    def __init__(self, baseChannel, stateServerChannel):
        ToontownInternalRepository.__init__(
            self, baseChannel, stateServerChannel, dcSuffix='UD')

        self.notify.setInfo(True)
        
    def createGlobals(self):
        self.chatManager = DistributedChatManagerUD.DistributedChatManagerUD(self)
        self.chatManager.generateWithRequiredAndId(OTP_DO_ID_CHAT_MANAGER, 0, 0)

    def handleConnected(self):
        rootObj = DistributedDirectoryAI(self)
        rootObj.generateWithRequiredAndId(self.getGameDoId(), 0, 0)         

        self.notify.info('Creating globals...')
        self.createGlobals()

        self.notify.info('Done.')