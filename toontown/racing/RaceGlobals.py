TrackSignDuration = 15
RaceCountdown = 3
MaxRacers = 4
MaxTickets = 99999
Practice = 0
ToonBattle = 1
Circuit = 2
Speedway = 0
Rural = 1
Urban = 2
RT_Speedway_1 = 0
RT_Speedway_1_rev = 1
RT_Rural_1 = 20
RT_Rural_1_rev = 21
RT_Urban_1 = 40
RT_Urban_1_rev = 41
RT_Speedway_2 = 60
RT_Speedway_2_rev = 61
RT_Rural_2 = 62
RT_Rural_2_rev = 63
RT_Urban_2 = 64
RT_Urban_2_rev = 65
KARTING_TICKETS_HOLIDAY_MULTIPLIER = 2


def getTrackGenre(trackId):
    if trackId in (
            RT_Speedway_1,
            RT_Speedway_1_rev,
            RT_Speedway_2,
            RT_Speedway_2_rev):
        return Speedway
    elif trackId in (RT_Rural_1, RT_Rural_1_rev, RT_Rural_2, RT_Rural_2_rev):
        return Rural
    else:
        return Urban


RT_Speedway_1_Gags = (
    (923.05200000000002,
     -1177.431,
     0.024),
    (926.09900000000005,
     -1187.345,
     0.024),
    (925.67999999999995,
     -1197.327,
     0.024),
    (925.16899999999998,
     -1209.502,
     0.024),
    (394.00900000000001,
     209.21899999999999,
     0.025000000000000001),
    (279.10899999999998,
     279.74400000000003,
     0.025000000000000001),
    (204.36600000000001,
     316.238,
     0.025000000000000001),
    (118.646,
     358.00900000000001,
     0.025000000000000001),
    (-1462.098,
     791.72199999999998,
     0.025000000000000001),
    (-1459.4459999999999,
     730.06399999999996,
     0.025000000000000001),
    (-1450.731,
     666.81100000000004,
     0.025000000000000001),
    (-1438.3879999999999,
     615.10000000000002,
     0.025000000000000001))
RT_Speedway_2_Gags = ((-355.18000000000001, -2430.0999999999999, -0.12672800000000001), (-343.45600000000002, -2421.4299999999998, -0.0116951), (-329.64400000000001, -2411.0599999999999, -0.016905300000000002), (-315.05399999999997, -2402.9099999999999, -0.080066700000000005), (243.29300000000001, -906.41200000000003, 0.021832000000000001),
                      (216.55500000000001, -910.88499999999999, -0.146125), (192.16, -915.92999999999995, -0.242366), (165.941, -922.38099999999997, -0.247588), (-840.62599999999998, 2405.96, 58.419499999999999), (-868.154, 2370.54, 56.739600000000003), (-896.12599999999998, 2332.5500000000002, 53.860700000000001), (-921.952, 2291.1599999999999, 49.820900000000002))
RT_Speedway_1_rev_Gags = (
    (1364.6010000000001,
     -664.452,
     0.025000000000000001),
    (1312.491,
     -588.21799999999996,
     0.025000000000000001),
    (1251.7750000000001,
     -509.55599999999998,
     0.025000000000000001),
    (1214.0519999999999,
     -461.74299999999999,
     0.025000000000000001),
    (-976.04399999999998,
     995.072,
     0.025000000000000001),
    (-1043.9169999999999,
     1018.78,
     0.025000000000000001),
    (-1124.5550000000001,
     1038.3620000000001,
     0.025000000000000001),
    (-1187.95,
     1047.0060000000001,
     0.025000000000000001),
    (-1174.5419999999999,
     -208.96799999999999,
     0.025000000000000001),
    (-1149.3399999999999,
     -270.69799999999998,
     0.025000000000000001),
    (-1121.2,
     -334.36700000000002,
     0.025000000000000001),
    (-1090.627,
     -392.66199999999998,
     0.025999999999999999))
