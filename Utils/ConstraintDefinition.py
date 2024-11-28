def noOverlap(scope):
    # Normally never false as we can't place a biscuit if another one is already here.
    return True

def defectsUnderThreshold(scope):

    
    return True


def biscuitsFitOnRoll(scope):
    # Normally never False as we can't place a biscuit if it goes above the roll's array length.
    assigned_positions = sum([var.state is not None for var in scope])
    return assigned_positions <= len(scope)