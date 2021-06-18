# Link Prediction
* 实验要求
  
  In this project, you are given a coauthor network with 16863 nodes and 46116 edges. You can split it as your training and validation set to learn an encoder. The encoder will give embeddings for each node based on which to predict whether a link exists between every pair of nodes. The learned encoder will be tested on a given testing set including node pairs drawn from the original network. You are going to label the pair as value ***p*** if the two given nodes are connected in the original network with probability ***p***. Here, ***p*** retains 4 decimal places.
* 数据格式
  1. 输入文件: course3_edge.csv，记录边的信息，总共16863个结点，46116条边，输入文件格式如下，source和target分别对应一条边上两点的编号
   
      |  Source   | Target  |
      |  ----  | ----  |
      | 221  | 5221 |
      | 12217  | 207 |
      | ...  | ... |
  2. 输入文件: course3_test.csv，给出测试集中的边和对应id，这些边有些包含在初始网络中，有些则没有，需要给出这些点对的连接概率，文件格式如下
   
      |  id   | source  | target |
      |  ----  | ----  | --- |
      | 0  | 221 | 5221 |
      | 1  | 11111 | 102 |
      | ...  | ... | ... |
  3. 输出文件:submission.csv，结合训练得到的embedding matrix，对测试集中的点对连接概率进行预测，保留4位小数，文件格式为

      |  id   | label  |
      |  ----  | ----  |
      | 0  | 0.1257 |
      | 1  | 0.2156 |
      | ...  | ... |
* 实验环境
  * Python (3.7.0)
  * Numpy (1.18.1)
  * tqdm (4.47.0)

* 实验方法
  
  采用network embedding算法，将图中的每一个结点用一个n维向量来表示，利用两个向量间的cosine距离刻画结点相似度，从而预测两点间存在连接的概率
  * 首先将course3_edge.csv中边的信息输入，将有向边全部视为无向边，以邻接矩阵的方式存储与每个点相连的边。本次实验中划分90%的边作为训练集，其余10%的边用于测试。
  * 本次实验选取的向量维度为100，embedding matrix的初始化是按照高斯分布随机生成，均值为0，方差为向量维度的倒数，即0.01
  * 随机游走：本次实验选取的游走长度为5，即每次游走在得到5个邻居节点后终止
    * 作为近似，针对softmax，在分母上不是取全图邻居节点，而是进行K次随机sample。本次实验中K取10
    * 游走方式: 采取node2vec的biased random walk。  
    return parameter p设为1，每个节点返回上一节点的概率为1(归一化之前)；  
    walk away” parameter q设为2，每个节点以dfs的方式游走至下一节点的概率为0.5(归一化之前)
  * 梯度下降更新embedding matrix，没有采用pytorch的自动求导，而是通过手动计算导数形式，利用numpy计算导数值，实现梯度的更新
  * 训练方式：每一个epoch中，对network graph中的每一个节点进行一次对应向量的更新。本次实验设置的epoch数为50
  * 测试方式：对测试集中每一个点对(u,v)，同时随机出一条不存在的边(u,v')，用训练得到的embedding matrix分别为这些边计算cosine距离，利用Area under the curve(AUC)衡量准确度



* 实验结果  

  实验结果受不同超参的影响，这里测试了一些不同超参设置对应的准确率  
  默认超参设置：

  |  向量维度d  | p  | q | walk length | 采样数k | epoch
  |  ----  | ----  | ---- |  ----  | ----  | ---- |
  | 100  | 1 | 2 |  5  | 10 | 50 |

  实验结果如下
  |  超参设置  | 收敛准确率  | 运行时间(s) |
  |  ----  | ----  | ---- |
  | 默认超参  | 91.2% | 589 |






