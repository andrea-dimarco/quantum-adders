import matplotlib.pyplot as plt 
import numpy as np

# here we want to create interesting plots regarding various 
# characteristics of each adder
# delay

nbits = np.array([2,4,8,16,32,64])


def plotQubitsHist():
    # number of qubits 
    # gidney 
    gidneyQB = nbits * 3-1
    # nagamani
    nagaQB = nbits * 3 + 1
    # takahashi
    takaQB = nbits * 2 + 1
    # thapliyal
    thapQB = nbits * 2 + 1
    data = np.array([nagaQB,gidneyQB,takaQB,thapQB])
    labels = ["Nagamani", "Gidney", "Takahashi", "Thapliyal"]
    index = np.arange(len(nbits))
    bar_width = 0.2
    plt.figure(figsize=(10,6))
    for i in range(len(labels)):
        plt.bar(index + i*bar_width, data[i], bar_width,label=labels[i])
    plt.xlabel("Operand Bit Size")
    plt.ylabel("Qubit Count")
    plt.title("Qubit requirement")
    plt.xticks(index+ bar_width * 1.5, nbits)
    plt.minorticks_on()
    plt.legend()
    plt.grid(True,axis="y")
    plt.savefig("qubitPlotHist.png")
    plt.show()

def plotQubitsLines():
    # number of qubits 
    # gidney 
    gidneyQB = nbits * 3-1
    # nagamani
    nagaQB = nbits * 3 + 1
    # takahashi
    takaQB = nbits * 2 + 1
    # thapliyal
    thapQB = nbits * 2 + 1

    data = np.array([nagaQB,gidneyQB,takaQB,thapQB])
    
    labels = ["Nagamani", "Gidney", "Takahashi", "Thapliyal"]
    index = np.arange(len(nbits))
    symbols = ['o-','s-','^-','d-']
    plt.figure(figsize=(10,6))
    for i in range(len(labels)):
        plt.plot(nbits, data[i], symbols[i],label=labels[i])
    plt.xlabel("Operand Bit Size")
    plt.ylabel("Qubit Count")
    plt.title("Qubit requirement")
    plt.xticks(nbits)
    plt.yticks(range(0,max([max(x) for x in data])+5,5))
    plt.minorticks_on()
    plt.legend()
    plt.grid(True,axis="y")
    plt.savefig("qubitPlotLines.png")
    plt.show()


def plotDelay():
    # Delay 
    # gidney 
    gidneyD = 15 * nbits-5
    # nagamani
    nagaD = 10 * nbits
    # takahashi
    takaD = 13 * nbits - 7
    # thapliyal
    thapD = 11 * nbits - 4

    data = np.array([nagaD,gidneyD,takaD,thapD])
    labels = ["Nagamani", "Gidney", "Takahashi", "Thapliyal"]
    index = np.arange(len(nbits))
    bar_width = 0.2
    plt.figure(figsize=(10,6))
    for i in range(len(labels)):
        plt.bar(index + i*bar_width, data[i], bar_width,label=labels[i])
    plt.xlabel("Operand Bit Size")
    plt.ylabel("Delay")
    plt.title("Cicuit Delay")
    plt.xticks(index+ bar_width * 1.5, nbits)
    plt.minorticks_on()
    plt.legend()
    plt.grid(True,axis="y")
    plt.savefig("delayPlot.png")
    plt.show()

def plotQuantumCost():
    #quantum cost  
    # gidney 
    gidneyQC = 18 * nbits-2
    # nagamani
    nagaQC = 12 * nbits
    # takahashi
    takaQC = 15 * nbits - 9
    # thapliyal
    thapQC = 13 * nbits - 8

    data = np.array([nagaQC,gidneyQC,takaQC,thapQC])
    labels = ["Nagamani", "Gidney", "Takahashi", "Thapliyal"]
    index = np.arange(len(nbits))
    bar_width = 0.2
    plt.figure(figsize=(10,6))
    for i in range(len(labels)):
        plt.bar(index + i*bar_width, data[i], bar_width,label=labels[i])
    plt.xlabel("Operand Bit Size")
    plt.ylabel("Quantum Cost")
    plt.title("Ciruit Quantum Cost")
    plt.xticks(index+ bar_width * 1.5, nbits)
    plt.minorticks_on()
    plt.legend()
    plt.grid(True,axis="y")
    plt.savefig("quantumCost.png")
    plt.show()

#plotQubits()
#plotQuantumCost()
plotQubitsHist()
#plotDelay()
#plotQuantumCost()