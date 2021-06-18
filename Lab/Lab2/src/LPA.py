import csv
import numpy as np
import copy
import tqdm
import random


# read file and get matrix
filename = "../data/edges.csv"
input_file = open(filename, "rb")
next(input_file)
data_matrix = np.loadtxt(input_file, delimiter=",", skiprows=0)
data_matrix = data_matrix.astype(int)

# build graph in dictionary
graph = {}
targeted_graph = {}
for i in range(data_matrix.shape[0]):
    source = data_matrix[i][0]
    target = data_matrix[i][1]
    if source in graph:
        graph[source].append(target)
    else:
        graph[source] = [target]

    if target not in graph:
        graph[target] = [source]
    else:
        graph[target].append(source)

    # if target not in targeted_graph:
    #     targeted_graph[target] = [source]
    # else:
    #     targeted_graph[target].append(source)
    # if source not in targeted_graph:
    #     targeted_graph[source] = []

# set seed node s
seed_node = 13762

# get attribute
N_nodes = len(graph)    #31136
N_edges = data_matrix.shape[0]  #220377
label_dict = {}
node_weight = [1]*N_nodes
for i in range(N_nodes):
    label_dict[i] = i



filename = "../data/ground_truth.csv"
input_file = open(filename, "rb")
next(input_file)
data_matrix = np.loadtxt(input_file, delimiter=",", skiprows=0)
data_matrix = data_matrix.astype(int)
for i in range(data_matrix.shape[0]):
    node = data_matrix[i][0]
    label = data_matrix[i][1]
    node_weight[node] = 1500
    label_dict[node] = label
    for adj_nodes in graph[node]:
        label_dict[adj_nodes] = label


print(label_dict)

def LabelProp(label_dict,graph,max_iter):
    all_nodes = [i for i in range(len(label_dict))]

    for cnt in range(max_iter):
        last_label_dict = copy.deepcopy(label_dict)
        stable_flag = True
        random.shuffle(all_nodes)
        for node in all_nodes:

            adjacent_nodes = graph[node]
            random.shuffle(adjacent_nodes)
            label_cnt = {}
            for adjacent_node in adjacent_nodes:

                label = label_dict[adjacent_node]

                # if label>4:
                #     continue

                if label not in label_cnt:
                    label_cnt[label] = node_weight[adjacent_node]
                else:
                    label_cnt[label] += node_weight[adjacent_node]
            label_cnt_item = list(label_cnt.items())
            random.shuffle(label_cnt_item)
            sorted_label_cnt = sorted(label_cnt_item, key=lambda d: d[1], reverse=True)
            if len(sorted_label_cnt) == 0 :
                continue
            if last_label_dict[node]!=sorted_label_cnt[0][0]:
                stable_flag = False
            last_label_dict[node] = sorted_label_cnt[0][0]
            # node_weight[node] = sorted_label_cnt[0][1]
        if stable_flag:
            break
        label_dict = copy.deepcopy(last_label_dict)
        print(label_dict)
    return label_dict



res = LabelProp(label_dict,graph,20)
print(res.values())
res_list = list(res.values())
print(f"zero is {res_list.count(0)}")
print(f"one  is {res_list.count(1)}")
print(f"two is {res_list.count(2)}")
print(f"three is {res_list.count(3)}")
print(f"four is {res_list.count(4)}")





