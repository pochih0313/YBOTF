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


a = []
tmp = ""
q = ""
f = open('data/dialog/q&a2_fix.txt','w',encoding = 'utf-8')
with open('data/dialog/q&a2.txt','r',encoding='utf-8') as dataset:
    for line in dataset:
        line = line.strip('\n')
        #print(line)
        
        if(line[0] == '/'):
            if(a != []):
                qa.append([q[1],a])
                q = ""
                a.clear
            q = line.split('/')
            f.write(line)
            f.write("\n")
        else:
            tmp = tmp + line
            if(line[len(line)-1] != '，'):
                tmp.replace("。"," ")
                a.append(tmp)
                f.write(tmp)
                f.write("\n")
                tmp = ""  
        
    print(qa)
            #print(line[0])
        #q,a = line.split('\t')
        #qa.append([q,a])
"""

ans = []
with open('data/dialog/q&a2_fix.txt','r',encoding='utf-8') as dataset:
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
f = open('data/segmentation/segResult2_1.txt', 'w', encoding = 'UTF-8')
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
qa.clear()
print("time of segmentation: %f sec"%(time.time()-start))