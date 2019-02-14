from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase import PythonUtil
from direct.task import Task
from toontown.fishing.FishPhoto import DirectRegion
from toontown.shtiker.ShtikerPage import ShtikerPage
from toontown.toonbase import ToontownGlobals, TTLocalizer
from FishPage import FishingTrophy
from toontown.golf import GolfGlobals
if __debug__:
    import pdb

PageMode = PythonUtil.Enum('Records, Trophy')


class GolfPage(ShtikerPage):
    notify = DirectNotifyGlobal.directNotify.newCategory('GolfPage')

    def __init__(self):
        ShtikerPage.__init__(self)
        self.avatar = None
        self.mode = PageMode.Trophy

    def enter(self):
        if not hasattr(self, 'title'):
            self.load()

        self.setMode(self.mode, 1)
        ShtikerPage.enter(self)

    def exit(self):
        self.golfTrophies.hide()
        self.golfRecords.hide()
        ShtikerPage.exit(self)

    def setAvatar(self, av):
        self.avatar = av

    def getAvatar(self):
        return self.avatar

    def load(self):
        ShtikerPage.load(self)
        self.golfRecords = GolfingRecordsUI(self.avatar, self)
        self.golfRecords.hide()
        self.golfRecords.load()
        self.golfTrophies = GolfTrophiesUI(self.avatar, self)
        self.golfTrophies.hide()
        self.golfTrophies.load()
        self.title = DirectLabel(
            parent=self,
            relief=None,
            text='',
            text_scale=0.10000000000000001,
            pos=(0, 0, 0.65000000000000002))
        normalColor = (1, 1, 1, 1)
        clickColor = (0.80000000000000004, 0.80000000000000004, 0, 1)
        rolloverColor = (0.14999999999999999, 0.81999999999999995, 1.0, 1)
        diabledColor = (1.0, 0.97999999999999998, 0.14999999999999999, 1)
        gui = loader.loadModel('phase_3.5/models/gui/fishingBook')
        self.recordsTab = DirectButton(
            parent=self,
            relief=None,
            text=TTLocalizer.GolfPageRecordsTab,
            text_scale=TTLocalizer.GPrecordsTab,
            text_align=TextNode.ALeft,
            image=gui.find('**/tabs/polySurface2'),
            image_pos=(0.12, 1, -0.91000000000000003),
            image_hpr=(0, 0, -90),
            image_scale=(0.033000000000000002, 0.033000000000000002,
                         0.035000000000000003),
            image_color=normalColor,
            image1_color=clickColor,
            image2_color=rolloverColor,
            image3_color=diabledColor,
            text_fg=Vec4(0.20000000000000001, 0.10000000000000001, 0, 1),
            command=self.setMode,
            extraArgs=[PageMode.Records],
            pos=TTLocalizer.GPrecordsTabPos)
        self.trophyTab = DirectButton(
            parent=self,
            relief=None,
            text=TTLocalizer.GolfPageTrophyTab,
            text_scale=TTLocalizer.GPtrophyTab,
            text_pos=TTLocalizer.GPtrophyTabTextPos,
            text_align=TextNode.ALeft,
            image=gui.find('**/tabs/polySurface3'),
            image_pos=(-0.28000000000000003, 1, -0.91000000000000003),
            image_hpr=(0, 0, -90),
            image_scale=(0.033000000000000002, 0.033000000000000002,
                         0.035000000000000003),
            image_color=normalColor,
            image1_color=clickColor,
            image2_color=rolloverColor,
            image3_color=diabledColor,
            text_fg=Vec4(0.20000000000000001, 0.10000000000000001, 0, 1),
            command=self.setMode,
            extraArgs=[PageMode.Trophy],
            pos=TTLocalizer.GPtrophyTabPos)
        self.recordsTab.setPos(-0.13, 0, 0.77500000000000002)
        self.trophyTab.setPos(0.28000000000000003, 0, 0.77500000000000002)
        adjust = -0.20000000000000001
        self.recordsTab.setX(self.recordsTab.getX() + adjust)
        self.trophyTab.setX(self.trophyTab.getX() + adjust)
        gui.removeNode()

    def unload(self):
        self.avatar = None
        ShtikerPage.unload(self)

    def setMode(self, mode, updateAnyways=0):
        messenger.send('wakeup')
        if not updateAnyways:
            if self.mode == mode:
                return None
            else:
                self.mode = mode

        if mode == PageMode.Records:
            self.title['text'] = TTLocalizer.GolfPageTitleRecords
            self.recordsTab['state'] = DGG.DISABLED
            self.trophyTab['state'] = DGG.NORMAL
        elif mode == PageMode.Trophy:
            self.title['text'] = TTLocalizer.GolfPageTitleTrophy
            self.recordsTab['state'] = DGG.NORMAL
            self.trophyTab['state'] = DGG.DISABLED
        else:
            raise Exception('GolfPage::setMode - Invalid Mode %s' % mode)
        self.updatePage()

    def updatePage(self):
        if self.mode == PageMode.Records:
            self.golfTrophies.hide()
            self.golfRecords.show()
        elif self.mode == PageMode.Trophy:
            self.golfTrophies.show()
            self.golfRecords.hide()
        else:
            raise Exception(
                'GolfPage::updatePage - Invalid Mode %s' % self.mode)


