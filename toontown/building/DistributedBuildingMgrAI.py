import os
from direct.task.Task import Task
import cPickle
from otp.ai.AIBaseGlobal import *
import DistributedBuildingAI
import HQBuildingAI
import GagshopBuildingAI
import PetshopBuildingAI
from toontown.building.KartShopBuildingAI import KartShopBuildingAI
from toontown.building import DistributedAnimBuildingAI
from direct.directnotify import DirectNotifyGlobal
from toontown.hood import ZoneUtil
import time
import random


class DistributedBuildingMgrAI:
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedBuildingMgrAI')
    serverDatafolder = simbase.config.GetString('server-data-folder', '')

    def __init__(self, air, branchID, dnaStore, trophyMgr):
        self.branchID = branchID
        self.canonicalBranchID = ZoneUtil.getCanonicalZoneId(branchID)
        self.air = air
        self._DistributedBuildingMgrAI__buildings = {}
        self.dnaStore = dnaStore
        self.trophyMgr = trophyMgr
        self.shard = str(air.districtId)
        self.backupExtension = '.bu'
        self.findAllLandmarkBuildings()
        self.doLaterTask = None

    def cleanup(self):
        taskMgr.remove(str(self.branchID) + '_delayed_save-timer')
        for building in self._DistributedBuildingMgrAI__buildings.values():
            building.cleanup()

        self._DistributedBuildingMgrAI__buildings = {}

    def isValidBlockNumber(self, blockNumber):
        return blockNumber in self._DistributedBuildingMgrAI__buildings

    def delayedSaveTask(self, task):
        self.save()
        self.doLaterTask = None
        return Task.done

    def isSuitBlock(self, blockNumber):
        return self._DistributedBuildingMgrAI__buildings[
            blockNumber].isSuitBlock()

    def getSuitBlocks(self):
        blocks = []
        for i in self._DistributedBuildingMgrAI__buildings.values():
            if i.isSuitBlock():
                blocks.append(i.getBlock()[0])
                continue

        return blocks

    def getEstablishedSuitBlocks(self):
        blocks = []
        for i in self._DistributedBuildingMgrAI__buildings.values():
            if i.isEstablishedSuitBlock():
                blocks.append(i.getBlock()[0])
                continue

        return blocks

    def getToonBlocks(self):
        blocks = []
        for i in self._DistributedBuildingMgrAI__buildings.values():
            if isinstance(i, HQBuildingAI.HQBuildingAI):
                continue

            if not i.isSuitBlock():
                blocks.append(i.getBlock()[0])
                continue

        return blocks

    def getBuildings(self):
        return self._DistributedBuildingMgrAI__buildings.values()

    def getFrontDoorPoint(self, blockNumber):
        return self._DistributedBuildingMgrAI__buildings[
            blockNumber].getFrontDoorPoint()

    def getBuildingTrack(self, blockNumber):
        return self._DistributedBuildingMgrAI__buildings[blockNumber].track

    def getBuilding(self, blockNumber):
        return self._DistributedBuildingMgrAI__buildings[blockNumber]

    def setFrontDoorPoint(self, blockNumber, point):
        return self._DistributedBuildingMgrAI__buildings[
            blockNumber].setFrontDoorPoint(point)

    def getDNABlockLists(self):
        blocks = []
        hqBlocks = []
        gagshopBlocks = []
        petshopBlocks = []
        kartshopBlocks = []
        animBldgBlocks = []
        for i in range(self.dnaStore.getNumBlockNumbers()):
            blockNumber = self.dnaStore.getBlockNumberAt(i)
            buildingType = self.dnaStore.getBlockBuildingType(blockNumber)
            if buildingType == 'hq':
                hqBlocks.append(blockNumber)
                continue
            if buildingType == 'gagshop':
                gagshopBlocks.append(blockNumber)
                continue
            if buildingType == 'petshop':
                petshopBlocks.append(blockNumber)
                continue
            if buildingType == 'kartshop':
                kartshopBlocks.append(blockNumber)
                continue
            if buildingType == 'animbldg':
                animBldgBlocks.append(blockNumber)
                continue
            blocks.append(blockNumber)

        return (blocks, hqBlocks, gagshopBlocks, petshopBlocks, kartshopBlocks,
                animBldgBlocks)

    def findAllLandmarkBuildings(self):
        buildings = self.load()
        (blocks, hqBlocks, gagshopBlocks, petshopBlocks, kartshopBlocks,
         animBldgBlocks) = self.getDNABlockLists()
        for block in blocks:
            self.newBuilding(block, buildings.get(block, None))

        for block in animBldgBlocks:
            self.newAnimBuilding(block, buildings.get(block, None))

        for block in hqBlocks:
            self.newHQBuilding(block)

        for block in gagshopBlocks:
            self.newGagshopBuilding(block)

        if simbase.wantPets:
            for block in petshopBlocks:
                self.newPetshopBuilding(block)

        if simbase.wantKarts:
            for block in kartshopBlocks:
                self.newKartShopBuilding(block)

    def newBuilding(self, blockNumber, blockData=None):
        building = DistributedBuildingAI.DistributedBuildingAI(
            self.air, blockNumber, self.branchID, self.trophyMgr)
        building.generateWithRequired(self.branchID)
        if blockData:
            building.track = blockData.get('track', 'c')
            building.difficulty = int(blockData.get('difficulty', 1))
            building.numFloors = int(blockData.get('numFloors', 1))
            building.numFloors = max(1, min(5, building.numFloors))
            if not ZoneUtil.isWelcomeValley(building.zoneId):
                building.updateSavedBy(blockData.get('savedBy'))
            else:
                self.notify.warning(
                    'we had a cog building in welcome valley %d' %
                    building.zoneId)
            building.becameSuitTime = blockData.get('becameSuitTime',
                                                    time.time())
            if blockData['state'] == 'suit':
                building.setState('suit')
            elif blockData['state'] == 'cogdo':
                if simbase.air.wantCogdominiums:
                    building.setState('cogdo')

            else:
                building.setState('toon')
        else:
            building.setState('toon')
        self._DistributedBuildingMgrAI__buildings[blockNumber] = building
        return building

    def newAnimBuilding(self, blockNumber, blockData=None):
        building = DistributedAnimBuildingAI.DistributedAnimBuildingAI(
            self.air, blockNumber, self.branchID, self.trophyMgr)
        building.generateWithRequired(self.branchID)
        if blockData:
            building.track = blockData.get('track', 'c')
            building.difficulty = int(blockData.get('difficulty', 1))
            building.numFloors = int(blockData.get('numFloors', 1))
            if not ZoneUtil.isWelcomeValley(building.zoneId):
                building.updateSavedBy(blockData.get('savedBy'))
            else:
                self.notify.warning(
                    'we had a cog building in welcome valley %d' %
                    building.zoneId)
            building.becameSuitTime = blockData.get('becameSuitTime',
                                                    time.time())
            if blockData['state'] == 'suit':
                building.setState('suit')
            else:
                building.setState('toon')
        else:
            building.setState('toon')
        self._DistributedBuildingMgrAI__buildings[blockNumber] = building
        return building

    def newHQBuilding(self, blockNumber):
        dnaStore = self.air.dnaStoreMap[self.canonicalBranchID]
        exteriorZoneId = dnaStore.getZoneFromBlockNumber(blockNumber)
        exteriorZoneId = ZoneUtil.getTrueZoneId(exteriorZoneId, self.branchID)
        interiorZoneId = (
            self.branchID - self.branchID % 100) + 500 + blockNumber
        building = HQBuildingAI.HQBuildingAI(self.air, exteriorZoneId,
                                             interiorZoneId, blockNumber)
        self._DistributedBuildingMgrAI__buildings[blockNumber] = building
        return building

    def newGagshopBuilding(self, blockNumber):
        dnaStore = self.air.dnaStoreMap[self.canonicalBranchID]
        exteriorZoneId = dnaStore.getZoneFromBlockNumber(blockNumber)
        exteriorZoneId = ZoneUtil.getTrueZoneId(exteriorZoneId, self.branchID)
        interiorZoneId = (
            self.branchID - self.branchID % 100) + 500 + blockNumber
        building = GagshopBuildingAI.GagshopBuildingAI(
            self.air, exteriorZoneId, interiorZoneId, blockNumber)
        self._DistributedBuildingMgrAI__buildings[blockNumber] = building
        return building

    def newPetshopBuilding(self, blockNumber):
        dnaStore = self.air.dnaStoreMap[self.canonicalBranchID]
        exteriorZoneId = dnaStore.getZoneFromBlockNumber(blockNumber)
        exteriorZoneId = ZoneUtil.getTrueZoneId(exteriorZoneId, self.branchID)
        interiorZoneId = (
            self.branchID - self.branchID % 100) + 500 + blockNumber
        building = PetshopBuildingAI.PetshopBuildingAI(
            self.air, exteriorZoneId, interiorZoneId, blockNumber)
        self._DistributedBuildingMgrAI__buildings[blockNumber] = building
        return building

    def newKartShopBuilding(self, blockNumber):
        dnaStore = self.air.dnaStoreMap[self.canonicalBranchID]
        exteriorZoneId = dnaStore.getZoneFromBlockNumber(blockNumber)
        exteriorZoneId = ZoneUtil.getTrueZoneId(exteriorZoneId, self.branchID)
        interiorZoneId = (
            self.branchID - self.branchID % 100) + 500 + blockNumber
        building = KartShopBuildingAI(self.air, exteriorZoneId, interiorZoneId,
                                      blockNumber)
        self._DistributedBuildingMgrAI__buildings[blockNumber] = building
        return building

    def getFileName(self):
        f = '%s%s_%d.buildings' % (self.serverDatafolder, self.shard,
                                   self.branchID)
        return f

    def saveTo(self, file, block=None):
        if block:
            pickleData = block.getPickleData()
            cPickle.dump(pickleData, file)
        else:
            for i in self._DistributedBuildingMgrAI__buildings.values():
                if isinstance(i, HQBuildingAI.HQBuildingAI):
                    continue

                pickleData = i.getPickleData()
                cPickle.dump(pickleData, file)

    def fastSave(self, block):
        return None

        try:
            fileName = self.getFileName() + '.delta'
            working = fileName + '.temp'
            if os.path.exists(working):
                os.remove(working)

            os.rename(fileName, working)
            file = open(working, 'w')
            file.seek(0, 2)
            self.saveTo(file, block)
            file.close()
            os.rename(working, fileName)
        except IOError:
            self.notify.error(str(sys.exc_info()[1]))

    def save(self):

        try:
            fileName = self.getFileName()
            backup = fileName + self.backupExtension
            if os.path.exists(fileName):
                os.rename(fileName, backup)

            file = open(fileName, 'w')
            file.seek(0)
            self.saveTo(file)
            file.close()
            if os.path.exists(backup):
                os.remove(backup)
        except EnvironmentError:
            self.notify.warning(str(sys.exc_info()[1]))

    def loadFrom(self, file):
        blocks = {}

        try:
            while None:
                pickleData = cPickle.load(file)
                blocks[int(pickleData['block'])] = pickleData
        except EOFError:
            pass

        return blocks

    def load(self):
        fileName = self.getFileName()

        try:
            file = open(fileName + self.backupExtension, 'r')
            if os.path.exists(fileName):
                os.remove(fileName)
        except IOError:

            try:
                file = open(fileName, 'r')
            except IOError:
                return {}

        file.seek(0)
        blocks = self.loadFrom(file)
        file.close()
        return blocks
