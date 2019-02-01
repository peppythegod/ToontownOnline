from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import ModifierButtons
ROTATE_LEFT_KEY = 'arrow_left'
ROTATE_RIGHT_KEY = 'arrow_right'
FORWARD_KEY = 'arrow_up'
BACKWARDS_KEY = 'arrow_down'
THROW_PIE_KEYS = [
    'control',
    'delete',
    'insert']


class PartyCogActivityInput(DirectObject):
    notify = directNotify.newCategory('PartyCogActivityInput')
    leftPressed = 0
    rightPressed = 0
    upPressed = 0
    downPressed = 0
    throwPiePressed = False
    throwPieWasReleased = False
    throwPiePressedStartTime = 0

    def __init__(self, exitActivityCallback):
        DirectObject.__init__(self)
        self.exitActivityCallback = exitActivityCallback
        self._prevModifierButtons = base.mouseWatcherNode.getModifierButtons()

    def enable(self):
        self.enableAimKeys()
        self.enableThrowPieKeys()

    def disable(self):
        self.disableAimKeys()
        self.disableThrowPieKeys()

    def enableExitActivityKeys(self):
        self.accept('escape', self.exitActivityCallback)

    def disableExitActivityKeys(self):
        self.ignore('escape')

    def enableThrowPieKeys(self):
        for key in THROW_PIE_KEYS:
            self.accept(key, self.handleThrowPieKeyPressed, [
                key])

        self.throwPiePressed = False
        self.readyToThrowPie = False

    def disableThrowPieKeys(self):
        for key in THROW_PIE_KEYS:
            self.ignore(key)
            self.ignore(key + '-up')

    def handleThrowPieKeyPressed(self, key):
        if self.throwPiePressed:
            return None

        self.throwPiePressed = True
        self.accept(key + '-up', self.handleThrowPieKeyReleased, [
            key])
        self.throwPiePressedStartTime = globalClock.getFrameTime()

    def handleThrowPieKeyReleased(self, key):
        if not self.throwPiePressed:
            return None

        self.ignore(key + '-up')
        self.throwPieWasReleased = True
        self.throwPiePressed = False

    def enableAimKeys(self):
        self.leftPressed = 0
        self.rightPressed = 0
        base.mouseWatcherNode.setModifierButtons(ModifierButtons())
        base.buttonThrowers[0].node().setModifierButtons(ModifierButtons())
        self.accept(
            ROTATE_LEFT_KEY,
            self._PartyCogActivityInput__handleLeftKeyPressed)
        self.accept(
            ROTATE_RIGHT_KEY,
            self._PartyCogActivityInput__handleRightKeyPressed)
        self.accept(
            FORWARD_KEY,
            self._PartyCogActivityInput__handleUpKeyPressed)
        self.accept(
            BACKWARDS_KEY,
            self._PartyCogActivityInput__handleDownKeyPressed)

    def disableAimKeys(self):
        self.ignore(ROTATE_LEFT_KEY)
        self.ignore(ROTATE_RIGHT_KEY)
        self.ignore(FORWARD_KEY)
        self.ignore(BACKWARDS_KEY)
        self.leftPressed = 0
        self.rightPressed = 0
        self.upPressed = 0
        self.downPressed = 0
        self.ignore(ROTATE_LEFT_KEY + '-up')
        self.ignore(ROTATE_RIGHT_KEY + '-up')
        self.ignore(FORWARD_KEY + '-up')
        self.ignore(BACKWARDS_KEY + '-up')
        base.mouseWatcherNode.setModifierButtons(self._prevModifierButtons)
        base.buttonThrowers[0].node().setModifierButtons(
            self._prevModifierButtons)

    def _PartyCogActivityInput__handleLeftKeyPressed(self):
        self.ignore(ROTATE_LEFT_KEY)
        self.accept(
            ROTATE_LEFT_KEY + '-up',
            self._PartyCogActivityInput__handleLeftKeyReleased)
        self._PartyCogActivityInput__leftPressed()

    def _PartyCogActivityInput__handleRightKeyPressed(self):
        self.ignore(ROTATE_RIGHT_KEY)
        self.accept(ROTATE_RIGHT_KEY + '-up',
                    self._PartyCogActivityInput__handleRightKeyReleased)
        self._PartyCogActivityInput__rightPressed()

    def _PartyCogActivityInput__handleLeftKeyReleased(self):
        self.ignore(ROTATE_LEFT_KEY + '-up')
        self.accept(
            ROTATE_LEFT_KEY,
            self._PartyCogActivityInput__handleLeftKeyPressed)
        self._PartyCogActivityInput__leftReleased()

    def _PartyCogActivityInput__handleRightKeyReleased(self):
        self.ignore(ROTATE_RIGHT_KEY + '-up')
        self.accept(
            ROTATE_RIGHT_KEY,
            self._PartyCogActivityInput__handleRightKeyPressed)
        self._PartyCogActivityInput__rightReleased()

    def _PartyCogActivityInput__handleUpKeyPressed(self):
        self.ignore(FORWARD_KEY)
        self.accept(
            FORWARD_KEY + '-up',
            self._PartyCogActivityInput__handleUpKeyReleased)
        self._PartyCogActivityInput__upPressed()

    def _PartyCogActivityInput__handleUpKeyReleased(self):
        self.ignore(FORWARD_KEY + '-up')
        self.accept(
            FORWARD_KEY,
            self._PartyCogActivityInput__handleUpKeyPressed)
        self._PartyCogActivityInput__upReleased()

    def _PartyCogActivityInput__handleDownKeyPressed(self):
        self.ignore(BACKWARDS_KEY)
        self.accept(
            BACKWARDS_KEY + '-up',
            self._PartyCogActivityInput__handleDownKeyReleased)
        self._PartyCogActivityInput__downPressed()

    def _PartyCogActivityInput__handleDownKeyReleased(self):
        self.ignore(BACKWARDS_KEY + '-up')
        self.accept(
            BACKWARDS_KEY,
            self._PartyCogActivityInput__handleDownKeyPressed)
        self._PartyCogActivityInput__downReleased()

    def _PartyCogActivityInput__leftPressed(self):
        self.leftPressed = self._PartyCogActivityInput__enterControlActive(
            self.leftPressed)

    def _PartyCogActivityInput__rightPressed(self):
        self.rightPressed = self._PartyCogActivityInput__enterControlActive(
            self.rightPressed)

    def _PartyCogActivityInput__upPressed(self):
        self.upPressed = self._PartyCogActivityInput__enterControlActive(
            self.upPressed)

    def _PartyCogActivityInput__downPressed(self):
        self.downPressed = self._PartyCogActivityInput__enterControlActive(
            self.downPressed)

    def _PartyCogActivityInput__leftReleased(self):
        self.leftPressed = self._PartyCogActivityInput__exitControlActive(
            self.leftPressed)

    def _PartyCogActivityInput__rightReleased(self):
        self.rightPressed = self._PartyCogActivityInput__exitControlActive(
            self.rightPressed)

    def _PartyCogActivityInput__upReleased(self):
        self.upPressed = self._PartyCogActivityInput__exitControlActive(
            self.upPressed)

    def _PartyCogActivityInput__downReleased(self):
        self.downPressed = self._PartyCogActivityInput__exitControlActive(
            self.downPressed)

    def _PartyCogActivityInput__enterControlActive(self, input):
        return input + 1

    def _PartyCogActivityInput__exitControlActive(self, input):
        return max(0, input - 1)
