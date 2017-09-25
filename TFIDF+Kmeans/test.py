# coding=utf-8
import  jieba.analyse
import  os
import numpy as np
from sklearn.cluster import KMeans
import codecs

def read_from_file(file_name):
    with open(file_name,"r",encoding="UTF-8") as fp:
        words = fp.read()
    return words

# file_name="/Users/wuyuhang/PycharmProjects/Test2/userdict.txt";
# words=read_from_file(file_name)
# print(words)

def stop_words(stop_word_file):
    words = read_from_file(stop_word_file)
    result = jieba.cut(words)
    new_words = []
    for r in result:
        new_words.append(r)
    return set(new_words) #返回时转换为set集合

def del_stop_words(words,stop_words_set):
#   words是已经切词但是没有去除停用词的文档。？？->words是原始文档的字符串
#   返回的会是去除停用词后的文档
    result = jieba.cut(words)
    new_words = []
    for r in result:
        if r not in stop_words_set:
            if r.replace('.','',1).isdigit():
                continue
            else:
                new_words.append(r)
    return new_words

#file_path传入文件夹，stop_words_set传入停用词表set
def get_all_vector(file_path,stop_words_set):
    #os.path.join(file_path,file) 把目录和文件名合成一个路径
    #os.listdir() 方法用于返回指定的文件夹包含的文件或文件夹的名字的列表
    #file_path:/Users/wuyuhang/PycharmProjects/Test2/files
    file_stopwords="/Users/wuyuhang/PycharmProjects/Test2/stop_word_file.txt"
    jieba.analyse.set_stop_words(file_stopwords)
    names = [ os.path.join(file_path,file) for file in os.listdir(file_path) ]
    new_names=[]
    for file in os.listdir(file_path):
        new_names.append(file)
    #posts中是一个个文本字符串

    posts = [ open(name,'r',encoding="GB18030").read() for name in names ]
    docs = []
    word_set = set()

    for post in posts: #post是一个文本string
        # doc = del_stop_words(post,stop_words_set) #doc是词汇表
        doc=jieba.analyse.extract_tags(post,topK=30,withWeight=False)
        docs.append(doc)
        word_set |= set(doc)  #|表示取并集word_set表示了所有的词汇合集（不重复）
        #print len(doc),len(word_set)
    save_key_words(docs)
    word_set = list(word_set)


    docs_vsm = []
    #for word in word_set[:30]:
        #print word.encode("utf-8"),
    for doc in docs:
        temp_vector = []
        for word in word_set:
            temp_vector.append(doc.count(word) * 1.0)
        #print temp_vector[-30:-1]
        docs_vsm.append(temp_vector)

    docs_matrix = np.array(docs_vsm) #产生了多维数组
    # nonzero(a)返回数组a中值不为零的元素的下标
    column_sum = [float(len(np.nonzero(docs_matrix[:, i])[0])) for i in
                  range(docs_matrix.shape[1])]  # column_sum代表每一个词汇出现的次数的集合
    column_sum = np.array(column_sum)  # 将column_sum变为array
    # IDF由总文件数目除以包含该词语之文件的数目，再将得到的商取对数得到
    column_sum = docs_matrix.shape[0] / column_sum
    idf = np.log(column_sum)
    idf = np.diag(idf)  # np.diag构建对角矩阵
    # 请仔细想想，根绝IDF的定义，计算词的IDF并不依赖于某个文档，所以我们提前计算好。
    # 注意一下计算都是矩阵运算，不是单个变量的运算。
    docs_matrix_fix = []


    word_sum = 0.0  # word_sum表示所有文本的总词数
    for row in docs_matrix:
        word_sum+=row.sum()

    for doc_v in docs_matrix:  # 一行行遍历
        if doc_v.sum() == 0:
            doc_v = doc_v / 1
            docs_matrix_fix.append(doc_v)
        else:
            doc_v = doc_v / word_sum
            docs_matrix_fix.append(doc_v)
    docs_matrix_fix=np.array(docs_matrix_fix)
    tfidf = np.dot(docs_matrix_fix, idf)  # dot表示矩阵点积

    sum_num=0
    temp=0
    dict={}
    tfidf=np.array(tfidf)
    for i in range(tfidf.shape[1]):
        temp=0
        for j in tfidf[:,i]:
            temp+=j
        dict[temp]=tfidf[:,i]
    dict=sorted(dict.items(),key=lambda e:e[0],reverse=True)
    count=0
    new_tfidf=[]
    for key in dict:
        if(count>10000):
            break
        new_tfidf.append(key[1])
        count+=1
    new_tfidf=np.array(new_tfidf)
    new_tfidf=new_tfidf.transpose()
    return new_names,tfidf


def K_Means(weight):
    print('Start Kmeans:')

    clf = KMeans(n_clusters=20)  # n_clusters表示质心数
    s = clf.fit(weight)
    print("s:")
    print(s)

    # 2个中心点
    print("clf.cluster_centers_:")
    print(clf.cluster_centers_)

    # 每个样本所属的簇
    print("clf.labels_:")
    print(clf.labels_)
    print("------------------------------------------------------------")
    i = 1
    while i <= len(clf.labels_):
        print(i, clf.labels_[i - 1])
        i = i + 1

        # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
    print(clf.inertia_)
    return clf.labels_


def save_key_words(docs):
    result=codecs.open("key_words.txt",'w','GBK')
    for row in docs:
        for col in row:
            result.write(col)
            result.write('  ')
        result.write('\r\n')

    result.close()