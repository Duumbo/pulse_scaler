#!/usr/bin/env python
# -*- coding-UFT-8 -*-
"""
Script __main__.

Generates images of scaled circuit represented as qiskit.pulse.Schedule
"""
import qiskit as qs
import matplotlib.pyplot as plt
from pulse_scaler.qubit_scaling import qubit_scaler
import pulse_scaler.backends.load_ibmq as cons
import pulse_scaler.extrapolation as ex


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
    q_c.x(qreg)
    trans_qc = qs.compiler.transpile(q_c,
                                     cons.IBMQBACKEND,
                                     optimization_level=0)
    # Transpile to the backend.
    # Convert to schedule.
    qc_sched = qs.schedule(trans_qc, cons.IBMQBACKEND)
    scaled_qc = qubit_scaler(qc_sched, 2)
    qc_sched += cons.MEAS_SCHED << qc_sched.duration
    job = cons.IBMQBACKEND.run(
        qc_sched,
        meas_return='avg',
        seed_simulator=cons.SEED,
        shots=cons.SHOTS
    )
    qs.tools.job_monitor(job)
    sim_result = job.result()
    # Scale the schedule.
    job = cons.IBMQBACKEND.run(
        scaled_qc,
        meas_return='avg',
        seed_simulator=cons.SEED,
        shots=cons.SHOTS
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


def mitigate_simple_circuit() -> None:
    """Mitigates a simple circuit with specified extrapolation technique."""
    # Create quantum circuit.
    qreg, creg = qs.QuantumRegister(2), qs.ClassicalRegister(2)
    q_c = qs.QuantumCircuit(qreg, creg)
    q_c.h(0)
    q_c.cx(0, 1)
    trans_qc = qs.compiler.transpile(q_c,
                                     cons.IBMQBACKEND,
                                     optimization_level=3)
    qc_sched = qs.schedule(trans_qc, cons.IBMQBACKEND)
    scaled_qc1 = qubit_scaler(qc_sched, 2)
    scaled_qc2 = qubit_scaler(qc_sched, 3)
    scaled_qc3 = qubit_scaler(qc_sched, 4)
    scaled_qc4 = qubit_scaler(qc_sched, 5)
    qc_sched += cons.MEAS_SCHED << qc_sched.duration
    to_run = [
        qc_sched,
        scaled_qc1,
        scaled_qc2,
        scaled_qc3,
        scaled_qc4
    ]
    expvals = []
    for circ in to_run:
        job = cons.IBMQBACKEND.run(
            circ,
            meas_return='avg',
            seed_simulator=cons.SEED,
            seed_transpiler=cons.SEED,
            shots=cons.SHOTS
        )
        qs.tools.job_monitor(job)
        sim_result = job.result()
        try:
            print(sim_result.get_counts())
            expvals.append(sim_result.get_counts()["0000001"] / cons.SHOTS)
        except KeyError:
            expvals.append(sim_result.get_counts()["01 00"] / cons.SHOTS)
    print(ex.rich_extr(expvals, [1, 2, 3]))


def looking_at_schedules() -> None:
    """Just peeking."""
    qreg, creg = qs.QuantumRegister(2), qs.ClassicalRegister(2)
    q_c = qs.QuantumCircuit(qreg, creg)
    q_c.cx(0, 1)
    trans_qc = qs.compiler.transpile(q_c,
                                     cons.IBMQBACKEND,
                                     optimization_level=0)
    qc_sched = qs.schedule(trans_qc, cons.IBMQBACKEND)
    qc_sched.draw()
    plt.savefig("Images/multi-qubit-sched.png")
    plt.clf()
    qc_sched = qubit_scaler(qc_sched, 2)
    qc_sched.draw()
    plt.savefig("Images/multi-qubit-sched-scaled.png")


def __main__() -> None:
    # scale_simple_circuit()
    mitigate_simple_circuit()
    # looking_at_schedules()


if __name__ == "__main__":
    __main__()
