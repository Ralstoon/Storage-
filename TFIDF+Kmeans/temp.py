# coding=utf-8
from gensim import corpora
from gensim import models

# documents = ["Human machine interface for lab abc computer applications",
#     "A survey of user opinion of computer system response time",
#     "The EPS user interface management system",
#     "System and human system engineering testing of EPS",
#     "Relation of user perceived response time to error measurement",
#     "The generation of random binary unordered trees",
#     "The intersection graph of paths in trees",
#     "Graph minors IV Widths of trees and well quasi ordering",
#     "Graph minors A survey"]
#
#
# texts=[doc.lower().split() for doc in documents]
# dict=corpora.Dictionary(texts) #自建词典
# print(dict.token2id)


texts="123 33213 3222 31 "
texts = [re.split(, t.lower()) for t in texts]
    for t in texts:
        while '' in t:
            t.remove('')