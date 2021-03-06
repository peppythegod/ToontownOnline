from pandac.PandaModules import Point3
from pandac.PandaModules import Vec3
import copy
from toontown.toonbase import TTLocalizer
__mickeyPaths = {
    'a': (Point3(17, -17, 4.0250000000000004), ('b', 'e')),
    'b': (Point3(17.5, 7.5999999999999996, 4.0250000000000004), ('c', 'e')),
    'c': (Point3(85, 11.5, 4.0250000000000004), ('d', )),
    'd': (Point3(85, -13, 4.0250000000000004), ('a', )),
    'e': (Point3(-27.5, -5.25, 0.0), ('a', 'b', 'f')),
    'f': (Point3(-106.15000000000001, -4.0, -2.5), ('e', 'g', 'h', 'i')),
    'g': (Point3(-89.5, 93.5, 0.5), ('f', 'h')),
    'h': (Point3(-139.94999999999999, 1.6899999999999999, 0.5), ('f', 'g',
                                                                 'i')),
    'i': (Point3(-110.95, -68.569999999999993, 0.5), ('f', 'h'))
}
__mickeyWaypoints = (('a', 'e', 1, []), ('b', 'e', 1, []), ('e', 'f', 1, [
    Point3(-76.870000000000005, -7.8499999999999996, -1.8500000000000001),
    Point3(-80.569999999999993, -4.0, -1.8500000000000001)
]), ('f', 'g', 1, [Point3(-106.62, 28.649999999999999, -1.5)]),
                     ('g', 'h', 1, [Point3(-128.38, 60.270000000000003,
                                           0.5)]), ('h', 'f', 1, []),
                     ('h', 'i', 1, [Point3(-137.13, -42.789999999999999,
                                           0.5)]), ('i', 'f', 1, []))
__minniePaths = {
    'a': (Point3(53.334000000000003, 71.057000000000002, 6.5250000000000004),
          ('b', 'r')),
    'b': (Point3(127.756, 58.664999999999999, -11.75), ('a', 's', 'c')),
    'c': (Point3(130.32499999999999, 15.173999999999999, -2.0030000000000001),
          ('b', 'd')),
    'd': (Point3(126.173, 7.0570000000000004, 0.52200000000000002), ('c',
                                                                     'e')),
    'e': (Point3(133.84299999999999, -6.6180000000000003, 4.71), ('d', 'f',
                                                                  'g', 'h')),
    'f': (Point3(116.876, 1.119, 3.3039999999999998), 'e'),
    'g': (Point3(116.271, -41.567999999999998, 3.3039999999999998), ('e',
                                                                     'h')),
    'h': (Point3(128.983, -49.655999999999999, -0.23100000000000001),
          ('e', 'g', 'i', 'j')),
    'i': (Point3(106.024, -75.248999999999995, -4.4980000000000002), 'h'),
    'j': (Point3(135.01599999999999, -93.072000000000003, -13.375999999999999),
          ('h', 'k', 'z')),
    'k': (Point3(123.96599999999999, -100.242, -10.879), ('j', 'l')),
    'l': (Point3(52.859000000000002, -109.081, 6.5250000000000004), ('k',
                                                                     'm')),
    'm': (Point3(-32.070999999999998, -107.04900000000001, 6.5250000000000004),
          ('l', 'n')),
    'n': (Point3(-40.518999999999998, -99.685000000000002, 6.5250000000000004),
          ('m', 'o')),
    'o': (Point3(-40.244999999999997, -88.634, 6.5250000000000004), ('n',
                                                                     'p')),
    'p': (Point3(-66.299999999999997, -62.192, 6.5250000000000004), ('o',
                                                                     'q')),
    'q': (Point3(-66.212000000000003, 23.068999999999999, 6.5250000000000004),
          ('p', 'r')),
    'r': (Point3(-18.344000000000001, 69.531999999999996, 6.5250000000000004),
          ('q', 'a')),
    's': (Point3(91.356999999999999, 44.545999999999999, -13.475), ('b', 't')),
    't': (Point3(90.355000000000004, 6.2789999999999999, -13.475), ('s', 'u')),
    'u': (Point3(-13.765000000000001, 42.362000000000002, -14.553000000000001),
          ('t', 'v')),
    'v': (Point3(-52.627000000000002, 7.4279999999999999, -14.553000000000001),
          ('u', 'w')),
    'w': (Point3(-50.654000000000003, -54.878999999999998,
                 -14.553000000000001), ('v', 'x')),
    'x': (Point3(-3.7109999999999999, -81.819000000000003,
                 -14.553000000000001), ('w', 'y')),
    'y': (Point3(90.777000000000001, -49.713999999999999, -13.475), ('z',
                                                                     'x')),
    'z': (Point3(90.058999999999997, -79.426000000000002, -13.475), ('j', 'y'))
}
__minnieWaypoints = (('a', 'b', 1, []), ('k', 'l', 1, []), ('b', 'c', 1, []),
                     ('c', 'd', 1, []), ('d', 'e', 1, []), ('e', 'f', 1, []),
                     ('e', 'g', 1, []), ('e', 'h', 1, []), ('g', 'h', 1, []),
                     ('h', 'i', 1, []), ('h', 'j', 1,
                                         []), ('s', 'b', 1,
                                               []), ('t', 'u', 1,
                                                     []), ('x', 'y', 1, []))
