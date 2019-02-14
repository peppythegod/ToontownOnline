from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toontowngui import TTDialog


class ElevatorNotifier:
    notify = DirectNotifyGlobal.directNotify.newCategory('CatalogNotifyDialog')

    def __init__(self):
        self.frame = None

    def handleButton(self):
        self._ElevatorNotifier__handleButton(1)

    def createFrame(self,
                    message,
                    framePos=None,
                    withStopping=True,
                    ttDialog=False):
        if not framePos:
            framePos = (0.0, 0, 0.78000000000000003)

        if not ttDialog:
            self.frame = DirectFrame(
                relief=None,
                image=DGG.getDefaultDialogGeom(),
                image_color=ToontownGlobals.GlobalDialogColor,
                image_scale=(1.0, 1.0, 0.40000000000000002),
                text=message,
                text_wordwrap=16,
                text_scale=0.059999999999999998,
                text_pos=(-0.0, 0.10000000000000001),
                pos=framePos)
        else:
            self.frame = TTDialog.TTDialog(
                relief=None,
                image=DGG.getDefaultDialogGeom(),
                image_color=ToontownGlobals.GlobalDialogColor,
                image_scale=(1.0, 1.0, 0.40000000000000002),
                text=message,
                text_wordwrap=16,
                text_scale=0.059999999999999998,
                text_pos=(-0.0, 0.10000000000000001),
                pos=framePos)
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        self.cancelImageList = (buttons.find('**/CloseBtn_UP'),
                                buttons.find('**/CloseBtn_DN'),
                                buttons.find('**/CloseBtn_Rllvr'))
        self.okImageList = (buttons.find('**/ChtBx_OKBtn_UP'),
                            buttons.find('**/ChtBx_OKBtn_DN'),
                            buttons.find('**/ChtBx_OKBtn_Rllvr'))
        self.doneButton = DirectButton(
            parent=self.frame,
            relief=None,
            image=self.cancelImageList,
            command=self.handleButton,
            pos=(0, 0, -0.14000000000000001))
        if not withStopping:
            self.doneButton[
                'command'] = self._ElevatorNotifier__handleButtonWithoutStopping

        self.doneButton.show()
        self.frame.show()

    def cleanup(self):
        if self.frame:
            self.frame.destroy()

        self.frame = None
        self.nextButton = None
        self.doneButton = None
        self.okImageList = None
        self.cancelImageList = None

    def setOkButton(self):
        self.doneButton['image'] = self.okImageList

    def setCancelButton(self):
        self.doneButton['image'] = self.cancelImageList

    def _ElevatorNotifier__handleButton(self, value):
        self.cleanup()
        place = base.cr.playGame.getPlace()
        if place:
            place.setState('walk')

    def showMe(self, message, pos=None, ttDialog=False):
        if self.frame == None:
            place = base.cr.playGame.getPlace()
            if place:
                self.createFrame(message, pos, True, ttDialog)
                place.setState('stopped')

    def showMeWithoutStopping(self, message, pos=None, ttDialog=False):
        if self.frame == None:
            self.createFrame(message, pos, False, ttDialog)

    def _ElevatorNotifier__handleButtonWithoutStopping(self):
        self.cleanup()

    def isNotifierOpen(self):
        if self.frame:
            return True
        else:
            return False
