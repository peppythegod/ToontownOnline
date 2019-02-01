from direct.fsm.StatePush import FunctionCall
from otp.level.EntityStateVarSet import EntityStateVarSet
from otp.level.LevelSpec import LevelSpec


class CogdoLevelGameBase:

    def getLevelSpec(self):
        return LevelSpec(self.getSpec())

    if __dev__:

        def startHandleEdits(self):
            fcs = []
            Consts = self.getConsts()
            for item in Consts.__dict__.itervalues():
                if isinstance(item, EntityStateVarSet):
                    for attribName in item._getAttributeNames():
                        handler = getattr(
                            self, '_handle%sChanged' %
                            attribName, None)
                        if handler:
                            stateVar = getattr(item, attribName)
                            fcs.append(FunctionCall(handler, stateVar))
                            continue

            self._functionCalls = fcs

        def stopHandleEdits(self):
            if __dev__:
                for fc in self._functionCalls:
                    fc.destroy()

                self._functionCalls = None

        def getEntityTypeReg(self):
            import CogdoEntityTypes as CogdoEntityTypes
            EntityTypeRegistry = EntityTypeRegistry
            import otp.level
            typeReg = EntityTypeRegistry.EntityTypeRegistry(CogdoEntityTypes)
            return typeReg
