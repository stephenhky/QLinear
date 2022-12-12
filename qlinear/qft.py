
from math import pi

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def qft_gate(nbdigits):
    qr = QuantumRegister(nbdigits, 'qr')
    circuit = QuantumCircuit(qr)
    for i in range(nbdigits):
        circuit.h(qr[i])
        for j in range(i+1, nbdigits):
            circuit.cp(2*pi/2**(j-i+1), j, i)
    return circuit.to_gate()
