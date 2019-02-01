from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.toontowngui import TeaserPanel


class TrialerForceAcknowledge:

    def __init__(self, doneEvent):
        self.doneEvent = doneEvent
        self.dialog = None

    def enter(self, destHood):
        doneStatus = {}

        def letThrough(self=self, doneStatus=doneStatus):
            doneStatus['mode'] = 'pass'
            messenger.send(self.doneEvent, [
                doneStatus])

        if not base.restrictTrialers:
            letThrough()
            return None

        if base.roamingTrialers:
            letThrough()
            return None

        if base.cr.isPaid():
            letThrough()
            return None

        if ZoneUtil.getCanonicalHoodId(destHood) in (
                ToontownGlobals.ToontownCentral,
                ToontownGlobals.MyEstate,
                ToontownGlobals.GoofySpeedway):
            letThrough()
            return None
        else:

            try:
                base.localAvatar.b_setAnimState('neutral', 1)
            except BaseException:
                pass

        doneStatus['mode'] = 'fail'
        self.doneStatus = doneStatus
        self.dialog = TeaserPanel.TeaserPanel(
            pageName='otherHoods', doneFunc=self.handleOk)

    def exit(self):
        if self.dialog:
            self.dialog.cleanup()
            self.dialog.unload()
            self.dialog = None

    def handleOk(self):
        messenger.send(self.doneEvent, [
            self.doneStatus])
