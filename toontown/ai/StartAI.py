from panda3d.core import *

from direct.showbase.ShowBase import *
from toontown.distributed import PythonUtil
import __builtin__

class Game:
    name = "toontown"

__builtin__.game = Game()

from otp.ai.AIBaseGlobal import *

__builtin__.process = 'ai'
__builtin__.isClient = lambda: PythonUtil.isClient()

from toontown.ai.ToontownAIRepository import ToontownAIRepository


simbase.air = ToontownAIRepository(config.GetInt('air-base-channel', 401000000),
                                   config.GetInt('air-stateserver', 1001),
                                   config.GetString('district-name', 'Genesis'))
                                   
host = config.GetString('air-connect', '127.0.0.1')
port = 7100
if ':' in host:
    host, port = host.split(':', 1)
    port = int(port)
simbase.air.connect(host, port)

try:
    run()
except SystemExit:
    raise
except Exception:
    info = PythonUtil.describeException()
    simbase.air.writeServerEvent('ai-exception', simbase.air.getAvatarIdFromSender(), simbase.air.getAccountIdFromSender(), info)
    raise