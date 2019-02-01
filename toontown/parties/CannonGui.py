from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectFrame, DirectButton
import direct.gui.DirectGuiGlobals as DGG
from toontown.parties import PartyUtils


class CannonGui(DirectObject):
    notify = directNotify.newCategory('CannonGui')
    FIRE_KEY = 'control'
    UP_KEY = 'arrow_up'
    DOWN_KEY = 'arrow_down'
    LEFT_KEY = 'arrow_left'
    RIGHT_KEY = 'arrow_right'
    FIRE_PRESSED = 'cannongui_fire_pressed'

    def __init__(self):
        self._CannonGui__loaded = False
        self.leftPressed = 0
        self.rightPressed = 0
        self.upPressed = 0
        self.downPressed = 0
        self._CannonGui__aimPad = None
        self._CannonGui__timerPad = None

    def load(self):
        if self._CannonGui__loaded:
            return None

        self._CannonGui__timerPad = PartyUtils.getNewToontownTimer()
        guiModel = 'phase_4/models/gui/cannon_game_gui'
        guiNode = loader.loadModel(guiModel)
        self._CannonGui__aimPad = DirectFrame(
            image=guiNode.find('**/CannonFire_PAD'), relief=None, pos=(
                0.69999999999999996, 0, -0.55333299999999996), scale=0.80000000000000004)
        guiNode.removeNode()
        self.fireButton = DirectButton(
            parent=self._CannonGui__aimPad,
            image=(
                (guiModel,
                 '**/Fire_Btn_UP'),
                (guiModel,
                 '**/Fire_Btn_DN'),
                (guiModel,
                 '**/Fire_Btn_RLVR')),
            relief=None,
            pos=(
                0.0115741,
                0,
                0.0050505100000000002),
            scale=1.0,
            command=self._CannonGui__firePressed)
        self.upButton = DirectButton(
            parent=self._CannonGui__aimPad,
            image=(
                (guiModel,
                 '**/Cannon_Arrow_UP'),
                (guiModel,
                 '**/Cannon_Arrow_DN'),
                (guiModel,
                 '**/Cannon_Arrow_RLVR')),
            relief=None,
            pos=(
                0.0115741,
                0,
                0.221717))
        self.downButton = DirectButton(
            parent=self._CannonGui__aimPad,
            image=(
                (guiModel,
                 '**/Cannon_Arrow_UP'),
                (guiModel,
                 '**/Cannon_Arrow_DN'),
                (guiModel,
                 '**/Cannon_Arrow_RLVR')),
            relief=None,
            pos=(
                0.0136112,
                0,
                -0.21010100000000001),
            image_hpr=(
                0,
                0,
                180))
        self.leftButton = DirectButton(
            parent=self._CannonGui__aimPad,
            image=(
                (guiModel,
                 '**/Cannon_Arrow_UP'),
                (guiModel,
                 '**/Cannon_Arrow_DN'),
                (guiModel,
                 '**/Cannon_Arrow_RLVR')),
            relief=None,
            pos=(
                -0.199352,
                0,
                -0.00050526900000000003),
            image_hpr=(
                0,
                0,
                -90))
        self.rightButton = DirectButton(
            parent=self._CannonGui__aimPad,
            image=(
                (guiModel,
                 '**/Cannon_Arrow_UP'),
                (guiModel,
                 '**/Cannon_Arrow_DN'),
                (guiModel,
                 '**/Cannon_Arrow_RLVR')),
            relief=None,
            pos=(
                0.219167,
                0,
                -0.0010102399999999999),
            image_hpr=(
                0,
                0,
                90))
        self._CannonGui__aimPad.setColor(1, 1, 1, 0.90000000000000002)

        def bindButton(button, upHandler, downHandler):
            button.bind(DGG.B1PRESS, lambda x, handler=upHandler: handler())
            button.bind(
                DGG.B1RELEASE,
                lambda x,
                handler=downHandler: handler())

        bindButton(
            self.upButton,
            self._CannonGui__upPressed,
            self._CannonGui__upReleased)
        bindButton(
            self.downButton,
            self._CannonGui__downPressed,
            self._CannonGui__downReleased)
        bindButton(
            self.leftButton,
            self._CannonGui__leftPressed,
            self._CannonGui__leftReleased)
        bindButton(
            self.rightButton,
            self._CannonGui__rightPressed,
            self._CannonGui__rightReleased)
        self._CannonGui__loaded = True

    def unload(self):
        self.ignoreAll()
        if not self._CannonGui__loaded:
            return None

        self.disable()
        self.upButton.unbind(DGG.B1PRESS)
        self.upButton.unbind(DGG.B1RELEASE)
        self.downButton.unbind(DGG.B1PRESS)
        self.downButton.unbind(DGG.B1RELEASE)
        self.leftButton.unbind(DGG.B1PRESS)
        self.leftButton.unbind(DGG.B1RELEASE)
        self.rightButton.unbind(DGG.B1PRESS)
        self.rightButton.unbind(DGG.B1RELEASE)
        self.fireButton.destroy()
        self._CannonGui__aimPad.destroy()
        del self._CannonGui__aimPad
        del self.fireButton
        del self.upButton
        del self.downButton
        del self.leftButton
        del self.rightButton
        self._CannonGui__timerPad.destroy()
        del self._CannonGui__timerPad
        self._CannonGui__loaded = False

    def enable(self, timer=0):
        self._CannonGui__aimPad.show()
        base.setCellsAvailable([
            base.bottomCells[3],
            base.bottomCells[4]], 0)
        base.setCellsAvailable([
            base.rightCells[1]], 0)
        if timer > 0:
            self._CannonGui__timerPad.setTime(timer)
            self._CannonGui__timerPad.countdown(timer)
            self._CannonGui__timerPad.show()

        self.enableKeys()

    def disable(self):
        self._CannonGui__aimPad.hide()
        base.setCellsAvailable([
            base.bottomCells[3],
            base.bottomCells[4]], 1)
        base.setCellsAvailable([
            base.rightCells[1]], 1)
        self._CannonGui__timerPad.hide()
        self.disableKeys()

    def enableKeys(self):
        self.enableAimKeys()
        self.enableFireKey()

    def disableKeys(self):
        self._CannonGui__aimPad.hide()
        self.disableAimKeys()
        self.disableFireKey()

    def enableAimKeys(self):
        self.leftPressed = 0
        self.rightPressed = 0
        self.upPressed = 0
        self.downPressed = 0
        self.accept(self.UP_KEY, self._CannonGui__upKeyPressed)
        self.accept(self.DOWN_KEY, self._CannonGui__downKeyPressed)
        self.accept(self.LEFT_KEY, self._CannonGui__leftKeyPressed)
        self.accept(self.RIGHT_KEY, self._CannonGui__rightKeyPressed)

    def disableAimKeys(self):
        self.ignore(self.UP_KEY)
        self.ignore(self.DOWN_KEY)
        self.ignore(self.LEFT_KEY)
        self.ignore(self.RIGHT_KEY)
        messenger.send(self.UP_KEY + '-up')
        messenger.send(self.DOWN_KEY + '-up')
        messenger.send(self.LEFT_KEY + '-up')
        messenger.send(self.RIGHT_KEY + '-up')
        self.ignore(self.UP_KEY + '-up')
        self.ignore(self.DOWN_KEY + '-up')
        self.ignore(self.LEFT_KEY + '-up')
        self.ignore(self.RIGHT_KEY + '-up')

    def enableFireKey(self):
        self.accept(self.FIRE_KEY, self._CannonGui__fireKeyPressed)

    def disableFireKey(self):
        self.ignore(self.FIRE_KEY)
        self.ignore(self.FIRE_KEY + '-up')

    def _CannonGui__fireKeyPressed(self):
        self.ignore(self.FIRE_KEY)
        self.accept(self.FIRE_KEY + '-up', self._CannonGui__fireKeyReleased)
        self._CannonGui__firePressed()

    def _CannonGui__upKeyPressed(self):
        self.ignore(self.UP_KEY)
        self.accept(self.UP_KEY + '-up', self._CannonGui__upKeyReleased)
        self._CannonGui__upPressed()

    def _CannonGui__downKeyPressed(self):
        self.ignore(self.DOWN_KEY)
        self.accept(self.DOWN_KEY + '-up', self._CannonGui__downKeyReleased)
        self._CannonGui__downPressed()

    def _CannonGui__leftKeyPressed(self):
        self.ignore(self.LEFT_KEY)
        self.accept(self.LEFT_KEY + '-up', self._CannonGui__leftKeyReleased)
        self._CannonGui__leftPressed()

    def _CannonGui__rightKeyPressed(self):
        self.ignore(self.RIGHT_KEY)
        self.accept(self.RIGHT_KEY + '-up', self._CannonGui__rightKeyReleased)
        self._CannonGui__rightPressed()

    def _CannonGui__fireKeyReleased(self):
        self.ignore(self.FIRE_KEY + '-up')
        self.accept(self.FIRE_KEY, self._CannonGui__fireKeyPressed)

    def _CannonGui__leftKeyReleased(self):
        self.ignore(self.LEFT_KEY + '-up')
        self.accept(self.LEFT_KEY, self._CannonGui__leftKeyPressed)
        self._CannonGui__leftReleased()

    def _CannonGui__rightKeyReleased(self):
        self.ignore(self.RIGHT_KEY + '-up')
        self.accept(self.RIGHT_KEY, self._CannonGui__rightKeyPressed)
        self._CannonGui__rightReleased()

    def _CannonGui__upKeyReleased(self):
        self.ignore(self.UP_KEY + '-up')
        self.accept(self.UP_KEY, self._CannonGui__upKeyPressed)
        self._CannonGui__upReleased()

    def _CannonGui__downKeyReleased(self):
        self.ignore(self.DOWN_KEY + '-up')
        self.accept(self.DOWN_KEY, self._CannonGui__downKeyPressed)
        self._CannonGui__downReleased()

    def _CannonGui__upPressed(self):
        self.notify.debug('up pressed')
        self.upPressed = self._CannonGui__enterControlActive(self.upPressed)

    def _CannonGui__downPressed(self):
        self.notify.debug('down pressed')
        self.downPressed = self._CannonGui__enterControlActive(
            self.downPressed)

    def _CannonGui__leftPressed(self):
        self.notify.debug('left pressed')
        self.leftPressed = self._CannonGui__enterControlActive(
            self.leftPressed)

    def _CannonGui__rightPressed(self):
        self.notify.debug('right pressed')
        self.rightPressed = self._CannonGui__enterControlActive(
            self.rightPressed)

    def _CannonGui__upReleased(self):
        self.notify.debug('up released')
        self.upPressed = self._CannonGui__exitControlActive(self.upPressed)

    def _CannonGui__downReleased(self):
        self.notify.debug('down released')
        self.downPressed = self._CannonGui__exitControlActive(self.downPressed)

    def _CannonGui__leftReleased(self):
        self.notify.debug('left released')
        self.leftPressed = self._CannonGui__exitControlActive(self.leftPressed)

    def _CannonGui__rightReleased(self):
        self.notify.debug('right released')
        self.rightPressed = self._CannonGui__exitControlActive(
            self.rightPressed)

    def _CannonGui__firePressed(self):
        self.notify.debug('fire pressed')
        messenger.send(CannonGui.FIRE_PRESSED)

    def _CannonGui__enterControlActive(self, control):
        return control + 1

    def _CannonGui__exitControlActive(self, control):
        return max(0, control - 1)
