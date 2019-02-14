from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
GAME_TIME = 60
MAX_SCORE = 23
MIN_SCORE = 5
NUMSTARS = 5
ONSCREENASSIGNMENTS = 5
PHOTO_ROTATION_MIN = -20
PHOTO_ROTATION_MAX = 20
PHOTO_ROTATION_VEL = 25.0
PHOTO_ANGLE_MIN = -15
PHOTO_ANGLE_MAX = 10
PHOTO_ANGLE_VEL = 25.0


def calcScore(t):
    range = MAX_SCORE - MIN_SCORE
    score = MAX_SCORE - range * (float(t) / GAME_TIME)
    return int(score + 0.5)


AREA_DATA = {}
AREA_DATA[ToontownGlobals.ToontownCentral] = {}
AREA_DATA[ToontownGlobals.ToontownCentral]['FILMCOUNT'] = 32
AREA_DATA[ToontownGlobals.ToontownCentral]['TIME'] = 120
AREA_DATA[ToontownGlobals.ToontownCentral]['CAMERA_INTIAL_POSTION'] = Point3(
    0, 50, 20)
AREA_DATA[ToontownGlobals.ToontownCentral]['DNA_TRIO'] = (
    'phase_4/dna/storage_TT_sz.dna', 'phase_4/dna/storage_TT.dna',
    'phase_4/dna/toontown_central_sz.dna')
AREA_DATA[ToontownGlobals.ToontownCentral]['TRIPOD_OFFSET'] = Point3(0, 0, 7.0)
AREA_DATA[ToontownGlobals.ToontownCentral]['START_HPR'] = Point3(
    -87.875200000000007, -0.37854900000000002, 0)
AREA_DATA[ToontownGlobals.ToontownCentral]['PATHS'] = ([
    Point3(10, 20, 4.0250000000000004),
    Point3(10, -3, 4.0250000000000004),
    Point3(32, -5, 4.0250000000000004),
    Point3(32, 12, 4.0250000000000004)
], [
    Point3(-58.396000000000001, -51.972000000000001, -1.3859999999999999),
    Point3(-59.966999999999999, -66.906000000000006, 0.025000000000000001),
    Point3(-56.415999999999997, -77.650999999999996, 0.025000000000000001),
    Point3(-26.619, -74.156000000000006, 0.025000000000000001),
    Point3(-10.664, -73.819999999999993, 0.025000000000000001),
    Point3(5.4210000000000003, -81.281999999999996, 2.5249999999999999),
    Point3(5.4210000000000003, -57.383000000000003, 0.025000000000000001),
    Point3(-27.497, -34.524999999999999, 0.025000000000000001),
    Point3(-41.783999999999999, -48.023000000000003, 0.025000000000000001)
], [
    Point3(-29.015000000000001, 36.497999999999998, 0.028000000000000001),
    Point3(-45.701000000000001, 42.963000000000001, -0.90400000000000003),
    Point3(-54.658999999999999, 65.986999999999995, 0.025000000000000001),
    Point3(-45.457999999999998, 81.477999999999994, 0.025000000000000001),
    Point3(-17.324999999999999, 83.590999999999994, 0.52500000000000002),
    Point3(4.1689999999999996, 69.941999999999993, 1.133),
    Point3(-10.625, 38.356999999999999, 0.035999999999999997)
], [
    Point3(-84.760999999999996, -74.519999999999996, 0.034000000000000002),
    Point3(-101.685, -75.619, 0.52500000000000002),
    Point3(-113.60599999999999, -71.805999999999997, 0.52500000000000002),
    Point3(-111.46299999999999, -63.671999999999997, 0.52500000000000002),
    Point3(-102.072, -60.866999999999997, 0.52500000000000002),
    Point3(-94.049000000000007, -60.518999999999998, 0.035000000000000003),
    Point3(-66.867999999999995, -64.715000000000003, 0.025000000000000001)
])
AREA_DATA[ToontownGlobals.ToontownCentral]['PATHANIMREL'] = (0, 0, 1, 2)
AREA_DATA[ToontownGlobals.ToontownCentral]['ANIMATIONS'] = ([
    ('wave', 2.0), (None, 1.0), (None, 1.0)
], [('slip-forward', 2.0), (None, 1.0), (None, 1.0)], [('shrug', 2.0),
                                                       (None, 1.0)])
