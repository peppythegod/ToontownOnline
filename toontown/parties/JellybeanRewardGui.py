from pandac.PandaModules import TextNode
from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectLabel
from direct.gui import DirectGuiGlobals
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer


class JellybeanRewardGui(DirectFrame):
    notify = directNotify.newCategory('JellybeanRewardGui')
    PreCountdownDelay = 1.0
    CountDownRate = 0.20000000000000001
    JarLabelTextColor = (0.94999999999999996, 0.94999999999999996, 0.0, 1.0)
    JarLabelMaxedTextColor = (1.0, 0.0, 0.0, 1.0)

    def __init__(self, doneEvent):
        self.doneEvent = doneEvent
        DirectFrame.__init__(self)
        self.reparentTo(aspect2d)
        self.setPos(0.0, 0.0, 0.16)
        self.stash()
        publicPartyGui = loader.loadModel(
            'phase_4/models/parties/publicPartyGUI')
        self.frame = DirectFrame(
            parent=self,
            geom=publicPartyGui.find('**/activities_background'),
            geom_pos=(-0.80000000000000004, 0.0, 0.20000000000000001),
            geom_scale=2.0,
            relief=None)
        self.earnedLabel = DirectLabel(
            parent=self,
            relief=None,
            text=str(0),
            text_align=TextNode.ACenter,
            text_pos=(0.0, -0.070000000000000007),
            text_scale=0.20000000000000001,
            text_fg=(0.94999999999999996, 0.94999999999999996, 0.0, 1.0),
            text_font=ToontownGlobals.getSignFont(),
            textMayChange=True,
            image=DirectGuiGlobals.getDefaultDialogGeom(),
            image_scale=(0.33000000000000002, 1.0, 0.33000000000000002),
            pos=(-0.29999999999999999, 0.0, 0.20000000000000001),
            scale=0.90000000000000002)
        purchaseModels = loader.loadModel('phase_4/models/gui/purchase_gui')
        jarImage = purchaseModels.find('**/Jar')
        self.jarLabel = DirectLabel(
            parent=self,
            relief=None,
            text=str(0),
            text_align=TextNode.ACenter,
            text_pos=(0.0, -0.070000000000000007),
            text_scale=0.20000000000000001,
            text_fg=JellybeanRewardGui.JarLabelTextColor,
            text_font=ToontownGlobals.getSignFont(),
            textMayChange=True,
            image=jarImage,
            scale=0.69999999999999996,
            pos=(0.29999999999999999, 0.0, 0.17000000000000001))
        purchaseModels.removeNode()
        del purchaseModels
        jarImage.removeNode()
        del jarImage
        self.messageLabel = DirectLabel(
            parent=self,
            relief=None,
            text='',
            text_align=TextNode.ALeft,
            text_wordwrap=16.0,
            text_scale=0.070000000000000007,
            pos=(-0.52000000000000002, 0.0, -0.10000000000000001),
            textMayChange=True)
        self.doubledJellybeanLabel = DirectLabel(
            parent=self,
            relief=None,
            text=TTLocalizer.PartyRewardDoubledJellybean,
            text_align=TextNode.ACenter,
            text_wordwrap=12.0,
            text_scale=0.089999999999999997,
            text_fg=(1.0, 0.125, 0.125, 1.0),
            pos=(0.0, 0.0, -0.46500000000000002),
            textMayChange=False)
        self.doubledJellybeanLabel.hide()
        self.closeButton = DirectButton(
            parent=self,
            relief=None,
            text=TTLocalizer.PartyJellybeanRewardOK,
            text_align=TextNode.ACenter,
            text_scale=0.065000000000000002,
            text_pos=(0.0, -0.625),
            geom=(publicPartyGui.find('**/startButton_up'),
                  publicPartyGui.find('**/startButton_down'),
                  publicPartyGui.find('**/startButton_rollover'),
                  publicPartyGui.find('**/startButton_inactive')),
            geom_pos=(-0.39000000000000001, 0.0, 0.125),
            command=self._close)
        publicPartyGui.removeNode()
        del publicPartyGui
        self.countSound = base.loadSfx(
            'phase_13/audio/sfx/tick_counter_short.mp3')
        self.overMaxSound = base.loadSfx(
            'phase_13/audio/sfx/tick_counter_overflow.mp3')

    def showReward(self, earnedAmount, jarAmount, message):
        JellybeanRewardGui.notify.debug(
            'showReward( earnedAmount=%d, jarAmount=%d, ...)' % (earnedAmount,
                                                                 jarAmount))
        self.earnedCount = earnedAmount
        self.earnedLabel['text'] = str(self.earnedCount)
        self.jarCount = jarAmount
        self.jarMax = base.localAvatar.getMaxMoney()
        self.jarLabel['text'] = str(self.jarCount)
        self.jarLabel['text_fg'] = JellybeanRewardGui.JarLabelTextColor
        self.messageLabel['text'] = message
        if base.cr.newsManager.isHolidayRunning(
                ToontownGlobals.JELLYBEAN_DAY
        ) and base.cr.newsManager.isHolidayRunning(
                ToontownGlobals.JELLYBEAN_PARTIES_HOLIDAY
        ) or base.cr.newsManager.isHolidayRunning(
                ToontownGlobals.JELLYBEAN_PARTIES_HOLIDAY_MONTH):
            self.doubledJellybeanLabel.show()
        else:
            self.doubledJellybeanLabel.hide()
        self.unstash()
        taskMgr.doMethodLater(
            JellybeanRewardGui.PreCountdownDelay,
            self.transferOneJellybean,
            'JellybeanRewardGuiTransferOneJellybean',
            extraArgs=[])

    def transferOneJellybean(self):
        if self.earnedCount == 0:
            return None

        self.earnedCount -= 1
        self.earnedLabel['text'] = str(self.earnedCount)
        self.jarCount += 1
        if self.jarCount <= self.jarMax:
            self.jarLabel['text'] = str(self.jarCount)
        elif self.jarCount > self.jarMax:
            self.jarLabel[
                'text_fg'] = JellybeanRewardGui.JarLabelMaxedTextColor

        if self.jarCount <= self.jarMax:
            base.playSfx(self.countSound)
        else:
            base.playSfx(self.overMaxSound)
        taskMgr.doMethodLater(
            JellybeanRewardGui.CountDownRate,
            self.transferOneJellybean,
            'JellybeanRewardGuiTransferOneJellybean',
            extraArgs=[])

    def _close(self):
        taskMgr.remove('JellybeanRewardGuiTransferOneJellybean')
        self.stash()
        messenger.send(self.doneEvent)

    def destroy(self):
        taskMgr.remove('JellybeanRewardGuiTransferOneJellybean')
        del self.countSound
        del self.overMaxSound
        self.frame.destroy()
        self.earnedLabel.destroy()
        self.jarLabel.destroy()
        self.messageLabel.destroy()
        self.closeButton.destroy()
        DirectFrame.destroy(self)
