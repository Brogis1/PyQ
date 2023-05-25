from pyqtorch.core.circuit import QuantumCircuit
from pyqtorch.ansatz import AlternateLayerAnsatz
from pyqtorch.converters.to_qiskit import pyq2qiskit

n_qubits = 4
n_layers = 2
ansatz = AlternateLayerAnsatz(n_qubits, n_layers)
state = QuantumCircuit(n_qubits).init_state(1)
qiskit_ansatz = pyq2qiskit(ansatz, state)
print(qiskit_ansatz)
