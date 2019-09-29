from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class NewMagicWordManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'MagicWordMgrAI')

    def setMagicWord(self, word, targetId):
        casterId = self.air.getAvatarIdFromSender()
        if not casterId:
            self.notify.warning("setMagicWord(): no caster id")
            return
            
        self.__handleMagicWord(word, casterId, targetId)
        
    def __handleMagicWord(self, word, casterId, targetId):
        command, args = self.parseMagicData(word)
        
        
    def parseMagicData(self, word):
        if word[0] != '~':
            self.notify.warning("Failed parsing magic word '%s' - no valid start" %word)
            return
        
        data = word[1:].split(' ')
        command = data.pop(0)
        return (command, data)