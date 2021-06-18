# Community detection
* 实验要求
  
  In this project, you are given a directed citation graph including 31136 nodes and 220377 edges. These papers are divided into 5 categories according to their conferences, e.g., AAAI, IJCAI, CVPR, ICCV, ICML. Your task is to divide all of these papers into 5 clusters using community detection methods.
* 数据格式
  1. 输入文件:edges.csv，记录边的信息，总共31136个结点，220377条边，结点编号从0递增，输入文件格式为
   
      |  Source   | Target  |
      |  ----  | ----  |
      | 0  | 1 |
      | 0  | 2 |
      | ...  | ... |
  2. 输入文件:ground_truth.csv，给出少数结点编号和对应的真实category，格式为
   
      |  id   | category  |
      |  ----  | ----  |
      | 17797  | 0 |
      | 4369  | 1 |
      | ...  | ... |
  3. 输出文件:submission.csv，结合图信息以及groundtruth，输出每个结点对应的category，要求格式为

      |  id   | category  |
      |  ----  | ----  |
      | 0  | 4 |
      | 1  | 3 |
      | ...  | ... |
* 实验环境
  * Python (3.7.0)
  * Numpy (1.18.1)

* 实验方法
  
  采用Louvain算法，先划分模块，再合并结点。不断循环直至相邻两次循环求得的划分不变
  * 首先将edges.csv中边的信息输入，将有向边全部视为无向边，以邻接矩阵的方式存储与每个点相连的边及相应权重
  * 在Louvain算法的第一阶段，需要划分模块，确定每个点所属的community直至稳定。
    * 划分方式为：对于图中的某一个点，分别考虑将其加入到相邻节点所属的不同cluster中，计算 modularity gain，将modularity gain最大的cluster记录下来，将该点加入至这个cluster
    * 稳定判断标准为：对图中每个点，将其划分至其他cluster都无法获得更大的modularity gain，即视为稳定，开始进行第二阶段的结点合并与图重构
  * 第二阶段，将第一阶段求出的属于同一cluster的结点压缩为一个结点，并从零下标开始编号重构图结构，修改各边权重

* 实验结果  

  该方法受第一阶段遍历节点的顺序影响很大，一些实验结果如下表(这里的运行时间为算法运行时间，不包括读取文件，写入文件的时间)
  |  遍历方式  | 准确率  | 运行时间(s) |
  |  ----  | ----  | ---- |
  | 顺序遍历  | 81.477% | 43.1 |
  | seed = 15  | 76.766% | 79.5 |
  | seed = 25  | 49.025% | 34.8 |