AREA_DATA[ToontownGlobals.ToontownCentral]['MOVEMODES'] = ([
    ('walk', 1.0), ('run', 0.40000000000000002)
], [('run', 0.40000000000000002)], [('walk', 1.0), ('sad-walk', 2.5)])
AREA_DATA[ToontownGlobals.DonaldsDock] = {}
AREA_DATA[ToontownGlobals.DonaldsDock]['FILMCOUNT'] = 28
AREA_DATA[ToontownGlobals.DonaldsDock]['TIME'] = 110
AREA_DATA[ToontownGlobals.DonaldsDock]['CAMERA_INTIAL_POSTION'] = Point3(
    0, 50, 20)
AREA_DATA[ToontownGlobals.DonaldsDock]['DNA_TRIO'] = (
    'phase_6/dna/storage_DD_sz.dna', 'phase_6/dna/storage_DD.dna',
    'phase_6/dna/donalds_dock_sz.dna')
AREA_DATA[ToontownGlobals.DonaldsDock]['TRIPOD_OFFSET'] = Point3(0, -4.0, 9.0)
AREA_DATA[ToontownGlobals.DonaldsDock]['START_HPR'] = Point3(
    218.21100000000001, -6.7878999999999996, 0)
AREA_DATA[ToontownGlobals.DonaldsDock]['PATHS'] = ([
    Point3(-115.59999999999999, 39.399999999999999, 5.6920000000000002),
    Point3(-109.90000000000001, -14, 5.6920000000000002),
    Point3(-112.652, -46.700000000000003, 5.6920000000000002),
    Point3(-68.900000000000006, -74.700000000000003, 5.6920000000000002),
    Point3(-0.20000000000000001, -82.0, 5.6920000000000002),
    Point3(-73.5, -72.200000000000003, 5.6920000000000002),
    Point3(-112.0, -45, 5.6920000000000002),
    Point3(-110.3, 17.5, 5.6920000000000002)
], [
    Point3(-67.143000000000001, 131.11699999999999, 3.2799999999999998),
    Point3(-56.399999999999999, 101.40000000000001, 3.2789999999999999),
    Point3(-51.424999999999997, 80.099999999999994, 3.2789999999999999),
    Point3(-87.632000000000005, 56.718000000000004, 2.3919999999999999),
    Point3(-114.09999999999999, 54.700000000000003, 3.2799999999999998),
    Point3(-108.5, 80.5, 3.2810000000000001),
    Point3(-82.671999999999997, 68.971000000000004, 3.2799999999999998),
    Point3(-83.122, 101.90000000000001, 3.2799999999999998)
], [
    Point3(11.456, -82.521000000000001, 3.2799999999999998),
    Point3(49.734999999999999, -70.459999999999994, 3.2799999999999998),
    Point3(60.665999999999997, -42.734999999999999, 3.2799999999999998),
    Point3(40.810000000000002, -76.632999999999996, 3.2799999999999998)
], [
    Point3(68.924000000000007, -33.680999999999997, 5.6920000000000002),
    Point3(60.509999999999998, -31.574000000000002, 5.6920000000000002),
    Point3(58.671999999999997, 12.253, 5.6920000000000002),
    Point3(69.808999999999997, 48.261000000000003, 5.6920000000000002),
    Point3(57.856999999999999, 46.134, 5.6920000000000002),
    Point3(66.057000000000002, -22.475999999999999, 5.6920000000000002)
], [
    Point3(-24.439, 37.429000000000002, 0.20000000000000001),
    Point3(-3.5489999999999999, 19.343, 0.20000000000000001),
    Point3(3.218, -1.4750000000000001, 0.20000000000000001),
    Point3(-12.292, -25.318000000000001, 0.20000000000000001),
    Point3(-42.954000000000001, -25.706, 0.20000000000000001),
    Point3(-55.101999999999997, 4.0410000000000004, 0.20000000000000001),
    Point3(-54.247, 16.050999999999998, 0.20000000000000001)
])
AREA_DATA[ToontownGlobals.DonaldsDock]['PATHANIMREL'] = (0, 0, 1, 2, 3)
AREA_DATA[ToontownGlobals.DonaldsDock]['ANIMATIONS'] = ([('wave', 2.0),
                                                         (None, 1.0)],
                                                        [('slip-forward', 2.0),
                                                         (None, 1.0),
                                                         (None, 1.0)],
                                                        [('shrug', 2.0),
                                                         (None, 1.0)], [(None,
                                                                         1.0)])
