import math
import jieba
import time

class BM25(object):
    def __init__(self, docs):
        self.docs = docs #所有文檔
        self.D = len(docs) #文檔數量
        self.avgdl = sum([len(docs[i])+0.0 for i in range(len(docs))]) / self.D #平均一個文檔的詞量
        self.tf = []  #列表的每一個元素是一個dict，dict儲存一個文檔中每個詞的出现次数
        self.df = {} #df,儲存每個詞以及出現該詞的文檔數量
        self.idf = {} #每個詞在語料庫中的頻率: 在語料庫中頻率愈高，重要性愈低（反比）
        self.k1 = 1.5 #最佳化參數
        self.b = 0.75 #值愈大，文章長度愈重要
        self.init()

    def init(self):
        for i in range(len(self.docs)):
            tmp = {}
            for j in range(len(self.docs[i])):
                tmp[self.docs[i][j]] = tmp.get(self.docs[i][j], 0) + 1  #儲存每個文檔中每個詞的出現次數
            self.tf.append(tmp)
            for k in tmp.keys():
                self.df[k] = self.df.get(k, 0) + 1
        for k, v in self.df.items():
            self.idf[k] = math.log(self.D-v+0.5)-math.log(v+0.5) #算idf值

    def sim(self, doc, index):
        score = 0
        for i in range(len(doc)):
            if doc[i] not in self.tf[index]:
                continue
            d = len(self.docs[index])
            score += (self.idf[doc[i]]*self.tf[index][doc[i]]*(self.k1+1)/(self.tf[index][doc[i]]+self.k1*(1-self.b+self.b*d/self.avgdl)))
        return score


    def simall(self, doc):  #計算query與所有文檔的相似度並回傳分數
        scores = []
        for index in range(self.D):
            score = self.sim(doc, index)
            scores.append(score)
        return scores


def q_a(query, docs, qa):
    words = [] #query分詞後
    scores = [] #matching分數

    bm25 = BM25(docs)
    words = list(jieba.cut(query)) #對query斷詞

    scores = bm25.simall(words)
    index = scores.index(max(scores))
    maxx = max(scores)/bm25.sim(docs[index], index) #獲取文本相似比例
    similarity = maxx*100 
    
    print("Matching score: ", similarity)
    print("Matched question: ",qa[index][0])
    print("Matched answer: ",qa[index][1])
    return qa[index][1], similarity #return對應答案與相似度