import datetime as dt
import os
from os.path import join
from time import sleep

import selenium
from selenium.webdriver.common.by import By  # type: ignore

from .gspread_func import cellsto1darray, cellsto2darray, connect_gspread
from .manage_browser import login_money_tree


def input_cash_log(browser, dt_now, store_info):
    try:
        print(store_info["date"], store_info["type"], store_info["detail"], store_info["value"])
        
        date_split = [ int(value) for value in store_info["date"].split("/")]
        year, month, day = date_split[0], date_split[1], date_split[2]

        now_year = dt_now.year
        now_month = dt_now.month
    except Exception as e:
        raise e
    
    diff_yaer = now_year - year
    diff_month = now_month - month + 12 * diff_yaer

    try:
        # serach x-path "Inputting cash"
        target_element = browser.find_element(by=By.XPATH, value='//*[@class="ng-scope"]//*[contains(text(), "現金入力")]')
        target_element.click()
        sleep(2.0)

        # select date
        target_element = browser.find_element(by=By.CLASS_NAME, value="datepicker")
        target_element.click()
        sleep(0.5)

        print("diff month", diff_month)

        # month
        for count in range(diff_month):
            target_element = browser.find_element(by=By.CLASS_NAME,value="picker__nav--prev")
            target_element.click()
            sleep(0.5)

        # day
        date_for_xpath = f"{year}年{month}月{day}日"
        target_element = browser.find_element(by=By.XPATH, value=f'//div[@aria-label="{date_for_xpath}"]')
        target_element.click()
        sleep(0.5)
        

        #入金(受け取りの場合 + にする)
        if "受け取り" in store_info["type"]:
            target_element = browser.find_element(by=By.CSS_SELECTOR, value=".icon-minus-circle.ng-scope")
            target_element.click()
            sleep(0.5)

        #金額入力
        target_element = browser.find_element(by=By.CLASS_NAME, value="input-amount")
        target_element.clear()
        target_element.send_keys(store_info["value"])
        sleep(0.5)

        # input detail
        # ref: https://qiita.com/VA_nakatsu/items/0095755dc48ad7e86e2f#10-label-%E3%81%A7%E6%A4%9C%E7%B4%A2
        target_element = browser.find_element(by=By.XPATH, value='//input[@placeholder="入力してください"]')
        target_element.clear()
        target_element.send_keys(store_info["detail"])
        sleep(0.5)

        # カテゴリ選択ボタンクリック
        target_element = browser.find_element(by=By.XPATH, value='//*[@class="ng-scope"]//*[contains(text(), "未定")]')
        target_element.click()
        sleep(0.5)

        # カテゴリ検索
        # paypay はすべて小文字
        target_element = browser.find_element(by=By.XPATH, value='//input[@type="search"]')
        target_element.clear()
        target_element.send_keys("paypay")
        sleep(0.5)

        # カテゴリ選択
        target_element = browser.find_element(by=By.XPATH, value='//*[@class="ng-scope"]//*[contains(text(), "PayPay")]')
        target_element.click()
        sleep(0.5)

        # save
        target_element = browser.find_element(by=By.CLASS_NAME, value="modal-header-done-text")
        target_element.click()

    except Exception as e:
        raise e


def store(browser: selenium.webdriver.chrome.webdriver.WebDriver): # type: ignore
    dt_now = dt.date.today()

    json_file_name = os.environ["GCP_AUTH_JSON"] 
    key = os.environ["SPREAD_SHEET_KEY"]

    file_path = os.path.dirname(os.path.abspath(__file__))
    jsonf = join(os.path.abspath(join(file_path, "..")), f"GCP_Auth/{json_file_name}")

    try:
        ws = connect_gspread(jsonf=jsonf, key=key)
    except Exception as e:
        print(e)
        raise e

    ss_row_count = ws.row_count
    ss_data_raw = ws.range('A1:F' + str(ss_row_count)) 

    # convert 1d array -> 2d array
    ss_data_2d = cellsto2darray(ss_data_raw, 6)
    ss_data_2d.pop(0)

    store_datas = []
    for i in range(len(ss_data_2d)):
        if ss_data_2d[i][4].value == "TRUE":
            continue
        ss_data_2d[i][3].value = int(ss_data_2d[i][3].value) # 元データ書き換え
        ss_data_2d[i][4].value = False # 元データを書き換え
        store_datas.append(ss_data_2d[i])

    update_list = []
    if len(store_datas) > 0:
        # connect money tree
        login_money_tree(browser)

        
        for i in range(len(store_datas)):

            store_info = {
                "date":store_datas[i][0].value,
                "type": store_datas[i][1].value,
                "detail": store_datas[i][2].value,
                "value": store_datas[i][3].value
            }

            try:
                input_cash_log(browser, dt_now, store_info)
                sleep(1.0)
            except Exception as e:
                print(e)
                continue
        
            store_datas[i][4].value = True
            store_datas[i][5].value = dt_now.strftime("%Y/%m/%d")
            update_list.append(store_datas[i])

    if update_list:
        ws.update_cells(cellsto1darray(update_list))
    else:
        print("There is no storing data")

