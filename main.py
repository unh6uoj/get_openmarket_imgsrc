from bs4 import BeautifulSoup
import requests
import json


def get_thumbnail(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    thumbnails = soup.find(class_="_2Yq5J2HeBn").find_all("img")

    r_text = "썸네일\n"
    try:
        for thumbnail in thumbnails:
            r_text += thumbnail.attrs["src"].replace("f40", "m510") + "\n"
    except:
        pass

    return r_text


def get_detail(url):
    code = url.split("/")[5].split("?")[0]

    r = requests.get(
        f"https://smartstore.naver.com/i/v1/products/{code}/contents/-1/PC"
    )
    soup = BeautifulSoup(str(json.loads(r.text)["renderContent"]), "html.parser")

    r_text = "상세페이지\n"
    try:
        main_contents = soup.find(class_="se-main-container")
        for img in main_contents.find_all("img"):
            if img.attrs["class"][0] == "se-image-resource":
                r_text += f'<img src="{img.attrs["data-src"]}" />' + "\n"
            elif img.attrs["class"][0] == "se-inline-image-resource":
                r_text += f'<img src="{img.attrs["data-src"]}" />' + "\n"
    except:
        pass

    return r_text


if __name__ == "__main__":
    print("썸네일만 가져오려면 1, 상세페이지만 가져오려면 2, 모두 가져오려면 3을 입력 해주세요")
    mode = input()

    print("url을 입력해주세요")
    url = input()
    url = url.split("?")[0]

    r_text = ""
    if mode == "1":
        r_text = get_thumbnail(url)
    elif mode == "2":
        r_text = get_detail(url)
    elif mode == "3":
        r_text = get_thumbnail(url) + "\n" + get_detail(url)

    f = open(url.split("/")[5].split("?")[0] + ".txt", "w")
    f.write(r_text)
    f.close()