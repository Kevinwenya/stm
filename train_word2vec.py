# coding=utf-8
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import corpus
from gensim import models, corpora

'''
Using gensim(https://radimrehurek.com/gensim/) to train word2vec model
'''
raw_doc_filename = r'sample_weibo.txt'
stopword_filename = r'stopwords.txt'

## 清理语料
clean_corpus = corpus.Word2vecCorpus(raw_doc_filename, stopword_filename)

## 训练模型
word2vec = models.Word2Vec(clean_corpus, window=5, min_count=5)

## 保存模型
word2vec.save('weibo_word2vec.model')

