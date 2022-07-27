# -*- coding: utf-8 -*-
"""
@Time ： 2022-07-25 11:06
@Auth ： Bingbing Zhou
@File ：correcter.py
@IDE ：PyCharm
@EMAIL：13270870157@163.com

"""

from pypinyin import lazy_pinyin
from cal_ngram import Ngram
from distance import text_feature_generator
import numpy as np


def create_trie():
    """
    :return:  构建pinyin的倒排索引
    """
    trie = {}

    for i in open("data/keyword", 'r', encoding='utf-8'):

        dd = "".join(lazy_pinyin(i.strip()))
        if dd not in trie:
            trie[dd] = {i.strip(): 100}
        else:
            if i.strip() not in trie[dd]:
                trie[dd][i.strip()] = 100
            else:
                continue
    return trie


trie = create_trie()
ED = text_feature_generator()
ngram = Ngram()


def pinyin_main(query_origin):
    query = "".join(lazy_pinyin(query_origin))
    if query in trie:
        # print(trie[query])
        if query_origin in trie[query]:
            print("没有错误")
            return []
        else:
            candidate = []
            candidate_ = []

            for i in list(trie.keys()):
                if ED.py_edit_distance(''.join(lazy_pinyin(i)), query) <= 1:
                    candidate.append(''.join(lazy_pinyin(i)))
            print(candidate)
            for ii in candidate:
                candidate_.append(trie[ii])
            print("寻找编辑距离为1的候选集:", candidate_)
    else:
        candidate = []
        candidate_ = []
        for i in list(trie.keys()):
            if ED.py_edit_distance(''.join(lazy_pinyin(i)), query) <= 1:
                candidate.append(''.join(lazy_pinyin(i)))
        print(candidate)
        for ii in candidate:
            candidate_.append(trie[ii])
        print("寻找编辑距离为1的候选集:", candidate_)
    # 1.首先有没有在词典的拼音相似度
    # 2.如果有我们看是不是存在跟原词一样的 找出候选解 原query是否在里面 如果在说明没有错直接return []，没有的话进行纠错召回候选解 return list
    # 3.如果没有拼音倒排索引 最近的那个相似度  找出候选解 return list
    return candidate_

#基于拼音或者字面编辑距离的优化
#pinyin_main("牛乃")


"""
基于ngram纠错的逻辑
"""
def _get_maybe_error_index(scores, ratio=0.6745, threshold=2):
    """
    取疑似错字的位置，通过平均绝对离差（MAD）
    :param scores: np.array
    :param ratio: 正态分布表参数
    :param threshold: 阈值越小，得到疑似错别字越多
    :return: 全部疑似错误字的index: list
    """
    result = []
    scores = np.array(scores)
    if len(scores.shape) == 1:
        scores = scores[:, None]
    median = np.median(scores, axis=0)  # get median of all scores
    margin_median = np.abs(scores - median).flatten()  # deviation from the median
    # 平均绝对离差值
    med_abs_deviation = np.median(margin_median)
    if med_abs_deviation == 0:
        return result
    y_score = ratio * margin_median / med_abs_deviation
    # 打平
    scores = scores.flatten()
    maybe_error_indices = np.where((y_score > threshold) & (scores < median))
    # 取全部疑似错误字的index
    result = [int(i) for i in maybe_error_indices[0]]
    return result


def _get_maybe_error_index_by_stddev(scores, n=2):
    """
    取疑似错字的位置，通过平均值上下n倍标准差之间属于正常点
    :param scores: list, float
    :param n: n倍
    :return: 全部疑似错误字的index: list
    """
    std = np.std(scores, ddof=1)
    mean = np.mean(scores)
    down_limit = mean - n * std
    upper_limit = mean + n * std
    maybe_error_indices = np.where((scores > upper_limit) | (scores < down_limit))
    # 取全部疑似错误字的index
    result = list(maybe_error_indices[0])
    return result


# 2-gram找个纠错的分布
# 检错阶段 还有 回填机制
PUNCTUATION_LIST = ".。,，,、?？:：;；{}[]【】“‘’”《》/!！%……（）<>@#$~^￥%&*\"\'=+-_——「」"
def is_alphabet_string(string):
    """判断是否全部为英文字母"""
    for c in string:
        if c < 'a' or c > 'z':
            return False
    return True

def is_filter_token(token):
    result = False
    # pass blank
    if not token.strip():
        result = True
    # pass punctuation
    if token in PUNCTUATION_LIST:
        result = True
    # pass num
    if token.isdigit():
        result = True
    # pass alpha
    if is_alphabet_string(token.lower()):
        result = True
    return result
def min_numpy(numps, pred=2): #目的是为了扩大阈值附近数值的方差，让差异化更明显
    indexs = np.argmin(numps, axis=0)
    for i, j in zip(indexs, range(6)):
        numps[i][j] = pred * numps[i][j]
    return numps
def ngram_check(sentence):
    """
    :param query: 针对搜索query 进行处理的 进行双向n-gram语言模型检错
    :return:
    """
    # 按照不同的分隔符进行分割
    ngram_avg_scores = []
    for n in [2, 3, 4]:
        scores = []
        length = len(sentence)
        sentences = ["<s>"] * (n - 1) + sentence + ['</s>'] * (n - 1)  # S我要吃饭了
        for i in range(n - 1, length + n - 1):
            word = sentences[i - n + 1:i + 1]
            score = ngram.score(" ".join(word))
            scores.append(score)
        if not scores:
            continue
        ngram_avg_scores.append(scores)
    # 取拼接后的n-gram平均得分
    remember_score = np.array(ngram_avg_scores).T
    for i in range(len(sentence)):
        print('正向n_gram:' + str(sentence[i]) + "  " + "分数：" + str(remember_score[i]))
    ngram_avg_scores_ni = []
    length = len(sentence)
    for n in [2, 3, 4]:
        scores = []
        sentences = ["<s>"] * (n - 1) + sentence + ['</s>'] * (n - 1)
        for i in range(n - 1, length + n - 1):
            word = sentences[i:i + n]
            score = ngram.ni_score(" ".join(word))
            scores.append(score)
        if not scores:
            continue
        ngram_avg_scores_ni.append(scores)
    # n逆序n-gram平均得分 帮我报小发票
    remember_score = np.array(ngram_avg_scores_ni).T
    for i in range(len(list(sentence))):
        print('后向n_gram:' + str(sentence[i]) + "  " + "分数：" + str(remember_score[i]))
    ngram_avg_scores.extend(ngram_avg_scores_ni)
    # print(ngram_avg_scores)
    ngram_avg_scores_finally = min_numpy(ngram_avg_scores)
    # print(ngram_avg_scores_finally)
    sent_ni_scores = list(np.sum(np.array(ngram_avg_scores_finally), axis=0))
    scores_end = np.sum(np.array([sent_ni_scores]), axis=0) / 7
    # log.info('输出的平均分数:' + str(scores_end))
    return scores_end, remember_score




