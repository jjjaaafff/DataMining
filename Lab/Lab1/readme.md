# Clustering
* 实验要求
  
  In this project, you are given 50000 papers’ feature vectors and each vector has 100 dimensions. These papers belong to 5 areas, e.g., Data Mining, Knowledge Management, Operation Research, Information Retrieval, Natural Language Processing. We have already hidden the ground truth of the areas, and your task is to implement a clustering algorithm in Python to divide these papers into 5 clusters. 
* 数据格式
  1. 输入文件:course1.csv，记录节点的信息，总共50000个节点，每个节点由100维空间进行表示，输入文件格式为
   
      |  PID   | DIM_0  | DIM_1 | ... | DIM_99 |
      |  ----  | ----  | --- | --- | --- |
      | 0  | 1.430556881 | 1.090160578 | ... | 1.933266454
      | 1  | 0.72888813 | 0.814373122 | ... | 0.652401052
      | ...  | ... | ... | ... | ...
      | 49999  | 1.570481581 | 0.908791991 | ... | 1.42298907

  2. 输出文件:Submission.csv，结合各节点信息进行聚类，输出每个结点对应的category，要求格式为

      |  id   | category  |
      |  ----  | ----  |
      | 0  | 4 |
      | 1  | 3 |
      | ...  | ... |
* 实验环境
  * Python (3.7.0)
  * Numpy (1.18.1)

* 实验方法
  
  采用k-means聚类算法，进行无监督的聚类划分
  * 程序首先利用numpy.loadtxt()读取给定的csv文件
  * 选取一个初始点，然后每次从距上一个点最远的位置选取1个点，得到初始k个点
  * 利用 k-means 聚类进行迭代直至收敛，或者迭代次数大于10000次
  * 将得到的五组聚类点按半径进行排序，按升序对这五个类从0到4进行编号
