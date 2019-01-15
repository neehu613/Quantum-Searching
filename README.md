# Quantum-Searching
Given 'N' cards we perform a quantum search operation to find that one card with desired properties in sqrt(N) steps.

The following are the steps involved:
<br>Step 1:
  Finding the number of qubits required:
  ```
  N = math.ceil(math.log(number_of_cards, 2))
  ```
  
<br>Step 2:
  Intitialize all N qubits to |0>
  ```
  grover_circuit.inst([I(q) for q in qubits])	
  ```
  
<br>Step 3:
  Put all N qubits in superposition by applying Hadamard Gate.
  ```
  grover_circuit.inst([H(q) for q in qubits])	
  ```
<br>Step 4:
  Apply Oracle to flip the sign of the amplitude of the required qubit.
  ```
  grover_circuit.inst(tuple([ORACLE_GATE_NAME] + qubits))
  ```
<br>Step 5:
  Apply Diffusion Operator to invert the amplitudes about the mean.
  ```
  grover_circuit.inst(tuple([DIFFUSION_GATE_NAME] + qubits))
  ```
<br>Step 6:
  Repeat Steps 4 and 5 for (PI)/4 * sqrt(no of cards) times.
