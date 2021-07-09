from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time

import sys
import os

# url 입력
url = input()

# 크롬드라이버 옵션 (headless로 할 수 있게)
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# chromedriver 경로 설정
# pyinstaller에 넣기 위해서 사용함
# if getattr(sys, 'frozen', False):
#     chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
#     driver = webdriver.Chrome(chromedriver_path, options=options)
# else:
#     driver = webdriver.Chrome()

# 크롬 드라이버 경로
chrome_driver_dir = '/Users/jeongjong-yun/Development/chromedriver'
driver = webdriver.Chrome(chrome_driver_dir)

response = requests.get(url)
if response.status_code == 200:
    # webdriver에 url 넣기
    driver.get(url)

    # 이렇게 하면 안되는데 일단 이렇게 함
    time.sleep(5)

    lis = driver.find_element_by_xpath(
        '//*[@id="content"]/div/div[2]/div[1]/ul').find_elements_by_tag_name('li')

    # 썸네일 가져오기
    thumbnailes = []
    for li in lis:
        li.click()

        thumbnailes.append(li.find_element_by_xpath(
            '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/img').get_attribute('data-src'))

    print(thumbnailes)

    # html 소스 받기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # img 받기
    image_containeres = soup.find_all(
        class_='se-image')

    # img태그가 들어있는 div태그에서 img태그 추출하기
    detailes = []
    for container in image_containeres:
        image = container.find('img')
        # image = str(image)

        print(image['data-src'])
        detailes.append(image['data-src'])

    # 드라이버 종료
    driver.quit()

    # txt파일로 저장할 str 변수 선언
    save_txt = ''
    save_txt += '썸네일\n'

    for thumbnail in thumbnailes:
        save_txt += thumbnail + '\n'

    save_txt += '\n상세페이지'

    for detail in detailes:
        save_txt += detail + '\n'

    # 파일 저장
    f = open(url[url.find('products')+9:]+'.txt', 'w')
    f.write(save_txt)
    f.close()

else:
    print('error!')
    print(response.status_code)
