import csv
import numpy as np
import copy
import random
import time

def readfile(filename):
    # read file and get matrix
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
            graph[source].append([target,1])
        else:
            graph[source] = [[target,1]]

        if target in graph:
            graph[target].append([source,1])
        else:
            graph[target] = [[source,1]]

    N_edges = data_matrix.shape[0]  #220377
    N_nodes = len(graph)   #31136
    return N_nodes,graph,N_edges

def calculate_ki(graph):
    k_i = [0 for n in range(len(graph))]
    for node in range(len(graph)):
        for neighbor in graph[node]:
            k_i[node] += neighbor[1]
    return k_i

def phase_one(graph,k_i,m):
    N_nodes = len(graph)
    communities = [i for i in range(N_nodes)]
    partition = [[node] for node in range(N_nodes)]
    sumtot = [k_i[node] for node in range(N_nodes)]
    not_stable = 1
    shuffled_order = [i for i in range(N_nodes)]
    while not_stable:
        not_stable = 0
        for node in shuffled_order:
            community = communities[node]
            max_community = community
            max_gain = 0
            max_sharelink = 0
            partition[community].remove(node)
            for neighbor in graph[node]:
                if node == neighbor[0]:
                    continue
                if communities[neighbor[0]] == community:
                    max_sharelink += neighbor[1]


            sumtot[community] -= k_i[node]
            communities[node] = -1

            neighbor_community = {}
            for neighbor in graph[node]:
                if node == neighbor[0]:
                    continue
                tmp_community = communities[neighbor[0]]
                if tmp_community in neighbor_community:
                    continue
                neighbor_community[communities[neighbor[0]]] = 1
                k_i_in = 0

                for tmp_neighbor in graph[node]:
                    if communities[tmp_neighbor[0]] == tmp_community:
                        k_i_in += tmp_neighbor[1]

                gain = (2 * m * k_i_in - k_i[node] * sumtot[communities[neighbor[0]]]) / (2 * m * m)
                if gain>max_gain:
                    max_gain = gain
                    max_community = communities[neighbor[0]]

            partition[max_community].append(node)
            communities[node] = max_community
            sumtot[max_community] += k_i[node]
            if community != max_community:
                not_stable = 1
    partition = [c for c in partition if c]
    return (partition,communities)

def phase_two(graph,partition,communities):
    new_communities = []
    hash_map = {}
    idx_cnt = 0
    for i in communities:
        if i in hash_map:
            new_communities.append(hash_map[i])
        else:
            hash_map[i] = idx_cnt
            new_communities.append(idx_cnt)
            idx_cnt += 1
    communities = copy.copy(new_communities)

    new_graph = {}
    for i in range(len(partition)):
        new_graph[i] = []


    for node in range(len(graph)):
        source_com = communities[node]
        for neighbor in graph[node]:
            neighbor_com = communities[neighbor[0]]
            exist_flag = 0
            for curlist in new_graph[source_com]:
                if curlist[0] == neighbor_com:
                    curlist[1] += neighbor[1]
                    exist_flag = 1
                    break
            if exist_flag == 0:
                new_graph[source_com].append([neighbor_com,neighbor[1]])
    return new_graph



if __name__ == '__main__':
    # filename setting
    input_filename = "../data/edges.csv"
    output_filename = "../data/Submission.csv"
    truth_filename = "../data/ground_truth.csv"

    final_partition = []

    total_nodes ,graph, m = readfile(input_filename)
    origin_graph = copy.deepcopy(graph)

    begin_time = time.time()
    for i in range(10):
        k_i = calculate_ki(graph)
        partition,communities = phase_one(graph,k_i,m)
        print("partition size ",len(partition))
        print("Phase one finish")

        if len(final_partition) == 0:
            final_partition = partition
        else:
            tmp_partition = []
            for cluster in partition:
                part = []
                for elem in cluster:
                    part.extend(final_partition[elem])
                tmp_partition.append(part)
            final_partition = copy.deepcopy(tmp_partition)

        graph = phase_two(graph,partition,communities)
        print("graph size",len(graph))
        print("phase two finish")



    print(f'Running time for algorithm is {time.time()-begin_time}')
    for i in final_partition:
        print(f'Size of cluster in final partition: {len(i)}')



    input_file = open(truth_filename, "rb")
    next(input_file)
    data_matrix = np.loadtxt(input_file, delimiter=",", skiprows=0)
    data_matrix = data_matrix.astype(int)
    ground_truth = {}
    for i in range(data_matrix.shape[0]):
        node = data_matrix[i][0]
        label = data_matrix[i][1]
        if label not in ground_truth:
            ground_truth[label] = [node]
        else:
            ground_truth[label].append(node)

    label_classifier = np.zeros((len(final_partition),len(ground_truth)))
    for label in ground_truth.keys():
        for truth_node in ground_truth[label]:
            for idx,community in enumerate(final_partition):
                if truth_node in community:
                    label_classifier[idx][label] += 1

    cluster_label = np.argmax(label_classifier,1)
    print(cluster_label)


    # cluster_elem_number = [0]*5
    # for idx,i in enumerate(final_partition):
    #     cluster_elem_number[cluster_label[idx]] += len(i)
    # print(cluster_elem_number)

    #
    # ambigous_cluster = []
    # confident_cluster = []
    # for i in range(len(final_partition)):
    #     if label_classifier[i][cluster_label[i]] == 0:
    #         ambigous_cluster.append(i)
    #     else:
    #         confident_cluster.append(i)
    # print("ambigous set",ambigous_cluster)
    # random.seed(seed)
    # random.shuffle(ambigous_cluster)
    #
    #
    #
    #
    # for ambigous_idx in ambigous_cluster:
    #     label_cnt = np.zeros(5)
    #     for i in final_partition[ambigous_idx]:
    #         for neighbor in origin_graph[i]:
    #             for confident_idx in confident_cluster:
    #                 if neighbor[0] in final_partition[confident_idx]:
    #                     label_cnt[cluster_label[confident_idx]] += 1
    #                     break
    #     max_idx = np.argmax(label_cnt)
    #     cluster_label[ambigous_idx] = max_idx
    #     # confident_cluster.append(ambigous_idx)
    #
    #
    cluster_elem_number = np.zeros(5)
    for i in range(len(final_partition)):
        cluster_elem_number[cluster_label[i]] += len(final_partition[i])
    print("after cluster label",cluster_elem_number)


    # 写入 81.477
    headers = ['id', 'category']
    with open(output_filename, 'w', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(headers)
        for i in range(total_nodes):
            for idx, community in enumerate(final_partition):
                if i in community:
                    writer.writerow([i, cluster_label[idx]])




    # new new xieru 81.541
    # headers = ['id', 'category']
    # with open('../data/Submission_new_new.csv', 'w', newline='') as fp:
    #     writer = csv.writer(fp)
    #     writer.writerow(headers)
    #     for i in range(total_nodes):
    #         for idx, community in enumerate(final_partition):
    #             if i in community:
    #                 if idx in confident_cluster:
    #                     writer.writerow([i, cluster_label[idx]])
    #                     continue
    #                 else:
    #                     label_cnt = np.zeros(5)
    #                     for neighbor in origin_graph[i]:
    #                         for neighbor_idx, neighbor_community in enumerate(final_partition):
    #                             if neighbor[0] in neighbor_community:
    #                                 label_cnt[cluster_label[neighbor_idx]] += 1
    #                                 break
    #                     writer.writerow([i, np.argmax(label_cnt)])
