import pickle
import csv
import news_parser
import ticker_to_news_list as ttnl
from constants import *
import os
from multiprocessing import Pool


# def get_last_news(news_count: int, print_progress: bool = False):
#     pages_count = news_count // 10
#     if news_count % 10 > 0:
#         pages_count += 1
#     url_maker = ttnl.TickerToNewsList()
#     with open(COMPANY_URLS_CSV, mode='r', newline='', encoding='utf-8') as file:
#         csv_reader = csv.reader(file)
#         header = True
#         for row in csv_reader:
#             if header:
#                 header = False
#                 continue
#             ticker, path = row
#             print(ticker)
#             links_list = url_maker.get_links(ticker, pages_count)
#             with open(f"{RECENT_NEWS_DIRECTORY}/{ticker}.csv", mode='w', newline='', encoding='utf-8') as company_news:
#                 writer = csv.DictWriter(company_news, fieldnames=["Title", "Text", "Time", "Url"])
#                 for i, url in enumerate(links_list[:news_count]):
#                     print(i)
#                     title, time, article_text = news_parser.NewsLoader.scrape_article(url)
#                     row = {"Title": title, "Text": article_text.strip(), "Time": time, "Url": url}
#                     writer.writerow(row)
def get_news_for_ticker(ticker_info):
    try:
        ticker, pages_count = ticker_info
        url_maker = ttnl.TickerToNewsList()
        links_list = url_maker.get_links(ticker, pages_count)

        news_data = []
        for url in links_list:
            title, time, article_text = news_parser.NewsLoader.scrape_article(url)
            news_data.append({"Title": title, "Text": article_text.strip(), "Time": time, "Url": url})

        # Сохраняем новости в файл
        with open(f"{RECENT_NEWS_DIRECTORY}/{ticker}.csv", mode='w', newline='', encoding='utf-8') as company_news:
            writer = csv.DictWriter(company_news, fieldnames=["Title", "Text", "Time", "Url"])
            writer.writeheader()
            writer.writerows(news_data)
    except Exception as ex:
        print("Exception", ex)


def get_last_news(news_count: int, print_progress: bool = False):
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
    with Pool(processes=2) as pool:
        pool.map(get_news_for_ticker, tickers)


if __name__ == '__main__':
    get_last_news(10, True)
