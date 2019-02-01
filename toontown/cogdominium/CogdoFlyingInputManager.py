from pandac.PandaModules import CollisionSphere, CollisionNode, BitMask32, CollisionHandlerEvent, CollisionRay
from toontown.minigame import ArrowKeys


class CogdoFlyingInputManager:

    def __init__(self):
        self.arrowKeys = ArrowKeys.ArrowKeys()
        self.arrowKeys.disable()

    def enable(self):
        self.arrowKeys.setPressHandlers([
            self._CogdoFlyingInputManager__upArrowPressed,
            self._CogdoFlyingInputManager__downArrowPressed,
            self._CogdoFlyingInputManager__leftArrowPressed,
            self._CogdoFlyingInputManager__rightArrowPressed,
            self._CogdoFlyingInputManager__controlPressed])
        self.arrowKeys.enable()

    def disable(self):
        self.arrowKeys.clearPressHandlers()
        self.arrowKeys.disable()

    def destroy(self):
        self.disable()
        self.arrowKeys.destroy()
        self.arrowKeys = None
        self.refuelLerp = None

    def _CogdoFlyingInputManager__upArrowPressed(self):
        pass

    def _CogdoFlyingInputManager__downArrowPressed(self):
        pass

    def _CogdoFlyingInputManager__leftArrowPressed(self):
        pass

    def _CogdoFlyingInputManager__rightArrowPressed(self):
        pass

    def _CogdoFlyingInputManager__controlPressed(self):
        pass
