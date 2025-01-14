from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from constants import *


class TickerToNewsURL:
    def __init__(self):
        self.driver = Driver(uc=True)
        self.wait = WebDriverWait(self.driver, 5)

    def get(self, ticker):
        self.driver.get(f"https://ru.investing.com/search?q={ticker}")
        time.sleep(3)

        first_result = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.js-inner-all-results-quote-item.row")))
        first_result.click()
        time.sleep(5)

        url = self.driver.current_url
        return url

    def quit(self):
        self.driver.quit()


if __name__ == '__main__':
    ttnu = TickerToNewsURL()

    done_tickers = set()
    with open(COMPANY_URLS_CSV, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            ticker, url = row
            done_tickers.add(ticker)
    print('done tickers:', done_tickers)

    with open('csv_files/tickers.csv', mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        header = True
        for row in csv_reader:
            if header:
                header = False
                continue
            ticker, _ = row
            if ticker in done_tickers:
                print('skip ticker:', ticker)
                continue

            print('getting url for', ticker, end=' ')
            url = ttnu.get(ticker)
            print(url)

            with open(COMPANY_URLS_CSV, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([ticker, url])
    ttnu.quit()
