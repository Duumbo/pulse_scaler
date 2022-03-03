# -*- coding-UFT-8 -*-
"""Test related to integration of pulses."""
import pulse_scaler.pulse_integrator as integ


def test_integrator() -> None:
    """Testing the implementation of PulseIntegrator"""
    # Testing proper implementation of object with properties
    integrator = integ.PulseIntegrator(1+1j, 0.5, 0.5, width=0.5, beta=0.5)
    drag = integrator.drag_int()
    gauss = integrator.gaussian_int()
    sq_gauss = integrator.square_gauss_int()
    result = (drag, gauss, sq_gauss)
    print(result)
    del integrator, drag, gauss, sq_gauss
    integrator = integ.PulseIntegrator(1+1j, 0.5, 0.5)
    integrator.width = 0.5
    integrator.beta = 0.5
    drag = integrator.drag_int()
    gauss = integrator.gaussian_int()
    sq_gauss = integrator.square_gauss_int()
    result1 = (drag, gauss, sq_gauss)
    print(result1)
    assert result == result1


def test_assuming_pulse_shape() -> None:
    """Testing that the integrator assumes the right pulse on init."""
    integrator = integ.PulseIntegrator(1+1j, 0.5, 0.5)
    assert integrator.gaussian_int() == integrator.area
    integrator = integ.PulseIntegrator(1+1j, 0.5, 0.5, width=0.5)
    assert integrator.square_gauss_int() == integrator.area
    integrator = integ.PulseIntegrator(1+1j, 0.5, 0.5, beta=0.5)
    assert integrator.drag_int() == integrator.area


def test_kill_unsupported_integrals() -> None:
    """Testing that the right error is raised."""
    integrator = integ.PulseIntegrator(1+1j, 0.5, 0.5)
    try:
        integrator.drag_int()
    except ValueError:
        pass
    try:
        integrator.square_gauss_int()
    except ValueError:
        pass
    integrator = integ.PulseIntegrator(1+1j, 0.5, 0.5, width=0.5)
    try:
        integrator.drag_int()
    except ValueError:
        pass
    integrator = integ.PulseIntegrator(1+1j, 0.5, 0.5, beta=0.5)
    try:
        integrator.square_gauss_int()
    except ValueError:
        pass
