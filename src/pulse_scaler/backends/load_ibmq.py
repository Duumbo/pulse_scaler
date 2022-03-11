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
import numpy as np
SEED = 67934


class NoiseLessBackend(fake_pulse_backend.FakePulseBackend):  # type: ignore
    """A fake 1 qubit backend with a low noise as possible."""

    np.random.seed(SEED)

    dirname = os.path.dirname(__file__)
    conf_filename = "noise_less/conf.json"
    props_filename = "noise_less/props.json"
    defs_filename = "noise_less/defs.json"
    backend_name = "noiseless_sim"

    def __init__(self) -> None:
        """Noiseless Backend."""
        super().__init__()
        self.std = 0.0


class NoiseBackend(fake_pulse_backend.FakePulseBackend):  # type: ignore
    """A fake 1 qubit backend with a low noise as possible."""

    np.random.seed(SEED)

    dirname = os.path.dirname(__file__)
    conf_filename = "base_noise/conf.json"
    props_filename = "base_noise/props.json"
    defs_filename = "base_noise/defs.json"
    backend_name = "noise_sim"

    def __init__(self, scale_factor: int) -> None:
        """Initialize as Noisy fake backend."""
        _ = scale_factor
        super().__init__()


SHOTS = 10_000
BASIS = ['id', 'rx', 'sx', 'x', 'cx']
provider = qs.IBMQ.get_provider(hub="ibm-q-sherbrooke",
                                group="udes", project="eibmq-iq")
IBMQBACKEND = provider.get_backend("ibmq_jakarta")
backend = IBMQBACKEND
FREQ_EST = 4.97e9
DRIVE_EST = 6.35e7
backen_config = backend.configuration()
defaults = backend.defaults()
armonk_model = PulseSystemModel.from_backend(backend)
CALIBRATION = defaults.instruction_schedule_map
CONFIG = backen_config
MEAS_SCHED = CALIBRATION.get('measure', range(CONFIG.n_qubits))
BACKEND = PulseSimulator.from_backend(backend)
