from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import TextNode
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TTDialog
from otp.otpgui.OTPDialog import *
from direct.interval.LerpInterval import LerpPosInterval, LerpScaleInterval, LerpFunc
from direct.interval.IntervalGlobal import Sequence, Parallel, Func, Wait
from direct.task import Task
import random


class ToontownLoadingBlocker(TTDialog.TTDialog):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'ToontownLoadingBlocker')

    def __init__(self, avList):
        if not self._ToontownLoadingBlocker__shouldShowBlocker(avList):
            return None

        TTDialog.TTDialog.__init__(self)
        gui = loader.loadModel('phase_3/models/gui/tt_m_gui_pat_mainGui')
        img = gui.find('**/tt_t_gui_pat_loadingPopup')
        self['image'] = img
        self['image_scale'] = (1, 0, 1)
        self['image_pos'] = (0, 0, -0.40000000000000002)
        gui.removeNode()
        self.loadingTextChangeTimer = 10.0
        self.loadingTextTimerVariant = 3.0
        self.loadingTextFreezeTime = 3.0
        self.toonTipChangeTimer = 20.0
        self.hideBlockerIval = None
        self.canChangeLoadingText = True
        self._ToontownLoadingBlocker__setupLoadingBar()
        self._ToontownLoadingBlocker__createTitleText()
        self._ToontownLoadingBlocker__createToonTip()
        self._ToontownLoadingBlocker__createLoadingText()
        self._ToontownLoadingBlocker__showBlocker()
        self.accept(
            'phaseComplete-4',
            self._ToontownLoadingBlocker__shrinkLoadingBar)
        self.accept(
            'launcherPercentPhaseComplete',
            self._ToontownLoadingBlocker__update)

    def destroy(self):
        taskMgr.remove('changeLoadingTextTask')
        taskMgr.remove('canChangeLoadingTextTask')
        taskMgr.remove('changeToonTipTask')
        self.ignore('phaseComplete-4')
        self.ignore('launcherPercentPhaseComplete')
        self._ToontownLoadingBlocker__cleanupHideBlockerIval()
        self.title.destroy()
        self.title = None
        self.loadingText.destroy()
        self.loadingText = None
        self.loadingTextList = None
        self.toonTipText.destroy()
        self.toonTipText = None
        self.bar.destroy()
        self.bar = None
        TTDialog.TTDialog.destroy(self)

    def _ToontownLoadingBlocker__hideBlocker(self):
        self.hide()
        if self._ToontownLoadingBlocker__isValidDownloadBar():
            base.downloadWatcher.text.show()

    def _ToontownLoadingBlocker__showBlocker(self):
        self.show()
        if self._ToontownLoadingBlocker__isValidDownloadBar():
            base.downloadWatcher.text.hide()

    def _ToontownLoadingBlocker__setupLoadingBar(self):
        self.bar = DirectWaitBar(
            parent=self, guiId='DownloadBlockerBar', pos=(
                0, 0, -0.31380000000000002), relief=DGG.SUNKEN, frameSize=(
                -0.59999999999999998, 0.59999999999999998, -0.10000000000000001, 0.10000000000000001), borderWidth=(
                0.02, 0.02), scale=(
                    0.80000000000000004, 0.80000000000000004, 0.5), range=100, sortOrder=5000, frameColor=(
                        0.5, 0.5, 0.5, 0.5), barColor=(
                            0.20000000000000001, 0.69999999999999996, 0.20000000000000001, 0.5), text='0%', text_scale=(
                                0.080000000000000002, 0.128), text_fg=(
                                    1, 1, 1, 1), text_align=TextNode.ACenter, text_pos=(
                                        0, -0.035000000000000003))
        self.bar.setBin('gui-popup', 1)
        if self._ToontownLoadingBlocker__isValidDownloadBar():
            base.downloadWatcher.bar.hide()

    def _ToontownLoadingBlocker__resetLoadingBar(self):
        self.bar.clearBin()
        if self._ToontownLoadingBlocker__isValidDownloadBar():
            base.downloadWatcher.bar.show()

    def _ToontownLoadingBlocker__isValidDownloadBar(self):
        if hasattr(base, 'downloadWatcher') and base.downloadWatcher:
            if hasattr(
                    base.downloadWatcher,
                    'bar') and base.downloadWatcher.bar:
                return True

        return False

    def _ToontownLoadingBlocker__createTitleText(self):
        self.title = DirectLabel(
            parent=self,
            relief=None,
            guiId='BlockerTitle',
            pos=(
                0,
                0,
                0.38),
            text=TTLocalizer.BlockerTitle,
            text_font=ToontownGlobals.getSignFont(),
            text_fg=(
                1,
                0.90000000000000002,
                0.10000000000000001,
                1),
            text_align=TextNode.ACenter,
            text_scale=0.10000000000000001,
            textMayChange=1,
            sortOrder=50)

    def _ToontownLoadingBlocker__createLoadingText(self):
        self.loadingText = DirectLabel(
            parent=self,
            relief=None,
            guiId='BlockerLoadingText',
            pos=(
                0,
                0,
                -0.23569999999999999),
            text='',
            text_fg=(
                1,
                1,
                1,
                1),
            text_scale=0.055,
            textMayChange=1,
            text_align=TextNode.ACenter,
            sortOrder=50)
        self.loadingTextList = TTLocalizer.BlockerLoadingTexts
        self._ToontownLoadingBlocker__changeLoadingText()
        taskMgr.doMethodLater(
            self.loadingTextChangeTimer,
            self._ToontownLoadingBlocker__changeLoadingTextTask,
            'changeLoadingTextTask')

    def _ToontownLoadingBlocker__changeLoadingText(self):

        def getLoadingText():
            listLen = len(self.loadingTextList)
            if listLen > 0:
                randomIndex = random.randrange(listLen)
                randomLoadingText = self.loadingTextList.pop(randomIndex)
                return randomLoadingText
            else:
                self.loadingTextList = TTLocalizer.BlockerLoadingTexts

        if self.canChangeLoadingText:
            self.loadingText['text'] = getLoadingText()
            self.canChangeLoadingText = False
            taskMgr.doMethodLater(
                self.loadingTextFreezeTime,
                self._ToontownLoadingBlocker__canChangeLoadingTextTask,
                'canChangeLoadingTextTask')

    def _ToontownLoadingBlocker__changeLoadingTextTask(self, task):
        self._ToontownLoadingBlocker__changeLoadingText()
        randVariation = random.uniform(-(self.loadingTextTimerVariant),
                                       self.loadingTextTimerVariant)
        task.delayTime = self.loadingTextChangeTimer + randVariation
        return task.again

    def _ToontownLoadingBlocker__canChangeLoadingTextTask(self, task):
        self.canChangeLoadingText = True
        return task.done

    def _ToontownLoadingBlocker__createToonTip(self):
        self.toonTipText = DirectLabel(
            parent=self,
            relief=None,
            guiId='BlockerToonTip',
            pos=(
                0,
                0,
                -0.46879999999999999),
            text='',
            text_fg=(
                1,
                1,
                1,
                1),
            text_scale=0.050000000000000003,
            textMayChange=1,
            text_align=TextNode.ACenter,
            text_wordwrap=32,
            sortOrder=50)
        self._ToontownLoadingBlocker__changeToonTip()
        taskMgr.doMethodLater(
            self.toonTipChangeTimer,
            self._ToontownLoadingBlocker__changeToonTipTask,
            'changeToonTipTask')

    def _ToontownLoadingBlocker__changeToonTip(self):

        def getTip(tipCategory):
            return TTLocalizer.TipTitle + '\n' + \
                random.choice(TTLocalizer.TipDict.get(tipCategory))

        self.toonTipText['text'] = getTip(TTLocalizer.TIP_GENERAL)

    def _ToontownLoadingBlocker__changeToonTipTask(self, task):
        self._ToontownLoadingBlocker__changeToonTip()
        return task.again

    def _ToontownLoadingBlocker__shouldShowBlocker(self, avList):

        def hasPlayableToon(avList):
            if len(avList) > 0:
                if base.cr.isPaid():
                    return True
                else:
                    for av in avList:
                        if av.position == 1:
                            return True
                            continue

            return False

        if hasPlayableToon(avList):
            if not base.launcher.getPhaseComplete(
                    3.5) and base.launcher.getPhaseComplete(4):
                return True

        return False

    def _ToontownLoadingBlocker__shrinkLoadingBar(self):
        if self._ToontownLoadingBlocker__isValidDownloadBar():
            ivalDuration = 0.5
            barPosIval = LerpPosInterval(
                self.bar, ivalDuration, (-0.81000000000000005, 0, -0.95999999999999996))
            barScaleIval = LerpScaleInterval(
                self.bar, ivalDuration, (0.25, 0.25, 0.25))

            def posText(pos):
                self.bar['text_pos'] = (0, pos)

            def scaleText(scale):
                self.bar['text_scale'] = (scale, scale)

            textScaleIval = LerpFunc(
                scaleText,
                fromData=0.080000000000000002,
                toData=0.16,
                duration=ivalDuration)
            textPosIval = LerpFunc(
                posText,
                fromData=-0.035000000000000003,
                toData=-0.050000000000000003,
                duration=ivalDuration)
            shrinkIval = Parallel(
                barPosIval,
                barScaleIval,
                textPosIval,
                textScaleIval,
                Func(
                    self.loadingText.hide))
            self.hideBlockerIval = Sequence(
                shrinkIval, Wait(0.5), Func(
                    self._ToontownLoadingBlocker__hideBlocker), Func(
                    self._ToontownLoadingBlocker__resetLoadingBar), Func(
                    self.destroy))
            self.hideBlockerIval.start()

    def _ToontownLoadingBlocker__cleanupHideBlockerIval(self):
        if self.hideBlockerIval:
            self.hideBlockerIval.finish()
            self.hideBlockerIval = None

    def _ToontownLoadingBlocker__update(
            self, phase, percent, reqByteRate, actualByteRate):
        if self._ToontownLoadingBlocker__isValidDownloadBar():
            percent = base.downloadWatcher.bar['value']
            self.bar['text'] = '%s %%' % percent
            self.bar['value'] = percent

        if percent == 0:
            self._ToontownLoadingBlocker__changeLoadingText()
