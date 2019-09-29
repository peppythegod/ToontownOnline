from direct.distributed.DistributedObject import DistributedObject
from direct.directnotify import DirectNotifyGlobal

class NewMagicWordManager(DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'MagicWordMgr')

    def generate(self):
        DistributedObject.generate(self)
        self.accept('magicWord', self.__handleMagicWord)
        
    def __handleMagicWord(self, word):
        target = base.cr.currentAvSelection
        if target == None:
            target == base.localAvatar.doId
        
        self.d_setMagicWord(word, target)
        
    def d_setMagicWord(self, word, targetId):
        self.sendUpdate('setMagicWord', [word, targetId])
        
    def delete(self):
        DistributedObject.delete(self)
        self.ignore('magicWord')