AREA_DATA[ToontownGlobals.DonaldsDock]['MOVEMODES'] = ([('walk', 1.0)], [
    ('run', 0.40000000000000002)
], [('walk', 1.0), ('sad-walk', 2.5)], [('swim', 1.0)])
AREA_DATA[ToontownGlobals.DaisyGardens] = {}
AREA_DATA[ToontownGlobals.DaisyGardens]['FILMCOUNT'] = 26
AREA_DATA[ToontownGlobals.DaisyGardens]['TIME'] = 100
AREA_DATA[ToontownGlobals.DaisyGardens]['CAMERA_INTIAL_POSTION'] = Point3(
    0, 50, 20)
AREA_DATA[ToontownGlobals.DaisyGardens]['DNA_TRIO'] = (
    'phase_8/dna/storage_DG_sz.dna', 'phase_8/dna/storage_DG.dna',
    'phase_8/dna/daisys_garden_sz.dna')
AREA_DATA[ToontownGlobals.DaisyGardens]['TRIPOD_OFFSET'] = Point3(0, 0, 6.0)
AREA_DATA[ToontownGlobals.DaisyGardens]['START_HPR'] = Point3(0.0, 0.0, 0.0)
AREA_DATA[ToontownGlobals.DaisyGardens]['PATHS'] = ([
    Point3(-37.252000000000002, 25.513000000000002, 0.025000000000000001),
    Point3(-30.032, 37.899999999999999, 0.025000000000000001),
    Point3(-38.694000000000003, 50.631, 0.025000000000000001),
    Point3(-52.100000000000001, 52.926000000000002, 0.025000000000000001),
    Point3(-62.807000000000002, 43.957000000000001, 0.025000000000000001)
], [
    Point3(36.213999999999999, 117.447, 5.0),
    Point3(3.5339999999999998, 137.083, 5.0),
    Point3(-9.3840000000000003, 136.97300000000001, 5.0),
    Point3(-26.376999999999999, 120.56399999999999, 5.0),
    Point3(-43.268000000000001, 122.33499999999999, 5.0),
    Point3(-26.376999999999999, 120.56399999999999, 5.0),
    Point3(-9.3840000000000003, 136.97300000000001, 5.0),
    Point3(3.5339999999999998, 137.083, 5.0)
], [
    Point3(15.675000000000001, 111.20999999999999, 0.025000000000000001),
    Point3(21.260999999999999, 119.429, 0.025000000000000001),
    Point3(6.2009999999999996, 129.047, 0.025000000000000001),
    Point3(-10.984, 124.684, 0.025000000000000001),
    Point3(4.0389999999999997, 130.27500000000001, 0.025000000000000001),
    Point3(22.645, 118.20399999999999, 0.025000000000000001)
], [
    Point3(27.347999999999999, 16.835999999999999, 0.025000000000000001),
    Point3(47.152000000000001, 18.038, 0.025000000000000001),
    Point3(65.325000000000003, 22.321999999999999, 0.025000000000000001),
    Point3(73.063000000000002, 43.545000000000002, 0.025000000000000001),
    Point3(75.227999999999994, 66.869, 0.025000000000000001),
    Point3(69.468000000000004, 23.797999999999998, 0.025000000000000001),
    Point3(46.43, 20.472999999999999, 0.025000000000000001)
])
AREA_DATA[ToontownGlobals.DaisyGardens]['PATHANIMREL'] = (0, 0, 1, 2)
AREA_DATA[ToontownGlobals.DaisyGardens]['ANIMATIONS'] = ([('wave', 2.0),
                                                          (None, 1.0)],
                                                         [('jump', 2.0),
                                                          (None, 1.0),
                                                          (None, 1.0)],
                                                         [('bow', 2.0),
                                                          ('happy-dance', 2.0),
                                                          (None, 1.0)])
