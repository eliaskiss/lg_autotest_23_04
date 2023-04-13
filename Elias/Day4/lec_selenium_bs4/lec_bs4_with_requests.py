from bs4 import BeautifulSoup as bs
import time
import wget
import os
import requests

req = requests.get('https://movie.naver.com/movie/running/current.nhn')
html = req.text

header = req.headers
for key in header.keys():
    print('Header:', key)
    print('Value:', header[key])
    print('-' * 20)

status = req.status_code
print('Status:', status)

soup = bs(html, 'html.parser')
# soup = bs(html, 'lxml')
# soup = bs(html, 'lxml-xml') # Error
# soup = bs(html, 'xml') # Error
# soup = bs(html, 'html5lib')
ul = soup.select_one('.lst_detail_t1')
li_list = ul.select('li')

for li in li_list:
    detail_link = li.select_one('a')
    detail_link = 'https://movie.naver.com' + detail_link['href']
    # detail_link = 'https://movie.naver.com' + detail_link.get('href')
    print('Detail Link:', detail_link)

    code = detail_link.split('=')[1]
    print('Code:', code)

    thumb = li.select_one('img')
    thumb = thumb['src']
    print('Thumbnail url:', thumb)

    title = li.select_one('.tit')
    rating = title.select_one('span')
    rating = rating.text

    # 없는 경우 예외처리
    try:
        rating = title.select_one('span')
        rating = rating.text
    except:
        rating = ''

    print('Rating:', rating)
    title = title.select_one('a')
    title = title.text
    print('Title:', title)

    if os.path.exists('./images') is False:
        os.mkdir('./images')

    wget.download(thumb, './images/%s.jpg' % code)
    # 큰 이미지
    # wget.download(thumb.split('?')[0], './images/%s.jpg' % code)
    print('#' * 100)
    break
print('Crawling is done!')