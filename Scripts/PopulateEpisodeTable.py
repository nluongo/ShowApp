import urllib.request
import sqlite3
from bs4 import BeautifulSoup
import re
import time

#Open connection to sqlite database
showconn = sqlite3.connect("../Databases/TopShows.db")
showc = showconn.cursor()

#Get show title names from TopShows table
showc.execute("SELECT * FROM TopShows")

rows = showc.fetchall()
showtitles = [row[1] for row in rows]


#For each show, grab list of episodes from wikipedia
for showtitle in showtitles:
    formattedtitle = showtitle.replace(' ','_')
    #print(formattedtitle)
    listofurl = "http://en.wikipedia.org/wiki/List_of_" + formattedtitle + "_episodes"
    #print(listofurl)
    try:
        HTML = urllib.request.urlopen(listofurl).read()
        source = "listof"
    except:
        try:
            tvseriesurl = "http://en.wikipedia.org/wiki/" + formattedtitle + "_(TV_series)"
            HTML = urllib.request.urlopen(tvseriesurl).read()
            source = "tvseries"
        except:
            print("Still nothing for this show:")
            print(showtitle)
            print(formattedtitle)
            print(listofurl)
    soup = BeautifulSoup(HTML, "html.parser")
    prettysoup = soup.prettify()
    seasonnumber = 0
    #Loop over all tables on the page
    for table in soup.body.find_all("table"):
        #Only consider the wikiepisodetable type tables
        if table.get("class") == [u'wikitable', u'plainrowheaders', u'wikiepisodetable']:
            #Get the row with the column titles
            headerrow = table.find("tr").find_all("th")
            #Split this row into separate text fields and replace any line breaks with spaces
            headercols = [col.text.replace("\n"," ") for col in headerrow]
            #If the first three column titles don't match the template, move to the next table
            if headercols[0:3] != ['No. overall', 'No. in season', 'Title']:
                continue
            #Assume every table we've found that passes the previous checks represents a new season
            seasonnumber += 1
            for tablerow in table.find_all("tr" , { "class" : "vevent"}):
                overallepnum = tablerow.find("th").text
                tdrows = tablerow.find_all("td")
                numinseason = tdrows[0].text
                epname = tdrows[1].text
                if epname == "TBA":
                    continue
                citeregex = re.compile('.+\[([0-9]+)\]')
                if citeregex.search(epname):
                    epname = re.sub('\[([0-9]+)\]','',epname)
                while epname[0] == '"' and epname[-1] == '"':
                    epname = epname[1:len(epname)-1]
                showc.execute("INSERT INTO Episodes VALUES ( NULL, ?, ?, ?, ?, ?, NULL, NULL )", (showtitle, overallepnum, seasonnumber, numinseason, epname,))
                #print(overallepnum)
                #print(seasonnumber)
                #print(numinseason)
                #print(epname)
    time.sleep(1)

showconn.commit()
showconn.close()