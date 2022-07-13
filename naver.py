import json
import requests

from bs4 import BeautifulSoup

class Naver:
    def __init__(self):
        pass

    def get_thumbnail(self, url):
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
        except Exception as e:
            print(e)
        
        return r_text

    def get_detail(self, url):
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

    def get_detail_v2(self, url):
        code = url.split("/")[5].split("?")[0]
        
        try:
            merchant_code, etc_code = self.get_etc_no(url)

            r = requests.get(
                f"https://smartstore.naver.com/i/v1/products/{code}/contents/{merchant_code}/PC"
            )
        except:
            return "상품 데이터 수집 중 오류 발생"

        soup = BeautifulSoup(str(r.json()["renderContent"]), "html.parser")

        r_text = "상세페이지\n"
        try:
            for img in soup.find_all("img"):
                r_text += f'<img src="{img.attrs["data-src"]}" />' + "\n"
        except Exception as e:
            print(e)

        return r_text

    # 기타 상품번호 추출
    def get_etc_no(self, url):
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
        results = []
        
        page = 1
        while True:
            response = requests.get(
                all_product_url.split("?")[0],
                params={
                    "st": "POPULAR",
                    "free": "false",
                    "dt": "IMAGE",
                    "page": page,
                    "size": 80
                }
            )
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            products = soup.find_all(class_='-qHwcFXhj0')

            for product in products:
                print(product)
                results.append({
                    "title": product.find('strong').text,
                    "url": f"https://smartstore.naver.com{product.find('a').attrs['href']}"
                })

            page += 1
            
            if len(products) != 80:
                break

        print(f"총 {len(results)}개의 상품")

        return results