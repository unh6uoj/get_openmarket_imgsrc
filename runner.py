import os, re

from gui import GUI
from ohou import Ohou
from naver import Naver

stores = ["스마트 스토어", "오늘의 집"]

gui = GUI("HTML 추출", 640, 450)

def store_run():
    gui_info = gui.get_selected_info()
    store = gui_info.get("store")
    mode = gui_info.get("mode")

    urls = [url for url in gui_info.get("url").split("\n") if url != ""]
    
    if store == "스마트 스토어":
        crawler = Naver(mode)
    elif store == "오늘의 집":
        crawler = Ohou(mode)

    for url in urls:
        crawler.set_url(url)
        product_code, result = crawler.run()

        f = open(f"{product_code}.txt", 'w')
        f.write(result)
        f.close()

gui.add_store_combobox(stores)
gui.add_url_text()
gui.add_mode_radio()
gui.add_is_img_radio()
gui.add_comfirm_button(store_run)

gui.main_loop()

# if __name__ == "__main__":
#         if is_all == "1":
#             url = url.split("?")[0]

#             r_text = ""
#             if mode == "1":
#                 r_text = get_thumbnail(url)
#             elif mode == "2":
#                 if get_detail(url):
#                     r_text = get_detail(url)
#                 else:
#                     r_text = get_detail_v2(url)
#             elif mode == "3":
#                 if get_detail(url):
#                     r_text = get_thumbnail(url) + "\n" + get_detail(url)
#                 else:
#                     r_text = get_thumbnail(url) + "\n" + get_detail_v2(url)

#             f = open(url.split("/")[5].split("?")[0] + ".txt", "w")
#             f.write(r_text)
#             f.close()

#         elif is_all == "2":
#             products = get_products_by_all_product_url(url)
#             brand = re.sub("[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\"…》\”\“\’·]", "", url.split("/")[3])

#             # 디렉토리 유무 체크 후 없으면 생성
#             if os.path.isdir(brand):
#                 pass
#             else:
#                 os.makedirs(brand)
            
#             for product in products:
#                 title = re.sub("[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\"…》\”\“\’·]", "",  product["title"])

#                 f = open(f"{brand}/{title}.txt", 'w')

#                 r_text = ""
#                 if get_detail(url):
#                     r_text = get_thumbnail(product["url"]) + "\n" + get_detail(product["url"])
#                 else:
#                     r_text = get_thumbnail(product["url"]) + "\n" + get_detail_v2(product["url"])
                
#                 f.write(r_text)
#                 f.close()