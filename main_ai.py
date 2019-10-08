import __builtin__

# Settings
from pandac.PandaModules import loadPrcFile
loadPrcFile("etc/ai.prc")

# Stuff that needs to be at hand
from libotp import SuitLegList
__builtin__.SuitLegList = SuitLegList.SuitLegList
__builtin__.SuitLeg = SuitLegList.SuitLeg

from toontown.dna.DNAParser import DNAStorage
from toontown.dna.DNAParser import DNAInteractiveProp
from toontown.dna.DNAParser import DNASuitPoint
__builtin__.DNAStorage = DNAStorage
__builtin__.DNAInteractiveProp = DNAInteractiveProp
__builtin__.DNASuitPoint = DNASuitPoint

# Start
import toontown.ai.StartAI