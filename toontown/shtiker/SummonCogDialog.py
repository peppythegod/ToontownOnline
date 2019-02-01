from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TTDialog
from toontown.toonbase import ToontownGlobals
from toontown.suit import SuitDNA
from toontown.suit import Suit
from toontown.battle import SuitBattleGlobals
from toontown.toon import NPCToons
TTL = TTLocalizer


class SummonCogDialog(DirectFrame, StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('SummonCogDialog')
    notify.setInfo(True)

    def __init__(self, suitIndex):
        DirectFrame.__init__(
            self,
            parent=aspect2dp,
            pos=(
                0,
                0,
                0.29999999999999999),
            relief=None,
            image=DGG.getDefaultDialogGeom(),
            image_scale=(
                1.6000000000000001,
                1,
                0.69999999999999996),
            image_pos=(
                0,
                0,
                0.17999999999999999),
            image_color=ToontownGlobals.GlobalDialogColor,
            text=TTL.SummonDlgTitle,
            text_scale=0.12,
            text_pos=(
                0,
                0.40000000000000002),
            borderWidth=(
                0.01,
                0.01),
            sortOrder=NO_FADE_SORT_INDEX)
        StateData.StateData.__init__(self, 'summon-cog-done')
        self.initialiseoptions(SummonCogDialog)
        self.suitIndex = suitIndex
        base.summonDialog = self
        self.popup = None
        self.suitName = SuitDNA.suitHeadTypes[self.suitIndex]
        self.suitFullName = SuitBattleGlobals.SuitAttributes[self.suitName]['name']

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
        gui = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        self.head = Suit.attachSuitHead(self, self.suitName)
        z = self.head.getZ()
        self.head.setPos(-0.40000000000000002, -
                         0.10000000000000001, z + 0.20000000000000001)
        self.suitLabel = DirectLabel(parent=self,
                                     relief=None,
                                     text=self.suitFullName,
                                     text_font=ToontownGlobals.getSuitFont(),
                                     pos=(-0.40000000000000002,
                                          0,
                                          0),
                                     scale=0.070000000000000007)
        closeButtonImage = (
            gui.find('**/CloseBtn_UP'),
            gui.find('**/CloseBtn_DN'),
            gui.find('**/CloseBtn_Rllvr'))
        buttonImage = (
            guiButton.find('**/QuitBtn_UP'),
            guiButton.find('**/QuitBtn_DN'),
            guiButton.find('**/QuitBtn_RLVR'))
        disabledColor = Vec4(0.5, 0.5, 0.5, 1)
        self.summonSingleButton = DirectButton(
            parent=self,
            relief=None,
            text=TTL.SummonDlgButton1,
            image=buttonImage,
            image_scale=(
                1.7,
                1,
                1),
            image3_color=disabledColor,
            text_scale=0.059999999999999998,
            text_pos=(
                0,
                -0.01),
            pos=(
                0.29999999999999999,
                0,
                0.25),
            command=self.issueSummons,
            extraArgs=['single'])
        self.summonBuildingButton = DirectButton(
            parent=self,
            relief=None,
            text=TTL.SummonDlgButton2,
            image=buttonImage,
            image_scale=(
                1.7,
                1,
                1),
            image3_color=disabledColor,
            text_scale=0.059999999999999998,
            text_pos=(
                0,
                -0.01),
            pos=(
                0.29999999999999999,
                0,
                0.125),
            command=self.issueSummons,
            extraArgs=['building'])
        self.summonInvasionButton = DirectButton(
            parent=self,
            relief=None,
            text=TTL.SummonDlgButton3,
            image=buttonImage,
            image_scale=(
                1.7,
                1,
                1),
            image3_color=disabledColor,
            text_scale=0.059999999999999998,
            text_pos=(
                0,
                -0.01),
            pos=(
                0.29999999999999999,
                0,
                0.0),
            command=self.issueSummons,
            extraArgs=['invasion'])
        self.statusLabel = DirectLabel(
            parent=self, relief=None, text='', text_wordwrap=12, pos=(
                0.29999999999999999, 0, 0.25), scale=0.070000000000000007)
        self.cancel = DirectButton(parent=self, relief=None, image=closeButtonImage, pos=(
            0.69999999999999996, 0, -0.10000000000000001), command=self._SummonCogDialog__cancel)
        gui.removeNode()
        guiButton.removeNode()
        self.hide()

    def enter(self):
        if self.isEntered == 1:
            return None

        self.isEntered = 1
        if self.isLoaded == 0:
            self.load()

        self.disableButtons()
        self.enableButtons()
        self.popup = None
        base.transitions.fadeScreen(0.5)
        self.show()

    def exit(self):
        if self.isEntered == 0:
            return None

        self.isEntered = 0
        self.cleanupDialogs()
        base.transitions.noTransitions()
        self.ignoreAll()
        self.hide()
        messenger.send(self.doneEvent, [])

    def cleanupDialogs(self):
        self.head = None
        if self.popup is not None:
            self.popup.cleanup()
            self.popup = None

    def cogSummonsDone(self, returnCode, suitIndex, buildingId):
        self.cancel['state'] = DGG.NORMAL
        if self.summonsType == 'single':
            if returnCode == 'success':
                self.statusLabel['text'] = TTL.SummonDlgSingleSuccess
            elif returnCode == 'badlocation':
                self.statusLabel['text'] = TTL.SummonDlgSingleBadLoc
            elif returnCode == 'fail':
                self.statusLabel['text'] = TTL.SummonDlgInvasionFail

        elif self.summonsType == 'building':
            if returnCode == 'success':
                building = base.cr.doId2do.get(buildingId)
                dnaStore = base.cr.playGame.dnaStore
                buildingTitle = dnaStore.getTitleFromBlockNumber(
                    building.block)
                buildingInteriorZone = building.zoneId + 500 + building.block
                npcName = TTLocalizer.SummonDlgShopkeeper
                npcId = NPCToons.zone2NpcDict.get(buildingInteriorZone)
                if npcId:
                    npcName = NPCToons.getNPCName(npcId[0])

                if buildingTitle:
                    self.statusLabel['text'] = TTL.SummonDlgBldgSuccess % (
                        npcName, buildingTitle)
                else:
                    self.statusLabel['text'] = TTL.SummonDlgBldgSuccess2
            elif returnCode == 'badlocation':
                self.statusLabel['text'] = TTL.SummonDlgBldgBadLoc
            elif returnCode == 'fail':
                self.statusLabel['text'] = TTL.SummonDlgInvasionFail

        elif self.summonsType == 'invasion':
            if returnCode == 'success':
                self.statusLabel['text'] = TTL.SummonDlgInvasionSuccess
            elif returnCode == 'busy':
                self.statusLabel['text'] = TTL.SummonDlgInvasionBusy % self.suitFullName
            elif returnCode == 'fail':
                self.statusLabel['text'] = TTL.SummonDlgInvasionFail

    def hideSummonButtons(self):
        self.summonSingleButton.hide()
        self.summonBuildingButton.hide()
        self.summonInvasionButton.hide()

    def issueSummons(self, summonsType):
        if summonsType == 'single':
            text = TTL.SummonDlgSingleConf
        elif summonsType == 'building':
            text = TTL.SummonDlgBuildingConf
        elif summonsType == 'invasion':
            text = TTL.SummonDlgInvasionConf

        text = text % self.suitFullName

        def handleResponse(resp):
            self.popup.cleanup()
            self.popup = None
            self.reparentTo(self.getParent(), NO_FADE_SORT_INDEX)
            base.transitions.fadeScreen(0.5)
            if resp == DGG.DIALOG_OK:
                self.notify.info(
                    'issuing %s summons for %s' %
                    (summonsType, self.suitIndex))
                self.accept('cog-summons-response', self.cogSummonsDone)
                self.summonsType = summonsType
                self.doIssueSummonsText()
                base.localAvatar.d_reqCogSummons(
                    self.summonsType, self.suitIndex)
                self.hideSummonButtons()
                self.cancel['state'] = DGG.DISABLED

        self.reparentTo(self.getParent(), 0)
        self.popup = TTDialog.TTDialog(
            parent=aspect2dp,
            style=TTDialog.YesNo,
            text=text,
            fadeScreen=1,
            command=handleResponse)

    def doIssueSummonsText(self):
        self.disableButtons()
        self.statusLabel['text'] = TTL.SummonDlgDelivering

    def disableButtons(self):
        self.summonSingleButton['state'] = DGG.DISABLED
        self.summonBuildingButton['state'] = DGG.DISABLED
        self.summonInvasionButton['state'] = DGG.DISABLED

    def enableButtons(self):
        if base.localAvatar.hasCogSummons(self.suitIndex, 'single'):
            self.summonSingleButton['state'] = DGG.NORMAL

        if base.localAvatar.hasCogSummons(self.suitIndex, 'building'):
            self.summonBuildingButton['state'] = DGG.NORMAL

        if base.localAvatar.hasCogSummons(self.suitIndex, 'invasion'):
            self.summonInvasionButton['state'] = DGG.NORMAL

    def _SummonCogDialog__cancel(self):
        self.exit()
