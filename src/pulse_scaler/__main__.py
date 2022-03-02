#!/usr/bin/env python
# -*- coding-UFT-8 -*-
"""
Script __main__.

Generates images of scaled circuit represented as qiskit.pulse.Schedule
"""
import qiskit as qs
import matplotlib.pyplot as plt
from pulse_scaler.one_qubit_scaling import one_qubit_scaler

qs.IBMQ.load_account()
provider = qs.IBMQ.get_provider(hub="ibm-q-sherbrooke",
                                group="udes", project="eibmq-iq")
IBMQBACKEND = provider.get_backend("ibmq_lima")
BACKEND = qs.Aer.get_backend("aer_simulator")


def scale_simple_circuit():
    """
    # scale_simple_circuit.

    Function that scale a simple one qubit circuit and compares the
    schedule to the scaled schedule.
    """
    # Create quantum circuit.
    qreg, creg = qs.QuantumRegister(1), qs.ClassicalRegister(1)
    q_c = qs.QuantumCircuit(qreg, creg)
    q_c.h(qreg)
    # Transpile to the backend.
    trans_qc = qs.compiler.transpile(q_c, IBMQBACKEND, optimization_level=3)
    # Convert to schedule.
    qc_sched = qs.schedule(trans_qc, IBMQBACKEND)
    # Scale the schedule.
    scaled_qc = one_qubit_scaler(qc_sched)
    # Generate the images.
    qc_sched.draw()
    plt.tight_layout()
    plt.savefig("Images/scale_simple_circuit_non_scaled.png")
    plt.clf()
    scaled_qc.draw()
    plt.tight_layout()
    plt.savefig("Images/scale_simple_circuit_scaled.png")


def __main__():
    scale_simple_circuit()


if __name__ == "__main__":
    __main__()
