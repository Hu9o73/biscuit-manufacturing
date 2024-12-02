def noOverlap(problem):
    biscuit_start_pos = problem.biscuit_start_pos
    roll = problem.roll
    biscuit_thresholds = problem.biscuit_thresholds 
    for x in biscuit_start_pos:
        problem.complexity += 1
        biscuitType = roll[x]
        biscuitSize = biscuit_thresholds[biscuitType]['size']
        
        for j in range(x, x+biscuitSize):
            problem.complexity += 1
            if roll[j] != biscuitType:
                return False

    return True

def defectsUnderThreshold(problem):
    biscuit_start_pos = problem.biscuit_start_pos
    roll = problem.roll
    biscuit_thresholds = problem.biscuit_thresholds 
    defect_data = problem.defect_data

    for i in biscuit_start_pos:
        problem.complexity += 1
        biscuitType = roll[i]
        biscuitSize = biscuit_thresholds[biscuitType]['size']
        
        defectsCount = [0,0,0]

        for j in range(i, i+biscuitSize):
            problem.complexity += 1
            if 'a' in defect_data[j]:
                defectsCount[0] += 1
            if 'b' in defect_data[j]:
                defectsCount[1] += 1
            if 'c' in defect_data[j]:
                defectsCount[2] += 1

        if defectsCount[0] > biscuit_thresholds[biscuitType]['a']:
            return False
        
        if defectsCount[1] > biscuit_thresholds[biscuitType]['b']:
            return False
        
        if defectsCount[2] > biscuit_thresholds[biscuitType]['c']:
            return False
    
    return True


def biscuitsFitOnRoll(scope):
    assigned_positions = sum([var.state is not None for var in scope])
    return assigned_positions <= len(scope)