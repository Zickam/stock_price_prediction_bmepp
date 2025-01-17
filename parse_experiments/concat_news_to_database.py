import datetime
import random
import csv
import time

from constants import *
import os
import asyncio
import datetime
import threading

from tinkoff.invest.utils import now
from tinkoff.invest.utils import CandleInterval

from analysis.functions_sync import getTanHNormalizedPriceChangeByTicker

PRINT_PROGRESS = True
DATABASE_NAME = 'database.csv'
FIELDNAMES = ['Title', 'Text', 'Time', 'Url', 'Value']

def value_from_stock_market(ticker: str, datetime_str: str):
    """datetime looks like: "21.10.2024, 12:31"""

    _datetime = datetime.datetime.strptime(datetime_str, "%d.%m.%Y, %H:%M")
    _datetime = _datetime.replace(tzinfo=datetime.timezone.utc)

    needed_datetime = _datetime + datetime.timedelta(days=30)

    return getTanHNormalizedPriceChangeByTicker(ticker, _datetime, needed_datetime)

def __concat(row, ticker, writer):
    title = row['Title']
    text = row['Text']
    _time = row['Time']
    url = row['Url']
    value = value_from_stock_market(ticker, _time)
    if value is None:
        print(f"None cost found for {ticker}, skipping...")
        return

    writer.writerow({"Title": title, "Text": text, "Time": _time, "Url": url, "Value": value})

def _concat(csv_path: str):
    rows = []
    file1 = open(DATABASE_NAME, mode='a', newline='', encoding='utf-8')
    writer = csv.DictWriter(file1, fieldnames=FIELDNAMES)
    with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
        lines_amount = len(file.readlines())
        file.seek(0)
        reader = csv.DictReader(file)
        ticker = csv_path.split('/')[-1].split('.')[0]

        for i, row in enumerate(reader):
            ok = False
            for j in range(1, 4):
                try:
                    __concat(row, ticker, writer)
                    ok = True

                except Exception as ex:
                    print(ex)
                    time.sleep(60 * j)

                if ok:
                    break

            if PRINT_PROGRESS:
                print(f"{ticker} is handled for {round(i / lines_amount * 100, 2)}%")
                # print('working with ticker', ticker, 'url:', url)



    print(ticker, "has finished processing")

def concat():

    with open(DATABASE_NAME, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()

    csv_list = [NEWS_CSV_DIRECTORY + '/' + filename for filename in os.listdir(NEWS_CSV_DIRECTORY)]

    threads = []
    for csv_path in csv_list:
        thread = threading.Thread(target=_concat, args=(csv_path, ))
        threads.append(thread)
        # thread.start()
        # thread.join()

    for thread in threads:
        thread.start()
        time.sleep(1)

    for thread in threads:
        thread.join()


if __name__ == '__main__':

    try:
        os.system("rm -r ../analysis/instruments")
        os.mkdir("../analysis/instruments")
    except Exception as ex:
        ...
    concat()
    # print(value_from_stock_market("VKCO", "21.10.2024, 12:31"))