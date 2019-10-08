import ply.lex as lex
import sys, collections
from panda3d.core import PandaNode, NodePath, Filename, DecalEffect, TextNode, SceneGraphReducer, FontPool
from panda3d.core import LVector3f, LVector4f, BitMask32, TexturePool, ModelNode, TextProperties, DepthWriteAttrib, LPoint3f, LVecBase3f
from direct.showbase import Loader
from direct.stdpy.file import *
import math, random
from DNATypesetter import DNATypesetter

tokens = [
  'FLOAT',
  'INTEGER',
  'UNQUOTED_STRING',
  'QUOTED_STRING'
]

reserved = {
  'store_suit_point' : 'STORE_SUIT_POINT',
  'group' : 'GROUP',
  'visgroup' : 'VISGROUP',
  'vis' : 'VIS',
  'STREET_POINT' : 'STREET_POINT',
  'FRONT_DOOR_POINT' : 'FRONT_DOOR_POINT',
  'SIDE_DOOR_POINT' : 'SIDE_DOOR_POINT',
  'COGHQ_IN_POINT' : 'COGHQ_IN_POINT',
  'COGHQ_OUT_POINT' : 'COGHQ_OUT_POINT',
  'suit_edge' : 'SUIT_EDGE',
  'battle_cell' : 'BATTLE_CELL',
  'prop' : 'PROP',
  'pos' : 'POS',
  'hpr' : 'HPR',
  'scale' : 'SCALE',
  'code' : 'CODE',
  'color' : 'COLOR',
  'model' : 'MODEL',
  'store_node' : 'STORE_NODE',
  'sign' : 'SIGN',
  'baseline' : 'BASELINE',
  'width' : 'WIDTH',
  'height' : 'HEIGHT',
  'stomp' : 'STOMP',
  'stumble' : 'STUMBLE',
  'indent' : 'INDENT',
  'wiggle' : 'WIGGLE',
  'kern' : 'KERN',
  'text' : 'TEXT',
  'letters' : 'LETTERS',
  'store_font' : 'STORE_FONT',
  'flat_building' : 'FLAT_BUILDING',
  'wall' : 'WALL',
  'windows' : 'WINDOWS',
  'count' : 'COUNT',
  'cornice' : 'CORNICE',
  'landmark_building' : 'LANDMARK_BUILDING',
  'title' : 'TITLE',
  'article' : 'ARTICLE',
  'building_type' : 'BUILDING_TYPE',
  'door' : 'DOOR',
  'store_texture' : 'STORE_TEXTURE',
  'street' : 'STREET',
  'texture' : 'TEXTURE',
  'graphic' : 'GRAPHIC',
  'hood_model' : 'HOODMODEL',
  'place_model' : 'PLACEMODEL',
  'nhpr' : 'NHPR',
  'flags' : 'FLAGS',
  'node' : 'NODE',
  'flat_door' : 'FLAT_DOOR',
  'anim' : 'ANIM',
  'cell_id' : 'CELL_ID',
  'anim_prop' : 'ANIM_PROP',
  'interactive_prop' : 'INTERACTIVE_PROP',
  'anim_building' : 'ANIM_BUILDING',
}
tokens += reserved.values()
t_ignore = ' \t'

literals = '[],'

def t_ignore_COMMENT(t):
    pass
t_ignore_COMMENT.__doc__ = r'[/]{2,2}.*'

def t_ignore_ML_COMMENT(t):
    pass
t_ignore_ML_COMMENT.__doc__ = r'\/\*([^*]|[\r\n])*\*/'

def t_QUOTED_STRING(t):
    t.value = t.value[1:-1]
    return t
t_QUOTED_STRING.__doc__ = r'["][^"]*["]'

def t_FLOAT(t):
    t.value = float(t.value)
    return t
t_FLOAT.__doc__ = r'[+-]?\d+[.]\d*([e][+-]\d+)?'

def t_INTEGER(t):
    t.value = int(t.value)
    return t
t_INTEGER.__doc__ = r'[+-]?\d+'

def t_UNQUOTED_STRING(t):
    if t.value in reserved:
        t.type = reserved[t.value]
    return t
t_UNQUOTED_STRING.__doc__ = r'[^ \t\n\r\[\],"]+'

def t_newline(t):
    t.lexer.lineno += len(t.value)
t_newline.__doc__ = r'\n+'

def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex(optimize=0)

def wl(file, ilevel, string):
    file.write('\t'*ilevel + string + '\n')

class DNAError(Exception):
    pass

