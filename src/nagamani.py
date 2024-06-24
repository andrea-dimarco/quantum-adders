from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from numpy import pi
import numpy as np
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_state_city
import qiskit.quantum_info as qi
import matplotlib.pyplot as plt

qreg_q = QuantumRegister(13, 'q')
circuit = QuantumCircuit(qreg_q)

a = "0110"
b = "0010"

if (a[3] == '1'):
    circuit.x(qreg_q[0]) # a0
if (a[2] == '1'):
    circuit.x(qreg_q[4]) # a1
if (a[1] == '1'):
    circuit.x(qreg_q[7]) # a2
if (a[0] == '1'):
    circuit.x(qreg_q[10]) # a3

if (b[3] == '1'):
    circuit.x(qreg_q[2]) # b0
if (b[2] == '1'):
    circuit.x(qreg_q[5]) # b1
if (b[1] == '1'):
    circuit.x(qreg_q[8]) # b2
if (b[0] == '1'):
    circuit.x(qreg_q[11]) # b3


#circuit.x(qreg_q[1]) # S0
#circuit.x(qreg_q[3]) # S1
#circuit.x(qreg_q[6]) # S2
#circuit.x(qreg_q[9]) # S3
#circuit.x(qreg_q[12]) # Carry


circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3], qreg_q[4], qreg_q[5], qreg_q[6], qreg_q[7], qreg_q[8], qreg_q[9], qreg_q[10], qreg_q[11], qreg_q[12])

circuit.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
circuit.cx(qreg_q[2], qreg_q[1])
circuit.ccx(qreg_q[0], qreg_q[1], qreg_q[3])
circuit.cx(qreg_q[0], qreg_q[1])

circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3], qreg_q[4], qreg_q[5], qreg_q[6], qreg_q[7], qreg_q[8], qreg_q[9], qreg_q[10], qreg_q[11], qreg_q[12])

circuit.ccx(qreg_q[3], qreg_q[5], qreg_q[6])
circuit.cx(qreg_q[5], qreg_q[3])
circuit.ccx(qreg_q[3], qreg_q[4], qreg_q[6])
circuit.cx(qreg_q[4], qreg_q[3])

circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3], qreg_q[4], qreg_q[5], qreg_q[6], qreg_q[7], qreg_q[8], qreg_q[9], qreg_q[10], qreg_q[11], qreg_q[12])

circuit.ccx(qreg_q[6], qreg_q[8], qreg_q[9])
circuit.cx(qreg_q[8], qreg_q[6])
circuit.ccx(qreg_q[6], qreg_q[7], qreg_q[9])
circuit.cx(qreg_q[7], qreg_q[6])

circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3], qreg_q[4], qreg_q[5], qreg_q[6], qreg_q[7], qreg_q[8], qreg_q[9], qreg_q[10], qreg_q[11], qreg_q[12])

circuit.ccx(qreg_q[9], qreg_q[11], qreg_q[12])
circuit.cx(qreg_q[11], qreg_q[9])
circuit.ccx(qreg_q[9], qreg_q[10], qreg_q[12])
circuit.cx(qreg_q[10], qreg_q[9])

circuit.measure_all()
# Transpile for simulator
simulator = AerSimulator()
circ = transpile(circuit, simulator)

# Run and get counts
result = simulator.run(circ).result()
#print(result)
counts = result.get_counts(circ)
value = list(counts.keys())[0]

s0 = value[-2]
s1 = value[-4]
s2 = value[-7]
s3 = value[-10]
cout = value[0]

print("Sum: ",cout,s3,s2,s1,s0)

#plot_histogram(counts, title='Bell-State counts')
#plt.show()
# # Create circuit
# circ = QuantumCircuit(2)
# circ.h(0)
# circ.cx(0, 1)
# circ.measure_all()




