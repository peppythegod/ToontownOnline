from direct.fsm.StatePush import StateVar
from otp.level.EntityStateVarSet import EntityStateVarSet
from toontown.cogdominium.CogdoEntityTypes import CogdoCraneGameSettings, CogdoCraneCogSettings
Settings = EntityStateVarSet(CogdoCraneGameSettings)
CogSettings = EntityStateVarSet(CogdoCraneCogSettings)
CranePosHprs = [(13.4, -136.59999999999999, 6, -45, 0, 0),
                (13.4, -91.400000000000006, 6, -135, 0, 0),
                (58.600000000000001, -91.400000000000006, 6, 135, 0, 0),
                (58.600000000000001, -136.59999999999999, 6, 45, 0, 0)]
MoneyBagPosHprs = [
    [77.200000000000003 - 84, -329.30000000000001 + 201, 0, -90, 0, 0],
    [77.099999999999994 - 84, -302.69999999999999 + 201, 0, -90, 0, 0],
    [165.69999999999999 - 84, -326.39999999999998 + 201, 0, 90, 0, 0],
    [165.5 - 84, -302.39999999999998 + 201, 0, 90, 0, 0],
    [107.8 - 84, -359.10000000000002 + 201, 0, 0, 0, 0],
    [133.90000000000001 - 84, -359.10000000000002 + 201, 0, 0, 0, 0],
    [107.0 - 84, -274.69999999999999 + 201, 0, 180, 0, 0],
    [134.19999999999999 - 84, -274.69999999999999 + 201, 0, 180, 0, 0]
]
for i in xrange(len(MoneyBagPosHprs)):
    MoneyBagPosHprs[i][2] += 6
