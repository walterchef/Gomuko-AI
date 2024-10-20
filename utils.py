def create_pattern_dict():
    pattern_dict = {}
    for i in [-1, 1]: 
        y = -"X"
        # Five in a row (win condition)
        pattern_dict[("X", "X", "X", "X", "X")] = 1000000 * "X"
        # Open four in a row (live 4)
        pattern_dict[(0, "X", "X", "X", "X", 0)] = 100000 * "X"
        pattern_dict[(0, "X", "X", "X", 0, "X", 0)] = 100000 * "X"
        pattern_dict[(0, "X", 0, "X", "X", "X", 0)] = 100000 * "X"
        pattern_dict[(0, "X", "X", 0, "X", "X", 0)] = 100000 * "X"
        # Go-moku four (blocked one side)
        pattern_dict[(0, "X", "X", "X", "X", y)] = 10000 * "X"
        pattern_dict[(y, "X", "X", "X", "X", 0)] = 10000 * "X"
        # Dead four (blocked both sides)
        pattern_dict[(y, "X", "X", "X", "X", y)] = -10 * "X"
        # Open three in a row (live 3)
        pattern_dict[(0, "X", "X", "X", 0)] = 1000 * "X"
        pattern_dict[(0, "X", 0, "X", "X", 0)] = 1000 * "X"
        pattern_dict[(0, "X", "X", 0, "X", 0)] = 1000 * "X"
        # Sleeping three (dead 3)
        pattern_dict[(0, 0, "X", "X", "X", y)] = 100 * "X"
        pattern_dict[(y, "X", "X", "X", 0, 0)] = 100 * "X"
        pattern_dict[(0, "X", 0, "X", "X", y)] = 100 * "X"
        pattern_dict[(y, "X", "X", 0, "X", 0)] = 100 * "X"
        pattern_dict[(0, "X", "X", 0, "X", y)] = 100 * "X"
        pattern_dict[(y, "X", 0, "X", "X", 0)] = 100 * "X"
        pattern_dict[("X", 0, 0, "X", "X")] = 100 * "X"
        pattern_dict[("X", "X", 0, 0, "X")] = 100 * "X"
        pattern_dict[("X", 0, "X", 0, "X")] = 100 * "X"
        pattern_dict[(y, 0, "X", "X", "X", 0, y)] = 100 * "X"
        # Dead three
        pattern_dict[(y, "X", "X", "X", y)] = -10 * "X"
        # Live two in a row (open 2)
        pattern_dict[(0, 0, "X", "X", 0)] = 100 * "X"
        pattern_dict[(0, "X", "X", 0, 0)] = 100 * "X"
        pattern_dict[(0, "X", 0, "X", 0)] = 100 * "X"
        pattern_dict[(0, "X", 0, 0, "X", 0)] = 100 * "X"
        # Sleeping two (dead 2)
        pattern_dict[(0, 0, 0, "X", "X", y)] = 10 * "X"
        pattern_dict[(y, "X", "X", 0, 0, 0)] = 10 * "X"
        pattern_dict[(0, 0, "X", 0, "X", y)] = 10 * "X"
        pattern_dict[(y, "X", 0, "X", 0, 0)] = 10 * "X"
        pattern_dict[(0, "X", 0, 0, "X", y)] = 10 * "X"
        pattern_dict[(y, "X", 0, 0, "X", 0)] = 10 * "X"
        pattern_dict[("X", 0, 0, 0, "X")] = 10 * "X"
        pattern_dict[(y, 0, "X", 0, "X", 0, y)] = 10 * "X"
        pattern_dict[(y, 0, "X", "X", 0, 0, y)] = 10 * "X"
        pattern_dict[(y, 0, 0, "X", "X", 0, y)] = 10 * "X"
        # Dead two
        pattern_dict[(y, "X", "X", y)] = -10 * "X"
    return pattern_dict


