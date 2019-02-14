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
    100002: {
        'type': 'button',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(-10.795999999999999, 37.918100000000003, 0),
        'hpr': Vec3(23.962499999999999, 0, 0),
        'scale': Vec3(3, 3, 3),
        'color': Vec4(1, 1, 1, 1),
        'isOn': 0,
        'isOnEvent': 0,
        'secondsOn': -1.0
    },
    100003: {
        'type': 'button',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(-11.023, -40.736400000000003, 0),
        'hpr': Vec3(338.19900000000001, 0, 0),
        'scale': Vec3(3, 3, 3),
        'color': Vec4(1, 1, 1, 1),
        'isOn': 0,
        'isOnEvent': 0,
        'secondsOn': -1.0
    },
    100006: {
        'type': 'door',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 100010,
        'pos': Point3(0, 0, 0),
        'hpr': Vec3(1.0230300000000001, 0, 0),
        'scale': Vec3(1, 1, 1),
        'color': Vec4(1, 1, 1, 1),
        'isLock0Unlocked': 0,
        'isLock1Unlocked': 1,
        'isLock2Unlocked': 0,
        'isLock3Unlocked': 1,
        'isOpen': 0,
        'isOpenEvent': 0,
        'isVisBlocker': 1,
        'secondsOpen': 1,
        'unlock0Event': 100000,
        'unlock1Event': 0,
        'unlock2Event': 100001,
        'unlock3Event': 0
    },
    100000: {
        'type':
        'laserField',
        'name':
        '<unnamed>',
        'comment':
        '',
        'parentEntId':
        0,
        'pos':
        Point3(-57.916499999999999, 36.490200000000002, 0.050000000000000003),
        'hpr':
        Vec3(296.565, 0, 0),
        'scale':
        Vec3(1, 1, 1),
        'cellId':
        0,
        'gridGame':
        'Random',
        'gridScaleX':
        40.0,
        'gridScaleY':
        40.0,
        'laserFactor':
        3,
        'modelPath':
        0,
        'projector':
        Point3(21, 21, 25),
        'switchId':
        100002
    },
    100001: {
        'type':
        'laserField',
        'name':
        'copy of <unnamed>',
        'comment':
        '',
        'parentEntId':
        0,
        'pos':
        Point3(-40.057099999999998, -3.3842400000000001, 0.070000000000000007),
        'hpr':
        Vec3(243.435, 0, 0),
        'scale':
        Vec3(1, 1, 1),
        'cellId':
        1,
        'gridGame':
        'Random',
        'gridScaleX':
        37.0,
        'gridScaleY':
        38.0,
        'laserFactor':
        3,
        'modelPath':
        0,
        'projector':
        Point3(21, 21, 25),
        'switchId':
        100003
    },
    100008: {
        'type':
        'model',
        'name':
        'testMoverModel',
        'comment':
        '',
        'parentEntId':
        0,
        'pos':
        Point3(0, 0, 0),
        'hpr':
        Vec3(0, 0, 0),
        'scale':
        Point3(0.59999999999999998, 0.59999999999999998, 0.59999999999999998),
        'collisionsOnly':
        0,
        'flattenType':
        'light',
        'loadType':
        'loadModelCopy',
        'modelPath':
        'phase_11/models/lawbotHQ/LB_paper_big_stacks2'
    },
    100011: {
        'type':
        'model',
        'name':
        'copy of <unnamed>',
        'comment':
        '',
        'parentEntId':
        0,
        'pos':
        Point3(-66.403099999999995, -28.3337, 0),
        'hpr':
        Vec3(330.94499999999999, 0, 0),
        'scale':
        Point3(0.59999999999999998, 0.59999999999999998, 0.59999999999999998),
        'collisionsOnly':
        0,
        'flattenType':
        'light',
        'loadType':
        'loadModelCopy',
        'modelPath':
        'phase_11/models/lawbotHQ/LB_paper_stacks'
    },
    100012: {
        'type':
        'model',
        'name':
        'copy of <unnamed> (2)',
        'comment':
        '',
        'parentEntId':
        0,
        'pos':
        Point3(-61.3414, 28.383900000000001, 0),
        'hpr':
        Vec3(330.94499999999999, 0, 0),
        'scale':
        Point3(0.59999999999999998, 0.59999999999999998, 0.59999999999999998),
        'collisionsOnly':
        0,
        'flattenType':
        'light',
        'loadType':
        'loadModelCopy',
        'modelPath':
        'phase_11/models/lawbotHQ/LB_paper_stacks'
    },
    100013: {
        'type':
        'model',
        'name':
        'copy of <unnamed> (3)',
        'comment':
        '',
        'parentEntId':
        0,
        'pos':
        Point3(-73.001900000000006, 23.1112, 0),
        'hpr':
        Vec3(311.42399999999998, 0, 0),
        'scale':
        Point3(0.59999999999999998, 0.59999999999999998, 0.59999999999999998),
        'collisionsOnly':
        0,
        'flattenType':
        'light',
        'loadType':
        'loadModelCopy',
        'modelPath':
        'phase_11/models/lawbotHQ/LB_paper_stacks'
    },
    100014: {
        'type':
        'model',
        'name':
        'critbox4',
        'comment':
        '',
        'parentEntId':
        0,
        'pos':
        Point3(-10.5395, 55.5366, 0),
        'hpr':
        Vec3(26.565100000000001, 0, 0),
        'scale':
        Point3(0.59999999999999998, 0.59999999999999998, 0.80000000000000004),
        'collisionsOnly':
        0,
        'flattenType':
        'light',
        'loadType':
        'loadModelCopy',
        'modelPath':
        'phase_11/models/lawbotHQ/LB_paper_big_stacks3'
    },
    100015: {
        'type':
        'model',
        'name':
        'critbox3',
        'comment':
        '',
        'parentEntId':
        0,
        'pos':
        Point3(-2.5155599999999998, -64.218900000000005, 0),
        'hpr':
        Vec3(333.435, 0, 0),
        'scale':
        Point3(0.59999999999999998, 0.59999999999999998, 0.80000000000000004),
        'collisionsOnly':
        0,
        'flattenType':
        'light',
        'loadType':
        'loadModelCopy',
        'modelPath':
        'phase_11/models/lawbotHQ/LB_paper_big_stacks3'
    },
    100016: {
        'type':
        'model',
        'name':
        'critbox2',
        'comment':
        '',
        'parentEntId':
        0,
        'pos':
        Point3(-0.55908400000000003, -27.465, 0.050000000000000003),
        'hpr':
        Vec3(333.435, 0, 0),
        'scale':
        Point3(0.59999999999999998, 0.59999999999999998, 0.80000000000000004),
        'collisionsOnly':
        0,
        'flattenType':
        'light',
        'loadType':
        'loadModelCopy',
        'modelPath':
        'phase_11/models/lawbotHQ/LB_paper_big_stacks2'
    },
    100019: {
        'type':
        'model',
        'name':
        'copy of crit box',
        'comment':
        '',
        'parentEntId':
        0,
        'pos':
        Point3(3.82422, 21.9664, 0),
        'hpr':
        Vec3(60.945399999999999, 0, 0),
        'scale':
        Point3(0.55000000000000004, 0.55000000000000004, 0.90000000000000002),
        'collisionsOnly':
        0,
        'flattenType':
        'light',
        'loadType':
        'loadModelCopy',
        'modelPath':
        'phase_11/models/lawbotHQ/LB_paper_big_stacks3'
    },
    100021: {
        'type':
        'model',
        'name':
        '<unnamed>',
        'comment':
        '',
        'parentEntId':
        100017,
        'pos':
        Point3(0, 0, 0),
        'hpr':
        Vec3(0, 0, 0),
        'scale':
        Point3(0.80000000000000004, 0.80000000000000004, 0.80000000000000004),
        'collisionsOnly':
        0,
        'flattenType':
        'light',
        'loadType':
        'loadModelCopy',
        'modelPath':
        'phase_11/models/lawbotHQ/LB_paper_big_stacks2'
    },
    100022: {
        'type':
        'model',
        'name':
        'copy of <unnamed>',
        'comment':
        '',
        'parentEntId':
        100017,
        'pos':
        Point3(-1.7202200000000001, 8.9438300000000002, 0),
        'hpr':
        Vec3(0, 0, 0),
        'scale':
        Point3(0.80000000000000004, 0.80000000000000004, 0.80000000000000004),
        'collisionsOnly':
        0,
        'flattenType':
        'light',
        'loadType':
        'loadModelCopy',
        'modelPath':
        'phase_11/models/lawbotHQ/LB_paper_big_stacks2'
    },
    100023: {
        'type':
        'model',
        'name':
        'copy of <unnamed> (2)',
        'comment':
        '',
        'parentEntId':
        100017,
        'pos':
        Point3(-1.27251, -8.8425600000000006, 0),
        'hpr':
        Vec3(0, 0, 0),
        'scale':
        Point3(0.80000000000000004, 0.80000000000000004, 0.80000000000000004),
        'collisionsOnly':
        0,
        'flattenType':
        'light',
        'loadType':
        'loadModelCopy',
        'modelPath':
        'phase_11/models/lawbotHQ/LB_paper_big_stacks2'
    },
    100026: {
        'type':
        'model',
        'name':
        'crit box',
        'comment':
        '',
        'parentEntId':
        0,
        'pos':
        Point3(1.3729, 25.043399999999998, 0),
        'hpr':
        Vec3(26.565100000000001, 0, 0),
        'scale':
        Point3(0.59999999999999998, 0.59999999999999998, 0.80000000000000004),
        'collisionsOnly':
        0,
        'flattenType':
        'light',
        'loadType':
        'loadModelCopy',
        'modelPath':
        'phase_11/models/lawbotHQ/LB_paper_big_stacks3'
    },
    100028: {
        'type':
        'model',
        'name':
        'copy of <unnamed> (3)',
        'comment':
        '',
        'parentEntId':
        100027,
        'pos':
        Point3(-0.75804899999999997, -10.1966, 0),
        'hpr':
        Vec3(0, 0, 0),
        'scale':
        Point3(0.59999999999999998, 0.59999999999999998, 0.80000000000000004),
        'collisionsOnly':
        0,
        'flattenType':
        'light',
        'loadType':
        'loadModelCopy',
        'modelPath':
        'phase_11/models/lawbotHQ/LB_paper_big_stacks3'
    },
    100029: {
        'type':
        'model',
        'name':
        'copy of <unnamed> (4)',
        'comment':
        '',
        'parentEntId':
        100027,
        'pos':
        Point3(1.8243799999999999, -2.94686, 0),
        'hpr':
        Vec3(0, 0, 0),
        'scale':
        Point3(0.59999999999999998, 0.59999999999999998, 0.80000000000000004),
        'collisionsOnly':
        0,
        'flattenType':
        'light',
        'loadType':
        'loadModelCopy',
        'modelPath':
        'phase_11/models/lawbotHQ/LB_paper_big_stacks3'
    },
    100030: {
        'type':
        'model',
        'name':
        'copy of <unnamed> (5)',
        'comment':
        '',
        'parentEntId':
        100027,
        'pos':
        Point3(0.16411300000000001, 4.4424400000000004, 0),
        'hpr':
        Vec3(0, 0, 0),
        'scale':
        Point3(0.59999999999999998, 0.59999999999999998, 0.80000000000000004),
        'collisionsOnly':
        0,
        'flattenType':
        'light',
        'loadType':
        'loadModelCopy',
        'modelPath':
        'phase_11/models/lawbotHQ/LB_paper_big_stacks3'
    },
    100031: {
        'type':
        'model',
        'name':
        'copy of <unnamed> (6)',
        'comment':
        '',
        'parentEntId':
        100027,
        'pos':
        Point3(5.1321700000000003, 10.0594, 0),
        'hpr':
        Vec3(0, 0, 0),
        'scale':
        Point3(0.59999999999999998, 0.59999999999999998, 0.80000000000000004),
        'collisionsOnly':
        0,
        'flattenType':
        'light',
        'loadType':
        'loadModelCopy',
        'modelPath':
        'phase_11/models/lawbotHQ/LB_paper_big_stacks3'
    },
    100035: {
        'type':
        'model',
        'name':
        'copy of crit box (2)',
        'comment':
        '',
        'parentEntId':
        0,
        'pos':
        Point3(3.0172099999999999, -23.374099999999999, 0),
        'hpr':
        Vec3(13.240500000000001, 0, 0),
        'scale':
        Point3(0.55000000000000004, 0.55000000000000004, 0.90000000000000002),
        'collisionsOnly':
        0,
        'flattenType':
        'light',
        'loadType':
        'loadModelCopy',
        'modelPath':
        'phase_11/models/lawbotHQ/LB_paper_big_stacks3'
    },
    100036: {
        'type':
        'model',
        'name':
        'copy of crit box (2)',
        'comment':
        '',
        'parentEntId':
        0,
        'pos':
        Point3(-8.5892300000000006, 61.954799999999999, 0),
        'hpr':
        Vec3(26.565100000000001, 0, 0),
        'scale':
        Point3(0.55000000000000004, 0.55000000000000004, 0.90000000000000002),
        'collisionsOnly':
        0,
        'flattenType':
        'light',
        'loadType':
        'loadModelCopy',
        'modelPath':
        'phase_11/models/lawbotHQ/LB_paper_big_stacks3'
    },
    100018: {
        'type': 'mover',
        'name': 'testMover',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(-64.381699999999995, 0, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'cycleType': 'return',
        'entity2Move': 100008,
        'modelPath': 0,
        'moveTarget': 100034,
        'pos0Move': 2,
        'pos0Wait': 2,
        'pos1Move': 2,
        'pos1Wait': 2,
        'startOn': 0,
        'switchId': 0
    },
    100024: {
        'type': 'mover',
        'name': 'paperwall2mover',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0, -46.395699999999998, 0),
        'hpr': Vec3(333.435, 0, 0),
        'scale': Vec3(1, 1, 1),
        'cycleType': 'oneWay',
        'entity2Move': 100017,
        'modelPath': 0,
        'moveTarget': 100025,
        'pos0Move': 2,
        'pos0Wait': 2,
        'pos1Move': 2,
        'pos1Wait': 2,
        'startOn': 0,
        'switchId': 100001
    },
    100032: {
        'type': 'mover',
        'name': 'paperwall1mover',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(-1.54332, 42.015700000000002, 0),
        'hpr': Vec3(26.565100000000001, 0, 0),
        'scale': Vec3(1, 1, 1),
        'cycleType': 'oneWay',
        'entity2Move': 100027,
        'modelPath': 0,
        'moveTarget': 100033,
        'pos0Move': 2,
        'pos0Wait': 2,
        'pos1Move': 2,
        'pos1Wait': 2,
        'startOn': 0,
        'switchId': 100000
    },
    100004: {
        'type': 'nodepath',
        'name': 'BattlePos1',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(-31.968900000000001, 28.7456, 0),
        'hpr': Vec3(22.619900000000001, 0, 0),
        'scale': Vec3(1, 1, 1)
    },
    100005: {
        'type': 'nodepath',
        'name': 'BattlePos2',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(-31.085799999999999, -34.983499999999999, 0),
        'hpr': Vec3(331.38999999999999, 0, 0),
        'scale': Vec3(1, 1, 1)
    },
    100007: {
        'type': 'nodepath',
        'name': 'copy of Cog Parent1',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(-11.0871, 37.400100000000002, 0),
        'hpr': Vec3(299.24900000000002, 0, 0),
        'scale': Vec3(1, 1, 1)
    },
    100009: {
        'type': 'nodepath',
        'name': 'Cog Parent1',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(-10.224600000000001, -41.594299999999997, 0),
        'hpr': Vec3(246.214, 0, 0),
        'scale': Vec3(1, 1, 1)
    },
    100010: {
        'type': 'nodepath',
        'name': 'doorparent',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(133.90000000000001, -1.81291, 0),
        'hpr': Vec3(265.74000000000001, 0, 0),
        'scale': Point3(1, 1, 1)
    },
    100017: {
        'type': 'nodepath',
        'name': 'PaperDoor2',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0, 0, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1)
    },
    100020: {
        'type': 'nodepath',
        'name': 'movertarget',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(-84.027299999999997, -14.7227, 0),
        'hpr': Vec3(270, 0, 0),
        'scale': Vec3(1, 1, 1)
    },
    100025: {
        'type': 'nodepath',
        'name': 'papperwall2target',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(14.299799999999999, -46.091099999999997, 0),
        'hpr': Vec3(336.03800000000001, 0, 0),
        'scale': Vec3(1, 1, 1)
    },
    100027: {
        'type': 'nodepath',
        'name': 'PaperWall1',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0, 0, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1)
    },
    100033: {
        'type': 'nodepath',
        'name': 'paperwall1movertarget',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(13.6684, 42.7864, 0),
        'hpr': Vec3(41.185899999999997, 0, 0),
        'scale': Vec3(1, 1, 1)
    },
    100034: {
        'type': 'nodepath',
        'name': 'test mover target',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(-51.154899999999998, 0, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1)
    }
}
Scenario0 = {}
levelSpec = {'globalEntities': GlobalEntities, 'scenarios': [Scenario0]}
