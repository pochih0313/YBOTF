import jieba
import time

stopwords = []
for line in open('data/dict/stopWord.txt','r'):
    stopwords.append(line.strip('\n'))

def seg(txt, result):
    qa = []
    with open(txt,'r',encoding='utf-8') as dataset:
        for line in dataset:
            line = line.strip('\n')
            q,a = line.split('\t')
            qa.append([q,a])
        
    start = time.time()
    f = open(result, 'w', encoding = 'UTF-8')
    for i in range(len(qa)): #分詞
        if(i%5000 == 0):
            print("loading...")
        l = list(jieba.cut(qa[i][0]))
        flag = 0
        for j in range(len(l)):
            if l[j] not in stopwords: #去stopword
                if(flag == 1):
                    f.write(" ")
                f.write("%s" % l[j])
                flag = 1
            #else:
                #print("stopword!%s"%item)
        f.write("\n")
    print("time of segmentation: %f sec"%(time.time()-start))

def seg1(txt, result):
    ans = []
    with open(txt,'r',encoding='utf-8') as dataset:
            q = []
            a = []
            for line in dataset:
                line = line.strip('\n')
                if(line[0] == '/'):
                    if(a != []):
                        for i in range(len(a)):
                            ans.append(a[i])
                        jieba.add_word(q[1], 3, 'n') #新增jieba辭典
                        q = []
                        a = []
                    q = line.split('/')
                else:
                    a.append(line)

    start = time.time()
    f = open(result, 'w', encoding = 'UTF-8')
    for i in range(len(ans)): #分詞
        if(i%5000 == 0):
            print("loading...")
        l = list(jieba.cut(ans[i]))
        flag = 0
        for j in range(len(l)):
            if l[j] not in stopwords: #去stopword
                if(flag == 1):
                    f.write(" ")
                f.write("%s" % l[j])
                flag = 1
            #else:
                #print("stopword!%s"%item)
        f.write("\n")
    print("time of segmentation: %f sec"%(time.time()-start))

#******************************************main*************************************#
if __name__ == '__main__':
    data1 = 'data/dialog/Gossiping-QA-Dataset.txt'
    data2 = 'data/dialog/q&a.txt'
    data3 = 'data/dialog/q&a1.txt'
    data4 = 'data/dialog/q&a2_fix.txt'
    result1 = 'data/segmentation/segResult.txt'
    result2 = 'data/segmentation/segResult0.txt'
    result3 = 'data/segmentation/segResult1.txt'
    result4 = 'data/segmentation/segResult2_1.txt'

    seg(data1, result1)
    seg(data2, result2)
    seg(data3, result3)
    seg1(data4, result4)