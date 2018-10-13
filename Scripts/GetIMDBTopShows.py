import urllib.request
from bs4 import BeautifulSoup
import re
import sqlite3

conn = sqlite3.connect("C:\ShowApp\Databases\TopShows.db")
c = conn.cursor()

imdburl = 'http://www.imdb.com/search/title?title_type=tv_series'
html = urllib.request.urlopen(imdburl).read()
soup = BeautifulSoup(html, "html.parser")
asoup = soup.find_all("a",href=re.compile("/title/tt"+".+"+"adv_li_tt"),text=re.compile("\w"))
writefile = open(r'C:\Users\Nicholas\Desktop\Soup.txt', "w")
for i in asoup:
    c.execute("INSERT INTO TopShows ( ShowName ) VALUES ( ? )", (i.text,))
    writefile.write(i.text+"\n")
    print(i.text)

conn.commit()
c.close()
writefile.close()
