import argparse
import getpass
import os
from os.path import dirname, join

import dotenv
from dotenv import load_dotenv


def set_dotenv(path:str):
    print("Set .env")
    dotenv_dict = {}
    dotenv_dict["MONEY_TREE_EMAIL"] = input(f"Enter money tree email ({dotenv_dict.get('MONEY_TREE_EMAIL')}) :")
    dotenv_dict["MONEY_TREE_PASS"] = getpass.getpass("Enter password : ")
    dotenv_dict["NOMURA_STOCK_EMAIL"] = input(f"Enter nomura stock email ({dotenv_dict.get('NOMURA_STOCK_EMAIL')}) :")
    dotenv_dict["NOMURA_STOCK_PASS"] = getpass.getpass("Enter password : ")

    text_list = [f"{key}={val}" for key, val in dotenv_dict.items()]
    text_dotenv = "\n".join(text_list)
    print(text_dotenv)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text_dotenv)

def store_stock():
    return

def store_paypay():
    return 

def main_exec(args):

    args_dict = args

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true", help="")
    parser.add_argument("--stock", action="store_true", help="stack value")
    parser.add_argument("--paypay", action="store_true", help="paypay")
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

if __name__ == "__main__":
    main()
