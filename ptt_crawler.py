import urllib.parse
import re
import requests
import time
from requests_html import HTML
from bs4 import BeautifulSoup
from six import u

domain = 'http://www.ptt.cc/'
start_url = 'https://www.ptt.cc/bbs/sex/index.html'

def fetch(ur1): #獲得原始碼
    response = requests.get(ur1, cookies={'over18': '1'})
    return response

def parse_article_entries(doc): #找到標題
    html = HTML(html=doc)
    post_entries = html.find('div.r-ent')
    return post_entries

def parse_article_meta(entry): #標題資訊抓取
    meta['title'] = entry.find('div.title', first=True).text

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

def get_url(url): #取得圖片url
    resp = fetch(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    main_content = soup.find(id = "main-content")

    img_urls = []
    for url in main_content.find_all('a', recursive = False):
        if url.get('href').startswith('https://i.imgur.com'):
            img_urls.append(url.get('href'))
    return img_urls

#******************************************main*************************************#
if __name__ == '__main__':
    n = int(input("Pages:"))

    start = time.time()
    metadata = get_paged_meta(start_url, num_pages=n)
    link = [urllib.parse.urljoin(domain, meta['link']) 
            for meta in metadata if 'link' in meta]
    print("preparing time: %f sec" % (time.time()-start))

    #*****Crawling pictures url*****# 
    point = time.time()
    
    urls = []
    f = open('data/img1_url.txt', 'w')
    for i in range(len(link)):
        urls = get_url(link[i])
        for j in range(len(urls)):
            f.write(urls[j])
            f.write("\n")
        print('time of crawling and writing data: %f sec' % (time.time()-point))

    print('total time: %f sec' % (time.time()-start))
    print("Done!")

