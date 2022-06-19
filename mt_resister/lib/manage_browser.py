# -*- coding: utf-8 -*-
import os
from time import sleep

import selenium  # type: ignore
from requests import options
from selenium import webdriver  # type: ignore
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  # type: ignore
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
serv = Service(ChromeDriverManager().install())

def create_browser(headless:bool = False)->None:
    if headless:
        options.add_argument("-headless")

    return webdriver.Chrome(service=serv, options=options)

def login_monery_tree(browser:selenium.webdriver.chrome.webdriver.WebDriver):
    try:
        email = os.environ["MONEY_TREE_EMAIL"]
        password = os.environ["MONEY_TREE_PASS"]
    except:
        KeyError("Email and password are not found.")
    
    try:
        # Log in to Money Tree
        browser.get("https://app.getmoneytree.com/login")
        sleep(5.0)

        mt_email_input = browser.find_element(by=By.NAME, value="guest[email]")
        mt_email_input.send_keys(email)

        mt_pass_input = browser.find_element(by=By.NAME, value="guest[password]")
        mt_pass_input.send_keys(password)

        mt_login_button = browser.find_element(by=By.CLASS_NAME, value="login-form-button")
        mt_login_button.submit()

        # Wait while process is completed
        sleep(10.0)
    except Exception as e:
        raise e

