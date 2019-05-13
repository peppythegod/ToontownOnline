from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from toontown.chat.TTWhiteList import TTWhiteList


class DistributedChatManagerUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        "DistributedChatManagerUD")
    WantWhitelist = config.GetBool('want-whitelist', 1)
        
    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
        self.whitelist = TTWhiteList()

    def chatString(self, message):
        sender = self.air.getAvatarIdFromSender()
        if sender == 0:
            self.notify.warning("chatString(): no sender")
            return

        modifications = []
        words = message.split(' ')
        if self.WantWhitelist:
            offset = 0
            for word in words:
                if word and not self.whitelist.isWord(word):
                    modifications.append((offset, offset + len(word) - 1))
                offset += len(word) + 1

        cleanMessage = message
        for modStart, modStop in modifications:
            cleanMessage = cleanMessage[:modStart] + '*'*(modStop-modStart+1) + cleanMessage[modStop+1:]

        dclass = self.air.dclassesByName['DistributedAvatarUD']
        dg = dclass.aiFormatUpdate(
            'setTalk', sender, sender, self.air.ourChannel,
            [0, 0, '', cleanMessage, modifications, 0])
        self.air.send(dg)

    def online(self):
        pass

    def adminChat(self, todo0, todo1):
        pass

    def setAvatarLocation(self, todo0, todo1, todo2):
        pass

    def setAvatarCrew(self, todo0, todo1):
        pass

    def setAvatarGuild(self, todo0, todo1):
        pass

    def chatParentId(self, todo0):
        pass

    def chatZoneId(self, todo0):
        pass

    def chatFace(self, todo0):
        pass

    def chatEmote(self, todo0):
        pass

    def chatEmoteTarget(self, todo0):
        pass

    def chatIndex(self, todo0):
        pass

    def speedChatTo(self, todo0):
        pass

    def speedChatFrom(self, todo0, todo1):
        pass

    def speedChatCustomTo(self, todo0):
        pass

    def speedChatCustomFrom(self, todo0, todo1):
        pass

    def whisperSCTo(self, todo0, todo1):
        pass

    def whisperSCFrom(self, todo0, todo1):
        pass

    def whisperSCCustomTo(self, todo0, todo1):
        pass

    def whisperSCCustomFrom(self, todo0, todo1):
        pass

    def whisperSCEmoteTo(self, todo0, todo1):
        pass

    def whisperSCEmoteFrom(self, todo0, todo1):
        pass

    def whisperIgnored(self, todo0):
        pass
