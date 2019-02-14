from direct.showbase import RandomNumGen


def getMazeName(gameDoId, numPlayers, mazeNames):

    try:
        return forcedMaze
    except BaseException:
        names = mazeNames[numPlayers - 1]
        return names[RandomNumGen.randHash(gameDoId) % len(names)]


ENDLESS_GAME = config.GetBool('endless-maze-game', 0)
GAME_DURATION = 60.0
SHOWSCORES_DURATION = 2.0
SUIT_TIC_FREQ = int(256)
WALK_SAME_DIRECTION_PROB = 4
WALK_TURN_AROUND_PROB = 30
SUIT_START_POSITIONS = ((0.25, 0.25), (0.75, 0.75), (0.25, 0.75), (0.75, 0.25),
                        (0.20000000000000001, 0.5), (0.80000000000000004, 0.5),
                        (0.5, 0.20000000000000001), (0.5, 0.80000000000000004),
                        (0.33000000000000002,
                         0.0), (0.66000000000000003,
                                0.0), (0.33000000000000002,
                                       1.0), (0.66000000000000003, 1.0),
                        (0.0, 0.33000000000000002), (0.0, 0.66000000000000003),
                        (1.0, 0.33000000000000002), (1.0, 0.66000000000000003))
