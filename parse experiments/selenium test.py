from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Тикер компании
ticker = "AAPL"

# Настройка драйвера
options = webdriver.ChromeOptions()
#options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Устанавливаем ожидание
wait = WebDriverWait(driver, 15)  # Увеличиваем время ожидания до 15 секунд

try:
    # Переход на сайт Investing.com
    driver.get(f"https://ru.investing.com/search?q={ticker}")
    time.sleep(3)

    # banner_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[id='onetrust-accept-btn-handler']")))
    # banner_button.click()
    # time.sleep(2)

    # Переход на вкладку "Новости"
    first_result = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.js-inner-all-results-quote-item.row")))
    first_result.click()
    time.sleep(5)  # Пауза для загрузки страницы компании

    proceed_button = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
    action = webdriver.ActionChains(driver)
    webdriver.ActionChains(driver)
    action.move_to_element(proceed_button)
    action.move_by_offset(10, 20)
    action.click(proceed_button)
    action.perform()

    # Переходим на вкладку "Новости"
    news_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'news')]")))
    news_tab.click()
    time.sleep(2) # Пауза для загрузки страницы новостей

    # Сбор новостей
    news_items = driver.find_elements(By.CSS_SELECTOR, 'article.js-article-item')
    for item in news_items:
        title = item.find_element(By.CSS_SELECTOR, "a.title").text
        link = item.find_element(By.CSS_SELECTOR, "a.title").get_attribute("href")
        date = item.find_element(By.CSS_SELECTOR, "span.date").text
        print(f"Заголовок: {title}\nСсылка: {link}\nДата: {date}\n")

finally:
    driver.quit()
