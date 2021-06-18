# Streaming Algorithm

## Task1: DGIM

* 实验要求
  
  DGIM is an efficient algorithm in processing large streams. When it's infeasible to store the flowing binary stream, DGIM can estimate the number of 1-bits in the window. In this coding, you're given the stream.txt (binary stream), and you need to implement the DGIM algorithm to count the number of 1-bits.
* 实验方法  
 
  Here I just store the entire stream as a list and read the element one by one. If we read the bit number from origin txt file one by one, much time will be wasted on the file reading. While we are more concerned about the performance of DGIM algorithm than file reading. In fact, we can also read bit number from file one by one by changing the reading command a little from read() to read(i)

* 实验结果  
 
  * The running time comparision
    * DGIM uses 0.05237412452697754 second
    * Linear search uses 0.0003046989440917969 second  
  * The prediction of our DGIM is 508, while the accurate result is 391  
  * The accuracy of our DGIM is 70%


## Task2: Bloom Filter
* 实验要求
  * A Bloom filter is a space-efficient probabilistic data structure.  
  * From the NLTK (Natural Language ToolKit) library, we import a large list of English dictionary words, commonly used by the very first spell-checking programs in Unix-like operating systems.
  * Then we load another dataset from the NLTK Corpora collection: movie_reviews.
  * The movie reviews are categorized between positive and negative, so we construct a list of words (usually called bag of words) for each category.
  * Now we get a data stream (word_list) and 2 query lists (neg_reviews and pos_reviews).

* 实验方法
  * 用多个哈希函数对每个单词映射到同一个大数组中，对应映射值下标均置为1
  * 查找时对单词用同样的哈希函数映射，若每个映射值下标对应的数组元素均为1，则认为该单词在数据集中
* 实验结果
  * We can find that the running time decreases a lot after we use bloom filter
    * For positive review, the time for linear search is 1377 seconds. While the time for bloom filter is 1.29 seconds
    * For negative review, the time for linear search is 1258 seconds. While the time for bloom filter is 1.24 seconds

  * The false positive rate for positive review data with different value of bit array length m and number of hash functions k is shown below  
  The calculation of false positive rate is predicted count of words minus true count of words divided by true count of words divided.  

    |  m(*size of word list) \ k  |1|2|3|4|5|6|7|8|9|10|
    |  ----  | -|-|-|-|-|-|-|-|-|-|
    | 1 | 0.26 | 0.26 | 0.33 | 0.36 | 0.38 | 0.38 | 0.38 | 0.39 | 0.39 | 0.39 
    | 2 | 0.20 | 0.18 | 0.11 | 0.28 | 0.22 | 0.34 | 0.32 | 0.35 | 0.36 | 0.37
    | 3 | 0.11 | 0.06 | 0.09 | 0.06 | 0.08 | 0.11 | 0.24 | 0.23 | 0.24 | 0.33
    | 4 | 0.05 | 0.11 | 0.11 | 0.03 | 0.06 | 0.18 | 0.09 | 0.07 | 0.18 | 0.20
    | 5 | 0.04 | 0.02 |  0.02 | 0.11 | 0.02 | 0.04 | 0.04 | 0.04 | 0.08 | 0.06



## Task3: Count-Min sketch
* 实验要求
  * In computing, the count–min sketch (CM sketch) is a probabilistic data structure that serves as a frequency table of events in a stream of data.
  * we use the query stream (neg_reviews or pos_reviews) from task 2.

* 实验方法
  * 利用和 Bloom Filter类似的想法，同样用多组哈希映射，对每个单词映射后的的多个计数值取最小作为预测计数结果
* 实验结果
 
  The error with different value of w and d is shown below  
  The calculation of error is $ \frac{\sum_{i}abs(\#predword_{i} - \#word_{i})}{\sum_{i}\#word_{i}}$  
  w 为映射数组大小， d 为哈希函数数目

  |  w\d  |1|2|3|4|5|6|7|8|9|10|
  |  ----  | -|-|-|-|-|-|-|-|-|-|
  | 1000  | 32 |11|8.5|7.3|7.0|6.3|6.0|5.6|5.4|5.1|
  | 5000  | 6.3 | 1.9 | 1.1 | 0.72 | 0.57 | 0.49 | 0.45 | 0.42 | 0.41 | 0.37
  | 10000  | 3.6 | 0.57 | 0.37 | 0.25 | 0.19 | 0.15 | 0.13 | 0.12 | 0.11 | 0.1
  | 50000  | 0.73 | 0.074 | 0.05 | 0.04 | 0.04 | 0.04 | 0.039 | 0.038 | 0.038 | 0.038
  | 100000  | 0.31 | 0.05 |  0.04 | 0.04 | 0.038 | 0.038 | 0.038 | 0.038 | 0.038 | 0.038 |
  | 500000  | 0.13 | 0.039 |  0.038 | 0.038 | 0.038 | 0.038 | 0.038 | 0.038 | 0.038 | 0.038 |


