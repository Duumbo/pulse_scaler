#!/usr/bin/env python
# -*- coding-UFT-8 -*-
"""Test related to the scaling of a circuit."""
import math
import qiskit as qs
from pulse_scaler.backends import load_ibmq as cons
from pulse_scaler.one_qubit_scaling import one_qubit_scaler


def test_single_h() -> None:
    """Tests implementation of scaled circuit vs unscaled on no_noise_sim."""
    qreg = qs.QuantumRegister(1)
    creg = qs.ClassicalRegister(1)
    q_c = qs.QuantumCircuit(qreg, creg)
    q_c.h(qreg)
    trans_qc = qs.compiler.transpile(q_c,
                                     cons.BACKEND,
                                     optimization_level=0)
    qc_sched = qs.schedule(trans_qc, cons.BACKEND)
    scaled_qc = one_qubit_scaler(qc_sched, 2)
    qc_sched += cons.MEAS_SCHED << qc_sched.duration
    job = qs.execute(
        qc_sched,
        cons.BACKEND,
        meas_return='avg',
        seed_simulator=cons.SEED,
        seed_transpiler=cons.SEED,
        shots=cons.SHOTS
    )
    qs.tools.job_monitor(job)
    sim_result = job.result()
    job = qs.execute(
        scaled_qc,
        cons.BACKEND,
        meas_return='avg',
        seed_simulator=cons.SEED,
        seed_transpiler=cons.SEED,
        shots=cons.SHOTS
    )
    qs.tools.job_monitor(job)
    scaled_sim_result = job.result()
    exp_val_norm = sim_result.get_counts()["1"] / cons.SHOTS
    exp_val_scaled = scaled_sim_result.get_counts()["1"] / cons.SHOTS
    print(exp_val_norm, exp_val_scaled)
    assert math.isclose(exp_val_norm, exp_val_scaled, rel_tol=0.1)


def test_regular_noiseless_circuit() -> None:
    """Test implementation of schedule simulation vs gate simulation."""
    qreg = qs.QuantumRegister(1)
    creg = qs.ClassicalRegister(1)
    q_c = qs.QuantumCircuit(qreg, creg)
    q_c.h(qreg)
    trans_qc = qs.compiler.transpile(q_c,
                                     cons.BACKEND,
                                     optimization_level=0)
    qc_sched = qs.schedule(trans_qc, cons.BACKEND)
    qc_sched += cons.MEAS_SCHED << qc_sched.duration
    job = qs.execute(
        qc_sched,
        cons.BACKEND,
        meas_return='avg',
        seed_simulator=cons.SEED,
        seed_transpiler=cons.SEED,
        shots=cons.SHOTS
    )
    qs.tools.job_monitor(job)
    sim_result = job.result()
    del q_c, qreg, creg
    qreg = qs.QuantumRegister(1)
    creg = qs.ClassicalRegister(1)
    q_c = qs.QuantumCircuit(qreg, creg)
    q_c.h(qreg)
    q_c.measure_all()
    trans_qc = qs.compiler.transpile(q_c,
                                     cons.IBMQBACKEND,
                                     optimization_level=0)
    backend = qs.Aer.get_backend("aer_simulator")
    job = qs.execute(q_c, backend, shots=cons.SHOTS)
    qs.tools.job_monitor(job)
    norm_result = job.result()
    exp_val_norm = norm_result.get_counts()["1 0"] / cons.SHOTS
    exp_val_sched = sim_result.get_counts()["1"] / cons.SHOTS
    print(exp_val_norm, exp_val_sched)
    assert math.isclose(exp_val_norm, exp_val_sched, rel_tol=0.1)
