from PlayingCard import PlayingCardNodePath
import PlayingCardGlobals
from pandac.PandaModules import NodePath, Vec3
from direct.interval.IntervalGlobal import LerpHprInterval, Parallel, SoundInterval


class PairingGameCard(PlayingCardNodePath):
    DoIntervalDefault = True
    FlipTime = 0.25
    UseDifferentCardColors = True
    CardColors = [
        (0.93359400000000003, 0.265625, 0.28125, 1.0),
        (0.55078099999999997, 0.82421900000000003, 0.32421899999999998, 1.0),
        (0.34765600000000002, 0.82031200000000004, 0.953125, 1.0),
        (0.46093800000000001, 0.37890600000000002, 0.82421900000000003, 1.0),
        (0.71093799999999996, 0.234375, 0.4375, 1.0),
        (0.28515600000000002, 0.328125, 0.72656200000000004, 1.0),
        (0.24218799999999999, 0.74218799999999996, 0.515625, 1.0),
        (0.96875, 0.69140599999999997, 0.69921900000000003, 1.0),
        (0.99609400000000003, 0.95703099999999997, 0.59765599999999997, 1.0),
        (0.99218799999999996, 0.48046899999999998, 0.16796900000000001, 1.0)
    ]

    def __init__(self, value):
        style = PlayingCardGlobals.Styles[0]
        PlayingCardNodePath.__init__(self, style, value)
        self.enterCallback = None
        self.exitCallback = None

    def load(self):
        oneCard = loader.loadModel(
            'phase_4/models/minigames/garden_sign_memory')
        prop = self.attachNewNode('prop')
        PlayingCardGlobals.getImage(self.style, self.suit,
                                    self.rank).copyTo(prop)
        prop.setScale(7)
        oneCard.find('**/glow').removeNode()
        cs = oneCard.find('**/collision')
        for solidIndex in range(cs.node().getNumSolids()):
            cs.node().modifySolid(solidIndex).setTangible(False)

        cs.node().setName('cardCollision-%d' % self.value)
        sign = oneCard.find('**/sign1')
        if self.UseDifferentCardColors:
            index = self.rank % len(self.CardColors)
            color = self.CardColors[index]
            sign.setColorScale(*color)

        prop.setPos(0.0, 0.0, 0.080000000000000002)
        prop.setP(-90)
        prop.reparentTo(oneCard)
        oneCard.reparentTo(self)
        cardBack = oneCard.find('**/sign2')
        cardBack.setColorScale(0.12, 0.34999999999999998, 0.5, 1.0)
        cardModel = loader.loadModel('phase_3.5/models/gui/playingCard')
        logo = cardModel.find('**/logo')
        logo.reparentTo(self)
        logo.setScale(0.45000000000000001)
        logo.setP(90)
        logo.setZ(0.025000000000000001)
        logo.setX(-0.050000000000000003)
        logo.setH(180)
        cardModel.remove()
        self.setR(0)
        self.setScale(2.5)
        self.flipIval = None
        self.turnUpSound = base.loadSfx(
            'phase_4/audio/sfx/MG_pairing_card_flip_face_up.mp3')
        self.turnDownSound = base.loadSfx(
            'phase_4/audio/sfx/MG_pairing_card_flip_face_down.mp3')

    def unload(self):
        self.clearFlipIval()
        self.removeNode()
        del self.turnUpSound
        del self.turnDownSound

    def turnUp(self, doInterval=DoIntervalDefault):
        self.faceUp = 1
        if doInterval:
            self.clearFlipIval()
            self.flipIval = Parallel(
                LerpHprInterval(self, self.FlipTime, Vec3(0, 0, 0)),
                SoundInterval(
                    self.turnUpSound,
                    node=self,
                    listenerNode=base.localAvatar,
                    cutOff=240))
            self.flipIval.start()
        else:
            self.setR(0)

    def clearFlipIval(self):
        if self.flipIval:
            self.flipIval.finish()
            self.flipIval = None

    def turnDown(self, doInterval=DoIntervalDefault):
        self.faceUp = 0
        if doInterval:
            self.clearFlipIval()
            self.flipIval = Parallel(
                LerpHprInterval(self, self.FlipTime, Vec3(0, 0, 180)),
                SoundInterval(
                    self.turnDownSound,
                    node=self,
                    listenerNode=base.localAvatar,
                    cutOff=240))
            self.flipIval.start()
        else:
            self.setR(180)
