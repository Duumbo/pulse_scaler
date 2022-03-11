#!/usr/bin/env python
# -*- coding-UFT-8 -*-
"""Test the implementation of the extrapolators."""
import numpy as np
import pulse_scaler.extrapolation as ex


def test_error_management_extrapolation() -> None:
    """
    Test error management.

    Bad input, should raise a ValueError.
    """
    x_vect: np.typing.NDArray[np.float64] = np.array(list(range(10)))
    y_vect: np.typing.NDArray[np.float64] = np.array(list(range(9)))
    try:
        _ = ex.lin_extr(y_vect, x_vect)
        assert False, "Bad error management."
    except ValueError:
        pass


def test_linear() -> None:
    """Test the linear extrapolator."""
    x_vect: np.typing.NDArray[np.float64] = np.array([1, 2, 3])
    y_vect: np.typing.NDArray[np.float64] = np.array([1, 2, 3])
    val = ex.lin_extr(y_vect, x_vect)
    print(val)
    assert np.isclose(val, 0)

    x_vect = np.array([2 * x for x in range(1, 10)])
    y_vect = np.array([4 * x for x in range(9)])
    val = ex.lin_extr(y_vect, x_vect)
    print(val)
    assert np.isclose(val, -4)
