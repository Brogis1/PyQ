import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as init

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from pyqtorch.core.circuit import QuantumCircuit
from pyqtorch.ansatz import AlternateLayerAnsatz
from pyqtorch.embedding import SingleLayerEncoding
from pyqtorch.core.operation import Z, RX
import math

# Create a circuit.

n_qubits = 1
n_layers = 1
ansatz = AlternateLayerAnsatz(n_qubits, n_layers)
print(type(ansatz))

from pyqtorch.converters.to_qiskit import pyq2qiskit

qiskit_ansatz = pyq2qiskit(ansatz)


# Generate state with different batches.

batch_size = 1
state = QuantumCircuit(n_qubits).init_state(batch_size)

# Reshaping was only necessary for the expectation value.
# state = state.reshape((2**n_qubits, batch_size))
print(state)
print(state.shape)


# from pyqtorch.converters.to_qiskit import pyq2qiskit

# qiskit_ansatz = pyq2qiskit(ansatz(state))
