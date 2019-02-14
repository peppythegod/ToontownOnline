from toontown.estate import PlantingGUI
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from direct.task import Task
from toontown.estate import GardenGlobals
from toontown.estate import DistributedToonStatuary
from direct.interval.IntervalGlobal import *
from direct.gui.DirectScrolledList import *
from toontown.toon import Toon
from toontown.toon import DistributedToon
from direct.distributed import DistributedObject


class ToonStatueSelectionGUI(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'ToonStatueSelectionGUI')

    def __init__(self, doneEvent, specialBoxActive=False):
        base.tssGUI = self
        instructions = TTLocalizer.GardeningChooseToonStatue
        instructionsPos = (0, 0.40000000000000002)
        DirectFrame.__init__(
            self,
            relief=None,
            state='normal',
            geom=DGG.getDefaultDialogGeom(),
            geom_color=ToontownGlobals.GlobalDialogColor,
            geom_scale=(1.5, 1.0, 1.0),
            frameSize=(-1, 1, -1, 1),
            pos=(0, 0, 0),
            text=instructions,
            text_wordwrap=18,
            text_scale=0.080000000000000002,
            text_pos=instructionsPos)
        self.initialiseoptions(ToonStatueSelectionGUI)
        self.doneEvent = doneEvent
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        okImageList = (buttons.find('**/ChtBx_OKBtn_UP'),
                       buttons.find('**/ChtBx_OKBtn_DN'),
                       buttons.find('**/ChtBx_OKBtn_Rllvr'))
        cancelImageList = (buttons.find('**/CloseBtn_UP'),
                           buttons.find('**/CloseBtn_DN'),
                           buttons.find('**/CloseBtn_Rllvr'))
        self.cancelButton = DirectButton(
            parent=self,
            relief=None,
            image=cancelImageList,
            pos=(-0.29999999999999999, 0, -0.34999999999999998),
            text=TTLocalizer.PlantingGuiCancel,
            text_scale=0.059999999999999998,
            text_pos=(0, -0.10000000000000001),
            command=self._ToonStatueSelectionGUI__cancel)
        self.okButton = DirectButton(
            parent=self,
            relief=None,
            image=okImageList,
            pos=(0.29999999999999999, 0, -0.34999999999999998),
            text=TTLocalizer.PlantingGuiOk,
            text_scale=0.059999999999999998,
            text_pos=(0, -0.10000000000000001),
            command=self._ToonStatueSelectionGUI__accept)
        buttons.removeNode()
        self.ffList = []
        self.friends = {}
        self.doId2Dna = {}
        self.textRolloverColor = Vec4(1, 1, 0, 1)
        self.textDownColor = Vec4(0.5, 0.90000000000000002, 1, 1)
        self.textDisabledColor = Vec4(0.40000000000000002, 0.80000000000000004,
                                      0.40000000000000002, 1)
        self.createFriendsList()

    def destroy(self):
        self.doneEvent = None
        self.previewToon.delete()
        self.previewToon = None
        for ff in self.ffList:
            self.friends[ff].destroy()

        self.ffList = []
        self.friends = {}
        self.doId2Dna = {}
        self.scrollList.destroy()
        DirectFrame.destroy(self)

    def _ToonStatueSelectionGUI__cancel(self):
        messenger.send(self.doneEvent, [0, '', -1])
        messenger.send('wakeup')

    def _ToonStatueSelectionGUI__accept(self):
        messenger.send(self.doneEvent, [
            1, '',
            DistributedToonStatuary.dnaCodeFromToonDNA(self.dnaSelected)
        ])
        messenger.send('wakeup')

    def createFriendsList(self):
        self._ToonStatueSelectionGUI__makeFFlist()
        if len(self.ffList) > 0:
            gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
            self.scrollList = DirectScrolledList(
                parent=self,
                relief=None,
                incButton_image=(gui.find('**/FndsLst_ScrollUp'),
                                 gui.find('**/FndsLst_ScrollDN'),
                                 gui.find('**/FndsLst_ScrollUp_Rllvr'),
                                 gui.find('**/FndsLst_ScrollUp')),
                incButton_relief=None,
                incButton_pos=(0.0, 0.0, -0.316),
                incButton_image1_color=Vec4(1.0, 0.90000000000000002,
                                            0.40000000000000002, 1.0),
                incButton_image3_color=Vec4(1.0, 1.0, 0.59999999999999998,
                                            0.5),
                incButton_scale=(1.0, 1.0, -1.0),
                decButton_image=(gui.find('**/FndsLst_ScrollUp'),
                                 gui.find('**/FndsLst_ScrollDN'),
                                 gui.find('**/FndsLst_ScrollUp_Rllvr'),
                                 gui.find('**/FndsLst_ScrollUp')),
                decButton_relief=None,
                decButton_pos=(0.0, 0.0, 0.11700000000000001),
                decButton_image1_color=Vec4(1.0, 1.0, 0.59999999999999998,
                                            1.0),
                decButton_image3_color=Vec4(1.0, 1.0, 0.59999999999999998,
                                            0.59999999999999998),
                itemFrame_pos=(-0.17000000000000001, 0.0,
                               0.059999999999999998),
                itemFrame_relief=DGG.SUNKEN,
                itemFrame_frameSize=(-0.01, 0.34999999999999998,
                                     -0.34999999999999998,
                                     0.040000000000000001),
                itemFrame_frameColor=(0.84999999999999998, 0.94999999999999996,
                                      1, 1),
                itemFrame_borderWidth=(0.01, 0.01),
                numItemsVisible=8,
                itemFrame_scale=1.0,
                items=[])
            gui.removeNode()
            self.scrollList.setPos(0.34999999999999998, 0, 0.125)
            self.scrollList.setScale(1.25)
            clipper = PlaneNode('clipper')
            clipper.setPlane(
                Plane(Vec3(-1, 0, 0), Point3(0.17000000000000001, 0, 0)))
            clipNP = self.scrollList.attachNewNode(clipper)
            self.scrollList.setClipPlane(clipNP)
            self._ToonStatueSelectionGUI__makeScrollList()

    def checkFamily(self, doId):
        test = 0
        for familyMember in base.cr.avList:
            if familyMember.id == doId:
                test = 1
                continue

        return test

    def _ToonStatueSelectionGUI__makeFFlist(self):
        playerAvatar = (base.localAvatar.doId, base.localAvatar.name,
                        NametagGroup.CCNonPlayer)
        self.ffList.append(playerAvatar)
        self.dnaSelected = base.localAvatar.style
        self.createPreviewToon(self.dnaSelected)
        for familyMember in base.cr.avList:
            if familyMember.id != base.localAvatar.doId:
                newFF = (familyMember.id, familyMember.name,
                         NametagGroup.CCNonPlayer)
                self.ffList.append(newFF)
                continue

        for friendPair in base.localAvatar.friendsList:
            (friendId, flags) = friendPair
            handle = base.cr.identifyFriend(friendId)
            if handle and not self.checkFamily(friendId):
                if hasattr(handle, 'getName'):
                    colorCode = NametagGroup.CCSpeedChat
                    if flags & ToontownGlobals.FriendChat:
                        colorCode = NametagGroup.CCFreeChat

                    newFF = (friendPair[0], handle.getName(), colorCode)
                    self.ffList.append(newFF)
                else:
                    self.notify.warning('Bad Handle for getName in makeFFlist')
            hasattr(handle, 'getName')

    def _ToonStatueSelectionGUI__makeScrollList(self):
        for ff in self.ffList:
            ffbutton = self.makeFamilyButton(ff[0], ff[1], ff[2])
            if ffbutton:
                self.scrollList.addItem(ffbutton, refresh=0)
                self.friends[ff] = ffbutton
                continue

        self.scrollList.refresh()

    def makeFamilyButton(self, familyId, familyName, colorCode):
        fg = NametagGlobals.getNameFg(colorCode, PGButton.SInactive)
        return DirectButton(
            relief=None,
            text=familyName,
            text_scale=0.040000000000000001,
            text_align=TextNode.ALeft,
            text_fg=fg,
            text1_bg=self.textDownColor,
            text2_bg=self.textRolloverColor,
            text3_fg=self.textDisabledColor,
            textMayChange=0,
            command=self._ToonStatueSelectionGUI__chooseFriend,
            extraArgs=[familyId, familyName])

    def _ToonStatueSelectionGUI__chooseFriend(self, friendId, friendName):
        messenger.send('wakeup')
        if self.checkFamily(friendId):
            if friendId == base.localAvatar.doId:
                self.createPreviewToon(base.localAvatar.style)
            elif friendId in self.doId2Dna:
                self.createPreviewToon(self.doId2Dna[friendId])
            else:
                familyAvatar = DistributedToon.DistributedToon(base.cr)
                familyAvatar.doId = friendId
                familyAvatar.forceAllowDelayDelete()
                base.cr.getAvatarDetails(
                    familyAvatar,
                    self._ToonStatueSelectionGUI__handleFamilyAvatar,
                    'DistributedToon')
        else:
            friend = base.cr.identifyFriend(friendId)
            if friend:
                self.createPreviewToon(friend.style)

    def _ToonStatueSelectionGUI__handleFamilyAvatar(self, gotData, avatar,
                                                    dclass):
        self.doId2Dna[avatar.doId] = avatar.style
        self.createPreviewToon(avatar.style)
        avatar.delete()

    def createPreviewToon(self, dna):
        if hasattr(self, 'previewToon'):
            self.previewToon.delete()

        self.dnaSelected = dna
        self.previewToon = Toon.Toon()
        self.previewToon.setDNA(dna)
        self.previewToon.loop('neutral')
        self.previewToon.setH(180)
        self.previewToon.setPos(-0.29999999999999999, 0, -0.29999999999999999)
        self.previewToon.setScale(0.13)
        self.previewToon.reparentTo(self)
        self.previewToon.startBlink()
        self.previewToon.startLookAround()
        self.previewToon.getGeomNode().setDepthWrite(1)
        self.previewToon.getGeomNode().setDepthTest(1)
