from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
import math
from toontown.toonbase import ToontownGlobals
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
from direct.fsm import State
from toontown.toon import Toon
from direct.showbase import RandomNumGen
from direct.task.Task import Task
from toontown.toonbase import TTLocalizer
import random
import cPickle
import time
from direct.showbase import PythonUtil
from toontown.hood import Place
import Estate
import HouseGlobals
from toontown.estate import GardenGlobals
from toontown.estate import DistributedFlower
from toontown.estate import DistributedGagTree
from toontown.estate import DistributedStatuary
import GardenDropGame
import GardenProgressMeter
from toontown.estate import FlowerSellGUI
from toontown.toontowngui import TTDialog


class DistributedEstate(DistributedObject.DistributedObject):
    notify = directNotify.newCategory('DistributedEstate')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.closestHouse = 0
        self.ground = None
        self.dayTrack = None
        self.sunTrack = None
        self.airplane = None
        self.flowerSellBox = None
        self.estateDoneEvent = 'estateDone'
        self.load()
        self.initCamera()
        self.plotTable = []
        self.idList = []
        base.estate = self
        self.flowerGuiDoneEvent = 'flowerGuiDone'

    def disable(self):
        self.notify.debug('disable')
        self._DistributedEstate__stopBirds()
        self._DistributedEstate__stopCrickets()
        DistributedObject.DistributedObject.disable(self)
        self.ignore('enterFlowerSellBox')

    def delete(self):
        self.notify.debug('delete')
        self.unload()
        DistributedObject.DistributedObject.delete(self)

    def load(self):
        self.lt = base.localAvatar
        newsManager = base.cr.newsManager
        if newsManager:
            holidayIds = base.cr.newsManager.getDecorationHolidayId()
            if ToontownGlobals.HALLOWEEN_COSTUMES in holidayIds or ToontownGlobals.SPOOKY_COSTUMES in holidayIds:
                self.loadWitch()
            else:
                self.loadAirplane()

        self.loadFlowerSellBox()
        self.oldClear = base.win.getClearColor()
        base.win.setClearColor(
            Vec4(
                0.089999999999999997,
                0.55000000000000004,
                0.20999999999999999,
                1.0))

    def unload(self):
        self.ignoreAll()
        base.win.setClearColor(self.oldClear)
        self._DistributedEstate__killAirplaneTask()
        self._DistributedEstate__killDaytimeTask()
        self._DistributedEstate__stopBirds()
        self._DistributedEstate__stopCrickets()
        if self.dayTrack:
            self.dayTrack.pause()
            self.dayTrack = None

        self._DistributedEstate__killSunTask()
        if self.sunTrack:
            self.sunTrack.pause()
            self.sunTrack = None

        if self.ground:
            self.ground.removeNode()
            del self.ground

        if self.airplane:
            self.airplane.removeNode()
            del self.airplane
            self.airplane = None

        if self.flowerSellBox:
            self.flowerSellBox.removeNode()
            del self.flowerSellBox
            self.flowerSellBox = None

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.accept('gardenGame', self.startGame)

    def startGame(self):
        self.game = GardenDropGame.GardenDropGame()

    def loadAirplane(self):
        self.airplane = loader.loadModel('phase_4/models/props/airplane.bam')
        self.airplane.setScale(4)
        self.airplane.setPos(0, 0, 1)
        self.banner = self.airplane.find('**/*banner')
        bannerText = TextNode('bannerText')
        bannerText.setTextColor(1, 0, 0, 1)
        bannerText.setAlign(bannerText.ACenter)
        bannerText.setFont(ToontownGlobals.getSignFont())
        bannerText.setText('Cog invasion!!!')
        self.bn = self.banner.attachNewNode(bannerText.generate())
        self.bn.setHpr(180, 0, 0)
        self.bn.setPos(-1.8, 0.10000000000000001, 0)
        self.bn.setScale(0.34999999999999998)
        self.banner.hide()

    def loadWitch(self):
        if not self.airplane:
            self.airplane = loader.loadModel(
                'phase_4/models/props/tt_m_prp_ext_flyingWitch.bam')

        def __replaceAirplane__():
            self.airplane.reparentTo(hidden)
            del self.airplane
            self.airplane = loader.loadModel(
                'phase_4/models/props/tt_m_prp_ext_flyingWitch.bam')
            self.airplane.setScale(2)
            self.airplane.setPos(0, 0, 1)
            bannerText = TextNode('bannerText')
            bannerText.setTextColor(1, 0, 0, 1)
            bannerText.setAlign(bannerText.ACenter)
            bannerText.setFont(ToontownGlobals.getSignFont())
            bannerText.setText('Happy halloween!!!')
            self.bn = self.airplane.attachNewNode(bannerText.generate())
            self.bn.setHpr(0, 0, 0)
            self.bn.setPos(20.0, -0.10000000000000001, 0)
            self.bn.setScale(2.3500000000000001)

        replacement = Sequence(
            LerpColorScaleInterval(
                self.airplane, 0.10000000000000001, Vec4(
                    1, 1, 1, 0)), Func(__replaceAirplane__), LerpColorScaleInterval(
                self.airplane, 0.10000000000000001, Vec4(
                    1, 1, 1, 1)))
        replacement.start()

    def unloadWitch(self):

        def __replaceWitch__():
            self.airplane.reparentTo(hidden)
            del self.airplane
            del self.bn
            self.airplane = loader.loadModel(
                'phase_4/models/props/airplane.bam')
            self.airplane.setScale(4)
            self.airplane.setPos(0, 0, 1)
            self.banner = self.airplane.find('**/*banner')
            bannerText = TextNode('bannerText')
            bannerText.setTextColor(1, 0, 0, 1)
            bannerText.setAlign(bannerText.ACenter)
            bannerText.setFont(ToontownGlobals.getSignFont())
            bannerText.setText('Happy halloween!!!')
            self.bn = self.banner.attachNewNode(bannerText.generate())
            self.bn.setHpr(180, 0, 0)
            self.bn.setPos(-1.8, 0.10000000000000001, 0)
            self.bn.setScale(0.34999999999999998)
            self.banner.hide()

        replacement = Sequence(
            LerpColorScaleInterval(
                self.airplane, 0.10000000000000001, Vec4(
                    1, 1, 1, 0)), Func(__replaceWitch__), LerpColorScaleInterval(
                self.airplane, 0.10000000000000001, Vec4(
                    1, 1, 1, 1)))
        replacement.start()

    def initCamera(self):
        initCamPos = VBase3(0, -10, 5)
        initCamHpr = VBase3(0, -10, 0)

    def setEstateType(self, index):
        self.estateType = index

    def setHouseInfo(self, houseInfo):
        self.notify.debug('setHouseInfo')
        (houseType, housePos) = cPickle.loads(houseInfo)
        self.loadEstate(houseType, housePos)

    def loadEstate(self, indexList, posList):
        self.notify.debug('loadEstate')
        self.houseType = indexList
        self.housePos = posList
        self.numHouses = len(self.houseType)
        self.house = [
            None] * self.numHouses

    def _DistributedEstate__startAirplaneTask(self):
        self.theta = 0
        self.phi = 0
        taskMgr.remove(self.taskName('estate-airplane'))
        taskMgr.add(self.airplaneFlyTask, self.taskName('estate-airplane'))

    def _DistributedEstate__pauseAirplaneTask(self):
        pause = 45
        self.phi = 0
        self.airplane.hide()
        self.theta = (self.theta + 10) % 360
        taskMgr.remove(self.taskName('estate-airplane'))
        taskMgr.doMethodLater(
            pause,
            self.airplaneFlyTask,
            self.taskName('estate-airplane'))

    def _DistributedEstate__killAirplaneTask(self):
        taskMgr.remove(self.taskName('estate-airplane'))

    def airplaneFlyTask(self, task):
        rad = 300.0
        amp = 80.0
        self.theta += 0.25
        self.phi += 0.0050000000000000001
        sinPhi = math.sin(self.phi)
        if sinPhi <= 0:
            self._DistributedEstate__pauseAirplaneTask()

        angle = math.pi * self.theta / 180.0
        x = rad * math.cos(angle)
        y = rad * math.sin(angle)
        z = amp * sinPhi
        self.airplane.reparentTo(render)
        self.airplane.setH(90 + self.theta + 180)
        self.airplane.setPos(x, y, z)
        return Task.cont

    def sendHouseColor(self, index, r, g, b, a):
        self.house[index].setColor(r, g, b, a)

    def setTreasureIds(self, doIds):
        self.flyingTreasureId = []
        for id in doIds:
            self.flyingTreasureId.append(id)

    def setDawnTime(self, ts):
        self.notify.debug('setDawnTime')
        self.dawnTime = ts
        self.sendUpdate('requestServerTime', [])

    def setServerTime(self, ts):
        self.notify.debug('setServerTime')
        self.serverTime = ts
        self.clientTime = time.time() % HouseGlobals.DAY_NIGHT_PERIOD
        self.deltaTime = self.clientTime - self.serverTime
        if base.dayNightEnabled:
            self._DistributedEstate__initDaytimeTask()
            self._DistributedEstate__initSunTask()

        self._DistributedEstate__startAirplaneTask()

    def getDeltaTime(self):
        curTime = time.time() % HouseGlobals.DAY_NIGHT_PERIOD
        dawnTime = self.dawnTime
        dT = (curTime - dawnTime - self.deltaTime) % HouseGlobals.DAY_NIGHT_PERIOD
        print 'getDeltaTime = %s. curTime=%s. dawnTime=%s. serverTime=%s.  deltaTime=%s' % (dT, curTime, dawnTime, self.serverTime, self.deltaTime)
        return dT

    def _DistributedEstate__initDaytimeTask(self):
        self._DistributedEstate__killDaytimeTask()
        task = Task(self._DistributedEstate__dayTimeTask)
        dT = self.getDeltaTime()
        task.ts = dT
        taskMgr.add(task, self.taskName('daytime'))

    def _DistributedEstate__killDaytimeTask(self):
        taskMgr.remove(self.taskName('daytime'))

    def _DistributedEstate__dayTimeTask(self, task):
        taskName = self.taskName('daytime')
        track = Sequence(
            Parallel(
                LerpColorScaleInterval(
                    base.cr.playGame.hood.loader.geom, HouseGlobals.HALF_DAY_PERIOD, Vec4(
                        1, 0.59999999999999998, 0.59999999999999998, 1)), LerpColorScaleInterval(
                    base.cr.playGame.hood.sky, HouseGlobals.HALF_DAY_PERIOD, Vec4(
                        1, 0.80000000000000004, 0.80000000000000004, 1))), Parallel(
                            LerpColorScaleInterval(
                                base.cr.playGame.hood.loader.geom, HouseGlobals.HALF_NIGHT_PERIOD, Vec4(
                                    0.20000000000000001, 0.20000000000000001, 0.5, 1)), LerpColorScaleInterval(
                                        base.cr.playGame.hood.sky, HouseGlobals.HALF_NIGHT_PERIOD, Vec4(
                                            0.40000000000000002, 0.40000000000000002, 0.59999999999999998, 1))), Parallel(
                                                LerpColorScaleInterval(
                                                    base.cr.playGame.hood.loader.geom, HouseGlobals.HALF_NIGHT_PERIOD, Vec4(
                                                        0.59999999999999998, 0.59999999999999998, 0.80000000000000004, 1)), LerpColorScaleInterval(
                                                            base.cr.playGame.hood.sky, HouseGlobals.HALF_NIGHT_PERIOD, Vec4(
                                                                0.69999999999999996, 0.69999999999999996, 0.80000000000000004, 1))), Parallel(
                                                                    LerpColorScaleInterval(
                                                                        base.cr.playGame.hood.loader.geom, HouseGlobals.HALF_DAY_PERIOD, Vec4(
                                                                            1, 1, 1, 1)), LerpColorScaleInterval(
                                                                                base.cr.playGame.hood.sky, HouseGlobals.HALF_DAY_PERIOD, Vec4(
                                                                                    1, 1, 1, 1))), Func(
                                                                                        base.cr.playGame.hood.loader.geom.clearColorScale), Func(
                                                                                            base.cr.playGame.hood.sky.clearColorScale))
        if self.dayTrack:
            self.dayTrack.finish()

        self.dayTrack = track
        ts = 0
        if hasattr(task, 'ts'):
            ts = task.ts

        print 'ts=%s' % ts
        self.dayTrack.start(ts)
        taskMgr.doMethodLater(
            HouseGlobals.DAY_NIGHT_PERIOD - ts,
            self._DistributedEstate__dayTimeTask,
            self.taskName('daytime'))
        return Task.done

    def _DistributedEstate__initSunTask(self):
        self._DistributedEstate__killSunTask()
        task = Task(self._DistributedEstate__sunTask)
        dT = self.getDeltaTime()
        task.ts = dT
        taskMgr.add(task, self.taskName('sunTask'))

    def _DistributedEstate__killSunTask(self):
        taskMgr.remove(self.taskName('sunTask'))

    def _DistributedEstate__sunTask(self, task):
        sunMoonNode = base.cr.playGame.hood.loader.sunMoonNode
        sun = base.cr.playGame.hood.loader.sun
        h = 30
        halfPeriod = HouseGlobals.DAY_NIGHT_PERIOD / 2.0
        track = Sequence(
            Parallel(
                LerpHprInterval(
                    sunMoonNode, HouseGlobals.HALF_DAY_PERIOD, Vec3(
                        0, 0, 0)), LerpColorScaleInterval(
                    sun, HouseGlobals.HALF_DAY_PERIOD, Vec4(
                        1, 1, 0.5, 1))), Func(
                            sun.clearColorScale), Func(
                                self._DistributedEstate__stopBirds), LerpHprInterval(
                                    sunMoonNode, 0.20000000000000001, Vec3(
                                        0, -h - 3, 0)), LerpHprInterval(
                                            sunMoonNode, 0.10000000000000001, Vec3(
                                                0, -h + 2, 0)), LerpHprInterval(
                                                    sunMoonNode, 0.10000000000000001, Vec3(
                                                        0, -h - 1.5, 0)), LerpHprInterval(
                                                            sunMoonNode, 0.10000000000000001, Vec3(
                                                                0, -h, 0)), Func(
                                                                    self.notify.debug, 'night'), Wait(
                                                                        HouseGlobals.HALF_NIGHT_PERIOD - 0.5), LerpHprInterval(
                                                                            sunMoonNode, HouseGlobals.HALF_NIGHT_PERIOD, Vec3(
                                                                                0, 0, 0)), Func(
                                                                                    self._DistributedEstate__startBirds), LerpHprInterval(
                                                                                        sunMoonNode, 0.20000000000000001, Vec3(
                                                                                            0, h + 3, 0)), LerpHprInterval(
                                                                                                sunMoonNode, 0.10000000000000001, Vec3(
                                                                                                    0, h - 2, 0)), LerpHprInterval(
                                                                                                        sunMoonNode, 0.10000000000000001, Vec3(
                                                                                                            0, h + 1.5, 0)), LerpHprInterval(
                                                                                                                sunMoonNode, 0.10000000000000001, Vec3(
                                                                                                                    0, h, 0)), Func(
                                                                                                                        self.notify.debug, 'day'), Func(
                                                                                                                            sunMoonNode.setHpr, 0, h, 0), Wait(
                                                                                                                                HouseGlobals.HALF_DAY_PERIOD - 0.5))
        if self.sunTrack:
            self.sunTrack.finish()

        self.sunTrack = track
        ts = 0
        if hasattr(task, 'ts'):
            ts = task.ts
            if ts > HouseGlobals.HALF_DAY_PERIOD and ts < HouseGlobals.DAY_NIGHT_PERIOD - \
                    HouseGlobals.HALF_DAY_PERIOD:
                self._DistributedEstate__stopBirds()
                self._DistributedEstate__startCrickets()
            else:
                self._DistributedEstate__stopCrickets()
                self._DistributedEstate__startBirds()

        print 'ts(sun)=%s' % ts
        self.sunTrack.start(ts)
        taskMgr.doMethodLater(
            HouseGlobals.DAY_NIGHT_PERIOD - ts,
            self._DistributedEstate__sunTask,
            self.taskName('sunTask'))
        return Task.done

    def _DistributedEstate__stopBirds(self):
        taskMgr.remove('estate-birds')

    def _DistributedEstate__startBirds(self):
        self._DistributedEstate__stopBirds()
        taskMgr.doMethodLater(
            1, self._DistributedEstate__birds, 'estate-birds')

    def _DistributedEstate__birds(self, task):
        base.playSfx(random.choice(base.cr.playGame.hood.loader.birdSound))
        t = random.random() * 20.0 + 1
        taskMgr.doMethodLater(
            t, self._DistributedEstate__birds, 'estate-birds')
        return Task.done

    def _DistributedEstate__stopCrickets(self):
        taskMgr.remove('estate-crickets')

    def _DistributedEstate__startCrickets(self):
        self._DistributedEstate__stopCrickets()
        taskMgr.doMethodLater(
            1,
            self._DistributedEstate__crickets,
            'estate-crickets')

    def _DistributedEstate__crickets(self, task):
        sfx = random.choice(base.cr.playGame.hood.loader.cricketSound)
        track = Sequence(Func(base.playSfx, sfx), Wait(1))
        track.play()
        t = random.random() * 20.0 + 1
        taskMgr.doMethodLater(
            t,
            self._DistributedEstate__crickets,
            'estate-crickets')
        return Task.done

    def getLastEpochTimeStamp(self):
        return self.lastEpochTimeStamp

    def setLastEpochTimeStamp(self, ts):
        self.lastEpochTimeStamp = ts

    def getIdList(self):
        return self.idList

    def setIdList(self, idList):
        self.idList = idList

    def loadFlowerSellBox(self):
        self.flowerSellBox = loader.loadModel(
            'phase_5.5/models/estate/wheelbarrel.bam')
        self.flowerSellBox.setPos(-142.58600000000001,
                                  4.3529999999999998, 0.025000000000000001)
        self.flowerSellBox.reparentTo(render)
        colNode = self.flowerSellBox.find('**/collision')
        colNode.setName('FlowerSellBox')
        self.accept(
            'enterFlowerSellBox',
            self._DistributedEstate__touchedFlowerSellBox)

    def _DistributedEstate__touchedFlowerSellBox(self, entry):
        if base.localAvatar.doId in self.idList:
            if len(base.localAvatar.flowerBasket.flowerList):
                self.popupFlowerGUI()

    def _DistributedEstate__handleSaleDone(self, sell=0):
        self.ignore(self.flowerGuiDoneEvent)
        self.sendUpdate('completeFlowerSale', [
            sell])
        self.ignore('stoppedAsleep')
        self.flowerGui.destroy()
        self.flowerGui = None

    def popupFlowerGUI(self):
        self.acceptOnce(
            self.flowerGuiDoneEvent,
            self._DistributedEstate__handleSaleDone)
        self.flowerGui = FlowerSellGUI.FlowerSellGUI(self.flowerGuiDoneEvent)
        self.accept('stoppedAsleep', self._DistributedEstate__handleSaleDone)

    def closedAwardDialog(self, value):
        self.awardDialog.destroy()
        base.cr.playGame.getPlace().detectedGardenPlotDone()

    def awardedTrophy(self, avId):
        if base.localAvatar.doId == avId:
            base.cr.playGame.getPlace().detectedGardenPlotUse()
            msg = TTLocalizer.GardenTrophyAwarded % (len(
                base.localAvatar.getFlowerCollection()),
                GardenGlobals.getNumberOfFlowerVarieties())
            self.awardDialog = TTDialog.TTDialog(
                style=TTDialog.Acknowledge, text=msg, command=self.closedAwardDialog)

    def setClouds(self, clouds):
        self.clouds = clouds
        base.cr.playGame.hood.loader.setCloudSwitch(clouds)

    def getClouds(self):
        if hasattr(self, 'clouds'):
            return self.clouds
        else:
            return 0

    def cannonsOver(self, arg=None):
        base.localAvatar.setSystemMessage(0, TTLocalizer.EstateCannonGameEnd)

    def gameTableOver(self, arg=None):
        base.localAvatar.setSystemMessage(0, TTLocalizer.GameTableRentalEnd)
