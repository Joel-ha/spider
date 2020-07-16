import json
import random
import requests
import pandas as pd
import multiprocessing
from bs4 import BeautifulSoup

"""
    爬取当当书籍500
"""

UA = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 '
      'Safari/600.7.12',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) '
      'Version/5.1 Safari/534.50 ',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
      ]
BASE_URL = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-'


def request_dangdang(url):
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


def parse_html(html):
    # pattern = re.compile(r'<li>.*?list_num.*?(\d+).</div>.*?<img src="(.*?)".*?class="name".*?title="(.*?)">.*?class="star">.*?class="tuijian">(.*?)</span>.*?class="publisher_info">.*?target="_blank">(.*?)</a>.*?class="biaosheng">.*?<span>(.*?)</span></div>.*?<p><span\sclass="price_n">&yen;(.*?)</span>.*?</li>', re.S)
    # items = re.findall(pattern, html)
    # for item in items:
    #     yield {
    #         'range': item[0],
    #         'image': item[1],
    #         'title': item[2],
    #         'recommend': item[3],
    #         'author': item[4],
    #         'times': item[5],
    #         'price': item[6]
    #     }
    list = html.find(class_='bang_list').find_all('li')
    for item in list:
        item_img = item.find('img').get('src')
        item_name = item.find(class_='name').text
        item_author = item.find(class_='publisher_info').text
        item_recommend = item.find(class_='tuijian').text
        item_star = item.find(class_='biaosheng').text
        item_price = item.find(class_='price_n').text
        print('爬取book：' + item_name + ' | ' + item_author + ' | ' + item_price)
        df = pd.DataFrame(
            {'name': item_name, 'img': item_img, 'author': item_author, 'recommend': item_recommend,
             'star': item_star, 'price': item_price}, index=[0])
        df.to_csv(u'当当最受欢迎的500本书.csv', mode='a')


def get_book(url):
    html = request_dangdang(url)
    soup = BeautifulSoup(html, 'lxml')
    parse_html(soup)


if __name__ == '__main__':
    urls = []
    for page in range(1, 26):
        url = BASE_URL + str(page)
        urls.append(url)

    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    pool.map(get_book, urls)
    pool.close()
    pool.join()
    books = pd.read_csv(u'static/当当最受欢迎的500本书.csv', encoding='utf-8').drop_duplicates().dropna(how='any')
    books.to_excel(u'当当最受欢迎的500本书.xlsx', sheet_name='当当书籍TOP500')