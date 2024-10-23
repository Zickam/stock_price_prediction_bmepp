import selenium
from selenium import webdriver


driver = webdriver.Chrome()
driver.get("https://ru.investing.com/equities/sberbank_rts-news")

def find_news(ticker: str)-> list[dict]:
    pass