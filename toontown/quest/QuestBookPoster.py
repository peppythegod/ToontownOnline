from QuestPoster import *
IMAGE_SCALE_LARGE = 0.14999999999999999
IMAGE_SCALE_SMALL = 0.10000000000000001
POSTER_WIDTH = 0.69999999999999996
TEXT_SCALE = TTLocalizer.QPtextScale * 0.69999999999999996
TEXT_WORDWRAP = TTLocalizer.QPtextWordwrap * 0.80000000000000004


class QuestBookPoster(QuestPoster):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestPoster')
    colors = {
        'white': (1, 1, 1, 1),
        'blue': (0.45000000000000001, 0.45000000000000001, 0.80000000000000004, 1),
        'lightBlue': (0.41999999999999998, 0.67100000000000004, 1.0, 1.0),
        'green': (0.45000000000000001, 0.80000000000000004, 0.45000000000000001, 1),
        'lightGreen': (0.78400000000000003, 1, 0.86299999999999999, 1),
        'red': (0.80000000000000004, 0.45000000000000001, 0.45000000000000001, 1),
        'rewardRed': (0.80000000000000004, 0.29999999999999999, 0.29999999999999999, 1),
        'brightRed': (1.0, 0.16, 0.16, 1.0),
        'brown': (0.52000000000000002, 0.41999999999999998, 0.22, 1)}
    normalTextColor = (0.29999999999999999, 0.25, 0.20000000000000001, 1)
    confirmDeleteButtonEvent = 'confirmDeleteButtonEvent'

    def __init__(self, parent=aspect2d, **kw):
        bookModel = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
        questCard = bookModel.find('**/questCard')
        optiondefs = (
            ('relief',
             None,
             None),
            ('reverse',
             0,
             None),
            ('mapIndex',
             0,
             None),
            ('image',
             questCard,
             None),
            ('image_scale',
             (0.80000000000000004,
              1.0,
              0.57999999999999996),
                None),
            ('state',
             DGG.NORMAL,
             None))
        self.defineoptions(kw, optiondefs)
        QuestPoster.__init__(self, relief=None)
        self.initialiseoptions(QuestBookPoster)
        self._deleteCallback = None
        self.questFrame = DirectFrame(parent=self, relief=None)
        gui = loader.loadModel(
            'phase_4/models/parties/schtickerbookHostingGUI')
        icon = gui.find('**/startPartyButton_inactive')
        iconNP = aspect2d.attachNewNode('iconNP')
        icon.reparentTo(iconNP)
        icon.setX((-12.0792 + 0.20000000000000001) / 30.48)
        icon.setZ((-9.7403999999999993 + 1) / 30.48)
        self.mapIndex = DirectLabel(
            parent=self.questFrame,
            relief=None,
            text='%s' % self['mapIndex'],
            text_fg=(
                1,
                1,
                1,
                1),
            text_scale=0.035000000000000003,
            text_align=TextNode.ACenter,
            image=iconNP,
            image_scale=0.29999999999999999,
            image_color=(
                1,
                0,
                0,
                1),
            pos=(
                -0.29999999999999999,
                0,
                0.14999999999999999))
        self.mapIndex.hide()
        iconNP.removeNode()
        gui.removeNode()
        bookModel.removeNode()
        self.reverseBG(self['reverse'])
        self.laffMeter = None

    def reverseBG(self, reverse=0):

        try:
            pass
        except AttributeError:
            self.initImageScale = self['image_scale']
            if reverse:
                self.initImageScale.setX(-abs(self.initImageScale[0]))
                self.questFrame.setX(0.014999999999999999)
            else:
                self.initImageScale.setX(abs(self.initImageScale[0]))
            self['image_scale'] = self.initImageScale
