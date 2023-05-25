# Copyright 2022 PyQ Development Team

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import torch

IMAT = torch.tensor([1, 1], dtype=torch.cdouble)
ZMAT = torch.tensor([1, -1], dtype=torch.cdouble)
NMAT = torch.tensor([0, 1], dtype=torch.cdouble)


def ZZ(N, i=0, j=0, device='cpu'):

    if i == j:
        return torch.ones(2**N).to(device)

    op_list = [ZMAT.to(device) if k in [i, j]
               else IMAT.to(device) for k in range(N)]
    operator = op_list[0]
    for op in op_list[1::]:
        operator = torch.kron(operator, op)

    return operator


def NN(N, i=0, j=0, device='cpu'):

    if i == j:
        return torch.ones(2**N, dtype=torch.cdouble).to(device)

    op_list = [NMAT.to(device) if k in [i, j]
               else IMAT.to(device) for k in range(N)]
    operator = op_list[0]
    for op in op_list[1::]:
        operator = torch.kron(operator, op)

    return operator


def single_Z(N, i=0, device='cpu'):
    op_list = [ZMAT.to(device) if k == i
               else IMAT.to(device) for k in range(N)]
    operator = op_list[0]
    for op in op_list[1::]:
        operator = torch.kron(operator, op)

    return operator


def single_N(N, i=0, device='cpu'):
    op_list = [NMAT.to(device) if k == i
               else IMAT.to(device) for k in range(N)]
    operator = op_list[0]
    for op in op_list[1::]:
        operator = torch.kron(operator, op)

    return operator


def sum_Z(N, device='cpu'):
    H = torch.zeros(2**N, dtype=torch.cdouble).to(device)
    for i in range(N):
        H += single_Z(N, i, device)
    return H


def sum_N(N, device='cpu'):
    H = torch.zeros(2**N, dtype=torch.cdouble).to(device)
    for i in range(N):
        H += single_N(N, i, device)
    return H


def generate_ising_from_graph(graph,
                              precomputed_zz=None,
                              type_ising='Z',
                              device='cpu'):
    N = graph.number_of_nodes()
    # construct the hamiltonian
    H = torch.zeros(2**N, dtype=torch.cdouble).to(device)

    for edge in graph.edges.data():
        if precomputed_zz is not None:
            if (edge[0], edge[1]) in precomputed_zz[N]:
                key = (edge[0], edge[1])
            else:
                key = (edge[1], edge[0])
            H += precomputed_zz[N][key]
        else:
            if type_ising == 'Z':
                H += ZZ(N, edge[0], edge[1], device)
            elif type_ising == 'N':
                H += NN(N, edge[0], edge[1], device)
            else:
                raise ValueError("'type_ising' must be in ['Z', 'N']")

    return H