RT_Rural_1_Gags = (
    (814.27599999999995,
     -552.928,
     2.1070000000000002),
    (847.73800000000006,
     -551.97000000000003,
     2.1059999999999999),
    (889.26499999999999,
     -549.56899999999996,
     2.1070000000000002),
    (922.02200000000005,
     -554.81299999999999,
     2.1059999999999999),
    (1791.4200000000001,
     2523.9099999999999,
     2.1059999999999999),
    (1754.1400000000001,
     2540.25,
     2.1070000000000002),
    (1689.6600000000001,
     2557.2800000000002,
     2.1070000000000002),
    (1614.01,
     2577.1599999999999,
     2.1059999999999999),
    (-1839.0,
     654.47699999999998,
     86.829999999999998),
    (-1894.3299999999999,
     640.125,
     80.390000000000001),
    (-1955.3,
     625.09000000000003,
     73.069999999999993),
    (-2016.99,
     611.74599999999998,
     65.859999999999999))
RT_Rural_2_Gags = (
    (2001.53,
     560.53200000000004,
     198.91200000000001),
    (2002.45,
     574.29200000000003,
     198.91200000000001),
    (2003.4200000000001,
     588.61199999999997,
     198.91200000000001),
    (2004,
     602.84900000000005,
     198.91200000000001),
    (-2107.4000000000001,
     2209.6700000000001,
     198.91300000000001),
    (-2086.1300000000001,
     2224.3099999999999,
     198.91300000000001),
    (-2058.1100000000001,
     2244.3099999999999,
     198.91200000000001),
    (-2023.8499999999999,
     2268.77,
     198.91200000000001),
    (-331.74599999999998,
     -1010.5700000000001,
     222.33199999999999),
    (-358.59500000000003,
     -1007.6799999999999,
     225.12899999999999),
    (-388.55599999999998,
     -1004.87,
     228.239),
    (-410.12200000000001,
     -1003.03,
     230.482),
    (69.763000000000005,
     -2324.5,
     198.91200000000001),
    (63.531399999999998,
     -2334.02,
     198.91300000000001),
    (57.966200000000001,
     -2349.1399999999999,
     198.91300000000001),
    (51.883800000000001,
     -2363.8699999999999,
     198.91300000000001))
RT_Urban_1_Gags = (
    (51.995199999999997,
     2431.6199999999999,
     55.705300000000001),
    (39.540700000000001,
     2421.6399999999999,
     65.705299999999994),
    (27.750399999999999,
     2411.6700000000001,
     55.705300000000001),
    (15.550000000000001,
     2401.6500000000001,
     65.705299999999994),
    (-1008.36,
     2116.4099999999999,
     0.024679799999999998),
    (-1050.3099999999999,
     2099.7800000000002,
     0.025000000000000001),
    (-1092.26,
     2083.1500000000001,
     0.025320200000000001),
    (-1134.21,
     2066.52,
     0.025640400000000001),
    (-1966.6800000000001,
     1139.3199999999999,
     1.7698100000000001),
    (-1970.46,
     1120.5699999999999,
     1.7698100000000001),
    (-1974.1800000000001,
     1101.8199999999999,
     1.7698100000000001),
    (-1977.9300000000001,
     1084.0699999999999,
     1.7698100000000001),
    (1419.05,
     -2987.1799999999998,
     0.025000000000000001),
    (1411.0899999999999,
     -3004.0900000000001,
     0.025000000000000001),
    (1403.1300000000001,
     -3021.0100000000002,
     0.025000000000000001),
    (1395.1700000000001,
     -3037.9200000000001,
     0.025000000000000001),
    (948.13099999999997,
     -1216.77,
     0.025000000000000001),
    (935.54499999999996,
     -1204.0899999999999,
     0.025000000000000001),
    (922.95899999999995,
     -1191.4100000000001,
     0.025000000000000001),
    (909.95899999999995,
     -1177.4100000000001,
     0.025000000000000001))
