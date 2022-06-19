import os
from re import I
from time import sleep

import selenium
from selenium.webdriver.common.by import By  # type: ignore

from .manage_browser import login_money_tree


def store(browser:selenium.webdriver.chrome.webdriver.WebDriver):

    #login_nomura(browser)
    try:
        email = os.environ["NOMURA_STOCK_EMAIL"]
        password = os.environ["NOMURA_STOCK_PASS"]
    except:
        KeyError("Email and password are not found.")

    browser.get("https://www.e-plan.nomura.co.jp/login/index.html")
    sleep(1.0)

    try:
        mail = browser.find_element(by=By.NAME, value="m_login_mail_address")
        password = browser.find_element(by=By.NAME, value="WEAPASS")
        mail.clear()
        password.clear()

        mail.send_keys(email)
        password.send_keys(password)

        nomura_login = browser.find_element(by=By.CLASS_NAME, value="m_login_btn_01")
        
        #login
        nomura_login.submit()
        sleep(5.0)
    except Exception as e:
        print("login to nomura is failer.")
        raise e

    # Skip Notice Page
    try:
        browser.find_element(by=By.CSS_SELECTOR, value=".e_btn_active.e_btn_large").click()
    except:
        pass

    sleep(5.0)

    try:
        #Get stock value
        now_stock_element = browser.find_element(by=By.XPATH, value='//*[@id="container"]/div[2]/div[2]/dl/dd/span[2]')
        stock_value = (now_stock_element.text).replace(",","")
        stock_value = int(stock_value)
        print(stock_value)

        # Log out from NOURA Stock service
        logout_element = browser.find_element(by=By.XPATH, value='//*[@id="m_self_reissue"]/ul/li[3]/a/span[2]')
        logout_element.click()

        sleep(3.0)

        # Log in to Money Tree
        login_money_tree(browser)

        # click "Kouza zandaka"
        zandaka_button_element = browser.find_element(by=By.XPATH, value='//*[@id="mt-webapp"]//*[contains(text(), "口座残高")]')
        zandaka_button_element.click()
        sleep(1.0)

        #Click "Sonota"
        other_in_list_element= browser.find_element(by=By.XPATH, value='//*[@id="mt-webapp"]//*[contains(text(), "その他")]')
        other_in_list_element.click()
        sleep(1.0)


        target_category_element = browser.find_element(by=By.XPATH, value='//*[@id="mt-webapp"]//*[contains(text(), "持株会")]')
        target_category_element.click()
        sleep(1.0)

        bank_value_element = browser.find_element(by=By.CSS_SELECTOR, value=".balance.ng-binding")
        bank_value_element.click()

        exp_inc_switch_element = browser.find_element(by=By.CSS_SELECTOR, value=".icon-minus-circle.ng-scope")
        exp_inc_switch_element.click()

        # input stock value
        banck_amount_element = browser.find_element(by=By.CLASS_NAME, value="input-amount")
        banck_amount_element.clear()
        banck_amount_element.send_keys(stock_value)

        update_element = browser.find_element(by=By.CSS_SELECTOR, value=".update.ng-scope")
        update_element.click()
    except Exception as e:
        raise 
