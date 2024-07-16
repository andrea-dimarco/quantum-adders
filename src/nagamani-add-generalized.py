from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from numpy import pi
import numpy as np
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_state_city
import qiskit.quantum_info as qi
import matplotlib.pyplot as plt

def createCircuit(ai,bi):
    
    nbits = len(bin(max(ai,bi))[2:])
    a = f'{ai:0{nbits}b}'
    b = f'{bi:0{nbits}b}'
    numLines = nbits * 3 + 1
    qreg_q = QuantumRegister(numLines, 'q')
    circuit = QuantumCircuit(qreg_q)

    # set initial qubits values
    # first addend
    if a[nbits-1] =="1":
        circuit.x(qreg_q[0]) # a0
    for i in range(1,nbits):
        if a[nbits-1-i] =="1":
            circuit.x(qreg_q[3 * i + 1 ]) # a0

    # second addend
    for i in range(nbits):
        if b[nbits-1-i] =="1":
            circuit.x(qreg_q[3 * i + 2]) # a0

    # add circuitry
    #first block is different
    circuit.barrier([qreg_q[i] for i in range(numLines)])

    circuit.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
    circuit.cx(qreg_q[2], qreg_q[1])
    circuit.ccx(qreg_q[0], qreg_q[1], qreg_q[3])
    circuit.cx(qreg_q[0], qreg_q[1])
    for i in range(1,nbits):
        circuit.barrier([qreg_q[i] for i in range(numLines)])
        circuit.ccx(qreg_q[3 * i], qreg_q[2 + 3*i], qreg_q[3+ 3*i])
        circuit.cx(qreg_q[2 + 3*i], qreg_q[3*i])
        circuit.ccx(qreg_q[3*i], qreg_q[1+3*i], qreg_q[3+3*i])
        circuit.cx(qreg_q[1+3*i], qreg_q[3*i])
    return circuit

def runCircuit(circuit):
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
    resultString = ""
    for i in range(nbits+1):
        if (i ==nbits):
            resultString += str(value[3*(i-1)+2])
        else: 
            resultString +=str(value[i*3])
    result = int(resultString,2)

    return result

def showCircuit(circuit):
    figure = circuit.draw(output="mpl",filename="nagamani-add-generalized.jpg",vertical_compression = "high")
    plt.show()
    return

if __name__ == "__main__":
    a = 50
    b = 18
    if max(a,b) > 256: raise ValueError("Too big")
    show = True
    nbits = len(bin(max(a,b))[2:])
    numLines = nbits * 3 + 1

    circuit = createCircuit(a,b)
    if show:
        showCircuit(circuit)
    result = runCircuit(circuit)
    print(a, "+", b, "=", result)
    # print(a, "+", b, "=", int(str(cout)+str(s4) + str(s3)+str(s2)+str(s1)+str(s0),2))
