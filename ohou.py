import requests
from bs4 import BeautifulSoup

from crawler import Crawler

class Ohou(Crawler):
    def __init__(self, mode):
        super().__init__(mode)

    def run(self):
        if super().get_mode() == 0: # 썸네일
            return self.get_product_code(), self.get_thumbnail_html()
        elif super().get_mode() == 1: # 상세페이지
            return self.get_product_code(), self.get_detail_html()
        elif super().get_mode() == 2: # 모두
            return self.get_product_code(), self.get_thumbnail_html() + self.get_detail_html()

    def get_product_code(self):
        product_code = self.url.split("/")[4]

        return product_code

    def get_detail_html(self):
        r = requests.get(super().get_url())
        soup = BeautifulSoup(r.text, "html.parser")

        detail = soup.find("div", "production-selling-description__content")
        imgs = detail.find_all("img")

        r_text = "상세페이지\n"
        for img in imgs:
            r_text += f"{img}\n"

        return r_text

    def get_thumbnail_html(self):
        r = requests.get(super().get_url())
        soup = BeautifulSoup(r.text, "html.parser")

        thumbnails = soup.find_all("img", "production-selling-cover-image__entry__image")

        r_text = "썸네일\n"
        for thumbnail in thumbnails:
            # 필요 없는 속성 제거
            del thumbnail["srcset"]
            del thumbnail["tabindex"]
            
            r_text += f"{thumbnail}\n"
        
        return r_text