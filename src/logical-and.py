from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from numpy import pi
import numpy as np
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_state_city
import qiskit.quantum_info as qi
import matplotlib.pyplot as plt


a = 1
b = 1

showCircuit = False

qreg_q = QuantumRegister(3, 'q')
circuit = QuantumCircuit(qreg_q)

if (a == 1):
    circuit.x(qreg_q[0]) # a
else:
    assert(False)
if (b == 1):
    circuit.x(qreg_q[1]) # b
else:
    assert(False)

circuit.h(qreg_q[2])
circuit.t(qreg_q[2])
circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2])
circuit.cx(qreg_q[0], qreg_q[2])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.cx(qreg_q[2], qreg_q[0])
circuit.cx(qreg_q[2], qreg_q[1])
circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2])
circuit.t(qreg_q[2])
circuit.tdg(qreg_q[0])
circuit.tdg(qreg_q[1])
circuit.cx(qreg_q[2], qreg_q[0])
circuit.cx(qreg_q[2], qreg_q[1])
circuit.h(qreg_q[2])
circuit.s(qreg_q[2])

if showCircuit:
    circuit.draw(output="mpl",filename="logical-and.jpg")
    plt.show()



circuit.measure_all()
# Transpile for simulator
simulator = AerSimulator()
circ = transpile(circuit, simulator)

# Run and get counts
result = simulator.run(circ).result()
#print(result)
counts = result.get_counts(circ)
value = list(counts.keys())[0]

logical_and = value[0]

print(a, "AND", b, "IS", logical_and)


#plot_histogram(counts, title='Bell-State counts')
#plt.show()
# # Create circuit
# circ = QuantumCircuit(2)
# circ.h(0)
# circ.cx(0, 1)
# circ.measure_all()


