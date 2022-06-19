import argparse
import getpass
import imp
import os
from mimetypes import init
from os.path import dirname, join

import dotenv
from dotenv import load_dotenv

from .lib import store_paypay, store_stock


def set_dotenv(path:str):
    print("Set .env")
    dotenv_dict = {}
    dotenv_dict["MONEY_TREE_EMAIL"] = input(f"Enter money tree email :")
    dotenv_dict["MONEY_TREE_PASS"] = getpass.getpass("Enter password : ")
    dotenv_dict["NOMURA_STOCK_EMAIL"] = input(f"Enter nomura stock email :")
    dotenv_dict["NOMURA_STOCK_PASS"] = getpass.getpass("Enter password :")
    dotenv_dict["SPREAD_SHEET_KEY"] = input(f"Enter Spread Sheet key :")
    dotenv_dict["GCP_AUTH_JSON"] = input(f"Enter Json file name for Authorization to GCP :")

    text_list = [f"{key}={val}" for key, val in dotenv_dict.items()]
    text_dotenv = "\n".join(text_list)
    print(text_dotenv)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text_dotenv)

def main_exec(args: argparse.Namespace):
    args_dict = vars(args)
    store = args_dict.get("store").lower()

    if store not in ["stock", "paypay"]:
        raise ValueError("The specified 'store' target does not exist.")
    
    if store == "stock":
        store_stock.store()
    elif store == "paypay":
        store_paypay.store()
    

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true", help="")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--store", help="[stock] or [paypay]", default="stock", type=str)
    
    args = parser.parse_args()

    dotenv_path = join(dirname(__file__), '.env')

    # .env ファイルが存在しない場合
    if not os.path.exists(dotenv_path) :
        print(f"{dotenv_path} is not found.")
        args.init = True

    if args.init is True:
        set_dotenv(dotenv_path)
    
    load_dotenv(dotenv_path)
    
    main_exec(args)
    
    return
