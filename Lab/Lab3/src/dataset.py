import csv
import numpy as np
import copy
import math
import random
import tqdm

class Dataset:
    def __init__(self,filename,split_ratio):
        input_file = open(filename, "rb")
        next(input_file)
        data_matrix = np.loadtxt(input_file, delimiter=",", skiprows=0)
        data_matrix = data_matrix.astype(int)
        # random.shuffle(data_matrix)

        self.ratio = split_ratio
        self.train_edge_number = int(data_matrix.shape[0] * split_ratio)
        self.test_edge_number = data_matrix.shape[0] - self.train_edge_number

        self.train_matrix = data_matrix[:self.train_edge_number]
        self.test_matrix = data_matrix[self.train_edge_number:]

        self.total_node_number = data_matrix.max()
        print("total ",self.total_node_number)
        self.train_node_bumber = self.train_matrix.max()
        self.test_node_bumber = self.test_matrix.max()

    def get_train_data(self):
        train_graph = [[] for i in range(self.train_node_bumber + 1)]
        for i in range(self.train_edge_number):
            source = self.train_matrix[i][0]
            target = self.train_matrix[i][1]
            train_graph[source].append(target)
            train_graph[target].append(source)
        self.train_graph = train_graph
        return train_graph

    def get_test_data(self):
        true_edge_set = self.test_matrix
        false_edge_set = []
        cnt = 0
        while cnt<self.test_edge_number:
            u = true_edge_set[cnt][0]
            v = random.randint(0,self.total_node_number)
            if v in self.train_graph[v]:
                continue
            false_edge_set.append([u,v])
            cnt += 1
        return true_edge_set, false_edge_set

if __name__ == '__main__':

    input_filename = "../data/course3_edge.csv"
    split_ratio = 0.9
    Ds = Dataset(input_filename,split_ratio)

    test = Ds.get_train_data()
    print(len(test))
    print(Ds.train_edge_number)
    print(Ds.test_node_bumber)
    Ds.get_test_data()





