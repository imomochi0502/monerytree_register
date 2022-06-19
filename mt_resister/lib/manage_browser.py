# -*- coding: utf-8 -*-
import os

import selenium  # type: ignore
from requests import options
from selenium import webdriver  # type: ignore
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  # type: ignore
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
serv = Service(ChromeDriverManager().install())

def open_browser(headless:bool = False):
    if headless:
        options.add_argument("-headless")

    return webdriver.Chrome(service=serv, options=options)

