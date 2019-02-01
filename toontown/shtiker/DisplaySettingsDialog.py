from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task.Task import Task
from direct.fsm import StateData
from direct.showbase import AppRunnerGlobal
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TTDialog
from toontown.toonbase import ToontownGlobals
from toontown.toonbase.DisplayOptions import DisplayOptions


class DisplaySettingsDialog(DirectFrame, StateData.StateData):
    ApplyTimeoutSeconds = 15
    TimeoutCountdownTask = 'DisplaySettingsTimeoutCountdown'
    WindowedMode = 0
    FullscreenMode = 1
    EmbeddedMode = 2
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DisplaySettingsDialog')

    def __init__(self):
        DirectFrame.__init__(
            self,
            pos=(
                0,
                0,
                0.29999999999999999),
            relief=None,
            image=DGG.getDefaultDialogGeom(),
            image_scale=(
                1.6000000000000001,
                1,
                1.2),
            image_pos=(
                0,
                0,
                -0.050000000000000003),
            image_color=ToontownGlobals.GlobalDialogColor,
            text=TTLocalizer.DisplaySettingsTitle,
            text_scale=0.12,
            text_pos=(
                0,
                0.40000000000000002),
            borderWidth=(
                0.01,
                0.01))
        StateData.StateData.__init__(self, 'display-settings-done')
        self.setBin('gui-popup', 0)
        self.initialiseoptions(DisplaySettingsDialog)

    def unload(self):
        if self.isLoaded == 0:
            return None

        self.isLoaded = 0
        self.exit()
        DirectFrame.destroy(self)

    def load(self):
        if self.isLoaded == 1:
            return None

        self.isLoaded = 1
        self.anyChanged = 0
        self.apiChanged = 0
        self.screenSizes = ((640, 480), (800, 600),
                            (1024, 768), (1280, 1024), (1600, 1200))
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        nameShopGui = loader.loadModel('phase_3/models/gui/nameshop_gui')
        circle = nameShopGui.find('**/namePanelCircle')
        innerCircle = circle.copyTo(hidden)
        innerCircle.setPos(0, 0, 0.20000000000000001)
        self.c1b = circle.copyTo(self, -1)
        self.c1b.setColor(0, 0, 0, 1)
        self.c1b.setPos(0.043999999999999997, 0, -0.20999999999999999)
        self.c1b.setScale(0.40000000000000002)
        c1f = circle.copyTo(self.c1b)
        c1f.setColor(1, 1, 1, 1)
        c1f.setScale(0.80000000000000004)
        self.c2b = circle.copyTo(self, -2)
        self.c2b.setColor(0, 0, 0, 1)
        self.c2b.setPos(0.043999999999999997, 0, -0.29999999999999999)
        self.c2b.setScale(0.40000000000000002)
        c2f = circle.copyTo(self.c2b)
        c2f.setColor(1, 1, 1, 1)
        c2f.setScale(0.80000000000000004)
        self.c3b = circle.copyTo(self, -2)
        self.c3b.setColor(0, 0, 0, 1)
        self.c3b.setPos(0.043999999999999997, 0, -0.40000000000000002)
        self.c3b.setScale(0.40000000000000002)
        c3f = circle.copyTo(self.c3b)
        c3f.setColor(1, 1, 1, 1)
        c3f.setScale(0.80000000000000004)
        self.introText = DirectLabel(parent=self,
                                     relief=None,
                                     scale=TTLocalizer.DSDintroText,
                                     text=TTLocalizer.DisplaySettingsIntro,
                                     text_wordwrap=TTLocalizer.DSDintroTextWordwrap,
                                     text_align=TextNode.ALeft,
                                     pos=(-0.72499999999999998,
                                          0,
                                          0.29999999999999999))
        self.introTextSimple = DirectLabel(parent=self,
                                           relief=None,
                                           scale=0.059999999999999998,
                                           text=TTLocalizer.DisplaySettingsIntroSimple,
                                           text_wordwrap=25,
                                           text_align=TextNode.ALeft,
                                           pos=(-0.72499999999999998,
                                                0,
                                                0.29999999999999999))
        self.apiLabel = DirectLabel(parent=self,
                                    relief=None,
                                    scale=0.059999999999999998,
                                    text=TTLocalizer.DisplaySettingsApi,
                                    text_align=TextNode.ARight,
                                    pos=(-0.080000000000000002,
                                         0,
                                         0))
        self.apiMenu = DirectOptionMenu(
            parent=self,
            relief=DGG.RAISED,
            scale=0.059999999999999998,
            items=['x'],
            pos=(
                0,
                0,
                0))
        self.screenSizeLabel = DirectLabel(parent=self,
                                           relief=None,
                                           scale=0.059999999999999998,
                                           text=TTLocalizer.DisplaySettingsResolution,
                                           text_align=TextNode.ARight,
                                           pos=(-0.080000000000000002,
                                                0,
                                                -0.10000000000000001))
        self.screenSizeLeftArrow = DirectButton(
            parent=self,
            relief=None,
            image=(
                gui.find('**/Horiz_Arrow_UP'),
                gui.find('**/Horiz_Arrow_DN'),
                gui.find('**/Horiz_Arrow_Rllvr'),
                gui.find('**/Horiz_Arrow_UP')),
            scale=(
                -1.0,
                1.0,
                1.0),
            pos=(
                0.040000000000000001,
                0,
                -0.085000000000000006),
            command=self._DisplaySettingsDialog__doScreenSizeLeft)
        self.screenSizeRightArrow = DirectButton(
            parent=self,
            relief=None,
            image=(
                gui.find('**/Horiz_Arrow_UP'),
                gui.find('**/Horiz_Arrow_DN'),
                gui.find('**/Horiz_Arrow_Rllvr'),
                gui.find('**/Horiz_Arrow_UP')),
            pos=(
                0.54000000000000004,
                0,
                -0.085000000000000006),
            command=self._DisplaySettingsDialog__doScreenSizeRight)
        self.screenSizeValueText = DirectLabel(
            parent=self,
            relief=None,
            text='x',
            text_align=TextNode.ACenter,
            text_scale=0.059999999999999998,
            pos=(
                0.28999999999999998,
                0,
                -0.10000000000000001))
        self.windowedButton = DirectCheckButton(
            parent=self,
            relief=None,
            text=TTLocalizer.DisplaySettingsWindowed,
            text_align=TextNode.ALeft,
            text_scale=0.59999999999999998,
            scale=0.10000000000000001,
            boxImage=innerCircle,
            boxImageScale=2.5,
            boxImageColor=VBase4(
                0,
                0.25,
                0.5,
                1),
            boxRelief=None,
            pos=TTLocalizer.DSDwindowedButtonPos,
            command=self._DisplaySettingsDialog__doWindowed)
        self.fullscreenButton = DirectCheckButton(
            parent=self,
            relief=None,
            text=TTLocalizer.DisplaySettingsFullscreen,
            text_align=TextNode.ALeft,
            text_scale=0.59999999999999998,
            scale=0.10000000000000001,
            boxImage=innerCircle,
            boxImageScale=2.5,
            boxImageColor=VBase4(
                0,
                0.25,
                0.5,
                1),
            boxRelief=None,
            pos=TTLocalizer.DSDfullscreenButtonPos,
            command=self._DisplaySettingsDialog__doFullscreen)
        self.embeddedButton = DirectCheckButton(
            parent=self,
            relief=None,
            text=TTLocalizer.DisplaySettingsEmbedded,
            text_align=TextNode.ALeft,
            text_scale=0.59999999999999998,
            scale=0.10000000000000001,
            boxImage=innerCircle,
            boxImageScale=2.5,
            boxImageColor=VBase4(
                0,
                0.25,
                0.5,
                1),
            boxRelief=None,
            pos=TTLocalizer.DSDembeddedButtonPos,
            command=self._DisplaySettingsDialog__doEmbedded)
        self.apply = DirectButton(
            parent=self,
            relief=None,
            image=(
                guiButton.find('**/QuitBtn_UP'),
                guiButton.find('**/QuitBtn_DN'),
                guiButton.find('**/QuitBtn_RLVR')),
            image_scale=(
                0.59999999999999998,
                1,
                1),
            text=TTLocalizer.DisplaySettingsApply,
            text_scale=0.059999999999999998,
            text_pos=(
                0,
                -0.02),
            pos=(
                0.52000000000000002,
                0,
                -0.53000000000000003),
            command=self._DisplaySettingsDialog__apply)
        self.cancel = DirectButton(
            parent=self,
            relief=None,
            text=TTLocalizer.DisplaySettingsCancel,
            image=(
                guiButton.find('**/QuitBtn_UP'),
                guiButton.find('**/QuitBtn_DN'),
                guiButton.find('**/QuitBtn_RLVR')),
            image_scale=(
                0.59999999999999998,
                1,
                1),
            text_scale=TTLocalizer.DSDcancel,
            text_pos=TTLocalizer.DSDcancelPos,
            pos=(
                0.20000000000000001,
                0,
                -0.53000000000000003),
            command=self._DisplaySettingsDialog__cancel)
        guiButton.removeNode()
        gui.removeNode()
        nameShopGui.removeNode()
        innerCircle.removeNode()
        self.hide()

    def enter(self, changeDisplaySettings, changeDisplayAPI):
        if self.isEntered == 1:
            return None

        self.isEntered = 1
        if self.isLoaded == 0:
            self.load()

        self.applyDialog = None
        self.timeoutDialog = None
        self.restoreDialog = None
        self.revertDialog = None
        base.transitions.fadeScreen(0.5)
        properties = base.win.getProperties()
        self.screenSizeIndex = self.chooseClosestScreenSize(
            properties.getXSize(), properties.getYSize())
        self.isFullscreen = properties.getFullscreen()
        if self.isCurrentlyEmbedded():
            self.displayMode = self.EmbeddedMode
        elif self.isFullscreen:
            self.displayMode = self.FullscreenMode
        else:
            self.displayMode = self.WindowedMode
        self.updateApiMenu(changeDisplaySettings, changeDisplayAPI)
        self.updateWindowed()
        self.updateScreenSize()
        if changeDisplaySettings:
            self.introText.show()
            self.introTextSimple.hide()
            if changeDisplayAPI and len(self.apis) > 1:
                self.apiLabel.show()
                self.apiMenu.show()
            else:
                self.apiLabel.hide()
                self.apiMenu.hide()
            if DisplayOptions.isWindowedPossible():
                self.c1b.show()
                self.windowedButton.show()
            else:
                self.c1b.hide()
                self.windowedButton.hide()
            self.c2b.show()
            self.fullscreenButton.show()
            if DisplayOptions.isEmbeddedPossible():
                self.c3b.show()
                self.embeddedButton.show()
            else:
                self.c3b.hide()
                self.embeddedButton.hide()
        else:
            self.introText.hide()
            self.introTextSimple.show()
            self.apiLabel.hide()
            self.apiMenu.hide()
            self.windowedButton.hide()
            self.fullscreenButton.hide()
            self.c1b.hide()
            self.c2b.hide()
            self.c3b.hide()
        self.anyChanged = 0
        self.apiChanged = 0
        self.show()

    def exit(self):
        if self.isEntered == 0:
            return None

        self.isEntered = 0
        self.cleanupDialogs()
        base.transitions.noTransitions()
        taskMgr.remove(self.TimeoutCountdownTask)
        self.ignoreAll()
        self.hide()
        messenger.send(self.doneEvent, [
            self.anyChanged,
            self.apiChanged])

    def cleanupDialogs(self):
        if self.applyDialog is not None:
            self.applyDialog.cleanup()
            self.applyDialog = None

        if self.timeoutDialog is not None:
            self.timeoutDialog.cleanup()
            self.timeoutDialog = None

        if self.restoreDialog is not None:
            self.restoreDialog.cleanup()
            self.restoreDialog = None

        if self.revertDialog is not None:
            self.revertDialog.cleanup()
            self.revertDialog = None

    def updateApiMenu(self, changeDisplaySettings, changeDisplayAPI):
        self.apis = []
        self.apiPipes = []
        if changeDisplayAPI:
            base.makeAllPipes()

        for pipe in base.pipeList:
            if pipe.isValid():
                self.apiPipes.append(pipe)
                self.apis.append(pipe.getInterfaceName())
                continue

        self.apiMenu['items'] = self.apis
        self.apiMenu.set(base.pipe.getInterfaceName())

    def updateWindowed(self):
        if self.displayMode == self.FullscreenMode:
            self.windowedButton['indicatorValue'] = 0
            self.fullscreenButton['indicatorValue'] = 1
            self.embeddedButton['indicatorValue'] = 0
        elif self.displayMode == self.WindowedMode:
            self.windowedButton['indicatorValue'] = 1
            self.fullscreenButton['indicatorValue'] = 0
            self.embeddedButton['indicatorValue'] = 0
        elif self.displayMode == self.EmbeddedMode:
            self.windowedButton['indicatorValue'] = 0
            self.fullscreenButton['indicatorValue'] = 0
            self.embeddedButton['indicatorValue'] = 1

    def updateScreenSize(self):
        (xSize, ySize) = self.screenSizes[self.screenSizeIndex]
        self.screenSizeValueText['text'] = '%s x %s' % (xSize, ySize)
        if self.screenSizeIndex > 0:
            self.screenSizeLeftArrow.show()
        else:
            self.screenSizeLeftArrow.hide()
        if self.screenSizeIndex < len(self.screenSizes) - 1:
            self.screenSizeRightArrow.show()
        else:
            self.screenSizeRightArrow.hide()

    def chooseClosestScreenSize(self, currentXSize, currentYSize):
        for i in range(len(self.screenSizes)):
            (xSize, ySize) = self.screenSizes[i]
            if currentXSize == xSize and currentYSize == ySize:
                return i
                continue

        currentCount = currentXSize * currentYSize
        bestDiff = None
        bestI = None
        for i in range(len(self.screenSizes)):
            (xSize, ySize) = self.screenSizes[i]
            diff = abs(xSize * ySize - currentCount)
            if bestI is None or diff < bestDiff:
                bestI = i
                bestDiff = diff
                continue

        return bestI

    def _DisplaySettingsDialog__doWindowed(self, value):
        self.displayMode = self.WindowedMode
        self.updateWindowed()

    def _DisplaySettingsDialog__doFullscreen(self, value):
        self.displayMode = self.FullscreenMode
        self.updateWindowed()

    def _DisplaySettingsDialog__doEmbedded(self, value):
        self.displayMode = self.EmbeddedMode
        self.updateWindowed()

    def _DisplaySettingsDialog__doScreenSizeLeft(self):
        if self.screenSizeIndex > 0:
            self.screenSizeIndex = self.screenSizeIndex - 1
            self.updateScreenSize()

    def _DisplaySettingsDialog__doScreenSizeRight(self):
        if self.screenSizeIndex < len(self.screenSizes) - 1:
            self.screenSizeIndex = self.screenSizeIndex + 1
            self.updateScreenSize()

    def _DisplaySettingsDialog__apply(self):
        self.cleanupDialogs()
        self.clearBin()
        self.applyDialog = TTDialog.TTDialog(
            dialogName='DisplaySettingsApply',
            style=TTDialog.TwoChoice,
            text=TTLocalizer.DisplaySettingsApplyWarning %
            self.ApplyTimeoutSeconds,
            text_wordwrap=15,
            command=self._DisplaySettingsDialog__applyDone)
        self.applyDialog.setBin('gui-popup', 0)

    def _DisplaySettingsDialog__applyDone(self, command):
        self.applyDialog.cleanup()
        self.applyDialog = None
        self.setBin('gui-popup', 0)
        base.transitions.fadeScreen(0.5)
        if command != DGG.DIALOG_OK:
            return None

        self.origPipe = base.pipe
        self.origProperties = base.win.getProperties()
        pipe = self.apiPipes[self.apiMenu.selectedIndex]
        properties = WindowProperties()
        (xSize, ySize) = self.screenSizes[self.screenSizeIndex]
        properties.setSize(xSize, ySize)
        properties.setFullscreen(self.displayMode == self.FullscreenMode)
        fullscreen = self.displayMode == self.FullscreenMode
        embedded = self.displayMode == self.EmbeddedMode
        if embedded:
            if DisplayOptions.isEmbeddedPossible():
                pass
            else:
                self.notify.warning(
                    'how was the player able to choose embedded')
                embedded = False

        if not self.changeDisplayProperties(
                pipe, xSize, ySize, fullscreen, embedded):
            self._DisplaySettingsDialog__revertBack(1)
            return None

        self.clearBin()
        self.timeoutDialog = TTDialog.TTDialog(
            dialogName='DisplaySettingsTimeout',
            style=TTDialog.TwoChoice,
            text=TTLocalizer.DisplaySettingsAccept %
            self.ApplyTimeoutSeconds,
            text_wordwrap=15,
            command=self._DisplaySettingsDialog__timeoutDone)
        self.timeoutDialog.setBin('gui-popup', 0)
        self.timeoutRemaining = self.ApplyTimeoutSeconds
        self.timeoutStart = None
        taskMgr.add(
            self._DisplaySettingsDialog__timeoutCountdown,
            self.TimeoutCountdownTask)

    def changeDisplayProperties(
            self,
            pipe,
            width,
            height,
            fullscreen=False,
            embedded=False):
        result = False
        self.notify.info('changeDisplayProperties')
        if embedded:
            if DisplayOptions.isEmbeddedPossible():
                width = base.appRunner.windowProperties.getXSize()
                height = base.appRunner.windowProperties.getYSize()

        self.current_pipe = base.pipe
        self.current_properties = WindowProperties(base.win.getProperties())
        properties = self.current_properties
        self.notify.debug('DISPLAY PREVIOUS:')
        self.notify.debug(
            '  EMBEDDED:   %s' %
            bool(
                properties.getParentWindow()))
        self.notify.debug(
            '  FULLSCREEN: %s' %
            bool(
                properties.getFullscreen()))
        self.notify.debug('  X SIZE:     %s' % properties.getXSize())
        self.notify.debug('  Y SIZE:     %s' % properties.getYSize())
        self.notify.debug('DISPLAY REQUESTED:')
        self.notify.debug('  EMBEDDED:   %s' % bool(embedded))
        self.notify.debug('  FULLSCREEN: %s' % bool(fullscreen))
        self.notify.debug('  X SIZE:     %s' % width)
        self.notify.debug('  Y SIZE:     %s' % height)
        if self.current_pipe == pipe and bool(self.current_properties.getParentWindow()) == bool(embedded) and self.current_properties.getFullscreen(
        ) == fullscreen and self.current_properties.getXSize() == width and self.current_properties.getYSize() == height:
            self.notify.info('DISPLAY NO CHANGE REQUIRED')
            state = True
        else:
            properties = WindowProperties()
            properties.setSize(width, height)
            properties.setFullscreen(fullscreen)
            properties.setParentWindow(0)
            if embedded:
                properties = base.appRunner.windowProperties

            original_sort = base.win.getSort()
            lastShader = base.cr.getLastShader()
            base.cr.useShader(None)
            if self.resetDisplayProperties(pipe, properties):
                self.notify.debug('DISPLAY CHANGE SET')
                properties = base.win.getProperties()
                self.notify.debug('DISPLAY ACHIEVED:')
                self.notify.debug(
                    '  EMBEDDED:   %s' %
                    bool(
                        properties.getParentWindow()))
                self.notify.debug(
                    '  FULLSCREEN: %s' %
                    bool(
                        properties.getFullscreen()))
                self.notify.debug('  X SIZE:     %s' % properties.getXSize())
                self.notify.debug('  Y SIZE:     %s' % properties.getYSize())
                if bool(properties.getParentWindow()) == bool(embedded) and properties.getFullscreen(
                ) == fullscreen and properties.getXSize() == width and properties.getYSize() == height:
                    self.notify.info('DISPLAY CHANGE VERIFIED')
                    result = True
                else:
                    self.notify.warning(
                        'DISPLAY CHANGE FAILED, RESTORING PREVIOUS DISPLAY')
            else:
                self.notify.warning('DISPLAY CHANGE FAILED')
            base.cr.useShader(lastShader)
            base.win.setSort(original_sort)
            base.graphicsEngine.renderFrame()
            base.graphicsEngine.renderFrame()
        return result

    def _DisplaySettingsDialog__timeoutCountdown(self, task):
        if self.timeoutStart is None:
            self.timeoutStart = globalClock.getRealTime()

        elapsed = int(globalClock.getFrameTime() - self.timeoutStart)
        remaining = max(self.ApplyTimeoutSeconds - elapsed, 0)
        if remaining < self.timeoutRemaining:
            self.timeoutRemaining = remaining
            self.timeoutDialog['text'] = (
                TTLocalizer.DisplaySettingsAccept %
                remaining,)

        if remaining == 0:
            self._DisplaySettingsDialog__timeoutDone('cancel')
            return Task.done

        return Task.cont

    def _DisplaySettingsDialog__timeoutDone(self, command):
        taskMgr.remove(self.TimeoutCountdownTask)
        self.timeoutDialog.cleanup()
        self.timeoutDialog = None
        self.setBin('gui-popup', 0)
        base.transitions.fadeScreen(0.5)
        if command == DGG.DIALOG_OK:
            self.anyChanged = 1
            self.exit()
            return None

        self._DisplaySettingsDialog__revertBack(0)

    def _DisplaySettingsDialog__revertBack(self, reason):
        if not self.resetDisplayProperties(self.origPipe, self.origProperties):
            self.notify.warning("Couldn't restore original display settings!")
            base.panda3dRenderError()

        self.clearBin()
        if reason == 0:
            revertText = TTLocalizer.DisplaySettingsRevertUser
        else:
            revertText = TTLocalizer.DisplaySettingsRevertFailed
        self.revertDialog = TTDialog.TTDialog(
            dialogName='DisplaySettingsRevert',
            style=TTDialog.Acknowledge,
            text=revertText,
            text_wordwrap=15,
            command=self._DisplaySettingsDialog__revertDone)
        self.revertDialog.setBin('gui-popup', 0)

    def _DisplaySettingsDialog__revertDone(self, command):
        self.revertDialog.cleanup()
        self.revertDialog = None
        self.setBin('gui-popup', 0)
        base.transitions.fadeScreen(0.5)

    def _DisplaySettingsDialog__cancel(self):
        self.exit()

    def resetDisplayProperties(self, pipe, properties):
        if base.win:
            currentProperties = base.win.getProperties()
            gsg = base.win.getGsg()
        else:
            currentProperties = WindowProperties.getDefault()
            gsg = None
        newProperties = WindowProperties(currentProperties)
        newProperties.addProperties(properties)
        if base.pipe != pipe:
            self.apiChanged = 1
            gsg = None

        if gsg is None and currentProperties.getFullscreen() != newProperties.getFullscreen(
        ) or currentProperties.getParentWindow() != newProperties.getParentWindow():
            self.notify.debug('window properties: %s' % properties)
            self.notify.debug('gsg: %s' % gsg)
            base.pipe = pipe
            if not base.openMainWindow(
                    props=properties, gsg=gsg, keepCamera=True):
                self.notify.warning('OPEN MAIN WINDOW FAILED')
                return 0

            self.notify.info('OPEN MAIN WINDOW PASSED')
            base.disableShowbaseMouse()
            NametagGlobals.setCamera(base.cam)
            NametagGlobals.setMouseWatcher(base.mouseWatcherNode)
            base.graphicsEngine.renderFrame()
            base.graphicsEngine.renderFrame()
            base.graphicsEngine.openWindows()
            if base.win.isClosed():
                self.notify.info('Window did not open, removing.')
                base.closeWindow(base.win)
                return 0

        else:
            self.notify.debug('Adjusting properties')
            base.win.requestProperties(properties)
            base.graphicsEngine.renderFrame()
        return 1

    def isCurrentlyEmbedded(self):
        result = False
        if base.win.getProperties().getParentWindow():
            result = True

        return result
