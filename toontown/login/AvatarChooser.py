from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
import AvatarChoice
from direct.fsm import StateData
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.launcher import DownloadForceAcknowledge
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from toontown.toonbase import DisplayOptions
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
import random
MAX_AVATARS = 6
POSITIONS = (Vec3(-0.840167, 0, 0.35933300000000001), Vec3(0.0093334899999999998, 0, 0.306533), Vec3(0.86199999999999999, 0, 0.32929999999999998),
             Vec3(-0.86355400000000004, 0, -0.44565900000000003), Vec3(0.0099999900000000003, 0, -0.5181), Vec3(0.86490699999999998, 0, -0.44565900000000003))
COLORS = (
    Vec4(
        0.91700000000000004, 0.16400000000000001, 0.16400000000000001, 1), Vec4(
            0.152, 0.75, 0.25800000000000001, 1), Vec4(
                0.59799999999999998, 0.40200000000000002, 0.875, 1), Vec4(
                    0.13300000000000001, 0.58999999999999997, 0.97699999999999998, 1), Vec4(
                        0.89500000000000002, 0.34799999999999998, 0.60199999999999998, 1), Vec4(
                            0.97699999999999998, 0.81599999999999995, 0.13300000000000001, 1))
chooser_notify = DirectNotifyGlobal.directNotify.newCategory('AvatarChooser')


