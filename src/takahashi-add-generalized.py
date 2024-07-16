from qiskit import QuantumRegister, QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_state_city
import qiskit.quantum_info as qi
import matplotlib.pyplot as plt

def createCircuit(ai,bi,nbits):
    
    # get bit representations of addends
    a = f'{ai:0{nbits}b}'
    b = f'{bi:0{nbits}b}'
    numLines = nbits * 2 + 1
    # create registers
    qreg_q = QuantumRegister(numLines, 'q')
    circuit = QuantumCircuit(qreg_q)
    
    # set addends values 
    # first addend
    for i in range(nbits):
        if a[nbits-1-i] =="1":
            circuit.x(qreg_q[1 + 2 * i]) # a0

    # second addend
    for i in range(nbits):
        if b[nbits-1-i] =="1":
            circuit.x(qreg_q[2*i]) # b0
    
    circuit.barrier([qreg_q[i] for i in range(numLines)])

    # create adder circuit

    # first cnot group

    for i in range(0,nbits-1):
        circuit.cx(qreg_q[3+i*2], qreg_q[2+i*2])

    circuit.barrier([qreg_q[i] for i in range(numLines)])

    
    # second cnot group
    circuit.cx(qreg_q[-2], qreg_q[-1])

    for i in range(1,nbits-1):
        circuit.cx(qreg_q[-2 + -2*i], qreg_q[-2 + -2*(i-1)])
    circuit.barrier([qreg_q[i] for i in range(numLines)])

    # first toffoli group
    for i in range(nbits-1):
        circuit.ccx(qreg_q[i*2], qreg_q[i*2+1], qreg_q[i*2+3])

    circuit.barrier([qreg_q[i] for i in range(numLines)])

    # toffoli and cnot group
    circuit.ccx(qreg_q[-3], qreg_q[-2], qreg_q[-1])

    for i in range(1,nbits):
        circuit.cx(qreg_q[-2*i], qreg_q[-2*i-1])
        circuit.ccx(qreg_q[-2*i -3], qreg_q[-2*i-2], qreg_q[-2*i])
    circuit.barrier([qreg_q[i] for i in range(numLines)])
        
    # third cnot group
    for i in range(1,nbits-1):
        circuit.cx(qreg_q[1 + 2*i], qreg_q[3+2*i])
    circuit.barrier([qreg_q[i] for i in range(numLines)])

    # fourth cnot group
    for i in range(nbits):
        circuit.cx(qreg_q[2*i+1], qreg_q[2*i])
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

    resultString = value[0] # we insert the carry
    for i in range(nbits):        
        resultString+=value[1:][1+i*2]
    result = int(resultString,2)

    return result

def showCircuit(circuit):
    figure = circuit.draw(output="mpl",filename="takahashi-add-generalized.jpg",vertical_compression = "high")
    plt.show()
    return


if __name__ == "__main__":
    a = 520
    b = 100
    if max(a,b) > 1024: raise ValueError("Too big")
    show = 1
    nbits = len(bin(max(a,b))[2:])
    if nbits < 2: 
        nbits = 2 # workaround for edge case
    circuit = createCircuit(a,b,nbits)
    if show:
        showCircuit(circuit)
    result = runCircuit(circuit,nbits)
    print(a, "+", b, "=", result)
