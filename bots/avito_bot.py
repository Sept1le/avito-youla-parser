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
        self.parsed_pages = []
        self.all = []

    def run(self):
        for city in self.cities:
            for page in range(1, self.pages + 1):
                self.driver.get('https://www.avito.ru/' + self.__transliteration(
                    city) + self.__transliteration(self.category) + '?p=' + str(page) + '&q=' + self.query)
                parsed_pages = self.driver.find_elements_by_xpath(
                    "//*[contains(@class, 'link-link-39EVK link-design-default-2sPEv title-root-395AQ iva-item-title-1Rmmj title-list-1IIB_ title-root_maxHeight-3obWc')]")
                for parsed_page in parsed_pages:
                    self.parsed_pages.append(parsed_page.get_attribute('href'))
                self.__parse_pages()
    
    def __parse_pages(self):
        for page in self.parsed_pages:
            self.driver.get(page)
            btn = self.driver.find_element_by_xpath("//*[contains(@class, 'button item-phone-button js-item-phone-button button-origin contactBar_greenColor button-origin_full-width button-origin_large-extra item-phone-button_hide-phone item-phone-button_card js-item-phone-button_card contactBar_height')]")
            btn.click()

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
        newtext = "_".join(newtext)
        return newtext