class DNAStorage:
    def __init__(self):
        self.suitPoints = []
        self.suitPointMap = {}
        self.DNAGroups = {}
        self.DNAVisGroups = []
        self.suitEdges = {}
        self.battleCells = []
        self.nodes = {}
        self.hoodNodes = {}
        self.placeNodes = {}
        self.fonts = {}
        self.blockTitles = {}
        self.blockArticles = {}
        self.blockBuildingTypes = {}
        self.blockDoors = {}
        self.blockNumbers = []
        self.blockZones = {}
        self.textures = {}
        self.catalogCodes = {}

    def getSuitPath(self, startPoint, endPoint, minPathLen = 40, maxPathLen = 300):
        path = DNASuitPath()
        path.addPoint(startPoint)
        while path.getNumPoints() < maxPathLen:
            startPointIndex = startPoint.getIndex()
            if startPointIndex == endPoint.getIndex():
                if path.getNumPoints() >= minPathLen:
                    break
            if startPointIndex not in self.suitEdges:
                raise DNAError('Could not find DNASuitPath.')
            edges = self.suitEdges[startPointIndex]
            for edge in edges:
                startPoint = edge.getEndPoint()
                startPointType = startPoint.getPointType()
                if startPointType != DNASuitPoint.FRONT_DOOR_POINT:
                    if startPointType != DNASuitPoint.SIDE_DOOR_POINT:
                        break
            else:
                raise DNAError('Could not find DNASuitPath.')
            path.addPoint(startPoint)
        return path

    def getSuitEdgeTravelTime(self, startIndex, endIndex, suitWalkSpeed):
        startPoint = self.suitPointMap.get(startIndex)
        endPoint = self.suitPointMap.get(endIndex)
        if (not startPoint) or (not endPoint):
            return 0.0
        distance = (endPoint.getPos()-startPoint.getPos()).length()
        return distance / suitWalkSpeed

    def getSuitEdgeZone(self, startIndex, endIndex):
        return self.getSuitEdge(startIndex, endIndex).getZoneId()

    def getAdjacentPoints(self, point):
        path = DNASuitPath()
        startIndex = point.getIndex()
        if startIndex not in self.suitEdges:
            return path
        for edge in self.suitEdges[startIndex]:
            path.addPoint(edge.getEndPoint())
        return path

    def storeSuitPoint(self, suitPoint):
        if not isinstance(suitPoint, DNASuitPoint):
            raise TypeError('suitPoint must be an instance of DNASuitPoint')
        self.suitPoints.append(suitPoint)
        self.suitPointMap[suitPoint.getIndex()] = suitPoint

    def getSuitPointAtIndex(self, index):
        return self.suitPoints[index]

    def getSuitPointWithIndex(self, index):
        return self.suitPointMap.get(index)

    def resetSuitPoints(self):
        self.suitPoints = []
        self.suitPointMap = {}
        self.suitEdges = {}

    def resetTextures(self):
        self.textures = {}

    def resetHood(self):
        self.resetBlockNumbers()

    def findDNAGroup(self, node):
        return self.DNAGroups[node]

    def removeDNAGroup(self, dnagroup):
        for node, group in self.DNAGroups.items():
            if group == dnagroup:
                del self.DNAGroups[node]

    def resetDNAGroups(self):
        self.DNAGroups = {}

    def getNumDNAVisGroups(self):
        return len(self.DNAVisGroups)

    def getDNAVisGroupName(self, i):
        return self.DNAVisGroups[i].getName()

    def storeDNAVisGroup(self, group):
        self.DNAVisGroups.append(group)

    def storeSuitEdge(self, startIndex, endIndex, zoneId):
        startPoint = self.getSuitPointWithIndex(startIndex)
        endPoint = self.getSuitPointWithIndex(endIndex)
        edge = DNASuitEdge(startPoint, endPoint, zoneId)
        self.suitEdges.setdefault(startIndex, []).append(edge)
        return edge

    def getSuitEdge(self, startIndex, endIndex):
        edges = self.suitEdges[startIndex]
        for edge in edges:
            if edge.getEndPoint().getIndex() == endIndex:
                return edge

    def removeBattleCell(self, cell):
        self.battleCells.remove(cell)

    def storeBattleCell(self, cell):
        self.battleCells.append(cell)

    def resetBattleCells(self):
        self.battleCells = []

    def findNode(self, code):
        if code in self.nodes:
            return self.nodes[code]
        if code in self.hoodNodes:
            return self.hoodNodes[code]
        if code in self.placeNodes:
            return self.placeNodes[code]

    def resetNodes(self):
        self.nodes = {}

    def resetHoodNodes(self):
        self.hoodNodes = {}

    def resetPlaceNodes(self):
        self.placeNodes = {}

    def storeNode(self, node, code):
        self.nodes[code] = node

    def storeHoodNode(self, node, code):
        self.hoodNodes[code] = node

    def storePlaceNode(self, node, code):
        self.placeNodes[code] = node

    def findFont(self, code):
        if code in self.fonts:
            return self.fonts[code]

    def resetFonts(self):
        self.fonts = {}

    def storeFont(self, font, code):
        self.fonts[code] = font

    def getBlock(self, name):
        block = name[name.find(':')-2:name.find(':')]
        if not block[0].isdigit():
            block = block[1:]
        return block

    def getBlockBuildingType(self, blockNumber):
        if blockNumber in self.blockBuildingTypes:
            return self.blockBuildingTypes[blockNumber]

    def getTitleFromBlockNumber(self, blockNumber):
        if blockNumber in self.blockTitles:
            return self.blockTitles[blockNumber]
        return ''

    def getDoorPosHprFromBlockNumber(self, blockNumber):
        key = str(blockNumber)
        if key in self.blockDoors:
            return self.blockDoors[key]

    def storeBlockDoor(self, blockNumber, door):
        self.blockDoors[str(blockNumber)] = door

    def storeBlockTitle(self, blockNumber, title):
        self.blockTitles[blockNumber] = title

    def storeBlockArticle(self, blockNumber, article):
        self.blockArticles[blockNumber] = article

    def storeBlockBuildingType(self, blockNumber, buildingType):
        self.blockBuildingTypes[blockNumber] = buildingType

    def storeTexture(self, name, texture):
        self.textures[name] = texture

    def getSignTransformFromBlockNumber(self, blockNumber):
        print('getSignTransformFromBlockNumber was called for blockNumber: {0}.'.format(blockNumber))
        from panda3d.core import Mat4
        return Mat4(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    def resetDNAVisGroups(self):
        self.DNAVisGroups = []

    def resetDNAVisGroupsAI(self):
        self.resetDNAVisGroups()

    def getNumDNAVisGroupsAI(self):
        return self.getNumDNAVisGroups()

    def getNumSuitPoints(self):
        return len(self.suitPoints)

    def getNumVisiblesInDNAVisGroup(self, i):
        return self.DNAVisGroups[i].getNumVisibles()

    def getVisibleName(self, i, j):
        return self.DNAVisGroups[i].getVisibleName(j)

    def getDNAVisGroupAI(self, i):
        return self.DNAVisGroups[i]

    def storeCatalogCode(self, category, code):
        if not category in self.catalogCodes:
            self.catalogCodes[category] = []
        self.catalogCodes[category].append(code)

    def getNumCatalogCodes(self, category):
        if category not in self.catalogCodes:
            return -1
        return len(self.catalogCodes[category])

    def getCatalogCode(self, category, index):
        return self.catalogCodes[category][index]

    def findTexture(self, name):
        if name in self.textures:
            return self.textures[name]

    def discoverContinuity(self):
        return 1  # TODO

    def resetBlockNumbers(self):
        self.blockNumbers = []
        self.blockZones = {}
        self.blockArticles = {}
        self.blockDoors = {}
        self.blockTitles = {}
        self.blockBuildingTypes = {}

    def getNumBlockNumbers(self):
        return len(self.blockNumbers)

    def storeBlockNumber(self, blockNumber):
        self.blockNumbers.append(blockNumber)

    def getBlockNumberAt(self, index):
        return self.blockNumbers[index]

    def getZoneFromBlockNumber(self, blockNumber):
        if blockNumber in self.blockZones:
            return self.blockZones[blockNumber]

    def storeBlockZone(self, blockNumber, zoneId):
        self.blockZones[blockNumber] = zoneId

    def resetBlockZones(self):
        self.blockZones = {}

    def ls(self):
        print 'DNASuitPoints:'
        for suitPoint in self.suitPoints:
            print '\t', suitPoint
        print 'DNABattleCells:'
        for cell in self.battleCells:
            print '\t', cell

class DNASuitPath:
    def __init__(self):
        self.suitPoints = []

    def getNumPoints(self):
        return len(self.suitPoints)

    def getPointIndex(self, pointIndex):
        return self.suitPoints[pointIndex].getIndex()

    def addPoint(self, point):
        self.suitPoints.append(point)

    def getPoint(self, pointIndex):
        return self.suitPoints[pointIndex]

    def reversePath(self):
        self.suitPoints.reverse()

class DNASuitPoint:
    STREET_POINT = 0
    FRONT_DOOR_POINT = 1
    SIDE_DOOR_POINT = 2
    COGHQ_IN_POINT = 3
    COGHQ_OUT_POINT = 4

    STREETPOINT = 0
    FRONTDOORPOINT = 1
    SIDEDOORPOINT = 2
    COGHQINPOINT = 3
    COGHQOUTPOINT = 4

    def __init__(self, index, pointType, pos, landmarkBuildingIndex = -1):
        self.index = index
        self.pointType = pointType
        self.pos = pos
        self.graphId = 0
        self.landmarkBuildingIndex = landmarkBuildingIndex

    def __str__(self):
        pointType = self.getPointType()
        if pointType == DNASuitPoint.STREET_POINT:
            pointTypeStr = 'STREET_POINT'
        elif pointType == DNASuitPoint.FRONT_DOOR_POINT:
            pointTypeStr = 'FRONT_DOOR_POINT'
        elif pointType == DNASuitPoint.SIDE_DOOR_POINT:
            pointTypeStr = 'SIDE_DOOR_POINT'
        elif pointType == DNASuitPoint.COGHQ_IN_POINT:
            pointTypeStr = 'COGHQ_IN_POINT'
        elif pointType == DNASuitPoint.COGHQ_OUT_POINT:
            pointTypeStr = 'COGHQ_OUT_POINT'
        else:
            pointTypeStr = '**invalid**'
        return 'DNASuitPoint index: {0}, pointType: {1}, pos: {2}'.format(
            self.getIndex(), pointTypeStr, self.getPos())

    def setIndex(self, index):
        self.index = index

    def getIndex(self):
        return self.index

    def getGraphId(self):
        return self.graphId

    def getLandmarkBuildingIndex(self):
        return self.landmarkBuildingIndex

    def getPos(self):
        return self.pos

    def isTerminal(self):
        return self.pointType <= 2

    def setGraphId(self, id):
        self.graphId = id

    def setLandmarkBuildingIndex(self, index):
        self.landmarkBuildingIndex = index

    def setPointType(self, pointType):
        if isinstance(pointType, int):
            if type == DNASuitPoint.STREET_POINT:
                self.pointType = DNASuitPoint.STREET_POINT
            elif type == DNASuitPoint.FRONT_DOOR_POINT:
                self.pointType = DNASuitPoint.FRONT_DOOR_POINT
            elif pointType == DNASuitPoint.SIDE_DOOR_POINT:
                self.pointType = DNASuitPoint.SIDE_DOOR_POINT
            elif pointType == DNASuitPoint.COGHQ_IN_POINT:
                self.pointType = DNASuitPoint.COGHQ_IN_POINT
            elif pointType == DNASuitPoint.COGHQ_OUT_POINT:
                self.pointType = DNASuitPoint.COGHQ_OUT_POINT
            else:
                raise TypeError('%i is not a valid DNASuitPointType' % pointType)
        elif isinstance(pointType, str):
            if type == 'STREET_POINT':
                self.pointType = DNASuitPoint.STREET_POINT
            elif type == 'FRONT_DOOR_POINT':
                self.pointType = DNASuitPoint.FRONT_DOOR_POINT
            elif pointType == 'SIDE_DOOR_POINT':
                self.pointType = DNASuitPoint.SIDE_DOOR_POINT
            elif pointType == 'COGHQ_IN_POINT':
                self.pointType = DNASuitPoint.COGHQ_IN_POINT
            elif pointType == 'COGHQ_OUT_POINT':
                self.pointType = DNASuitPoint.COGHQ_OUT_POINT
            else:
                raise TypeError('%s is not a valid DNASuitPointType' % pointType)

    def getPointType(self):
        return self.pointType

    def setPos(self, pos):
        self.pos = pos

class DNABattleCell:

    def __init__(self, width, height, pos):
        self.width = width
        self.height = height
        self.pos = pos

    def __str__(self):
        return 'DNABattleCell width: ' + str(self.width) + ' height: ' + str(self.height) + ' pos: ' + str(self.pos)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getPos(self):
        return self.pos

    def setWidthHeight(self, width, height):
        self.width = width
        self.height = height

class DNASuitEdge:

    def __init__(self, startpt, endpt, zoneId):
        self.startpt = startpt
        self.endpt = endpt
        self.zoneId = zoneId

    def getEndPoint(self):
        return self.endpt

    def getStartPoint(self):
        return self.startpt

    def getZoneId(self):
        return self.zoneId

    def setZoneId(self, zoneId):
        self.zoneId = zoneId

class DNAGroup:

    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None
        self.visGroup = None

    def add(self, child):
        self.children += [child]

    def at(self, index):
        return self.children[index]

    def clearParent(self):
        self.parent = None
        self.visGroup = None

    def getVisGroup(self):
        return self.visGroup

    def getNumChildren(self):
        return len(self.children)

    def getParent(self):
        return self.parent

    def remove(self, child):
        self.children.remove(child)

    def setParent(self, parent):
        self.parent = parent
        self.visGroup = parent.getVisGroup()

    def getName(self):
        return self.name

    def traverse(self, nodePath, dnaStorage):
        node = PandaNode(self.name)
        nodePath = nodePath.attachNewNode(node, 0)
        for child in self.children:
            child.traverse(nodePath, dnaStorage)

class DNAVisGroup(DNAGroup):

    def __init__(self, name):
        DNAGroup.__init__(self, name)
        self.visibles = []
        self.suitEdges = []
        self.battleCells = []

    def getVisGroup(self):
        return self

    def addBattleCell(self, battleCell):
        self.battleCells.append(battleCell)

    def addSuitEdge(self, suitEdge):
        self.suitEdges.append(suitEdge)

    def addVisible(self, visible):
        self.visibles.append(visible)

    def getBattleCell(self, i):
        return self.battleCells[i]

    def getNumBattleCells(self):
        return len(self.battleCells)

    def getNumSuitEdges(self):
        return len(self.suitEdges)

    def getNumVisibles(self):
        return len(self.visibles)

    def getSuitEdge(self, i):
        return self.suitEdges[i]

    def getVisibleName(self, i):
        return self.visibles[i]

    def removeBattleCell(self, cell):
        self.battleCells.remove(cell)

    def removeSuitEdge(self, edge):
        self.suitEdges.remove(edge)

    def removeVisible(self, visible):
        self.visibles.remove(visible)

    def traverse(self, nodePath, dnaStorage):
        DNAGroup.traverse(self, nodePath, dnaStorage)

class DNAData(DNAGroup):

    def __init__(self, name):
        DNAGroup.__init__(self, name)
        self.coordSystem = 0
        self.dnaFilename = ''
        self.dnaStorage = None

    def getCoordSystem(self):
        return self.coordSystem

    def getDnaFilename(self):
        return self.dnaFilename

    def getDnaStorage(self):
        if self.dnaStorage is None:
            self.dnaStorage = DNAStorage()
        return self.dnaStorage

    def setCoordSystem(self, system):
        self.coordSystem = system

    def setDnaFilename(self, filename):
        self.dnaFilename = filename

    def setDnaStorage(self, storage):
        self.dnaStorage = storage

    def read(self, stream):
        parser = yacc.yacc(debug=0, optimize=0, write_tables=0)
        parser.dnaData = self
        parser.parentGroup = parser.dnaData
        parser.dnaStore = self.getDnaStorage()
        parser.nodePath = None
        parser.parse(stream.read())

class DNANode(DNAGroup):

    def __init__(self, name):
        DNAGroup.__init__(self, name)
        self.pos = LVector3f(0, 0, 0)
        self.hpr = LVector3f(0, 0, 0)
        self.scale = LVector3f(1, 1, 1)

    def getPos(self):
        return self.pos

    def getHpr(self):
        return self.hpr

    def getScale(self):
        return self.scale

    def setPos(self, pos):
        self.pos = pos

    def setHpr(self, hpr):
        self.hpr = hpr

    def setScale(self, scale):
        self.scale = scale

    def traverse(self, nodePath, dnaStorage):
        node = PandaNode(self.name)
        node = nodePath.attachNewNode(node, 0)
        node.setPosHprScale(self.pos, self.hpr, self.scale)
        node.setColorScale(LVector4f(nodePath.getColor()), 0)

        for child in self.children:
            child.traverse(node, dnaStorage)

class DNAProp(DNANode):

    def __init__(self, name):
        DNANode.__init__(self, name)
        self.code = ''
        self.color = LVector4f(1, 1, 1, 1)

    def setCode(self, code):
        self.code = code

    def setColor(self, color):
        self.color = color

    def getCode(self):
        return self.code

    def getColor(self):
        return self.color

    def traverse(self, nodePath, dnaStorage):
        if self.code == 'DCS':
            node = ModelNode(self.name)
            node.setPreserveTransform(ModelNode.PTNet)
            node = nodePath.attachNewNode(node)
        else:
            node = dnaStorage.findNode(self.code)
            if node is None:
                return
            
            node = node.copyTo(nodePath, 0)
        
        node.setPosHprScale(self.pos, self.hpr, self.scale)
        node.setName(self.name)
        node.setColorScale(LVector4f(self.color), 0)

        for child in self.children:
            child.traverse(node, dnaStorage)

class DNASign(DNANode):

    def __init__(self):
        DNANode.__init__(self, '')
        self.code = ''
        self.color = LVector4f(1, 1, 1, 1)

    def setCode(self, code):
        self.code = code

    def setColor(self, color):
        self.color = color

    def getCode(self):
        return self.code

    def getColor(self):
        return self.color

    def traverse(self, nodePath, dnaStorage):
        sign = dnaStorage.findNode(self.code)
        if not sign:
            sign = NodePath(self.name)
        signOrigin = nodePath.find('**/*sign_origin')
        if not signOrigin:
            signOrigin = nodePath
        node = sign.copyTo(signOrigin)
        node.setDepthOffset(50) # todo
        node.setPosHprScale(signOrigin, self.pos, self.hpr, self.scale)
        node.setPos(node, 0, -0.1, 0)
        node.setColor(LVector4f(self.color))
        for child in self.children:
            child.traverse(node, dnaStorage)
        
        node.flattenStrong()

class DNASignBaseline(DNANode):

    def __init__(self):
        DNANode.__init__(self, '')
        self.code = ''
        self.color = LVector4f(1, 1, 1, 1)
        self.font = None
        self.flags = ''
        self.indent = 0.0
        self.kern = 0.0
        self.wiggle = 0.0
        self.stumble = 0.0
        self.stomp = 0.0
        self.width = 0
        self.height = 0

    def setCode(self, code):
        self.code = code

    def setColor(self, color):
        self.color = color

    def getCode(self):
        return self.code

    def getColor(self):
        return self.color

    def getFont(self):
        return self.font

    def getHeight(self):
        return self.height

    def getIndent(self):
        return self.indent

    def getKern(self):
        return self.kern

    def getStomp(self):
        return self.stomp

    def getStumble(self):
        return self.stumble

    def getWidth(self):
        return self.width

    def getWiggle(self):
        return self.wiggle

    def setFont(self, font):
        self.font = font

    def setHeight(self, height):
        self.height = height

    def setIndent(self, indent):
        self.indent = indent

    def setKern(self, kern):
        self.kern = kern

    def setStomp(self, stomp):
        self.stomp = stomp

    def setStumble(self, stumble):
        self.stumble = stumble

    def setWidth(self, width):
        self.width = width

    def setWiggle(self, wiggle):
        self.wiggle = wiggle

    def setFlags(self, flags):
        self.flags = flags

    def getFlags(self):
        return self.flags

    def traverse(self, nodePath, dnaStorage):
        nodePath = nodePath.attachNewNode('baseline', 0)
        nodePath.setPos(self.pos)
        nodePath.setHpr(self.hpr)
        nodePath.setDepthOffset(50)
        nodePath.setColor(LVector4f(self.color))

        texts = []
        for child in self.children:
            if child.__class__ == DNASignText:
                texts.append(child.letters)
            else:
                child.traverse(nodePath, dnaStorage)

        typesetter = DNATypesetter(self, dnaStorage)
        np = typesetter.generate(texts)
        if np:
            np.reparentTo(nodePath, 0)

class DNASignText(DNANode):

    def __init__(self):
        DNANode.__init__(self, '')
        self.letters = ''

    def setLetters(self, letters):
        self.letters = letters

    def traverse(self, nodePath, dnaStorage):
        return

class DNAFlatBuilding(DNANode):
    currentWallHeight = 0

    def __init__(self, name):
        DNANode.__init__(self, name)
        self.hasDoor = False

    def getWidth(self):
        return self.width

    def setWidth(self, width):
        self.width = width

    def getCurrentWallHeight(self):
        return DNAFlatBuilding.currentWallHeight

    def setHasDoor(self, hasDoor):
        self.hasDoor = True

    def getHasDoor(self):
        return self.hasDoor

    def setupSuitFlatBuilding(self, nodePath, dnaStorage):
        name = self.getName()
        if name[:2] != 'tb':
            return
        name = 'sb' + name[2:]
        node = nodePath.attachNewNode(name)
        node.setPosHpr(self.getPos(), self.getHpr())
        numCodes = dnaStorage.getNumCatalogCodes('suit_wall')
        if numCodes < 1:
            return
        code = dnaStorage.getCatalogCode(
            'suit_wall', random.randint(0, numCodes - 1))
        wallNode = dnaStorage.findNode(code)
        if not wallNode:
            return
        wallNode = wallNode.copyTo(node, 0)
        wallScale = wallNode.getScale()
        wallScale.setX(self.width)
        wallScale.setZ(DNAFlatBuilding.currentWallHeight)
        wallNode.setScale(wallScale)
        wallNode.flattenMedium()
        if self.getHasDoor():
            wallNodePath = node.find('wall_*')
            doorNode = dnaStorage.findNode('suit_door')
            doorNode = doorNode.copyTo(wallNodePath, 0)
            doorNode.setScale(NodePath(), (1, 1, 1))
            doorNode.setPosHpr(0.5, 0, 0, 0, 0, 0)
            wallNodePath.setEffect(DecalEffect.make())
        
        node.flattenMedium()
        node.stash()

    def setupCogdoFlatBuilding(self, nodePath, dnaStorage):
        name = self.getName()
        if name[:2] != 'tb':
            return
        name = 'cb' + name[2:]
        node = nodePath.attachNewNode(name)
        node.setPosHpr(self.getPos(), self.getHpr())
        numCodes = dnaStorage.getNumCatalogCodes('cogdo_wall')
        if numCodes < 1:
            return
        code = dnaStorage.getCatalogCode(
            'cogdo_wall', random.randint(0, numCodes - 1))
        wallNode = dnaStorage.findNode(code)
        if not wallNode:
            return
        wallNode = wallNode.copyTo(node, 0)
        wallScale = wallNode.getScale()
        wallScale.setX(self.width)
        wallScale.setZ(DNAFlatBuilding.currentWallHeight)
        wallNode.setScale(wallScale)
        if self.getHasDoor():
            wallNodePath = node.find('wall_*')
            doorNode = dnaStorage.findNode('suit_door')
            doorNode = doorNode.copyTo(wallNodePath, 0)
            doorNode.setScale(NodePath(), (1, 1, 1))
            doorNode.setPosHpr(0.5, 0, 0, 0, 0, 0)
            wallNodePath.setEffect(DecalEffect.make())
        node.flattenMedium()
        node.stash()

    def traverse(self, nodePath, dnaStorage):
        DNAFlatBuilding.currentWallHeight = 0
        node = nodePath.attachNewNode(self.getName())
        internalNode = node.attachNewNode(self.getName() + '-internal')
        scale = self.getScale()
        scale.setX(self.width)
        internalNode.setScale(scale)
        node.setPosHpr(self.getPos(), self.getHpr())
        for child in self.children:
            if isinstance(child, DNAWall):
                child.traverse(internalNode, dnaStorage)
            else:
                child.traverse(node, dnaStorage)
        if DNAFlatBuilding.currentWallHeight == 0:
            print 'empty flat building with no walls'
        else:
            cameraBarrier = dnaStorage.findNode('wall_camera_barrier')
            if cameraBarrier is None:
                raise DNAError('DNAFlatBuilding requires that there is a wall_camera_barrier in storage')
            cameraBarrier = cameraBarrier.copyTo(internalNode, 0)
            cameraBarrier.setScale((1, 1, DNAFlatBuilding.currentWallHeight))
            internalNode.flattenStrong()
            collisionNode = node.find('**/door_*/+CollisionNode')
            if not collisionNode.isEmpty():
                collisionNode.setName('KnockKnockDoorSphere_' + dnaStorage.getBlock(self.getName()))
            cameraBarrier.wrtReparentTo(nodePath, 0)
            wallCollection = internalNode.findAllMatches('wall*')
            wallHolder = node.attachNewNode('wall_holder')
            wallDecal = node.attachNewNode('wall_decal')
            windowCollection = internalNode.findAllMatches('**/window*')
            doorCollection = internalNode.findAllMatches('**/door*')
            corniceCollection = internalNode.findAllMatches('**/cornice*_d')
            wallCollection.reparentTo(wallHolder)
            windowCollection.reparentTo(wallDecal)
            doorCollection.reparentTo(wallDecal)
            corniceCollection.reparentTo(wallDecal)
            for i in xrange(wallHolder.getNumChildren()):
                iNode = wallHolder.getChild(i)
                iNode.clearTag('DNACode')
                iNode.clearTag('DNARoot')
            wallHolder.flattenStrong()
            wallDecal.flattenStrong()
            holderChild0 = wallHolder.getChild(0)
            wallDecal.getChildren().reparentTo(holderChild0)
            holderChild0.reparentTo(internalNode)
            holderChild0.setEffect(DecalEffect.make())
            wallHolder.removeNode()
            wallDecal.removeNode()
            self.setupSuitFlatBuilding(nodePath, dnaStorage)
            self.setupCogdoFlatBuilding(nodePath, dnaStorage)

class DNAWall(DNANode):

    def __init__(self, name):
        DNANode.__init__(self, name)
        self.code = ''
        self.height = 10
        self.color = LVector4f(1, 1, 1, 1)

    def getCode(self):
        return self.code

    def getColor(self):
        return self.color

    def getHeight(self):
        return self.height

    def setCode(self, code):
        self.code = code

    def setColor(self, color):
        self.color = color

    def setHeight(self, height):
        self.height = height

    def traverse(self, nodePath, dnaStorage):
        node = dnaStorage.findNode(self.code)
        if node is None:
            raise DNAError('DNAWall code ' + self.code + ' not found in DNAStorage')
        node = node.copyTo(nodePath, 0)
        self.pos.setZ(DNAFlatBuilding.currentWallHeight)
        self.scale.setZ(self.height)
        node.setPosHprScale(self.pos, self.hpr, self.scale)
        node.setColor(LVector4f(self.color))
        for child in self.children:
            child.traverse(node, dnaStorage)
        DNAFlatBuilding.currentWallHeight += self.height

class DNAWindows(DNAGroup):

    def __init__(self, name):
        DNAGroup.__init__(self, name)
        self.setCode('')
        self.setColor(LVector4f(1, 1, 1, 1))
        self.setWindowCount(1)

    def getCode(self):
        return self.code

    def getColor(self):
        return self.color

    def getWindowCount(self):
        return self.windowCount

    def setCode(self, code):
        self.code = code

    def setColor(self, color):
        self.color = color

    def setWindowCount(self, count):
        self.windowCount = count

    def getCode(self):
        return self.code

    def getColor(self):
        return self.color

    def getWindowCount(self):
        return self.windowCount

    def setCode(self, code):
        self.code = code

    def setColor(self, color):
        self.color = color

    def setWindowCount(self, count):
        self.windowCount = count

    @staticmethod
    def setupWindows(parentNode, dnaStorage, code, windowCount, color, hpr,
                     scale):
        stripped = code[:-1]
        node_r = dnaStorage.findNode(stripped + 'r')
        node_l = dnaStorage.findNode(stripped + 'l')
        if (node_r is None) or (node_l is None):
            raise DNAError('DNAWindows code {0} not found in'
                           'DNAStorage'.format(code))

        def makeWindow(x, y, z, parentNode, color, scale, hpr, flip = False):
            node = node_r if not flip else node_l
            window = node.copyTo(parentNode, 0)
            window.setColor(LVector4f(color))
            window.setScale(NodePath(), scale)
            window.setHpr(hpr)
            window.setPos(x, 0, z)
            window.setAttrib(DepthWriteAttrib.makeDefault(), 0)
            return window

        offset = lambda: random.random() % 0.0375
        if windowCount == 1:
            makeWindow(offset() + 0.5, 0, offset() + 0.5,
                       parentNode, LVector4f(color), scale, hpr)
        elif windowCount == 2:
            makeWindow(offset() + 0.33, 0, offset() + 0.5,
                       parentNode, LVector4f(color), scale, hpr)
            makeWindow(offset() + 0.66, 0, offset() + 0.5,
                       parentNode, LVector4f(color), scale, hpr, True)
        elif windowCount == 3:
            makeWindow(offset() + 0.33, 0, offset() + 0.66,
                       parentNode, LVector4f(color), scale, hpr)
            makeWindow(offset() + 0.66, 0, offset() + 0.66,
                       parentNode, LVector4f(color), scale, hpr, True)
            makeWindow(offset() + 0.5, 0, offset() + 0.33,
                       parentNode, LVector4f(color), scale, hpr)
        elif windowCount == 4:
            makeWindow(offset() + 0.33, 0, offset() + 0.25,
                       parentNode, LVector4f(color), scale, hpr)
            makeWindow(offset() + 0.66, 0, offset() + 0.25,
                       parentNode, LVector4f(color), scale, hpr, True)
            makeWindow(offset() + 0.33, 0, offset() + 0.66,
                       parentNode, LVector4f(color), scale, hpr)
            makeWindow(offset() + 0.66, 0, offset() + 0.66,
                       parentNode, LVector4f(color), scale, hpr, True)
        else:
            raise NotImplementedError(
                'Invalid window count {0}'.format(windowCount))

    def traverse(self, nodePath, dnaStorage):
        if self.getWindowCount() == 0:
            return
        parentX = nodePath.getParent().getScale().getX()
        scale = random.random() % 0.0375
        if parentX <= 5.0:
            scale += 1.0
        elif parentX <= 10.0:
            scale += 1.15
        else:
            scale += 1.3
        hpr = (0, 0, 0)
        DNAWindows.setupWindows(nodePath, dnaStorage, self.getCode(),
                                self.getWindowCount(), LVector4f(self.getColor()), hpr,
                                scale)

class DNACornice(DNAGroup):

    def __init__(self, name):
        DNAGroup.__init__(self, name)
        self.setCode('')
        self.setColor(LVector4f(1, 1, 1, 1))

    def setCode(self, code):
        self.code = code

    def setColor(self, color):
        self.color = color

    def getCode(self):
        return self.code

    def getColor(self):
        return self.color

    def traverse(self, nodePath, dnaStorage):
        pParentXScale = nodePath.getParent().getScale().getX()
        parentZScale = nodePath.getScale().getZ()
        node = dnaStorage.findNode(self.getCode())
        if node is None:
            raise DNAError('DNACornice code {0} not found in '
                           'DNAStorage'.format(self.getCode()))
        nodePathA = nodePath.attachNewNode('cornice-internal', 0)
        node = node.find('**/*_d')
        np = node.copyTo(nodePathA, 0)
        np.setPosHprScale(
            LVector3f(0, 0, 0),
            LVector3f(0, 0, 0),
            LVector3f(1, pParentXScale/parentZScale,
                      pParentXScale/parentZScale))
        np.setEffect(DecalEffect.make())
        node = node.getParent().find('**/*_nd')
        np = node.copyTo(nodePathA, 1)
        np.setPosHprScale(
            LVector3f(0, 0, 0),
            LVector3f(0, 0, 0),
            LVector3f(1, pParentXScale/parentZScale,
                      pParentXScale/parentZScale))
        nodePathA.setPosHprScale(
            LVector3f(0, 0, node.getScale().getZ()),
            LVector3f(0, 0, 0),
            LVector3f(1, 1, 1))
        nodePathA.setColor(LVector4f(self.getColor()))

class DNALandmarkBuilding(DNANode):

    def __init__(self, name):
        DNANode.__init__(self, name)
        self.code = ''
        self.wallColor = LVector4f(1, 1, 1, 1)
        self.title = ''
        self.article = ''
        self.buildingType = ''
        self.door = None

    def getArticle(self):
        return self.article

    def getBuildingType(self):
        return self.buildingType

    def getTitle(self):
        return self.title

    def setCode(self, code):
        self.code = code

    def setWallColor(self, color):
        self.wallColor = color

    def getCode(self):
        return self.code

    def getWallColor(self):
        return self.wallColor

    def setArticle(self, article):
        self.article = article

    def setBuildingType(self, buildingType):
        self.buildingType = buildingType

    def setTitle(self, title):
        self.title = title

    def setupSuitBuildingOrigin(self, nodePathA, nodePathB):
        if (self.getName()[:2] == 'tb') and (self.getName()[3].isdigit()) and (self.getName().find(':') != -1):
            name = self.getName()
            name = 's' + name[1:]
            node = nodePathB.find('**/*suit_building_origin')
            if node.isEmpty():
                node = nodePathA.attachNewNode(name)
                node.setPosHprScale(self.getPos(), self.getHpr(), self.getScale())
            else:
                node.wrtReparentTo(nodePathA, 0)
                node.setName(name)

    def traverse(self, nodePath, dnaStorage):
        node = dnaStorage.findNode(self.code)
        if node is None:
            raise DNAError('DNALandmarkBuilding code ' + self.code + ' not found in DNAStorage')
        npA = nodePath
        nodePath = node.copyTo(nodePath, 0)
        nodePath.setName(self.getName())
        nodePath.setPosHprScale(self.getPos(), self.getHpr(), self.getScale())
        nodePath.setColorScale(LVector4f(self.getWallColor()))
        self.setupSuitBuildingOrigin(npA, nodePath)
        for child in self.children:
            child.traverse(nodePath, dnaStorage)
        nodePath.flattenStrong()

class DNADoor(DNAGroup):

    def __init__(self, name):
        DNAGroup.__init__(self, name)
        self.code = ''
        self.color = LVector4f(1, 1, 1, 1)

    def setCode(self, code):
        self.code = code

    def setColor(self, color):
        self.color = color

    def getCode(self):
        return self.code

    def getColor(self):
        return self.color

    @staticmethod
    def setupDoor(doorNodePath, parentNode, doorOrigin, dnaStore, block, color):
        doorNodePath.setPosHprScale(doorOrigin, (0, 0, 0), (0, 0, 0), (1, 1, 1))
        doorNodePath.setColor(color, 0)
        leftHole = doorNodePath.find('door_*_hole_left')
        leftHole.setName('doorFrameHoleLeft')
        rightHole = doorNodePath.find('door_*_hole_right')
        rightHole.setName('doorFrameHoleRight')
        leftDoor = doorNodePath.find('door_*_left')
        leftDoor.setName('leftDoor')
        rightDoor = doorNodePath.find('door_*_right')
        rightDoor.setName('rightDoor')
        doorFlat = doorNodePath.find('door_*_flat')
        leftHole.wrtReparentTo(doorFlat, 0)
        rightHole.wrtReparentTo(doorFlat, 0)
        doorFlat.setEffect(DecalEffect.make())
        rightDoor.wrtReparentTo(parentNode, 0)
        leftDoor.wrtReparentTo(parentNode, 0)

        rightDoor.setColor(color, 0)
        leftDoor.setColor(color, 0)
        leftHole.setColor((0, 0, 0, 1), 0)
        rightHole.setColor((0, 0, 0, 1), 0)

        leftDoor.hide()
        rightDoor.hide()
        leftHole.hide()
        rightHole.hide()

        doorTrigger = doorNodePath.find('door_*_trigger')
        doorTrigger.setScale(2, 2, 2)
        doorTrigger.wrtReparentTo(parentNode, 0)
        doorTrigger.setName('door_trigger_' + block)

        if not dnaStore.getDoorPosHprFromBlockNumber(block):
            store = NodePath('door-%s' % block)
            store.setPosHprScale(doorNodePath, (0, 0, 0), (0, 0, 0), (1, 1, 1))
            dnaStore.storeBlockDoor(block, store)

    def traverse(self, nodePath, dnaStorage):
        frontNode = nodePath.find('**/*_front')
        if not frontNode.getNode(0).isGeomNode():
            frontNode = frontNode.find('**/+GeomNode')
        frontNode.setEffect(DecalEffect.make())
        node = dnaStorage.findNode(self.code)
        if node is None:
            raise DNAError('DNADoor code ' + self.code + ' not found in DNAStorage')
        doorNode = node.copyTo(frontNode, 0)
        block = dnaStorage.getBlock(nodePath.getName())
        DNADoor.setupDoor(doorNode, nodePath, nodePath.find('**/*door_origin'), dnaStorage, block, self.color)

class DNAStreet(DNANode):

    def __init__(self, name):
        DNANode.__init__(self, name)
        self.code = ''
        self.streetTexture = ''
        self.sideWalkTexture = ''
        self.curbTexture = ''
        self.streetColor = LVector4f(1, 1, 1, 1)
        self.sidewalkColor = LVector4f(1, 1, 1, 1)
        self.curbColor = LVector4f(1, 1, 1, 1)
        self.setTexCnt = 0
        self.setColCnt = 0

    def setCode(self, code):
        self.code = code

    def getCode(self):
        return self.code

    def getStreetTexture(self):
        return self.streetTexture

    def getSidewalkTexture(self):
        return self.sidewalkTexture

    def getCurbTexture(self):
        return self.curbTexture

    def getStreetColor(self):
        return self.streetColor

    def getSidewalkColor(self):
        return self.sidewalkColor

    def getCurbColor(self):
        return self.curbColor

    def setStreetTexture(self, texture):
        self.streetTexture = texture

    def setSidewalkTexture(self, texture):
        self.sidewalkTexture = texture

    def setCurbTexture(self, texture):
        self.curbTexture = texture

    def setStreetColor(self, color):
        self.streetColor = color

    def setSidewalkColor(self, color):
        self.SidewalkColor = color

    def setTextureColor(self, color):
        self.Color = color

    def setTexture(self, texture):
        if self.setTexCnt == 0:
            self.streetTexture = texture
        if self.setTexCnt == 1:
            self.sidewalkTexture = texture
        if self.setTexCnt == 2:
            self.curbTexture = texture
        self.setTexCnt += 1

    def setColor(self, color):
        if self.setColCnt == 0:
            self.streetColor = color
        if self.setColCnt == 1:
            self.sidewalkColor = color
        if self.setColCnt == 2:
            self.curbColor = color
        self.setColCnt += 1

    def traverse(self, nodePath, dnaStorage):
        node = dnaStorage.findNode(self.code)
        if node is None:
            raise DNAError('DNAStreet code ' + self.code + ' not found in DNAStorage')
        nodePath = node.copyTo(nodePath, 0)
        node.setName(self.getName())
        streetTexture = dnaStorage.findTexture(self.streetTexture)
        sidewalkTexture = dnaStorage.findTexture(self.sidewalkTexture)
        curbTexture = dnaStorage.findTexture(self.curbTexture)
        if streetTexture is None:
            raise DNAError('street texture not found in DNAStorage : ' + self.streetTexture)
        if sidewalkTexture is None:
            raise DNAError('sidewalk texture not found in DNAStorage : ' + self.sidewalkTexture)
        if curbTexture is None:
            raise DNAError('curb texture not found in DNAStorage : ' + self.curbTexture)
        streetNode = nodePath.find('**/*_street')
        sidewalkNode = nodePath.find('**/*_sidewalk')
        curbNode = nodePath.find('**/*_curb')

        if not streetNode.isEmpty():
            streetNode.setTexture(streetTexture, 1)
            streetNode.setColorScale(LVector4f(self.streetColor), 0)
        if not sidewalkNode.isEmpty():
            sidewalkNode.setTexture(sidewalkTexture, 1)
            sidewalkNode.setColorScale(LVector4f(self.sidewalkColor), 0)
        if not curbNode.isEmpty():
            curbNode.setTexture(curbTexture, 1)
            curbNode.setColorScale(LVector4f(self.curbColor), 0)

        nodePath.setPosHprScale(self.getPos(), self.getHpr(), self.getScale())

class DNASignGraphic(DNANode):

    def __init__(self, name):
        DNANode.__init__(self, name)
        self.code = ''
        self.color = LVector4f(1, 1, 1, 1)
        self.width = 0
        self.height = 0
        self.bDefaultColor = True

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getCode(self):
        return self.code

    def getColor(self):
        return self.Color

    def setWidth(self, width):
        self.width = width

    def setHeight(self, height):
        self.height = height

    def setCode(self, code):
        self.code = code

    def setColor(self, color):
        self.color = color
        self.bDefaultColor = False

    def traverse(self, nodePath, dnaStorage):
        nodePath.getTop().getNode(0).setEffect(DecalEffect.make())
        node = dnaStorage.findNode(self.code)
        if node is None:
            raise DNAError('DNASignGraphic code ' + self.code + ' not found in storage')
        node = node.copyTo(nodePath, 0)
        node.setScale(self.scale)
        node.setScale(node, self.getParent().scale)
        node.setPosHpr(self.pos, self.hpr)
        node.setColor(LVector4f(self.color))
        for child in self.children:
            child.traverse(node, dnaStorage)

class DNAFlatDoor(DNADoor):

    def __init__(self, name):
        DNADoor.__init__(self, name)

    def traverse(self, nodePath, dnaStorage):
        node = dnaStorage.findNode(self.getCode())
        node = node.copyTo(nodePath, 0)
        node.setScale(NodePath(), (1, 1, 1))
        node.setPosHpr((0.5, 0, 0), (0, 0, 0))
        node.setColor(LVector4f(self.getColor()))
        node.getNode(0).setEffect(DecalEffect.make())

class DNAAnimProp(DNAProp):

    def __init__(self, name):
        DNAProp.__init__(self, name)
        self.animName = ''

    def setAnim(self, anim):
        self.animName = anim

    def getAnim(self):
        return self.animName

    def traverse(self, nodePath, dnaStorage):
        node = None
        if self.getCode() == "DCS":
            node = ModelNode(self.getName())
            node.setPreserveTransform(ModelNode.PTNet)
            node = nodePath.attachNewNode(node, 0)
        else:
            node = dnaStorage.findNode(self.getCode())
            node = node.copyTo(nodePath, 0)
            node.setName(self.getName())

        node.setTag('DNAAnim', self.getAnim())
        node.setPosHprScale(self.getPos(), self.getHpr(), self.getScale())
        node.setColorScale(LVector4f(self.getColor()), 0)
        for child in self.children:
            child.traverse(node, dnaStorage)

class DNAInteractiveProp(DNAAnimProp):

    def __init__(self, name):
        DNAAnimProp.__init__(self, name)
        self.cellId = -1

    def setCellId(self, id):
        self.cellId = id

    def getCellId(self):
        return self.cellId

    def traverse(self, nodePath, dnaStorage):
        node = None
        if self.getCode() == "DCS":
            node = ModelNode(self.getName())
            node.setPreserveTransform(ModelNode.PTNet)
            node = nodePath.attachNewNode(node, 0)
        else:
            node = dnaStorage.findNode(self.getCode())
            node = node.copyTo(nodePath, 0)
            node.setName(self.getName())

        node.setTag('DNAAnim', self.getAnim())
        node.setTag('DNACellIndex', str(self.cellId))
        node.setPosHprScale(self.getPos(), self.getHpr(), self.getScale())
        node.setColorScale(LVector4f(self.getColor()), 0)
        for child in self.children:
            child.traverse(node, dnaStorage)

class DNAAnimBuilding(DNALandmarkBuilding):

    def __init__(self, name):
        DNALandmarkBuilding.__init__(self, name)
        self.animName = ''

    def setAnim(self, anim):
        self.animName = anim

    def getAnim(self):
        return self.animName

    def traverse(self, nodePath, dnaStorage):
        node = dnaStorage.findNode(self.getCode())
        if node is None:
            raise DNAError('DNAAnimBuilding code ' + self.getCode() + ' not found in dnastore')
        node = node.copyTo(nodePath, 0)
        node.setName(self.getName())
        node.setPosHprScale(self.getPos(), self.getHpr(), self.getScale())
        node.setTag('DNAAnim', self.animName)
        self.setupSuitBuildingOrigin(nodePath, node)
        for child in self.children:
            child.traverse(nodePath, dnaStorage)
        nodePath.flattenStrong()

class DNALoader:

    def __init__(self):
        node = PandaNode('dna')
        self.nodePath = NodePath(node)
        self.data = DNAData("loader_data")

    def buildGraph(self):
        self.data.traverse(self.nodePath, self.data.getDnaStorage())
        if self.nodePath.getChild(0).getNumChildren() == 0:
            return None
        return self.nodePath.getChild(0).getChild(0)

    def getData(self):
        return self.data

import ply.yacc as yacc

def p_dna(p):
    pass
p_dna.__doc__ = \
    '''dna : dna object
           | object'''

def p_object(p):
    p[0] = p[1]
p_object.__doc__ = \
    '''object : suitpoint
              | group
              | model
              | font
              | store_texture'''

def p_number(p):
    p[0] = p[1]
p_number.__doc__ = \
    '''number : FLOAT
              | INTEGER'''

def p_lpoint3f(p):
    p[0] = LVector3f(p[1], p[2], p[3])
p_lpoint3f.__doc__ = '''lpoint3f : number number number'''

def p_suitpoint(p):
    landmarkBuildingIndex = -1
    if len(p) > 9:
        landmarkBuildingIndex = p[9]
    point = DNASuitPoint(p[3], p[5], p[7],
                         landmarkBuildingIndex=landmarkBuildingIndex)
    p.parser.dnaStore.storeSuitPoint(point)
p_suitpoint.__doc__ = \
    '''suitpoint : STORE_SUIT_POINT "[" number "," suitpointtype "," lpoint3f "]"
                 | STORE_SUIT_POINT "[" number "," suitpointtype "," lpoint3f "," number "]"'''

def p_suitpointtype(p):
    pointTypeStr = p[1]
    if pointTypeStr == 'STREET_POINT':
        p[0] = DNASuitPoint.STREET_POINT
    elif pointTypeStr == 'FRONT_DOOR_POINT':
        p[0] = DNASuitPoint.FRONT_DOOR_POINT
    elif pointTypeStr == 'SIDE_DOOR_POINT':
        p[0] = DNASuitPoint.SIDE_DOOR_POINT
    elif pointTypeStr == 'COGHQ_IN_POINT':
        p[0] = DNASuitPoint.COGHQ_IN_POINT
    elif pointTypeStr == 'COGHQ_OUT_POINT':
        p[0] = DNASuitPoint.COGHQ_OUT_POINT
p_suitpointtype.__doc__ = \
    '''suitpointtype : STREET_POINT
                     | FRONT_DOOR_POINT
                     | SIDE_DOOR_POINT
                     | COGHQ_IN_POINT
                     | COGHQ_OUT_POINT'''

def p_string(p):
    p[0] = p[1]
p_string.__doc__ = \
    '''string : QUOTED_STRING
              | UNQUOTED_STRING'''

def p_dnagroupdef(p):
    p[0] = DNAGroup(p[2])
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]
p_dnagroupdef.__doc__ = '''dnagroupdef : GROUP string'''