RT_Urban_2_Gags = ((-2761.4899999999998, -3070.9699999999998, -0.25512200000000002), (-2730.1799999999998, -3084.0900000000001, -0.25515300000000002), (-2701.4499999999998, -3096.2600000000002, -0.25566899999999998), (-2669.8099999999999, -3108.9000000000001, -0.25525199999999998), (735.47900000000004, -423.82799999999997, 23.7334), (759.02599999999995, -427.19799999999998, 23.006799999999998), (783.23199999999997, -430.65899999999999, 22.256900000000002), (809.91399999999999, -434.476, 21.432600000000001), (3100.0900000000001, 240.411, 23.467199999999998), (3089.0900000000001, 242.01900000000001,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     23.525099999999998), (3077.6799999999998, 243.68799999999999, 23.685700000000001), (3064.8200000000002, 245.56700000000001, 23.877099999999999), (-10.738899999999999, 2980.48, -0.25560899999999998), (-41.264400000000002, 2974.5300000000002, -0.25512200000000002), (-69.842299999999994, 2989.98, -0.25568200000000002), (-102.331, 2986.0999999999999, -0.255637), (-1978.6700000000001, 588.98099999999999, -0.255685), (-1977.0699999999999, 560.79700000000003, -0.255415), (-1948.5799999999999, 544.78200000000004, -0.25512200000000002), (-1943.4200000000001, 510.262, -0.25586599999999998))
RT_Urban_1_rev_Gags = (
    (1034.4300000000001,
     -366.37099999999998,
     0.025000000000000001),
    (1051.8399999999999,
     -360.47300000000001,
     0.025000000000000001),
    (1069.25,
     -354.57499999999999,
     0.025000000000000001),
    (1086.6600000000001,
     -348.67700000000002,
     0.025000000000000001),
    (1849.6600000000001,
     -2807.21,
     0.0246158),
    (1858.55,
     -2795.9899999999998,
     0.0246158),
    (1867.4400000000001,
     -2784.7600000000002,
     0.0246158),
    (1876.3299999999999,
     -2773.5300000000002,
     0.0246158),
    (316.34199999999998,
     -44.9529,
     0.025000000000000001),
    (305.173,
     -63.4405,
     0.025000000000000001),
    (294.00400000000002,
     -81.928100000000001,
     0.025000000000000001),
    (282.83499999999998,
     -100.416,
     0.025000000000000001),
    (-762.37699999999995,
     2979.25,
     0.025000000000000001),
    (-753.029,
     2995.6900000000001,
     0.025000000000000001),
    (-743.68100000000004,
     3012.1399999999999,
     0.025000000000000001),
    (-734.33299999999997,
     3028.5799999999999,
     0.025000000000000001),
    (470.62799999999999,
     1828.3199999999999,
     55.0),
    (481.28399999999999,
     1836.8900000000001,
     55.0),
    (491.94099999999997,
     1845.47,
     55.0),
    (502.59699999999998,
     1854.04,
     55.0))
Speedway_1_Boosts = (((-320, 685, 1), (415, 0, 0)),)
Speedway_1_Rev_Boosts = (((-320, 685, 0.10000000000000001), (235, 0, 0)),)
Speedway_2_Boosts = (((-120, 430, 1.0), (-50, 0, 0)),)
Speedway_2_Rev_Boosts = (((176, 625, 1.0), (130, 0, 0)),)
Rural_1_Boosts = (((3132.6399999999999, 859.55999999999995, 5.0), (384.44, 363.5, 0)),
                  ((-3050.3299999999999, -1804.97, 207.69999999999999), (229.40000000000001, 353.25, 342.89999999999998)))
Rural_1_Rev_Boosts = (((3132.6399999999999, 859.55999999999995, 5.0), (197.09999999999999, -2.25, 0)),
                      ((-3151.3400000000001, -1569.5599999999999, 200.62100000000001), (189.46000000000001, 182.75, 195.255)))