AREA_DATA[ToontownGlobals.DaisyGardens]['MOVEMODES'] = ([
    ('walk', 1.0), ('run', 0.40000000000000002)
], [('run', 0.40000000000000002)], [('walk', 1.0), ('run',
                                                    0.40000000000000002)])
AREA_DATA[ToontownGlobals.MinniesMelodyland] = {}
AREA_DATA[ToontownGlobals.MinniesMelodyland]['FILMCOUNT'] = 23
AREA_DATA[ToontownGlobals.MinniesMelodyland]['TIME'] = 95
AREA_DATA[ToontownGlobals.MinniesMelodyland]['CAMERA_INTIAL_POSTION'] = Point3(
    0, -50, 20)
AREA_DATA[ToontownGlobals.MinniesMelodyland]['DNA_TRIO'] = (
    'phase_6/dna/storage_MM_sz.dna', 'phase_6/dna/storage_MM.dna',
    'phase_6/dna/minnies_melody_land_sz.dna')
AREA_DATA[ToontownGlobals.MinniesMelodyland]['TRIPOD_OFFSET'] = Point3(
    0, 0, 6.0)
AREA_DATA[ToontownGlobals.MinniesMelodyland]['START_HPR'] = Point3(
    71.302800000000005, -3.1293199999999999, 0)
AREA_DATA[ToontownGlobals.MinniesMelodyland]['PATHS'] = ([
    Point3(-42.350000000000001, -16.0, -12.476000000000001),
    Point3(-23.699999999999999, -49.0, -12.476000000000001),
    Point3(12.4, -62.100000000000001, -12.476000000000001),
    Point3(37.799999999999997, -31.163, -12.476000000000001),
    Point3(29.5, 8.9000000000000004, -12.476000000000001),
    Point3(-11.1, 19.600000000000001, -12.476000000000001),
    Point3(-34.399999999999999, -3.3999999999999999, -12.476000000000001)
], [
    Point3(133.976, -67.686000000000007, -6.6180000000000003),
    Point3(126.749, -47.350999999999999, 0.40400000000000003),
    Point3(130.49299999999999, -33.429000000000002, 4.5339999999999998),
    Point3(126.239, -15.853, 5.25),
    Point3(129.774, -0.53500000000000003, 3.1139999999999999),
    Point3(130.83000000000001, 25.079999999999998, -5.6879999999999997),
    Point3(128.077, -5.3300000000000001, 4.2910000000000004),
    Point3(128.399, -23.141999999999999, 5.4569999999999999),
    Point3(129.239, -39.886000000000003, 2.9140000000000001),
    Point3(133.06299999999999, -78.314999999999998, -10.756)
], [
    Point3(50.756999999999998, -102.705, 6.7249999999999996),
    Point3(-23.276, -108.54600000000001, 6.7249999999999996),
    Point3(-57.283000000000001, -72.081000000000003, 6.7249999999999996),
    Point3(-21.699000000000002, -109.80800000000001, 6.7249999999999996),
    Point3(19.614000000000001, -108.59099999999999, 6.7249999999999996)
], [
    Point3(51.761000000000003, -36.128999999999998, -14.627000000000001),
    Point3(26.373999999999999, -73.664000000000001, -14.645),
    Point3(14.321999999999999, -89.378, -14.561999999999999),
    Point3(61.594000000000001, -91.930999999999997, -14.523999999999999)
])
AREA_DATA[ToontownGlobals.MinniesMelodyland]['PATHANIMREL'] = (0, 0, 1, 2)
AREA_DATA[ToontownGlobals.MinniesMelodyland]['ANIMATIONS'] = ([('wave', 2.0),
                                                               (None, 1.0)],
                                                              [('jump', 2.0),
                                                               ('slip-forward',
                                                                2.0),
                                                               (None, 1.0),
                                                               (None, 1.0)],
                                                              [('shrug', 2.0),
                                                               ('confused',
                                                                2.0),
                                                               (None, 1.0)])