def p_dnanodedef(p):
    p[0] = DNANode(p[2])
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]
p_dnanodedef.__doc__ = '''dnanodedef : NODE string'''

def p_visgroupdef(p):
    p[0] = DNAVisGroup(p[2])
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]
    p.parser.dnaStore.storeDNAVisGroup(p[0])
p_visgroupdef.__doc__ = '''visgroupdef : VISGROUP string'''

def p_dnagroup(p):
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()
p_dnagroup.__doc__ = '''dnagroup : dnagroupdef "[" subgroup_list "]"'''

def p_visgroup(p):
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()
p_visgroup.__doc__ = '''visgroup : visgroupdef "[" subvisgroup_list "]"'''

def p_string_opt_list(p):
    if len(p) == 2:
        p[0] = []
    if len(p) == 3 and not p[2] is None:
        p[0] = p[1]
        p[0] += [p[2]]
p_string_opt_list.__doc__ = \
    '''string_opt_list : string_opt_list string
                       | empty'''

def p_vis(p):
    p.parser.parentGroup.addVisible(p[3])
    for vis in p[4]:
        p.parser.parentGroup.addVisible(vis)
p_vis.__doc__ = '''vis : VIS "[" string string_opt_list "]"'''

def p_empty(p):
    pass
p_empty.__doc__ = \
    '''empty : '''

