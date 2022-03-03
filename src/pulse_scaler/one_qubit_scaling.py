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
    meas_sched = ps.Schedule()
    d0 = ps.MeasureChannel(0)
    mem0 = ps.MemorySlot(1)
    precise_amp = 0.3051214347689275+0.1714669357180885j
    meas_pulse = ps.GaussianSquare(duration=22400,
                                   amp=precise_amp,
                                   sigma=64,
                                   width=22144,
                                   name='M_m0')
    meas_sched += ps.Acquire(22400, d0, mem0)
    meas_sched += ps.Play(meas_pulse, d0, name='M_m0')
    out_sched += meas_sched << offset

    return out_sched
