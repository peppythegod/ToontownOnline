from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
from direct.showbase import DirectObject
from direct.fsm import StateData
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from toontown.effects import DistributedFireworkShow
from toontown.parties import DistributedPartyFireworksActivity
from direct.directnotify import DirectNotifyGlobal


class ShtikerBook(DirectFrame, StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('ShtikerBook')

    def __init__(self, doneEvent):
        DirectFrame.__init__(
            self, relief=None, sortOrder=DGG.BACKGROUND_SORT_INDEX)
        self.initialiseoptions(ShtikerBook)
        StateData.StateData.__init__(self, doneEvent)
        self.pages = []
        self.pageTabs = []
        self.currPageTabIndex = None
        self.pageTabFrame = DirectFrame(
            parent=self,
            relief=None,
            pos=(0.93000000000000005, 1, 0.57499999999999996),
            scale=1.25)
        self.pageTabFrame.hide()
        self.currPageIndex = None
        self.pageBeforeNews = None
        self.entered = 0
        self.safeMode = 0
        self._ShtikerBook__obscured = 0
        self._ShtikerBook__shown = 0
        self._ShtikerBook__isOpen = 0
        self.hide()
        self.setPos(0, 0, 0.10000000000000001)
        self.pageOrder = [
            TTLocalizer.OptionsPageTitle, TTLocalizer.ShardPageTitle,
            TTLocalizer.MapPageTitle, TTLocalizer.InventoryPageTitle,
            TTLocalizer.QuestPageToonTasks, TTLocalizer.TrackPageShortTitle,
            TTLocalizer.SuitPageTitle, TTLocalizer.FishPageTitle,
            TTLocalizer.KartPageTitle, TTLocalizer.DisguisePageTitle,
            TTLocalizer.NPCFriendPageTitle, TTLocalizer.GardenPageTitle,
            TTLocalizer.GolfPageTitle, TTLocalizer.EventsPageName,
            TTLocalizer.NewsPageName
        ]

    def setSafeMode(self, setting):
        self.safeMode = setting

    def enter(self):
        if base.config.GetBool('want-qa-regression', 0):
            self.notify.info('QA-REGRESSION: SHTICKERBOOK: Open')

        if self.entered:
            return None

        self.entered = 1
        messenger.send('releaseDirector')
        messenger.send('stickerBookEntered')
        base.playSfx(self.openSound)
        base.disableMouse()
        base.render.hide()
        base.setBackgroundColor(0.050000000000000003, 0.14999999999999999,
                                0.40000000000000002)
        base.setCellsAvailable([base.rightCells[0]], 0)
        self.oldMin2dAlpha = NametagGlobals.getMin2dAlpha()
        self.oldMax2dAlpha = NametagGlobals.getMax2dAlpha()
        NametagGlobals.setMin2dAlpha(0.80000000000000004)
        NametagGlobals.setMax2dAlpha(1.0)
        self._ShtikerBook__isOpen = 1
        self._ShtikerBook__setButtonVisibility()
        self.show()
        self.showPageArrows()
        if not self.safeMode:
            self.accept('shtiker-page-done', self._ShtikerBook__pageDone)
            self.accept(ToontownGlobals.StickerBookHotkey,
                        self._ShtikerBook__close)
            self.accept(ToontownGlobals.OptionsPageHotkey,
                        self._ShtikerBook__close)
            self.pageTabFrame.show()

        self.pages[self.currPageIndex].enter()
        if hasattr(localAvatar, 'newsButtonMgr') and localAvatar.newsButtonMgr:
            localAvatar.newsButtonMgr.hideNewIssueButton()

    def exit(self):
        if not self.entered:
            return None

        self.entered = 0
        messenger.send('stickerBookExited')
        base.playSfx(self.closeSound)
        self.pages[self.currPageIndex].exit()
        base.render.show()
        setBlackBackground = 0
        for obj in base.cr.doId2do.values():
            if isinstance(obj, DistributedFireworkShow.DistributedFireworkShow
                          ) or isinstance(
                              obj, DistributedPartyFireworksActivity.
                              DistributedPartyFireworksActivity):
                setBlackBackground = 1
                continue

        if setBlackBackground:
            base.setBackgroundColor(Vec4(0, 0, 0, 1))
        else:
            base.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)
        gsg = base.win.getGsg()
        if gsg:
            base.render.prepareScene(gsg)

        NametagGlobals.setMin2dAlpha(self.oldMin2dAlpha)
        NametagGlobals.setMax2dAlpha(self.oldMax2dAlpha)
        base.setCellsAvailable([base.rightCells[0]], 1)
        self._ShtikerBook__isOpen = 0
        self.hide()
        self.hideButton()
        cleanupDialog('globalDialog')
        self.pageTabFrame.hide()
        self.ignore('shtiker-page-done')
        self.ignore(ToontownGlobals.StickerBookHotkey)
        self.ignore(ToontownGlobals.OptionsPageHotkey)
        self.ignore('arrow_right')
        self.ignore('arrow_left')
        if base.config.GetBool('want-qa-regression', 0):
            self.notify.info('QA-REGRESSION: SHTICKERBOOK: Close')

    def load(self):
        self.checkGardenStarted = localAvatar.getGardenStarted()
        bookModel = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
        self['image'] = bookModel.find('**/big_book')
        self['image_scale'] = (2, 1, 1.5)
        self.resetFrameSize()
        self.bookOpenButton = DirectButton(
            image=(bookModel.find('**/BookIcon_CLSD'),
                   bookModel.find('**/BookIcon_OPEN'),
                   bookModel.find('**/BookIcon_RLVR')),
            relief=None,
            pos=(1.175, 0, -0.82999999999999996),
            scale=0.30499999999999999,
            command=self._ShtikerBook__open)
        self.bookCloseButton = DirectButton(
            image=(bookModel.find('**/BookIcon_OPEN'),
                   bookModel.find('**/BookIcon_CLSD'),
                   bookModel.find('**/BookIcon_RLVR2')),
            relief=None,
            pos=(1.175, 0, -0.82999999999999996),
            scale=0.30499999999999999,
            command=self._ShtikerBook__close)
        self.bookOpenButton.hide()
        self.bookCloseButton.hide()
        self.nextArrow = DirectButton(
            parent=self,
            relief=None,
            image=(bookModel.find('**/arrow_button'),
                   bookModel.find('**/arrow_down'),
                   bookModel.find('**/arrow_rollover')),
            scale=(0.10000000000000001, 0.10000000000000001,
                   0.10000000000000001),
            pos=(0.83799999999999997, 0, -0.66100000000000003),
            command=self._ShtikerBook__pageChange,
            extraArgs=[1])
        self.prevArrow = DirectButton(
            parent=self,
            relief=None,
            image=(bookModel.find('**/arrow_button'),
                   bookModel.find('**/arrow_down'),
                   bookModel.find('**/arrow_rollover')),
            scale=(-0.10000000000000001, 0.10000000000000001,
                   0.10000000000000001),
            pos=(-0.83799999999999997, 0, -0.66100000000000003),
            command=self._ShtikerBook__pageChange,
            extraArgs=[-1])
        bookModel.removeNode()
        self.openSound = base.loadSfx(
            'phase_3.5/audio/sfx/GUI_stickerbook_open.mp3')
        self.closeSound = base.loadSfx(
            'phase_3.5/audio/sfx/GUI_stickerbook_delete.mp3')
        self.pageSound = base.loadSfx(
            'phase_3.5/audio/sfx/GUI_stickerbook_turn.mp3')

    def unload(self):
        loader.unloadModel('phase_3.5/models/gui/stickerbook_gui')
        self.destroy()
        self.bookOpenButton.destroy()
        del self.bookOpenButton
        self.bookCloseButton.destroy()
        del self.bookCloseButton
        self.nextArrow.destroy()
        del self.nextArrow
        self.prevArrow.destroy()
        del self.prevArrow
        for page in self.pages:
            page.unload()

        del self.pages
        for pageTab in self.pageTabs:
            pageTab.destroy()

        del self.pageTabs
        del self.currPageTabIndex
        del self.openSound
        del self.closeSound
        del self.pageSound

    def addPage(self, page, pageName='Page'):
        if pageName not in self.pageOrder:
            self.notify.error(
                'Trying to add page %s in the ShtickerBook. Page not listed in the order.'
                % pageName)
            return None

        pageIndex = 0
        if len(self.pages):
            newIndex = len(self.pages)
            prevIndex = newIndex - 1
            if self.pages[prevIndex].pageName == TTLocalizer.NewsPageName:
                self.pages.insert(prevIndex, page)
                pageIndex = prevIndex
                if self.currPageIndex >= pageIndex:
                    self.currPageIndex += 1

            else:
                self.pages.append(page)
                pageIndex = len(self.pages) - 1
        else:
            self.pages.append(page)
            pageIndex = len(self.pages) - 1
        page.setBook(self)
        page.setPageName(pageName)
        page.reparentTo(self)
        self.addPageTab(page, pageIndex, pageName)
        import MapPage
        if isinstance(page, MapPage.MapPage):
            self.pageBeforeNews = page

    def addPageTab(self, page, pageIndex, pageName='Page'):
        tabIndex = len(self.pageTabs)

        def goToPage():
            messenger.send('wakeup')
            base.playSfx(self.pageSound)
            self.setPage(page)
            if base.config.GetBool('want-qa-regression', 0):
                self.notify.info('QA-REGRESSION: SHTICKERBOOK: Browse tabs %s'
                                 % page.pageName)

            localAvatar.newsButtonMgr.setGoingToNewsPageFromStickerBook(False)
            localAvatar.newsButtonMgr.showAppropriateButton()

        yOffset = 0.070000000000000007 * pageIndex
        iconGeom = None
        iconImage = None
        iconScale = 1
        iconColor = Vec4(1)
        buttonPressedCommand = goToPage
        extraArgs = []
        if pageName == TTLocalizer.OptionsPageTitle:
            iconModels = loader.loadModel('phase_3.5/models/gui/sos_textures')
            iconGeom = iconModels.find('**/switch')
            iconModels.detachNode()
        elif pageName == TTLocalizer.ShardPageTitle:
            iconModels = loader.loadModel('phase_3.5/models/gui/sos_textures')
            iconGeom = iconModels.find('**/district')
            iconModels.detachNode()
        elif pageName == TTLocalizer.MapPageTitle:
            iconModels = loader.loadModel('phase_3.5/models/gui/sos_textures')
            iconGeom = iconModels.find('**/teleportIcon')
            iconModels.detachNode()
        elif pageName == TTLocalizer.InventoryPageTitle:
            iconModels = loader.loadModel(
                'phase_3.5/models/gui/inventory_icons')
            iconGeom = iconModels.find('**/inventory_tart')
            iconScale = 7
            iconModels.detachNode()
        elif pageName == TTLocalizer.QuestPageToonTasks:
            iconModels = loader.loadModel(
                'phase_3.5/models/gui/stickerbook_gui')
            iconGeom = iconModels.find('**/questCard')
            iconScale = 0.90000000000000002
            iconModels.detachNode()
        elif pageName == TTLocalizer.TrackPageShortTitle:
            iconGeom = loader.loadModel('phase_3.5/models/gui/filmstrip')
            iconModels = loader.loadModel('phase_3.5/models/gui/filmstrip')
            iconScale = 1.1000000000000001
            iconColor = Vec4(0.69999999999999996, 0.69999999999999996,
                             0.69999999999999996, 1)
            iconModels.detachNode()
        elif pageName == TTLocalizer.SuitPageTitle:
            iconModels = loader.loadModel('phase_3.5/models/gui/sos_textures')
            iconGeom = iconModels.find('**/gui_gear')
            iconModels.detachNode()
        elif pageName == TTLocalizer.FishPageTitle:
            iconModels = loader.loadModel('phase_3.5/models/gui/sos_textures')
            iconGeom = iconModels.find('**/fish')
            iconModels.detachNode()
        elif pageName == TTLocalizer.GardenPageTitle:
            iconModels = loader.loadModel('phase_3.5/models/gui/sos_textures')
            iconGeom = iconModels.find('**/gardenIcon')
            iconModels.detachNode()
        elif pageName == TTLocalizer.DisguisePageTitle:
            iconModels = loader.loadModel('phase_3.5/models/gui/sos_textures')
            iconGeom = iconModels.find('**/disguise2')
            iconColor = Vec4(0.69999999999999996, 0.69999999999999996,
                             0.69999999999999996, 1)
            iconModels.detachNode()
        elif pageName == TTLocalizer.NPCFriendPageTitle:
            iconModels = loader.loadModel('phase_3.5/models/gui/playingCard')
            iconImage = iconModels.find('**/card_back')
            iconGeom = iconModels.find('**/logo')
            iconScale = 0.22
            iconModels.detachNode()
        elif pageName == TTLocalizer.KartPageTitle:
            iconModels = loader.loadModel('phase_3.5/models/gui/sos_textures')
            iconGeom = iconModels.find('**/kartIcon')
            iconModels.detachNode()
        elif pageName == TTLocalizer.GolfPageTitle:
            iconModels = loader.loadModel('phase_6/models/golf/golf_gui')
            iconGeom = iconModels.find('**/score_card_icon')
            iconModels.detachNode()
        elif pageName == TTLocalizer.EventsPageName:
            iconModels = loader.loadModel(
                'phase_4/models/parties/partyStickerbook')
            iconGeom = iconModels.find('**/Stickerbook_PartyIcon')
            iconModels.detachNode()
        elif pageName == TTLocalizer.NewsPageName:
            iconModels = loader.loadModel('phase_3.5/models/gui/sos_textures')
            iconGeom = iconModels.find('**/tt_t_gui_sbk_newsPageTab')
            iconModels.detachNode()
            buttonPressedCommand = self.goToNewsPage
            extraArgs = [page]

        if pageName == TTLocalizer.OptionsPageTitle:
            pageName = TTLocalizer.OptionsTabTitle

        pageTab = DirectButton(
            parent=self.pageTabFrame,
            relief=DGG.RAISED,
            frameSize=(-0.57499999999999996, 0.57499999999999996,
                       -0.57499999999999996, 0.57499999999999996),
            borderWidth=(0.050000000000000003, 0.050000000000000003),
            text=('', '', pageName, ''),
            text_align=TextNode.ALeft,
            text_pos=(1, -0.20000000000000001),
            text_scale=TTLocalizer.SBpageTab,
            text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 1),
            image=iconImage,
            image_scale=iconScale,
            geom=iconGeom,
            geom_scale=iconScale,
            geom_color=iconColor,
            pos=(0, 0, -yOffset),
            scale=0.059999999999999998,
            command=buttonPressedCommand,
            extraArgs=extraArgs)
        self.pageTabs.insert(pageIndex, pageTab)

    def setPage(self, page, enterPage=True):
        if self.currPageIndex is not None:
            self.pages[self.currPageIndex].exit()

        self.currPageIndex = self.pages.index(page)
        self.setPageTabIndex(self.currPageIndex)
        if enterPage:
            self.showPageArrows()
            page.enter()

        import NewsPage
        if not isinstance(page, NewsPage.NewsPage):
            self.pageBeforeNews = page

    def setPageBeforeNews(self, enterPage=True):
        self.setPage(self.pageBeforeNews, enterPage)
        self.accept(ToontownGlobals.StickerBookHotkey,
                    self._ShtikerBook__close)
        self.accept(ToontownGlobals.OptionsPageHotkey,
                    self._ShtikerBook__close)

    def setPageTabIndex(self, pageTabIndex):
        if self.currPageTabIndex is not None and pageTabIndex != self.currPageTabIndex:
            self.pageTabs[self.currPageTabIndex]['relief'] = DGG.RAISED

        self.currPageTabIndex = pageTabIndex
        self.pageTabs[self.currPageTabIndex]['relief'] = DGG.SUNKEN

    def isOnPage(self, page):
        result = False
        if self.currPageIndex is not None:
            curPage = self.pages[self.currPageIndex]
            if curPage == page:
                result = True

        return result

    def obscureButton(self, obscured):
        self._ShtikerBook__obscured = obscured
        self._ShtikerBook__setButtonVisibility()

    def isObscured(self):
        return self._ShtikerBook__obscured

    def showButton(self):
        self._ShtikerBook__shown = 1
        self._ShtikerBook__setButtonVisibility()
        localAvatar.newsButtonMgr.showAppropriateButton()

    def hideButton(self):
        self._ShtikerBook__shown = 0
        self._ShtikerBook__setButtonVisibility()
        localAvatar.newsButtonMgr.request('Hidden')

    def _ShtikerBook__setButtonVisibility(self):
        if self._ShtikerBook__isOpen:
            self.bookOpenButton.hide()
            self.bookCloseButton.show()
        elif self._ShtikerBook__shown and not (self._ShtikerBook__obscured):
            self.bookOpenButton.show()
            self.bookCloseButton.hide()
        else:
            self.bookOpenButton.hide()
            self.bookCloseButton.hide()

    def shouldBookButtonBeHidden(self):
        result = False
        if self._ShtikerBook__isOpen:
            pass
        1
        if self._ShtikerBook__shown and not (self._ShtikerBook__obscured):
            pass
        1
        result = True
        return result

    def _ShtikerBook__open(self):
        messenger.send('enterStickerBook')
        if not localAvatar.getGardenStarted():
            for tab in self.pageTabs:
                if tab['text'][2] == TTLocalizer.GardenPageTitle:
                    tab.hide()
                    continue

    def _ShtikerBook__close(self):
        base.playSfx(self.closeSound)
        self.doneStatus = {'mode': 'close'}
        messenger.send('exitStickerBook')
        messenger.send(self.doneEvent)

    def closeBook(self):
        self._ShtikerBook__close()

    def _ShtikerBook__pageDone(self):
        page = self.pages[self.currPageIndex]
        pageDoneStatus = page.getDoneStatus()
        if pageDoneStatus:
            if pageDoneStatus['mode'] == 'close':
                self._ShtikerBook__close()
            else:
                self.doneStatus = pageDoneStatus
                messenger.send(self.doneEvent)

    def _ShtikerBook__pageChange(self, offset):
        messenger.send('wakeup')
        base.playSfx(self.pageSound)
        self.pages[self.currPageIndex].exit()
        self.currPageIndex = self.currPageIndex + offset
        messenger.send('stickerBookPageChange-' + str(self.currPageIndex))
        self.currPageIndex = max(self.currPageIndex, 0)
        self.currPageIndex = min(self.currPageIndex, len(self.pages) - 1)
        self.setPageTabIndex(self.currPageIndex)
        self.showPageArrows()
        page = self.pages[self.currPageIndex]
        import NewsPage
        if isinstance(page, NewsPage.NewsPage):
            self.goToNewsPage(page)
        else:
            page.enter()
            self.pageBeforeNews = page

    def showPageArrows(self):
        if self.currPageIndex == len(self.pages) - 1:
            self.prevArrow.show()
            self.nextArrow.hide()
        else:
            self.prevArrow.show()
            self.nextArrow.show()
        self._ShtikerBook__checkForNewsPage()
        if self.currPageIndex == 0:
            self.prevArrow.hide()
            self.nextArrow.show()

    def _ShtikerBook__checkForNewsPage(self):
        import NewsPage
        self.ignore('arrow_left')
        self.ignore('arrow_right')
        if isinstance(self.pages[self.currPageIndex], NewsPage.NewsPage):
            self.ignore('arrow_left')
            self.ignore('arrow_right')
        else:
            self.accept('arrow_right', self._ShtikerBook__pageChange, [1])
            self.accept('arrow_left', self._ShtikerBook__pageChange, [-1])

    def goToNewsPage(self, page):
        messenger.send('wakeup')
        base.playSfx(self.pageSound)
        localAvatar.newsButtonMgr.setGoingToNewsPageFromStickerBook(True)
        localAvatar.newsButtonMgr.showAppropriateButton()
        self.setPage(page)
        if base.config.GetBool('want-qa-regression', 0):
            self.notify.info(
                'QA-REGRESSION: SHTICKERBOOK: Browse tabs %s' % page.pageName)

        self.ignore(ToontownGlobals.StickerBookHotkey)
        self.ignore(ToontownGlobals.OptionsPageHotkey)
        localAvatar.newsButtonMgr.acceptEscapeKeyPress()

    def disableBookCloseButton(self):
        if self.bookCloseButton:
            self.bookCloseButton['command'] = None

    def enableBookCloseButton(self):
        if self.bookCloseButton:
            self.bookCloseButton['command'] = self._ShtikerBook__close

    def disableAllPageTabs(self):
        for button in self.pageTabs:
            button['state'] = DGG.DISABLED

    def enableAllPageTabs(self):
        for button in self.pageTabs:
            button['state'] = DGG.NORMAL
