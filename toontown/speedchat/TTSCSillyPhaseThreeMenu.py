from direct.showbase import PythonUtil
from otp.speedchat.SCMenu import SCMenu
from otp.speedchat.SCMenuHolder import SCMenuHolder
from otp.speedchat.SCStaticTextTerminal import SCStaticTextTerminal
from otp.otpbase import OTPLocalizer
SillyPhaseThreeMenu = [(OTPLocalizer.SillyHolidayMenuSections[1],
                        [30323, 30324, 30325, 30326, 30327]),
                       (OTPLocalizer.SillyHolidayMenuSections[2],
                        [30318, 30319, 30320, 30321, 30322])]


class TTSCSillyPhaseThreeMenu(SCMenu):
    def __init__(self):
        SCMenu.__init__(self)
        self._TTSCSillyPhaseThreeMenu__SillyPhaseThreeMessagesChanged()
        submenus = []

    def destroy(self):
        SCMenu.destroy(self)

    def clearMenu(self):
        SCMenu.clearMenu(self)

    def _TTSCSillyPhaseThreeMenu__SillyPhaseThreeMessagesChanged(self):
        self.clearMenu()

        try:
            lt = base.localAvatar
        except BaseException:
            return None

        for section in SillyPhaseThreeMenu:
            if section[0] == -1:
                for phrase in section[1]:
                    if phrase not in OTPLocalizer.SpeedChatStaticText:
                        print 'warning: tried to link Silly PhaseThree phrase %s which does not seem to exist' % phrase
                        break

                    self.append(SCStaticTextTerminal(phrase))

            menu = SCMenu()
            for phrase in section[1]:
                if phrase not in OTPLocalizer.SpeedChatStaticText:
                    print 'warning: tried to link Silly PhaseThree phrase %s which does not seem to exist' % phrase
                    break

                menu.append(SCStaticTextTerminal(phrase))

            menuName = str(section[0])
            self.append(SCMenuHolder(menuName, menu))
