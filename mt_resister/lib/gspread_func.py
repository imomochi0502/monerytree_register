import gspread
from httplib2 import Credentials
from oauth2client.service_account import ServiceAccountCredentials


def connect_gspread(jsonf,key):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    SPREADSHEET_KEY = key
    worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
    return worksheet

# https://qiita.com/yH3PO4/items/6517481b1e7128ca7b36
def cellsto2darray(cells, col):  # colは列の数
    cells2d = []
    for i in range(len(cells) // col):
        cells2d.append(cells[i * col:(i + 1) * col])
    return cells2d

def cellsto1darray(cells2d):
    cells1d = []
    for cells in cells2d:
        cells1d.extend(cells)
    return cells1d