__goofyPaths = {
    'a': (Point3(64.995000000000005, 169.66499999999999, 10.026999999999999),
          ('b', 'q')),
    'b': (Point3(48.893000000000001, 208.91200000000001, 10.026999999999999),
          ('a', 'c')),
    'c': (Point3(5.4820000000000002, 210.47900000000001, 10.029999999999999),
          ('b', 'd')),
    'd': (Point3(-34.152999999999999, 203.28399999999999, 10.029), ('c', 'e')),
    'e': (Point3(-66.656000000000006, 174.334, 10.026), ('d', 'f')),
    'f': (Point3(-55.994, 162.33000000000001, 10.026), ('e', 'g')),
    'g': (Point3(-84.554000000000002, 142.09899999999999, 0.027), ('f', 'h')),
    'h': (Point3(-92.215000000000003, 96.445999999999998, 0.027), ('g', 'i')),
    'i': (Point3(-63.167999999999999, 60.055, 0.027), ('h', 'j')),
    'j': (Point3(-37.637, 69.974000000000004, 0.027), ('i', 'k')),
    'k': (Point3(-3.0179999999999998, 26.157, 0.027), ('j', 'l', 'm')),
    'l': (Point3(-0.71099999999999997, 46.843000000000004, 0.027), 'k'),
    'm': (Point3(26.071000000000002, 46.401000000000003, 0.027), ('k', 'n')),
    'n': (Point3(30.870000000000001, 67.432000000000002, 0.027), ('m', 'o')),
    'o': (Point3(93.903000000000006, 90.685000000000002, 0.027), ('n', 'p')),
    'p': (Point3(88.129000000000005, 140.57499999999999, 0.027), ('o', 'q')),
    'q': (Point3(53.988, 158.232, 10.026999999999999), ('p', 'a'))
}
__goofyWaypoints = (('f', 'g', 1, []), ('p', 'q', 1, []))
__goofySpeedwayPaths = {
    'a': (Point3(-9.0, -19.516999999999999, -0.32300000000000001), ('b', 'k')),
    'b': (Point3(-30.047000000000001, -1.5780000000000001, -0.373), ('a',
                                                                     'c')),
    'c': (Point3(-10.367000000000001, 49.042000000000002, -0.373), ('b', 'd')),
    'd': (Point3(38.439, 44.347999999999999, -0.373), ('c', 'e')),
    'e': (Point3(25.527000000000001, -2.395, -0.373), ('d', 'f')),
    'f': (Point3(-4.0430000000000001, -59.865000000000002,
                 -0.0030000000000000001), ('e', 'g')),
    'g': (Point3(0.39000000000000001, -99.474999999999994,
                 -0.0089999999999999993), ('f', 'h')),
    'h': (Point3(21.146999999999998, -109.127, -0.012999999999999999), ('g',
                                                                        'i')),
    'i': (Point3(5.9809999999999999, -147.60599999999999,
                 -0.012999999999999999), ('h', 'j')),
    'j': (Point3(-24.898, -120.61799999999999, -0.012999999999999999), ('i',
                                                                        'k')),
    'k': (Point3(-2.71, -90.314999999999998, -0.010999999999999999), ('j',
                                                                      'a'))
}
__goofySpeedwayWaypoints = (('a', 'k', 1, []), ('k', 'a', 1, []))
__donaldPaths = {
    'a': (Point3(-94.882999999999996, -94.024000000000001,
                 0.025000000000000001), 'b'),
    'b': (Point3(-13.962, -92.233000000000004, 0.025000000000000001), ('a',
                                                                       'h')),
    'c': (Point3(68.417000000000002, -91.929000000000002,
                 0.025000000000000001), ('m', 'g')),
    'd': (Point3(68.745000000000005, 91.227000000000004, 0.025000000000000001),
          ('k', 'i')),
    'e': (Point3(4.0469999999999997, 94.260000000000005, 0.025000000000000001),
          ('i', 'j')),
    'f': (Point3(-91.271000000000001, 90.986999999999995,
                 0.025000000000000001), 'j'),
    'g': (Point3(43.823999999999998, -94.129000000000005,
                 0.025000000000000001), ('c', 'h')),
    'h': (Point3(13.904999999999999, -91.334000000000003,
                 0.025000000000000001), ('b', 'g')),
    'i': (Point3(43.061999999999998, 88.152000000000001, 0.025000000000000001),
          ('d', 'e')),
    'j': (Point3(-48.960000000000001, 88.564999999999998,
                 0.025000000000000001), ('e', 'f')),
    'k': (Point3(75.117999999999995, 52.840000000000003, -16.620000000000001),
          ('d', 'l')),
    'l': (Point3(44.677, 27.091000000000001, -15.385), ('k', 'm')),
    'm': (Point3(77.009, -16.021999999999998, -14.975), ('l', 'c'))
}
__donaldWaypoints = (('d', 'k', 1, []), ('k', 'l', 1, []), ('l', 'm', 1, []),
                     ('m', 'c', 1, []), ('b', 'a', 1, [
                         Point3(-55.883000000000003, -89.0,
                                0.025000000000000001)
                     ]))
