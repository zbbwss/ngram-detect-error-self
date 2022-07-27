# -*- coding: utf-8 -*-
"""
@Time ： 2022-07-27 14:28
@Auth ： Bingbing Zhou
@File ：create_ngram.py
@IDE ：PyCharm
@EMAIL：13270870157@163.com
"""
# 计算 ngram片段的数据
import re
def write_ngram(k):
    k = sorted(k.items(), key=lambda x: x[1], reverse=True)
    with open('./data/ngram.txt', 'w', encoding='utf-8')as f:
        for i, j in k:
            f.write(i + "%##%" + str(j) + "\n")


def sub_run(path):  # n 记录每次切片的一组中包含的字符数
    f1 = open(path, 'r', encoding='utf-8')
    texts = []
    for line in f1:
        line = line.lstrip().strip()
        line = [i for i in re.split('\【|\】|\}|\[|\]|\ |，|。|！|,|!|\（|\(|\)|\）', line) if i ]
        texts.extend(line)
    results = {}
    counts = 0
    for text in texts:
        counts += 1
        text = list(text)
        text=["<s>"]*3+text+["</s>"]*3
        for n in range(0, 4):
            for i in range(3, len(text)):
                word = " ".join(text[i - n:i + 1]).strip()
                word = word.lstrip().strip()
                if not word:
                    continue
                if word not in results:
                    results[word] = 1
                else:
                    results[word] = results.get(word) + 1
    results['总行数：'] = counts
    return results
filepath = './data/product.txt'  # 用于统计用的文本路径
results0 = sub_run(filepath)
write_ngram(results0)
