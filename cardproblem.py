import numpy as np
import math, random, os
from pyquil.quil import Program
from pyquil.api import QVMConnection
from pyquil.gates import H, I

os.system("clear")
number_of_cards = int(input("Enter the number of cards: "))
N = math.ceil(math.log(number_of_cards, 2))				#no of qubits


# Placing the queen at some random position
queen_position = random.randrange(number_of_cards)
queen_position_binary = np.binary_repr(queen_position, N)



# Generating the black box
print("\nBelow given is the black box containing one queen placed at some random position")
printline = "|" + "-"*3*number_of_cards + "|"
print (printline)
blackbox = " "
print(" ")
for i in range(number_of_cards):
    if i == queen_position:
        blackbox += " Q "
    else:
        blackbox += " X "
print (blackbox)
print(" ")
print(printline)


if number_of_cards == 1:
    print("Queen is at position 1\n")
    quit()

qvm = QVMConnection()
grover_circuit = Program()
qubits = list(reversed(range(N)))
print ("No of qubits required: ", len(qubits))


printline1 = "--"*50


#Step 1 of Grover's Algorithm - Initialization
print("\nStep 1 : Initialization")
print(printline1)
grover_circuit.inst([I(q) for q in qubits])			#(1)|00>
print(qvm.wavefunction(grover_circuit))


print("\nApplying the H gate")
grover_circuit.inst([H(q) for q in qubits])			#(1/2)|00> + (1/2)|01> + (1/2)|10> + (1/2)|11>
print(qvm.wavefunction(grover_circuit))



# Step 2 of Grover's Algorithm - Define quantum oracle
print("\nStep 2 : Define quantum oracle")
print(printline1)
oracle = np.zeros(shape=(2 ** N, 2 ** N))
for b in range(2 ** N):
    if np.binary_repr(b, N) == queen_position_binary:
        oracle[b, b] = -1
    else:
        oracle[b, b] = 1

print("The corresponding ORACLE used is\n\n")
print(oracle)
ORACLE_GATE_NAME = "GROVER_ORACLE"
grover_circuit.defgate(ORACLE_GATE_NAME, oracle)



# Step 3 of Grover's Algorithm - Define inversion around the mean
# Grover's Diffusion operator : D = 2A - I
print("\nStep 3 : Define inversion around the mean")
print(printline1)
DIFFUSION_GATE_NAME = "DIFFUSION"
diffusion = 2.0 * np.full((2**N, 2**N), 1/(2**N)) - np.eye(2**N)
print("Corresponding Grover's Diffusion Operator\n\n", diffusion)
grover_circuit.defgate(DIFFUSION_GATE_NAME, diffusion)

# Number of algorithm iterations 
N_ITER = int(np.pi / 4 * np.sqrt(2**N))

# O(sqrt(number_of_cards)) : Apply ORACLE and DIFFUSION operator N_ITER times
count=1
for i in range(N_ITER):
    print("\nNumber of iterations: ", count)
    print("\nAfter applying ORACLE (required qubit's amplitude is flipped)\n")    
    grover_circuit.inst(tuple([ORACLE_GATE_NAME] + qubits))
    print(qvm.wavefunction(grover_circuit))

    print("\nAfter applying DIFFUSION operator (inversion about the mean)\n")
    grover_circuit.inst(tuple([DIFFUSION_GATE_NAME] + qubits))
    print(qvm.wavefunction(grover_circuit))
    count += 1


# Step 4 of Grover's Algorithm : Measuring the qubits
print("\nStep 4 : Measuring the qubits")
print(printline1)
for q in qubits:
    grover_circuit.measure(qubit_index=q, classical_reg=q)

ret = qvm.run(grover_circuit, classical_addresses=qubits)
ret_string = ''.join([str(q) for q in ret[0]])
print("Queen is at position", int(ret_string, 2)+1)