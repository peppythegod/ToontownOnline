import __builtin__, os

# Settings
from pandac.PandaModules import loadPrcFile, loadPrcFileData
loadPrcFile("etc/ai.prc")

loadPrcFileData("base channel env", "air-base-channel %s" %os.getenv('BASE_CHANNEL', 401000000))
loadPrcFileData("district name env", "district-name %s" %os.getenv('DISTRICT_NAME', "Genesis"))

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