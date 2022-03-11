#!/usr/bin/env python
# -*- coding-UFT-8 -*-
"""
# Qubit Scaling.

## Implements qubit scaling using qiskit pulse.
### Autor: Dimitri Bonanni-Surprenant
"""
import qiskit.pulse as ps
from pulse_scaler.pulse_integrator import find_pulse_amp
from pulse_scaler.backends.load_ibmq import MEAS_SCHED


def qubit_scaler(sched: ps.Schedule, scale_factor: float) -> ps.Schedule:
    """
    # Qubit Scaler.

    Scales a schedule on one qubit
    """
    # pylint: disable=too-many-locals.
    # Will fix later.

    offset = 0
    out_sched = ps.Schedule()
    for _, sub_sched in sched.children:
        tmp_sched = ps.Schedule()
        for _, instr in sub_sched.children:
            if isinstance(instr, ps.instructions.Play):
                pulse, chan = instr.pulse, instr.channel
                if isinstance(pulse, ps.Drag):
                    dur, amp, sig, beta = (pulse.duration, pulse.amp,
                                           pulse.sigma, pulse.beta)
                    amp = find_pulse_amp(
                        "Drag", dur, amp, sig, scale_factor, beta=beta
                    )
                    new_pulse = ps.Drag(
                        dur * scale_factor,
                        amp, sig * scale_factor,
                        beta * scale_factor
                    )
                elif isinstance(pulse, ps.GaussianSquare):
                    dur, amp, sig, width = (pulse.duration, pulse.amp,
                                            pulse.sigma, float(pulse.width))
                    amp = find_pulse_amp(
                        "Gaussian_Square",
                        dur, amp, sig, scale_factor, width=width
                    )
                    new_pulse = ps.GaussianSquare(
                        dur * scale_factor,
                        amp, sig * scale_factor,
                        width * scale_factor
                    )
                offset += dur * scale_factor
                instr = ps.Play(new_pulse, chan)
            tmp_sched += instr
        out_sched += tmp_sched
    out_sched += MEAS_SCHED << out_sched.stop_time

    return out_sched