__plutoPaths = {
    'a': (Point3(-110.0, -37.799999999999997, 8.5999999999999996), ('b', 'c')),
    'b': (Point3(-11.9, -128.19999999999999, 6.2000000000000002), ('a', 'c')),
    'c': (Point3(48.899999999999999, -14.4, 6.2000000000000002), ('b', 'a',
                                                                  'd')),
    'd': (Point3(0.25, 80.5, 6.2000000000000002), ('c', 'e')),
    'e': (Point3(-83.299999999999997, 36.100000000000001, 6.2000000000000002),
          ('d', 'a'))
}
__plutoWaypoints = (('a', 'b', 1, [
    Point3(-90.400000000000006, -57.200000000000003, 3.0),
    Point3(-63.600000000000001, -79.799999999999997, 3.0),
    Point3(-50.100000000000001, -89.099999999999994, 6.2000000000000002)
]), ('c', 'a', 1, [
    Point3(-15.6, -25.600000000000001, 6.2000000000000002),
    Point3(-37.5, -38.5, 3.0),
    Point3(-55.0, -55.0, 3.0),
    Point3(-85.0, -46.399999999999999, 3.0)
]), ('d', 'e', 0, [
    Point3(-25.800000000000001, 60.0, 6.2000000000000002),
    Point3(-61.899999999999999, 64.5, 6.2000000000000002)
]), ('e', 'a', 1, [
    Point3(-77.200000000000003, 28.5, 6.2000000000000002),
    Point3(-76.400000000000006, 12.0, 3.0),
    Point3(-93.200000000000003, -21.199999999999999, 3.0)
]))
__daisyPaths = {
    'a': (Point3(64.995000000000005, 169.66499999999999, 10.026999999999999),
          ('b', 'q')),
    'b': (Point3(48.893000000000001, 208.91200000000001, 10.026999999999999),
          ('a', 'c')),
    'c': (Point3(5.4820000000000002, 210.47900000000001, 10.029999999999999),
          ('b', 'd')),
    'd': (Point3(-34.152999999999999, 203.28399999999999, 10.029), ('c', 'e')),
    'e': (Point3(-66.656000000000006, 174.334, 10.026), ('d', 'f')),
    'f': (Point3(-55.994, 162.33000000000001, 10.026), ('e', 'g')),
    'g': (Point3(-84.554000000000002, 142.09899999999999, 0.027), ('f', 'h')),
    'h': (Point3(-92.215000000000003, 96.445999999999998, 0.027), ('g', 'i')),
    'i': (Point3(-63.167999999999999, 60.055, 0.027), ('h', 'j')),
    'j': (Point3(-37.637, 69.974000000000004, 0.027), ('i', 'k')),
    'k': (Point3(-3.0179999999999998, 26.157, 0.027), ('j', 'l', 'm')),
    'l': (Point3(-0.71099999999999997, 46.843000000000004, 0.027), 'k'),
    'm': (Point3(26.071000000000002, 46.401000000000003, 0.027), ('k', 'n')),
    'n': (Point3(30.870000000000001, 67.432000000000002, 0.027), ('m', 'o')),
    'o': (Point3(93.903000000000006, 90.685000000000002, 0.027), ('n', 'p')),
    'p': (Point3(88.129000000000005, 140.57499999999999, 0.027), ('o', 'q')),
    'q': (Point3(53.988, 158.232, 10.026999999999999), ('p', 'a'))
}
__daisyWaypoints = (('f', 'g', 1, []), ('p', 'q', 1, []))
__chipPaths = {
    'a': (Point3(50.003999999999998, 102.72499999999999, 0.59999999999999998),
          ('b', 'k')),
    'b': (Point3(-29.552, 112.53100000000001, 0.59999999999999998), ('c',
                                                                     'a')),
    'c': (Point3(-51.941000000000003, 146.155, 0.025000000000000001), ('d',
                                                                       'b')),
    'd': (Point3(-212.334, -3.6389999999999998, 0.025000000000000001), ('e',
                                                                        'c')),
    'e': (Point3(-143.46600000000001, -67.525999999999996,
                 0.025000000000000001), ('f', 'd', 'i')),
    'f': (Point3(-107.556, -62.256999999999998, 0.025000000000000001),
          ('g', 'e', 'j')),
    'g': (Point3(-43.103000000000002, -71.518000000000001,
                 0.27339999999999998), ('h', 'f', 'j')),
    'h': (Point3(-40.604999999999997, -125.124, 0.025000000000000001), ('i',
                                                                        'g')),
    'i': (Point3(-123.05, -124.542, 0.025000000000000001), ('h', 'e')),
    'j': (Point3(-40.091999999999999, 2.7839999999999998, 1.268), ('k', 'b',
                                                                   'f', 'g')),
    'k': (Point3(75.295000000000002, 26.715, 1.3999999999999999), ('a', 'j'))
}
__chipWaypoints = (('a', 'b', 1, []), ('a', 'k', 1, []), ('b', 'c', 1, []),
                   ('b', 'j', 1, []), ('c', 'd', 1, []), ('d', 'e', 1, []),
                   ('e', 'f', 1, []), ('e', 'i', 1, []), ('f', 'g', 1, []),
                   ('f', 'j', 1, []), ('g', 'h', 1, []), ('g', 'j', 1,
                                                          []), ('h', 'i', 1,
                                                                []), ('j', 'k',
                                                                      1, []))
