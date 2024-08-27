def xp_required_calc(level):
    """
    Calculate the required XP for the next level based on the given level (int)

    Returns:
        int: The required XP
    """
    return 5 * (level ** 2) + 10 * level + 10
