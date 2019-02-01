from otp.distributed.OtpDoGlobals import *
from otp.friends import FriendManager
from toontown.distributed import ToontownClientRepository
from direct.showbase.MessengerGlobal import *
from ToonBaseGlobal import *
from direct.gui.DirectGui import *
import ToontownLoader
from otp.otpbase import OTPGlobals
import TTLocalizer
import ToonBase
import ToontownGlobals
from direct.gui import DirectGuiGlobals
from pandac.PandaModules import *
import random
import sys
import os
import time
import __builtin__


class game:
    name = 'toontown'
    process = 'client'


__builtin__.game = game()

try:
    pass
except BaseException:
    from toontown.launcher.ToontownDummyLauncher import ToontownDummyLauncher
    launcher = ToontownDummyLauncher()
    __builtin__.launcher = launcher

launcher.setRegistry('EXIT_PAGE', 'normal')
pollingDelay = 0.5
print 'ToontownStart: Polling for game2 to finish...'
while not launcher.getGame2Done():
    time.sleep(pollingDelay)
print 'ToontownStart: Game2 is finished.'
print 'ToontownStart: Starting the game.'
if launcher.isDummy():
    http = HTTPClient()
else:
    http = launcher.http
tempLoader = PandaLoader()
backgroundNode = tempLoader.loadSync(
    Filename('phase_3/models/gui/loading-background'))
print 'ToontownStart: setting default font'
DirectGuiGlobals.setDefaultFontFunc(
    ToontownGlobals.getInterfaceFont)
launcher.setPandaErrorCode(7)
ToonBase.ToonBase()
if base.win is None:
    print 'Unable to open window; aborting.'
    sys.exit()

launcher.setPandaErrorCode(0)
launcher.setPandaWindowOpen()
ConfigVariableDouble('decompressor-step-time').setValue(0.01)
ConfigVariableDouble('extractor-step-time').setValue(0.01)
backgroundNodePath = aspect2d.attachNewNode(backgroundNode, 0)
backgroundNodePath.setPos(0.0, 0.0, 0.0)
backgroundNodePath.setScale(render2d, VBase3(1))
backgroundNodePath.find('**/fg').setBin('fixed', 20)
backgroundNodePath.find('**/bg').setBin('fixed', 10)
base.graphicsEngine.renderFrame()
DirectGuiGlobals.setDefaultRolloverSound(
    base.loadSfx('phase_3/audio/sfx/GUI_rollover.mp3'))
DirectGuiGlobals.setDefaultClickSound(base.loadSfx(
    'phase_3/audio/sfx/GUI_create_toon_fwd.mp3'))
DirectGuiGlobals.setDefaultDialogGeom(
    loader.loadModel('phase_3/models/gui/dialog_box_gui'))
OTPGlobals.setDefaultProductPrefix(TTLocalizer.ProductPrefix)
if base.musicManagerIsValid:
    music = base.musicManager.getSound('phase_3/audio/bgm/tt_theme.mid')
    if music:
        music.setLoop(1)
        music.setVolume(0.90000000000000002)
        music.play()

    print 'ToontownStart: Loading default gui sounds'
    DirectGuiGlobals.setDefaultRolloverSound(base.loadSfx(
        'phase_3/audio/sfx/GUI_rollover.mp3'))
    DirectGuiGlobals.setDefaultClickSound(base.loadSfx(
        'phase_3/audio/sfx/GUI_create_toon_fwd.mp3'))
else:
    music = None
serverVersion = base.config.GetString('server-version', 'no_version_set')
print 'ToontownStart: serverVersion: ', serverVersion
version = OnscreenText(serverVersion,
                       pos=(-1.3,
                            -0.97499999999999998),
                       scale=0.059999999999999998,
                       fg=Vec4(0,
                               0,
                               1,
                               0.59999999999999998),
                       align=TextNode.ALeft)
loader.beginBulkLoad(
    'init',
    TTLocalizer.LoaderLabel,
    138,
    0,
    TTLocalizer.TIP_NONE)
cr = ToontownClientRepository.ToontownClientRepository(serverVersion, launcher)
cr.music = music
del music
base.initNametagGlobals()
base.cr = cr
loader.endBulkLoad('init')
cr.generateGlobalObject(OTP_DO_ID_FRIEND_MANAGER, 'FriendManager')
if not launcher.isDummy():
    base.startShow(cr, launcher.getGameServer())
else:
    base.startShow(cr)
backgroundNodePath.reparentTo(hidden)
backgroundNodePath.removeNode()
del backgroundNodePath
del backgroundNode
del tempLoader
version.cleanup()
del version
base.loader = base.loader
__builtin__.loader = base.loader
autoRun = ConfigVariableBool('toontown-auto-run', 1)
if autoRun and launcher.isDummy():
    if not Thread.isTrueThreads() or __name__ == '__main__':

        try:
            run()
        except SystemExit:
            raise
        except BaseException:
            from direct.showbase import PythonUtil
            print PythonUtil.describeException()
            raise
