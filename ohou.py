from bs4 import BeautifulSoup
import requests
import json, os, re

class Ohou:
    def __init__(self):
        pass

    def get_detail_html(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        detail = soup.find("div", "production-selling-description__content")
        imgs = detail.find_all("img")

        r_text = "상세페이지\n"
        for img in imgs:
            r_text += f"{img}\n"

        return r_text