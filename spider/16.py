import random
import requests
import multiprocessing
import pandas as pd
from bs4 import BeautifulSoup

'''
    多进程 爬取豆瓣电影TOP250
'''

BASE_URl = 'https://movie.douban.com/top250?start='
UA = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 '           
      'Safari/600.7.12',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) '                  
      'Version/5.1 Safari/534.50 ',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
      ]


def request_douban(url):
    try:
        response = requests.request(
            'GET',
            url,
            headers={
                'User-agent': random.choice(UA)
            }
        )
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def drink_soup(soup):

    list = soup.find(class_='grid_view').find_all('li')
    for item in list:
        item_name = item.find(class_='title').string
        item_img = item.find('a').find('img').get('src')
        item_director = item.find('p').text
        item_star = item.find(class_='rating_num').string
        item_inq = item.find(class_='inq').text if item.find(class_='inq') else ' '
        # print('爬取电影：' + item_index + ' | ' + item_name + ' | ' + item_director + ' | ' + item_inq)
        df = pd.DataFrame(
            {'name': item_name, 'img': item_img, 'author': item_director, 'star': item_star,
             'synopsis': item_inq}, index=[0])
        df.to_csv(u'豆瓣最受欢迎的250部电影.csv', mode='a')


def get_movie(url):

    html = request_douban(url)
    soup = BeautifulSoup(html, 'lxml')
    drink_soup(soup)


if __name__ == '__main__':
    urls = []
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    for page in range(0, 11):
        url = BASE_URl + str(page * 25) + '&filter='
        urls.append(url)

    pool.map(get_movie, urls)
    pool.close()
    pool.join()
    movies = pd.read_csv(u'static/豆瓣最受欢迎的250部电影.csv', encoding='utf-8').drop_duplicates().dropna(how='any')  # 去掉重复行及含有NaN的行
    movies.to_excel(u'豆瓣最受欢迎的250部电影.xlsx', sheet_name='豆瓣电影TOP250')
