from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
from constants import *


class TickerToNewsList:
    def __init__(self):
        self.driver = Driver(uc=True, headless=True)
        self.wait = WebDriverWait(self.driver, 5)
        self.ticker_dct = {}
        with open(COMPANY_URLS_CSV, 'r', newline='', encoding='utf-8') as csv_reader:
            header = True
            for row in csv_reader:
                if header:
                    header = False
                    continue

                ticker, url = row.strip().split(',')
                url = url + '-news'
                self.ticker_dct[ticker] = url

    def get_links(self, ticker: str,
                  pages_count: int = -1,
                  print_progress: bool = False,
                  start: int = 0):
        """
        :param pages_count: how many pages with news list would be checked. -1 = All"""
        print(ticker, self.ticker_dct.keys())
        assert ticker in self.ticker_dct

        url = self.ticker_dct[ticker]
        links = []
        if pages_count > 0:
            for i in range(start, pages_count):
                if print_progress:
                    print(f'parsing news lists for {ticker}: {i+1} of {pages_count}')
                current_page_url = url + '/' + str(i+1)
                self.driver.get(current_page_url)

                lis = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.border-\\[\\#E6E9EB\\]")))

                for li in lis:
                    link = li.find_element(By.TAG_NAME, "a")
                    href = link.get_attribute("href")
                    links.append(href)

                self.driver.close()
        else:
            i = start
            while True:
                if print_progress:
                    print(f'parsing news lists for {ticker}: {i+1} of {pages_count}')
                current_page_url = url + '/' + str(i+1)
                self.driver.get(current_page_url)
                try:
                    lis = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.border-\\[\\#E6E9EB\\]")))
                except Exception as error:
                    print(error)
                    break
                for li in lis:
                    link = li.find_element(By.TAG_NAME, "a")
                    href = link.get_attribute("href")
                    links.append(href)
                i += 1
            self.driver.close()

        return links

    def get_to_pickle(self, ticker: str,
                  pages_count: int = -1,
                  print_progress: bool = False,
                  start: int = 0,
                  path_folder: str = PICKLE_LINKS_DIRECTORY):
        links = self.get_links(ticker, pages_count, print_progress, start, path_folder)
        with open(path_folder + f'/{ticker}.pickle', 'wb') as file:
            pickle.dump(links, file)

if __name__ == '__main__':
    ttnl = TickerToNewsList()
    ttnl.get_to_pickle('BELU', print_progress=True)
