
def create_pattern_dict():
    PLAYER = 1
    OPPONENT = -1
    patternDict = {}
    for x in (PLAYER, OPPONENT):
        y = -x
        # long_5
        patternDict[(x, x, x, x, x)] = 1000000 * x
        # live_4
        patternDict[(0, x, x, x, x, 0)] = 100000 * x
        patternDict[(0, x, x, x, 0, x, 0)] = 100000 * x
        patternDict[(0, x, 0, x, x, x, 0)] = 100000 * x
        patternDict[(0, x, x, 0, x, x, 0)] = 100000 * x
        # go_4
        patternDict[(0, x, x, x, x, y)] = 10000 * x
        patternDict[(y, x, x, x, x, 0)] = 10000 * x
        # dead_4
        patternDict[(y, x, x, x, x, y)] = -10 * x
        # live_3
        patternDict[(0, x, x, x, 0)] = 1000 * x
        patternDict[(0, x, 0, x, x, 0)] = 1000 * x
        patternDict[(0, x, x, 0, x, 0)] = 1000 * x
        # sleep_3
        patternDict[(0, 0, x, x, x, y)] = 100 * x
        patternDict[(y, x, x, x, 0, 0)] = 100 * x
        patternDict[(0, x, 0, x, x, y)] = 100 * x
        patternDict[(y, x, x, 0, x, 0)] = 100 * x
        patternDict[(0, x, x, 0, x, y)] = 100 * x
        patternDict[(y, x, 0, x, x, 0)] = 100 * x
        patternDict[(x, 0, 0, x, x)] = 100 * x
        patternDict[(x, x, 0, 0, x)] = 100 * x
        patternDict[(x, 0, x, 0, x)] = 100 * x
        patternDict[(y, 0, x, x, x, 0, y)] = 100 * x
        # dead_3
        patternDict[(y, x, x, x, y)] = -10 * x
        # live_2
        patternDict[(0, 0, x, x, 0)] = 100 * x
        patternDict[(0, x, x, 0, 0)] = 100 * x
        patternDict[(0, x, 0, x, 0)] = 100 * x
        patternDict[(0, x, 0, 0, x, 0)] = 100 * x
        # sleep_2
        patternDict[(0, 0, 0, x, x, y)] = 10 * x
        patternDict[(y, x, x, 0, 0, 0)] = 10 * x
        patternDict[(0, 0, x, 0, x, y)] = 10 * x
        patternDict[(y, x, 0, x, 0, 0)] = 10 * x
        patternDict[(0, x, 0, 0, x, y)] = 10 * x
        patternDict[(y, x, 0, 0, x, 0)] = 10 * x
        patternDict[(x, 0, 0, 0, x)] = 10 * x
        patternDict[(y, 0, x, 0, x, 0, y)] = 10 * x
        patternDict[(y, 0, x, x, 0, 0, y)] = 10 * x
        patternDict[(y, 0, 0, x, x, 0, y)] = 10 * x
        # dead_2
        patternDict[(y, x, x, y)] = -10 * x
 
    return patternDict

