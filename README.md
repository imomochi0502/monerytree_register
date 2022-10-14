# monerytree_resiter

## Use Package In this Script
- selenium
- gspread
- webdriver_manager
- oauth2client
- httplib2
# Set up
## Set .env
In .env, please set money-tree / nomura's account information, spread-sheet-key and  Google clout auth json information.
example:
```
MONEY_TREE_EMAIL=xxxxxxxx@example.com
MONEY_TREE_PASS=xxxxxxx
NOMURA_STOCK_EMAIL=xxxxxxxx@example.com
NOMURA_STOCK_PASS=yyyyyyyyyy
SPREAD_SHEET_KEY=XXXXX-111111-xxxxxxx-2222222
GCP_AUTH_JSON=gspred-sheets-python-xxxxxxx-xxxxxxx.json
```

## Store GCP Auth json file
Details on how to set up.

https://www.twilio.com/blog/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python-jp

The json file which include Auth information is saved at *GCP_Auth* directory.
# Run this application
With GUI (no headless)
> cd  "This package directory"

> python -m mt_resister --store [paypay | stock]

No use GUI (headless)
> cd "This package directory"

> python -m mt_resister --store [paypay | stock]