DaleOrbitDistanceOverride = {('b', 'c'): 2.5, ('e', 'f'): 2.5}
startNode = 'a'


def getPaths(charName, location=0):
    if charName == TTLocalizer.Mickey:
        return __mickeyPaths
    elif charName == TTLocalizer.VampireMickey:
        return __mickeyPaths
    elif charName == TTLocalizer.Minnie:
        return __minniePaths
    elif charName == TTLocalizer.WitchMinnie:
        return __minniePaths
    elif charName == TTLocalizer.Daisy or charName == TTLocalizer.SockHopDaisy:
        return __daisyPaths
    elif charName == TTLocalizer.Goofy:
        if location == 0:
            return __goofyPaths
        else:
            return __goofySpeedwayPaths
    elif charName == TTLocalizer.SuperGoofy:
        return __goofySpeedwayPaths
    elif charName == TTLocalizer.Donald or charName == TTLocalizer.FrankenDonald:
        return __donaldPaths
    elif charName == TTLocalizer.Pluto:
        return __plutoPaths
    elif charName == TTLocalizer.WesternPluto:
        return __plutoPaths
    elif charName == TTLocalizer.Chip or charName == TTLocalizer.PoliceChip:
        return __chipPaths
    elif charName == TTLocalizer.Dale or charName == TTLocalizer.JailbirdDale:
        return __chipPaths
    elif charName == TTLocalizer.DonaldDock:
        return {'a': (Point3(0, 0, 0), 'a')}


