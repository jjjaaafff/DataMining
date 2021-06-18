import csv
import numpy as np
import copy

# read file and get matrix
filename = "../data/edges.csv"
input_file = open(filename, "rb")
next(input_file)
data_matrix = np.loadtxt(input_file, delimiter=",", skiprows=0)
data_matrix = data_matrix.astype(int)

# build graph in dictionary
graph = {}
for i in range(data_matrix.shape[0]):
    source = data_matrix[i][0]
    target = data_matrix[i][1]
    if source in graph:
        graph[source].append(target)
    else:
        graph[source] = [target]

    if target not in graph:
        graph[target] = []

# set seed node s
seed_node = 22492

# get attribute
N_nodes = len(graph)    #31136
N_edges = data_matrix.shape[0]  #220377
degree_vector = np.zeros(N_nodes)
for i in range(N_nodes):
    degree_vector[i] = len(graph[i])



# PPR
r = np.zeros(N_nodes)
q = np.zeros(N_nodes)
q[seed_node] = 1
beta = 0.5
epsilon = 0.01

# c = np.divide(a, b, out=np.zeros_like(a), where=b!=0)
# 除零控制

q_divide_d = np.divide(q, degree_vector, out=np.zeros_like(q), where=degree_vector!=0)

# return the index of one legal vertex
def check_loop_condition(q,degree_vector,epsilon):
    length = len(q)
    idx = -1
    maxval = 0
    for i in range(length):
        if q[i] - epsilon * degree_vector[i]> maxval:
            maxval = q[i] - epsilon * degree_vector[i]
            idx = i
    return idx

u = check_loop_condition(q,degree_vector,epsilon)
while u!=-1:
    d_u = degree_vector[u]
    r_prime = copy.copy(r)
    q_prime = copy.copy(q)

    r_prime[u] = r[u] + (1-beta)*q[u]
    q_prime[u] = 0.5 * beta * q[u]
    for v in graph[u]:
        q_prime[v] = q[v] + 0.5 * beta * q[u] / d_u
    r = copy.copy(r_prime)
    q = copy.copy(q_prime)
    u = check_loop_condition(q, degree_vector, epsilon)
    print(np.count_nonzero(q))
    # q_divide_d = np.divide(q, degree_vector, out=np.zeros_like(q), where=degree_vector != 0)



sorted_nodes = sorted(range(len(r)), key=lambda k: r[k],reverse=True)
A = []
phi_A = [0]*N_nodes
cut = 0
vol = 0
for idx,node in enumerate(sorted_nodes):
    A.append(node)
    vol += degree_vector[node]
    cut += degree_vector[node]
    edge_cnt = 0
    for neigibor in graph[node]:
        if neigibor in A:
            edge_cnt += 1
    cut -= edge_cnt
    phi_A[idx] = cut/vol
    if idx == 30:
        break

print(phi_A)


print(sorted(r,reverse=True))
print(np.count_nonzero(r))
print(r[sorted_nodes[0]])


