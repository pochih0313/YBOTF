import math
import jieba
import time

class BM25(object):
    def __init__(self, docs):
        self.D = len(docs) ##文檔數量
        self.avgdl = sum([len(docs[i])+0.0 for i in range(len(docs))]) / self.D
        self.docs = docs
        self.f = []  # 列表的每一个元素是一个dict，dict存储着一个文档中每个词的出现次数
        self.df = {} # 存储每个词及出现了该词的文档数量
        self.idf = {} # 存储每个词的idf值
        self.k1 = 1.5
        self.b = 0.75
        self.init()

    def init(self):
        for i in range(len(self.docs)):
            tmp = {}
            for j in range(len(self.docs[i])):
                tmp[self.docs[i][j]] = tmp.get(self.docs[i][j], 0) + 1  # 存储每个文档中每个词的出现次数
            self.f.append(tmp)
            #print(tmp)
            for k in tmp.keys():
                self.df[k] = self.df.get(k, 0) + 1
        for k, v in self.df.items():
            self.idf[k] = math.log(self.D-v+0.5)-math.log(v+0.5)
        #print(self.f)

    def sim(self, doc, index):
        score = 0
        #print(doc)
        for i in range(len(doc)):
            #print(doc[i])
            #print(self.f)
            #print(self.f[index][i])
            if doc[i] not in self.f[index]:
                continue
            d = len(self.docs[index])
            #print(d)
            score += (self.idf[doc[i]]*self.f[index][doc[i]]*(self.k1+1)/(self.f[index][doc[i]]+self.k1*(1-self.b+self.b*d/self.avgdl)))
        return score


    def simall(self, doc):
        scores = []
        for index in range(self.D):
            score = self.sim(doc, index)
            scores.append(score)
        return scores


def q_a(query, docs, qa):
    words = [] #query分詞後
    scores = []

    """
    with open('Gossiping-QA-Dataset.txt','r',encoding='utf-8') as dataset:
        for line in dataset:
            line = line.strip('\n')
            q,a = line.split('\t')
            qa.append([q,a])
            question.append(q)

    with open('Q&A.txt','r',encoding='utf-8') as dataset:
        for line in dataset:
            line = line.strip('\n')
            q,a = line.split('\t')
            qa.append([q,a])
            question.append(q)
    

    start = time.time()
    f = open('segResult.txt', 'w', encoding = 'UTF-8')
    for i in range(len(qa)): #分詞
        if(i%5000 == 0):
            print("loading...")
        l = list(jieba.cut(qa[i][0]))
        for item in l:
            f.write("%s " % item)
        f.write("\n")
    print("time of segmentation: %f sec"%(time.time()-start))

    with open('segResult.txt','r',encoding='utf-8') as dataset:
        for line in dataset:
            line = line.strip('\n')
            #doc = []
            docs.append(line.split(' '))
            #docs.append(doc)
            #question.append(q)     
    """
    #print(docs)

    bm25 = BM25(docs)
    words = list(jieba.cut(query)) #斷詞
    #query = input()
    #query = "你是不是腦殘"

    print(words)
    scores = bm25.simall(words)
    index = scores.index(max(scores))
    maxx = max(scores)/bm25.sim(docs[index], index) #獲取文本相似比例
    print(docs[index])
    similarity = maxx*100 
    #print(docs[index])
    
    print(similarity)
    print(max(scores))
    print(bm25.sim(docs[index], index))
    print(qa[index][0])
    print(qa[index][1])
    return qa[index][1], similarity
    #score = bm25.sim(words, 0)
    #scores.append(score)
    