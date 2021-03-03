from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
import datetime as dt


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
        self.first_parsed_pages = []
        self.all = []
        self.options = Options()
        self.options.binary_location = r"C:/Program Files/Mozilla Firefox/firefox.exe"
        self.driver = webdriver.Firefox(
            options=self.options, executable_path='data\drivers\geckodriver-v0.29.0-win64\geckodriver.exe')
        self.today = dt.date.today()
        self.month = {
            'январ': 1,
            'феврал': 2,
            'март': 3,
            'апрел': 4,
            'мая': 5,
            'июн': 6,
            'июл': 7,
            'август': 8,
            'сентябр': 9,
            'октябр': 10,
            'ноябр': 11,
            'декабр': 12
        }

    def run(self):
        for city in self.cities:
            for page in range(1, self.pages + 1):
                while not self.first_parsed_pages:
                    self.__get_pages(city, page)
                for parsed_page in self.first_parsed_pages:
                    self.parsed_pages.append(parsed_page.get_attribute('href'))
                self.__parse_pages()

    def __get_pages(self, city, page):
        self.driver.get('https://www.avito.ru/' + self.__transliteration(
                    city) + self.__transliteration(self.category) + '?p=' + str(page) + '&q=' + self.query)
        try:
            self.first_parsed_pages = self.driver.find_elements_by_xpath("//*[contains(@class, 'link-link-39EVK link-design-default-2sPEv title-root-395AQ iva-item-title-1Rmmj title-list-1IIB_ title-root_maxHeight-3obWc')]")
        except Exception:
            self.first_parsed_pages = self.driver.find_elements_by_xpath("//*[contains(@class, 'link-link-39EVK link-design-default-2sPEv title-root-395AQ iva-item-title-1Rmmj title-listRedesign-3RaU2 title-root_maxHeight-3obWc')]")
    
    def __parse_pages(self):
        for page in self.parsed_pages:
            self.driver.get(page)
            try:
                price = int(self.driver.find_element_by_xpath("//*[contains(@class, 'js-item-price')]").get_attribute('content'))

                date = self.driver.find_element_by_xpath("//*[contains(@class, 'title-info-metadata-item-redesign')]").text
                if 'сегодня' in date:
                    date = self.today
                elif 'вчера' in date:
                    date = self.today - dt.timedelta(days=1)
                elif 'недел' in date:
                    date = self.today - dt.timedelta(weeks=int(date[0]))
                else:
                    for month in self.month:
                        if month in date:
                            m = self.month[month]
                    date = self.today - dt.timedelta(days=int(date.split()[0]), month=m)
                print(date)

                views = self.driver.find_element_by_xpath("//*[contains(@class, 'title-info-metadata-item title-info-metadata-views')]").text
                views = int(views[:views.index('(')])
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
