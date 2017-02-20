def target_statistics(predicted,reference,field='',norm=False):
    '''
    Calculates the statistics needed to create a target diagram as 
    described in Jolliff et al. (2009) using the data provided in the 
    predicted field (PREDICTED) and the reference field (REFERENCE).
    
    The statistics are returned in the STATS dictionary.

    If a dictionary is provided for PREDICTED or REFERENCE, then 
    the name of the field must be supplied in FIELD.
 
    The function currently supports dictionaries, lists, and np.ndarray,
    types for the PREDICTED and REFERENCE variables.
 
    Input:
    PREDICTED : predicted field
    REFERENCE : reference field
    FIELD     : name of field to use in PREDICTED and REFERENCE dictionaries
                (optional)
    NORM      : logical flag specifying statistics are to be normalized 
                with respect to standard deviation of reference field
                = True,  statistics are normalized
                = False, statistics are not normalized
 
    Output:
    STATS          : dictionary containing statistics
    STATS['bias']  : bias (B)
    STATS['crmsd'] : centered root-mean-square (RMS) differences (E')
    STATS['rmsd']  : total RMS difference (RMSD)
 
    Each of these outputs are one-dimensional with the same length.
 
    Reference:
 
    Jolliff, J. K., J. C. Kindle, I. Shulman, B. Penta, M. Friedrichs, 
      R. Helber, and R. Arnone (2009), Skill assessment for coupled 
      biological/physical models of marine systems, J. Mar. Sys., 76(1-2),
      64-82, doi:10.1016/j.jmarsys.2008.05.014

    Author: Peter A. Rochford
        Symplectic, LLC
        www.thesymplectic.com
        prochford@thesymplectic.com

    Created on Nov 24, 2016
    '''
    import numpy as np
    from skill_metrics import centered_rms_dev

    # Check for valid arguments
    if isinstance(predicted, dict):
        if field == '':
            raise ValueError('FIELD argument not supplied.')
        if field in predicted:
            p = predicted[field]
        else:
            raise ValueError('Field is not in PREDICTED dictionary: ' + field)
    elif isinstance(predicted, list):
        p = np.array(predicted)
    elif isinstance(predicted, np.ndarray):
        p = predicted
    else:
        raise ValueError('PREDICTED argument must be a dictionary.')
            
    if isinstance(reference, dict):
        if field == '':
            raise ValueError('FIELD argument not supplied.')
        if field in reference:
            r = reference[field]
        else:
            raise ValueError('Field is not in REFERENCE dictionary: ' + field)
    elif isinstance(reference, list):
        r = np.array(reference)
    elif isinstance(reference, np.ndarray):
        r = reference
    else:
        raise ValueError('REFERENCE argument must be a dictionary.')

    # Check that dimensions of predicted and reference fields match
    #ToDo: Implement check

    # Calculate bias (B)
    bias = np.mean(p) - np.mean(r)

    # Calculate centered root-mean-square (RMS) difference (E')
    crmsd = centered_rms_dev(p,r)

    # Calculate RMS difference (RMSD)
    rmsd = np.sqrt(np.sum(np.square(np.subtract(p,r)))/float(p.size))

    # Normalize if requested
    if norm == True:
        sigma_ref = np.std(r)
        bias = bias/sigma_ref
        crmsd = crmsd/sigma_ref
        rmsd = rmsd/sigma_ref

    # Store statistics in a dictionary
    stats = {'bias': bias, 'crmsd': crmsd, 'rmsd': rmsd}
    if norm == True:
        stats['type'] = 'normalized'
    else:
        stats['type'] = 'unnormalized'

    return stats
