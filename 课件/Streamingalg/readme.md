# Streaming Algorithm

* Data Stream
  * a sequence of signals used to transmit or receive information
  * we don't know the entire data set in advance
  * The stream may be large and can't fit all the data into memory

* Sampling from a data stream
  * Suppose we need to maintain a fixed-size s sample. At time n, we have seen n iterms in the stream.
  * Algorithm
    * For the arriving n-th elements, we will keep this element with probability s/n. We will discard it with (1-s/n) probability.
    * If we take this elements, we will replace one of the elements in maintained sample. The replaced element will be picked uniformly at random. 

* Filter data streams
  * Motivation: Given a list of keys S, we want to determine which elements of stream are in S
  * First cut solution
    * use a bit arrat B with length n
    * use a hash function h mapping elements to range [0,n)
    * for each elements in given list, set B[h(elem)] = 1
    * for each elements in stream, regard it in the list S if B[h(elem)] = 1 
  * We get no false negative, but may get false positive
  * Bloom Filter
    * use k different hash functions. h1, h2, ..., hk 
    * for each elements in given list, set B[hi(elem)] = 1 for all i = 1,2,...,k
    * for each elements in stream, regard it in the list S if B[hi(elem)] = 1 for all i=1,2,...,k
  * Bloom Filter analysis
    * Suppose |S| = m, |B| = n, # hash function = k
    * false positive probability is (1-exp(-km/n))^k
    * Optimal value of k is (n * ln2 / m)
    * having 1 big B is equal to having k small B
    * Disadvantage: only insertion, no deletion from Bloom Filter

* Count element frequency
  * Similar to Bloom Filter
  * use a (k x b) matrix COUNT to store the count and initialize all elements as zero
  * for each element in data stream, COUNT[i, hi(elem)]+=1 for i = 1,2,...,k
  * Retrive, count of one specific element, count = min COUNT[i, hi(elem)] for i = 1,2,...,k
  * Analysis
    * Adding another hash function exponentially decreases the chance of hash conflicts
    * Increasing the width helps spread up the counts with a linear effect

* Queries over a Sliding Window
  * Problem: given a stream of 0s and 1s, how many 1s are in the last k bits
  * We can't store the most recent N bits when N is extremely large.
  * DGIM(Datar-Gionis-Indyk-Motwani) Algorithm
    * assign each bit in the stream a time stamp starting from 1, 2, ...
    * define bucket: a record consisting of time stamp of end and number of 1s(the number of 1s must be power of 2)
    1. when a new bit comes from the stream, drop the last bucket if its time stamp is prior to N
    2. If this bit is zero, no other changes needed
    3. If this bit is one, we append a new bucket with (time-stamp, 0) at the end of current bucket lists. 
    4. Then we detect whether there exists three buckets with same number of 1s. If so, we combine the oldest two into one bucket with double number of 1s.
  * Query of DGIM
    * Sum the sizes of all buckets but the last partially overlapping with the query
    * Add half the size of the last bucket 
  * Analysis of DGIM algorithm
    * The timestamp of its end [O(log N) bits] (This is because we record timestamps modulo N (the window size) in reality)
    * The number of 1s between its beginning and end [O(log log N) bits]
    * The relative error is at most 50% due to the last uncertain bucket.
  * Optimization
    * Instead of maintaining 1 or 2 of each size bucket, we allow either s-1 or s buckets (s > 2)

* Count distinct elements
  * Problem: maintain a count of the number of different elements in a stream seen so far
  * we can't maintain the set of elements seen so far due to storage limitation
  * Flajolet-Martin Approach
    * pick a hash function h mapping each of the N elements to at least log2 N bits
    * define r(a) be the number of tailing 0s in the binary representation of h(a)
    * record R = max r(a) over all the items a seen so far, then the estimated number of distinct elements is 2^R
  * Why this approach works?
    * refer to the lecture note

* Computing Moments
  * Defination
    * Suppose a stream has elements chosen from a set A of N values (say 1 to N)
    * Let mi be the number of times value i occurs in the stream
    * the k-th moment is sum{(m_i)^k} for all value i in set A
  * Special case
    * 0-th moment is the number of distinct elements
    * 1-st moment is the length of the stream
    * 2-nd moment is called surprise number S, a measure of how uneven the distribution is
  * AMS(Alon-Matias-Szegedy) Method
    * It works for all moments, here we consider 2-nd situation
    * We pick some random time t (t < n) to start.
    * Then we maintain count c of the number of t's element in the stream starting from the chosen time t
    * The estimation of 2nd moment is S = f(X) = n*(2*c-1)
  * Detail refer to lecture note









