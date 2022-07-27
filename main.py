import time

import numpy as np

from detect import ngram_check, is_filter_token
def main():
    sentence=input("sentence输入：")
    a=time.time()
    ress=[]
    score_ng, back_score = ngram_check(list(sentence))  # 判定我们的结果要不要继续纠错  这里另外考虑我们的后向得情况
    res = list(np.where(score_ng < -4.6)[0])
    print(np.where(back_score.T <= -10))
    res2 = list(np.where(back_score.T <= -10)[1])  # 查找我们的后向有问题索引
    res.extend(res2)
    # res = set(res)-set(res2)
    for i in res:
        token = sentence[i]
        if is_filter_token(token):
            continue
        ress.append([token,i])
    print(sorted(ress, key=lambda k: k[1], reverse=False))
    b = time.time()
    print(b-a)