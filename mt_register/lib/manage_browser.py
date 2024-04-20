# -*- coding: utf-8 -*-
import os
from time import sleep

import selenium  # type: ignore
from selenium import webdriver  # type: ignore
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  # type: ignore
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = ChromeOptions()
serv = Service(ChromeDriverManager().install())


def create_browser(headless: bool = False):
    if headless:
        chrome_options.add_argument("-headless")

    return webdriver.Chrome(service=serv, options=chrome_options)  # type: ignore # noqa


def login_money_tree(browser: selenium.webdriver.chrome.webdriver.WebDriver):  # type: ignore
    try:
        email = os.environ["MONEY_TREE_EMAIL"]
        password = os.environ["MONEY_TREE_PASS"]
    except Exception as e:
        print(e)
        raise KeyError("Email and password are not found.")

    try:
        # Log in to Money Tree
        browser.get("https://app.getmoneytree.com/login")
        sleep(3.0)

        mt_email_input = browser.find_element(by=By.NAME, value="guest[email]")
        mt_email_input.send_keys(email)

        mt_pass_input = browser.find_element(by=By.NAME, value="guest[password]")
        mt_pass_input.send_keys(password)

        mt_login_button = browser.find_element(
            by=By.CLASS_NAME, value="login-form-button"
        )
        mt_login_button.submit()

        print("Logined MoneryTree")
        # Wait while process is completed
        # サインインからコンテンツ取得までに時間を要する場合がある。長めに設定
        sleep(60.0)
    except Exception as e:
        print("MoneyTree Login failer.")
        raise e


def logout_money_tree(browser: selenium.webdriver.chrome.webdriver.WebDriver):  # type: ignore
    try:
        mt_setting_element = browser.find_element(
            by=By.CLASS_NAME, value="icon-thin-cog"
        )
        mt_setting_element.click()
        sleep(3.0)
        mt_logout_element = browser.find_element(
            by=By.CSS_SELECTOR, value=".logout.ng-scope"
        )
        mt_logout_element.click()
        print("Logout MoneyTree")
    except Exception as e:
        print("MoneyTree Logout failer.")
        raise e
