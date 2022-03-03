#!/usr/bin/env python
# -*- coding-UFT-8 -*-
"""
# Module pulse_integrator.

Contains everything needed to integrate certain qiskit types of pulses.
It also contains methods to keep pulse's under the cruve area constant.
"""
from typing import Callable, Any, cast
import numpy as np
from scipy.integrate import quad
from scipy.optimize import fsolve


class PulseIntegrator:
    """
    # Integrator object for certain types of qiskit pulse.

    Contains method to integrate the pulse of certain qiskit pulse.
    Currently:
    - Drag
    - Gaussian
    - Square Gaussian
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self,
                 amp: complex,
                 dur: float,
                 sig: float,
                 **kwargs: float | None) -> None:
        """
        Instantiate PulseIntegrator.

        Args:
        - amp: amplitude of the pulse.
        - dur: time duration of the pulse.
        - sig: std of the pulse.
        - width: width of gaussian square pulse.
        - beta: beta of drag pulse.
        """
        self.amp = amp
        self.dur = dur
        self.sig = sig
        self.width = None
        self.beta = None
        self.area = self.gaussian_int()
        for key, item in kwargs.items():
            if "width" == key:
                self.width = item
                self.area = self.square_gauss_int()
            if "beta" == key:
                self.beta = item
                self.area = self.drag_int()

    def __str__(self) -> str:
        """Print all the instance attributes."""
        return f"""
        area: {self.area}
        amp: {self.amp},
        dur: {self.dur},
        sig: {self.sig},
        width: {self.width},
        beta: {self.beta}
        """

    @property
    def width(self) -> float | None:
        """Width for square gaussian pulse."""
        return self._width

    @width.setter
    def width(self, val: float | None) -> None:
        self._width = val

    @property
    def area(self) -> tuple[complex, float, float]:
        """Area of pulse."""
        return self._area

    @area.setter
    def area(self, val: tuple[complex, float, float]) -> None:
        self._area = val

    @property
    def amp(self) -> complex:
        """Amplitude of pulse."""
        return self._amp

    @amp.setter
    def amp(self, val: complex) -> None:
        self._amp = val

    @property
    def sig(self) -> float:
        """Std of pulse."""
        return self._sig

    @sig.setter
    def sig(self, val: float) -> None:
        self._sig = val

    @property
    def beta(self) -> float | None:
        """Beta for Drag pulse."""
        return self._beta

    @beta.setter
    def beta(self, val: float | None) -> None:
        self._beta = val

    @property
    def dur(self) -> float:
        """Duration of pulse."""
        return self._dur

    @dur.setter
    def dur(self, val: float) -> None:
        self._dur = val

    def gaussian_int(self) -> tuple[complex, float, float]:
        """
        # Integral of the gaussian pulse of qiskit.

        Computes the integral of the gaussian pulse from
        qiskit.pulse.Gaussian.
        """
        dur = self.dur
        sig = self.sig
        amp = self.amp
        halfdur = dur / 2

        def f_prime(tmp: float) -> float:
            return cast(float, np.exp(-.5 * s_q(tmp - halfdur) / s_q(sig)))
        fm1 = f_prime(-1)

        def integral(tmp: float) -> complex:
            return amp * (f_prime(tmp) - fm1) / (1 - fm1)
        return complex_quadrature(integral, 0, dur)

    def square_gauss_int(self) -> tuple[complex, float, float]:
        """
        # Integral of the square gaussian pulse of qiskit.

        Computes the integral of the square gaussian pulse from
        qiskit.pulse.SquareGaussian.
        """
        width = self.width
        dur = self.dur
        sig = self.sig
        amp = self.amp
        if width is None:
            errmess = "Argument 'width' is required for 'square_gauss_int'"
            raise ValueError(errmess)
        assert isinstance(width, float)
        rise_fall = (dur - width) / 2

        def f_prime(x_val: float) -> float:
            if x_val < rise_fall:
                output = np.exp(-.5 * s_q(x_val - rise_fall) / s_q(sig))
            elif rise_fall <= x_val < rise_fall + cast(float, width):
                output = 1
            elif rise_fall + cast(float, width) <= x_val:
                num = x_val - rise_fall + cast(float, width)
                output = np.exp(-.5 * s_q(num) / s_q(sig))
            return float(output)
        fm1 = f_prime(-1)

        def integral(tmp: float) -> complex:
            return amp * (f_prime(tmp) - fm1) / (1 - fm1)
        return complex_quadrature(integral, 0, dur)

    def drag_int(self) -> tuple[complex, float, float]:
        """
        # Integral of the drag pulse of qiskit.

        Computes the integral of the drag pulse from
        qiskit.pulse.Drag.
        """
        beta = self.beta
        amp = self.amp
        dur = self.dur
        sig = self.sig
        if beta is None:
            errmess = "Argument 'width' is required for 'square_gauss_int'"
            raise ValueError(errmess)
        assert isinstance(beta, float)
        halfdur = dur / 2

        def g_func(x_val: float) -> float:
            return float(np.exp(-.5 * s_q(x_val - halfdur) / s_q(sig)))

        def f_prime(x_val: float) -> complex:
            g_prime = (halfdur - x_val) * g_func(x_val) / s_q(sig)
            return g_func(x_val) + 0j * cast(float, beta) * g_prime

        fm1 = f_prime(-1)

        def integral(tmp: float) -> complex:
            return amp * (f_prime(tmp) - fm1) / (1 - fm1)
        return complex_quadrature(integral, 0, dur)


def _func_to_find_zero(integrator: PulseIntegrator,
                       func: Callable[[], tuple[complex, float, float]],
                       amp: complex) -> complex:
    """Return a value shifted to be zero when the area is constant."""
    PulseIntegrator.amp.fset(integrator, amp)  # type: ignore
    new_area = func()
    return new_area[0] - integrator.area[0]


def func_as_real(func: Callable[[complex], complex]
                 ) -> Callable[[list[float]], list[float]]:
    """Use a one argument function as real."""
    def inner(args: list[float]) -> list[float]:
        temp_number = func(complex(*args))
        return [temp_number.real, temp_number.imag]
    return inner


def complex_quadrature(func: Callable[[float], complex],
                       lower_bound: float,
                       upper_bound: float,
                       **kwargs: Any) -> tuple[complex, float, float]:
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
        return np.real(func(tmp))

    def imag_func(tmp: float) -> float:
        return np.imag(func(tmp))
    real_integral = quad(real_func, lower_bound, upper_bound, **kwargs)
    imag_integral = quad(imag_func, lower_bound, upper_bound, **kwargs)
    return (real_integral[0] + 1j*imag_integral[0],
            real_integral[1:], imag_integral[1:])


def s_q(any_float: float) -> float:
    """Squares number."""
    return any_float * any_float


def find_pulse_amp(pulse: str,
                   dur: float,
                   amp: complex,
                   sig: float,
                   beta: float,
                   scale: float) -> complex | None:
    """Find the pulse amplitude of a scaled pulse."""
    # pylint: disable=too-many-arguments
    # Will fix later
    if pulse == "Drag":
        integrator = PulseIntegrator(amp, dur, sig, beta=beta)
        integrator.dur = dur * scale
        integrator.sig = sig * scale
        integrator.beta = beta * scale

        @func_as_real
        def optimize(amplitude: complex) -> complex:
            return _func_to_find_zero(integrator,
                                      integrator.drag_int,
                                      amplitude)
        return complex(*fsolve(optimize, [amp.real, amp.imag]))
    return None
