from SCMenu import SCMenu
from SCCustomTerminal import SCCustomTerminal
from otp.otpbase.OTPLocalizer import CustomSCStrings


class SCCustomMenu(SCMenu):
    def __init__(self):
        SCMenu.__init__(self)
        self.accept('customMessagesChanged',
                    self._SCCustomMenu__customMessagesChanged)
        self._SCCustomMenu__customMessagesChanged()

    def destroy(self):
        SCMenu.destroy(self)

    def _SCCustomMenu__customMessagesChanged(self):
        self.clearMenu()

        try:
            lt = base.localAvatar
        except BaseException:
            return None

        for msgIndex in lt.customMessages:
            if msgIndex in CustomSCStrings:
                self.append(SCCustomTerminal(msgIndex))
                continue
