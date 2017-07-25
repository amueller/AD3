"""Test pystruct integration"""
# Author: Vlad Niculae <vlad@vene.ro>

try:
    import pystruct
    has_pystruct = True
except ImportError:
    has_pystruct = False

import numpy as np
from numpy.testing import assert_array_equal, assert_almost_equal
from nose import SkipTest


def test_pystruct():
    if not has_pystruct:
        raise SkipTest("pystruct not available")

    from pystruct.inference import inference_ad3

    unaries = np.zeros((3, 5))
    unaries[1, 2] = 2
    pairwise = np.eye(5)
    edges = np.array([[0, 1], [1, 2], [0, 2]], dtype=np.intp)

    # no parameters
    labels = inference_ad3(unaries, pairwise, edges)
    assert_array_equal(labels, [2, 2, 2])

    # exact decoding
    labels_exact = inference_ad3(unaries, pairwise, edges,
                                 branch_and_bound=True)
    assert_array_equal(labels_exact, [2, 2, 2])

    # request energy
    labels, energy = inference_ad3(unaries, pairwise, edges,
                                   return_energy=True)
    assert_array_equal(energy, -5)

    # exact decoding and request energy
    labels, energy = inference_ad3(unaries, pairwise, edges,
                                   branch_and_bound=True, return_energy=True)
    assert_array_equal(energy, -5)