def p_group(p):
    p[0] = p[1]
p_group.__doc__ = \
    '''group : dnagroup
             | visgroup
             | dnanode
             | windows
             | cornice
             | door'''

def p_dnanode(p):
    p[0] = p[1]
p_dnanode.__doc__ = \
    '''dnanode : prop
               | sign
               | signbaseline
               | signtext
               | flatbuilding
               | wall
               | landmarkbuilding
               | street
               | signgraphic
               | dnanode_grp'''

def p_dnanode_grp(p):
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()
p_dnanode_grp.__doc__ = '''dnanode_grp : dnanodedef "[" subdnanode_list "]"'''

def p_sign(p):
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()
p_sign.__doc__ = '''sign : signdef "[" subprop_list "]"'''

def p_signgraphic(p):
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()
p_signgraphic.__doc__ = '''signgraphic : signgraphicdef "[" subsigngraphic_list "]"'''

def p_prop(p):
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()
p_prop.__doc__ = \
    '''prop : propdef "[" subprop_list "]"
            | animpropdef "[" subanimprop_list "]"
            | interactivepropdef "[" subinteractiveprop_list "]"'''

def p_signbaseline(p):
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()
p_signbaseline.__doc__ = '''signbaseline : baselinedef "[" subbaseline_list "]"'''

