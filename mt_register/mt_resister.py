import argparse
import getpass
import os
from os.path import dirname, join

from dotenv import load_dotenv

from .lib import manage_browser, store_paypay, store_stock


def set_dotenv(path: str):
    print("Set .env")
    dotenv_dict = {}
    dotenv_dict["MONEY_TREE_EMAIL"] = input("Enter money tree email :")
    dotenv_dict["MONEY_TREE_PASS"] = getpass.getpass("Enter password : ")
    dotenv_dict["NOMURA_STOCK_EMAIL"] = input("Enter nomura stock email :")
    dotenv_dict["NOMURA_STOCK_PASS"] = getpass.getpass("Enter password :")
    dotenv_dict["SPREAD_SHEET_KEY"] = input("Enter Spread Sheet key :")
    dotenv_dict["GCP_AUTH_JSON"] = input(
        "Enter Json file name for Authorization to GCP :"
    )

    text_list = [f"{key}={val}" for key, val in dotenv_dict.items()]
    text_dotenv = "\n".join(text_list)
    print(text_dotenv)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text_dotenv)


def main_exec(args: argparse.Namespace):
    args_dict = vars(args)
    store = args_dict.get("store", "").lower()

    if store not in ["stock", "paypay", "cash"]:
        raise ValueError("The specified 'store' target does not exist.")

    browser = manage_browser.create_browser(headless=args_dict["headless"])
    print("Browser Creation Success")
    try:
        if store == "stock":
            store_stock.store(browser=browser)
        elif store == "paypay":
            store_paypay.store(browser=browser, regist_name="paypay")
        elif store == "cash":
            store_paypay.store(browser=browser, regist_name="cash")
    except Exception as e:
        print(e)
    finally:
        browser.close()

    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true", help="")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument(
        "--store",
        help="[stock] or [paypay] or [cash]",
        default="stock",
        type=str,  # noqa
    )

    args = parser.parse_args()

    dotenv_path = join(dirname(__file__), ".env")

    # .env ファイルが存在しない場合
    if not os.path.exists(dotenv_path):
        print(f"{dotenv_path} is not found.")
        args.init = True

    if args.init is True:
        set_dotenv(dotenv_path)

    load_dotenv(dotenv_path)

    main_exec(args)

    return
