import bs4
import csv
import re

class TickerDataExtractor:
    def __init__(self, html_file):
        self.html_file = html_file
        self.ticker_dict = {}
        self.name_dict = {}

    def load_html(self):
        with open(self.html_file, encoding='utf-8') as file:
            text = file.read()
        return bs4.BeautifulSoup(text, 'html.parser')

    def extract_tickers(self, soup):
        tickers = soup.find_all('a', attrs={'class': "apply-common-tooltip tickerNameBox-GrtoTeat tickerName-GrtoTeat"})
        descriptions = soup.find_all('sup', attrs={"class": "apply-common-tooltip tickerDescription-GrtoTeat"})

        for ticker_tag, description_tag in zip(tickers, descriptions):
            name = self.clean_name(description_tag.text)
            ticker = ticker_tag.text.strip()
            self.ticker_dict[ticker] = name
            self.name_dict[name] = ticker

    def clean_name(self, name):
        return (name.replace(' - обыкн.', '')
                    .replace(' ПАО', '')
                    .replace('ПАО ', '')
                    .replace('(ПАО)', '')
                    .replace('ПАО', '')
                    .strip())

    def clean_string(self, string):
        return re.sub(r'"', "'", string).strip()

    def save_to_csv(self, csv_file):
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Ticker', 'Name'])
            for ticker, name in self.ticker_dict.items():
                writer.writerow([self.clean_string(ticker), self.clean_string(name)])

    def process(self, csv_file):
        soup = self.load_html()
        self.extract_tickers(soup)
        self.save_to_csv(csv_file)

# Применение класса
if __name__ == "__main__":
    extractor = TickerDataExtractor('all tickers.html')
    extractor.process('csv_files/tickers1.csv')