def p_signtest(p):
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()
p_signtest.__doc__ = '''signtext : signtextdef "[" subtext_list "]"'''

def p_flatbuilding(p):
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()
p_flatbuilding.__doc__ = '''flatbuilding : flatbuildingdef "[" subflatbuilding_list "]"'''

def p_wall(p):
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()
p_wall.__doc__ = '''wall : walldef "[" subwall_list "]"'''

def p_windows(p):
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()
p_windows.__doc__ = '''windows : windowsdef "[" subwindows_list "]"'''

def p_cornice(p):
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()
p_cornice.__doc__ = '''cornice : cornicedef "[" subcornice_list "]"'''

def p_landmarkbuilding(p):
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()
p_landmarkbuilding.__doc__ = '''landmarkbuilding : landmarkbuildingdef "[" sublandmarkbuilding_list "]"
                                                 | animbuildingdef "[" subanimbuilding_list "]"'''

def p_street(p):
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()
p_street.__doc__ = '''street : streetdef "[" substreet_list "]"'''

def p_door(p):
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()
p_door.__doc__ = \
    '''door : doordef "[" subdoor_list "]"
            | flatdoordef "[" subdoor_list "]"'''

def p_propdef(p):
    p[0] = DNAProp(p[2])
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]
p_propdef.__doc__ = '''propdef : PROP string'''

