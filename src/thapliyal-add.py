from qiskit import QuantumCircuit, transpile
from numpy import pi
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_state_city
import matplotlib.pyplot as plt

showCircuit = False
first_addend = 18
second_addend = 2


a = f'{first_addend:05b}'
b = f'{second_addend:05b}'



qasm = """
OPENQASM 2.0;
include "qelib1.inc";
gate pG a, b, c {
  h c;
  barrier a, b, c;
  tdg c;
  tdg b;
  tdg a;
  cx b, a;
  cx a, c;
  cx c, b;
  barrier a, b, c;
  tdg c;
  t a;
  t b;
  cx a, b;
  t b;
  barrier a, b, c;
  cx a, c;
  cx c, b;
  h c;
}
qreg q[11];
"""

if (a[4] == '1'):
    qasm += "x q[1];\n" # a0
if (a[3] == '1'):
    qasm += "x q[3];\n" # a1
if (a[2] == '1'):
    qasm += "x q[5];\n" # a2
if (a[1] == '1'):
    qasm += "x q[7];\n" # a3
if (a[0] == '1'):
    qasm += "x q[9];\n" # a4

if (b[4] == '1'):
    qasm += "x q[0];\n" # b0
if (b[3] == '1'):
    qasm += "x q[2];\n" # b1
if (b[2] == '1'):
    qasm += "x q[4];\n" # b2
if (b[1] == '1'):
    qasm += "x q[6];\n" # b3
if (b[0] == '1'):
    qasm += "x q[8];\n" # b4


qasm +="""

cx q[9], q[8];
cx q[3], q[2];
cx q[5], q[4];
cx q[7], q[6];
cx q[9], q[10];
cx q[7], q[9];
cx q[5], q[7];
cx q[3], q[5];
ccx q[1], q[0], q[3];
ccx q[3], q[2], q[5];
ccx q[5], q[4], q[7];
ccx q[7], q[6], q[9];
pG q[8], q[9], q[10];
pG q[6], q[7], q[9];
pG q[4], q[5], q[7];
pG q[2], q[3], q[5];
pG q[0], q[1], q[3];
cx q[3], q[5];
cx q[5], q[7];
cx q[7], q[9];
barrier q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10];
cx q[9], q[8];
cx q[3], q[2];
cx q[7], q[6];
cx q[5], q[4];

"""
circuit = QuantumCircuit.from_qasm_str(qasm)
if showCircuit:
    circuit.draw(output="mpl",filename="thapliyal-add.jpg")
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

s0 = value[-1]
s1 = value[-3]
s2 = value[-5]
s3 = value[-7]
s4 = value[-9]
cout = value[0]
print(first_addend, "+", second_addend, "=", int(str(cout)+str(s4) + str(s3)+str(s2)+str(s1)+str(s0),2))


