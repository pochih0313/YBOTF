import re
import requests
import time
from bs4 import BeautifulSoup

def fetch(ur1): #獲得原始碼
    response = requests.get(ur1)
    return response.text

def parse_article_entries(doc): #找到標題
    soup = BeautifulSoup(doc, 'html5lib')
    rows = soup.find_all('div', class_ = 'tr')
    colname = list(rows.pop(0).stripped_strings) #取得第1列當作colname
    return rows

def parse_article_meta(entry): #標題資訊抓取
    thisweek_rank = entry.find_next('div', attrs = {'class':'td'})
    updown = thisweek_rank.find_next('div')
    lastweek_rank = updown.find_next('div')

    if thisweek_rank.string == str(1): #排名第1
        movie_title = lastweek_rank.find_next('h2').text
    else:
        movie_title = lastweek_rank.find_next('div', attrs={'class':'rank_txt'}).text

    meta = {
        'title': movie_title,
        'link': lastweek_rank.find_next('a')['href']
    }
    return meta

#******************************************main*************************************#
#if __name__ == '__main__':
