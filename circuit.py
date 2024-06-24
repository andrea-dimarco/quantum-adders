from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from numpy import pi

qreg_q = QuantumRegister(13, 'q')

circuit = QuantumCircuit(qreg_q)

circuit.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
circuit.cx(qreg_q[2], qreg_q[1])
circuit.ccx(qreg_q[0], qreg_q[1], qreg_q[3])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.ccx(qreg_q[3], qreg_q[5], qreg_q[6])
circuit.cx(qreg_q[5], qreg_q[3])
circuit.ccx(qreg_q[3], qreg_q[4], qreg_q[6])
circuit.ccx(qreg_q[6], qreg_q[8], qreg_q[9])
circuit.cx(qreg_q[8], qreg_q[6])
circuit.ccx(qreg_q[6], qreg_q[7], qreg_q[9])
circuit.cx(qreg_q[7], qreg_q[6])
circuit.cx(qreg_q[4], qreg_q[3])
circuit.ccx(qreg_q[9], qreg_q[11], qreg_q[12])
circuit.cx(qreg_q[11], qreg_q[9])
circuit.ccx(qreg_q[9], qreg_q[10], qreg_q[12])
circuit.cx(qreg_q[10], qreg_q[9])