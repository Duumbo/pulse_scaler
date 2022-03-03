#!/usr/bin/env python
# -*- coding-UFT-8 -*-
"""
# One Qubit Scaling.

## Implements single qubit scaling using qiskit pulse.
### Autor: Dimitri Bonanni-Surprenant
"""
import qiskit.pulse as ps
from pulse_scaler.pulse_integrator import find_pulse_amp


def one_qubit_scaler(sched: ps.Schedule) -> ps.Schedule:
    """
    # One Qubit Scaler.

    Scales a schedule on one qubit
    """
    offset = 0
    ancien_offset = 0
    out_sched = ps.Schedule()
    for _, sub_sched in sched.children:
        tmp_sched = ps.Schedule()
        for _, instr in sub_sched.children:
            if isinstance(instr, ps.instructions.Play):
                pulse, chan = instr.pulse, instr.channel
                dur, amp, sig, beta = (pulse.duration, pulse.amp,
                                       pulse.sigma, pulse.beta)
                amp = find_pulse_amp("Drag", dur, amp, sig, beta, 2)
                new_pulse = ps.Drag(dur * 2, amp, sig * 2, beta * 2)
                ancien_offset = offset
                offset += dur * 2
                instr = ps.Play(new_pulse, chan)
            tmp_sched += instr << ancien_offset
        out_sched += tmp_sched

    return out_sched
