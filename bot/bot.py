from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class Bot:
    def __init__(self):
        self.path = 'D:/'
        self.query = 'автомобиль'
        self.pages = 1
        self.options = Options()
        self.options.binary_location = r"C:/Program Files/Mozilla Firefox/firefox.exe"
        self.driver = webdriver.Firefox(
            options=self.options, executable_path='data\drivers\geckodriver-v0.29.0-win64\geckodriver.exe')
        self.price = [0, 1000000]
        self.cities = ['москва']
        self.category = ''
        self.year = [0, 2021]
        self.ads = [0, 10000000]
        self.goods = [0, 1000000]
        self.views = [0, 1000000000]

    def run(self):
        for city in self.cities:
            for page in range(1, self.pages + 1):
                self.driver.get('https://www.avito.ru/' + self.__transliteration(city) + '?p=' + str(page) + '&q=' + self.query)
                a = self.driver.find_elements_by_xpath("//*[contains(@class, 'link-link-39EVK link-design-default-2sPEv title-root-395AQ iva-item-title-1Rmmj title-list-1IIB_ title-root_maxHeight-3obWc')]")

    def __transliteration(self, text: str) -> str:
        cyrillic = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        latin = 'a|b|v|g|d|e|e|zh|z|i|y|k|l|m|n|o|p|r|s|t|u|f|kh|tc|ch|sh|shch||y||e|yu|ya'.split(
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
