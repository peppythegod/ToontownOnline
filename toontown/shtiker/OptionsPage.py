from pandac.PandaModules import *
import ShtikerPage
from toontown.toontowngui import TTDialog
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
import DisplaySettingsDialog
from direct.task import Task
from otp.speedchat import SpeedChat
from otp.speedchat import SCColorScheme
from otp.speedchat import SCStaticTextTerminal
from direct.showbase import PythonUtil
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
speedChatStyles = ((2000, (200 / 255.0, 60 / 255.0, 229 / 255.0),
                    (200 / 255.0, 135 / 255.0, 255 / 255.0),
                    (220 / 255.0, 195 / 255.0,
                     229 / 255.0)), (2001, (0 / 255.0, 0 / 255.0, 255 / 255.0),
                                     (140 / 255.0, 150 / 255.0, 235 / 255.0),
                                     (201 / 255.0, 215 / 255.0, 255 / 255.0)),
                   (2002, (90 / 255.0, 175 / 255.0, 225 / 255.0),
                    (120 / 255.0, 215 / 255.0,
                     255 / 255.0), (208 / 255.0, 230 / 255.0, 250 / 255.0)),
                   (2003, (130 / 255.0, 235 / 255.0, 235 / 255.0),
                    (120 / 255.0, 225 / 255.0,
                     225 / 255.0), (234 / 255.0, 255 / 255.0, 255 / 255.0)),
                   (2004, (0 / 255.0, 200 / 255.0,
                           70 / 255.0), (0 / 255.0, 200 / 255.0, 80 / 255.0),
                    (204 / 255.0, 255 / 255.0,
                     204 / 255.0)), (2005, (235 / 255.0, 230 / 255.0,
                                            0 / 255.0),
                                     (255 / 255.0, 250 / 255.0, 100 / 255.0),
                                     (255 / 255.0, 250 / 255.0, 204 / 255.0)),
                   (2006, (255 / 255.0, 153 / 255.0,
                           0 / 255.0), (229 / 255.0, 147 / 255.0, 0 / 255.0),
                    (255 / 255.0, 234 / 255.0,
                     204 / 255.0)), (2007, (255 / 255.0, 0 / 255.0,
                                            50 / 255.0),
                                     (229 / 255.0, 0 / 255.0, 50 / 255.0),
                                     (255 / 255.0, 204 / 255.0, 204 / 255.0)),
                   (2008, (255 / 255.0, 153 / 255.0, 193 / 255.0),
                    (240 / 255.0, 157 / 255.0, 192 / 255.0),
                    (255 / 255.0, 215 / 255.0,
                     238 / 255.0)), (2009, (170 / 255.0, 120 / 255.0,
                                            20 / 255.0),
                                     (165 / 255.0, 120 / 255.0, 50 / 255.0),
                                     (210 / 255.0, 200 / 255.0, 180 / 255.0)))
visualEffects = ((2050, 'None'), (2051, 'bw'), (2052, 'sepia'))
PageMode = PythonUtil.Enum('Options, Codes')


class OptionsPage(ShtikerPage.ShtikerPage):
    notify = DirectNotifyGlobal.directNotify.newCategory('OptionsPage')

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)

    def load(self):
        ShtikerPage.ShtikerPage.load(self)
        self.optionsTabPage = OptionsTabPage(self)
        self.optionsTabPage.hide()
        self.codesTabPage = CodesTabPage(self)
        self.codesTabPage.hide()
        titleHeight = 0.60999999999999999
        self.title = DirectLabel(
            parent=self,
            relief=None,
            text=TTLocalizer.OptionsPageTitle,
            text_scale=0.12,
            pos=(0, 0, titleHeight))
        normalColor = (1, 1, 1, 1)
        clickColor = (0.80000000000000004, 0.80000000000000004, 0, 1)
        rolloverColor = (0.14999999999999999, 0.81999999999999995, 1.0, 1)
        diabledColor = (1.0, 0.97999999999999998, 0.14999999999999999, 1)
        gui = loader.loadModel('phase_3.5/models/gui/fishingBook')
        self.optionsTab = DirectButton(
            parent=self,
            relief=None,
            text=TTLocalizer.OptionsPageTitle,
            text_scale=TTLocalizer.OPoptionsTab,
            text_align=TextNode.ALeft,
            text_pos=(0.01, 0.0, 0.0),
            image=gui.find('**/tabs/polySurface1'),
            image_pos=(0.55000000000000004, 1, -0.91000000000000003),
            image_hpr=(0, 0, -90),
            image_scale=(0.033000000000000002, 0.033000000000000002,
                         0.035000000000000003),
            image_color=normalColor,
            image1_color=clickColor,
            image2_color=rolloverColor,
            image3_color=diabledColor,
            text_fg=Vec4(0.20000000000000001, 0.10000000000000001, 0, 1),
            command=self.setMode,
            extraArgs=[PageMode.Options],
            pos=(-0.35999999999999999, 0, 0.77000000000000002))
        self.codesTab = DirectButton(
            parent=self,
            relief=None,
            text=TTLocalizer.OptionsPageCodesTab,
            text_scale=TTLocalizer.OPoptionsTab,
            text_align=TextNode.ALeft,
            text_pos=(-0.035000000000000003, 0.0, 0.0),
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
            extraArgs=[PageMode.Codes],
            pos=(0.11, 0, 0.77000000000000002))

    def enter(self):
        self.setMode(PageMode.Options, updateAnyways=1)
        ShtikerPage.ShtikerPage.enter(self)

    def exit(self):
        self.optionsTabPage.exit()
        self.codesTabPage.exit()
        ShtikerPage.ShtikerPage.exit(self)

    def unload(self):
        self.optionsTabPage.unload()
        del self.title
        ShtikerPage.ShtikerPage.unload(self)

    def setMode(self, mode, updateAnyways=0):
        messenger.send('wakeup')
        if not updateAnyways:
            if self.mode == mode:
                return None
            else:
                self.mode = mode

        if mode == PageMode.Options:
            self.mode = PageMode.Options
            self.title['text'] = TTLocalizer.OptionsPageTitle
            self.optionsTab['state'] = DGG.DISABLED
            self.optionsTabPage.enter()
            self.codesTab['state'] = DGG.NORMAL
            self.codesTabPage.exit()
        elif mode == PageMode.Codes:
            self.mode = PageMode.Codes
            self.title['text'] = TTLocalizer.CdrPageTitle
            self.optionsTab['state'] = DGG.NORMAL
            self.optionsTabPage.exit()
            self.codesTab['state'] = DGG.DISABLED
            self.codesTabPage.enter()
        else:
            raise Exception('OptionsPage::setMode - Invalid Mode %s' % mode)


