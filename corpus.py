#coding=utf8

import jieba.posseg as pseg
from gensim import corpora
from gensim import utils

'''
Generate raw corpus from text file, using jieba(https://github.com/fxsjy/jieba) to do text segmentation
'''
class RawCorpus(object):
        '''
        constructor for raw corpus.

        @parameters:
            corpus_file_name, string: the full file path of raw texts, in which each line is a weibo
            clean, boolean: raw texts need clean or not. if not, to clean @.
            pos_list, list; using position of speech to remove stopword
        '''
        def __init__(self, corpus_file_name, clean = True, pos_list=['ad','vn','an','nz','nr','ns','nt','v','nrt','a','b','i','f','j','l','n','s','z']):
                self.corpus_file_name = corpus_file_name
                self.clean = clean
                self.preserved_pos = set()
                for ele in pos_list:
                        self.preserved_pos.add(ele)
                        
        '''
        iterator that generates the word of weibo
        '''
        def __iter__(self):
                for line in open(self.corpus_file_name).xreadlines():
                        if not self.clean:
                                line = self.clean_at(line)
                        yield [w.word for w in pseg.cut(line) if w.flag in self.preserved_pos]

        '''
        clean the weibo with @, such as '@xxx'.

        @parameters:
            text, string: text that need to be cleand

        @return:
            cleaned text 
        '''
        def clean_at(self, text):
                while text:
                        start, end = (-1, -1)
                        start = text.find("//@")
                        if start == -1:
                                break
                        end = text.find(":", start+1)
                        if end == -1:
                                break
                        text = text[0:start] + text[end+1:]
                while text:
                        start, end = (-1, -1)
                        start = text.find("@")
                        if start == -1:
                                break
                        end = text.find(" ", start+1)
                        if end == -1:
                                end = text.find(":", start+1)
                                if end == -1:
                                        text = text[0:start]
                                        break
                        text = text[0:start] + text[end+1:]
                return text.strip()

'''
Based on RawCorpus, the clean corpus remove stopword and words that only occur once.
At the same time, the CleanCorpus transfer the word list to format form that can be used in other text analysis, such as LDA, LSI.
'''
class CleanCorpus(object):
        def __init__(self, corpus_file_name, stopwords_file_name):
                self.raw_corpus = RawCorpus(corpus_file_name)
                self.dictionary = corpora.Dictionary(wordlist for wordlist in self.raw_corpus)
                stop_ids = []
                for stopwordlist in RawCorpus(stopwords_file_name):
                        for stopword in stopwordlist:
                                # stopword = utils.to_utf8(stopword) ## texts coded with utf-8 need to transfer
                                if stopword in self.dictionary.token2id:
                                        stop_ids.append(self.dictionary.token2id[stopword])
                once_ids = [tokenid for tokenid, docfreq in self.dictionary.dfs.iteritems() if docfreq == 1]
                # print stop_ids[:10]
                # print once_ids[:10]
                self.dictionary.filter_tokens(stop_ids + once_ids)
                self.dictionary.compactify()

        def __iter__(self):
                for wordlist in self.raw_corpus:
                        yield self.dictionary.doc2bow(wordlist)

        def save_dict(self, dict_filename):
                self.dictionary.save(dict_filename)

'''
Generate corpus for Word2vec
'''                
class Word2vecCorpus(object):
        def __init__(self, corpus_file_name, stopword_file_name, pos_list=['ad','vn','an','nz','nr','ns','nt','v','nrt','a','b','i','f','j','l','n','s','z']):
                self.corpus_file_name = corpus_file_name
                self.preserved_pos = set()
                self.stopword = set()
                for ele in pos_list:
                        self.preserved_pos.add(ele)
                for wordlist in RawCorpus(stopword_file_name):
                        for word in wordlist:
                              self.stopword.add(word)  
        def __iter__(self):
                for line in open(self.corpus_file_name).xreadlines():
                        line = self.clean_at(line)
                        yield [w.word for w in pseg.cut(line) if w.flag in self.preserved_pos and w.word not in self.stopword]

        def clean_at(self, text):
                while text:
                        start, end = (-1, -1)
                        start = text.find("//@")
                        if start == -1:
                                break
                        end = text.find(":", start+1)
                        if end == -1:
                                break
                        text = text[0:start] + text[end+1:]
                while text:
                        start, end = (-1, -1)
                        start = text.find("@")
                        if start == -1:
                                break
                        end = text.find(" ", start+1)
                        if end == -1:
                                end = text.find(":", start+1)
                                if end == -1:
                                        text = text[0:start]
                                        break
                        text = text[0:start] + text[end+1:]
                return text.strip()
                
# util tool for parse doc                        
def clean_at(text):
        while text:
                start, end = (-1, -1)
                start = text.find("//@")
                if start == -1:
                        break
                end = text.find(":", start+1)
                if end == -1:
                        break
                text = text[0:start] + text[end+1:]
        while text:
                start, end = (-1, -1)
                start = text.find("@")
                if start == -1:
                        break
                end = text.find(" ", start+1)
                if end == -1:
                        end = text.find(":", start+1)
                        if end == -1:
                                text = text[0:start]
                                break
                text = text[0:start] + text[end+1:]
        return text.strip()

# parse the doc with word2vec model
def parse_doc(word2vec_model, doc):
        doc = clean_at(doc)
        return [w.word for w in pseg.cut(doc) if w.word in word2vec_model]

if __name__ == '__main__':
        pass
