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
driver.get('https://movie.naver.com/movie/running/current.nhn')

soup = bs(driver.page_source, 'html.parser')
# soup = bs(driver.page_source, 'lxml')
# soup = bs(driver.page_source, 'lxml-xml') # Only XML
# soup = bs(driver.page_source, 'xml') # Only XML
# soup = bs(driver.page_source, 'html5lib')
ul = soup.find('ul', class_='lst_detail_t1')
# li_list = ul.find_all('li')
li_list = ul.findChildren()
for li in li_list:
    detail_link = li.find('a')
    detail_link = 'https://movie.naver.com' + detail_link['href']
    # detail_link = 'https://movie.naver.com' + detail_link.get('href')
    print('Detail Link:', detail_link)

    code = detail_link.split('=')[1]
    print('Code:', code)

    thumb = li.find('img')
    thumb = thumb['src']
    print('Thumbnail url:', thumb)

    title = li.find('dt', class_='tit')
    rating = title.find('span')
    rating = rating.text
    # 없는 경우 예외처리
    # try:
    #     rating = title.select_one('span')
    #     rating = rating.text
    # except:
    #     rating = ''
    print('Rating:', rating)
    title = title.find('a')
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
driver.quit()