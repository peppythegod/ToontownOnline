from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
import HolidayDecorator
from toontown.toonbase import ToontownGlobals
from pandac.PandaModules import Vec4, CSDefault, TransformState, NodePath, TransparencyAttrib
from toontown.hood import GSHood
#! add dna


class CrashedLeaderBoardDecorator(HolidayDecorator.HolidayDecorator):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'CrashedLeaderBoardDecorator')

    def __init__(self):
        HolidayDecorator.HolidayDecorator.__init__(self)

    def decorate(self):
        self.updateHoodDNAStore()
        self.swapIval = self.getSwapVisibleIval()
        if self.swapIval:
            self.swapIval.start()

        holidayIds = base.cr.newsManager.getDecorationHolidayId()
        if ToontownGlobals.CRASHED_LEADERBOARD not in holidayIds:
            return None

        if base.config.GetBool('want-crashedLeaderBoard-Smoke', 1):
            self.startSmokeEffect()

    def startSmokeEffect(self):
        if isinstance(base.cr.playGame.getPlace().loader.hood, GSHood.GSHood):
            base.cr.playGame.getPlace().loader.startSmokeEffect()

    def stopSmokeEffect(self):
        if isinstance(base.cr.playGame.getPlace().loader.hood, GSHood.GSHood):
            base.cr.playGame.getPlace().loader.stopSmokeEffect()

    def undecorate(self):
        if base.config.GetBool('want-crashedLeaderBoard-Smoke', 1):
            self.stopSmokeEffect()

        holidayIds = base.cr.newsManager.getDecorationHolidayId()
        if len(holidayIds) > 0:
            self.decorate()
            return None

        storageFile = base.cr.playGame.hood.storageDNAFile
        if storageFile:
            loadDNAFile(self.dnaStore, storageFile, CSDefault)

        self.swapIval = self.getSwapVisibleIval()
        if self.swapIval:
            self.swapIval.start()
