from random import random
from urllib.request import urlopen, Request
import pprint

url = 'http://www.bing.com'
ua = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 '
      'Safari/600.7.12',
      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) '
      'Version/5.1 Safari/534.50 ',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
]

req = Request(
    url,
    headers={
        'User-agent': random.choice(ua)
    }
)

response = urlopen(req, timeout=5)
print(response.closed)

with response:
    print(type(response))
    print(response.status)
    print(response._method)
    print(response.read())
    print(response.info())
    pprint.pprint(response.geturl())

print(response.closed)