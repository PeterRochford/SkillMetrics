def report_duplicate_stats(duplicates):
    '''
    Reports list of pairs of statistics that are duplicates.

    INPUTS:
    DUPLICATES : List of tuples of paired statistics that are duplicates produced
                 by the check_duplicate_stats function

    OUTPUTS:
    None

    Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com
        prochford@thesymplectic.com

    Created on Apr 23, 2017
    '''

    if len(duplicates) == 0: return

    # Report duplicates to screen
    print('Duplicate pairs of statistics:')
    for pair in duplicates:
        print(str(pair))

