import numpy as np
from pypinyin import lazy_pinyin

class text_feature_generator:
    """
    edit_distance: 中文编辑距离
    py_edit_distance: 拼音编辑距离
    edit_dist_cn_for_word1: 中文编辑编辑距离/Query1长度
    edit_dist_cn_for_word2: 中文编辑编辑距离/Query2长度
    py_edit_dist_py_for_word1: 拼音编辑编辑距离/Query1长度
    py_edit_dist_py_for_word2: 拼音编辑编辑距离/Query2长度
    is_same_prefix: 是否相同前缀
    is_same_postfix: 是否相同尾缀
    query_length: word1，word2长度
    """

    def edit_distance(self, word1, word2):
        len1 = len(word1)
        len2 = len(word2)
        dp = np.zeros((len1 + 1, len2 + 1))
        for i in range(len1 + 1):
            dp[i][0] = i
        for j in range(len2 + 1):
            dp[0][j] = j
        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                delta = 0 if word1[i - 1] == word2[j - 1] else 1
                dp[i][j] = min(dp[i - 1][j - 1] + delta, min(dp[i - 1][j] + 1, dp[i][j - 1] + 1))
        return dp[len1][len2]

    def py_edit_distance(self, word1, word2):
        # word1 = ''.join(lazy_pinyin(word1))
        # word2 = ''.join(lazy_pinyin(word2))
        return self.edit_distance(word1, word2)

    def edit_dist_cn(self, word1, word2):
        dist_ratio = self.edit_distance(word1, word2)
        return dist_ratio

    # def edit_dist_cn_for_word2(self, word1, word2):
    #     dist_ratio = self.edit_distance(word1, word2) / len(word2)
    #     return dist_ratio

    def py_edit_dist_py_for_word1(self, word1, word2):
        dist_ratio = self.py_edit_distance(word1, word2) / len(''.join(lazy_pinyin(word1)))
        return dist_ratio

    def py_edit_dist_py_for_word2(self, word1, word2):
        dist_ratio = self.py_edit_distance(word1, word2) / len(''.join(lazy_pinyin(word2)))
        return dist_ratio

    def is_same_prefix(self, word1, word2):
        if word1[0] == word2[0]:
            return True
        else:
            return False

    def is_same_postfix(self, word1, word2):
        if word1[-1] == word2[-1]:
            return True
        else:
            return False

    def is_word2_prefix(self, word1, word2):
        try:
            if word1 in word2[1:]:
                return True
            else:
                return False
        except:
            print(word1, word2)

    def is_word1_prefix(self, word1, word2):
        if word2 in word1[1:]:
            return True
        else:
            return False

    def coverage_rate(self, word1, word2):
        min_len = min(len(word1), len(word2))
        word_max = word1 if len(word1) > len(word2) else word2
        word_min = word1 if len(word1) < len(word2) else word2
        cnt = 0
        for i in word_max:
            if i in word_min:
                cnt += 1
        return cnt / min_len

    def query_length(self, word):
        return len(word)


# print(text_feature_generator().py_edit_distance('sshi打水','苏打水'))