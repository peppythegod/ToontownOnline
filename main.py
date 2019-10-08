import __builtin__

# Settings
from pandac.PandaModules import loadPrcFile
loadPrcFile("etc/config.prc")

# Required stuff
from otp.otpbase import GameSettings
__builtin__.Settings = GameSettings.GameSettings()
__builtin__.isClient = lambda: True

# Stuff that needs to be at hand
from toontown.dna.DNAParser import DNAStorage
from toontown.dna.DNAParser import DNADoor
__builtin__.DNAStorage = DNAStorage
__builtin__.DNADoor = DNADoor

from libotp import NametagGlobals, NametagGroup, NametagFloat2d, Nametag, SuitLegList
from libotp._constants import *
__builtin__.NametagGlobals = NametagGlobals
__builtin__.NametagGroup = NametagGroup
__builtin__.NametagFloat2d = NametagFloat2d
__builtin__.Nametag = Nametag
__builtin__.CFSpeech = CFSpeech
__builtin__.CFThought = CFThought
__builtin__.CFQuicktalker = CFQuicktalker
__builtin__.CFTimeout = CFTimeout
__builtin__.CFPageButton = CFPageButton
__builtin__.CFQuitButton = CFQuitButton
__builtin__.CFReversed = CFReversed
__builtin__.CFSndOpenchat = CFSndOpenchat
__builtin__.CFNoQuitButton = CFNoQuitButton
__builtin__.SuitLegList = SuitLegList.SuitLegList
__builtin__.SuitLeg = SuitLegList.SuitLeg

# Start
import toontown.toonbase.ToontownStart