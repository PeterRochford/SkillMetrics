def check_duplicate_stats(stats1, stats2, threshold = 0.01):
    '''
    Checks two lists of paired statistics for duplicates and returns a list of
    the pairs that agree within to <1%.

    INPUTS:
    STATS1 : List of first statistical metric, e.g. Standard Deviations
    STATS2 : List of second statistical metric, e.g. Centered Root Mean Square Difference

    OUTPUTS:
    DUPLICATES : List of tuples of paired statistics that are duplicates. The list contains
                 the index locations of the pairs of statistics followed by their values
                 as 2-tuples.

    Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com
        prochford@thesymplectic.com

    Created on Apr 23, 2017
    '''
    if threshold < 1e-7:
        raise ValueError('threshold value must be positive: ' + str(threshold))

    # Check for non-empty lists
    if len(stats1) == 0:
        raise ValueError('Argument stats1 is empty list!')
    elif len(stats2) == 0:
        raise ValueError('Argument stats2 is empty list!')

    # Check for matching list lengths
    if len(stats1) != len(stats2):
        raise ValueError('Arguments stats1 and stats2 have different list lengths.\n' +
                   'len(stats1) = ' + str(len(stats1)) + ' != len(stats2) = ' +
                   str(len(stats2)))
    
    # Search for duplicate pairs of statistics
    duplicates = []
    n = len(stats1)
    for i in range(n):
        for j in range(i+1,n):
            diff1 = abs((stats1[i] - stats1[j])/stats1[i])
            diff2 = abs((stats2[i] - stats2[j])/stats2[i])
            if diff1 < threshold and diff2 < threshold:
                duplicates.append( (i, j, (stats1[i], stats2[i]), (stats1[j], stats2[j])) )
 
    return duplicates

