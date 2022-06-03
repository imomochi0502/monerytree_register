# -*- coding: utf-8 -*-
import selenium # type: ignore
import os
from selenium import webdriver # type: ignore
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By # type: ignore
from time import sleep

email_nomura = os.environ["NOMURA_STOCK_EMAIL"]
pass_nomura = os.environ["NOMURA_STOCK_PASS"]

email_money_t = os.environ["MONEY_TREE_EMAIL"]
pass_money_t = os.environ["MONEY_TREE_PASS"]

options = webdriver.ChromeOptions()

#TODO: Switch this option usgin args
# options.add_argument('-headless')

serv = Service(ChromeDriverManager().install())

browser = webdriver.Chrome(service=serv, options=options)

# ---------Nomura Employee Stock Site-------
browser.get("https://www.e-plan.nomura.co.jp/login/index.html")
sleep(1.0)

mail = browser.find_element(by=By.NAME, value="m_login_mail_address")

password = browser.find_element(by=By.NAME, value="WEAPASS")

mail.clear()
password.clear()

mail.send_keys(email_nomura)
password.send_keys(pass_nomura)

nomura_login = browser.find_element(by=By.CLASS_NAME, value="m_login_btn_01")

#login
nomura_login.submit()
sleep(5.0)

# Skip Notice Page
try:
    browser.find_element(by=By.CSS_SELECTOR, value=".e_btn_active.e_btn_large").click()
except:
    pass

sleep(5.0)

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
browser.get("https://app.getmoneytree.com/login")
sleep(5.0)

mt_email_input = browser.find_element(by=By.NAME, value="guest[email]")
mt_email_input.send_keys(email_money_t)

mt_pass_input = browser.find_element(by=By.NAME, value="guest[password]")
mt_pass_input.send_keys(pass_money_t)

mt_login_button = browser.find_element(by=By.CLASS_NAME, value="login-form-button")
mt_login_button.submit()

# Wait while process is completed
sleep(10.0)

# click "Kouza zandaka"
zandaka_button_element = browser.find_element(by=By.XPATH, value='//*[@id="mt-webapp"]//*[contains(text(), "口座残高")]')
zandaka_button_element.click()
sleep(1.0)

#Click "その他"
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

#ログアウト処理
mt_setting_element = browser.find_element(by=By.CLASS_NAME, value="icon-thin-cog")
mt_setting_element.click()
mt_logout_element = browser.find_element(by=By.CSS_SELECTOR, value=".logout.ng-scope")
mt_logout_element.click()

browser.close()
