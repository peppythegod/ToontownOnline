import __builtin__

# Settings
from pandac.PandaModules import loadPrcFile
loadPrcFile("etc/config.prc")

# Required stuff
from otp.otpbase import GameSettings
__builtin__.Settings = GameSettings.GameSettings()
__builtin__.isClient = lambda: True

# Start
import toontown.toonbase.ToontownStart