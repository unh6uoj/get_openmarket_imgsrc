import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

import sys
import os


class Image():
    def __init__(self):
        pass

    def start(self, url):
        if url.find('11st.co.kr') != -1:
            self.eleven(url)
        elif url.find('gmarket.co.kr') != -1:
            self.gmarket(url)
        else:
            self.naver(url)

    def get_driver(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('disable-gpu')

        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # if getattr(sys, 'frozen', False):
        #     chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
        #     driver = webdriver.Chrome(chromedriver_path, options=options)
        # else:
        #     driver = webdriver.Chrome()

        chrome_driver_dir = '/Users/jeongjong-yun/Development/chromedriver'
        driver = webdriver.Chrome(chrome_driver_dir, options=options)

        driver.implicitly_wait(10)

        driver.get(url)

        return driver

    def save(self, market_name, thumbnails, details):
        # txt파일로 저장할 str 변수 선언
        save_txt = ''
        save_txt += '썸네일\n'

        for thumbnail in thumbnails:
            save_txt += thumbnail + '\n'

        save_txt += '\n상세페이지\n'

        for detail in details:
            save_txt += detail + '\n'

        # 파일 저장
        f = open(market_name + url[url.find('products')+9:url.find('?')
                 if url.find('?') != -1 else None]+'.txt', 'w')
        f.write(save_txt)
        f.close()

    def eleven(self, url):

        driver = self.get_driver(url)

        # 썸네일
        thumb_list = []
        thumb_boxes = driver.find_element_by_xpath(
            '//*[@id="smallImg"]').find_elements_by_tag_name('a')

        for thumb in thumb_boxes:
            thumb_resize = thumb.get_attribute(
                'innerHTML').replace('64x64', '600x600').strip()

            print(thumb_resize)
            thumb_list.append(thumb_resize)

        # 상세페이지
        detail_list = []
        driver.switch_to.frame('prdDescIfrm')
        img_boxes = driver.find_elements_by_class_name('img-box')
        if len(img_boxes) != 0:
            for box in img_boxes:
                img = box.find_element_by_tag_name(
                    'img').get_attribute('outerHTML')

                if img.find('"text-align: center;"') != -1:
                    img = img.replace(
                        '"text-align: center;', '"text-align: center; width: 100%;"')
                else:
                    img = img.replace(
                        '">', '" "width: 100%;">')

                print(img)
                detail_list.append(img)
        else:
            imges = driver.find_element_by_class_name(
                'ifrm_prdc_detail').find_elements_by_tag_name('img')

            for img in imges:
                result = img.get_attribute('outerHTML')
                if result.find('style="') != -1:
                    result = result.replace(
                        'style="text-align: center;', 'style="text-align: center; width: 100%;"')
                else:
                    result = result.replace(
                        '">', '" style="width: 100%;">')

                print(result)
                detail_list.append(result)

        self.save('11번가: ', thumb_list, detail_list)

    def gmarket(self, url):
        pass

    def naver(self, url):

        driver = self.get_driver(url)

        # 썸네일 가져오기
        thumb_list = []
        try:
            lis = driver.find_element_by_xpath(
                '//*[@id="content"]/div/div[2]/div[1]/ul').find_elements_by_tag_name('li')

            for li in lis:
                li.click()

                thumbnail = driver.find_element_by_xpath(
                    '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/img').get_attribute('data-src')
                try:
                    thumb_list.append(thumbnail[:thumbnail.find('?')])
                except:
                    pass
        except:
            thumbnail = driver.find_element_by_xpath(
                '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/img').get_attribute('data-src')
            try:
                thumb_list.append(thumbnail[:thumbnail.find('?')])
            except:
                pass

        print(thumb_list)

        # html 소스 받기
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # img 받기
        image_containeres = soup.find_all(
            class_='se-image')

        # img태그가 들어있는 div태그에서 img태그 추출하기
        detail_list = []
        for container in image_containeres:
            image = container.find('img')
            image_src = image['data-src']
            detail_list.append(image_src[:image_src.find('?')])
        print(detail_list)

        self.save('네이버: ', thumb_list, detail_list)


if __name__ == '__main__':
    image = Image()
    url = input()
    image.start(url)