class OptionsTabPage(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('OptionsTabPage')
    DisplaySettingsTaskName = 'save-display-settings'
    DisplaySettingsDelay = 60
    ChangeDisplaySettings = base.config.GetBool('change-display-settings', 1)
    ChangeDisplayAPI = base.config.GetBool('change-display-api', 0)
    DisplaySettingsApiMap = {
        'OpenGL': Settings.GL,
        'DirectX7': Settings.DX7,
        'DirectX8': Settings.DX8
    }

    def __init__(self, parent=aspect2d):
        self.parent = parent
        self.currentSizeIndex = None
        DirectFrame.__init__(
            self,
            parent=self.parent,
            relief=None,
            pos=(0.0, 0.0, 0.0),
            scale=(1.0, 1.0, 1.0))
        self.load()

    def destroy(self):
        self.parent = None
        DirectFrame.destroy(self)

    def load(self):
        self.displaySettings = None
        self.displaySettingsChanged = 0
        self.displaySettingsSize = (None, None)
        self.displaySettingsFullscreen = None
        self.displaySettingsEmbedded = None
        self.displaySettingsApi = None
        self.displaySettingsApiChanged = 0
        self.visualEffectIndex = 0
        wantShaders = config.GetBool('want-shaders', 0)
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        if wantShaders:
            titleHeight = 0.70999999999999996
            textStartHeight = 0.5
            textRowHeight = 0.13500000000000001
        else:
            titleHeight = 0.60999999999999999
            textStartHeight = 0.45000000000000001
            textRowHeight = 0.14499999999999999
        leftMargin = -0.71999999999999997
        buttonbase_xcoord = 0.34999999999999998
        if wantShaders:
            buttonbase_ycoord = 0.5
        else:
            buttonbase_ycoord = 0.45000000000000001
        button_image_scale = (0.69999999999999996, 1, 1)
        button_textpos = (0, -0.02)
        options_text_scale = 0.051999999999999998
        disabled_arrow_color = Vec4(0.59999999999999998, 0.59999999999999998,
                                    0.59999999999999998, 1.0)
        self.speed_chat_scale = 0.055
        self.Music_Label = DirectLabel(
            parent=self,
            relief=None,
            text='',
            text_align=TextNode.ALeft,
            text_scale=options_text_scale,
            pos=(leftMargin, 0, textStartHeight))
        self.SoundFX_Label = DirectLabel(
            parent=self,
            relief=None,
            text='',
            text_align=TextNode.ALeft,
            text_scale=options_text_scale,
            text_wordwrap=16,
            pos=(leftMargin, 0, textStartHeight - textRowHeight))
        self.Friends_Label = DirectLabel(
            parent=self,
            relief=None,
            text='',
            text_align=TextNode.ALeft,
            text_scale=options_text_scale,
            text_wordwrap=16,
            pos=(leftMargin, 0, textStartHeight - 3 * textRowHeight))
        self.Whispers_Label = DirectLabel(
            parent=self,
            relief=None,
            text='',
            text_align=TextNode.ALeft,
            text_scale=options_text_scale,
            text_wordwrap=16,
            pos=(leftMargin, 0, textStartHeight - 4 * textRowHeight))
        self.DisplaySettings_Label = DirectLabel(
            parent=self,
            relief=None,
            text='',
            text_align=TextNode.ALeft,
            text_scale=options_text_scale,
            text_wordwrap=10,
            pos=(leftMargin, 0, textStartHeight - 5 * textRowHeight))
        self.SpeedChatStyle_Label = DirectLabel(
            parent=self,
            relief=None,
            text=TTLocalizer.OptionsPageSpeedChatStyleLabel,
            text_align=TextNode.ALeft,
            text_scale=options_text_scale,
            text_wordwrap=10,
            pos=(leftMargin, 0, textStartHeight - 6 * textRowHeight))
        if wantShaders:
            self.VisualEffect_Label = DirectLabel(
                parent=self,
                relief=None,
                text='Visual Effect',
                text_align=TextNode.ALeft,
                text_scale=options_text_scale,
                text_wordwrap=10,
                pos=(leftMargin, 0, textStartHeight - 7 * textRowHeight))

        self.ToonChatSounds_Label = DirectLabel(
            parent=self,
            relief=None,
            text='',
            text_align=TextNode.ALeft,
            text_scale=options_text_scale,
            text_wordwrap=15,
            pos=(leftMargin, 0,
                 (textStartHeight - 2 * textRowHeight) + 0.025000000000000001))
        self.ToonChatSounds_Label.setScale(0.90000000000000002)
        self.Music_toggleButton = DirectButton(
            parent=self,
            relief=None,
            image=(guiButton.find('**/QuitBtn_UP'),
                   guiButton.find('**/QuitBtn_DN'),
                   guiButton.find('**/QuitBtn_RLVR')),
            image_scale=button_image_scale,
            text='',
            text_scale=options_text_scale,
            text_pos=button_textpos,
            pos=(buttonbase_xcoord, 0.0, buttonbase_ycoord),
            command=self._OptionsTabPage__doToggleMusic)
        self.SoundFX_toggleButton = DirectButton(
            parent=self,
            relief=None,
            image=(guiButton.find('**/QuitBtn_UP'),
                   guiButton.find('**/QuitBtn_DN'),
                   guiButton.find('**/QuitBtn_RLVR')),
            image_scale=button_image_scale,
            text='',
            text_scale=options_text_scale,
            text_pos=button_textpos,
            pos=(buttonbase_xcoord, 0.0, buttonbase_ycoord - textRowHeight),
            command=self._OptionsTabPage__doToggleSfx)
        self.Friends_toggleButton = DirectButton(
            parent=self,
            relief=None,
            image=(guiButton.find('**/QuitBtn_UP'),
                   guiButton.find('**/QuitBtn_DN'),
                   guiButton.find('**/QuitBtn_RLVR')),
            image_scale=button_image_scale,
            text='',
            text_scale=options_text_scale,
            text_pos=button_textpos,
            pos=(buttonbase_xcoord, 0.0,
                 buttonbase_ycoord - textRowHeight * 3),
            command=self._OptionsTabPage__doToggleAcceptFriends)
        self.Whispers_toggleButton = DirectButton(
            parent=self,
            relief=None,
            image=(guiButton.find('**/QuitBtn_UP'),
                   guiButton.find('**/QuitBtn_DN'),
                   guiButton.find('**/QuitBtn_RLVR')),
            image_scale=button_image_scale,
            text='',
            text_scale=options_text_scale,
            text_pos=button_textpos,
            pos=(buttonbase_xcoord, 0.0,
                 buttonbase_ycoord - textRowHeight * 4),
            command=self._OptionsTabPage__doToggleAcceptWhispers)
        self.DisplaySettingsButton = DirectButton(
            parent=self,
            relief=None,
            image=(guiButton.find('**/QuitBtn_UP'),
                   guiButton.find('**/QuitBtn_DN'),
                   guiButton.find('**/QuitBtn_RLVR')),
            image3_color=Vec4(0.5, 0.5, 0.5, 0.5),
            image_scale=button_image_scale,
            text=TTLocalizer.OptionsPageChange,
            text3_fg=(0.5, 0.5, 0.5, 0.75),
            text_scale=options_text_scale,
            text_pos=button_textpos,
            pos=(buttonbase_xcoord, 0.0,
                 buttonbase_ycoord - textRowHeight * 5),
            command=self._OptionsTabPage__doDisplaySettings)
        self.speedChatStyleLeftArrow = DirectButton(
            parent=self,
            relief=None,
            image=(gui.find('**/Horiz_Arrow_UP'),
                   gui.find('**/Horiz_Arrow_DN'),
                   gui.find('**/Horiz_Arrow_Rllvr'),
                   gui.find('**/Horiz_Arrow_UP')),
            image3_color=Vec4(1, 1, 1, 0.5),
            scale=(-1.0, 1.0, 1.0),
            pos=(0.25, 0, buttonbase_ycoord - textRowHeight * 6),
            command=self._OptionsTabPage__doSpeedChatStyleLeft)
        self.speedChatStyleRightArrow = DirectButton(
            parent=self,
            relief=None,
            image=(gui.find('**/Horiz_Arrow_UP'),
                   gui.find('**/Horiz_Arrow_DN'),
                   gui.find('**/Horiz_Arrow_Rllvr'),
                   gui.find('**/Horiz_Arrow_UP')),
            image3_color=Vec4(1, 1, 1, 0.5),
            pos=(0.65000000000000002, 0,
                 buttonbase_ycoord - textRowHeight * 6),
            command=self._OptionsTabPage__doSpeedChatStyleRight)
        if wantShaders:
            self.visualEffectLeftArrow = DirectButton(
                parent=self,
                relief=None,
                image=(gui.find('**/Horiz_Arrow_UP'),
                       gui.find('**/Horiz_Arrow_DN'),
                       gui.find('**/Horiz_Arrow_Rllvr'),
                       gui.find('**/Horiz_Arrow_UP')),
                image3_color=Vec4(1, 1, 1, 0.5),
                scale=(-1.0, 1.0, 1.0),
                pos=(0.25, 0, buttonbase_ycoord - textRowHeight * 7),
                command=self._OptionsTabPage__doVisualEffectLeft)
            self.visualEffectRightArrow = DirectButton(
                parent=self,
                relief=None,
                image=(gui.find('**/Horiz_Arrow_UP'),
                       gui.find('**/Horiz_Arrow_DN'),
                       gui.find('**/Horiz_Arrow_Rllvr'),
                       gui.find('**/Horiz_Arrow_UP')),
                image3_color=Vec4(1, 1, 1, 0.5),
                pos=(0.65000000000000002, 0,
                     buttonbase_ycoord - textRowHeight * 7),
                command=self._OptionsTabPage__doVisualEffectRight)
        else:
            self.visualEffectLeftArrow = None
            self.visualEffectRightArrow = None
        self.ToonChatSounds_toggleButton = DirectButton(
            parent=self,
            relief=None,
            image=(guiButton.find('**/QuitBtn_UP'),
                   guiButton.find('**/QuitBtn_DN'),
                   guiButton.find('**/QuitBtn_RLVR'),
                   guiButton.find('**/QuitBtn_UP')),
            image3_color=Vec4(0.5, 0.5, 0.5, 0.5),
            image_scale=button_image_scale,
            text='',
            text3_fg=(0.5, 0.5, 0.5, 0.75),
            text_scale=options_text_scale,
            text_pos=button_textpos,
            pos=(buttonbase_xcoord, 0.0,
                 (buttonbase_ycoord - textRowHeight * 2) +
                 0.025000000000000001),
            command=self._OptionsTabPage__doToggleToonChatSounds)
        self.ToonChatSounds_toggleButton.setScale(0.80000000000000004)
        self.speedChatStyleText = SpeedChat.SpeedChat(
            name='OptionsPageStyleText',
            structure=[2000],
            backgroundModelName='phase_3/models/gui/ChatPanel',
            guiModelName='phase_3.5/models/gui/speedChatGui')
        self.speedChatStyleText.setScale(self.speed_chat_scale)
        self.speedChatStyleText.setPos(
            0.37, 0,
            (buttonbase_ycoord - textRowHeight * 6) + 0.029999999999999999)
        self.speedChatStyleText.reparentTo(self, DGG.FOREGROUND_SORT_INDEX)
        if wantShaders:
            self.visualEffectText = SpeedChat.SpeedChat(
                name='OptionsPageStyleText',
                structure=[2000],
                backgroundModelName='phase_3/models/gui/ChatPanel',
                guiModelName='phase_3.5/models/gui/speedChatGui')
            self.visualEffectText.setScale(self.speed_chat_scale)
            self.visualEffectText.setPos(
                0.37, 0,
                (buttonbase_ycoord - textRowHeight * 7) + 0.029999999999999999)
            self.visualEffectText.reparentTo(self, DGG.FOREGROUND_SORT_INDEX)
        else:
            self.visualEffectText = None
        self.exitButton = DirectButton(
            parent=self,
            relief=None,
            image=(guiButton.find('**/QuitBtn_UP'),
                   guiButton.find('**/QuitBtn_DN'),
                   guiButton.find('**/QuitBtn_RLVR')),
            image_scale=1.1499999999999999,
            text=TTLocalizer.OptionsPageExitToontown,
            text_scale=options_text_scale,
            text_pos=button_textpos,
            textMayChange=0,
            pos=(0.45000000000000001, 0, -0.59999999999999998),
            command=self._OptionsTabPage__handleExitShowWithConfirm)
        guiButton.removeNode()
        gui.removeNode()

    def enter(self):
        self.show()
        taskMgr.remove(self.DisplaySettingsTaskName)
        self.settingsChanged = 0
        self._OptionsTabPage__setMusicButton()
        self._OptionsTabPage__setSoundFXButton()
        self._OptionsTabPage__setAcceptFriendsButton()
        self._OptionsTabPage__setAcceptWhispersButton()
        self._OptionsTabPage__setDisplaySettings()
        self._OptionsTabPage__setToonChatSoundsButton()
        self.speedChatStyleText.enter()
        self.speedChatStyleIndex = base.localAvatar.getSpeedChatStyleIndex()
        self.updateSpeedChatStyle()
        if self.visualEffectText:
            self.visualEffectText.enter()
            self.updateVisualEffect()

        if self.parent.book.safeMode:
            self.exitButton.hide()
        else:
            self.exitButton.show()

    def exit(self):
        self.ignore('confirmDone')
        self.hide()
        if self.settingsChanged != 0:
            Settings.writeSettings()

        self.speedChatStyleText.exit()
        if self.visualEffectText:
            self.visualEffectText.exit()

        if self.displaySettingsChanged:
            taskMgr.doMethodLater(self.DisplaySettingsDelay,
                                  self.writeDisplaySettings,
                                  self.DisplaySettingsTaskName)

    def unload(self):
        self.writeDisplaySettings()
        taskMgr.remove(self.DisplaySettingsTaskName)
        if self.displaySettings is not None:
            self.ignore(self.displaySettings.doneEvent)
            self.displaySettings.unload()

        self.displaySettings = None
        self.exitButton.destroy()
        self.Music_toggleButton.destroy()
        self.SoundFX_toggleButton.destroy()
        self.Friends_toggleButton.destroy()
        self.Whispers_toggleButton.destroy()
        self.DisplaySettingsButton.destroy()
        self.speedChatStyleLeftArrow.destroy()
        self.speedChatStyleRightArrow.destroy()
        if self.visualEffectLeftArrow:
            self.visualEffectLeftArrow.destroy()

        if self.visualEffectRightArrow:
            self.visualEffectRightArrow.destroy()

        del self.exitButton
        del self.SoundFX_Label
        del self.Music_Label
        del self.Friends_Label
        del self.Whispers_Label
        del self.SpeedChatStyle_Label
        del self.SoundFX_toggleButton
        del self.Music_toggleButton
        del self.Friends_toggleButton
        del self.Whispers_toggleButton
        del self.speedChatStyleLeftArrow
        del self.speedChatStyleRightArrow
        self.speedChatStyleText.exit()
        self.speedChatStyleText.destroy()
        del self.speedChatStyleText
        if self.visualEffectLeftArrow:
            del self.visualEffectLeftArrow

        if self.visualEffectRightArrow:
            del self.visualEffectRightArrow

        if self.visualEffectText:
            self.visualEffectText.exit()
            self.visualEffectText.destroy()
            del self.visualEffectText

        self.currentSizeIndex = None

    def _OptionsTabPage__doToggleMusic(self):
        messenger.send('wakeup')
        if base.musicActive:
            base.enableMusic(0)
            Settings.setMusic(0)
        else:
            base.enableMusic(1)
            Settings.setMusic(1)
        self.settingsChanged = 1
        self._OptionsTabPage__setMusicButton()

    def _OptionsTabPage__setMusicButton(self):
        if base.musicActive:
            self.Music_Label['text'] = TTLocalizer.OptionsPageMusicOnLabel
            self.Music_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff
        else:
            self.Music_Label['text'] = TTLocalizer.OptionsPageMusicOffLabel
            self.Music_toggleButton['text'] = TTLocalizer.OptionsPageToggleOn

    def _OptionsTabPage__doToggleSfx(self):
        messenger.send('wakeup')
        if base.sfxActive:
            base.enableSoundEffects(0)
            Settings.setSfx(0)
        else:
            base.enableSoundEffects(1)
            Settings.setSfx(1)
        self.settingsChanged = 1
        self._OptionsTabPage__setSoundFXButton()

    def _OptionsTabPage__doToggleToonChatSounds(self):
        messenger.send('wakeup')
        if base.toonChatSounds:
            base.toonChatSounds = 0
            Settings.setToonChatSounds(0)
        else:
            base.toonChatSounds = 1
            Settings.setToonChatSounds(1)
        self.settingsChanged = 1
        self._OptionsTabPage__setToonChatSoundsButton()

    def _OptionsTabPage__setSoundFXButton(self):
        if base.sfxActive:
            self.SoundFX_Label['text'] = TTLocalizer.OptionsPageSFXOnLabel
            self.SoundFX_toggleButton[
                'text'] = TTLocalizer.OptionsPageToggleOff
        else:
            self.SoundFX_Label['text'] = TTLocalizer.OptionsPageSFXOffLabel
            self.SoundFX_toggleButton['text'] = TTLocalizer.OptionsPageToggleOn
        self._OptionsTabPage__setToonChatSoundsButton()

    def _OptionsTabPage__setToonChatSoundsButton(self):
        if base.toonChatSounds:
            self.ToonChatSounds_Label[
                'text'] = TTLocalizer.OptionsPageToonChatSoundsOnLabel
            self.ToonChatSounds_toggleButton[
                'text'] = TTLocalizer.OptionsPageToggleOff
        else:
            self.ToonChatSounds_Label[
                'text'] = TTLocalizer.OptionsPageToonChatSoundsOffLabel
            self.ToonChatSounds_toggleButton[
                'text'] = TTLocalizer.OptionsPageToggleOn
        if base.sfxActive:
            self.ToonChatSounds_Label.setColorScale(1.0, 1.0, 1.0, 1.0)
            self.ToonChatSounds_toggleButton['state'] = DGG.NORMAL
        else:
            self.ToonChatSounds_Label.setColorScale(0.5, 0.5, 0.5, 0.5)
            self.ToonChatSounds_toggleButton['state'] = DGG.DISABLED

    def _OptionsTabPage__doToggleAcceptFriends(self):
        messenger.send('wakeup')
        if base.localAvatar.acceptingNewFriends:
            base.localAvatar.acceptingNewFriends = 0
            Settings.setAcceptingNewFriends(0)
        else:
            base.localAvatar.acceptingNewFriends = 1
            Settings.setAcceptingNewFriends(1)
        self.settingsChanged = 1
        self._OptionsTabPage__setAcceptFriendsButton()

    def _OptionsTabPage__doToggleAcceptWhispers(self):
        messenger.send('wakeup')
        if base.localAvatar.acceptingNonFriendWhispers:
            base.localAvatar.acceptingNonFriendWhispers = 0
            Settings.setAcceptingNonFriendWhispers(0)
        else:
            base.localAvatar.acceptingNonFriendWhispers = 1
            Settings.setAcceptingNonFriendWhispers(1)
        self.settingsChanged = 1
        self._OptionsTabPage__setAcceptWhispersButton()

    def _OptionsTabPage__setAcceptFriendsButton(self):
        if base.localAvatar.acceptingNewFriends:
            self.Friends_Label[
                'text'] = TTLocalizer.OptionsPageFriendsEnabledLabel
            self.Friends_toggleButton[
                'text'] = TTLocalizer.OptionsPageToggleOff
        else:
            self.Friends_Label[
                'text'] = TTLocalizer.OptionsPageFriendsDisabledLabel
            self.Friends_toggleButton['text'] = TTLocalizer.OptionsPageToggleOn

    def _OptionsTabPage__setAcceptWhispersButton(self):
        if base.localAvatar.acceptingNonFriendWhispers:
            self.Whispers_Label[
                'text'] = TTLocalizer.OptionsPageWhisperEnabledLabel
            self.Whispers_toggleButton[
                'text'] = TTLocalizer.OptionsPageToggleOff
        else:
            self.Whispers_Label[
                'text'] = TTLocalizer.OptionsPageWhisperDisabledLabel
            self.Whispers_toggleButton[
                'text'] = TTLocalizer.OptionsPageToggleOn

    def _OptionsTabPage__doDisplaySettings(self):
        if self.displaySettings is None:
            self.displaySettings = DisplaySettingsDialog.DisplaySettingsDialog(
            )
            self.displaySettings.load()
            self.accept(self.displaySettings.doneEvent,
                        self._OptionsTabPage__doneDisplaySettings)

        self.displaySettings.enter(self.ChangeDisplaySettings,
                                   self.ChangeDisplayAPI)

    def _OptionsTabPage__doneDisplaySettings(self, anyChanged, apiChanged):
        if anyChanged:
            self._OptionsTabPage__setDisplaySettings()
            properties = base.win.getProperties()
            self.displaySettingsChanged = 1
            self.displaySettingsSize = (properties.getXSize(),
                                        properties.getYSize())
            self.displaySettingsFullscreen = properties.getFullscreen()
            self.displaySettingsEmbedded = self.isPropertiesEmbedded(
                properties)
            self.displaySettingsApi = base.pipe.getInterfaceName()
            self.displaySettingsApiChanged = apiChanged

    def isPropertiesEmbedded(self, properties):
        result = False
        if properties.getParentWindow():
            result = True

        return result

    def _OptionsTabPage__setDisplaySettings(self):
        properties = base.win.getProperties()
        if properties.getFullscreen():
            screensize = '%s x %s' % (properties.getXSize(),
                                      properties.getYSize())
        else:
            screensize = TTLocalizer.OptionsPageDisplayWindowed
        isEmbedded = self.isPropertiesEmbedded(properties)
        if isEmbedded:
            screensize = TTLocalizer.OptionsPageDisplayEmbedded

        api = base.pipe.getInterfaceName()
        settings = {'screensize': screensize, 'api': api}
        if self.ChangeDisplayAPI:
            OptionsPage.notify.debug('change display settings...')
            text = TTLocalizer.OptionsPageDisplaySettings % settings
        else:
            OptionsPage.notify.debug('no change display settings...')
            text = TTLocalizer.OptionsPageDisplaySettingsNoApi % settings
        self.DisplaySettings_Label['text'] = text

    def _OptionsTabPage__doSpeedChatStyleLeft(self):
        if self.speedChatStyleIndex > 0:
            self.speedChatStyleIndex = self.speedChatStyleIndex - 1
            self.updateSpeedChatStyle()

    def _OptionsTabPage__doSpeedChatStyleRight(self):
        if self.speedChatStyleIndex < len(speedChatStyles) - 1:
            self.speedChatStyleIndex = self.speedChatStyleIndex + 1
            self.updateSpeedChatStyle()

    def _OptionsTabPage__doVisualEffectLeft(self):
        if self.visualEffectIndex > 0:
            self.visualEffectIndex = self.visualEffectIndex - 1
            self.updateVisualEffect()

    def _OptionsTabPage__doVisualEffectRight(self):
        if self.visualEffectIndex < len(visualEffects) - 1:
            self.visualEffectIndex = self.visualEffectIndex + 1
            self.updateVisualEffect()

    def updateSpeedChatStyle(self):
        (nameKey, arrowColor, rolloverColor,
         frameColor) = speedChatStyles[self.speedChatStyleIndex]
        newSCColorScheme = SCColorScheme.SCColorScheme(
            arrowColor=arrowColor,
            rolloverColor=rolloverColor,
            frameColor=frameColor)
        self.speedChatStyleText.setColorScheme(newSCColorScheme)
        self.speedChatStyleText.clearMenu()
        colorName = SCStaticTextTerminal.SCStaticTextTerminal(nameKey)
        self.speedChatStyleText.append(colorName)
        self.speedChatStyleText.finalize()
        self.speedChatStyleText.setPos(
            0.44500000000000001 -
            self.speedChatStyleText.getWidth() * self.speed_chat_scale / 2, 0,
            self.speedChatStyleText.getPos()[2])
        if self.speedChatStyleIndex > 0:
            self.speedChatStyleLeftArrow['state'] = DGG.NORMAL
        else:
            self.speedChatStyleLeftArrow['state'] = DGG.DISABLED
        if self.speedChatStyleIndex < len(speedChatStyles) - 1:
            self.speedChatStyleRightArrow['state'] = DGG.NORMAL
        else:
            self.speedChatStyleRightArrow['state'] = DGG.DISABLED
        base.localAvatar.b_setSpeedChatStyleIndex(self.speedChatStyleIndex)

    def updateVisualEffect(self):
        (newEffectKey, newEffectName) = visualEffects[self.visualEffectIndex]
        self.visualEffectText.clearMenu()
        effectName = SCStaticTextTerminal.SCStaticTextTerminal(newEffectKey)
        self.visualEffectText.append(effectName)
        self.visualEffectText.finalize()
        self.visualEffectText.setPos(
            0.44500000000000001 -
            self.visualEffectText.getWidth() * self.speed_chat_scale / 2, 0,
            self.visualEffectText.getPos()[2])
        if self.visualEffectIndex > 0:
            self.visualEffectLeftArrow['state'] = DGG.NORMAL
        else:
            self.visualEffectLeftArrow['state'] = DGG.DISABLED
        if self.visualEffectIndex < len(visualEffects) - 1:
            self.visualEffectRightArrow['state'] = DGG.NORMAL
        else:
            self.visualEffectRightArrow['state'] = DGG.DISABLED
        base.cr.useShader(newEffectName)

    def writeDisplaySettings(self, task=None):
        if not self.displaySettingsChanged:
            return None

        taskMgr.remove(self.DisplaySettingsTaskName)
        self.notify.info(
            'writing new display settings %s, fullscreen %s, embedded %s, %s to SettingsFile.'
            % (self.displaySettingsSize, self.displaySettingsFullscreen,
               self.displaySettingsEmbedded, self.displaySettingsApi))
        Settings.setResolutionDimensions(self.displaySettingsSize[0],
                                         self.displaySettingsSize[1])
        Settings.setWindowedMode(not (self.displaySettingsFullscreen))
        Settings.setEmbeddedMode(self.displaySettingsEmbedded)
        if self.displaySettingsApiChanged:
            api = self.DisplaySettingsApiMap.get(self.displaySettingsApi)
            if api is None:
                self.notify.warning('Cannot save unknown display API: %s' %
                                    self.displaySettingsApi)
            else:
                Settings.setDisplayDriver(api)

        Settings.writeSettings()
        self.displaySettingsChanged = 0
        return Task.done

    def _OptionsTabPage__handleExitShowWithConfirm(self):
        self.confirm = TTDialog.TTGlobalDialog(
            doneEvent='confirmDone',
            message=TTLocalizer.OptionsPageExitConfirm,
            style=TTDialog.TwoChoice)
        self.confirm.show()
        self.parent.doneStatus = {'mode': 'exit', 'exitTo': 'closeShard'}
        self.accept('confirmDone', self._OptionsTabPage__handleConfirm)

    def _OptionsTabPage__handleConfirm(self):
        status = self.confirm.doneStatus
        self.ignore('confirmDone')
        self.confirm.cleanup()
        del self.confirm
        if status == 'ok':
            base.cr._userLoggingOut = True
            messenger.send(self.parent.doneEvent)


class CodesTabPage(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('CodesTabPage')

    def __init__(self, parent=aspect2d):
        self.parent = parent
        DirectFrame.__init__(
            self,
            parent=self.parent,
            relief=None,
            pos=(0.0, 0.0, 0.0),
            scale=(1.0, 1.0, 1.0))
        self.load()

    def destroy(self):
        self.parent = None
        DirectFrame.destroy(self)

    def load(self):
        cdrGui = loader.loadModel(
            'phase_3.5/models/gui/tt_m_gui_sbk_codeRedemptionGui')
        instructionGui = cdrGui.find('**/tt_t_gui_sbk_cdrPresent')
        flippyGui = cdrGui.find('**/tt_t_gui_sbk_cdrFlippy')
        codeBoxGui = cdrGui.find('**/tt_t_gui_sbk_cdrCodeBox')
        self.resultPanelSuccessGui = cdrGui.find(
            '**/tt_t_gui_sbk_cdrResultPanel_success')
        self.resultPanelFailureGui = cdrGui.find(
            '**/tt_t_gui_sbk_cdrResultPanel_failure')
        self.resultPanelErrorGui = cdrGui.find(
            '**/tt_t_gui_sbk_cdrResultPanel_error')
        self.successSfx = base.loadSfx(
            'phase_3.5/audio/sfx/tt_s_gui_sbk_cdrSuccess.mp3')
        self.failureSfx = base.loadSfx(
            'phase_3.5/audio/sfx/tt_s_gui_sbk_cdrFailure.mp3')
        self.instructionPanel = DirectFrame(
            parent=self,
            relief=None,
            image=instructionGui,
            image_scale=0.80000000000000004,
            text=TTLocalizer.CdrInstructions,
            text_pos=TTLocalizer.OPCodesInstructionPanelTextPos,
            text_align=TextNode.ACenter,
            text_scale=TTLocalizer.OPCodesResultPanelTextScale,
            text_wordwrap=TTLocalizer.OPCodesInstructionPanelTextWordWrap,
            pos=(-0.42899999999999999, 0, -0.050000000000000003))
        self.codeBox = DirectFrame(
            parent=self,
            relief=None,
            image=codeBoxGui,
            pos=(0.433, 0, 0.34999999999999998))
        self.flippyFrame = DirectFrame(
            parent=self,
            relief=None,
            image=flippyGui,
            pos=(0.44, 0, -0.35299999999999998))
        self.codeInput = DirectEntry(
            parent=self.codeBox,
            relief=DGG.GROOVE,
            scale=0.080000000000000002,
            pos=(-0.33000000000000002, 0, -0.0060000000000000001),
            borderWidth=(0.050000000000000003, 0.050000000000000003),
            frameColor=((1, 1, 1, 1), (1, 1, 1, 1), (0.5, 0.5, 0.5, 0.5)),
            state=DGG.NORMAL,
            text_align=TextNode.ALeft,
            text_scale=TTLocalizer.OPCodesInputTextScale,
            width=10.5,
            numLines=1,
            focus=1,
            backgroundFocus=0,
            cursorKeys=1,
            text_fg=(0, 0, 0, 1),
            suppressMouse=1,
            autoCapitalize=0,
            command=self._CodesTabPage__submitCode)
        submitButtonGui = loader.loadModel('phase_3/models/gui/quit_button')
        self.submitButton = DirectButton(
            parent=self,
            relief=None,
            image=(submitButtonGui.find('**/QuitBtn_UP'),
                   submitButtonGui.find('**/QuitBtn_DN'),
                   submitButtonGui.find('**/QuitBtn_RLVR'),
                   submitButtonGui.find('**/QuitBtn_UP')),
            image3_color=Vec4(0.5, 0.5, 0.5, 0.5),
            image_scale=1.1499999999999999,
            state=DGG.NORMAL,
            text=TTLocalizer.NameShopSubmitButton,
            text_scale=TTLocalizer.OPCodesSubmitTextScale,
            text_align=TextNode.ACenter,
            text_pos=TTLocalizer.OPCodesSubmitTextPos,
            text3_fg=(0.5, 0.5, 0.5, 0.75),
            textMayChange=0,
            pos=(0.45000000000000001, 0.0, 0.089599999999999999),
            command=self._CodesTabPage__submitCode)
        self.resultPanel = DirectFrame(
            parent=self,
            relief=None,
            image=self.resultPanelSuccessGui,
            text='',
            text_pos=TTLocalizer.OPCodesResultPanelTextPos,
            text_align=TextNode.ACenter,
            text_scale=TTLocalizer.OPCodesResultPanelTextScale,
            text_wordwrap=TTLocalizer.OPCodesResultPanelTextWordWrap,
            pos=(-0.41999999999999998, 0, -0.0567))
        self.resultPanel.hide()
        closeButtonGui = loader.loadModel(
            'phase_3/models/gui/dialog_box_buttons_gui')
        self.closeButton = DirectButton(
            parent=self.resultPanel,
            pos=(0.29599999999999999, 0, -0.46600000000000003),
            relief=None,
            state=DGG.NORMAL,
            image=(closeButtonGui.find('**/CloseBtn_UP'),
                   closeButtonGui.find('**/CloseBtn_DN'),
                   closeButtonGui.find('**/CloseBtn_Rllvr')),
            image_scale=(1, 1, 1),
            command=self._CodesTabPage__hideResultPanel)
        closeButtonGui.removeNode()
        cdrGui.removeNode()
        submitButtonGui.removeNode()

    def enter(self):
        self.show()
        localAvatar.chatMgr.fsm.request('otherDialog')
        self.codeInput['focus'] = 1
        self.codeInput.enterText('')
        self._CodesTabPage__enableCodeEntry()

    def exit(self):
        self.resultPanel.hide()
        self.hide()
        localAvatar.chatMgr.fsm.request('mainMenu')

    def unload(self):
        self.instructionPanel.destroy()
        self.instructionPanel = None
        self.codeBox.destroy()
        self.codeBox = None
        self.flippyFrame.destroy()
        self.flippyFrame = None
        self.codeInput.destroy()
        self.codeInput = None
        self.submitButton.destroy()
        self.submitButton = None
        self.resultPanel.destroy()
        self.resultPanel = None
        self.closeButton.destroy()
        self.closeButton = None
        del self.successSfx
        del self.failureSfx

    def _CodesTabPage__submitCode(self, input=None):
        if input is None:
            input = self.codeInput.get()

        self.codeInput['focus'] = 1
        if input == '':
            return None

        messenger.send('wakeup')
        if hasattr(base, 'codeRedemptionMgr'):
            base.codeRedemptionMgr.redeemCode(
                input, self._CodesTabPage__getCodeResult)

        self.codeInput.enterText('')
        self._CodesTabPage__disableCodeEntry()

    def _CodesTabPage__getCodeResult(self, result, awardMgrResult):
        self.notify.debug('result = %s' % result)
        self.notify.debug('awardMgrResult = %s' % awardMgrResult)
        self._CodesTabPage__enableCodeEntry()
        if result == 0:
            self.resultPanel['image'] = self.resultPanelSuccessGui
            self.resultPanel['text'] = TTLocalizer.CdrResultSuccess
        elif result == 1 or result == 3:
            self.resultPanel['image'] = self.resultPanelFailureGui
            self.resultPanel['text'] = TTLocalizer.CdrResultInvalidCode
        elif result == 2:
            self.resultPanel['image'] = self.resultPanelFailureGui
            self.resultPanel['text'] = TTLocalizer.CdrResultExpiredCode
        elif result == 4:
            self.resultPanel['image'] = self.resultPanelErrorGui
            if awardMgrResult == 0:
                self.resultPanel['text'] = TTLocalizer.CdrResultSuccess
            elif awardMgrResult == 1 and awardMgrResult == 2 and awardMgrResult == 15 or awardMgrResult == 16:
                self.resultPanel['text'] = TTLocalizer.CdrResultUnknownError
            elif awardMgrResult == 3 or awardMgrResult == 4:
                self.resultPanel['text'] = TTLocalizer.CdrResultMailboxFull
            elif awardMgrResult == 5 or awardMgrResult == 10:
                self.resultPanel[
                    'text'] = TTLocalizer.CdrResultAlreadyInMailbox
            elif awardMgrResult == 6 and awardMgrResult == 7 or awardMgrResult == 11:
                self.resultPanel['text'] = TTLocalizer.CdrResultAlreadyInQueue
            elif awardMgrResult == 8:
                self.resultPanel['text'] = TTLocalizer.CdrResultAlreadyInCloset
            elif awardMgrResult == 9:
                self.resultPanel[
                    'text'] = TTLocalizer.CdrResultAlreadyBeingWorn
            elif awardMgrResult == 12 and awardMgrResult == 13 or awardMgrResult == 14:
                self.resultPanel['text'] = TTLocalizer.CdrResultAlreadyReceived

        elif result == 5:
            self.resultPanel['text'] = TTLocalizer.CdrResultTooManyFails
            self._CodesTabPage__disableCodeEntry()
        elif result == 6:
            self.resultPanel['text'] = TTLocalizer.CdrResultServiceUnavailable
            self._CodesTabPage__disableCodeEntry()

        if result == 0:
            self.successSfx.play()
        else:
            self.failureSfx.play()
        self.resultPanel.show()

    def _CodesTabPage__hideResultPanel(self):
        self.resultPanel.hide()

    def _CodesTabPage__disableCodeEntry(self):
        self.codeInput['state'] = DGG.DISABLED
        self.submitButton['state'] = DGG.DISABLED

    def _CodesTabPage__enableCodeEntry(self):
        self.codeInput['state'] = DGG.NORMAL
        self.codeInput['focus'] = 1
        self.submitButton['state'] = DGG.NORMAL
