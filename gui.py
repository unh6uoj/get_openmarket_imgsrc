import tkinter
from tkinter import ttk

class GUI:
    def __init__(self, title, width, height, resizable=False):
        self.root = tkinter.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(resizable, resizable)

    def add_store_combobox(self, stores):
        store_label = tkinter.Label(self.root, text="스토어를 선택 해주세요", width=30, height=2)
        store_label.pack()

        self.store_combobox = ttk.Combobox(self.root, height=15, values=stores, state="readonly")
        self.store_combobox.set(stores[0])
        self.store_combobox.pack()

    def add_url_text(self):
        url_label = tkinter.Label(self.root, text="URL을 입력해주세요\n여러 줄을 넣으시면 함께 가져옵니다.", width=30, height=2)
        url_label.pack()

        self.url_text = tkinter.Text(self.root, height=10)
        self.url_text.pack()

    def add_mode_radio(self):
        mode_label = tkinter.Label(self.root, text="썸네일, 상세페이지를 선택 해주세요", width=30, height=2)
        mode_label.pack()

        mode_container = tkinter.Label(self.root)
        mode_container.pack()

        self.mode_var = tkinter.IntVar()

        thumbnail_radio = tkinter.Radiobutton(mode_container, text="썸네일", value=0, variable=self.mode_var)
        thumbnail_radio.select()
        thumbnail_radio.pack(side="left")
        detail_radio = tkinter.Radiobutton(mode_container, text="상세페이지", value=1, variable=self.mode_var)
        detail_radio.pack(side="left")
        all_radio = tkinter.Radiobutton(mode_container, text="모두", value=2, variable=self.mode_var)
        all_radio.pack(side="left")
    
    def add_is_img_radio(self):
        is_img_label = tkinter.Label(self.root, text="이미지 파일로 가져올까요?", width=30, height=2)
        is_img_label.pack()

        is_img_container = tkinter.Label(self.root)
        is_img_container.pack()

        self.is_img_var = tkinter.IntVar()

        thumbnail_radio = tkinter.Radiobutton(is_img_container, text="HTML", value=0, variable=self.is_img_var)
        thumbnail_radio.select()
        thumbnail_radio.pack(side="left")
        detail_radio = tkinter.Radiobutton(is_img_container, text="이미지", value=1, variable=self.is_img_var)
        detail_radio.pack(side="left")

    def add_comfirm_button(self, store_run):
        self.confirm_button = ttk.Button(self.root, text="확인", command=store_run)
        self.confirm_button.pack()

    def get_selected_info(self):
        return {
            "store": self.store_combobox.get(),
            "mode": self.mode_var.get(),
            "is_img": self.is_img_var.get(),
            "url": self.url_text.get(1.0, 10.100)
        }

    def main_loop(self):
        self.root.mainloop()