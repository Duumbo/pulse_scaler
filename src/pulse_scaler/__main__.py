#!/usr/bin/env python
# -*- coding-UFT-8 -*-
"""
Script __main__.

Generates images of scaled circuit represented as qiskit.pulse.Schedule
"""
import qiskit as qs
import matplotlib.pyplot as plt
from pulse_scaler.one_qubit_scaling import one_qubit_scaler
import pulse_scaler.load_ibmq as cons


def scale_simple_circuit() -> None:
    """
    # scale_simple_circuit.

    Function that scale a simple one qubit circuit and compares the
    schedule to the scaled schedule.
    """
    # Create quantum circuit.
    qreg, creg = qs.QuantumRegister(1), qs.ClassicalRegister(1)
    q_c = qs.QuantumCircuit(qreg, creg)
    q_c.x(qreg)
    trans_qc = qs.compiler.transpile(q_c,
                                     cons.IBMQBACKEND,
                                     optimization_level=0)
    # Transpile to the backend.
    # Convert to schedule.
    qc_sched = qs.schedule(trans_qc, cons.IBMQBACKEND)
    scaled_qc = one_qubit_scaler(qc_sched, 2)
    qc_sched += cons.MEAS_SCHED << qc_sched.duration
    job = qs.execute(
        qc_sched,
        cons.BACKEND,
        meas_return='avg',
        seed_simulator=cons.SEED,
        seed_transpiler=cons.SEED,
        shots=10000
    )
    qs.tools.job_monitor(job)
    sim_result = job.result()
    # Scale the schedule.
    job = qs.execute(
        scaled_qc,
        cons.BACKEND,
        meas_return='avg',
        seed_simulator=cons.SEED,
        seed_transpiler=cons.SEED,
        shots=10000
    )
    qs.tools.job_monitor(job)
    scaled_sim_result = job.result()
    print(sim_result.get_counts(), scaled_sim_result.get_counts())
    # Generate the images.
    qc_sched.draw()
    plt.tight_layout()
    plt.savefig("Images/scale_simple_circuit_non_scaled.png")
    plt.clf()
    scaled_qc.draw()
    plt.tight_layout()
    plt.savefig("Images/scale_simple_circuit_scaled.png")


def __main__() -> None:
    scale_simple_circuit()


if __name__ == "__main__":
    __main__()
