#!/usr/bin/env python
# -*- codind-UFT-8 -*-
"""
# Constant module.

Defines many usefull constants.
- SEED: transpiler and simulator seed.
- BASIS: basis gate set.
- IBMQBACKEND: Backend of the chosen ibmq system.
- BACKEND: Pulse simulator backend.
- CONFIG: IbmqBackend configuration at the current time.
- MEAS_SCHED: Measure schedule defined in configuration.
- CALIBRATION: Calibration defined by the IBMq system.
"""
import qiskit as qs
from qiskit.providers.aer import PulseSimulator
from qiskit.providers.aer.pulse import PulseSystemModel
from qiskit.test.mock import FakeArmonk
import numpy as np

SEED = 6793428708
SHOTS = 10_000
BASIS = ['id', 'rx', 'sx', 'x']
provider = qs.IBMQ.get_provider(hub="ibm-q-sherbrooke",
                                group="udes", project="eibmq-iq")
IBMQBACKEND = provider.get_backend("ibmq_armonk")
backend = FakeArmonk()
FREQ_EST = 4.97e9
DRIVE_EST = 6.35e7
backend.defaults().qubit_freq_est = [FREQ_EST]
backen_config = backend.configuration()
backen_config.hamiltonian['h_str'] = ['wq0*0.5*(I0-Z0)', 'omegad0*X0||D0']
backen_config.hamiltonian['vars'] = {
    'wq0': 2 * np.pi * FREQ_EST,
    'omegad0': DRIVE_EST
}
backen_config.hamiltonian['qub'] = {'0': 2}
backen_config.dt = 2.2222222222222221e-10
defaults = backend.defaults()
armonk_model = PulseSystemModel.from_backend(backend)
CALIBRATION = defaults.instruction_schedule_map
CONFIG = backen_config
MEAS_SCHED = CALIBRATION.get('measure', range(CONFIG.n_qubits))
BACKEND = PulseSimulator.from_backend(backend)
print(BACKEND.properties().gate_error('x', 0))
