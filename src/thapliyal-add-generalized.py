from qiskit import QuantumCircuit, transpile
from numpy import pi
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_state_city
import matplotlib.pyplot as plt

def createCircuit(ai,bi,nbits):
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
    """
    numlines = nbits * 2 + 1
    # create registers
    init_registers = f"""
    qreg q[{numlines}];
    """
    qasm +=init_registers

    # initialize registers 
    a = f'{ai:0{nbits}b}'
    b = f'{bi:0{nbits}b}'

    # set addends values 
    # first addend
    for i in range(nbits):
        if a[nbits-1-i] =="1":
            index = 1 + 2 * i
            qasm += f"x q[{index}];"

    # second addend
    for i in range(nbits):
        if b[nbits-1-i] =="1":
            index = 2 * i
            qasm += f"x q[{index}];"
    
    # barrier string
    barrier = "barrier "
    for i in range(nbits * 2 + 1):
        if i == nbits * 2: 
            barrier += f"q[{i}];"
        else:
            barrier += f"q[{i}],"
    qasm +=barrier

    # circuit creation
 
    # first cnot group
    for i in range(1,nbits):
        qasm += f"cx q[{i * 2+1}], q[{i * 2}];"

    # second cnot group 
    qasm += f"cx q[{numlines -2}], q[{numlines -1}];"
    for i in range (1,nbits-1):
        qasm += f"cx q[{numlines-2 + -2*i}], q[{numlines-2 + -2 *(i-1)}];"

    # toffoli group 
    for i in range (nbits-1):
        qasm += f"ccx q[{2*i+1}], q[{2*i}], q[{2*i+3}];"


    # pg group 
    qasm += f"pG q[{numlines-3}], q[{numlines-2}], q[{numlines-1}];"
    for i in range (1,nbits):
        ind1 =numlines-3 + -2 * i
        ind2 = numlines-2 + -2 * i
        ind3 =numlines + -2 * i
        qasm += f"pG q[{ind1}], q[{ind2}], q[{ind3}];"

    # third cnot group 
    for i in range(1,nbits-1):
        qasm+= f"cx q[{1 + i*2}], q[{1 + (i+1)*2}];"
    qasm += barrier
    # fourth cnot group
    for i in range(1,nbits):
        qasm+= f"cx q[{1 + i*2}], q[{i*2}];"

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
    a = 34
    b = 19
    if max(a,b) > 1024: raise ValueError("Too big")
    show = 0
    nbits = len(bin(max(a,b))[2:])
    if nbits < 2: 
        nbits = 2 # workaround for edge case
    circuit = createCircuit(a,b,nbits)
    if show:
        showCircuit(circuit)
    result = runCircuit(circuit,nbits)
    print(a, "+", b, "=", result)

