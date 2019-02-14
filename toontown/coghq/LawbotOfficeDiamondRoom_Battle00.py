from toontown.coghq.SpecImports import *
GlobalEntities = {
    1000: {
        'type': 'levelMgr',
        'name': 'LevelMgr',
        'comment': '',
        'parentEntId': 0,
        'cogLevel': 0,
        'farPlaneDistance': 1500,
        'modelFilename': 'phase_11/models/lawbotHQ/LB_Zone13a',
        'wantDoors': 1
    },
    1001: {
        'type': 'editMgr',
        'name': 'EditMgr',
        'parentEntId': 0,
        'insertEntity': None,
        'removeEntity': None,
        'requestNewEntity': None,
        'requestSave': None
    },
    0: {
        'type': 'zone',
        'name': 'UberZone',
        'comment': '',
        'parentEntId': 0,
        'scale': 1,
        'description': '',
        'visibility': []
    },
    10001: {
        'type': 'battleBlocker',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(140, -2, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': 1,
        'cellId': 0,
        'radius': 15.0
    },
    10002: {
        'type': 'collisionSolid',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-96.727400000000003, 20.532299999999999, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'length': 10.0,
        'radius': 6.0,
        'showSolid': 0,
        'solidType': 'tube'
    },
    10003: {
        'type': 'collisionSolid',
        'name': 'copy of <unnamed>',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-96.727400000000003, -23.011700000000001, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'length': 10.0,
        'radius': 6.0,
        'showSolid': 0,
        'solidType': 'tube'
    },
    100001: {
        'type': 'model',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-4.7530200000000002, 55.148000000000003, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_torch_lampB'
    },
    100002: {
        'type': 'model',
        'name': 'copy of <unnamed>',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-4.7530200000000002, -55.149999999999999, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_torch_lampB'
    },
    100003: {
        'type': 'model',
        'name': 'copy of <unnamed> (2)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-24.807200000000002, -17.676200000000001, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_torch_lampB'
    },
    100004: {
        'type': 'model',
        'name': 'copy of <unnamed> (3)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-24.807200000000002, 17.68, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_torch_lampB'
    },
    100005: {
        'type': 'model',
        'name': 'copy of <unnamed> (4)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-93.695300000000003, 17.68, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(8, 8, 8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_pottedplantA'
    },
    100006: {
        'type': 'model',
        'name': 'copy of <unnamed> (5)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-99.5488, 17.68, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(8, 8, 8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_pottedplantA'
    },
    100007: {
        'type': 'model',
        'name': 'copy of <unnamed> (6)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-99.5488, -20.5, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(8, 8, 8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_pottedplantA'
    },
    100008: {
        'type': 'model',
        'name': 'copy of <unnamed> (5)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-93.695300000000003, -20.5, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(8, 8, 8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_pottedplantA'
    },
    100009: {
        'type': 'model',
        'name': 'copy of <unnamed> (2)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(13.263500000000001, -58.811999999999998, 0),
        'hpr': Vec3(211.70099999999999, 0, 0),
        'scale': Vec3(1.8, 1.8, 1.8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_bookshelfA'
    },
    100010: {
        'type': 'model',
        'name': 'copy of <unnamed> (3)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(32.482500000000002, -48.421599999999998, 0),
        'hpr': Vec3(211.70099999999999, 0, 0),
        'scale': Vec3(1.8, 1.8, 1.8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_bookshelfA'
    },
    100011: {
        'type': 'model',
        'name': 'copy of <unnamed> (4)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(53.5274, -37.233899999999998, 0),
        'hpr': Vec3(204.77500000000001, 0, 0),
        'scale': Vec3(1.8, 1.8, 1.8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_bookshelfA'
    },
    100012: {
        'type': 'model',
        'name': 'copy of <unnamed> (3)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(14.898, 55.5914, 0),
        'hpr': Vec3(336.37099999999998, 0, 0),
        'scale': Vec3(1.8, 1.8, 1.8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_bookshelfA'
    },
    100013: {
        'type': 'model',
        'name': 'copy of <unnamed> (4)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(37.338099999999997, 45.453400000000002, 0),
        'hpr': Vec3(335.22500000000002, 0, 0),
        'scale': Vec3(1.8, 1.8, 1.8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_bookshelfA'
    },
    100014: {
        'type': 'model',
        'name': 'copy of <unnamed> (5)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(60.449399999999997, 34.232300000000002, 0),
        'hpr': Vec3(334.01100000000002, 0, 0),
        'scale': Vec3(1.8, 1.8, 1.8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_bookshelfA'
    },
    10000: {
        'type': 'nodepath',
        'name': 'cogs',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(100, 0, 0),
        'hpr': Point3(270, 0, 0),
        'scale': Vec3(1, 1, 1)
    },
    100000: {
        'type': 'nodepath',
        'name': 'props',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0, 0, 0.050000000000000003),
        'hpr': Vec3(0, 0, 0),
        'scale': 1
    },
    100015: {
        'type': 'nodepath',
        'name': 'lights',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0, 0, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': 1
    },
    100017: {
        'type': 'nodepath',
        'name': 'cameratarget1',
        'comment': '',
        'parentEntId': 100015,
        'pos': Point3(-67.013800000000003, 21.058, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1)
    },
    100018: {
        'type': 'nodepath',
        'name': 'copy of cameratarget1',
        'comment': '',
        'parentEntId': 100015,
        'pos': Point3(-3.8951600000000002, 39.262999999999998, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1)
    },
    100019: {
        'type': 'nodepath',
        'name': 'copy of cameratarget1 (2)',
        'comment': '',
        'parentEntId': 100015,
        'pos': Point3(-23.922799999999999, 20.374400000000001, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1)
    },
    100020: {
        'type': 'nodepath',
        'name': 'lights2',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0, 4.9793000000000003, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1)
    },
    100022: {
        'type': 'nodepath',
        'name': 'camtar1',
        'comment': '',
        'parentEntId': 100020,
        'pos': Point3(16.287600000000001, -35.707099999999997, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1)
    },
    100023: {
        'type': 'nodepath',
        'name': 'copy of camtar1',
        'comment': '',
        'parentEntId': 100020,
        'pos': Point3(-52.291499999999999, -8.5052900000000005, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1)
    },
    100024: {
        'type': 'nodepath',
        'name': 'copy of camtar1 (2)',
        'comment': '',
        'parentEntId': 100020,
        'pos': Point3(-52.291499999999999, -37.532200000000003, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1)
    },
    100016: {
        'type':
        'securityCamera',
        'name':
        '<unnamed>',
        'comment':
        '',
        'parentEntId':
        100015,
        'pos':
        Point3(-45.870800000000003, 39.221499999999999, 0.050000000000000003),
        'hpr':
        Vec3(0, 0, 0),
        'scale':
        Vec3(1, 1, 1),
        'accel':
        5.0,
        'damPow':
        8,
        'hideModel':
        0,
        'maxVel':
        12.0,
        'modelPath':
        0,
        'projector':
        Point3(6, 6, 25),
        'radius':
        5,
        'switchId':
        0,
        'trackTarget1':
        100017,
        'trackTarget2':
        100018,
        'trackTarget3':
        100019
    },
    100021: {
        'type': 'securityCamera',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 100020,
        'pos': Point3(-45.286200000000001, -55.4163, 0.050000000000000003),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'accel': 5.0,
        'damPow': 8,
        'hideModel': 0,
        'maxVel': 12.0,
        'modelPath': 0,
        'projector': Point3(6, 6, 25),
        'radius': 5,
        'switchId': 0,
        'trackTarget1': 100022,
        'trackTarget2': 100023,
        'trackTarget3': 100024
    }
}
Scenario0 = {}
levelSpec = {'globalEntities': GlobalEntities, 'scenarios': [Scenario0]}