def p_animpropdef(p):
    p[0] = DNAAnimProp(p[2])
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]
p_animpropdef.__doc__ = '''animpropdef : ANIM_PROP string'''

def p_interactivepropdef(p):
    p[0] = DNAInteractiveProp(p[2])
    p[0] = DNAInteractiveProp(p[2])
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]
p_interactivepropdef.__doc__ = '''interactivepropdef : INTERACTIVE_PROP string'''

def p_flatbuildingdef(p):
    p[0] = DNAFlatBuilding(p[2])
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]
p_flatbuildingdef.__doc__ = '''flatbuildingdef : FLAT_BUILDING string'''

def p_walldef(p):
    p[0] = DNAWall('')
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]
p_walldef.__doc__ = '''walldef : WALL'''

def p_windowsdef(p):
    p[0] = DNAWindows('')
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]
p_windowsdef.__doc__ = '''windowsdef : WINDOWS'''

def p_cornicedef(p):
    p[0] = DNACornice('')
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]
p_cornicedef.__doc__ = '''cornicedef : CORNICE'''

def p_landmarkbuildingdef(p):
    p[0] = DNALandmarkBuilding(p[2])
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    blockNumber = int(p.parser.dnaStore.getBlock(p[0].getName()))
    p.parser.dnaStore.storeBlockNumber(blockNumber)
    zoneId = int(p[0].getVisGroup().getName().split(':')[0])
    p.parser.dnaStore.storeBlockZone(blockNumber, zoneId)
    p.parser.parentGroup = p[0]
