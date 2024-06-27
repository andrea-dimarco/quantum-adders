from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from numpy import pi
import numpy as np
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_state_city
import qiskit.quantum_info as qi
import matplotlib.pyplot as plt


first_addend = 5
second_addend = 20


qasm = """
OPENQASM 2.0;
include "qelib1.inc";
gate ketT a {
  h a;
  t a;
}
gate lAND a, b, c {
  cx a, c;
  cx b, c;
  cx c, a;
  cx c, b;
  barrier a;
  t c;
  tdg a;
  tdg b;
  cx c, b;
  cx c, a;
  h c;
  s c;
}
gate rAND a, b, c {
  s c;
  h c;
  cx c, b;
  cx c, a;
  tdg b;
  t c;
  tdg a;
  cx c, b;
  cx c, a;
  cx b, c;
  cx a, c;
}

qreg q[14];

"""

a = f'{first_addend:05b}'
b = f'{second_addend:05b}'

if (a[4] == '1'):
    qasm += "x q[0];\n" # a0
if (a[3] == '1'):
    qasm += "x q[3];\n" # a1
if (a[2] == '1'):
    qasm += "x q[6];\n" # a2
if (a[1] == '1'):
    qasm += "x q[9];\n" # a3
if (a[0] == '1'):
    qasm += "x q[12];\n" # a4

if (b[4] == '1'):
    qasm += "x q[1];\n" # b0
if (b[3] == '1'):
    qasm += "x q[4];\n" # b1
if (b[2] == '1'):
    qasm += "x q[7];\n" # b2
if (b[1] == '1'):
    qasm += "x q[10];\n" # b3
if (b[0] == '1'):
    qasm += "x q[13];\n" # b4


qasm += """
ketT q[2];
ketT q[5];
ketT q[8];
ketT q[11];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13];
lAND q[0], q[1], q[2];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13];
cx q[2], q[3];
cx q[2], q[4];
lAND q[3], q[4], q[5];
cx q[2], q[5];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13];
cx q[5], q[6];
cx q[5], q[7];
lAND q[6], q[7], q[8];
cx q[5], q[8];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13];
cx q[8], q[9];
cx q[8], q[10];
lAND q[9], q[10], q[11];
cx q[8], q[11];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13];
cx q[11], q[13];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13];
cx q[8], q[11];
rAND q[9], q[10], q[11];
cx q[8], q[9];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13];
cx q[5], q[8];
rAND q[6], q[7], q[8];
cx q[5], q[6];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13];
cx q[2], q[5];
rAND q[3], q[4], q[5];
cx q[2], q[3];
rAND q[0], q[1], q[2];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13];
cx q[0], q[1];
cx q[3], q[4];
cx q[6], q[7];
cx q[9], q[10];
cx q[12], q[13];

"""
circuit = QuantumCircuit.from_qasm_str(qasm)

showCircuit = False
if showCircuit:
    circuit.draw(output="mpl",filename="gidney-rev.jpg")
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

s0 = value[12]
s1 = value[9]
s2 = value[6]
s3 = value[3]
s4 = value[0]

print(first_addend, "+", second_addend, "=", int(str(s4)+str(s3)+str(s2)+str(s1)+str(s0),2))

#plot_histogram(counts, title='Bell-State counts')
#plt.show()
# # Create circuit
# circ = QuantumCircuit(2)
# circ.h(0)
# circ.cx(0, 1)
# circ.measure_all()