Rural_2_Boosts = (((873.255, -593.66399999999999, 199.5), (87.715000000000003, 0, 0)),
                  ((-1747.6199999999999, 801.55999999999995, 199.5), (-126.51600000000001, 0, 0)))
Rural_2_Rev_Boosts = (((-428.00400000000002, -243.69200000000001, 324.51600000000002),
                       (51.427999999999997, 6, 1)), ((-384.04300000000001, 211.62, 193.5), (-127.85899999999999, 1, 0)))
Urban_1_Boosts = (
    ((677.05700000000002,
      1618.24,
      0.025000000000000001),
     (35.999499999999998,
      0,
      0)),
    ((-2250.3499999999999,
      1618.0999999999999,
      0.0241526),
     (-154.80000000000001,
      0,
      0)),
    ((400.13,
      -1090.26,
      0.025000000000000001),
     (-175.20400000000001,
      0,
      0)))
Urban_1_Rev_Boosts = (
    ((488.73899999999998,
      -2055.0700000000002,
      0.025000000000000001),
     (3.5975299999999999,
      0,
      0)),
    ((-1737.29,
      588.13800000000003,
      0.025000000000000001),
     (26.397500000000001,
      0,
      0)),
    ((-212.31399999999999,
      2638.3400000000001,
      0.025000000000000001),
     (-128.404,
      0,
      0)))
Urban_2_Boosts = (((358.13400000000001, -1655.4200000000001, 0.29999999999999999), (-4.9500000000000002, 1, 0)), ((2058.77, 2560.0300000000002,
                                                                                                                   0.29999999999999999), (77.310000000000002, 0, 0)), ((-3081.3299999999999, -1037.55, 0.25), (177.35900000000001, 0, 0)))
Urban_2_Rev_Boosts = (
    ((-2007.3800000000001,
      484.87799999999999,
      0.25),
     (30.9102,
      0,
      0)),
    ((2646.5100000000002,
      1455.1500000000001,
      0.25),
     (-120.172,
      0,
      0)),
    ((-472.21499999999997,
      -2048.21,
      0.25),
     (136.19200000000001,
      0,
      0)))


def RaceInfo2RacePadId(trackId, trackType):
    rev = trackId % 2
    if not rev:
        if trackType == Practice:
            padId = 0
        else:
            padId = 2
    elif trackType == Practice:
        padId = 1
    else:
        padId = 3
    return padId


def getTrackGenreString(genreId):
    genreStrings = [
        'Speedway',
        'Country',
        'City']
    return genreStrings[genreId].lower()


def getTunnelSignName(genreId, padId):
    if genreId == 2 and padId == 0:
        return 'tunne1l_citysign'
    elif genreId == 1 and padId == 0:
        return 'tunnel_countrysign1'
    else:
        return 'tunnel%s_%ssign' % (padId + 1, getTrackGenreString(genreId))


RacePadId2RaceInfo = {
    0: (0, Practice, 3),
    1: (1, Practice, 3),
    2: (0, ToonBattle, 3),
    3: (1, ToonBattle, 3)}


def getGenreFromString(string):
    if string == 'town':
        return Urban
    elif string == 'stadium':
        return Speedway
    else:
        return Rural


def getTrackListByType(genre, type):
    return Rural


def getTrackListByType(genre, type):
    genreDict = {
        Urban: [
            [
                RT_Urban_1,
                RT_Urban_2],
            [
                RT_Urban_1_rev,
                RT_Urban_2_rev]],
        Rural: [
            [
                RT_Rural_1,
                RT_Rural_2],
            [
                RT_Rural_1_rev,
                RT_Rural_2_rev]],
        Speedway: [
            [
                RT_Speedway_1,
                RT_Speedway_2],
            [
                RT_Speedway_1_rev,
                RT_Speedway_2_rev]]}
    trackIdList = genreDict.get(genre)
    return trackIdList[type]


