import time

def bit_cnt(windowsize, filename):
    bucket = []
    time_stamp = 0
    bit_sum = 0
    true_bit_sum = 0
    with open(filename, 'r') as f:
        file_content = f.read()
        stream_list = file_content.split("\t")

    begin_time = time.time()
    for i in range(len(stream_list) - 1):
        time_stamp += 1

        if len(bucket) != 0 and bucket[0]["time"] == time_stamp % windowsize:
            del bucket[0]

        if int(stream_list[i]) == 0:
            continue

        elif int(stream_list[i]) == 1:
            bucket.append({"time": time_stamp % windowsize, "cnt": 0})
            merge_idx = len(bucket) - 1
            while merge_idx > 1:
                if bucket[merge_idx]["cnt"] == bucket[merge_idx - 2]["cnt"]:
                    bucket[merge_idx - 1]["cnt"] += 1
                    del bucket[merge_idx - 2]
                    merge_idx -= 2
                else:
                    break

    for i in range(len(bucket)):
        bit_sum += 2 ** (bucket[i]['cnt'])

    bit_sum -= 2 ** (bucket[0]['cnt'] - 1)

    print("running time for DGIM is ", time.time() - begin_time)
    print("bit count for DGIM is ", bit_sum)
    return bit_sum


def last_bit_cnt(windowsize, filename, lastsize):
    bucket = []
    time_stamp = 0
    bit_sum = 0
    true_bit_sum = 0
    with open(filename, 'r') as f:
        lala = f.read()
        stream_list = lala.split("\t")

    begin_time = time.time()
    for i in range(len(stream_list) - 1):
        time_stamp += 1

        if len(bucket) != 0 and bucket[0]["time"] == time_stamp % windowsize:
            del bucket[0]

        if int(stream_list[i]) == 0:
            continue

        elif int(stream_list[i]) == 1:
            bucket.append({"time": time_stamp % windowsize, "cnt": 0})
            merge_idx = len(bucket) - 1
            while merge_idx > 1:
                if bucket[merge_idx]["cnt"] == bucket[merge_idx - 2]["cnt"]:
                    bucket[merge_idx - 1]["cnt"] += 1
                    del bucket[merge_idx - 2]
                    merge_idx -= 2
                else:
                    break

    check_time = 0

    for i in range(len(bucket) - 1, -1, -1):
        if bucket[i]['time'] >= (time_stamp - lastsize) % windowsize:
            bit_sum += 2 ** (bucket[i]['cnt'])
            check_time = i
        else:
            break

    bit_sum -= 2 ** (bucket[check_time]['cnt'] - 1)

    print(f'bit count for DGIM in the last {lastsize} bits of stream is {bit_sum}')
    return bit_sum


def acc_bit_cnt(windowsize, filename):
    true_bit_sum = 0
    with open(filename, 'r') as f:
        lala = f.read()
        stream_list = lala.split("\t")

    begin_time = time.time()
    for i in range(len(stream_list) - (windowsize + 1), len(stream_list) - 1):
        if int(stream_list[i]) == 1:
            true_bit_sum += 1
    print("running time for linear search is ", time.time() - begin_time)
    print("bit count for linear search is ", true_bit_sum)
    return true_bit_sum


window_size = 1000
filename = "../data/stream.txt"
last_size = 500


bit_cnt(1000,filename)
res= last_bit_cnt(window_size, filename, last_size)
acc_bit_cnt(window_size,filename)








