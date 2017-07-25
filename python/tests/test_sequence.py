# Author: Vlad Niculae <vlad@vene.ro>
# License: GNU LGPL v3

import numpy as np
from numpy.testing import assert_array_equal

from .. import factor_graph as fg
from .. import solve


def test_sequence_dense():

    n_states = 3
    transition = np.eye(n_states).ravel()
    graph = fg.PFactorGraph()

    vars_expected = [0, 1, None, None, 1]
    vars = [graph.create_multi_variable(n_states) for _ in vars_expected]
    factors = [graph.create_factor_dense([prev, curr], transition)
               for prev, curr in zip(vars, vars[1:])]
    for var, ix in zip(vars, vars_expected):
        if ix is not None:
            var.set_log_potential(ix, 1)

    value, marginals, additionals, status = solve(graph)
    # 3 points for "observed" values, 3 points for consecutive equal vals
    assert value == 6

    expected = [0, 1, 1, 1, 1]
    obtained = np.array(marginals).reshape(5, -1).argmax(axis=1)
    assert_array_equal(expected, obtained)