class GolfingRecordsUI(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('GolfingRecordsUI')

    def __init__(self, avatar, parent=aspect2d):
        self.avatar = avatar
        self.bestDisplayList = []
        self.lastHoleBest = []
        self.lastCourseBest = []
        self.scrollList = None
        DirectFrame.__init__(
            self,
            parent=parent,
            relief=None,
            pos=(0.0, 0.0, 0.0),
            scale=(1.0, 1.0, 1.0))

    def destroy(self):
        self.gui.removeNode()
        self.scrollList.destroy()
        del self.avatar
        del self.lastHoleBest
        del self.lastCourseBest
        del self.bestDisplayList
        del self.scrollList
        DirectFrame.destroy(self)

    def load(self):
        self.gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        self.listXorigin = -0.5
        self.listFrameSizeX = 1.5
        self.listZorigin = -0.90000000000000002
        self.listFrameSizeZ = 1.04
        self.arrowButtonScale = 1.3
        self.itemFrameXorigin = -0.23699999999999999
        self.itemFrameZorigin = 0.36499999999999999
        self.labelXstart = self.itemFrameXorigin + 0.29299999999999998
        self.scrollList = DirectScrolledList(
            parent=self,
            relief=None,
            pos=(0, 0, 0),
            incButton_image=(self.gui.find('**/FndsLst_ScrollUp'),
                             self.gui.find('**/FndsLst_ScrollDN'),
                             self.gui.find('**/FndsLst_ScrollUp_Rllvr'),
                             self.gui.find('**/FndsLst_ScrollUp')),
            incButton_relief=None,
            incButton_scale=(self.arrowButtonScale, self.arrowButtonScale,
                             -(self.arrowButtonScale)),
            incButton_pos=(self.labelXstart, 0, self.itemFrameZorigin - 0.999),
            incButton_image3_color=Vec4(1, 1, 1, 0.20000000000000001),
            decButton_image=(self.gui.find('**/FndsLst_ScrollUp'),
                             self.gui.find('**/FndsLst_ScrollDN'),
                             self.gui.find('**/FndsLst_ScrollUp_Rllvr'),
                             self.gui.find('**/FndsLst_ScrollUp')),
            decButton_relief=None,
            decButton_scale=(self.arrowButtonScale, self.arrowButtonScale,
                             self.arrowButtonScale),
            decButton_pos=(self.labelXstart, 0,
                           self.itemFrameZorigin + 0.22700000000000001),
            decButton_image3_color=Vec4(1, 1, 1, 0.20000000000000001),
            itemFrame_pos=(self.itemFrameXorigin, 0, self.itemFrameZorigin),
            itemFrame_scale=1.0,
            itemFrame_relief=DGG.SUNKEN,
            itemFrame_frameSize=(self.listXorigin,
                                 self.listXorigin + self.listFrameSizeX,
                                 self.listZorigin,
                                 self.listZorigin + self.listFrameSizeZ),
            itemFrame_frameColor=(0.84999999999999998, 0.94999999999999996, 1,
                                  1),
            itemFrame_borderWidth=(0.01, 0.01),
            numItemsVisible=12,
            forceHeight=0.083000000000000004,
            items=[])
        for courseId in GolfGlobals.CourseInfo:
            courseName = GolfGlobals.getCourseName(courseId)
            frame = DirectFrame(parent=self.scrollList, relief=None)
            courseNameDisplay = DirectLabel(
                parent=frame,
                relief=None,
                pos=(-0.47499999999999998, 0, 0.050000000000000003),
                text=courseName,
                text_align=TextNode.ALeft,
                text_scale=0.074999999999999997,
                text_fg=(0.84999999999999998, 0.64000000000000001, 0.13, 1.0),
                text_shadow=(0, 0, 0, 1),
                text_font=ToontownGlobals.getSignFont())
            bestScoreDisplay = DirectLabel(
                parent=frame,
                relief=None,
                pos=(0.90000000000000002, 0, 0.050000000000000003),
                text=TTLocalizer.KartRace_Unraced,
                text_scale=0.059999999999999998,
                text_fg=(0.0, 0.0, 0.0, 1.0),
                text_font=ToontownGlobals.getToonFont())
            self.bestDisplayList.append(bestScoreDisplay)
            self.scrollList.addItem(frame)

        for holeId in GolfGlobals.HoleInfo:
            holeName = GolfGlobals.getHoleName(holeId)
            frame = DirectFrame(parent=self.scrollList, relief=None)
            holeNameDisplay = DirectLabel(
                parent=frame,
                relief=None,
                pos=(-0.47499999999999998, 0, 0.050000000000000003),
                text=holeName,
                text_align=TextNode.ALeft,
                text_scale=0.074999999999999997,
                text_fg=(0.94999999999999996, 0.94999999999999996, 0.0, 1.0),
                text_shadow=(0, 0, 0, 1),
                text_font=ToontownGlobals.getSignFont())
            bestScoreDisplay = DirectLabel(
                parent=frame,
                relief=None,
                pos=(0.90000000000000002, 0, 0.050000000000000003),
                text=TTLocalizer.KartRace_Unraced,
                text_scale=0.059999999999999998,
                text_fg=(0.0, 0.0, 0.0, 1.0),
                text_font=ToontownGlobals.getToonFont())
            self.bestDisplayList.append(bestScoreDisplay)
            self.scrollList.addItem(frame)

    def show(self):
        bestHoles = self.avatar.getGolfHoleBest()
        bestCourses = self.avatar.getGolfCourseBest()
        if bestHoles != self.lastHoleBest or bestCourses != self.lastCourseBest:
            numCourse = len(GolfGlobals.CourseInfo.keys())
            numHoles = len(GolfGlobals.HoleInfo.keys())
            for i in xrange(numCourse):
                score = bestCourses[i]
                if score != 0:
                    self.bestDisplayList[i]['text'] = (str(score), )
                    continue
                self.bestDisplayList[i]['text'] = TTLocalizer.KartRace_Unraced

            for i in xrange(numHoles):
                score = bestHoles[i]
                if score != 0:
                    self.bestDisplayList[i + numCourse]['text'] = str(score)
                    continue
                self.bestDisplayList[
                    i + numCourse]['text'] = TTLocalizer.KartRace_Unraced

        self.lastHoleBest = bestHoles[:]
        self.lastCourseBest = bestCourses[:]
        DirectFrame.show(self)

    def regenerateScrollList(self):
        print '### regen scroll'
        selectedIndex = 0
        if self.scrollList:
            selectedIndex = self.scrollList.getSelectedIndex()
            for label in self.bestDisplayList:
                label.detachNode()

            self.scrollList.destroy()
            self.scrollList = None

        self.scrollList.scrollTo(selectedIndex)


class GolfTrophiesUI(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('GolfTrophiesUI')

    def __init__(self, avatar, parent=aspect2d):
        self.avatar = avatar
        self.trophyPanels = []
        self.cupPanels = []
        self.trophies = None
        self.cups = None
        self.trophyTextDisplay = None
        DirectFrame.__init__(
            self,
            parent=parent,
            relief=None,
            pos=(0.0, 0.0, 0.0),
            scale=(1.0, 1.0, 1.0))

    def destroy(self):
        for panel in self.trophyPanels:
            panel.destroy()

        for panel in self.cupPanels:
            panel.destroy()

        self.currentHistory.destroy()
        self.trophyTextDisplay.destroy()
        del self.avatar
        del self.currentHistory
        del self.trophyPanels
        del self.trophies
        del self.trophyTextDisplay
        del self.cups
        del self.cupPanels
        DirectFrame.destroy(self)

    def load(self):
        self.trophies = base.localAvatar.getGolfTrophies()[:]
        self.cups = base.localAvatar.getGolfCups()[:]
        xStart = -0.76000000000000001
        yStart = 0.47499999999999998
        xOffset = 0.17000000000000001
        yOffset = 0.23000000000000001
        for j in range(GolfGlobals.NumCups):
            for i in range(GolfGlobals.TrophiesPerCup):
                trophyPanel = DirectLabel(
                    parent=self,
                    relief=None,
                    pos=(xStart + i * xOffset, 0.0, yStart - j * yOffset),
                    state=DGG.NORMAL,
                    image=DGG.getDefaultDialogGeom(),
                    image_scale=(0.75, 1, 1),
                    image_color=(0.80000000000000004, 0.80000000000000004,
                                 0.80000000000000004, 1),
                    text=TTLocalizer.SuitPageMystery[0],
                    text_scale=0.45000000000000001,
                    text_fg=(0, 0, 0, 1),
                    text_pos=(0, 0, -0.25),
                    text_font=ToontownGlobals.getInterfaceFont(),
                    text_wordwrap=5.5)
                trophyPanel.scale = 0.20000000000000001
                trophyPanel.setScale(trophyPanel.scale)
                self.trophyPanels.append(trophyPanel)

        xStart = -0.25
        yStart = -0.38
        xOffset = 0.25
        for i in range(GolfGlobals.NumCups):
            cupPanel = DirectLabel(
                parent=self,
                relief=None,
                pos=(xStart + i * xOffset, 0.0, yStart),
                state=DGG.NORMAL,
                image=DGG.getDefaultDialogGeom(),
                image_scale=(0.75, 1, 1),
                image_color=(0.80000000000000004, 0.80000000000000004,
                             0.80000000000000004, 1),
                text=TTLocalizer.SuitPageMystery[0],
                text_scale=0.45000000000000001,
                text_fg=(0, 0, 0, 1),
                text_pos=(0, 0, -0.25),
                text_font=ToontownGlobals.getInterfaceFont(),
                text_wordwrap=5.5)
            cupPanel.scale = 0.29999999999999999
            cupPanel.setScale(cupPanel.scale)
            self.cupPanels.append(cupPanel)

        self.currentHistory = DirectLabel(
            parent=self,
            relief=None,
            text='',
            text_scale=0.050000000000000003,
            text_fg=(0, 0, 0.94999999999999996, 1.0),
            text_pos=(0, -0.65000000000000002))
        self.trophyTextDisplay = DirectLabel(
            parent=self,
            relief=None,
            text='',
            text_scale=0.070000000000000007,
            text_fg=(1, 0, 0, 1),
            text_shadow=(0, 0, 0, 0),
            text_pos=(0.0, -0.17499999999999999),
            text_font=ToontownGlobals.getInterfaceFont())
        self.updateTrophies()

    def grow(self, index, pos):
        self.trophyPanels[index]['image_color'] = Vec4(
            1.0, 1.0, 0.80000000000000004, 1.0)
        if index < GolfGlobals.NumTrophies:
            self.trophyTextDisplay[
                'text'] = TTLocalizer.GolfTrophyTextDisplay % {
                    'number': index + 1,
                    'desc': TTLocalizer.GolfTrophyDescriptions[index]
                }
            historyIndex = GolfGlobals.getHistoryIndexForTrophy(index)
            if historyIndex >= 0:
                self.currentHistory[
                    'text'] = TTLocalizer.GolfCurrentHistory % {
                        'historyDesc':
                        TTLocalizer.GolfHistoryDescriptions[historyIndex],
                        'num':
                        self.avatar.getGolfHistory()[historyIndex]
                    }

    def shrink(self, index, pos):
        self.trophyPanels[index]['image_color'] = Vec4(1.0, 1.0, 1.0, 1.0)
        self.trophyTextDisplay['text'] = ''
        self.currentHistory['text'] = ''

    def growCup(self, index, pos):
        self.cupPanels[index]['image_color'] = Vec4(1.0, 1.0,
                                                    0.80000000000000004, 1.0)
        if index < GolfGlobals.NumTrophies:
            self.trophyTextDisplay['text'] = TTLocalizer.GolfCupTextDisplay % {
                'number': index + 1,
                'desc': TTLocalizer.GolfCupDescriptions[index]
            }

    def shrinkCup(self, index, pos):
        self.cupPanels[index]['image_color'] = Vec4(1.0, 1.0, 1.0, 1.0)
        self.trophyTextDisplay['text'] = ''

    def show(self):
        self.currentHistory['text'] = ''
        if self.trophies != base.localAvatar.getGolfTrophies():
            self.trophies = base.localAvatar.getGolfTrophies()
            self.cups = base.localAvatar.getGolfCups()
            self.updateTrophies()

        DirectFrame.show(self)

    def updateTrophies(self):
        for t in range(len(self.trophyPanels)):
            if self.trophies[t]:
                trophyPanel = self.trophyPanels[t]
                trophyPanel['text'] = ''
                golfTrophy = trophyPanel.find('**/*GolfTrophy*')
                if golfTrophy.isEmpty():
                    trophyModel = GolfTrophy(t)
                    trophyModel.reparentTo(trophyPanel)
                    trophyModel.nameLabel.hide()
                    trophyModel.setPos(0, 0, -0.40000000000000002)

                trophyPanel['image_color'] = Vec4(1.0, 1.0, 1.0, 1.0)
                trophyPanel.bind(DGG.ENTER, self.grow, extraArgs=[t])
                trophyPanel.bind(DGG.EXIT, self.shrink, extraArgs=[t])
                continue
            trophyPanel = self.trophyPanels[t]
            toBeNukedGolfTrophy = trophyPanel.find('**/*GolfTrophy*')
            if not toBeNukedGolfTrophy.isEmpty():
                toBeNukedGolfTrophy.removeNode()

            trophyPanel['text'] = TTLocalizer.SuitPageMystery[0]
            trophyPanel['image_color'] = Vec4(0.80000000000000004,
                                              0.80000000000000004,
                                              0.80000000000000004, 1)
            trophyPanel.unbind(DGG.ENTER)
            trophyPanel.unbind(DGG.EXIT)

        for t in range(len(self.cupPanels)):
            if self.cups[t]:
                cupPanel = self.cupPanels[t]
                cupPanel['text'] = ''
                cupTrophy = cupPanel.find('**/*GolfTrophy*')
                if cupTrophy.isEmpty():
                    cupModel = GolfTrophy(t + GolfGlobals.NumTrophies)
                    cupModel.reparentTo(cupPanel)
                    cupModel.nameLabel.hide()
                    cupModel.setPos(0, 0, -0.40000000000000002)

                cupPanel['image_color'] = Vec4(1.0, 1.0, 1.0, 1.0)
                cupPanel.bind(DGG.ENTER, self.growCup, extraArgs=[t])
                cupPanel.bind(DGG.EXIT, self.shrinkCup, extraArgs=[t])
                continue
            cupPanel = self.cupPanels[t]
            toBeNukedGolfCup = cupPanel.find('**/*GolfTrophy*')
            if not toBeNukedGolfCup.isEmpty():
                toBeNukedGolfCup.removeNode()

            cupPanel['text'] = TTLocalizer.SuitPageMystery[0]
            cupPanel['image_color'] = Vec4(0.80000000000000004,
                                           0.80000000000000004,
                                           0.80000000000000004, 1)
            cupPanel.unbind(DGG.ENTER)
            cupPanel.unbind(DGG.EXIT)


class GolfTrophy(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('GolfTrophy')

    def __init__(self, level, *args, **kwargs):
        opts = {'relief': None}
        opts.update(kwargs)
        DirectFrame.__init__(self, *args, **args)
        self.trophy = loader.loadModel('phase_6/models/golf/golfTrophy')
        self.trophy.reparentTo(self)
        self.trophy.setPos(0, 1, 0)
        self.trophy.setScale(0.10000000000000001)
        self.base = self.trophy.find('**/trophyBase')
        self.column = self.trophy.find('**/trophyColumn')
        self.top = self.trophy.find('**/trophyTop')
        self.topBase = self.trophy.find('**/trophyTopBase')
        self.statue = self.trophy.find('**/trophyStatue')
        self.base.setColorScale(1, 1, 0.80000000000000004, 1)
        self.topBase.setColorScale(1, 1, 0.80000000000000004, 1)
        self.greyBowl = loader.loadModel(
            'phase_6/models/gui/racingTrophyBowl2')
        self.greyBowl.reparentTo(self)
        self.greyBowl.setPos(0, 0.5, 0)
        self.greyBowl.setScale(2.0)
        self.goldBowl = loader.loadModel('phase_6/models/gui/racingTrophyBowl')
        self.goldBowl.reparentTo(self)
        self.goldBowl.setPos(0, 0.5, 0)
        self.goldBowl.setScale(2.0)
        self.goldBowlBase = self.goldBowl.find('**/fishingTrophyBase')
        self.goldBowlBase.hide()
        self.nameLabel = DirectLabel(
            parent=self,
            relief=None,
            pos=(0, 0, -0.14999999999999999),
            text='',
            text_scale=0.125,
            text_fg=Vec4(0.90000000000000002, 0.90000000000000002,
                         0.40000000000000002, 1))
        self.shadow = loader.loadModel('phase_3/models/props/drop_shadow')
        self.shadow.reparentTo(self)
        self.shadow.setColor(1, 1, 1, 0.20000000000000001)
        self.shadow.setPosHprScale(0, 1, 0.34999999999999998, 0, 90, 0,
                                   0.10000000000000001, 0.14000000000000001,
                                   0.10000000000000001)
        self.setLevel(level)

    def setLevel(self, level):
        self.level = level
        if level == -1:
            self.trophy.hide()
            self.greyBowl.hide()
            self.goldBowl.hide()
            self.nameLabel.hide()
        else:
            self.nameLabel.show()
            if level >= 30:
                self.trophy.hide()
                self.greyBowl.hide()
                self.goldBowl.show()
                self.goldBowlBase.hide()
            else:
                self.trophy.show()
                self.goldBowl.hide()
                self.greyBowl.hide()
            if level == 30:
                self.goldBowl.setScale(4.4000000000000004, 3.1000000000000001,
                                       3.1000000000000001)
            elif level == 31:
                self.goldBowl.setScale(3.6000000000000001, 3.5, 3.5)
            elif level >= 32:
                self.goldBowl.setScale(5.5999999999999996, 3.8999999999999999,
                                       3.8999999999999999)

            if level % 3 == 0:
                self.column.setScale(1.3229, 1.26468, 1.1187800000000001)
                self.top.setPos(0, 0, -1)
                self._GolfTrophy__bronze()
            elif level % 3 == 1:
                self.column.setScale(1.3229, 1.26468, 1.6187800000000001)
                self.top.setPos(0, 0, -0.5)
                self._GolfTrophy__silver()
            elif level % 3 == 2:
                self.column.setScale(1.3229, 1.26468, 2.1187800000000001)
                self.top.setPos(0, 0, 0)
                self._GolfTrophy__gold()

            if level < 10:
                self._GolfTrophy__tealColumn()
            elif level < 20:
                self._GolfTrophy__purpleColumn()
            elif level < 30:
                self._GolfTrophy__blueColumn()
            else:
                self._GolfTrophy__redColumn()

    def _GolfTrophy__bronze(self):
        self.statue.setColorScale(0.90000000000000002, 0.59999999999999998,
                                  0.33000000000000002, 1)

    def _GolfTrophy__silver(self):
        self.statue.setColorScale(0.90000000000000002, 0.90000000000000002, 1,
                                  1)

    def _GolfTrophy__gold(self):
        self.statue.setColorScale(1, 0.94999999999999996, 0.10000000000000001,
                                  1)

    def _GolfTrophy__platinum(self):
        self.statue.setColorScale(1, 0.94999999999999996, 0.10000000000000001,
                                  1)

    def _GolfTrophy__tealColumn(self):
        self.column.setColorScale(0.5, 1.2, 0.84999999999999998, 1)

    def _GolfTrophy__purpleColumn(self):
        self.column.setColorScale(1, 0.69999999999999996, 0.94999999999999996,
                                  1)

    def _GolfTrophy__redColumn(self):
        self.column.setColorScale(1.2, 0.59999999999999998,
                                  0.59999999999999998, 1)

    def _GolfTrophy__yellowColumn(self):
        self.column.setColorScale(1, 1, 0.80000000000000004, 1)

    def _GolfTrophy__blueColumn(self):
        self.column.setColorScale(0.59999999999999998, 0.75, 1.2, 1)

    def destroy(self):
        self.trophy.removeNode()
        self.goldBowl.removeNode()
        self.greyBowl.removeNode()
        self.shadow.removeNode()
        DirectFrame.destroy(self)
