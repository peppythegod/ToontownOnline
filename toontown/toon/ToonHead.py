from direct.actor import Actor
from direct.task import Task
from toontown.toonbase import ToontownGlobals
import string
import random
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.directnotify import DirectNotifyGlobal
if not base.config.GetBool('want-new-anims', 1):
    HeadDict = {
        'dls': '/models/char/dogMM_Shorts-head-',
        'dss': '/models/char/dogMM_Skirt-head-',
        'dsl': '/models/char/dogSS_Shorts-head-',
        'dll': '/models/char/dogLL_Shorts-head-',
        'c': '/models/char/cat-heads-',
        'h': '/models/char/horse-heads-',
        'm': '/models/char/mouse-heads-',
        'r': '/models/char/rabbit-heads-',
        'f': '/models/char/duck-heads-',
        'p': '/models/char/monkey-heads-',
        'b': '/models/char/bear-heads-',
        's': '/models/char/pig-heads-'
    }
else:
    HeadDict = {
        'dls': '/models/char/tt_a_chr_dgm_shorts_head_',
        'dss': '/models/char/tt_a_chr_dgm_skirt_head_',
        'dsl': '/models/char/tt_a_chr_dgs_shorts_head_',
        'dll': '/models/char/tt_a_chr_dgl_shorts_head_',
        'c': '/models/char/cat-heads-',
        'h': '/models/char/horse-heads-',
        'm': '/models/char/mouse-heads-',
        'r': '/models/char/rabbit-heads-',
        'f': '/models/char/duck-heads-',
        'p': '/models/char/monkey-heads-',
        'b': '/models/char/bear-heads-',
        's': '/models/char/pig-heads-'
    }
EyelashDict = {
    'd': '/models/char/dog-lashes',
    'c': '/models/char/cat-lashes',
    'h': '/models/char/horse-lashes',
    'm': '/models/char/mouse-lashes',
    'r': '/models/char/rabbit-lashes',
    'f': '/models/char/duck-lashes',
    'p': '/models/char/monkey-lashes',
    'b': '/models/char/bear-lashes',
    's': '/models/char/pig-lashes'
}
DogMuzzleDict = {
    'dls': '/models/char/dogMM_Shorts-headMuzzles-',
    'dss': '/models/char/dogMM_Skirt-headMuzzles-',
    'dsl': '/models/char/dogSS_Shorts-headMuzzles-',
    'dll': '/models/char/dogLL_Shorts-headMuzzles-'
}


