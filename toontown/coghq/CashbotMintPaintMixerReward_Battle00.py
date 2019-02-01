from toontown.coghq.SpecImports import *
GlobalEntities = {
    1000: {
        'type': 'levelMgr',
        'name': 'LevelMgr',
        'comment': '',
        'parentEntId': 0,
        'cogLevel': 0,
        'farPlaneDistance': 1500,
        'modelFilename': 'phase_10/models/cashbotHQ/ZONE11a',
        'wantDoors': 1},
    1001: {
        'type': 'editMgr',
        'name': 'EditMgr',
        'parentEntId': 0,
        'insertEntity': None,
        'removeEntity': None,
        'requestNewEntity': None,
        'requestSave': None},
    0: {
        'type': 'zone',
        'name': 'UberZone',
        'comment': '',
        'parentEntId': 0,
        'scale': 1,
        'description': '',
        'visibility': []},
    10024: {
        'type': 'mintProduct',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10023,
        'pos': Point3(-4.0706076621999996, 0.0, 0.0),
        'hpr': Vec3(0.0, 0.0, 0.0),
        'scale': Vec3(1.0, 1.0, 1.0),
        'mintId': 12500},
    10003: {
        'type': 'mintShelf',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10008,
        'pos': Point3(0.0, 0.0, 0.0),
        'hpr': Vec3(0.0, 0.0, 0.0),
        'scale': Vec3(1.0, 1.0, 1.0),
        'mintId': 12600},
    10005: {
        'type': 'mintShelf',
        'name': 'copy of <unnamed>',
        'comment': '',
        'parentEntId': 10006,
        'pos': Point3(0.0, 0.0, 0.0),
        'hpr': Vec3(0.0, 0.0, 0.0),
        'scale': Vec3(1.0, 1.0, 1.0),
        'mintId': 12600},
    10007: {
        'type': 'mintShelf',
        'name': 'copy of <unnamed> (2)',
        'comment': '',
        'parentEntId': 10006,
        'pos': Point3(13.4306573868, 0.0, 0.0),
        'hpr': Vec3(0.0, 0.0, 0.0),
        'scale': Vec3(1.0, 1.0, 1.0),
        'mintId': 12600},
    10009: {
        'type': 'mintShelf',
        'name': 'copy of <unnamed>',
        'comment': '',
        'parentEntId': 10008,
        'pos': Point3(-13.4300003052, 0.0, 0.0),
        'hpr': Vec3(0.0, 0.0, 0.0),
        'scale': Vec3(1.0, 1.0, 1.0),
        'mintId': 12600},
    10013: {
        'type': 'mintShelf',
        'name': 'copy of <unnamed>',
        'comment': '',
        'parentEntId': 10011,
        'pos': Point3(-13.4300003052, 0.0, 0.0),
        'hpr': Vec3(0.0, 0.0, 0.0),
        'scale': Vec3(1.0, 1.0, 1.0),
        'mintId': 12600},
    10014: {
        'type': 'mintShelf',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10011,
        'pos': Point3(0.0, 0.0, 0.0),
        'hpr': Vec3(0.0, 0.0, 0.0),
        'scale': Vec3(1.0, 1.0, 1.0),
        'mintId': 12600},
    10015: {
        'type': 'mintShelf',
        'name': 'copy of <unnamed>',
        'comment': '',
        'parentEntId': 10012,
        'pos': Point3(0.0, 0.0, 0.0),
        'hpr': Vec3(0.0, 0.0, 0.0),
        'scale': Vec3(1.0, 1.0, 1.0),
        'mintId': 12600},
    10016: {
        'type': 'mintShelf',
        'name': 'copy of <unnamed> (2)',
        'comment': '',
        'parentEntId': 10012,
        'pos': Point3(13.4306573868, 0.0, 0.0),
        'hpr': Vec3(0.0, 0.0, 0.0),
        'scale': Vec3(1.0, 1.0, 1.0),
        'mintId': 12600},
    10001: {
        'type': 'model',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0.0, 22.236824035600002, 0.0),
        'hpr': Vec3(0.0, 0.0, 0.0),
        'scale': Vec3(1.0, 1.0, 1.0),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/VaultDoorCover.bam'},
    10000: {
        'type': 'nodepath',
        'name': 'cogs',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0.0, 0.0, 0.0),
        'hpr': Point3(0.0, 0.0, 0.0),
        'scale': Vec3(1.0, 1.0, 1.0)},
    10002: {
        'type': 'nodepath',
        'name': 'props',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0.0, 0.0, 0.0),
        'hpr': Vec3(0.0, 0.0, 0.0),
        'scale': 1},
    10004: {
        'type': 'nodepath',
        'name': 'backWall',
        'comment': '',
        'parentEntId': 10002,
        'pos': Point3(0.0, 19.078205108599999, 0.0),
        'hpr': Vec3(0.0, 0.0, 0.0),
        'scale': Vec3(1.0, 1.0, 1.0)},
    10006: {
        'type': 'nodepath',
        'name': 'rightShelves',
        'comment': '',
        'parentEntId': 10004,
        'pos': Point3(17.210630416899999, 0.0, 0.0),
        'hpr': Vec3(0.0, 0.0, 0.0),
        'scale': Vec3(1.0, 1.0, 1.0)},
    10008: {
        'type': 'nodepath',
        'name': 'leftShelves',
        'comment': '',
        'parentEntId': 10004,
        'pos': Point3(-17.477125167800001, 0.0, 0.0),
        'hpr': Vec3(0.0, 0.0, 0.0),
        'scale': Vec3(1.0, 1.0, 1.0)},
    10010: {
        'type': 'nodepath',
        'name': 'frontWall',
        'comment': '',
        'parentEntId': 10002,
        'pos': Point3(0.0, -19.125411987300001, 0.0),
        'hpr': Point3(180.0, 0.0, 0.0),
        'scale': Vec3(1.0, 1.0, 1.0)},
    10011: {
        'type': 'nodepath',
        'name': 'leftShelves',
        'comment': '',
        'parentEntId': 10010,
        'pos': Point3(-17.477125167800001, 0.0, 0.0),
        'hpr': Vec3(0.0, 0.0, 0.0),
        'scale': Vec3(1.0, 1.0, 1.0)},
    10012: {
        'type': 'nodepath',
        'name': 'rightShelves',
        'comment': '',
        'parentEntId': 10010,
        'pos': Point3(17.210630416899999, 0.0, 0.0),
        'hpr': Vec3(0.0, 0.0, 0.0),
        'scale': Vec3(1.0, 1.0, 1.0)},
    10023: {
        'type': 'nodepath',
        'name': 'byVaultDoor',
        'comment': '',
        'parentEntId': 10002,
        'pos': Point3(0.0, 16.037338256799998, 0.0),
        'hpr': Vec3(0.0, 0.0, 0.0),
        'scale': Vec3(1.0, 1.0, 1.0)}}
Scenario0 = {}
levelSpec = {
    'globalEntities': GlobalEntities,
    'scenarios': [
        Scenario0]}
