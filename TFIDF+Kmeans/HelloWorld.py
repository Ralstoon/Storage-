import test
import  show_Kmeans
import  time
from  gensim import corpora
from gensim import models
import  codecs
# 测试文件夹/Users/wuyuhang/PycharmProjects/Test2/textFiles

def generater_Kmeans():
    start = time.clock()
    stop_word_file = "/Users/wuyuhang/PycharmProjects/Test2/stop_word_file.txt";
    stop_words = test.stop_words(stop_word_file);

    file_path = "/Users/wuyuhang/PycharmProjects/Test2/files"
    names, tfidf = test.get_all_vector(file_path, stop_words)

    clf_labels = test.K_Means(tfidf)
    show_Kmeans.Merge_show(names, clf_labels)

    end = time.clock()

    print("===========================")
    print("Running time : %s Seconds " % (end - start))

class MyWords(object):
    def __init__(self,file_name):
        self.file_name=file_name
    def __iter__(self):
        for line in open(self.file_name,encoding='GB18030'):
            yield line.strip().split()


def get_key_words_and_saveDict():
    File_original_key_words='/Users/wuyuhang/PycharmProjects/Test2/key_words.txt'
    words=MyWords(File_original_key_words)
    dictionary=corpora.Dictionary(words)
    dictionary.save('/Users/wuyuhang/PycharmProjects/Test2/save/dict.dict')

def generator_corpus_and_tfidfModel():
    dict=corpora.Dictionary.load('/Users/wuyuhang/PycharmProjects/Test2/save/dict.dict')
    File_original_key_words='/Users/wuyuhang/PycharmProjects/Test2/key_words.txt'
    texts=MyWords(File_original_key_words)
    corpus = [dict.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('/Users/wuyuhang/PycharmProjects/Test2/save/corpus.mm',corpus)
    tfidf=models.TfidfModel(corpus)
    tfidf.save('/Users/wuyuhang/PycharmProjects/Test2/save/model.tfidf')


# generator_corpus_and_tfidfModel() #用于生成tfidf模型

def save_temp_file(docs):
    result=codecs.open("temp_file",'w','GBK')
    for row in docs:
        result.write(row)
        result.write('\r\n')

    result.close()

def sort_by_tfidf():
    corpus=corpora.MmCorpus('/Users/wuyuhang/PycharmProjects/Test2/save/corpus.mm')
    tfidf=models.TfidfModel.load('/Users/wuyuhang/PycharmProjects/Test2/save/model.tfidf')
    dict=corpora.Dictionary.load('/Users/wuyuhang/PycharmProjects/Test2/save/dict.dict')
    corpus_tfidf=tfidf[corpus]
    new_corpus_tfidf=[]
    temp=[]
    for i in corpus_tfidf:
        for j in i:
            temp.append(j)
    # save_temp_file(temp)
    for tep in sorted(temp,key=lambda x:-x[1]):
        new_corpus_tfidf.append(tep)
    # save_temp_file(new_corpus_tfidf)
    # print(new_corpus_tfidf)

    map_word=dict.token2id
    new_dict = {v: k for k, v in map_word.items()}
    # print(map_word)
    count=0
    word_set=set()
    for i in new_corpus_tfidf:
        if count>5000:
            break
        index=i[0] # value
        if i[0] in new_dict.keys():
            # print(map_word[i[0]])
            word_set.add(new_dict[i[0]])
        count+=1
    save_temp_file(word_set)
sort_by_tfidf()