class ToonHead(Actor.Actor):
    notify = DirectNotifyGlobal.directNotify.newCategory('ToonHead')
    EyesOpen = loader.loadTexture('phase_3/maps/eyes.jpg',
                                  'phase_3/maps/eyes_a.rgb')
    EyesOpen.setMinfilter(Texture.FTLinear)
    EyesOpen.setMagfilter(Texture.FTLinear)
    EyesClosed = loader.loadTexture('phase_3/maps/eyesClosed.jpg',
                                    'phase_3/maps/eyesClosed_a.rgb')
    EyesClosed.setMinfilter(Texture.FTLinear)
    EyesClosed.setMagfilter(Texture.FTLinear)
    EyesSadOpen = loader.loadTexture('phase_3/maps/eyesSad.jpg',
                                     'phase_3/maps/eyesSad_a.rgb')
    EyesSadOpen.setMinfilter(Texture.FTLinear)
    EyesSadOpen.setMagfilter(Texture.FTLinear)
    EyesSadClosed = loader.loadTexture('phase_3/maps/eyesSadClosed.jpg',
                                       'phase_3/maps/eyesSadClosed_a.rgb')
    EyesSadClosed.setMinfilter(Texture.FTLinear)
    EyesSadClosed.setMagfilter(Texture.FTLinear)
    EyesAngryOpen = loader.loadTexture('phase_3/maps/eyesAngry.jpg',
                                       'phase_3/maps/eyesAngry_a.rgb')
    EyesAngryOpen.setMinfilter(Texture.FTLinear)
    EyesAngryOpen.setMagfilter(Texture.FTLinear)
    EyesAngryClosed = loader.loadTexture('phase_3/maps/eyesAngryClosed.jpg',
                                         'phase_3/maps/eyesAngryClosed_a.rgb')
    EyesAngryClosed.setMinfilter(Texture.FTLinear)
    EyesAngryClosed.setMagfilter(Texture.FTLinear)
    EyesSurprised = loader.loadTexture('phase_3/maps/eyesSurprised.jpg',
                                       'phase_3/maps/eyesSurprised_a.rgb')
    EyesSurprised.setMinfilter(Texture.FTLinear)
    EyesSurprised.setMagfilter(Texture.FTLinear)
    Muzzle = loader.loadTexture('phase_3/maps/muzzleShrtGeneric.jpg')
    Muzzle.setMinfilter(Texture.FTLinear)
    Muzzle.setMagfilter(Texture.FTLinear)
    MuzzleSurprised = loader.loadTexture(
        'phase_3/maps/muzzleShortSurprised.jpg')
    MuzzleSurprised.setMinfilter(Texture.FTLinear)
    MuzzleSurprised.setMagfilter(Texture.FTLinear)
    LeftA = Point3(0.059999999999999998, 0.0, 0.14000000000000001)
    LeftB = Point3(-0.13, 0.0, 0.10000000000000001)
    LeftC = Point3(-0.050000000000000003, 0.0, 0.0)
    LeftD = Point3(0.059999999999999998, 0.0, 0.0)
    RightA = Point3(0.13, 0.0, 0.10000000000000001)
    RightB = Point3(-0.059999999999999998, 0.0, 0.14000000000000001)
    RightC = Point3(-0.059999999999999998, 0.0, 0.0)
    RightD = Point3(0.050000000000000003, 0.0, 0.0)
    LeftAD = Point3(
        LeftA[0] - LeftA[2] * (LeftD[0] - LeftA[0]) / (LeftD[2] - LeftA[2]),
        0.0, 0.0)
    LeftBC = Point3(
        LeftB[0] - LeftB[2] * (LeftC[0] - LeftB[0]) / (LeftC[2] - LeftB[2]),
        0.0, 0.0)
    RightAD = Point3(
        RightA[0] -
        RightA[2] * (RightD[0] - RightA[0]) / (RightD[2] - RightA[2]), 0.0,
        0.0)
    RightBC = Point3(
        RightB[0] -
        RightB[2] * (RightC[0] - RightB[0]) / (RightC[2] - RightB[2]), 0.0,
        0.0)

    def __init__(self):

        try:
            pass
        except:
            self.ToonHead_initialized = 1
            Actor.Actor.__init__(self)
            self.toonName = 'ToonHead-' + str(self.this)
            self._ToonHead__blinkName = 'blink-' + self.toonName
            self._ToonHead__stareAtName = 'stareAt-' + self.toonName
            self._ToonHead__lookName = 'look-' + self.toonName
            self.lookAtTrack = None
            self._ToonHead__eyes = None
            self._ToonHead__eyelashOpen = None
            self._ToonHead__eyelashClosed = None
            self._ToonHead__lod500Eyes = None
            self._ToonHead__lod250Eyes = None
            self._ToonHead__lpupil = None
            self._ToonHead__lod500lPupil = None
            self._ToonHead__lod250lPupil = None
            self._ToonHead__rpupil = None
            self._ToonHead__lod500rPupil = None
            self._ToonHead__lod250rPupil = None
            self._ToonHead__muzzle = None
            self._ToonHead__eyesOpen = ToonHead.EyesOpen
            self._ToonHead__eyesClosed = ToonHead.EyesClosed
            self._ToonHead__height = 0.0
            self._ToonHead__eyelashesHiddenByGlasses = False
            self.randGen = random.Random()
            self.randGen.seed(random.random())
            self.eyelids = ClassicFSM('eyelids', [
                State('off', self.enterEyelidsOff, self.exitEyelidsOff,
                      ['open', 'closed', 'surprised']),
                State('open', self.enterEyelidsOpen, self.exitEyelidsOpen,
                      ['closed', 'surprised', 'off']),
                State('surprised', self.enterEyelidsSurprised,
                      self.exitEyelidsSurprised, ['open', 'closed', 'off']),
                State('closed', self.enterEyelidsClosed,
                      self.exitEyelidsClosed, ['open', 'surprised', 'off'])
            ], 'off', 'off')
            self.eyelids.enterInitialState()
            self.emote = None
            self._ToonHead__stareAtNode = NodePath()
            self._ToonHead__defaultStarePoint = Point3(0, 0, 0)
            self._ToonHead__stareAtPoint = self._ToonHead__defaultStarePoint
            self._ToonHead__stareAtTime = 0
            self.lookAtPositionCallbackArgs = None

    def delete(self):

        try:
            pass
        except:
            self.ToonHead_deleted = 1
            taskMgr.remove(self._ToonHead__blinkName)
            taskMgr.remove(self._ToonHead__lookName)
            taskMgr.remove(self._ToonHead__stareAtName)
            if self.lookAtTrack:
                self.lookAtTrack.finish()
                self.lookAtTrack = None

            del self.eyelids
            del self._ToonHead__stareAtNode
            del self._ToonHead__stareAtPoint
            if self._ToonHead__eyes:
                del self._ToonHead__eyes

            if self._ToonHead__lpupil:
                del self._ToonHead__lpupil

            if self._ToonHead__rpupil:
                del self._ToonHead__rpupil

            if self._ToonHead__eyelashOpen:
                del self._ToonHead__eyelashOpen

            if self._ToonHead__eyelashClosed:
                del self._ToonHead__eyelashClosed

            self.lookAtPositionCallbackArgs = None
            Actor.Actor.delete(self)

    def setupHead(self, dna, forGui=0):
        self._ToonHead__height = self.generateToonHead(1, dna, ('1000', ),
                                                       forGui)
        self.generateToonColor(dna)
        animalStyle = dna.getAnimal()
        bodyScale = ToontownGlobals.toonBodyScales[animalStyle]
        headScale = ToontownGlobals.toonHeadScales[animalStyle]
        self.getGeomNode().setScale(headScale[0] * bodyScale * 1.3,
                                    headScale[1] * bodyScale * 1.3,
                                    headScale[2] * bodyScale * 1.3)
        if forGui:
            self.getGeomNode().setDepthWrite(1)
            self.getGeomNode().setDepthTest(1)

        if dna.getAnimal() == 'dog':
            self.loop('neutral')

    def fitAndCenterHead(self, maxDim, forGui=0):
        p1 = Point3()
        p2 = Point3()
        self.calcTightBounds(p1, p2)
        if forGui:
            h = 180
            t = p1[0]
            p1.setX(-p2[0])
            p2.setX(-t)
        else:
            h = 0
        d = p2 - p1
        biggest = max(d[0], d[2])
        s = maxDim / biggest
        mid = (p1 + d / 2.0) * s
        self.setPosHprScale(-mid[0], -mid[1] + 1, -mid[2], h, 0, 0, s, s, s)

    def setLookAtPositionCallbackArgs(self, argTuple):
        self.lookAtPositionCallbackArgs = argTuple

    def getHeight(self):
        return self._ToonHead__height

    def getRandomForwardLookAtPoint(self):
        x = self.randGen.choice((-0.80000000000000004, -0.5, 0, 0.5,
                                 0.80000000000000004))
        z = self.randGen.choice((-0.5, 0, 0.5, 0.80000000000000004))
        return Point3(x, 1.5, z)

    def findSomethingToLookAt(self):
        if self.lookAtPositionCallbackArgs != None:
            pnt = self.lookAtPositionCallbackArgs[0].getLookAtPosition(
                self.lookAtPositionCallbackArgs[1],
                self.lookAtPositionCallbackArgs[2])
            self.startStareAt(self, pnt)
            return None

        if self.randGen.random() < 0.33000000000000002:
            lookAtPnt = self.getRandomForwardLookAtPoint()
        else:
            lookAtPnt = self._ToonHead__defaultStarePoint
        self.lerpLookAt(lookAtPnt, blink=1)

    def generateToonHead(self, copy, style, lods, forGui=0):
        headStyle = style.head
        fix = None
        if headStyle == 'dls':
            filePrefix = HeadDict['dls']
            headHeight = 0.75
        elif headStyle == 'dss':
            filePrefix = HeadDict['dss']
            headHeight = 0.5
        elif headStyle == 'dsl':
            filePrefix = HeadDict['dsl']
            headHeight = 0.5
        elif headStyle == 'dll':
            filePrefix = HeadDict['dll']
            headHeight = 0.75
        elif headStyle == 'cls':
            filePrefix = HeadDict['c']
            fix = self._ToonHead__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'css':
            filePrefix = HeadDict['c']
            fix = self._ToonHead__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'csl':
            filePrefix = HeadDict['c']
            fix = self._ToonHead__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'cll':
            filePrefix = HeadDict['c']
            fix = self._ToonHead__fixHeadLongLong
            headHeight = 0.75
        elif headStyle == 'hls':
            filePrefix = HeadDict['h']
            fix = self._ToonHead__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'hss':
            filePrefix = HeadDict['h']
            fix = self._ToonHead__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'hsl':
            filePrefix = HeadDict['h']
            fix = self._ToonHead__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'hll':
            filePrefix = HeadDict['h']
            fix = self._ToonHead__fixHeadLongLong
            headHeight = 0.75
        elif headStyle == 'mls':
            filePrefix = HeadDict['m']
            fix = self._ToonHead__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'mss':
            filePrefix = HeadDict['m']
            fix = self._ToonHead__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'rls':
            filePrefix = HeadDict['r']
            fix = self._ToonHead__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'rss':
            filePrefix = HeadDict['r']
            fix = self._ToonHead__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'rsl':
            filePrefix = HeadDict['r']
            fix = self._ToonHead__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'rll':
            filePrefix = HeadDict['r']
            fix = self._ToonHead__fixHeadLongLong
            headHeight = 0.75
        elif headStyle == 'fls':
            filePrefix = HeadDict['f']
            fix = self._ToonHead__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'fss':
            filePrefix = HeadDict['f']
            fix = self._ToonHead__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'fsl':
            filePrefix = HeadDict['f']
            fix = self._ToonHead__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'fll':
            filePrefix = HeadDict['f']
            fix = self._ToonHead__fixHeadLongLong
            headHeight = 0.75
        elif headStyle == 'pls':
            filePrefix = HeadDict['p']
            fix = self._ToonHead__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'pss':
            filePrefix = HeadDict['p']
            fix = self._ToonHead__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'psl':
            filePrefix = HeadDict['p']
            fix = self._ToonHead__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'pll':
            filePrefix = HeadDict['p']
            fix = self._ToonHead__fixHeadLongLong
            headHeight = 0.75
        elif headStyle == 'bls':
            filePrefix = HeadDict['b']
            fix = self._ToonHead__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'bss':
            filePrefix = HeadDict['b']
            fix = self._ToonHead__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'bsl':
            filePrefix = HeadDict['b']
            fix = self._ToonHead__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'bll':
            filePrefix = HeadDict['b']
            fix = self._ToonHead__fixHeadLongLong
            headHeight = 0.75
        elif headStyle == 'sls':
            filePrefix = HeadDict['s']
            fix = self._ToonHead__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'sss':
            filePrefix = HeadDict['s']
            fix = self._ToonHead__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'ssl':
            filePrefix = HeadDict['s']
            fix = self._ToonHead__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'sll':
            filePrefix = HeadDict['s']
            fix = self._ToonHead__fixHeadLongLong
            headHeight = 0.75
        else:
            ToonHead.notify.error('unknown head style: %s' % headStyle)
        if len(lods) == 1:
            self.loadModel('phase_3' + filePrefix + lods[0], 'head', 'lodRoot',
                           copy)
            if not forGui:
                pLoaded = self.loadPumpkin(headStyle[1], None, copy)
                self.loadSnowMan(headStyle[1], None, copy)

            if not copy:
                self.showAllParts('head')

            if fix != None:
                fix(style, None, copy)

            if not forGui:
                if pLoaded:
                    self._ToonHead__fixPumpkin(style, None, copy)
                else:
                    self._ToonHead__lods = lods
                    self._ToonHead__style = style
                    self._ToonHead__headStyle = headStyle
                    self._ToonHead__copy = copy

        else:
            for lod in lods:
                self.loadModel('phase_3' + filePrefix + lod, 'head', lod, copy)
                if not forGui:
                    pLoaded = self.loadPumpkin(headStyle[1], lod, copy)
                    self.loadSnowMan(headStyle[1], lod, copy)

                if not copy:
                    self.showAllParts('head', lod)

                if fix != None:
                    fix(style, lod, copy)

                if not forGui:
                    if pLoaded:
                        self._ToonHead__fixPumpkin(style, lod, copy)
                    else:
                        self._ToonHead__lods = lods
                        self._ToonHead__style = style
                        self._ToonHead__headStyle = headStyle
                        self._ToonHead__copy = copy

        self._ToonHead__fixEyes(style, forGui)
        self.setupEyelashes(style)
        self.eyelids.request('closed')
        self.eyelids.request('open')
        self.setupMuzzles(style)
        return headHeight

    def loadPumpkin(self, headStyle, lod, copy):
        if hasattr(base, 'launcher'):
            if (not (base.launcher)
                    or base.launcher) and base.launcher.getPhaseComplete(4):
                if not hasattr(self, 'pumpkins'):
                    self.pumpkins = NodePathCollection()

                ppath = 'phase_4/models/estate/pumpkin_'
                if headStyle is 'l':
                    if copy:
                        pmodel = loader.loadModel(ppath + 'tall')
                    else:
                        pmodel = loader.loadModel(ppath + 'tall')
                    ptype = 'tall'
                elif copy:
                    pmodel = loader.loadModel(ppath + 'short')
                else:
                    pmodel = loader.loadModel(ppath + 'short')
                ptype = 'short'
                if pmodel:
                    p = pmodel.find('**/pumpkin_' + ptype + '*')
                    p.setScale(0.5)
                    p.setZ(-0.5)
                    p.setH(180)
                    if lod:
                        p.reparentTo(
                            self.find('**/' + lod + '/**/__Actor_head'))
                    else:
                        p.reparentTo(self.find('**/__Actor_head'))
                    self.pumpkins.addPath(p)
                    pmodel.remove()
                    return True
                else:
                    del self.pumpkins
                    return False
            else:
                ToonHead.notify.debug(
                    'phase_4 not complete yet. Postponing pumpkin head load.')

    def loadSnowMan(self, headStyle, lod, copy):
        if hasattr(base, 'launcher'):
            if (not (base.launcher)
                    or base.launcher) and base.launcher.getPhaseComplete(4):
                if not hasattr(self, 'snowMen'):
                    self.snowMen = NodePathCollection()

                snowManPath = 'phase_4/models/props/tt_m_efx_snowmanHead_'
                if headStyle is 'l':
                    snowManPath = snowManPath + 'tall'
                else:
                    snowManPath = snowManPath + 'short'
                model = loader.loadModel(snowManPath)
                if model:
                    model.setZ(-0.5)
                    model.setH(180)
                    if lod:
                        model.reparentTo(self.getPart('head', lod))
                    else:
                        model.reparentTo(self.find('**/__Actor_head'))
                    self.snowMen.addPath(model)
                    model.stash()
                    return True
                else:
                    del self.snowMen
                    return False
            else:
                ToonHead.notify.debug('phase_4 not loaded yet.')

    def _ToonHead__fixPumpkin(self, style, lodName=None, copy=1):
        if lodName == None:
            searchRoot = self
        else:
            searchRoot = self.find('**/' + str(lodName))
        pumpkin = searchRoot.find('**/__Actor_head/pumpkin*')
        pumpkin.stash()

    def enablePumpkins(self, enable):
        if not hasattr(self, 'pumpkins'):
            if len(self._ToonHead__lods) == 1:
                pLoaded = self.loadPumpkin(self._ToonHead__headStyle[1], None,
                                           self._ToonHead__copy)
                if pLoaded:
                    self._ToonHead__fixPumpkin(self._ToonHead__style, None,
                                               self._ToonHead__copy)

            else:
                for lod in self._ToonHead__lods:
                    pLoaded = self.loadPumpkin(self._ToonHead__headStyle[1],
                                               lod, self._ToonHead__copy)
                    if pLoaded:
                        self._ToonHead__fixPumpkin(self._ToonHead__style, lod,
                                                   self._ToonHead__copy)
                        continue

            if hasattr(self, 'pumpkins'):
                for x in ['__lods', '__style', '__headStyle', '__copy']:
                    if hasattr(self, '_ToonHead' + x):
                        delattr(self, '_ToonHead' + x)
                        continue

        if hasattr(self, 'pumpkins'):
            if enable:
                if self._ToonHead__eyelashOpen:
                    self._ToonHead__eyelashOpen.stash()

                if self._ToonHead__eyelashClosed:
                    self._ToonHead__eyelashClosed.stash()

                self.pumpkins.unstash()
            elif not self._ToonHead__eyelashesHiddenByGlasses:
                if self._ToonHead__eyelashOpen:
                    self._ToonHead__eyelashOpen.unstash()

                if self._ToonHead__eyelashClosed:
                    self._ToonHead__eyelashClosed.unstash()

            self.pumpkins.stash()

    def enableSnowMen(self, enable):
        if not hasattr(self, 'snowMen'):
            if len(self._ToonHead__lods) == 1:
                self.loadSnowMan(self._ToonHead__headStyle[1], None,
                                 self._ToonHead__copy)
            else:
                for lod in self._ToonHead__lds:
                    self.loadSnowMan(self._ToonHead__headStyle[1], lod,
                                     self._ToonHead__copy)

        if hasattr(self, 'snowMen'):
            if enable:
                if self._ToonHead__eyelashOpen:
                    self._ToonHead__eyelashOpen.stash()

                if self._ToonHead__eyelashClosed:
                    self._ToonHead__eyelashClosed.stash()

                self.snowMen.unstash()
            elif not self._ToonHead__eyelashesHiddenByGlasses:
                if self._ToonHead__eyelashOpen:
                    self._ToonHead__eyelashOpen.unstash()

                if self._ToonHead__eyelashClosed:
                    self._ToonHead__eyelashClosed.unstash()

            self.snowMen.stash()

    def hideEars(self):
        self.findAllMatches('**/ears*;+s').stash()

    def showEars(self):
        self.findAllMatches('**/ears*;+s').unstash()

    def hideEyelashes(self):
        if self._ToonHead__eyelashOpen:
            self._ToonHead__eyelashOpen.stash()

        if self._ToonHead__eyelashClosed:
            self._ToonHead__eyelashClosed.stash()

        self._ToonHead__eyelashesHiddenByGlasses = True

    def showEyelashes(self):
        if self._ToonHead__eyelashOpen:
            self._ToonHead__eyelashOpen.unstash()

        if self._ToonHead__eyelashClosed:
            self._ToonHead__eyelashClosed.unstash()

        self._ToonHead__eyelashesHiddenByGlasses = False

    def generateToonColor(self, style):
        parts = self.findAllMatches('**/head*')
        parts.setColor(style.getHeadColor())
        animalType = style.getAnimal()
        if animalType == 'cat' and animalType == 'rabbit' and animalType == 'bear' and animalType == 'mouse' or animalType == 'pig':
            parts = self.findAllMatches('**/ear?-*')
            parts.setColor(style.getHeadColor())

    def _ToonHead__fixEyes(self, style, forGui=0):
        mode = -3
        if forGui:
            mode = -2

        if self.hasLOD():
            for lodName in self.getLODNames():
                self.drawInFront('eyes*', 'head-front*', mode, lodName=lodName)
                if base.config.GetBool('want-new-anims', 1):
                    if not self.find('**/joint_pupil*').isEmpty():
                        self.drawInFront(
                            'joint_pupil*', 'eyes*', -1, lodName=lodName)
                    else:
                        self.drawInFront(
                            'def_*_pupil', 'eyes*', -1, lodName=lodName)
                self.find('**/joint_pupil*').isEmpty()
                self.drawInFront('joint_pupil*', 'eyes*', -1, lodName=lodName)

            self._ToonHead__eyes = self.getLOD(1000).find('**/eyes*')
            self._ToonHead__lod500Eyes = self.getLOD(500).find('**/eyes*')
            self._ToonHead__lod250Eyes = self.getLOD(250).find('**/eyes*')
            if self._ToonHead__lod500Eyes.isEmpty():
                self._ToonHead__lod500Eyes = None
            else:
                self._ToonHead__lod500Eyes.setColorOff()
                if base.config.GetBool('want-new-anims', 1):
                    if not self.find('**/joint_pupilL*').isEmpty():
                        self._ToonHead__lod500lPupil = self._ToonHead__lod500Eyes.find(
                            '**/joint_pupilL*')
                        self._ToonHead__lod500rPupil = self._ToonHead__lod500Eyes.find(
                            '**/joint_pupilR*')
                    else:
                        self._ToonHead__lod500lPupil = self._ToonHead__lod500Eyes.find(
                            '**/def_left_pupil*')
                        self._ToonHead__lod500rPupil = self._ToonHead__lod500Eyes.find(
                            '**/def_right_pupil*')
                else:
                    self._ToonHead__lod500lPupil = self._ToonHead__lod500Eyes.find(
                        '**/joint_pupilL*')
                    self._ToonHead__lod500rPupil = self._ToonHead__lod500Eyes.find(
                        '**/joint_pupilR*')
            if self._ToonHead__lod250Eyes.isEmpty():
                self._ToonHead__lod250Eyes = None
            else:
                self._ToonHead__lod250Eyes.setColorOff()
                if base.config.GetBool('want-new-anims', 1):
                    if not self.find('**/joint_pupilL*').isEmpty():
                        self._ToonHead__lod250lPupil = self._ToonHead__lod250Eyes.find(
                            '**/joint_pupilL*')
                        self._ToonHead__lod250rPupil = self._ToonHead__lod250Eyes.find(
                            '**/joint_pupilR*')
                    else:
                        self._ToonHead__lod250lPupil = self._ToonHead__lod250Eyes.find(
                            '**/def_left_pupil*')
                        self._ToonHead__lod250rPupil = self._ToonHead__lod250Eyes.find(
                            '**/def_right_pupil*')
                else:
                    self._ToonHead__lod250lPupil = self._ToonHead__lod250Eyes.find(
                        '**/joint_pupilL*')
                    self._ToonHead__lod250rPupil = self._ToonHead__lod250Eyes.find(
                        '**/joint_pupilR*')
        else:
            self.drawInFront('eyes*', 'head-front*', mode)
            if base.config.GetBool('want-new-anims', 1):
                if not self.find('joint_pupil*').isEmpty():
                    self.drawInFront('joint_pupil*', 'eyes*', -1)
                else:
                    self.drawInFront('def_*_pupil', 'eyes*', -1)
            else:
                self.drawInFront('joint_pupil*', 'eyes*', -1)
            self._ToonHead__eyes = self.find('**/eyes*')
        if not self._ToonHead__eyes.isEmpty():
            self._ToonHead__eyes.setColorOff()
            self._ToonHead__lpupil = None
            self._ToonHead__rpupil = None
            if base.config.GetBool('want-new-anims', 1):
                if not self.find('**/joint_pupilL*').isEmpty():
                    if self.getLOD(1000):
                        lp = self.getLOD(1000).find('**/joint_pupilL*')
                        rp = self.getLOD(1000).find('**/joint_pupilR*')
                    else:
                        lp = self.find('**/joint_pupilL*')
                        rp = self.find('**/joint_pupilR*')
                elif not self.getLOD(1000):
                    lp = self.find('**/def_left_pupil*')
                    rp = self.find('**/def_right_pupil*')
                else:
                    lp = self.getLOD(1000).find('**/def_left_pupil*')
                    rp = self.getLOD(1000).find('**/def_right_pupil*')
            else:
                lp = self._ToonHead__eyes.find('**/joint_pupilL*')
                rp = self._ToonHead__eyes.find('**/joint_pupilR*')
            if lp.isEmpty() or rp.isEmpty():
                print 'Unable to locate pupils.'
            else:
                leye = self._ToonHead__eyes.attachNewNode('leye')
                reye = self._ToonHead__eyes.attachNewNode('reye')
                lmat = Mat4(0.80217400000000005, 0.59709000000000001, 0, 0,
                            -0.58619100000000002, 0.78753099999999998,
                            0.190197, 0, 0.113565, -0.15257100000000001,
                            0.98174600000000001, 0, -0.23363400000000001,
                            0.41806199999999999, 0.0196875, 1)
                leye.setMat(lmat)
                rmat = Mat4(0.78678800000000004, -0.61722399999999999, 0, 0,
                            0.60283600000000004, 0.76844699999999999,
                            0.21465799999999999, 0, -0.132492,
                            -0.16889000000000001, 0.97668900000000003, 0,
                            0.23363400000000001, 0.41806199999999999,
                            0.0196875, 1)
                reye.setMat(rmat)
                self._ToonHead__lpupil = leye.attachNewNode('lpupil')
                self._ToonHead__rpupil = reye.attachNewNode('rpupil')
                lpt = self._ToonHead__eyes.attachNewNode('')
                rpt = self._ToonHead__eyes.attachNewNode('')
                lpt.wrtReparentTo(self._ToonHead__lpupil)
                rpt.wrtReparentTo(self._ToonHead__rpupil)
                lp.reparentTo(lpt)
                rp.reparentTo(rpt)
                self._ToonHead__lpupil.adjustAllPriorities(1)
                self._ToonHead__rpupil.adjustAllPriorities(1)
                if self._ToonHead__lod500Eyes:
                    self._ToonHead__lod500lPupil.adjustAllPriorities(1)
                    self._ToonHead__lod500rPupil.adjustAllPriorities(1)

                if self._ToonHead__lod250Eyes:
                    self._ToonHead__lod250lPupil.adjustAllPriorities(1)
                    self._ToonHead__lod250rPupil.adjustAllPriorities(1)

                animalType = style.getAnimal()
                if animalType != 'dog':
                    self._ToonHead__lpupil.flattenStrong()
                    self._ToonHead__rpupil.flattenStrong()

    def _ToonHead__setPupilDirection(self, x, y):
        if y < 0.0:
            y2 = -y
            left1 = self.LeftAD + (self.LeftD - self.LeftAD) * y2
            left2 = self.LeftBC + (self.LeftC - self.LeftBC) * y2
            right1 = self.RightAD + (self.RightD - self.RightAD) * y2
            right2 = self.RightBC + (self.RightC - self.RightBC) * y2
        else:
            y2 = y
            left1 = self.LeftAD + (self.LeftA - self.LeftAD) * y2
            left2 = self.LeftBC + (self.LeftB - self.LeftBC) * y2
            right1 = self.RightAD + (self.RightA - self.RightAD) * y2
            right2 = self.RightBC + (self.RightB - self.RightBC) * y2
        left0 = Point3(
            0.0, 0.0, left1[2] -
            left1[0] * (left2[2] - left1[2]) / (left2[0] - left1[0]))
        right0 = Point3(
            0.0, 0.0, right1[2] -
            right1[0] * (right2[2] - right1[2]) / (right2[0] - right1[0]))
        if x < 0.0:
            x2 = -x
            left = left0 + (left2 - left0) * x2
            right = right0 + (right2 - right0) * x2
        else:
            x2 = x
            left = left0 + (left1 - left0) * x2
            right = right0 + (right1 - right0) * x2
        self._ToonHead__lpupil.setPos(left)
        self._ToonHead__rpupil.setPos(right)

    def _ToonHead__lookPupilsAt(self, node, point):
        if node != None:
            mat = node.getMat(self._ToonHead__eyes)
            point = mat.xformPoint(point)

        distance = 1.0
        recip_z = 1.0 / max(0.10000000000000001, point[1])
        x = distance * point[0] * recip_z
        y = distance * point[2] * recip_z
        x = min(max(x, -1), 1)
        y = min(max(y, -1), 1)
        self._ToonHead__setPupilDirection(x, y)

    def _ToonHead__lookHeadAt(self, node, point, frac=1.0, lod=None):
        reachedTarget = 1
        if lod == None:
            head = self.getPart('head', self.getLODNames()[0])
        else:
            head = self.getPart('head', lod)
        if node != None:
            headParent = head.getParent()
            mat = node.getMat(headParent)
            point = mat.xformPoint(point)

        rot = Mat3(0, 0, 0, 0, 0, 0, 0, 0, 0)
        lookAt(rot, Vec3(point), Vec3(0, 0, 1), CSDefault)
        scale = VBase3(0, 0, 0)
        hpr = VBase3(0, 0, 0)
        if decomposeMatrix(rot, scale, hpr, CSDefault):
            hpr = VBase3(
                min(max(hpr[0], -60), 60), min(max(hpr[1], -20), 30), 0)
            if frac != 1:
                currentHpr = head.getHpr()
                if abs(hpr[0] - currentHpr[0]) < 1.0:
                    pass
                reachedTarget = abs(hpr[1] - currentHpr[1]) < 1.0
                hpr = currentHpr + (hpr - currentHpr) * frac

            if lod == None:
                for lodName in self.getLODNames():
                    head = self.getPart('head', lodName)
                    head.setHpr(hpr)

            else:
                head.setHpr(hpr)

        return reachedTarget

    def setupEyelashes(self, style):
        if style.getGender() == 'm':
            if self._ToonHead__eyelashOpen:
                self._ToonHead__eyelashOpen.removeNode()
                self._ToonHead__eyelashOpen = None

            if self._ToonHead__eyelashClosed:
                self._ToonHead__eyelashClosed.removeNode()
                self._ToonHead__eyelashClosed = None

        elif self._ToonHead__eyelashOpen:
            self._ToonHead__eyelashOpen.removeNode()

        if self._ToonHead__eyelashClosed:
            self._ToonHead__eyelashClosed.removeNode()

        animal = style.head[0]
        model = loader.loadModel('phase_3' + EyelashDict[animal])
        if self.hasLOD():
            head = self.getPart('head', '1000')
        else:
            head = self.getPart('head', 'lodRoot')
        length = style.head[1]
        if length == 'l':
            openString = 'open-long'
            closedString = 'closed-long'
        else:
            openString = 'open-short'
            closedString = 'closed-short'
        self._ToonHead__eyelashOpen = model.find('**/' +
                                                 openString).copyTo(head)
        self._ToonHead__eyelashClosed = model.find('**/' +
                                                   closedString).copyTo(head)
        model.removeNode()

    def _ToonHead__fixHeadLongLong(self, style, lodName=None, copy=1):
        if lodName == None:
            searchRoot = self
        else:
            searchRoot = self.find('**/' + str(lodName))
        otherParts = searchRoot.findAllMatches('**/*short*')
        for partNum in range(0, otherParts.getNumPaths()):
            if copy:
                otherParts.getPath(partNum).removeNode()
                continue
            otherParts.getPath(partNum).stash()

    def _ToonHead__fixHeadLongShort(self, style, lodName=None, copy=1):
        animalType = style.getAnimal()
        headStyle = style.head
        if lodName == None:
            searchRoot = self
        else:
            searchRoot = self.find('**/' + str(lodName))
        if animalType != 'duck' and animalType != 'horse':
            if animalType == 'rabbit':
                if copy:
                    searchRoot.find('**/ears-long').removeNode()
                else:
                    searchRoot.find('**/ears-long').hide()
            elif copy:
                searchRoot.find('**/ears-short').removeNode()
            else:
                searchRoot.find('**/ears-short').hide()

        if animalType != 'rabbit':
            if copy:
                searchRoot.find('**/eyes-short').removeNode()
            else:
                searchRoot.find('**/eyes-short').hide()

        if animalType != 'dog':
            if copy:
                searchRoot.find('**/joint_pupilL_short').removeNode()
                searchRoot.find('**/joint_pupilR_short').removeNode()
            else:
                searchRoot.find('**/joint_pupilL_short').stash()
                searchRoot.find('**/joint_pupilR_short').stash()

        if copy:
            self.find('**/head-short').removeNode()
            self.find('**/head-front-short').removeNode()
        else:
            self.find('**/head-short').hide()
            self.find('**/head-front-short').hide()
        if animalType != 'rabbit':
            muzzleParts = searchRoot.findAllMatches('**/muzzle-long*')
            for partNum in range(0, muzzleParts.getNumPaths()):
                if copy:
                    muzzleParts.getPath(partNum).removeNode()
                    continue
                muzzleParts.getPath(partNum).hide()

        else:
            muzzleParts = searchRoot.findAllMatches('**/muzzle-short*')
            for partNum in range(0, muzzleParts.getNumPaths()):
                if copy:
                    muzzleParts.getPath(partNum).removeNode()
                    continue
                muzzleParts.getPath(partNum).hide()

    def _ToonHead__fixHeadShortLong(self, style, lodName=None, copy=1):
        animalType = style.getAnimal()
        headStyle = style.head
        if lodName == None:
            searchRoot = self
        else:
            searchRoot = self.find('**/' + str(lodName))
        if animalType != 'duck' and animalType != 'horse':
            if animalType == 'rabbit':
                if copy:
                    searchRoot.find('**/ears-short').removeNode()
                else:
                    searchRoot.find('**/ears-short').hide()
            elif copy:
                searchRoot.find('**/ears-long').removeNode()
            else:
                searchRoot.find('**/ears-long').hide()

        if animalType != 'rabbit':
            if copy:
                searchRoot.find('**/eyes-long').removeNode()
            else:
                searchRoot.find('**/eyes-long').hide()

        if animalType != 'dog':
            if copy:
                searchRoot.find('**/joint_pupilL_long').removeNode()
                searchRoot.find('**/joint_pupilR_long').removeNode()
            else:
                searchRoot.find('**/joint_pupilL_long').stash()
                searchRoot.find('**/joint_pupilR_long').stash()

        if copy:
            searchRoot.find('**/head-long').removeNode()
            searchRoot.find('**/head-front-long').removeNode()
        else:
            searchRoot.find('**/head-long').hide()
            searchRoot.find('**/head-front-long').hide()
        if animalType != 'rabbit':
            muzzleParts = searchRoot.findAllMatches('**/muzzle-short*')
            for partNum in range(0, muzzleParts.getNumPaths()):
                if copy:
                    muzzleParts.getPath(partNum).removeNode()
                    continue
                muzzleParts.getPath(partNum).hide()

        else:
            muzzleParts = searchRoot.findAllMatches('**/muzzle-long*')
            for partNum in range(0, muzzleParts.getNumPaths()):
                if copy:
                    muzzleParts.getPath(partNum).removeNode()
                    continue
                muzzleParts.getPath(partNum).hide()

    def _ToonHead__fixHeadShortShort(self, style, lodName=None, copy=1):
        if lodName == None:
            searchRoot = self
        else:
            searchRoot = self.find('**/' + str(lodName))
        otherParts = searchRoot.findAllMatches('**/*long*')
        for partNum in range(0, otherParts.getNumPaths()):
            if copy:
                otherParts.getPath(partNum).removeNode()
                continue
            otherParts.getPath(partNum).stash()

    def _ToonHead__blinkOpenEyes(self, task):
        if self.eyelids.getCurrentState().getName() == 'closed':
            self.eyelids.request('open')

        r = self.randGen.random()
        if r < 0.10000000000000001:
            t = 0.20000000000000001
        else:
            t = r * 4.0 + 1.0
        taskMgr.doMethodLater(t, self._ToonHead__blinkCloseEyes,
                              self._ToonHead__blinkName)
        return Task.done

    def _ToonHead__blinkCloseEyes(self, task):
        if self.eyelids.getCurrentState().getName() != 'open':
            taskMgr.doMethodLater(4.0, self._ToonHead__blinkCloseEyes,
                                  self._ToonHead__blinkName)
        else:
            self.eyelids.request('closed')
            taskMgr.doMethodLater(0.125, self._ToonHead__blinkOpenEyes,
                                  self._ToonHead__blinkName)
        return Task.done

    def startBlink(self):
        taskMgr.remove(self._ToonHead__blinkName)
        if self._ToonHead__eyes:
            self.openEyes()

        taskMgr.doMethodLater(self.randGen.random() * 4.0 + 1,
                              self._ToonHead__blinkCloseEyes,
                              self._ToonHead__blinkName)

    def stopBlink(self):
        taskMgr.remove(self._ToonHead__blinkName)
        if self._ToonHead__eyes:
            self.eyelids.request('open')

    def closeEyes(self):
        self.eyelids.request('closed')

    def openEyes(self):
        self.eyelids.request('open')

    def surpriseEyes(self):
        self.eyelids.request('surprised')

    def sadEyes(self):
        self._ToonHead__eyesOpen = ToonHead.EyesSadOpen
        self._ToonHead__eyesClosed = ToonHead.EyesSadClosed

    def angryEyes(self):
        self._ToonHead__eyesOpen = ToonHead.EyesAngryOpen
        self._ToonHead__eyesClosed = ToonHead.EyesAngryClosed

    def normalEyes(self):
        self._ToonHead__eyesOpen = ToonHead.EyesOpen
        self._ToonHead__eyesClosed = ToonHead.EyesClosed

    def blinkEyes(self):
        taskMgr.remove(self._ToonHead__blinkName)
        self.eyelids.request('closed')
        taskMgr.doMethodLater(0.10000000000000001,
                              self._ToonHead__blinkOpenEyes,
                              self._ToonHead__blinkName)

    def _ToonHead__stareAt(self, task):
        frac = 2 * globalClock.getDt()
        reachedTarget = self._ToonHead__lookHeadAt(
            self._ToonHead__stareAtNode, self._ToonHead__stareAtPoint, frac)
        self._ToonHead__lookPupilsAt(self._ToonHead__stareAtNode,
                                     self._ToonHead__stareAtPoint)
        if reachedTarget and self._ToonHead__stareAtNode == None:
            return Task.done
        else:
            return Task.cont

    def doLookAroundToStareAt(self, node, point):
        self.startStareAt(node, point)
        self.startLookAround()

    def startStareAtHeadPoint(self, point):
        self.startStareAt(self, point)

    def startStareAt(self, node, point):
        taskMgr.remove(self._ToonHead__stareAtName)
        if self.lookAtTrack:
            self.lookAtTrack.finish()
            self.lookAtTrack = None

        self._ToonHead__stareAtNode = node
        if point != None:
            self._ToonHead__stareAtPoint = point
        else:
            self._ToonHead__stareAtPoint = self._ToonHead__defaultStarePoint
        self._ToonHead__stareAtTime = globalClock.getFrameTime()
        taskMgr.add(self._ToonHead__stareAt, self._ToonHead__stareAtName)

    def lerpLookAt(self, point, time=1.0, blink=0):
        taskMgr.remove(self._ToonHead__stareAtName)
        if self.lookAtTrack:
            self.lookAtTrack.finish()
            self.lookAtTrack = None

        lodNames = self.getLODNames()
        if lodNames:
            lodName = lodNames[0]
        else:
            return 0
        head = self.getPart('head', lodName)
        startHpr = head.getHpr()
        startLpupil = self._ToonHead__lpupil.getPos()
        startRpupil = self._ToonHead__rpupil.getPos()
        self._ToonHead__lookHeadAt(None, point, lod=lodName)
        self._ToonHead__lookPupilsAt(None, point)
        endHpr = head.getHpr()
        endLpupil = self._ToonHead__lpupil.getPos() * 0.5
        endRpupil = self._ToonHead__rpupil.getPos() * 0.5
        head.setHpr(startHpr)
        self._ToonHead__lpupil.setPos(startLpupil)
        self._ToonHead__rpupil.setPos(startRpupil)
        if startHpr.almostEqual(endHpr, 10):
            return 0

        if blink:
            self.blinkEyes()

        lookToTgt_TimeFraction = 0.20000000000000001
        lookToTgtTime = time * lookToTgt_TimeFraction
        returnToEyeCenterTime = time - lookToTgtTime - 0.5
        origin = Point3(0, 0, 0)
        blendType = 'easeOut'
        self.lookAtTrack = Parallel(
            Sequence(
                LerpPosInterval(
                    self._ToonHead__lpupil,
                    lookToTgtTime,
                    endLpupil,
                    blendType=blendType), Wait(0.5),
                LerpPosInterval(
                    self._ToonHead__lpupil,
                    returnToEyeCenterTime,
                    origin,
                    blendType=blendType)),
            Sequence(
                LerpPosInterval(
                    self._ToonHead__rpupil,
                    lookToTgtTime,
                    endRpupil,
                    blendType=blendType), Wait(0.5),
                LerpPosInterval(
                    self._ToonHead__rpupil,
                    returnToEyeCenterTime,
                    origin,
                    blendType=blendType)),
            name=self._ToonHead__stareAtName)
        for lodName in self.getLODNames():
            head = self.getPart('head', lodName)
            self.lookAtTrack.append(
                LerpHprInterval(head, time, endHpr, blendType='easeInOut'))

        self.lookAtTrack.start()
        return 1

    def stopStareAt(self):
        self.lerpLookAt(Vec3.forward())

    def stopStareAtNow(self):
        taskMgr.remove(self._ToonHead__stareAtName)
        if self.lookAtTrack:
            self.lookAtTrack.finish()
            self.lookAtTrack = None

        if self._ToonHead__lpupil and self._ToonHead__rpupil:
            self._ToonHead__setPupilDirection(0, 0)

        for lodName in self.getLODNames():
            head = self.getPart('head', lodName)
            head.setHpr(0, 0, 0)

    def _ToonHead__lookAround(self, task):
        self.findSomethingToLookAt()
        t = self.randGen.random() * 4.0 + 3.0
        taskMgr.doMethodLater(t, self._ToonHead__lookAround,
                              self._ToonHead__lookName)
        return Task.done

    def startLookAround(self):
        taskMgr.remove(self._ToonHead__lookName)
        t = self.randGen.random() * 5.0 + 2.0
        taskMgr.doMethodLater(t, self._ToonHead__lookAround,
                              self._ToonHead__lookName)

    def stopLookAround(self):
        taskMgr.remove(self._ToonHead__lookName)
        self.stopStareAt()

    def stopLookAroundNow(self):
        taskMgr.remove(self._ToonHead__lookName)
        self.stopStareAtNow()

    def enterEyelidsOff(self):
        pass

    def exitEyelidsOff(self):
        pass

    def enterEyelidsOpen(self):
        if not self._ToonHead__eyes.isEmpty():
            self._ToonHead__eyes.setTexture(self._ToonHead__eyesOpen, 1)
            if self._ToonHead__eyelashOpen:
                self._ToonHead__eyelashOpen.show()

            if self._ToonHead__eyelashClosed:
                self._ToonHead__eyelashClosed.hide()

            if self._ToonHead__lod500Eyes:
                self._ToonHead__lod500Eyes.setTexture(self._ToonHead__eyesOpen,
                                                      1)

            if self._ToonHead__lod250Eyes:
                self._ToonHead__lod250Eyes.setTexture(self._ToonHead__eyesOpen,
                                                      1)

            if self._ToonHead__lpupil:
                self._ToonHead__lpupil.show()
                self._ToonHead__rpupil.show()

            if self._ToonHead__lod500lPupil:
                self._ToonHead__lod500lPupil.show()
                self._ToonHead__lod500rPupil.show()

            if self._ToonHead__lod250lPupil:
                self._ToonHead__lod250lPupil.show()
                self._ToonHead__lod250rPupil.show()

    def exitEyelidsOpen(self):
        pass

    def enterEyelidsClosed(self):
        if not self._ToonHead__eyes.isEmpty() and self._ToonHead__eyesClosed:
            self._ToonHead__eyes.setTexture(self._ToonHead__eyesClosed, 1)
            if self._ToonHead__eyelashOpen:
                self._ToonHead__eyelashOpen.hide()

            if self._ToonHead__eyelashClosed:
                self._ToonHead__eyelashClosed.show()

            if self._ToonHead__lod500Eyes:
                self._ToonHead__lod500Eyes.setTexture(
                    self._ToonHead__eyesClosed, 1)

            if self._ToonHead__lod250Eyes:
                self._ToonHead__lod250Eyes.setTexture(
                    self._ToonHead__eyesClosed, 1)

            if self._ToonHead__lpupil:
                self._ToonHead__lpupil.hide()
                self._ToonHead__rpupil.hide()

            if self._ToonHead__lod500lPupil:
                self._ToonHead__lod500lPupil.hide()
                self._ToonHead__lod500rPupil.hide()

            if self._ToonHead__lod250lPupil:
                self._ToonHead__lod250lPupil.hide()
                self._ToonHead__lod250rPupil.hide()

    def exitEyelidsClosed(self):
        pass

    def enterEyelidsSurprised(self):
        if not self._ToonHead__eyes.isEmpty() and ToonHead.EyesSurprised:
            self._ToonHead__eyes.setTexture(ToonHead.EyesSurprised, 1)
            if self._ToonHead__eyelashOpen:
                self._ToonHead__eyelashOpen.hide()

            if self._ToonHead__eyelashClosed:
                self._ToonHead__eyelashClosed.hide()

            if self._ToonHead__lod500Eyes:
                self._ToonHead__lod500Eyes.setTexture(ToonHead.EyesSurprised,
                                                      1)

            if self._ToonHead__lod250Eyes:
                self._ToonHead__lod250Eyes.setTexture(ToonHead.EyesSurprised,
                                                      1)

            if self._ToonHead__muzzle:
                self._ToonHead__muzzle.setTexture(ToonHead.MuzzleSurprised, 1)

            if self._ToonHead__lpupil:
                self._ToonHead__lpupil.show()
                self._ToonHead__rpupil.show()

            if self._ToonHead__lod500lPupil:
                self._ToonHead__lod500lPupil.show()
                self._ToonHead__lod500rPupil.show()

            if self._ToonHead__lod250lPupil:
                self._ToonHead__lod250lPupil.show()
                self._ToonHead__lod250rPupil.show()

    def exitEyelidsSurprised(self):
        if self._ToonHead__muzzle:
            self._ToonHead__muzzle.setTexture(ToonHead.Muzzle, 1)

    def setupMuzzles(self, style):
        self._ToonHead__muzzles = []
        self._ToonHead__surpriseMuzzles = []
        self._ToonHead__angryMuzzles = []
        self._ToonHead__sadMuzzles = []
        self._ToonHead__smileMuzzles = []
        self._ToonHead__laughMuzzles = []

        def hideAddNonEmptyItemToList(item, list):
            if not item.isEmpty():
                item.hide()
                list.append(item)

        def hideNonEmptyItem(item):
            if not item.isEmpty():
                item.hide()

        if self.hasLOD():
            for lodName in self.getLODNames():
                animal = style.getAnimal()
                if animal != 'dog':
                    muzzle = self.find('**/' + lodName + '/**/muzzle*neutral')
                else:
                    muzzle = self.find('**/' + lodName + '/**/muzzle*')
                    if lodName == '1000' or lodName == '500':
                        filePrefix = DogMuzzleDict[style.head]
                        muzzles = loader.loadModel('phase_3' + filePrefix +
                                                   lodName)
                        if base.config.GetBool('want-new-anims', 1):
                            if not self.find(
                                    '**/' + lodName +
                                    '/**/__Actor_head/def_head').isEmpty():
                                muzzles.reparentTo(
                                    self.find('**/' + lodName +
                                              '/**/__Actor_head/def_head'))
                            else:
                                muzzles.reparentTo(
                                    self.find('**/' + lodName +
                                              '/**/joint_toHead'))
                        elif self.find('**/' + lodName + '/**/joint_toHead'):
                            muzzles.reparentTo(
                                self.find('**/' + lodName +
                                          '/**/joint_toHead'))

                surpriseMuzzle = self.find('**/' + lodName +
                                           '/**/muzzle*surprise')
                angryMuzzle = self.find('**/' + lodName + '/**/muzzle*angry')
                sadMuzzle = self.find('**/' + lodName + '/**/muzzle*sad')
                smileMuzzle = self.find('**/' + lodName + '/**/muzzle*smile')
                laughMuzzle = self.find('**/' + lodName + '/**/muzzle*laugh')
                self._ToonHead__muzzles.append(muzzle)
                hideAddNonEmptyItemToList(surpriseMuzzle,
                                          self._ToonHead__surpriseMuzzles)
                hideAddNonEmptyItemToList(angryMuzzle,
                                          self._ToonHead__angryMuzzles)
                hideAddNonEmptyItemToList(sadMuzzle,
                                          self._ToonHead__sadMuzzles)
                hideAddNonEmptyItemToList(smileMuzzle,
                                          self._ToonHead__smileMuzzles)
                hideAddNonEmptyItemToList(laughMuzzle,
                                          self._ToonHead__laughMuzzles)

        elif style.getAnimal() != 'dog':
            muzzle = self.find('**/muzzle*neutral')
        else:
            muzzle = self.find('**/muzzle*')
            filePrefix = DogMuzzleDict[style.head]
            muzzles = loader.loadModel('phase_3' + filePrefix + '1000')
            if base.config.GetBool('want-new-anims', 1):
                if not self.find('**/def_head').isEmpty():
                    muzzles.reparentTo(self.find('**/def_head'))
                else:
                    muzzles.reparentTo(self.find('**/joint_toHead'))
            else:
                muzzles.reparentTo(self.find('**/joint_toHead'))
        surpriseMuzzle = self.find('**/muzzle*surprise')
        angryMuzzle = self.find('**/muzzle*angry')
        sadMuzzle = self.find('**/muzzle*sad')
        smileMuzzle = self.find('**/muzzle*smile')
        laughMuzzle = self.find('**/muzzle*laugh')
        self._ToonHead__muzzles.append(muzzle)
        hideAddNonEmptyItemToList(surpriseMuzzle,
                                  self._ToonHead__surpriseMuzzles)
        hideAddNonEmptyItemToList(angryMuzzle, self._ToonHead__angryMuzzles)
        hideAddNonEmptyItemToList(sadMuzzle, self._ToonHead__sadMuzzles)
        hideAddNonEmptyItemToList(smileMuzzle, self._ToonHead__smileMuzzles)
        hideAddNonEmptyItemToList(laughMuzzle, self._ToonHead__laughMuzzles)

    def getMuzzles(self):
        return self._ToonHead__muzzles

    def getSurpriseMuzzles(self):
        return self._ToonHead__surpriseMuzzles

    def getAngryMuzzles(self):
        return self._ToonHead__angryMuzzles

    def getSadMuzzles(self):
        return self._ToonHead__sadMuzzles

    def getSmileMuzzles(self):
        return self._ToonHead__smileMuzzles

    def getLaughMuzzles(self):
        return self._ToonHead__laughMuzzles

    def showNormalMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return None

        for muzzleNum in range(len(self._ToonHead__muzzles)):
            self._ToonHead__muzzles[muzzleNum].show()

    def hideNormalMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return None

        for muzzleNum in range(len(self._ToonHead__muzzles)):
            self._ToonHead__muzzles[muzzleNum].hide()

    def showAngryMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return None

        for muzzleNum in range(len(self._ToonHead__angryMuzzles)):
            self._ToonHead__angryMuzzles[muzzleNum].show()
            self._ToonHead__muzzles[muzzleNum].hide()

    def hideAngryMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return None

        for muzzleNum in range(len(self._ToonHead__angryMuzzles)):
            self._ToonHead__angryMuzzles[muzzleNum].hide()
            self._ToonHead__muzzles[muzzleNum].show()

    def showSadMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return None

        for muzzleNum in range(len(self._ToonHead__sadMuzzles)):
            self._ToonHead__sadMuzzles[muzzleNum].show()
            self._ToonHead__muzzles[muzzleNum].hide()

    def hideSadMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return None

        for muzzleNum in range(len(self._ToonHead__sadMuzzles)):
            self._ToonHead__sadMuzzles[muzzleNum].hide()
            self._ToonHead__muzzles[muzzleNum].show()

    def showSmileMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return None

        for muzzleNum in range(len(self._ToonHead__smileMuzzles)):
            self._ToonHead__smileMuzzles[muzzleNum].show()
            self._ToonHead__muzzles[muzzleNum].hide()

    def hideSmileMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return None

        for muzzleNum in range(len(self._ToonHead__smileMuzzles)):
            self._ToonHead__smileMuzzles[muzzleNum].hide()
            self._ToonHead__muzzles[muzzleNum].show()

    def showLaughMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return None

        for muzzleNum in range(len(self._ToonHead__laughMuzzles)):
            self._ToonHead__laughMuzzles[muzzleNum].show()
            self._ToonHead__muzzles[muzzleNum].hide()

    def hideLaughMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return None

        for muzzleNum in range(len(self._ToonHead__laughMuzzles)):
            self._ToonHead__laughMuzzles[muzzleNum].hide()
            self._ToonHead__muzzles[muzzleNum].show()

    def showSurpriseMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return None

        for muzzleNum in range(len(self._ToonHead__surpriseMuzzles)):
            self._ToonHead__surpriseMuzzles[muzzleNum].show()
            self._ToonHead__muzzles[muzzleNum].hide()

    def hideSurpriseMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return None

        for muzzleNum in range(len(self._ToonHead__surpriseMuzzles)):
            self._ToonHead__surpriseMuzzles[muzzleNum].hide()
            self._ToonHead__muzzles[muzzleNum].show()

    def isIgnoreCheesyEffect(self):
        if hasattr(self, 'savedCheesyEffect'):
            if self.savedCheesyEffect == 10 and self.savedCheesyEffect == 11 and self.savedCheesyEffect == 12 and self.savedCheesyEffect == 13 or self.savedCheesyEffect == 14:
                return True

        return False
