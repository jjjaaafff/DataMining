from nltk.corpus import words
from nltk.corpus import movie_reviews
import numpy as np
import random


neg_reviews = []
pos_reviews = []

for fileid in movie_reviews.fileids('neg'):
  neg_reviews.extend(movie_reviews.words(fileid))
for fileid in movie_reviews.fileids('pos'):
  pos_reviews.extend(movie_reviews.words(fileid))


print("pos",len(pos_reviews))
print("neg",len(neg_reviews))

word_list = words.words()
print("words",len(word_list))


def AccOccuranceCnt(pos_review):
    cnt_dic = {}
    for i in pos_review:
        if i in cnt_dic:
            cnt_dic[i] += 1
        else:
            cnt_dic[i] = 0

    return cnt_dic


def CMsketch(pos_review, w, d):
    cnt_matrix = np.zeros((d, w))

    seeds = []
    for i in range(d):
        seeds.append(random.randint(0, 10000))

    for word in pos_review:
        for i in range(0, d):
            hash_pos = (hash(word) ^ seeds[i]) % w
            cnt_matrix[i][hash_pos] += 1

    cnt_dic = {}

    for word in pos_review:
        min_cnt = cnt_matrix[0][(hash(word) ^ seeds[0]) % w]
        for i in range(1, d):
            if cnt_matrix[i][(hash(word) ^ seeds[i]) % w] < min_cnt:
                min_cnt = cnt_matrix[i][(hash(word) ^ seeds[i]) % w]

        cnt_dic[word] = min_cnt
    return cnt_dic




true_cnt_dic = AccOccuranceCnt(pos_reviews)

# test the influence on error with different value of w and d
for w in [1000, 5000, 10000, 50000, 100000, 500000]:
    for d in range(1, 11):
        pre_cnt = CMsketch(pos_reviews, w, d)

        dif = 0
        total = 0

        for word in true_cnt_dic.keys():
            total += true_cnt_dic[word]

            dif += abs(true_cnt_dic[word] - pre_cnt[word])

        print(f' when w={w}, d={d}, the error is {dif}/{total} in float form: {dif / total}')