AREA_DATA[ToontownGlobals.MinniesMelodyland]['MOVEMODES'] = ([
    ('walk', 1.0), ('run', 0.40000000000000002)
], [('run', 0.40000000000000002)], [('walk', 1.0), ('sad-walk', 2.5)])
AREA_DATA[ToontownGlobals.TheBrrrgh] = {}
AREA_DATA[ToontownGlobals.TheBrrrgh]['FILMCOUNT'] = 21
AREA_DATA[ToontownGlobals.TheBrrrgh]['TIME'] = 90
AREA_DATA[ToontownGlobals.TheBrrrgh]['CAMERA_INTIAL_POSTION'] = Point3(
    0, 50, 20)
AREA_DATA[ToontownGlobals.TheBrrrgh]['DNA_TRIO'] = (
    'phase_8/dna/storage_BR_sz.dna', 'phase_8/dna/storage_BR.dna',
    'phase_8/dna/the_burrrgh_sz.dna')
AREA_DATA[ToontownGlobals.TheBrrrgh]['TRIPOD_OFFSET'] = Point3(0, 0, 6.0)
AREA_DATA[ToontownGlobals.TheBrrrgh]['START_HPR'] = Point3(
    -49.401000000000003, -11.6266, 0)
AREA_DATA[ToontownGlobals.TheBrrrgh]['PATHS'] = ([
    Point3(-82.519999999999996, -28.727, 3.0089999999999999),
    Point3(-77.641999999999996, -4.6159999999999997, 3.0089999999999999),
    Point3(-51.006, 1.05, 3.0089999999999999),
    Point3(-28.617999999999999, -28.449000000000002, 4.0259999999999998),
    Point3(-37.948, -64.704999999999998, 4.7140000000000004)
], [
    Point3(-74.671999999999997, 62.149999999999999, 6.1920000000000002),
    Point3(-92.602000000000004, 38.734000000000002, 6.1920000000000002),
    Point3(-126.887, 34.756999999999998, 6.1920000000000002),
    Point3(-138.12, 56.002000000000002, 6.1920000000000002),
    Point3(-113.968, 32.661000000000001, 6.1920000000000002),
    Point3(-84.716999999999999, 46.837000000000003, 6.1920000000000002)
], [
    Point3(-55.238999999999997, -126.92100000000001, 6.1920000000000002),
    Point3(-20.350000000000001, -108.696, 6.1920000000000002),
    Point3(5.0279999999999996, -61.737000000000002, 6.1920000000000002),
    Point3(27.966999999999999, -19.683, 6.1920000000000002),
    Point3(11.487, 2.9129999999999998, 6.1920000000000002),
    Point3(-23.727, -47.344000000000001, 6.1920000000000002)
], [
    Point3(-143.22, -104.727, 6.1920000000000002),
    Point3(-152.989, -64.372, 6.1920000000000002),
    Point3(-139.328, -6.6280000000000001, 4.0179999999999998),
    Point3(-135.815, -39.935000000000002, 3.0089999999999999)
])
AREA_DATA[ToontownGlobals.TheBrrrgh]['PATHANIMREL'] = (0, 0, 1, 2)
AREA_DATA[ToontownGlobals.TheBrrrgh]['ANIMATIONS'] = ([('wave', 2.0),
                                                       (None, 1.0)],
                                                      [('applause', 2.0),
                                                       ('slip-forward', 2.0),
                                                       (None, 1.0), (None,
                                                                     1.0)],
                                                      [('shrug', 2.0),
                                                       ('confused', 2.0),
                                                       ('angry', 2.0),
                                                       (None, 1.0)])
