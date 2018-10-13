import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import sqlite3
import time
from selenium import webdriver

conn = sqlite3.connect("C:\ShowApp\Databases\TopShows.db")
c = conn.cursor()

justwatchurl = 'https://www.justwatch.com/us/provider/hulu?content_type=show'
driver = webdriver.Chrome("C:\Python35\chromedriver")
driver.get(justwatchurl)
time.sleep(2)
for i in range(4):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
time.sleep(2)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
asoup = soup.find_all("img", {"style" : re.compile("width: 100%; height: auto;"+".+")})
#print(soup)
#print("End of the soup")
for i in asoup:
    showtitle = i["alt"]
    print(showtitle)
    c.execute("SELECT * FROM TopShows WHERE ShowName = ?", (showtitle,))
    returnedrows = c.fetchall()
    print("Before")
    print(returnedrows)
    if len(returnedrows) > 0:
        print("Existing row")
        c.execute("UPDATE TopShows SET IsHulu = 1 WHERE ShowName = ?", (showtitle,))
    else:
        print("No existing row")
        c.execute("INSERT INTO TopShows ( ShowName, IsHulu ) VALUES ( ?, 1 )", (showtitle,))
    print("After")
    c.execute("SELECT * FROM TopShows WHERE ShowName = ?", (showtitle,))
    returnedrows = c.fetchall()
    print(returnedrows)

conn.commit()
conn.close()

driver.close()