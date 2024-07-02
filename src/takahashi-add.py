from qiskit import QuantumRegister, QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_state_city
import qiskit.quantum_info as qi
import matplotlib.pyplot as plt

showCircuit = True
first_addend = 16
second_addend = 2

qreg_q0 = QuantumRegister(11, 'q0')
circuit = QuantumCircuit(qreg_q0)


a = f'{first_addend:05b}'
b = f'{second_addend:05b}'


if (a[4] == '1'):
    circuit.x(qreg_q0[1]) #a0
if (a[3] == '1'):
    circuit.x(qreg_q0[3]) #a1
if (a[2] == '1'):
    circuit.x(qreg_q0[5]) #a2
if (a[1] == '1'):
    circuit.x(qreg_q0[7]) #a3
if (a[0] == '1'):
    circuit.x(qreg_q0[9]) #a4

if (b[4] == '1'):
    circuit.x(qreg_q0[0]) # b0
if (b[3] == '1'):
    circuit.x(qreg_q0[2]) # b0
if (b[2] == '1'):
    circuit.x(qreg_q0[4]) # b1
if (b[1] == '1'):
    circuit.x(qreg_q0[6]) # b2
if (b[0] == '1'):
    circuit.x(qreg_q0[8]) # b3


circuit.cx(qreg_q0[9], qreg_q0[8])
circuit.cx(qreg_q0[3], qreg_q0[2])
circuit.cx(qreg_q0[5], qreg_q0[4])
circuit.cx(qreg_q0[7], qreg_q0[6])
circuit.cx(qreg_q0[9], qreg_q0[10])
circuit.cx(qreg_q0[7], qreg_q0[9])
circuit.cx(qreg_q0[5], qreg_q0[7])
circuit.cx(qreg_q0[3], qreg_q0[5])
circuit.ccx(qreg_q0[0], qreg_q0[1], qreg_q0[3])
circuit.ccx(qreg_q0[2], qreg_q0[3], qreg_q0[5])
circuit.ccx(qreg_q0[4], qreg_q0[5], qreg_q0[7])
circuit.ccx(qreg_q0[6], qreg_q0[7], qreg_q0[9])
circuit.ccx(qreg_q0[8], qreg_q0[9], qreg_q0[10])
circuit.cx(qreg_q0[9], qreg_q0[8])
circuit.ccx(qreg_q0[6], qreg_q0[7], qreg_q0[9])
circuit.cx(qreg_q0[7], qreg_q0[6])
circuit.ccx(qreg_q0[4], qreg_q0[5], qreg_q0[7])
circuit.cx(qreg_q0[5], qreg_q0[4])
circuit.ccx(qreg_q0[2], qreg_q0[3], qreg_q0[5])
circuit.cx(qreg_q0[3], qreg_q0[2])
circuit.ccx(qreg_q0[0], qreg_q0[1], qreg_q0[3])
circuit.cx(qreg_q0[3], qreg_q0[5])
circuit.cx(qreg_q0[5], qreg_q0[7])
circuit.cx(qreg_q0[7], qreg_q0[9])
circuit.barrier(qreg_q0[0], qreg_q0[1], qreg_q0[2], qreg_q0[3], qreg_q0[4], qreg_q0[5], qreg_q0[6], qreg_q0[7], qreg_q0[8], qreg_q0[9], qreg_q0[10])
circuit.cx(qreg_q0[1], qreg_q0[0])
circuit.cx(qreg_q0[3], qreg_q0[2])
circuit.cx(qreg_q0[5], qreg_q0[4])
circuit.cx(qreg_q0[7], qreg_q0[6])
circuit.cx(qreg_q0[9], qreg_q0[8])

if showCircuit:
    circuit.draw(output="mpl",filename="takahashi-add.jpg")
    plt.show()

circuit.measure_all()

# Transpile for simulator
simulator = AerSimulator()
circ = transpile(circuit, simulator)

# Run and get counts
result = simulator.run(circ).result()
counts = result.get_counts(circ)
value = list(counts.keys())[0]

s0 = value[-1]
s1 = value[-3]
s2 = value[-5]
s3 = value[-7]
s4 = value[-9]
cout = value[0]
print(first_addend, "+", second_addend, "=", int(str(cout)+str(s4) + str(s3)+str(s2)+str(s1)+str(s0),2))


