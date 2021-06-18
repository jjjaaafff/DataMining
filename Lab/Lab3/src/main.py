import csv
import numpy as np
import copy
import math
import random
import tqdm
from dataset import Dataset
import time


def sigmoid(x):
    # 防止溢出，当x是比较小的负数时会出现上溢，此时可以通过计算exp(x) / (1+exp(x)) 来解决
    if x < 0:
        return math.exp(x)/(1+math.exp(x))
    else:
        return 1/(1+math.exp(-x))


def GetNeighbor(graph, node, p, q, fixedlength):
    """
    :param graph: network graph
    :param node: start node in a biased walk
    :param p: return parameter, with prob. 1/p to go back to previous node
    :param q: walk-away parameter, with prob. 1/q to go further from current node
    :param fixedlength: length of a biased walk
    :return: a list containing the nodes in one biased walk except start node
    """
    walk = [node]
    while len(walk) < fixedlength:
        cur_node = walk[-1]
        cur_neighbor = graph[cur_node]
        if len(cur_neighbor) > 0:
            if len(walk) == 1:
                walk.append(random.choice(cur_neighbor))
            else:
                prev_node = walk[-2]
                candidate_node = []
                candidate_prob = []
                prob_sum = 0
                for neighbor in cur_neighbor:
                    if neighbor == prev_node:
                        # go back to previous node with probability 1/p
                        candidate_node.append(neighbor)
                        candidate_prob.append(1/p)
                        prob_sum += 1/p
                        continue
                    if neighbor in graph[prev_node]:
                        candidate_node.append(neighbor)
                        candidate_prob.append(1)
                        prob_sum += 1
                    else:
                        candidate_node.append(neighbor)
                        candidate_prob.append(1/q)
                        prob_sum += 1/q
                for i in range(len(candidate_prob)):
                    candidate_prob[i] /= prob_sum
                next = np.random.choice(candidate_node, p=candidate_prob)
                walk.append(next)
        else:
            break
    return walk[1:]


def train(graph, embed_matrix, k, p, q, fixedlength):
    N_node = len(graph)
    alpha = 0.025

    for u in range(N_node):
        if len(graph[u]) == 0:
            continue
        neighbor = GetNeighbor(graph,u,p,q,fixedlength)
        neighbor_derivate = []
        sample_derivate = []
        sample_list = []
        for v in neighbor:
            sigm = sigmoid(np.dot(embed_matrix[u],embed_matrix[v].T))
            neighbor_derivate.append(1-sigm)

        for i in range(k * fixed_neighbor_size):
            sampled_node = random.randint(0, N_node-1)
            sample_list.append(sampled_node)
            sigm_tmp = sigmoid(np.dot(embed_matrix[u],embed_matrix[sampled_node].T))
            sample_derivate.append(1-sigm_tmp)

        # gradient descent
        for i in range(len(neighbor)):
            embed_matrix[u] += (alpha * neighbor_derivate[i] * embed_matrix[neighbor[i]])
        for i in range(len(sample_list)):
            embed_matrix[u] -= (alpha * sample_derivate[i] * embed_matrix[sample_list[i]])



def test(embed_matrix, true_edge_set, false_edge_set):
    """
    :param embed_matrix: embed_matrix
    :param true_edge_set: the edge set contains existing edge in origin graph
    :param false_edge_set: the edge set contains false edge
    :return: accuracy
    """
    edge_number = len(false_test_set)
    correct_cnt = 0
    true_list = []
    false_list = []
    for i in range(edge_number):
        true_u = embed_matrix[true_edge_set[i][0]]
        true_v = embed_matrix[true_test_set[i][1]]
        true_prob = np.dot(true_u, true_v.T) / (np.linalg.norm(true_u) * np.linalg.norm(true_v))
        true_list.append(true_prob)

        false_u = embed_matrix[false_edge_set[i][0]]
        false_v = embed_matrix[false_test_set[i][1]]
        false_prob = np.dot(false_u, false_v.T) / (np.linalg.norm(false_u) * np.linalg.norm(false_v))
        false_list.append(false_prob)



    for false_prob in false_list:
        for true_prob in true_list:
            if true_prob > false_prob:
                correct_cnt += 1


    print(f'test accuracy: {correct_cnt/(edge_number*edge_number)}')
    return correct_cnt/(edge_number*edge_number)


def test_write(embed_matrix, true_edge_set, false_edge_set):
    edge_number = len(false_test_set)
    correct_cnt = 0

    headers = ['True', 'False']
    with open('../data/compare.csv', 'w', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(headers)
        for i in range(edge_number):
            true_u = embed_matrix[true_edge_set[i][0]]
            true_v = embed_matrix[true_test_set[i][1]]
            true_prob = np.dot(true_u, true_v.T) / (np.linalg.norm(true_u) * np.linalg.norm(true_v))

            false_u = embed_matrix[false_edge_set[i][0]]
            false_v = embed_matrix[false_test_set[i][1]]
            false_prob = np.dot(false_u, false_v.T) / (np.linalg.norm(false_u) * np.linalg.norm(false_v))
            writer.writerow([true_prob, false_prob])


def writefile(testfilename, outfilename, embed_matrix):
    input_file = open(testfilename, "rb")
    next(input_file)
    data_matrix = np.loadtxt(input_file, delimiter=",", skiprows=0)
    data_matrix = data_matrix.astype(int)


    headers = ['id', 'label']
    with open(outfilename, 'w', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(headers)
        for i in range(len(data_matrix)):
            a = embed_matrix[data_matrix[i][1]]
            b = embed_matrix[data_matrix[i][2]]
            prob = np.dot(a, b.T)/(np.linalg.norm(a) * np.linalg.norm(b))
            writer.writerow([data_matrix[i][0], '%.4f' % prob])


if __name__ == '__main__':
    # parameter setting

    input_filename = "../data/course3_edge.csv"
    output_filename = "../data/submission.csv"
    test_filename = "../data/course3_test.csv"
    split_ratio = 0.9
    d = 100 # dimension

    epoch = 50
    k = 10  # negative sample number
    fixed_neighbor_size = 6 # walk length
    p = 1   # Return parameter: return back to the previous node
    q = 2   # In-out parameter
    premodel_flag = 0 # 1 for use pretrained embed matrix, 0 for a new one

    # read input data, get train and test data
    ds = Dataset(input_filename,split_ratio)
    train_graph = ds.get_train_data()
    true_test_set, false_test_set = ds.get_test_data()

    # initialize embedding matrix: randomize or pre-model
    if premodel_flag == 1:
        embed_matrix = np.load("embed_acc-0.9121837692538564_dim-100_p-1_q-2_time-588.5861568450928.npy")
    elif premodel_flag == 0:
        embed_matrix = np.random.normal(0, 0.1, size=(ds.total_node_number + 1, d))
    else:
        print(f'check the premodel flag, expect 0 or 1 but now is {premodel_flag}')
        raise NotImplementedError



    # train and test
    begin_time = time.time()
    acc = 0
    for i in tqdm.tqdm(range(epoch)):
        train(train_graph,embed_matrix,k,p,q,fixed_neighbor_size)
        acc = test(embed_matrix,true_test_set,false_test_set)
    total_time = time.time()-begin_time
    print(f'Final time for {epoch} epoch is {total_time}')
    np.save(f'embed_acc-{acc}_dim-{d}_p-{p}_q-{q}_time-{total_time}.npy', embed_matrix)

    # test_write(embed_matrix,true_test_set,false_test_set)

    # write result at submission.csv
    writefile(test_filename, output_filename, embed_matrix)