def getCanonicalPadId(padId):
    return padId % 4


def getNextRaceInfo(prevTrackId, genreString, padId):
    genre = getGenreFromString(genreString)
    cPadId = getCanonicalPadId(padId)
    raceInfo = RacePadId2RaceInfo.get(cPadId)
    trackList = getTrackListByType(genre, raceInfo[0])
    if trackList.count(prevTrackId) == 0:
        trackId = trackList[1]
    else:
        index = trackList.index(prevTrackId)
        index += 1
        index %= len(trackList)
        trackId = trackList[index]
    return (trackId, raceInfo[1], raceInfo[2])


TrackPath = 'phase_6/models/karting/'
TrackDict = {
    RT_Speedway_1: (TrackPath + 'RT_SpeedwayA', 240.0, 115.0, (50, 500), RT_Speedway_1_Gags, Speedway_1_Boosts, 1.0, 'GS_Race_SS.mid', (0.01, 0.014999999999999999)),
    RT_Speedway_1_rev: (TrackPath + 'RT_SpeedwayA', 240.0, 115.0, (50, 500), RT_Speedway_1_rev_Gags, Speedway_1_Rev_Boosts, 1.0, 'GS_Race_SS.mid', (0.01, 0.014999999999999999)),
    RT_Speedway_2: (TrackPath + 'RT_SpeedwayB', 335.0, 210.0, (75, 1000), RT_Speedway_2_Gags, Speedway_2_Boosts, 1.0, 'GS_Race_SS.mid', (0.01, 0.014999999999999999)),
    RT_Speedway_2_rev: (TrackPath + 'RT_SpeedwayB', 335.0, 210.0, (75, 1000), RT_Speedway_2_Gags, Speedway_2_Rev_Boosts, 1.0, 'GS_Race_SS.mid', (0.01, 0.014999999999999999)),
    RT_Rural_1: (TrackPath + 'RT_RuralB', 360.0, 230.0, (100, 500), RT_Rural_1_Gags, Rural_1_Boosts, 0.75, 'GS_Race_RR.mid', (0.0030000000000000001, 0.0040000000000000001)),
    RT_Rural_1_rev: (TrackPath + 'RT_RuralB', 360.0, 230.0, (100, 500), RT_Rural_1_Gags, Rural_1_Rev_Boosts, 0.75, 'GS_Race_RR.mid', (0.0030000000000000001, 0.0040000000000000001)),
    RT_Rural_2: (TrackPath + 'RT_RuralB2', 480.0, 360.0, (150, 1000), RT_Rural_2_Gags, Rural_2_Boosts, 0.75, 'GS_Race_RR.mid', (0.0030000000000000001, 0.0040000000000000001)),
    RT_Rural_2_rev: (TrackPath + 'RT_RuralB2', 480.0, 360.0, (150, 1000), RT_Rural_2_Gags, Rural_2_Rev_Boosts, 0.75, 'GS_Race_RR.mid', (0.0030000000000000001, 0.0040000000000000001)),
    RT_Urban_1: (TrackPath + 'RT_UrbanA', 480.0, 305.0, (300, 500), RT_Urban_1_Gags, Urban_1_Boosts, 1.0, 'GS_Race_CC.mid', (0.002, 0.0030000000000000001)),
    RT_Urban_1_rev: (TrackPath + 'RT_UrbanA', 480.0, 305.0, (300, 500), RT_Urban_1_rev_Gags, Urban_1_Rev_Boosts, 1.0, 'GS_Race_CC.mid', (0.002, 0.0030000000000000001)),
    RT_Urban_2: (TrackPath + 'RT_UrbanB', 480.0, 280.0, (400, 1000), RT_Urban_2_Gags, Urban_2_Boosts, 1.0, 'GS_Race_CC.mid', (0.002, 0.0030000000000000001)),
    RT_Urban_2_rev: (TrackPath + 'RT_UrbanB', 480.0, 280.0, (400, 1000), RT_Urban_2_Gags, Urban_2_Rev_Boosts, 1.0, 'GS_Race_CC.mid', (0.002, 0.0030000000000000001))}
