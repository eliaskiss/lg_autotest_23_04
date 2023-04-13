from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import wget
import os
from webdriver_manager.chrome import ChromeDriverManager

chrome_option = webdriver.ChromeOptions()

# chrome_option.add_argument('headless') # 웹브라우저를 Hidden
chrome_option.add_argument('window-size=1920x1080')
chrome_option.add_argument('disable-gpu')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_option)

time.sleep(1)
# 네이버로 이동
driver.get('https://www.naver.com')

# 검색입력창 찾기
input_search = driver.find_element(By.ID, 'query')
# input_search = driver.find_element_by_name('query')
# input_search = driver.find_element(By.NAME, 'query')
# input_search = driver.find_element(By.CLASS_NAME, 'input_text')
# input_search = driver.find_element(By.CSS_SELECTOR, '#query')       # '#': Element ID
# input_search = driver.find_element(By.CSS_SELECTOR, '.input_text')  # '.': Element Class Name, '': Tag Name
time.sleep(1)

# 검색어 입력
input_search.send_keys('네이버 영화')
time.sleep(1)

# 엔터키 입력
input_search.send_keys(Keys.ENTER)
time.sleep(1)

# 네이버 영화링크
link = driver.find_element(By.CSS_SELECTOR, '.link_name')
print('Link Address:', link.get_attribute('href'))
link.click()
time.sleep(1)

# 상영장/예정작 클릭
driver.switch_to.window(driver.window_handles[-1])
# running_film = driver.find_element(By.CLASS_NAME, 'menu02')
running_film = driver.find_element(By.XPATH, '//*[@id="scrollbar"]/div[1]/div/div/ul/li[2]/a')
running_film.click()
time.sleep(1)

# 영화목록 리스트 상단 엘리먼트
ul = driver.find_element(By.CLASS_NAME, 'lst_detail_t1')
# li_list = driver.find_elements(By.TAG_NAME, 'li') # HTML 페이지에 있는 모든 li 엘리먼트를 다 가져옴
li_list = ul.find_elements(By.TAG_NAME, 'li') # lst_detail_t1 하위에 있는 모든 li 엘리먼트를 가져옴

for li in li_list:
    # 상세페이지 링크
    detail_link = li.find_element(By.TAG_NAME, 'a')
    detail_link = detail_link.get_attribute('href')
    print(f'Detail Link: {detail_link}')

    # 영화코드
    code = detail_link.split('=')[1]
    print(f'Code: {code}')

    # 썸네일 이미지링크
    thumb = li.find_element(By.TAG_NAME, 'img')
    thumb = thumb.get_attribute('src')
    print(f'Thumbnail URL: {thumb}')

    # Title Element
    title = li.find_element(By.CLASS_NAME, 'tit')

    # 관람연령
    try:
        rating = title.find_element(By.TAG_NAME, 'span')
        rating = rating.text
    except:
        rating = ''
    print(f'Rating: {rating}')

    # 영화제목
    title = title.find_element(By.TAG_NAME, 'a')
    title = title.text
    print(f'Title: {title}')

    # Image 폴더존재여부 확인
    if os.path.exists('./images') is False:
        os.mkdir('images')

    # 썸네일 이미지 다운로드
    # wget.download(thumb, f'./images/{code}.jpg')
    wget.download(thumb.split('?')[0], f'./images/{code}_origin.jpg')
    print('#' * 100)

print('Crawling is done!!!')
driver.close()

