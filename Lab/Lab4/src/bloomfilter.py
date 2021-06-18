from nltk.corpus import words
from nltk.corpus import movie_reviews
import math
import tqdm
import time
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


def AccDetermine(pos_review, neg_review, word_list):
    pos_total = len(pos_review)
    neg_total = len(neg_review)
    word_total = len(word_list)

    pos_in = 0
    neg_in = 0
    begin_time = time.time()
    for i in tqdm.tqdm(pos_review):
        if i in word_list:
            pos_in += 1
    print("linear pos search time is ",time.time()-begin_time)
    print(f'pos number: {pos_in}/{pos_total}')
    # linear pos search time is  1796.4529583454132
    # pos number: 600128/832564


    second_time = time.time()
    for i in tqdm.tqdm(neg_review):
        if i in word_list:
            neg_in += 1
    print("linear neg search time is ",time.time()-second_time)
    print(f'neg number: {neg_in}/{neg_total}')
    # linear neg search time is 1258.8483040332794
    # neg number: 540998 / 751256


def bloomfilter(pos_review, neg_review, word_list, bit_length):
    pos_total = len(pos_review)
    neg_total = len(neg_review)
    word_total = len(word_list)

    k = int(bit_length * math.log(2) / word_total)

    B = [0] * bit_length

    seeds = []
    for i in range(k):
        seeds.append(random.randint(0, 10000))

    for word in tqdm.tqdm(word_list):
        for i in range(k):
            hash_pos = (hash(word) ^ seeds[i]) % bit_length
            B[hash_pos] = 1

    begin_time = time.time()
    pos_cnt = 0
    for pos_word in tqdm.tqdm(pos_review):
        for i in range(k):
            if B[(hash(pos_word) ^ seeds[i]) % bit_length] == 0:
                pos_cnt += 1
                break
    print("bloom pos search time is ", time.time() - begin_time)
    print(f'pos number: {pos_total - pos_cnt}/{pos_total}')

    neg_cnt = 0
    second_time = time.time()
    for neg_word in tqdm.tqdm(neg_review):
        for i in range(k):
            if B[(hash(neg_word) ^ seeds[i]) % bit_length] == 0:
                neg_cnt += 1
                break
    print("bloom neg search time is ", time.time() - second_time)
    print(f'neg number: {neg_total - neg_cnt}/{neg_total}')


def testbloomfilter(pos_review, neg_review, word_list, bit_length, k):
    pos_total = len(pos_review)
    neg_total = len(neg_review)
    word_total = len(word_list)

    B = [0] * bit_length

    seeds = []
    for i in range(k):
        seeds.append(random.randint(0, 10000))

    for word in word_list:
        for i in range(k):
            hash_pos = (hash(word) ^ seeds[i]) % bit_length
            B[hash_pos] = 1

    begin_time = time.time()
    pos_cnt = 0
    for pos_word in pos_review:
        for i in range(k):
            if B[(hash(pos_word) ^ seeds[i]) % bit_length] == 0:
                pos_cnt += 1
                break

    neg_cnt = 0
    second_time = time.time()
    for neg_word in neg_review:
        for i in range(k):
            if B[(hash(neg_word) ^ seeds[i]) % bit_length] == 0:
                neg_cnt += 1
                break

    return pos_total - pos_cnt, neg_total - neg_cnt


# Accurate determine
AccDetermine(pos_reviews, neg_reviews, word_list)

# Bloom filter determine
bloomfilter(pos_reviews,neg_reviews,word_list,len(word_list)*3)

# test the influence on false positive rate with different value of m and k
true_pos = 600128
true_neg = 540998
for i in range(1,6):
    for k in range(1,11):
        poscnt, negcnt = testbloomfilter(pos_reviews,neg_reviews,word_list,len(word_list)*i,k)
        print(f'when m={i}*word_list  k={k}, postive review fp rate is {(poscnt - true_pos)/true_pos}, negative review fp rate is {(negcnt - true_neg)/true_neg}')








