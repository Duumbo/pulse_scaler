#!/usr/bin/env python
# -*- coding-UFT-8 -*-
"""
# One Qubit Scaling.

## Implements single qubit scaling using qiskit pulse.
### Autor: Dimitri Bonanni-Surprenant
"""
import qiskit.pulse as ps
from pulse_scaler.pulse_integrator import find_pulse_amp
from pulse_scaler.backends.load_ibmq import MEAS_SCHED


def one_qubit_scaler(sched: ps.Schedule, scale_factor: float) -> ps.Schedule:
    """
    # One Qubit Scaler.

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
                dur, amp, sig, beta = (pulse.duration, pulse.amp,
                                       pulse.sigma, pulse.beta)
                amp = find_pulse_amp("Drag", dur, amp, sig, beta, scale_factor)
                new_pulse = ps.Drag(
                    dur * scale_factor,
                    amp, sig * scale_factor,
                    beta * scale_factor
                )
                offset += dur * scale_factor
                instr = ps.Play(new_pulse, chan)
            tmp_sched += instr
        out_sched += tmp_sched
    out_sched += MEAS_SCHED << offset

    return out_sched
