# -*- coding: utf-8 -*-
"""
@Time ： 2022-07-27 10:41
@Auth ： Bingbing Zhou
@File ：cal_ngram.py
@IDE ：PyCharm
@EMAIL：13270870157@163.com

"""
import math
import time


class Ngram():
    def __init__(self):
        self.dicts, self.all_numbers = self.openfile()

    def openfile(self):
        res = {}
        with open('./data/ngram.txt', 'r', encoding='utf-8') as fr:
            for line in fr:
                x, y = line.split('%##%')
                res[x] = int(y)
        return res, res['总行数：']

    def ppl(self, sentence):
        # 计算bigram
        res2 = []
        res3 = []
        res4 = []
        ppl_scores = []
        sentence2 = ["<s>"] + list(sentence) + ["</s>"]
        # 计算2gram
        for i in range(len(sentence2) - 1):
            if sentence2[i:i + 2]:
                res2.append(self.score(" ".join(sentence2[i:i + 2])))
            else:
                break
        # 计算3gram
        sentence3 = ["<s>"] * 2 + list(sentence) + ["</s>"] * 2
        for i in range(len(sentence3) - 2):
            if sentence3[i:i + 3]:
                res3.append(self.score(" ".join(sentence3[i:i + 3])))
            else:
                break
        # 计算4gram
        sentence4 = ["<s>"] * 3 + list(sentence) + ["</s>"] * 3
        for i in range(len(sentence4) - 3):
            if sentence4[i:i + 4]:
                res4.append(self.score(" ".join(sentence4[i:i + 4])))
            else:
                break
        ppl_scores.append(sum(res2) / 4)
        ppl_scores.append(sum(res3) / 2)
        ppl_scores.append(sum(res4) / 4)
        return sum(ppl_scores)

    def score(self, token):
        tokens = token.split()
        # if len(tokens)==1:
        #     tokens=["<s>",token]
        # if " ".join(tokens[:-1])  not in self.dicts or " ".join(tokens) not in self.dicts:
        # if " ".join(tokens[:-1])  not in self.dicts and len(tokens[:-1])!=1:
        #     return -10
        if " ".join(tokens[1:]) not in self.dicts or " ".join(tokens) not in self.dicts:
            return -10
        if " ".join(tokens) not in self.dicts:
            return -10
        if tokens[:-1] == ['<s>'] or tokens[:-1] == ['<s>'] * 2 or tokens[:-1] == ['<s>'] * 3:
            freq = math.log10(self.dicts[" ".join(tokens)] / self.all_numbers)
            return freq
        freq = math.log10(self.dicts[" ".join(tokens)] / self.dicts[" ".join(tokens[:-1])])
        return freq

    def ni_score(self, token):
        tokens = token.split()
        if " ".join(tokens[1:]) not in self.dicts or " ".join(tokens) not in self.dicts:
            return -10
        if tokens[:-1] == ['<s>'] or tokens[:-1] == ['<s>'] * 2 or tokens[:-1] == ['<s>'] * 3:
            freq = math.log10(self.dicts[" ".join(tokens)] / self.all_numbers)
            return freq
        freq = math.log10(self.dicts[" ".join(tokens)] / self.dicts[" ".join(tokens[1:])])
        return freq
