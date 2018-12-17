#!/usr/bin/env python
# coding: utf-8

import urllib.parse
import re
import requests
#import jieba
import time
from requests_html import HTML
from bs4 import BeautifulSoup
from six import u
#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy

#from multiprocessing import Pool

# class define #
def fetch(ur1): #獲得原始碼
    response = requests.get(ur1)
    return response

def parse_article_entries(doc): #找到標題
    html = HTML(html=doc)
    post_entries = html.find('div.r-ent')
    return post_entries

def parse_article_meta(entry): #標題資訊抓取
    meta = {
        'title': entry.find('div.title', first=True).text,
        'push': entry.find('div.nrec', first=True).text,
        'date': entry.find('div.date', first=True).text,
        #'author': entry.find('div.author', first=True).text,
        #'link': entry.find('div.title > a', first=True).attrs['href'],
    }
    
    try:
        # 正常狀況取得資料
        meta['author'] = entry.find('div.author', first=True).text
        meta['link'] = entry.find('div.title > a', first=True).attrs['href']
    except AttributeError:
        # 但碰上文章被刪除時，就沒有辦法像原本的方法取得 作者 跟 連結
        if '(本文已被刪除)' in meta['title']:
            # e.g., "(本文已被刪除) [haudai]"
            match_author = re.search('\[(\w*)\]', meta['title'])
            if match_author:
                meta['author'] = match_author.group(1)
        elif re.search('已被\w*刪除', meta['title']):
            # e.g., "(已被cappa刪除) <edisonchu> op"
            match_author = re.search('\<(\w*)\>', meta['title'])
            if match_author:
                meta['author'] = match_author.group(1)
    return meta

def get_metadata_from(url): #從某一頁面取得內容

    def parse_next_link(doc):
        html = HTML(html=doc)
        controls = html.find('.action-bar a.btn.wide')
        link = controls[1].attrs.get('href')
        return urllib.parse.urljoin(domain, link)

    resp = fetch(url)
    post_entries = parse_article_entries(resp.text)
    next_link = parse_next_link(resp.text)

    metadata = [parse_article_meta(entry) for entry in post_entries]
    return metadata, next_link

def get_paged_meta(url, num_pages): #取得所有頁面內容
    collected_meta = []

    for _ in range(num_pages):
        posts, link = get_metadata_from(url)
        collected_meta += posts
        url = urllib.parse.urljoin(domain, link)

    return collected_meta

def get_posts(url): #取得文章內容
    resp = fetch(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    main_content = soup.find(id = "main-content")
    metas = main_content.select('div.article-metaline')

    url = []
    url = soup.find_all('a')['href']
    print(url)

    #url = soup.find_next('a')['href']

    filtered = [ v for v in main_content.stripped_strings 
                if v[0] not in [u'※', u'◆'] and v[:2] not in [u'--'] ]
    expr = re.compile(u(r'[^\u4e00-\u9fa5\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\s\w:/-_.?~%()]'))
    for i in range(len(filtered)):
        filtered[i] = re.sub(expr, '', filtered[i])

    filtered = [_f for _f in filtered if _f]  # remove empty strings
    #filtered = [x for x in filtered if article_id not in x]  # remove last line containing the url of the article
    content = ' '.join(filtered)
    content = re.sub(r'(\s)+', ' ', content)
    #post_link = [
    #    urllib.parse.urljoin(domain, meta['link']) 
    #    for meta in metadata if 'link' in meta]
    
    meta['link'] = entry.find('div.title > a', first=True).attrs['href']
    return url


domain = 'http://www.ptt.cc/'
start_url = 'https://www.ptt.cc/bbs/Beauty/index.html'

#******************************************main*************************************#
if __name__ == '__main__':

    n = int(input("Pages:"))

    start = time.time()
    metadata = get_paged_meta(start_url, num_pages=n)
    link = [urllib.parse.urljoin(domain, meta['link']) 
            for meta in metadata if 'link' in meta]

    #*****Segmentation*****# 
    post = ''
    seg_list = []

    for i in range(len(link)):
        contents = get_posts(link[i]) + '\n'
        seg = jieba.cut(contents)
        seg_list.append(' '.join(seg))
        post += contents

    print('time of crawling and segmentation: %f sec' % (time.time()-start)) 


    print("Done!")
    print('total time: %f sec' % (time.time()-start))





#print(metadata)
#print(link[1])

#for meta in metadata:
#    print(meta['link'])
#print(get_posts(metadata))
#print(post_entries)


#for post, resps in zip(metadata, resps):
#    print('{0} {1: <15} {2}, 網頁內容共 {3} 字'.format(
#        post['date'], post['author'], post['title'], len(resps.text)))




# In[ ]:




