import json
import random
import requests
import xlwt
import pandas as pd

from bs4 import BeautifulSoup

'''
    爬取豆瓣电影TOP250
'''

BASE_URl = 'https://movie.douban.com/top250?start='
UA = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 '           
      'Safari/600.7.12',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) '                  
      'Version/5.1 Safari/534.50 ',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
      ]

# book = xlwt.Workbook(encoding='utf-8', style_compression=0)
#
# sheet = book.add_sheet('豆瓣电影top250', cell_overwrite_ok=True)
# sheet.write(0, 0, 'name')
# sheet.write(0, 1, 'img')
# sheet.write(0, 2, 'index')
# sheet.write(0, 3, 'author')
# sheet.write(0, 4, 'star')
# sheet.write(0, 5, 'synopsis')


def request_douban(BASE_URl, page):
    try:
        response = requests.request(
            'GET',
            BASE_URl + str(page*25) + '&filter=',
            headers={
                'User-agent': random.choice(UA)
            }
        )
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def drink_soup(soup, book = None):
    list = soup.find(class_='grid_view').find_all('li')
    # sheet = book.get_sheet('豆瓣电影top250')
    for item in list:
        item_name = item.find(class_='title').string
        item_img = item.find('a').find('img').get('src')
        item_index = item.find(class_='').string
        item_director = item.find('p').text
        item_star = item.find(class_='rating_num').string
        item_inq = item.find(class_='inq').text if item.find(class_='inq') else ' '
        # print('爬取电影：' + item_index + ' | ' + item_name + ' | ' + item_director + ' | ' + item_inq)
        df = pd.DataFrame({'name': item_name, 'img': item_img, 'index': item_index, 'author': item_director, 'star': item_star, 'synopsis':item_inq}, index=[0])
        df.to_csv(u'豆瓣最受欢迎的250部电影.csv', mode='a')


if __name__ == '__main__':
    for page in range(0, 11):
        html = request_douban(BASE_URl, page)
        soup = BeautifulSoup(html, 'lxml')
        drink_soup(soup)
    movies = pd.read_csv(u'static/豆瓣最受欢迎的250部电影.csv')