def __getWaypointList(paths):
    if paths == __mickeyPaths:
        return __mickeyWaypoints
    elif paths == __minniePaths:
        return __minnieWaypoints
    elif paths == __daisyPaths:
        return __daisyWaypoints
    elif paths == __goofyPaths:
        return __goofyWaypoints
    elif paths == __goofySpeedwayPaths:
        return __goofySpeedwayWaypoints
    elif paths == __donaldPaths:
        return __donaldWaypoints
    elif paths == __plutoPaths:
        return __plutoWaypoints
    elif paths == __chipPaths:
        return __chipWaypoints
    elif paths == __dalePaths:
        return __chipWaypoints


def getNodePos(node, paths):
    return paths[node][0]


def getAdjacentNodes(node, paths):
    return paths[node][1]


def getWayPoints(fromNode, toNode, paths, wpts=None):
    list = []
    if fromNode != toNode:
        if wpts is None:
            wpts = __getWaypointList(paths)

        for path in wpts:
            if path[0] == fromNode and path[1] == toNode:
                for point in path[3]:
                    list.append(Point3(point))

                break
                continue
            if path[0] == toNode and path[1] == fromNode:
                for point in path[3]:
                    list = [Point3(point)] + list

                break
                continue

    return list


def getRaycastFlag(fromNode, toNode, paths):
    result = 0
    if fromNode != toNode:
        wpts = __getWaypointList(paths)
        for path in wpts:
            if path[0] == fromNode and path[1] == toNode:
                if path[2]:
                    result = 1
                    break

            path[2]
            if path[0] == toNode and path[1] == fromNode:
                if path[2]:
                    result = 1
                    break

            path[2]

    return result


def getPointsFromTo(fromNode, toNode, paths):
    startPoint = Point3(getNodePos(fromNode, paths))
    endPoint = Point3(getNodePos(toNode, paths))
    return [startPoint] + getWayPoints(fromNode, toNode, paths) + [endPoint]


def getWalkDuration(fromNode, toNode, velocity, paths):
    posPoints = getPointsFromTo(fromNode, toNode, paths)
    duration = 0
    for pointIndex in range(len(posPoints) - 1):
        startPoint = posPoints[pointIndex]
        endPoint = posPoints[pointIndex + 1]
        distance = Vec3(endPoint - startPoint).length()
        duration += distance / velocity

    return duration


def getWalkDistance(fromNode, toNode, velocity, paths):
    posPoints = getPointsFromTo(fromNode, toNode, paths)
    retval = 0
    for pointIndex in range(len(posPoints) - 1):
        startPoint = posPoints[pointIndex]
        endPoint = posPoints[pointIndex + 1]
        distance = Vec3(endPoint - startPoint).length()
        retval += distance

    return retval
