from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep


class Bot:
    def __init__(self, query: str, pages: int, price: list, cities: list, category: str, date: list, views: list):
        self.path = 'D:/'
        self.query = query
        self.pages = pages
        self.price = price
        self.cities = cities
        self.category = category
        self.date = date
        self.views = views
        self.parsed_pages = []
        self.all = []
        self.options = Options()
        self.options.binary_location = r"C:/Program Files/Mozilla Firefox/firefox.exe"
        self.driver = webdriver.Firefox(
            options=self.options, executable_path='data\drivers\geckodriver-v0.29.0-win64\geckodriver.exe')

    def run(self):
        for city in self.cities:
            for page in range(1, self.pages + 1):
                self.driver.get('https://www.avito.ru/' + self.__transliteration(
                    city) + self.__transliteration(self.category) + '?p=' + str(page) + '&q=' + self.query)
                try:
                    parsed_pages = self.driver.find_elements_by_xpath(
                        "//*[contains(@class, 'link-link-39EVK link-design-default-2sPEv title-root-395AQ iva-item-title-1Rmmj title-list-1IIB_ title-root_maxHeight-3obWc')]")
                except Exception:
                    parsed_pages = self.driver.find_elements_by_xpath(
                        "//*[contains(@class, 'link-link-39EVK link-design-default-2sPEv title-root-395AQ iva-item-title-1Rmmj title-listRedesign-3RaU2 title-root_maxHeight-3obWc')]")
                for parsed_page in parsed_pages:
                    self.parsed_pages.append(parsed_page.get_attribute('href'))
                self.__parse_pages()

    def __parse_pages(self):
        for page in self.parsed_pages:
            self.driver.get(page)
            try:
                btn = self.driver.find_element_by_xpath(
                    "//*[contains(@class, 'button item-phone-button js-item-phone-button button-origin contactBar_greenColor button-origin_full-width button-origin_large-extra item-phone-button_hide-phone item-phone-button_card js-item-phone-button_card contactBar_height')]")
                btn.click()
                sleep(3)
                self.driver.get(self.driver.find_element_by_xpath('/html/body/div[12]/div/div/div/div/div[1]/img').get_attribute('src'))
                self.driver.save_screenshot('data/img/avito.png')
            except Exception:
                pass
        
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
