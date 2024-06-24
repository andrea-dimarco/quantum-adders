from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from numpy import pi
import numpy as np
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_state_city
import qiskit.quantum_info as qi
import matplotlib.pyplot as plt

qasm = """
OPENQASM 2.0;
include "qelib1.inc";
gate lAND a, b, c {
  t c;
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

qreg q[14];
creg c[1];
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
barrier q[9], q[10], q[11];
h q[11];
measure q[11] -> c[0];
barrier q[9], q[10], q[11];
if (c == 0) cz q[9], q[10];
cx q[8], q[9];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13];
cx q[5], q[8];
barrier q[6], q[7], q[8];
h q[8];
measure q[8] -> c[0];
barrier q[6], q[7], q[8];
if (c == 0) cz q[6], q[7];
cx q[5], q[6];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13];
cx q[2], q[5];
barrier q[3], q[4], q[5];
h q[5];
measure q[5] -> c[0];
barrier q[3], q[4], q[5];
if (c == 0) cz q[3], q[4];
cx q[2], q[3];
barrier q[1], q[2], q[3];
h q[3];
measure q[3] -> c[0];
barrier q[1], q[2], q[3];
if (c == 0) cz q[1], q[2];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13];
cx q[0], q[1];
cx q[3], q[4];
cx q[6], q[7];
cx q[9], q[10];
cx q[12], q[13];

"""
circuit = QuantumCircuit.from_qasm_str(qasm)

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
#cout = value[0]

print("Sum: ", s4, s3, s2, s1, s0)

#plot_histogram(counts, title='Bell-State counts')
#plt.show()
# # Create circuit
# circ = QuantumCircuit(2)
# circ.h(0)
# circ.cx(0, 1)
# circ.measure_all()

