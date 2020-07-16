import os
import requests
import concurrent
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


def request_page(url):
    try:
        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def get_page_urls():

    for i in range(1, 250):
        base_url = 'https://www.mzitu.com/page/{}'.format(str(i))
        html = request_page(base_url)
        soup = BeautifulSoup(html, 'lxml')
        list = soup.find(class_='postlist').find_all('li')
        urls = []
        for item in list:
            url = item.find('span').find('a').get('href')
            print('页面链接：%s' % url)
            urls.append(url)

        return urls


def header(referer):
    headers = {
        'Host': 'i.mzitu.net',
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.106 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Upgrade - Insecure - Requests': 1,
        'Referer': '{}'.format(referer),
    }

    return headers


def download_Pic(title, image_list):
    os.mkdir(title)
    j = 1
    for item in image_list:
        filename = '%s/%s.jpg' % (title, str(j))
        print('downloading....%s : NO.%s' % (title, str(j)))
        with open(filename, 'wb') as f:
            f.write(requests.get(item, headers=header(item)).content)
        j+=1


def download(url):
    html = request_page(url)
    soup = BeautifulSoup(html, 'lxml')
    total = soup.find(class_='pagenavi').find_all('a')[-2].find('span').string
    title = soup.find('h2').string
    image_list = []

    for i in range(int(total)):
        html = request_page(url + '/%s'%(i+1))
        soup = BeautifulSoup(html, 'lxml')
        img_url = soup.find('img').get('src')
        image_list.append(img_url)

    download_Pic(title, image_list)


def download_all_images(list_page_urls):
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as exector:
        for url in list_page_urls:
            exector.submit(download, url)


if __name__ == '__main__':
    list_page_urls = get_page_urls()
    download_all_images(list_page_urls)