from otp.avatar import DistributedAvatar
import Char


class DistributedChar(DistributedAvatar.DistributedAvatar, Char.Char):
    def __init__(self, cr):
        self.DistributedChar_initialized = 1
        DistributedAvatar.DistributedAvatar.__init__(self, cr)
        Char.Char.__init__(self)

    def delete(self):
        self.DistributedChar_deleted = 1
        Char.Char.delete(self)
        DistributedAvatar.DistributedAvatar.delete(self)

    def setDNAString(self, dnaString):
        Char.Char.setDNAString(self, dnaString)

    def setDNA(self, dna):
        Char.Char.setDNA(self, dna)

    def playDialogue(self, *args):
        Char.Char.playDialogue(self, *args)

    def setHp(self, hp):
        self.hp = hp
