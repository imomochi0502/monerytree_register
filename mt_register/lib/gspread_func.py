import gspread
from oauth2client.service_account import ServiceAccountCredentials


def connect_gspread(jsonf, spred_sheet_key):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    worksheet_client = gc.open_by_key(spred_sheet_key)
    return worksheet_client

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
