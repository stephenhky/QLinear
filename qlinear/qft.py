
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
    for i in range(nbdigits // 2):
        circuit.swap(i, nbdigits-i-1)
    return circuit.to_gate()


def inv_qft_gate(nbdigits):
    qr = QuantumRegister(nbdigits, 'qr')
    circuit = QuantumCircuit(qr)
    for i in range(nbdigits // 2):
        circuit.swap(i, nbdigits-i-1)
    for i in range(nbdigits):
        circuit.h(qr[i])
        for j in range(i+1, nbdigits):
            rot_phase = - 2*pi/2**(j-i+1)
            circuit.cp(rot_phase, j, i)
    return circuit.to_gate()


def phase_estimation_circuit(gate, nbdigits, initial_momopartite_state=[0, 1]):
    # customized controlled gate
    controlled_gate = gate.control(1)
    # initial_state
    assert len(initial_momopartite_state) == 2
    assert np.linalg.norm(initial_momopartite_state) == 1
    initial_state = np.zeros(2**(nbdigits+1), dtype=np.complex_)
    initial_state[0] = initial_momopartite_state[0]
    initial_state[2**nbdigits] = initial_momopartite_state[1]

    # building the circuit
    circuit = QuantumCircuit(nbdigits + 1, nbdigits)
    circuit.initialize(initial_state)
    circuit.h(range(nbdigits))
    for i in range(nbdigits):
        for _ in range(2 ** (i)):
            circuit.append(controlled_gate, [i, nbdigits])
            # circuit.cp(2*pi*theta, i, nbdigits)
    circuit.append(inv_qft_gate(nbdigits), range(nbdigits))
    circuit.measure(range(nbdigits), range(nbdigits))

    return circuit

