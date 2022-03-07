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
import os
import qiskit as qs
from qiskit.providers.aer import PulseSimulator
from qiskit.providers.aer.pulse import PulseSystemModel
from qiskit.test.mock import fake_pulse_backend


class NoiseLessBackend(fake_pulse_backend.FakePulseBackend):  # type: ignore
    """A fake 1 qubit backend with a low noise as possible."""

    dirname = os.path.dirname(__file__)
    conf_filename = "conf.json"
    props_filename = "props.json"
    defs_filename = "defs.json"
    backend_name = "noiseless_sim"


SEED = 6793428708
SHOTS = 10_000
BASIS = ['id', 'rx', 'sx', 'x']
provider = qs.IBMQ.get_provider(hub="ibm-q-sherbrooke",
                                group="udes", project="eibmq-iq")
IBMQBACKEND = provider.get_backend("ibmq_armonk")
backend = NoiseLessBackend()
FREQ_EST = 4.97e9
DRIVE_EST = 6.35e7
backend.defaults().qubit_freq_est = [FREQ_EST]
backen_config = backend.configuration()
defaults = backend.defaults()
armonk_model = PulseSystemModel.from_backend(backend)
CALIBRATION = defaults.instruction_schedule_map
CONFIG = backen_config
MEAS_SCHED = CALIBRATION.get('measure', range(CONFIG.n_qubits))
BACKEND = PulseSimulator.from_backend(backend)
