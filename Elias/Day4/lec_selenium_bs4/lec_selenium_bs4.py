from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bs
import wget
import os
from webdriver_manager.chrome import ChromeDriverManager

chrome_option = webdriver.ChromeOptions()
# chrome_option.add_argument('headless')
chrome_option.add_argument('window-size=1920x1080')
chrome_option.add_argument('disable-gpu')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_option)

# Wait for web-browser loading
driver.implicitly_wait(3)

# 네이버 이동
driver.get('https://movie.naver.com/movie/running/current.naver')

# 해당 페이지를 html파일로 저장
with open('naver.html', 'w', encoding='utf8') as f:
    f.write(driver.page_source)

soup = bs(driver.page_source, 'html.parser')
# soup = bs(driver.page_source, 'lxml') # pip install lxml
# soup = bs(driver.page_source, 'lxml-xml') # Only XML
# soup = bs(driver.page_source, 'xml') # Only XML
# soup = bs(driver.page_source, 'html5lib')
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

    # rating = title.select_one('span')
    # rating = rating.text
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

    # 큰 이미지
    wget.download(thumb, './images/%s.jpg' % code)
    # wget.download(thumb.split('?')[0], './images/%s.jpg' % code)
    print('#' * 100)
    break
print('Crawling is done!')
driver.quit()