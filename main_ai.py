import __builtin__

# Settings
from pandac.PandaModules import loadPrcFile
loadPrcFile("etc/ai.prc")

# Stuff that needs to be at hand
from libotp import SuitLegList
__builtin__.SuitLegList = SuitLegList.SuitLegList
__builtin__.SuitLeg = SuitLegList.SuitLeg

# Start
import toontown.ai.StartAI