from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from numpy import pi
import numpy as np
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_state_city
import qiskit.quantum_info as qi
import matplotlib.pyplot as plt

def createCircuit(ai,bi,nbits):
    a = f'{ai:0{nbits}b}'
    b = f'{bi:0{nbits}b}'
    numlines = nbits * 3-1

    # barrier string
    barrier = "barrier "
    for i in range(numlines):
        if i == numlines-1: 
            barrier += f"q[{i}];"
        else:
            barrier += f"q[{i}],"

    qasm = qasm = """
    OPENQASM 2.0;
    include "qelib1.inc";

    gate sT a {
    h a;
    t a;
    }
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
    creg c[1];
    """

    # create registers
    init_registers = f"""
    qreg q[{numlines}];
    """
    qasm +=init_registers

    # initialize registers 

    # set addends values 
    # first addend
    for i in range(nbits):
        if a[nbits-1-i] == "1":
            index = 3 * i
            qasm += f"x q[{index}];"

    # second addend
    for i in range(nbits):
        if b[nbits-1-i] =="1":
            index = 3 * i + 1
            qasm += f"x q[{index}];"

    # insert ket T
    for i in range(nbits-1):
        qasm += f"ketT q[{2+ 3* i}];"
    qasm +=barrier

    # insert initial lAND portion
    qasm += "lAND q[0], q[1], q[2];"
    qasm +=barrier

    # insert rest of initial lAND modules
    for i in range(0,nbits-2):
        qasm += f"cx q[{2 + 3*i}], q[{3 + 3*i}];"
        qasm += f"cx q[{2 + 3*i}], q[{4 + 3*i}];"
        qasm += f"lAND q[{3*(i+1)}], q[{3*(i+1) + 1}], q[{3*(i+1) +2}];"
        qasm += f"cx q[{2 + 3 * i}], q[{2 + 3 * (i+1)}];"
        qasm +=barrier

    # insert sole cnot MAYBE WRONG
    qasm += f"cx q[{(nbits-1) * 3 - 1}], q[{(nbits-1) * 3 + 1}];"
    qasm +=barrier

    # start of reverse lAND modules (cx, h, measure,cz,cx)
    for i in range(nbits-3,-1,-1):
        ind1 =2 + 3 * i
        ind2 =2 + 3 * (i+1)
        #print(ind1,ind2)
        qasm += f"cx q[{ind1}], q[{ind2}];"
        qasm += f"barrier q[{ind2-2}], q[{ind2-1}], q[{ind2}];"
        qasm += f"h q[{ind2}];"
        qasm += f"measure q[{ind2}] -> c[0];"
        qasm += f"barrier q[{ind2-2}], q[{ind2-1}], q[{ind2}];"
        qasm += f"if (c == 0) cz q[{ind1+1}], q[{ind2-1}];"
        #qasm += f"lAND q[{3*(i+1)}], q[{3*(i+1) + 1}], q[{3*(i+1) +2}];"
        qasm += f"cx q[{ind1}], q[{ind1+1}];"
        qasm +=barrier

    # last reverse lAND 
    qasm += f"barrier q[0], q[1], q[2];"
    qasm += "h q[2];"
    qasm += "measure q[2] -> c[0];"
    qasm += f"barrier q[0], q[1], q[2];"
    qasm += "if (c == 0) cz q[0], q[1];"
    qasm +=barrier
    # last cnot group
    for i in range(nbits):
        qasm+= f"cx q[{i*3}], q[{i*3 + 1}];"
    circuit = QuantumCircuit.from_qasm_str(qasm)
    return circuit
        
def runCircuit(circuit, nbits):

    circuit.measure_all()
    # Transpile for simulator
    simulator = AerSimulator()
    circ = transpile(circuit, simulator)

    # Run and get counts
    result = simulator.run(circ).result()
    #print(result)
    counts = result.get_counts(circ)
    value = list(counts.keys())[0]
    print(value)
    resultString = value[:-2][::3]
    #resultString = "1"
    print(resultString)
    result = int(resultString,2)

    return result


def showCircuit(circuit):
    figure = circuit.draw(output="mpl",filename="gidney-read-generalized.jpg",vertical_compression = "high")
    plt.show()
    return


if __name__ == "__main__":
    a = 30
    b = 3
    if max(a,b) > 64: raise ValueError("Too big")
    show = 0
    nbits = len(bin(max(a,b))[2:]) + 1 # add extra bit since gidney has no carry
    circuit = createCircuit(a,b,nbits)
    if show:
        showCircuit(circuit)
    result = runCircuit(circuit,nbits)
    print(a, "+", b, "=", result)

