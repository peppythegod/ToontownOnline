from pandac.PandaModules import *
import ShtikerPage
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.quest import Quests
from toontown.toon import NPCToons
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.quest import QuestBookPoster
from direct.directnotify import DirectNotifyGlobal


class QuestPage(ShtikerPage.ShtikerPage):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestPage')

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.quests = {
            0: None,
            1: None,
            2: None,
            3: None}
        self.textRolloverColor = Vec4(1, 1, 0, 1)
        self.textDownColor = Vec4(0.5, 0.90000000000000002, 1, 1)
        self.textDisabledColor = Vec4(
            0.40000000000000002,
            0.80000000000000004,
            0.40000000000000002,
            1)
        self.onscreen = 0
        self.lastQuestTime = globalClock.getRealTime()

    def load(self):
        self.title = DirectLabel(
            parent=self,
            relief=None,
            text=TTLocalizer.QuestPageToonTasks,
            text_scale=0.12,
            textMayChange=0,
            pos=(
                0,
                0,
                0.59999999999999998))
        questFramePlaceList = ((-0.45000000000000001, 0, 0.25, 0, 0, 0), (-0.45000000000000001, 0, -0.34999999999999998,
                                                                          0, 0, 0), (0.45000000000000001, 0, 0.25, 0, 0, 0), (0.45000000000000001, 0, -0.34999999999999998, 0, 0, 0))
        self.questFrames = []
        for i in range(ToontownGlobals.MaxQuestCarryLimit):
            frame = QuestBookPoster.QuestBookPoster(
                reverse=i > 1, mapIndex=i + 1)
            frame.reparentTo(self)
            frame.setPosHpr(*questFramePlaceList[i])
            frame.setScale(1.0600000000000001)
            self.questFrames.append(frame)

        self.accept('questsChanged', self.updatePage)

    def acceptOnscreenHooks(self):
        self.accept(ToontownGlobals.QuestsHotkeyOn, self.showQuestsOnscreen)
        self.accept(ToontownGlobals.QuestsHotkeyOff, self.hideQuestsOnscreen)

    def ignoreOnscreenHooks(self):
        self.ignore(ToontownGlobals.QuestsHotkeyOn)
        self.ignore(ToontownGlobals.QuestsHotkeyOff)

    def unload(self):
        self.ignore('questsChanged')
        del self.title
        del self.quests
        del self.questFrames
        loader.unloadModel('phase_3.5/models/gui/stickerbook_gui')
        ShtikerPage.ShtikerPage.unload(self)

    def clearQuestFrame(self, index):
        self.questFrames[index].clear()
        self.quests[index] = None

    def fillQuestFrame(self, questDesc, index):
        self.questFrames[index].update(questDesc)
        self.quests[index] = questDesc

    def getLowestUnusedIndex(self):
        for i in range(ToontownGlobals.MaxQuestCarryLimit):
            if self.quests[i] is None:
                return i
                continue

        return -1

    def updatePage(self):
        self.notify.debug('updatePage()')
        newQuests = base.localAvatar.quests
        carryLimit = base.localAvatar.getQuestCarryLimit()
        for i in range(ToontownGlobals.MaxQuestCarryLimit):
            if i < carryLimit:
                self.questFrames[i].show()
                continue
            self.questFrames[i].hide()

        for (index, questDesc) in self.quests.items():
            if questDesc is not None and list(questDesc) not in newQuests:
                self.clearQuestFrame(index)
                continue

        for questDesc in newQuests:
            newQuestDesc = tuple(questDesc)
            if newQuestDesc not in self.quests.values():
                index = self.getLowestUnusedIndex()
                self.fillQuestFrame(newQuestDesc, index)
                continue

        for (i, questDesc) in self.quests.iteritems():
            if questDesc:
                if self.canDeleteQuest(questDesc):
                    self.questFrames[i].setDeleteCallback(
                        self._QuestPage__deleteQuest)
                else:
                    self.questFrames[i].setDeleteCallback(None)
                self.questFrames[i].update(questDesc)
                continue
            self.questFrames[i].unbindMouseEnter()

        messenger.send('questPageUpdated')

    def enter(self):
        self.updatePage()
        ShtikerPage.ShtikerPage.enter(self)

    def exit(self):
        ShtikerPage.ShtikerPage.exit(self)

    def showQuestsOnscreenTutorial(self):
        self.setPos(0, 0, -0.20000000000000001)
        self.showQuestsOnscreen()

    def showQuestsOnscreen(self):
        messenger.send('wakeup')
        timedif = globalClock.getRealTime() - self.lastQuestTime
        if timedif < 0.69999999999999996:
            return None

        self.lastQuestTime = globalClock.getRealTime()
        if self.onscreen or base.localAvatar.invPage.onscreen:
            return None

        self.onscreen = 1
        for i in range(ToontownGlobals.MaxQuestCarryLimit):
            if hasattr(self.questFrames[i], 'mapIndex'):
                self.questFrames[i].mapIndex.show()
                continue

        self.updatePage()
        self.reparentTo(aspect2d)
        self.title.hide()
        self.show()

    def hideQuestsOnscreenTutorial(self):
        self.setPos(0, 0, 0)
        self.hideQuestsOnscreen()

    def hideQuestsOnscreen(self):
        if not self.onscreen:
            return None

        self.onscreen = 0
        for i in range(ToontownGlobals.MaxQuestCarryLimit):
            if hasattr(self.questFrames[i], 'mapIndex'):
                self.questFrames[i].mapIndex.hide()
                continue

        self.reparentTo(self.book)
        self.title.show()
        self.hide()

    def canDeleteQuest(self, questDesc):
        if Quests.isQuestJustForFun(questDesc[0], questDesc[3]):
            pass
        return self.onscreen == 0

    def _QuestPage__deleteQuest(self, questDesc):
        base.localAvatar.d_requestDeleteQuest(questDesc)
