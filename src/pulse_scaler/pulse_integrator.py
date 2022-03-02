#!/usr/bin/env python
# -*- coding-UFT-8 -*-
"""
# Module pulse_integrator.

Contains everything needed to integrate certain qiskit types of pulses.
It also contains methods to keep pulse's under the cruve area constant.
"""

from typing import Callable, Tuple, Any, cast
import numpy as np
from scipy.integrate import quad


def complex_quadrature(func: Callable[[float], complex],
                       lower_bound: float,
                       upper_bound: float,
                       **kwargs: Any) -> Tuple[complex, float, float]:
    """
    # Complex quadrature of a function.

    Computes the complex quadrature of a function by using two integrals
    to avoid an error by scipy about handling complex numbers.

    params:
        func: function to integrate, Callable
        lower_bound: lower bound, float
        upper_bound: upper bound, float
        kwargs: any keyword arguments to pass to quad.
    """

    def real_func(tmp: float) -> float:
        return cast(float, np.real(func(tmp)))

    def imag_func(tmp: float) -> float:
        return cast(float, np.imag(func(tmp)))
    real_integral = quad(real_func, lower_bound, upper_bound, **kwargs)
    imag_integral = quad(imag_func, lower_bound, upper_bound, **kwargs)
    return (real_integral[0] + 1j*imag_integral[0],
            real_integral[1:], imag_integral[1:])


def s_q(any_float: float) -> float:
    """Squares number."""
    return any_float * any_float


def gaussian_int(amp: complex,
                 dur: float,
                 sig: float) -> Tuple[complex, float, float]:
    """
    # Integral of the gaussian pulse of qiskit.

    Computes the integral of the gaussian pulse from
    qiskit.pulse.Gaussian.
    """
    halfdur = dur / 2

    def f_prime(tmp: float) -> float:
        return cast(float, np.exp(-.5 * s_q(tmp - halfdur) / s_q(sig)))
    fm1 = f_prime(-1)

    def integral(tmp: float) -> complex:
        return amp * (f_prime(tmp) - fm1) / (1 - fm1)
    return complex_quadrature(integral, 0, dur)


def square_gauss_int(amp: complex,
                     dur: float,
                     width: float,
                     sig: float) -> Tuple[complex, float, float]:
    """
    # Integral of the square gaussian pulse of qiskit.

    Computes the integral of the square gaussian pulse from
    qiskit.pulse.SquareGaussian.
    """
    rise_fall = (dur - width) / 2

    def f_prime(x_val: float) -> float:
        if x_val < rise_fall:
            output = np.exp(-.5 * s_q(x_val - rise_fall) / s_q(sig))
        elif rise_fall <= x_val < rise_fall + width:
            output = 1
        elif rise_fall + width <= x_val:
            output = np.exp(-.5 * s_q(x_val - (rise_fall + width)) / s_q(sig))
        return float(output)
    fm1 = f_prime(-1)

    def integral(tmp: float) -> complex:
        return amp * (f_prime(tmp) - fm1) / (1 - fm1)
    return complex_quadrature(integral, 0, dur)


def drag_int(amp: complex,
             dur: float,
             beta: float,
             sig: float) -> Tuple[complex, float, float]:
    """
    # Integral of the drag pulse of qiskit.

    Computes the integral of the drag pulse from
    qiskit.pulse.Drag.
    """
    halfdur = dur / 2

    def g_func(x_val: float) -> float:
        return float(np.exp(-.5 * s_q(x_val - halfdur) / s_q(sig)))

    def f_prime(x_val: float) -> complex:
        g_prime = (halfdur - x_val) * g_func(x_val) / s_q(sig)
        return g_func(x_val) + 0j * beta * g_prime

    fm1 = f_prime(-1)

    def integral(tmp: float) -> complex:
        return amp * (f_prime(tmp) - fm1) / (1 - fm1)
    return complex_quadrature(integral, 0, dur)
