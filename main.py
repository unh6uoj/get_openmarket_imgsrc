from bs4 import BeautifulSoup
import requests
import json


def get_thumbnail(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    try:
        thumbnails = soup.find(class_="_2Yq5J2HeBn").find_all("img")
    except:
        thumbnails = soup.find(class_="_23RpOU6xpc").find_all("img")

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

    try:
        soup = BeautifulSoup(str(json.loads(r.text)["renderContent"]), "html.parser")
        r_text = "상세페이지\n"
        main_contents = soup.find(class_="se-main-container")
        for img in main_contents.find_all("img"):
            if img.attrs["class"][0] == "se-image-resource":
                r_text += f'<img src="{img.attrs["data-src"]}" />' + "\n"
            elif img.attrs["class"][0] == "se-inline-image-resource":
                r_text += f'<img src="{img.attrs["data-src"]}" />' + "\n"
    except:
        return False

    return r_text

def get_detail_v2(url):
    code = url.split("/")[5].split("?")[0]
    merchant_code, etc_code = get_etc_no(url)

    r = requests.get(
        f"https://smartstore.naver.com/i/v1/products/{code}/contents/{merchant_code}/PC"
    )

    soup = BeautifulSoup(str(r.json()["renderContent"]), "html.parser")

    r_text = "상세페이지\n"
    try:
        for img in soup.find_all("img"):
            r_text += f'<img src="{img.attrs["data-src"]}" />' + "\n"
    except Exception as e:
        print(e)

    return r_text

# 기타 상품번호 추출
def get_etc_no(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        # 받은 url에서 json추출
        # salecount는 두 번째 script태그 안에 있다
        script = soup.find_all('script')[1]
        # 가져온 script를 str형으로 변환
        script = str(script)
        # str데이터 스플릿 (json형태로 변환)
        script_json = script[script.find(
            '__=')+3: script.find('</script>')]
        # str을 dictionary로 변환
        script_json = json.loads(script_json)
    except:
        return False

    # JSON에서 데이터 가져오기
    return script_json['product']['A']['channel']['naverPaySellerNo'], script_json['product']['A']['productNo']

def get_products_by_all_product_url(all_product_url):   # 스마트 스토어 전체상품 url 입력 시 전체 상품 가져옴
    # all_product_url = all_product_url.replace("size=40", "size=80")
    all_product_url += "&size=80"
    response = requests.get(all_product_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    products = soup.find_all(class_='-qHwcFXhj0')

    results = []
    for product in products:
        results.append({
            "title": product.find('strong').text,
            "url": f"https://smartstore.naver.com{product.find('a').attrs['href']}"
        })

    return results

if __name__ == "__main__":
    print("썸네일만 가져오려면 1, 상세페이지만 가져오려면 2, 모두 가져오려면 3을 입력 해주세요")
    mode = input()

    

    print("단일 상품을 가져오시려면 1번, 전체 상품 목록에서 가져오시려면 2번을 눌러주세요")
    is_all = input()

    print("url을 입력해주세요")
    if is_all == "1":
        url = input()
        url = url.split("?")[0]

        r_text = ""
        if mode == "1":
            r_text = get_thumbnail(url)
        elif mode == "2":
            if get_detail(url):
                r_text = get_detail(url)
            else:
                r_text = get_detail_v2(url)
        elif mode == "3":
            if get_detail(url):
                r_text = get_thumbnail(url) + "\n" + get_detail(url)
            else:
                r_text = get_thumbnail(url) + "\n" + get_detail_v2(url)

        f = open(url.split("/")[5].split("?")[0] + ".txt", "w")
        f.write(r_text)
        f.close()

    elif is_all == "2":
        url = input()

        products = get_products_by_all_product_url(url)
        
        for product in products:
            f = open(f"{product['title']}.txt", 'w')
            r_text = ""
            if get_detail(url):
                r_text = get_thumbnail(product["url"]) + "\n" + get_detail(product["url"])
            else:
                r_text = get_thumbnail(product["url"]) + "\n" + get_detail_v2(product["url"])
            
            f.write(r_text)
            f.close()