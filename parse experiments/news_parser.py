from constants import PICKLE_LINKS_DIRECTORY, NEWS_CSV_DIRECTORY
import pickle
import os
import csv
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time as time_lib


class NewsLoader:
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
        self.driver = Driver(uc=True, headless=True)
        self.wait = WebDriverWait(self.driver, 5)
        with open(f'{PICKLE_LINKS_DIRECTORY}/{self.ticker}.pickle', 'rb') as file:
            self.urls_list = pickle.load(file)

        self.csv_file_path = f'{NEWS_CSV_DIRECTORY}/{self.ticker}.csv'
        if not os.path.isfile(self.csv_file_path):
            with open(self.csv_file_path, mode='w', newline='', encoding='utf-8') as file:
                fieldnames = ["Title", "Text", "Time", "Url"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

    def load(self, print_progress: bool = False):
        start = time_lib.time()
        with open(self.csv_file_path, mode='r+', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            existing_urls = {row["Url"] for row in reader}
            not_existing_urls = [url for url in self.urls_list if url not in existing_urls]

            file.seek(0, 2)
            writer = csv.DictWriter(file, fieldnames=["Title", "Text", "Time", "Url"])

            for i, url in enumerate(not_existing_urls):
                title, time, article_text = self.scrape_article(url)

                if print_progress:
                    time_passed = time_lib.time() - start
                    print(self.ticker,
                          f'| Progress: {i+1} of {len(not_existing_urls)}',
                          f'| Passed time: {round(time_passed)}s',
                          '|', url)

                row = {"Title": title, "Text": article_text, "Time": time, "Url": url}
                writer.writerow(row)
                file.flush()

    def scrape_article(self, url):
        self.driver.get(url)
        title = self.wait.until(EC.presence_of_element_located((By.ID, 'articleTitle'))).text
        time = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div .mt-2.flex.flex-col.gap-2.text-xs.md\\:mt-2\\.5.md\\:gap-2\\.5')
        ))
        time = time.find_element(By.CSS_SELECTOR, 'span').text
        time = time.replace('Опубликовано ', '')
        separator_div = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.-mb-2.mt-12.h-0\\.5.w-\\[250px\\].bg-gradient-pro-separator")
        ))

        article_text = ""
        elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//p | //blockquote")))

        for element in elements:
            if element.location['y'] >= separator_div.location['y']:
                break
            article_text += element.text

            spans = element.find_elements(By.TAG_NAME, "span")
            for span in spans:
                article_text += span.text + " "
            article_text += '\n'

        return title, time, article_text.strip()


def load_news_from_all_pickle_urls():
    tickers_with_pickle = [filename.split('.')[0] for filename in os.listdir(PICKLE_LINKS_DIRECTORY)]
    for ticker in tickers_with_pickle:
        print('INIT NewsLoader for', ticker)
        news_loader = NewsLoader(ticker)
        news_loader.load(True)


if __name__ == '__main__':
    load_news_from_all_pickle_urls()