TrackIds = sorted(TrackDict.keys())


def getEntryFee(trackId, raceType):
    fee = 0
    if raceType == ToonBattle:
        fee = TrackDict[trackId][3][0]
    elif raceType == Circuit:
        fee = TrackDict[trackId][3][1]

    return fee


def getQualifyingTime(trackId):
    return TrackDict[trackId][1]


def getDefaultRecordTime(trackId):
    return TrackDict[trackId][2]


Daily = 0
Weekly = 1
AllTime = 2
PeriodDict = {
    Daily: 10,
    Weekly: 100,
    AllTime: 1000}
PeriodIds = PeriodDict.keys()
NumRecordPeriods = len(PeriodIds)
NumRecordsPerPeriod = 10
Winnings = [
    3.0,
    1.0,
    0.5,
    0.14999999999999999]
PracticeWinnings = 20
SpeedwayQuals = 0
RuralQuals = 1
UrbanQuals = 2
SpeedwayWins = 3
RuralWins = 4
UrbanWins = 5
CircuitWins = 6
TwoPlayerWins = 7
ThreePlayerWins = 8
FourPlayerWins = 9
CircuitSweeps = 10
CircuitQuals = 11
QualsList = [
    SpeedwayQuals,
    RuralQuals,
    UrbanQuals]
WinsList = [
    SpeedwayWins,
    RuralWins,
    UrbanWins]
SpeedwayQuals1 = 0
SpeedwayQuals2 = 1
SpeedwayQuals3 = 2
RuralQuals1 = 3
RuralQuals2 = 4
RuralQuals3 = 5
UrbanQuals1 = 6
UrbanQuals2 = 7
UrbanQuals3 = 8
TotalQuals = 9
SpeedwayWins1 = 10
SpeedwayWins2 = 11
SpeedwayWins3 = 12
RuralWins1 = 13
RuralWins2 = 14
RuralWins3 = 15
UrbanWins1 = 16
UrbanWins2 = 17
UrbanWins3 = 18
TotalWins = 19
CircuitQuals1 = 20
CircuitQuals2 = 21
CircuitQuals3 = 22
CircuitWins1 = 23
CircuitWins2 = 24
CircuitWins3 = 25
CircuitSweeps1 = 26
CircuitSweeps2 = 27
CircuitSweeps3 = 28
GrandTouring = 29
NumTrophies = 30
TenTrophyCup = 30
TwentyTrophyCup = 31
ThirtyTrophyCup = 32
TrophyCups = [
    TenTrophyCup,
    TwentyTrophyCup,
    ThirtyTrophyCup]
NumCups = 3
SpeedwayQualsList = [
    SpeedwayQuals1,
    SpeedwayQuals2,
    SpeedwayQuals3]
RuralQualsList = [
    RuralQuals1,
    RuralQuals2,
    RuralQuals3]
UrbanQualsList = [
    UrbanQuals1,
    UrbanQuals2,
    UrbanQuals3]
SpeedwayWinsList = [
    SpeedwayWins1,
    SpeedwayWins2,
    SpeedwayWins3]
RuralWinsList = [
    RuralWins1,
    RuralWins2,
    RuralWins3]
UrbanWinsList = [
    UrbanWins1,
    UrbanWins2,
    UrbanWins3]
CircuitWinsList = [
    CircuitWins1,
    CircuitWins2,
    CircuitWins3]
CircuitSweepsList = [
    CircuitSweeps1,
    CircuitSweeps2,
    CircuitSweeps3]
CircuitQualList = [
    CircuitQuals1,
    CircuitQuals2,
    CircuitQuals3]
AllQualsList = [
    SpeedwayQualsList,
    RuralQualsList,
    UrbanQualsList]