p_landmarkbuildingdef.__doc__ = '''landmarkbuildingdef : LANDMARK_BUILDING string'''

def p_animbuildingdef(p):
    p[0] = DNAAnimBuilding(p[2])
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]
p_animbuildingdef.__doc__ = '''animbuildingdef : ANIM_BUILDING string'''

def p_doordef(p):
    p[0] = DNADoor('')
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]
p_doordef.__doc__ = '''doordef : DOOR'''

def p_flatdoordef(p):
    p[0] = DNAFlatDoor('')
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup.getParent().setHasDoor(True)
    p.parser.parentGroup = p[0]
p_flatdoordef.__doc__ = '''flatdoordef : FLAT_DOOR'''

def p_streetdef(p):
    p[0] = DNAStreet(p[2])
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]
p_streetdef.__doc__ = '''streetdef : STREET string'''

def p_signdef(p):
    p[0] = DNASign()
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]
p_signdef.__doc__ = '''signdef : SIGN'''

def p_signgraphicdef(p):
    p[0] = DNASignGraphic('')
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]
p_signgraphicdef.__doc__ = '''signgraphicdef : GRAPHIC'''

def p_baselinedef(p):
    p[0] = DNASignBaseline()
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]
p_baselinedef.__doc__ = '''baselinedef : BASELINE'''

def p_signtextdef(p):
    p[0] = DNASignText()
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]
p_signtextdef.__doc__ = '''signtextdef : TEXT'''

def p_suitedge(p):
    zoneId = int(p.parser.parentGroup.getName())
    edge = p.parser.dnaStore.storeSuitEdge(p[3], p[4], zoneId)
    p.parser.parentGroup.addSuitEdge(edge)
p_suitedge.__doc__ = '''suitedge : SUIT_EDGE "[" number number "]"'''

def p_battlecell(p):
    p[0] = DNABattleCell(p[3], p[4], p[5])
    p.parser.dnaStore.storeBattleCell(p[0])
    p.parser.parentGroup.addBattleCell(p[0])
p_battlecell.__doc__ = '''battlecell : BATTLE_CELL "[" number number lpoint3f "]"'''

def p_subgroup_list(p):
    p[0] = p[1]
    if len(p) == 3:
        p[0] += [p[2]]
    else:
        p[0] = []
p_subgroup_list.__doc__ = \
    '''subgroup_list : subgroup_list group
                     | empty'''

def p_subvisgroup_list(p):
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []
p_subvisgroup_list.__doc__ = \
    '''subvisgroup_list : subvisgroup_list group
                        | subvisgroup_list suitedge
                        | subvisgroup_list battlecell
                        | subvisgroup_list vis
                        | empty'''

def p_pos(p):
    p.parser.parentGroup.setPos(p[3])
p_pos.__doc__ = '''pos : POS "[" lpoint3f "]"'''

def p_hpr(p):
    p.parser.parentGroup.setHpr(p[3])
p_hpr.__doc__ = \
    '''hpr : HPR "[" lpoint3f "]"
           | NHPR "[" lpoint3f "]"'''

def p_scale(p):
    p.parser.parentGroup.setScale(p[3])
p_scale.__doc__ = '''scale : SCALE "[" lpoint3f "]"'''

def p_flags(p):
    p.parser.parentGroup.setFlags(p[3])
p_flags.__doc__ = '''flags : FLAGS "[" string "]"'''

def p_dnanode_sub(p):
    p[0] = p[1]
p_dnanode_sub.__doc__ = \
    '''dnanode_sub : group
                   | pos
                   | hpr
                   | scale'''

def p_dnaprop_sub(p):
    p[0] = p[1]
p_dnaprop_sub.__doc__ = \
    '''dnaprop_sub : code
                   | color'''

def p_dnaanimprop_sub(p):
    p[0] = p[1]
p_dnaanimprop_sub.__doc__ = '''dnaanimprop_sub : anim'''

def p_dnainteractiveprop_sub(p):
    p[0] = p[1]
p_dnainteractiveprop_sub.__doc__ = '''dnainteractiveprop_sub : cell_id'''

def p_anim(p):
    p.parser.parentGroup.setAnim(p[3])
p_anim.__doc__ = '''anim : ANIM "[" string "]"'''

def p_cell_id(p):
    p.parser.parentGroup.setCellId(p[3])
p_cell_id.__doc__ = '''cell_id : CELL_ID "[" number "]"'''

def p_baseline_sub(p):
    p[0] = p[1]
p_baseline_sub.__doc__ = \
    '''baseline_sub : code
                    | color
                    | width
                    | height
                    | indent
                    | kern
                    | stomp
                    | stumble
                    | wiggle
                    | flags'''

def p_text_sub(p):
    p[0] = p[1]
p_text_sub.__doc__ = '''text_sub : letters'''

def p_signgraphic_sub(p):
    p[0] = p[1]
p_signgraphic_sub.__doc__ = \
    '''signgraphic_sub : width
                       | height
                       | code
                       | color'''

def p_flatbuilding_sub(p):
    p[0] = p[1]
p_flatbuilding_sub.__doc__ = '''flatbuilding_sub : width'''

def p_wall_sub(p):
    p[0] = p[1]
p_wall_sub.__doc__ = \
    '''wall_sub : height
                | code
                | color'''

def p_windows_sub(p):
    p[0] = p[1]
p_windows_sub.__doc__ = \
    '''windows_sub : code
                   | color
                   | windowcount'''

def p_cornice_sub(p):
    p[0] = p[1]
p_cornice_sub.__doc__ = \
    '''cornice_sub : code
                   | color'''

def p_landmarkbuilding_sub(p):
    p[0] = p[1]
p_landmarkbuilding_sub.__doc__ = \
    '''landmarkbuilding_sub : code
                            | title
                            | article
                            | building_type
                            | wall_color'''

def p_animbuilding_sub(p):
    p[0] = p[1]
p_animbuilding_sub.__doc__ = \
    '''animbuilding_sub : anim'''

def p_door_sub(p):
    p[0] = p[1]
p_door_sub.__doc__ = \
    '''door_sub : code
                | color'''

def p_street_sub(p):
    p[0] = p[1]
p_street_sub.__doc__ = \
    '''street_sub : code
                  | texture
                  | color'''

def p_texture(p):
    p.parser.parentGroup.setTexture(p[3])
p_texture.__doc__ = '''texture : TEXTURE "[" string "]"'''

def p_title(p):
    p.parser.parentGroup.setTitle(p[3])
    blockNumber = int(p.parser.dnaStore.getBlock(p.parser.parentGroup.getName()))
    p.parser.dnaStore.storeBlockTitle(blockNumber, p[3])
p_title.__doc__ = '''title : TITLE "[" string "]"'''

