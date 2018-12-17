import jieba
import time

qa = []
stopwords = []

"""
for line in open('data/dict/stopWord.txt','r'):
    stopwords.append(line.strip('\n'))

with open('data/dialog/Gossiping-QA-Dataset.txt','r',encoding='utf-8') as dataset:
    for line in dataset:
        line = line.strip('\n')
        q,a = line.split('\t')
        qa.append([q,a])
    
start = time.time()
f = open('data/segmentation/segResult.txt', 'w', encoding = 'UTF-8')
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
qa.clear()
print("time of segmentation: %f sec"%(time.time()-start))

with open('data/dialog/q&a.txt','r',encoding='utf-8') as dataset:
    for line in dataset:
        line = line.strip('\n')
        q,a = line.split('\t')
        qa.append([q,a])

start = time.time()
f = open('data/segmentation/segResult0.txt', 'w', encoding = 'UTF-8')
for i in range(len(qa)): #分詞
    if(i%5000 == 0):
        print("loading...")
    l = list(jieba.cut(qa[i][0]))
    flag = 0
    for j in range(len(l)):
        if(flag == 1):
            f.write(" ")
        f.write("%s" % l[j])
        flag = 1
    f.write("\n")
qa.clear()
print("time of segmentation1: %f sec"%(time.time()-start))

with open('data/dialog/q&a1.txt','r',encoding='utf-8') as dataset:
    for line in dataset:
        line = line.strip('\n')
        q,a = line.split('\t')
        qa.append([q,a])

start = time.time()
f = open('data/segmentation/segResult1.txt', 'w', encoding = 'UTF-8')
for i in range(len(qa)): #分詞
    if(i%5000 == 0):
        print("loading...")
    l = list(jieba.cut(qa[i][0]))
    flag = 0
    for j in range(len(l)):
        if(flag == 1):
            f.write(" ")
        f.write("%s" % l[j])
        flag = 1
    f.write("\n")
qa.clear()
print("time of segmentation1: %f sec"%(time.time()-start))

with open('data/dialog/q&a1_2.txt','r',encoding='utf-8') as dataset:
    for line in dataset:
        line = line.strip('\n')
        q,a = line.split('\t')
        qa.append([q,a])

start = time.time()
f = open('data/segmentation/segResult1_2.txt', 'w', encoding = 'UTF-8')
for i in range(len(qa)): #分詞
    if(i%5000 == 0):
        print("loading...")
    l = list(jieba.cut(qa[i][0]))
    flag = 0
    for j in range(len(l)):
        if(flag == 1):
            f.write(" ")
        f.write("%s" % l[j])
        flag = 1
    f.write("\n")
qa.clear()
print("time of segmentation1: %f sec"%(time.time()-start))
"""
with open('data/dialog/q&a1_2.txt','r',encoding='utf-8') as dataset:
    for line in dataset:
        line = line.strip('\n')
        q,a = line.split('\t')
        qa.append([q,a])

start = time.time()
f = open('data/segmentation/segResult1_2.txt', 'w', encoding = 'UTF-8')
for i in range(len(qa)): #分詞
    if(i%5000 == 0):
        print("loading...")
    l = list(jieba.cut(qa[i][0]))
    flag = 0
    for j in range(len(l)):
        if(flag == 1):
            f.write(" ")
        f.write("%s" % l[j])
        flag = 1
    f.write("\n")
qa.clear()
print("time of segmentation1: %f sec"%(time.time()-start))
