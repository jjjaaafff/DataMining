import csv
import numpy as np
import copy



if __name__ == '__main__':
    # 读取course1.csv 去掉第一行和第一列
    input_file = open("../data/course1.csv","rb")
    next(input_file)
    data_matrix = np.loadtxt(input_file,delimiter=",",skiprows=0)
    data_matrix = np.delete(data_matrix,0,axis=1)
    paper_num = data_matrix.shape[0]
    dimenson_num = data_matrix.shape[1]
    k = 5

    # 选取五个初始点
    inipoint_set = [30704]
    for i in range(k-1):
        min_dis = float("-inf")
        record_point = 0
        for j in range(paper_num):
            crt_dis = np.sum(np.square(data_matrix[j] - data_matrix[inipoint_set[-1]]))
            if crt_dis > min_dis and (not j in inipoint_set):
                min_dis = crt_dis
                record_point = j
        inipoint_set.append(record_point)
    print(inipoint_set)
    centroid_matrix = copy.deepcopy(data_matrix[inipoint_set,:])


    # loop until convergence
    last_distance = 0
    for loop_cnt in range(10000):
        # 计算欧氏距离
        x_square = np.sum(data_matrix * data_matrix, axis=1, keepdims=True)
        y_square = np.sum(centroid_matrix * centroid_matrix, axis=1, keepdims=True).T
        distance_matrix = np.dot(data_matrix, centroid_matrix.T)
        distance_matrix *= -2
        distance_matrix += x_square
        distance_matrix += y_square
        # result maybe less than 0 due to floating point rounding errors.
        np.maximum(distance_matrix, 0, distance_matrix)

        cong_value = distance_matrix.min(1).sum()
        if cong_value == last_distance:
            break
        last_distance = cong_value
        print(cong_value)

        # 更新centroid并记录各点的最小下标
        cent_elemcnt = [0]*k
        idx_matrix = np.argmin(distance_matrix,axis=1)
        for i in range(paper_num):
            idx = idx_matrix[i]
            cent_elemcnt[idx] += 1
            centroid_matrix[idx] += data_matrix[i]

        for i in range(k):
            if cent_elemcnt[i] == 0:
                continue
            centroid_matrix[i] /= cent_elemcnt[i]

    radius = [0]*k
    for i in range(paper_num):
        cluster_id = idx_matrix[i]
        radius[cluster_id] = max(np.sum(np.square(data_matrix[i] - centroid_matrix[cluster_id])),radius[cluster_id])
    print(radius)
    after_idx = sorted(range(len(radius)), key=lambda k: radius[k])
    print(after_idx)
    # 写入结果csv文件
    headers = ['id','category']
    with open('../data/Submission.csv', 'w', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(headers)
        for i in range(paper_num):
            writer.writerow([i,after_idx[idx_matrix[i]]])

