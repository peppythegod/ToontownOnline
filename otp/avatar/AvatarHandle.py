
class AvatarHandle:
    dclassName = 'AvatarHandle'

    def getName(self):
        if __dev__:
            pass
        1
        return ''

    def isOnline(self):
        if __dev__:
            pass
        1
        return False

    def isUnderstandable(self):
        if __dev__:
            pass
        1
        return True

    def setTalkWhisper(self, fromAV, fromAC, avatarName, chat, mods, flags):
        (newText, scrubbed) = localAvatar.scrubTalk(chat, mods)
        base.talkAssistant.receiveWhisperTalk(
            fromAV,
            avatarName,
            fromAC,
            None,
            self.avatarId,
            self.getName(),
            newText,
            scrubbed)
