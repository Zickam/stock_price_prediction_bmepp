import datetime
import random
import csv
from constants import *
import os
import asyncio
import datetime

from tinkoff.invest.utils import now
from tinkoff.invest.utils import CandleInterval

from analysis.functions import getTanHNormalizedPriceChangeByTicker


def value_from_stock_market(ticker: str, datetime_str: str):
    """datetime looks like: "21.10.2024, 12:31"""
    # return 1

    _datetime = datetime.datetime.strptime(datetime_str, "%d.%m.%Y, %H:%M")
    _datetime = _datetime.replace(tzinfo=datetime.timezone.utc)

    return asyncio.run(getTanHNormalizedPriceChangeByTicker(ticker, _datetime, now()))


def concat(print_progress=False):
    database_name = 'database.csv'
    fieldnames = ['Title', 'Text', 'Time', 'Url', 'Value']

    with open(database_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

    csv_list = [NEWS_CSV_DIRECTORY + '/' + filename for filename in os.listdir(NEWS_CSV_DIRECTORY)]

    for csv_path in csv_list:
        with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            ticker = csv_path.split('/')[-1].split('.')[0]

            for row in reader:
                title = row['Title']
                text = row['Text']
                time = row['Time']
                url = row['Url']
                if print_progress:
                    print('working with ticker', ticker, 'url:', url)

                value = value_from_stock_market(ticker, time)

                with open(database_name, mode='a', newline='', encoding='utf-8') as file1:
                    writer = csv.DictWriter(file1, fieldnames=fieldnames)
                    row = {"Title": title, "Text": text, "Time": time, "Url": url, "Value": value}
                    writer.writerow(row)


if __name__ == '__main__':
    concat(True)
    # print(value_from_stock_market("VKCO", "21.10.2024, 12:31"))