def p_article(p):
    p.parser.parentGroup.setArticle(p[3])
    blockNumber = int(p.parser.dnaStore.getBlock(p.parser.parentGroup.getName()))
    p.parser.dnaStore.storeBlockArticle(blockNumber, p[3])
p_article.__doc__ = '''article : ARTICLE "[" string "]"'''

def p_building_type(p):
    p.parser.parentGroup.setBuildingType(p[3])
    blockNumber = int(p.parser.dnaStore.getBlock(p.parser.parentGroup.getName()))
    p.parser.dnaStore.storeBlockBuildingType(blockNumber, p[3])
p_building_type.__doc__ = '''building_type : BUILDING_TYPE "[" string "]"'''

def p_wall_color(p):
    p.parser.parentGroup.setWallColor((p[3],p[4],p[5],p[6]))
p_wall_color.__doc__ = '''wall_color : COLOR "[" number number number number "]"'''

def p_count(p):
    p.parser.parentGroup.setWindowCount(p[3])
p_count.__doc__ = '''windowcount : COUNT "[" number "]"'''

def p_letters(p):
    p.parser.parentGroup.setLetters(p[3])
p_letters.__doc__ = '''letters : LETTERS "[" string "]"'''

def p_width(p):
    p.parser.parentGroup.setWidth(p[3])
p_width.__doc__ = '''width : WIDTH "[" number "]"'''

def p_height(p):
    p.parser.parentGroup.setHeight(p[3])
p_height.__doc__ = '''height : HEIGHT "[" number "]"'''

def p_stomp(p):
    p.parser.parentGroup.setStomp(p[3])
p_stomp.__doc__ = '''stomp : STOMP "[" number "]"'''

def p_indent(p):
    p.parser.parentGroup.setIndent(p[3])
p_indent.__doc__ = '''indent : INDENT "[" number "]"'''

def p_kern(p):
    p.parser.parentGroup.setKern(p[3])
p_kern.__doc__ = '''kern : KERN "[" number "]"'''

def p_stumble(p):
    p.parser.parentGroup.setStumble(p[3])
p_stumble.__doc__ = '''stumble : STUMBLE "[" number "]"'''

def p_wiggle(p):
    p.parser.parentGroup.setWiggle(p[3])
p_wiggle.__doc__ = '''wiggle : WIGGLE "[" number "]"'''

def p_code(p):
    p.parser.parentGroup.setCode(p[3])
p_code.__doc__ = '''code : CODE "[" string "]"'''

def p_color(p):
    p.parser.parentGroup.setColor((p[3],p[4],p[5],p[6]))
p_color.__doc__ = '''color : COLOR "[" number number number number "]"'''

def p_subprop_list(p):
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []
p_subprop_list.__doc__ = \
    '''subprop_list : subprop_list dnanode_sub
                    | subprop_list dnaprop_sub
                    | empty'''

def p_subanimprop_list(p):
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []
p_subanimprop_list.__doc__ = \
    '''subanimprop_list : subanimprop_list dnanode_sub
                        | subanimprop_list dnaprop_sub
                        | subanimprop_list dnaanimprop_sub
                        | empty'''

def p_subinteractiveprop_list(p):
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []
p_subinteractiveprop_list.__doc__ = \
    '''subinteractiveprop_list : subinteractiveprop_list dnanode_sub
                    | subinteractiveprop_list dnaprop_sub
                    | subinteractiveprop_list dnaanimprop_sub
                    | subinteractiveprop_list dnainteractiveprop_sub
                    | empty'''

def p_subbaseline_list(p):
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []
p_subbaseline_list.__doc__ = \
    '''subbaseline_list : subbaseline_list dnanode_sub
                        | subbaseline_list baseline_sub
                        | empty'''

def p_subtext_list(p):
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []
p_subtext_list.__doc__ = \
    '''subtext_list : subtext_list dnanode_sub
                    | subtext_list text_sub
                    | empty'''

def p_subdnanode_list(p):
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []
p_subdnanode_list.__doc__ = \
    '''subdnanode_list : subdnanode_list dnanode_sub
                       | empty'''

def p_subsigngraphic_list(p):
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []
p_subsigngraphic_list.__doc__ = \
    '''subsigngraphic_list : subsigngraphic_list dnanode_sub
                           | subsigngraphic_list signgraphic_sub
                           | empty'''

def p_subflatbuilding_list(p):
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []
p_subflatbuilding_list.__doc__ = \
    '''subflatbuilding_list : subflatbuilding_list dnanode_sub
                            | subflatbuilding_list flatbuilding_sub
                            | empty'''

def p_subwall_list(p):
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []
p_subwall_list.__doc__ = \
    '''subwall_list : subwall_list dnanode_sub
                    | subwall_list wall_sub
                    | empty'''

def p_subwindows_list(p):
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []
p_subwindows_list.__doc__ = \
    '''subwindows_list : subwindows_list dnanode_sub
                       | subwindows_list windows_sub
                       | empty'''

def p_subcornice_list(p):
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []
p_subcornice_list.__doc__ = \
    '''subcornice_list : subcornice_list dnanode_sub
                       | subcornice_list cornice_sub
                       | empty'''

def p_sublandmarkbuilding_list(p):
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []
p_sublandmarkbuilding_list.__doc__ = \
    '''sublandmarkbuilding_list : sublandmarkbuilding_list dnanode_sub
                                | sublandmarkbuilding_list landmarkbuilding_sub
                                | empty'''

def p_subanimbuilding_list(p):
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []
p_subanimbuilding_list.__doc__ = \
    '''subanimbuilding_list : subanimbuilding_list dnanode_sub
                            | subanimbuilding_list landmarkbuilding_sub
                            | subanimbuilding_list animbuilding_sub
                            | empty'''

def p_subdoor_list(p):
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []
p_subdoor_list.__doc__ = \
    '''subdoor_list : subdoor_list dnanode_sub
                    | subdoor_list door_sub
                    | empty'''

def p_substreet_list(p):
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []
p_substreet_list.__doc__ = \
    '''substreet_list : substreet_list dnanode_sub
                      | substreet_list street_sub
                      | empty'''

def p_modeldef(p):
    filename = Filename(p[2])
    filename.setExtension('bam')
    p.parser.nodePath = base.loader.loadModel(filename)
    p.parser.modelType = p[1]
p_modeldef.__doc__ = \
    '''modeldef : MODEL string
                | HOODMODEL string
                | PLACEMODEL string'''

def p_model(p):
    pass
p_model.__doc__ = '''model : modeldef "[" modelnode_list "]"'''

def p_modelnode_list(p):
    pass
p_modelnode_list.__doc__ = \
    '''modelnode_list : modelnode_list node
                      | empty'''

def p_node(p):
    nodePath = None
    search = ''
    code = ''
    root = ''
    if len(p) == 6:
        search = p[4]
        code = search
        root = p[3]
    else:
        search = p[5]
        code = p[4]
        root = p[3]
    p.parser.dnaStore.storeCatalogCode(root, code)
    if search != '':
        if search[0] == '!':
            nodePath = p.parser.nodePath
            nodePath.find('**/' + search[1:]).removeNode()
        else:
            nodePath = p.parser.nodePath.find('**/' + search)
    else:
        nodePath = p.parser.nodePath
    nodePath.setTag('DNACode', p[4])
    nodePath.setTag('DNARoot', p[3])
    if p.parser.modelType == 'hood_model':
        p.parser.dnaStore.storeHoodNode(nodePath, p[4])
    elif p.parser.modelType == 'place_model':
        p.parser.dnaStore.storePlaceNode(nodePath, p[4])
    else:
        p.parser.dnaStore.storeNode(nodePath, p[4])
p_node.__doc__ = \
    '''node : STORE_NODE "[" string string "]"
            | STORE_NODE "[" string string string "]"'''

def p_store_texture(p):
    filename = p[4]
    if len(p) == 7:
        filename = p[5]
    name = p[3]
    if len(p) == 7:
        name = p[4]
        p.parser.dnaStore.storeCatalogCode(p[3], name)
    texture = TexturePool.loadTexture(Filename(filename))
    p.parser.dnaStore.storeTexture(name, texture)
p_store_texture.__doc__ = \
    '''store_texture : STORE_TEXTURE "[" string string "]"
                     | STORE_TEXTURE "[" string string string "]"'''

def p_font(p):
    filename = Filename(p[5])
    if not filename.getExtension():
        filename.setExtension('bam')
    p.parser.dnaStore.storeFont(FontPool.loadFont(filename.cStr()), p[4])
p_font.__doc__ = \
    '''font : STORE_FONT "[" string string string "]"'''

def p_error(p):
    if p is None:
        raise DNAError('Syntax error unexpected EOF')
    raise DNAError('Syntax error at line ' + str(p.lexer.lineno) + ' token=' + str(p))

def loadDNAFile(dnaStore, filename, cs, editing):
    print 'Reading DNA file...', filename
    dnaloader = DNALoader()
    dnaloader.getData().setDnaStorage(dnaStore)
    dnaloader.getData().read(open(filename, 'r'))
    graph = dnaloader.buildGraph()
    if not graph is None:
        return graph.getNode(0)
    return None

def loadDNAFileAI(dnaStore, filename, cs):
    dnaloader = DNALoader()
    dnaloader.getData().setDnaStorage(dnaStore)
    dnaloader.getData().read(open(filename, 'r'))
    return dnaloader.getData()