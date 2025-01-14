import csv
import news_parser
import ticker_to_news_list as ttnl
from constants import *
import os
from multiprocessing import Pool

USELESS_TICKERS = ['DIOD', 'NFAZ', 'INGR', 'KMEZ', 'LPSB', 'MRSB', 'NFAZ', 'PMSB', 'APRI', 'CHGZ','ZILL', 'GECO', 'YKEN', 'TUZA',
                   'VGSB', 'STSB', 'ARSA', 'RUSI', 'RDRB', 'CHKZ', 'DVEC', 'GEMA', 'PRFN', 'RDRB', 'RUSI', 'YRSB', 'ASSB', 'DZRD',
                   'IVAT', 'KRSB', 'EELT', 'VLHZ', 'SVET', 'VRSB', 'KAZT', 'KUZB','MAGE', 'NKSH', 'PRMB', 'RGSS', 'RZSB', 'ZVEZ',
                   'KBSB', 'KZOS', 'PRMD', 'KCHE', 'NNSB', 'SAGO', 'TASB', 'MGTS', 'VSEH', 'KGKC', 'MISB', 'NSVZ', 'SARE', 'TCSG',
                   'KLSB', 'VSYD', 'RTGZ', 'KLVZ', 'TGKB', 'RTSB', 'WTCM', 'TGKN', 'TORS', 'SLEN', 'VEON-RX']

def get_news_for_ticker(ticker_info, need_to_replace):
    ticker, pages_count = ticker_info
    file_path = f"{RECENT_NEWS_DIRECTORY}/{ticker}.csv"
    if (os.path.exists(file_path) or ticker in USELESS_TICKERS) and not need_to_replace:
        print(f"Новости для компании {ticker} уже загружены. Пропускаем.")
        return
    url_maker = ttnl.TickerToNewsList()
    links_list = url_maker.get_links(ticker, pages_count, print_progress=True)

    news_data = []
    for url in links_list:
        title, time, article_text = news_parser.NewsLoader.scrape_article(url)
        news_data.append({"Title": title, "Text": article_text.strip(), "Time": time, "Url": url})

    # Сохраняем новости в файл
    with open(file_path, mode='w', newline='', encoding='utf-8') as company_news:
        writer = csv.DictWriter(company_news, fieldnames=["Title", "Text", "Time", "Url"])
        writer.writeheader()
        writer.writerows(news_data)


def get_last_news(news_count: int, need_to_replace: bool = False):
    pages_count = news_count // 10 + (news_count % 10 > 0)

    tickers = []
    with open(COMPANY_URLS_CSV, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        header = True
        for row in csv_reader:
            if header:
                header = False
                continue
            ticker, path = row
            tickers.append((ticker, pages_count))

    # Используем multiprocessing для параллельной обработки тикеров
    with Pool(processes=4) as pool:
        pool.map(get_news_for_ticker, tickers, need_to_replace)


if __name__ == '__main__':
    get_last_news(10)
