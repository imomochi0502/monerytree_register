from .manage_browser import open_browser


def store():
    browser = open_browser()
    browser.get("https://www.google.com/")
