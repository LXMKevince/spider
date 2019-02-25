from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re


chrome_driver = 'C:/Users/Administrator/Desktop/spiders/day3/chromedriver_win32/chromedriver.exe'
browser = webdriver.Chrome(executable_path=chrome_driver)


wait = WebDriverWait(browser, 10)


def search():
    try:
        browser.get('https://www.jd.com')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#key"))
        )
        submit = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#search > div > div.form > button'))
        )
        input.send_keys('美食')
        submit.click()
        total = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > em:nth-child(1) > b'))
        )
        return total.text
    except TimeoutException:
        return search()


def next_page(page_number):
    try:
        input = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > input"))
        )
        submit = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > a'))
        )
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, '#J_bottomPage > span.p-num > a.curr'), str(page_number))
        )
    except TimeoutException:
        next_page(page_number)


def main():
    total = search()
    total = int(total)
    for i in range(2, total + 1):
        next_page(i)

if __name__ == '__main__':
    main()
