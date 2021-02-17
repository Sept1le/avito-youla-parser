from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class Bot:
    def __init__(self):
        self.path = 'D:/'
        self.pages = []
        self.options = Options()
        self.options.binary_location = r"C:/Program Files/Mozilla Firefox/firefox.exe"
        self.driver = webdriver.Firefox(
            options=self.options, executable_path='data\drivers\geckodriver-v0.29.0-win64\geckodriver.exe')
        self.driver.get('http://google.com/')
        self.price = [0, 1000000]
        self.cities = []
        self.category = ''
        self.year = [0, 2021]
        self.ads = [0, 10000000]
        self.goods = [0, 1000000]
        self.views = [0, 1000000000]

    def __transliteration(self, text: str) -> str:
        cyrillic = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        latin = 'a|b|v|g|d|e|e|zh|z|i|i|k|l|m|n|o|p|r|s|t|u|f|kh|tc|ch|sh|shch||y||e|yu|ya'.split(
            '|')
        trantab = {k: v for k, v in zip(cyrillic, latin)}
        newtext = ''
        for ch in text:
            casefunc = str.lower
            newtext += casefunc(trantab.get(ch.lower(), ch))
        newtext = newtext.split()
        if len(newtext) > 2:
            newtext = "-".join(newtext)
        else:
            newtext = "_".join(newtext)
        return newtext