class AvatarChooser(StateData.StateData):

    def __init__(self, avatarList, parentFSM, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        self.choice = None
        self.avatarList = avatarList
        self.displayOptions = None
        self.fsm = ClassicFSM.ClassicFSM('AvatarChooser', [
            State.State('Choose', self.enterChoose, self.exitChoose, [
                'CheckDownload']),
            State.State('CheckDownload', self.enterCheckDownload, self.exitCheckDownload, [
                'Choose'])], 'Choose', 'Choose')
        self.fsm.enterInitialState()
        self.parentFSM = parentFSM
        self.parentFSM.getCurrentState().addChild(self.fsm)

    def enter(self):
        self.notify.info('AvatarChooser.enter')
        if not self.displayOptions:
            self.displayOptions = DisplayOptions.DisplayOptions()

        self.notify.info(
            'calling self.displayOptions.restrictToEmbedded(False)')
        if base.appRunner:
            self.displayOptions.loadFromSettings()
            self.displayOptions.restrictToEmbedded(False)

        if self.isLoaded == 0:
            self.load()

        base.disableMouse()
        self.title.reparentTo(aspect2d)
        self.quitButton.show()
        if base.cr.loginInterface.supportsRelogin():
            self.logoutButton.show()

        self.pickAToonBG.reparentTo(base.camera)
        choice = base.config.GetInt('auto-avatar-choice', -1)
        for panel in self.panelList:
            panel.show()
            self.accept(panel.doneEvent, self._AvatarChooser__handlePanelDone)
            if panel.position == choice and panel.mode == AvatarChoice.AvatarChoice.MODE_CHOOSE:
                self._AvatarChooser__handlePanelDone(
                    'chose', panelChoice=choice)
                continue

    def exit(self):
        if self.isLoaded == 0:
            return None

        for panel in self.panelList:
            panel.hide()

        self.ignoreAll()
        self.title.reparentTo(hidden)
        self.quitButton.hide()
        self.logoutButton.hide()
        self.pickAToonBG.reparentTo(hidden)

    def load(self, isPaid):
        if self.isLoaded == 1:
            return None

        self.isPaid = isPaid
        gui = loader.loadModel('phase_3/models/gui/pick_a_toon_gui')
        gui2 = loader.loadModel('phase_3/models/gui/quit_button')
        newGui = loader.loadModel('phase_3/models/gui/tt_m_gui_pat_mainGui')
        self.pickAToonBG = newGui.find('**/tt_t_gui_pat_background')
        self.pickAToonBG.reparentTo(hidden)
        self.pickAToonBG.setPos(0.0, 2.73, 0.0)
        self.pickAToonBG.setScale(1, 1, 1)
        self.title = OnscreenText(
            TTLocalizer.AvatarChooserPickAToon,
            scale=TTLocalizer.ACtitle,
            parent=hidden,
            font=ToontownGlobals.getSignFont(),
            fg=(
                1,
                0.90000000000000002,
                0.10000000000000001,
                1),
            pos=(
                0.0,
                0.81999999999999995))
        quitHover = gui.find('**/QuitBtn_RLVR')
        self.quitButton = DirectButton(
            image=(
                quitHover,
                quitHover,
                quitHover),
            relief=None,
            text=TTLocalizer.AvatarChooserQuit,
            text_font=ToontownGlobals.getSignFont(),
            text_fg=(
                0.97699999999999998,
                0.81599999999999995,
                0.13300000000000001,
                1),
            text_pos=TTLocalizer.ACquitButtonPos,
            text_scale=TTLocalizer.ACquitButton,
            image_scale=1,
            image1_scale=1.05,
            image2_scale=1.05,
            scale=1.05,
            pos=(
                1.0800000000000001,
                0,
                -0.90700000000000003),
            command=self._AvatarChooser__handleQuit)
        self.logoutButton = DirectButton(
            relief=None,
            image=(
                quitHover,
                quitHover,
                quitHover),
            text=TTLocalizer.OptionsPageLogout,
            text_font=ToontownGlobals.getSignFont(),
            text_fg=(
                0.97699999999999998,
                0.81599999999999995,
                0.13300000000000001,
                1),
            text_scale=TTLocalizer.AClogoutButton,
            text_pos=(
                0,
                -0.035000000000000003),
            pos=(
                -1.1699999999999999,
                0,
                -0.91400000000000003),
            image_scale=1.1499999999999999,
            image1_scale=1.1499999999999999,
            image2_scale=1.1799999999999999,
            scale=0.5,
            command=self._AvatarChooser__handleLogoutWithoutConfirm)
        self.logoutButton.hide()
        gui.removeNode()
        gui2.removeNode()
        newGui.removeNode()
        self.panelList = []
        used_position_indexs = []
        for av in self.avatarList:
            if base.cr.isPaid():
                okToLockout = 0
            else:
                okToLockout = 1
                if av.position in AvatarChoice.AvatarChoice.OLD_TRIALER_OPEN_POS:
                    okToLockout = 0

            panel = AvatarChoice.AvatarChoice(
                av, position=av.position, paid=isPaid, okToLockout=okToLockout)
            panel.setPos(POSITIONS[av.position])
            used_position_indexs.append(av.position)
            self.panelList.append(panel)

        for panelNum in range(0, MAX_AVATARS):
            if panelNum not in used_position_indexs:
                panel = AvatarChoice.AvatarChoice(
                    position=panelNum, paid=isPaid)
                panel.setPos(POSITIONS[panelNum])
                self.panelList.append(panel)
                continue

        if len(self.avatarList) > 0:
            self.initLookAtInfo()

        self.isLoaded = 1

    def getLookAtPosition(self, toonHead, toonidx):
        lookAtChoice = random.random()
        if len(self.used_panel_indexs) == 1:
            lookFwdPercent = 0.33000000000000002
            lookAtOthersPercent = 0
        else:
            lookFwdPercent = 0.20000000000000001
            if len(self.used_panel_indexs) == 2:
                lookAtOthersPercent = 0.40000000000000002
            else:
                lookAtOthersPercent = 0.65000000000000002
        lookRandomPercent = 1.0 - lookFwdPercent - lookAtOthersPercent
        if lookAtChoice < lookFwdPercent:
            self.IsLookingAt[toonidx] = 'f'
            return Vec3(0, 1.5, 0)
        elif lookAtChoice < lookRandomPercent + lookFwdPercent or len(self.used_panel_indexs) == 1:
            self.IsLookingAt[toonidx] = 'r'
            return toonHead.getRandomForwardLookAtPoint()
        else:
            other_toon_idxs = []
            for i in range(len(self.IsLookingAt)):
                if self.IsLookingAt[i] == toonidx:
                    other_toon_idxs.append(i)
                    continue

            if len(other_toon_idxs) == 1:
                IgnoreStarersPercent = 0.40000000000000002
            else:
                IgnoreStarersPercent = 0.20000000000000001
            NoticeStarersPercent = 0.5
            bStareTargetTurnsToMe = 0
            if len(other_toon_idxs) == 0 or random.random(
            ) < IgnoreStarersPercent:
                other_toon_idxs = []
                for i in self.used_panel_indexs:
                    if i != toonidx:
                        other_toon_idxs.append(i)
                        continue

                if random.random() < NoticeStarersPercent:
                    bStareTargetTurnsToMe = 1

            if len(other_toon_idxs) == 0:
                return toonHead.getRandomForwardLookAtPoint()
            else:
                lookingAtIdx = random.choice(other_toon_idxs)
            if bStareTargetTurnsToMe:
                self.IsLookingAt[lookingAtIdx] = toonidx
                otherToonHead = None
                for panel in self.panelList:
                    if panel.position == lookingAtIdx:
                        otherToonHead = panel.headModel
                        continue

                otherToonHead.doLookAroundToStareAt(
                    otherToonHead, self.getLookAtToPosVec(
                        lookingAtIdx, toonidx))

            self.IsLookingAt[toonidx] = lookingAtIdx
            return self.getLookAtToPosVec(toonidx, lookingAtIdx)

    def getLookAtToPosVec(self, fromIdx, toIdx):
        x = -(POSITIONS[toIdx][0] - POSITIONS[fromIdx][0])
        y = POSITIONS[toIdx][1] - POSITIONS[fromIdx][1]
        z = POSITIONS[toIdx][2] - POSITIONS[fromIdx][2]
        return Vec3(x, y, z)

    def initLookAtInfo(self):
        self.used_panel_indexs = []
        for panel in self.panelList:
            if panel.dna is not None:
                self.used_panel_indexs.append(panel.position)
                continue

        if len(self.used_panel_indexs) == 0:
            return None

        self.IsLookingAt = []
        for i in range(MAX_AVATARS):
            self.IsLookingAt.append('f')

        for panel in self.panelList:
            if panel.dna is not None:
                panel.headModel.setLookAtPositionCallbackArgs(
                    (self, panel.headModel, panel.position))
                continue

    def unload(self):
        if self.isLoaded == 0:
            return None

        cleanupDialog('globalDialog')
        for panel in self.panelList:
            panel.destroy()

        del self.panelList
        self.title.removeNode()
        del self.title
        self.quitButton.destroy()
        del self.quitButton
        self.logoutButton.destroy()
        del self.logoutButton
        self.pickAToonBG.removeNode()
        del self.pickAToonBG
        del self.avatarList
        self.parentFSM.getCurrentState().removeChild(self.fsm)
        del self.parentFSM
        del self.fsm
        self.ignoreAll()
        self.isLoaded = 0
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()

    def _AvatarChooser__handlePanelDone(self, panelDoneStatus, panelChoice=0):
        self.doneStatus = {}
        self.doneStatus['mode'] = panelDoneStatus
        self.choice = panelChoice
        if panelDoneStatus == 'chose':
            self._AvatarChooser__handleChoice()
        elif panelDoneStatus == 'nameIt':
            self._AvatarChooser__handleCreate()
        elif panelDoneStatus == 'delete':
            self._AvatarChooser__handleDelete()
        elif panelDoneStatus == 'create':
            self._AvatarChooser__handleCreate()

    def getChoice(self):
        return self.choice

    def _AvatarChooser__handleChoice(self):
        self.fsm.request('CheckDownload')

    def _AvatarChooser__handleCreate(self):
        base.transitions.fadeOut(finishIval=EventInterval(self.doneEvent, [
            self.doneStatus]))

    def _AvatarChooser__handleDelete(self):
        messenger.send(self.doneEvent, [
            self.doneStatus])

    def _AvatarChooser__handleQuit(self):
        cleanupDialog('globalDialog')
        self.doneStatus = {
            'mode': 'exit'}
        messenger.send(self.doneEvent, [
            self.doneStatus])

    def enterChoose(self):
        pass

    def exitChoose(self):
        pass

    def enterCheckDownload(self):
        self.accept('downloadAck-response',
                    self._AvatarChooser__handleDownloadAck)
        self.downloadAck = DownloadForceAcknowledge.DownloadForceAcknowledge(
            'downloadAck-response')
        self.downloadAck.enter(4)

    def exitCheckDownload(self):
        self.downloadAck.exit()
        self.downloadAck = None
        self.ignore('downloadAck-response')

    def _AvatarChooser__handleDownloadAck(self, doneStatus):
        if doneStatus['mode'] == 'complete':
            base.transitions.fadeOut(finishIval=EventInterval(self.doneEvent, [
                self.doneStatus]))
        else:
            self.fsm.request('Choose')

    def _AvatarChooser__handleLogoutWithoutConfirm(self):
        base.cr.loginFSM.request('login')