AllWinsList = [
    SpeedwayWinsList,
    RuralWinsList,
    UrbanWinsList]
TrophiesPerCup = NumTrophies / NumCups
QualifiedRaces = [
    1,
    10,
    100]
TotalQualifiedRaces = 100
WonRaces = [
    1,
    10,
    100]
TotalWonRaces = 100
WonCircuitRaces = [
    1,
    5,
    25]
SweptCircuitRaces = [
    1,
    5,
    25]
QualifiedCircuitRaces = [
    1,
    5,
    25]
LBSubscription = {
    'stadium': [
        (RT_Speedway_1, Daily),
        (RT_Speedway_1, Weekly),
        (RT_Speedway_1, AllTime),
        (RT_Speedway_1_rev, Daily),
        (RT_Speedway_1_rev, Weekly),
        (RT_Speedway_1_rev, AllTime),
        (RT_Speedway_2, Daily),
        (RT_Speedway_2, Weekly),
        (RT_Speedway_2, AllTime),
        (RT_Speedway_2_rev, Daily),
        (RT_Speedway_2_rev, Weekly),
        (RT_Speedway_2_rev, AllTime)],
    'country': [
        (RT_Rural_1, Daily),
        (RT_Rural_1, Weekly),
        (RT_Rural_1, AllTime),
        (RT_Rural_1_rev, Daily),
        (RT_Rural_1_rev, Weekly),
        (RT_Rural_1_rev, AllTime),
        (RT_Rural_2, Daily),
        (RT_Rural_2, Weekly),
        (RT_Rural_2, AllTime),
        (RT_Rural_2_rev, Daily),
        (RT_Rural_2_rev, Weekly),
        (RT_Rural_2_rev, AllTime)],
    'city': [
        (RT_Urban_1, Daily),
        (RT_Urban_1, Weekly),
        (RT_Urban_1, AllTime),
        (RT_Urban_1_rev, Daily),
        (RT_Urban_1_rev, Weekly),
        (RT_Urban_1_rev, AllTime),
        (RT_Urban_2, Daily),
        (RT_Urban_2, Weekly),
        (RT_Urban_2, AllTime),
        (RT_Urban_2_rev, Daily),
        (RT_Urban_2_rev, Weekly),
        (RT_Urban_2_rev, AllTime)]}
BANANA = 1
TURBO = 2
ANVIL = 3
PIE = 4
GagFreq = [
    [
        PIE,
        BANANA,
        BANANA,
        BANANA,
        TURBO,
        PIE],
    [
        PIE,
        BANANA,
        BANANA,
        TURBO,
        ANVIL,
        PIE],
    [
        PIE,
        BANANA,
        TURBO,
        TURBO,
        ANVIL,
        PIE],
    [
        BANANA,
        TURBO,
        TURBO,
        TURBO,
        ANVIL,
        PIE]]
CircuitLoops = [
    [
        RT_Speedway_1,
        RT_Rural_1,
        RT_Urban_1],
    [
        RT_Speedway_1_rev,
        RT_Rural_1_rev,
        RT_Urban_1_rev],
    [
        RT_Speedway_2,
        RT_Rural_2,
        RT_Urban_2],
    [
        RT_Speedway_2_rev,
        RT_Rural_2_rev,
        RT_Urban_2_rev]]
CircuitPoints = [
    10,
    8,
    6,
    4]


def getCircuitLoop(startingTrack):
    circuitLoop = [
        startingTrack]
    for loop in CircuitLoops:
        if startingTrack in loop:
            print loop
            numTracks = len(loop)
            tempLoop = loop * 2
            startingIndex = tempLoop.index(startingTrack)
            circuitLoop = tempLoop[startingIndex:startingIndex + numTracks]
            break
            continue

    return circuitLoop


Exit_UserReq = 0
Exit_Barrier = 1
Exit_Slow = 2
Exit_BarrierNoRefund = 3
