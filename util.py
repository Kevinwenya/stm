# coding=utf-8

import random

# 从 0 - orign_big_n 中随机选取 target_small_m 个数字
# 参见[http://blog.csdn.net/sgbfblog/article/details/7917685]
def random_select(orign_big_n, target_small_m):
    selected = []
    for i in range(orign_big_n):
        if not target_small_m:
            break
        if random.getrandbits(128) % (orign_big_n - i) < target_small_m:
            selected.append(i)
            target_small_m -= 1
    return selected

# 从文档集中随机选出指定文档个数的文档，其中一个文档为一行
def random_pick_docs(raw_filepath, target_small_m, full=False): 
    docs = [line for line in open(raw_filepath).xreadlines()]
    if full:
        return docs

    if len(docs) > target_small_m and target_small_m > 0:
        target_docs = []
        selected_line_num = random_select(len(docs), target_small_m)
        for line_num in selected_line_num:
            target_docs.append(docs[line_num])
        return target_docs
    else:
        return docs

# 从文档集中随机选出指定比例的文档个数，其中一个文档为一行
def random_pick_docs_given_ratio(raw_filepath, target_small_ratio, full=False):
    length = len([line for line in open(raw_filepath).xreadlines()])
    return random_pick_docs(raw_filepath, int(length*target_small_ratio), full=False)

if __name__ == '__main__':
    raw_filepath = 'raw_text.txt'
    sample_filepath = 'sample_weibo.txt'
    sample_file = open(sample_filepath, 'w')
    sample_docs = random_pick_docs_given_ratio(raw_filepath, 0.3)
    for line in sample_docs:
        sample_file.write(line)

