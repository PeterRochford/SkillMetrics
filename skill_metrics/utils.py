import numpy as np


def check_arrays(predicted,
                 reference):
    """Generic check of input arrays."""
    pdims = predicted.shape
    rdims = reference.shape
    if not np.array_equal(pdims, rdims):
        raise ValueError("""
*
*   The predicted and reference field dimensions do not match.
*       shape(predicted) = {0}
*       shape(reference) = {1}
*       predicted type: {2}
*
""".format(pdims, rdims, type(predicted)))
