import bs4
import csv
import re

file = open('all tickers.html', encoding='utf-8')
text = file.read()
soup = bs4.BeautifulSoup(text, 'html.parser')
ashki = soup.find_all('a', attrs={'class':"apply-common-tooltip tickerNameBox-GrtoTeat tickerName-GrtoTeat"})
supchiki = soup.find_all('sup', attrs={"class":"apply-common-tooltip tickerDescription-GrtoTeat"})
print(ashki)
print(supchiki)

ticker_dict = {}
name_dict = {}

for atag, suptag in zip(ashki, supchiki):
    name = (suptag.text
            .replace(' - обыкн.', '')
            .replace(' ПАО', '')
            .replace('ПАО ', '')
            .replace('(ПАО)', '')
            .replace('ПАО', ''))
    ticker = atag.text
    ticker_dict[ticker] = name
    name_dict[name] = ticker
    print(ticker, name)


def clean_string(s):
    return re.sub(r'"', "'", s).strip()


with open('tickers.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Ticker', 'Name'])
    for ticker, name in ticker_dict.items():
        writer.writerow([clean_string(ticker), clean_string(name)])
