import sqlite3
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import re

def Login():
    driver.find_element_by_class_name('navigation__action-button').click()
    # Modify the next two lines to check local file for login information
    driver.find_element_by_name('email').send_keys([email here])
    driver.find_element_by_name('password').send_keys([password here])
    # This is to avoid putting login info into a repository
    driver.find_elements_by_class_name('login-button')[1].click()
    time.sleep(2)
    driver.find_element_by_link_text('Nicholas').click()

def GetUrlsForShow(show):
    driver.find_element_by_id('q').send_keys(show)
    driver.find_element_by_id('search-icon').click()
    time.sleep(1)
    driver.find_element_by_link_text(show).click()
    time.sleep(1)
    driver.find_element_by_xpath('//a[starts-with(@href,"' + '/grid/' + '")]').click()
    time.sleep(1)
    numberofseasons = int(GetSeasonNumber())
    #print(numberofseasons)
    allinfo = []
    for season in range(1,numberofseasons+1):
        driver.find_element_by_link_text(str(season)).click()
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        epurls = [x.get_attribute('href') for x in driver.find_elements_by_xpath('//a[starts-with(@href,"/watch/")]')]
        epseasstrings = [re.findall(r'\d+',x.text)[:2] for x in driver.find_elements_by_partial_link_text('Season')]
        epsinseason = max([int(x[1]) for x in epseasstrings])
        seasinfo = [[int(x[0]), int(x[1]), y] for x,y in zip(epseasstrings, epurls)]
        allinfo += seasinfo
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
    return allinfo

def GetSeasonNumber():
    allseasonnums = [x.text for x in driver.find_elements_by_xpath('//a[starts-with(@class,"btn")]')]
    maxseasonnum = max([num for num in allseasonnums if num != 'ALL'])
    return maxseasonnum

def UpdateEpisodeTable(showinfo,show):
    for row in showinfo:
        c.execute('UPDATE Episodes SET HuluUrl = ? WHERE ShowName = ? AND EpisodeNumber = ? AND SeasonNumber = ?',
                 (row[2],show,row[1],row[0],))

conn = sqlite3.connect("C:\ShowApp\Databases\TopShows.db")
c = conn.cursor()

huluurl = 'https://www.hulu.com/'
showname = 'Malcolm in the Middle'
driver = webdriver.Chrome("C:\Python35\chromedriver")
driver.maximize_window()
driver.get(huluurl)
time.sleep(2)
if driver.current_url == 'https://www.hulu.com/welcome':
    Login()
time.sleep(2)
showinfo = GetUrlsForShow(showname)
print(showinfo)
UpdateEpisodeTable(showinfo,showname)
conn.commit()
conn.close()

driver.close()

