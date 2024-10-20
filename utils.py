def create_pattern_dict():
    """Create a pattern dictionary with detailed patterns for evaluation."""
    pattern_dict = {}
    for i in [-1, 1]:  # Handle both player (1) and opponent (-1)
        y = i
        # Five in a row (win condition)
        pattern_dict[(i, i, i, i, i)] = 1000000 * i
        
        # Open four in a row (live 4)
        pattern_dict[(0, i, i, i, i, 0)] = 100000 * i
        pattern_dict[(0, i, i, i, 0, i, 0)] = 100000 * i
        pattern_dict[(0, i, 0, i, i, i, 0)] = 100000 * i
        pattern_dict[(0, i, i, 0, i, i, 0)] = 100000 * i

        # Blocked one side (go-moku four)
        pattern_dict[(0, i, i, i, i, y)] = 10000 * i
        pattern_dict[(y, i, i, i, i, 0)] = 10000 * i

        # Blocked both sides (dead four)
        pattern_dict[(y, i, i, i, i, y)] = -10 * i

        # Open three in a row (live 3)
        pattern_dict[(0, i, i, i, 0)] = 1000 * i
        pattern_dict[(0, i, 0, i, i, 0)] = 1000 * i
        pattern_dict[(0, i, i, 0, i, 0)] = 1000 * i

        # Sleeping three (blocked one side, dead 3)
        pattern_dict[(0, 0, i, i, i, y)] = 100 * i
        pattern_dict[(y, i, i, i, 0, 0)] = 100 * i
        pattern_dict[(0, i, 0, i, i, y)] = 100 * i
        pattern_dict[(y, i, i, 0, i, 0)] = 100 * i

        # Dead three
        pattern_dict[(y, i, i, i, y)] = -10 * i

        # Live two in a row (open 2)
        pattern_dict[(0, 0, i, i, 0)] = 100 * i
        pattern_dict[(0, i, i, 0, 0)] = 100 * i
        pattern_dict[(0, i, 0, i, 0)] = 100 * i

        # Sleeping two (dead 2)
        pattern_dict[(0, 0, 0, i, i, y)] = 10 * i
        pattern_dict[(y, i, i, 0, 0, 0)] = 10 * i

        # Dead two
        pattern_dict[(y, i, i, y)] = -10 * i

    return pattern_dict
