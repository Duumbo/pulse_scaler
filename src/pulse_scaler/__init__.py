"""
# Pulse Scaler.

Module that scales circuit as qiskit.Schedule by stretching them
while keeping the area under the curve that defines the pulse constant.
"""
import qiskit as qs
qs.IBMQ.load_account()
