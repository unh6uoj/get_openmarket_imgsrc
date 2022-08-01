import os, re

from gui import GUI
from ohou import Ohou
from naver import Naver

stores = ["스마트 스토어", "오늘의 집"]

gui = GUI("HTML 추출", 640, 450)

def store_run(gui):
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
gui.add_comfirm_button(lambda: store_run(gui))
gui.main_loop()