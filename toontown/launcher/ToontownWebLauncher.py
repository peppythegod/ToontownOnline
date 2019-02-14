import os
from otp.launcher.WebLauncherBase import WebLauncherBase
from toontown.toonbase import TTLocalizer
from pandac.PandaModules import *


class ToontownWebLauncher(WebLauncherBase):
    GameName = 'Toontown'
    LauncherPhases = [(3, 'tt_3'), (3.5, 'tt_3_5'), (4, 'tt_4'), (5, 'tt_5'),
                      (5.5, 'tt_5_5'), (6, 'tt_6'), (7, 'tt_7'), (8, 'tt_8'),
                      (9, 'tt_9'), (10, 'tt_10'), (11, 'tt_11'), (12, 'tt_12'),
                      (13, 'tt_13')]
    Localizer = TTLocalizer

    def __init__(self, appRunner):
        WebLauncherBase.__init__(self, appRunner)
        self.http = HTTPClient.getGlobalPtr()
        self.webAcctParams = 'WEB_ACCT_PARAMS'
        self.parseWebAcctParams()
        self.startDownload()
        self.toontownBlueKey = 'TOONTOWN_BLUE'
        self.toontownPlayTokenKey = 'TOONTOWN_PLAYTOKEN'
        self.launcherMessageKey = 'LAUNCHER_MESSAGE'
        self.game1DoneKey = 'GAME1_DONE'
        self.game2DoneKey = 'GAME2_DONE'
        self.tutorialCompleteKey = 'TUTORIAL_DONE'
        ToontownStart = ToontownStart
        import toontown.toonbase

    def getAccountServer(self):
        return self.getValue('ACCOUNT_SERVER', '')

    def getNeedPwForSecretKey(self):
        return self.secretNeedsParentPasswordKey

    def getParentPasswordSet(self):
        return self.chatEligibleKey

    def setTutorialComplete(self):
        pass

    def getTutorialComplete(self):
        return False

    def getGame2Done(self):
        return True

    def parseWebAcctParams(self):
        s = ConfigVariableString('fake-web-acct-params', '').getValue()
        if not s:
            s = self.getValue(self.webAcctParams, '')

        l = s.split('&')
        length = len(l)
        dict = {}
        for index in range(0, len(l)):
            args = l[index].split('=')
            if len(args) == 3:
                (name, value) = args[-2:]
                dict[name] = int(value)
                continue
            if len(args) == 2:
                (name, value) = args
                dict[name] = int(value)
                continue

        self.secretNeedsParentPasswordKey = 1
        if 'secretsNeedsParentPassword' in dict:
            self.secretNeedsParentPasswordKey = dict[
                'secretsNeedsParentPassword']
        else:
            self.notify.warning(
                'no secretNeedsParentPassword token in webAcctParams')
        self.notify.info('secretNeedsParentPassword = %d' %
                         self.secretNeedsParentPasswordKey)
        self.chatEligibleKey = 0
        if 'chatEligible' in dict:
            self.chatEligibleKey = dict['chatEligible']
        else:
            self.notify.warning('no chatEligible token in webAcctParams')
        self.notify.info('chatEligibleKey = %d' % self.chatEligibleKey)

    def getBlue(self):
        blue = self.getValue(self.toontownBlueKey)
        self.setValue(self.toontownBlueKey, '')
        if blue == 'NO BLUE':
            blue = None

        return blue

    def getPlayToken(self):
        playToken = self.getValue(self.toontownPlayTokenKey)
        self.setValue(self.toontownPlayTokenKey, '')
        if playToken == 'NO PLAYTOKEN':
            playToken = None

        return playToken