AREA_DATA[ToontownGlobals.TheBrrrgh]['MOVEMODES'] = ([
    ('walk', 1.0), ('running-jump', 0.40000000000000002)
], [('run', 0.40000000000000002)], [('walk', 1.0), ('sad-walk', 2.5)])
AREA_DATA[ToontownGlobals.DonaldsDreamland] = {}
AREA_DATA[ToontownGlobals.DonaldsDreamland]['FILMCOUNT'] = 18
AREA_DATA[ToontownGlobals.DonaldsDreamland]['TIME'] = 85
AREA_DATA[ToontownGlobals.DonaldsDreamland]['CAMERA_INTIAL_POSTION'] = Point3(
    0, 50, 20)
AREA_DATA[ToontownGlobals.DonaldsDreamland]['DNA_TRIO'] = (
    'phase_8/dna/storage_DL_sz.dna', 'phase_8/dna/storage_DL.dna',
    'phase_8/dna/donalds_dreamland_sz.dna')
AREA_DATA[ToontownGlobals.DonaldsDreamland]['TRIPOD_OFFSET'] = Point3(
    0, 0, 6.0)
AREA_DATA[ToontownGlobals.DonaldsDreamland]['START_HPR'] = Point3(
    -137.18299999999999, -9.06236, 0)
AREA_DATA[ToontownGlobals.DonaldsDreamland]['PATHS'] = ([
    Point3(-51.222000000000001, 90.873999999999995, 0.025000000000000001),
    Point3(0.71499999999999997, 94.789000000000001, 0.025000000000000001),
    Point3(30.715, 94.0, 0.025000000000000001),
    Point3(69.180999999999997, 93.450000000000003, 0.025000000000000001),
    Point3(30.715, 94.0, 0.025000000000000001),
    Point3(-8.6959999999999997, 91.799000000000007, 0.025000000000000001)
], [
    Point3(-70.403000000000006, 29.574999999999999, 2.125),
    Point3(-68.828999999999994, -21.076000000000001, 2.125),
    Point3(-104.669, -24.757999999999999, 2.125),
    Point3(-114.801, 21.777000000000001, 2.125)
], [
    Point3(15.923, -41.823999999999998, -16.088999999999999),
    Point3(18.216999999999999, 34.322000000000003, -14.731999999999999),
    Point3(7.0869999999999997, 61.963999999999999, -16.058),
    Point3(50.447000000000003, 8.1699999999999999, -13.975),
    Point3(-15.792999999999999, -19.916, -14.041),
    Point3(-26.41, 26.786000000000001, -14.371),
    Point3(20.853000000000002, 1.639, -13.975)
], [
    Point3(-35.390999999999998, -24.111999999999998, -14.241),
    Point3(-54.363999999999997, -12.996, -13.975),
    Point3(-51.578000000000003, 21.963999999999999, -14.138999999999999),
    Point3(-10.49, 15.537000000000001, -13.974),
    Point3(-25.728000000000002, -14.664999999999999, -13.975),
    Point3(-43.923000000000002, -32.323999999999998, -14.634)
])
AREA_DATA[ToontownGlobals.DonaldsDreamland]['PATHANIMREL'] = (0, 0, 1, 2)
AREA_DATA[ToontownGlobals.DonaldsDreamland]['ANIMATIONS'] = ([
    ('wave', 2.0), (None, 1.0)
], [('applause', 2.0), ('jump', 2.0), ('slip-forward', 2.0), (None, 1.0),
    (None, 1.0)], [('shrug', 2.0), ('angry', 2.0), (None, 1.0)])
AREA_DATA[ToontownGlobals.DonaldsDreamland]['MOVEMODES'] = ([
    ('walk', 1.0), ('catch-run', 0.40000000000000002)
], [('run', 0.40000000000000002), ('running-jump',
                                   0.40000000000000002)], [('walk', 1.0),
                                                           ('sad-walk', 2.5)])
