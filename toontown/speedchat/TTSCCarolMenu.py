from direct.showbase import PythonUtil
from otp.speedchat.SCMenu import SCMenu
from otp.speedchat.SCMenuHolder import SCMenuHolder
from otp.speedchat.SCStaticTextTerminal import SCStaticTextTerminal
from otp.otpbase.OTPLocalizer import SpeedChatStaticText
from toontown.speedchat.TTSCIndexedTerminal import TTSCIndexedTerminal
from otp.otpbase import OTPLocalizer
CarolMenu = [
    (OTPLocalizer.CarolMenuSections[0], {
        60200: 60220,
        60201: 60221,
        60202: 60222,
        60203: 60223,
        60204: 60224,
        60205: 60225})]


class TTSCCarolMenu(SCMenu):

    def __init__(self):
        SCMenu.__init__(self)
        self._TTSCCarolMenu__carolMessagesChanged()
        submenus = []

    def destroy(self):
        SCMenu.destroy(self)

    def clearMenu(self):
        SCMenu.clearMenu(self)

    def _TTSCCarolMenu__carolMessagesChanged(self):
        self.clearMenu()

        try:
            lt = base.localAvatar
        except BaseException:
            return None

        for section in CarolMenu:
            if section[0] == -1:
                for phrase in section[1].keys():
                    blatherTxt = section[1][phrase]
                    if blatherTxt not in OTPLocalizer.SpeedChatStaticText:
                        print 'warning: tried to link Carol phrase %s which does not seem to exist' % blatherTxt
                        break

                    self.append(
                        TTSCIndexedTerminal(
                            SpeedChatStaticText.get(
                                phrase, None), blatherTxt))

            menu = SCMenu()
            for phrase in section[1]:
                if phrase not in OTPLocalizer.SpeedChatStaticText:
                    print 'warning: tried to link Carol phrase %s which does not seem to exist' % phrase
                    break

                menu.append(SCStaticTextTerminal(phrase))

            menuName = str(section[0])
            self.append(SCMenuHolder(menuName, menu))
