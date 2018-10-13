from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import pandas

driver = webdriver.Chrome("C:\\Python34\\selenium\\webdriver\\chromedriver\\chromedriver.exe")
driver.set_page_load_timeout(30)
driver.get("http://www.netflix.com")
driver.maximize_window()
driver.implicitly_wait(20)
driver.find_element_by_link_text('Sign In').click()
# Need to modify following lines to call into local file holding login information
driver.find_element_by_name('email').send_keys([email here])
driver.find_element_by_name('password').send_keys([username here])
# This is to avoid putting login info into a repository
driver.find_element_by_tag_name('button').click()
driver.find_elements_by_class_name('profile-icon')[1].click()

MyListButton = driver.find_element_by_link_text('My List')
BrowseElement = driver.find_element_by_css_selector('.browse.active.hasSubMenu')
actions = ActionChains(driver)
actions.move_to_element(BrowseElement)
actions.click(MyListButton)
actions.perform()
time.sleep(3)
#MITMPlayButton = driver.find_element_by_css_selector('.bob-play.bob-play-lowerTop.playLink')

#driver.find_elements_by_class_name('video-artwork')[0].click()
MITMSpot = driver.find_element_by_xpath('//div[@aria-label="Malcolm in the Middle"]')
MITMSpot.find_element_by_class_name('video-artwork').click()
driver.find_element_by_class_name('Episodes').click()
time.sleep(3)
driver.find_element_by_class_name('sub-menu-link').click()


# Initializes function with two arguments
def Chooser(Update=0, MinView=0):
    # Opens .csv file containing episodes
    EpTable = pandas.DataFrame.from_csv(path='C:\\Users\\Nicholas\\My Documents\\MITMEpisodes.csv')

    # If MinView is set to 1, only an episode number with the minimum number of view may be selected
    if MinView:
        MinRows = EpTable[EpTable['Views'] == min(EpTable['Views'])]
        # print(MinRows)
        Num = random.choice(MinRows.index)
    # If MinView is set to 0, any episode number from 1 to 151 may be chosen
    else:
        Num = random.randint(1, 151)
    # If Update set to 1, the Views column of the selected episode is increased by 1
    if Update:
        # print(EpTable.loc[Num])
        EpTable.loc[Num, 'Views'] += 1
    # Selects row from .csv file with episode number equal to Num
    Output = EpTable.loc[Num]
    # Print episode info
    print("Episode: " + str(Output[0]))
    print("Season: " + str(Output[1]))
    print("Name: " + str(Output[2]))
    print("Views: " + str(Output[3]))

    # Saves changes to .csv file
    EpTable.to_csv('C:\\Users\\Nicholas\\My Documents\\MITMEpisodes.csv', index=True, mode='w')

    return Output

# Calls function
EpInfo = Chooser(Update=1, MinView=1)

SeasonNum = str(int(EpInfo[1]))
SeasonString = 'Season ' + SeasonNum
print(SeasonString)
driver.find_element_by_link_text(SeasonString).click()

EpisodeNum = str(int(EpInfo[0]))

print(EpisodeNum)

Playing = 0

CurrentEps = []

while Playing == 0:
    time.sleep(2)
    CurrentEpsElements = driver.find_elements_by_class_name('episodeNumber')
    CurrentEps.clear()

    for Ep in CurrentEpsElements:
        #print(Ep.text)
        if Ep.text != '':
            CurrentEps.append(int(Ep.text))

    print('CurrentEps')
    print(CurrentEps)
    print(max(CurrentEps))
    print(min(CurrentEps))


    if int(EpisodeNum) in CurrentEps:
        time.sleep(1)
        print(EpisodeNum)
        #EpisodeElement = driver.find_element_by_xpath("//span[contains(text(), EpisodeNum)]")
        driver.find_element_by_xpath(("//*[span = " + EpisodeNum + "]")).click()
        Playing = 1
    elif int(EpisodeNum) < min(CurrentEps):
        driver.find_element_by_css_selector('span.handle.handlePrev.active').click()
        #Hit the left button
    else:
        driver.find_element_by_css_selector('span.handle.handleNext.active').click()
        #Hit the right button



#EpisodeNumberElement.find_element_by_xpath('..').click()