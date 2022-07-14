class Crawler:
    def __init__(self, mode):
        self.mode = mode
        self.url = ""

    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url

    def get_mode(self):
        return self.mode