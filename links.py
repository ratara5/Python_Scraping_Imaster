import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from getpass import getuser

options=webdriver.ChromeOptions()
options.add_argument(r'--user-data-dir=C:/Users/{}/AppData/Local/Google/Chrome/User DataDefault'.format(getuser()))
options.add_argument('--profile-directory=Default')
#options.add_argument('--headless')

#INSTANCE WEBDRIVER
chrome_browser=webdriver.Chrome(executable_path=r'C:/Users/{}/VscodeFiles/python/linksImaster/driver/chromedriver.exe'.format(getuser()),options=options) 

#SURF TO WEB
chrome_browser.get('https://imaster.academy/login')

#LOGIN: Identify Webelements
user=chrome_browser.find_element(By.XPATH,'//input[@name="username"]')
password=chrome_browser.find_element(By.XPATH,'//input[@name="password"]')

#LOGIN: Write Content
userMsg='' #TODO: write user as string
passMsg='' #TODO: wrte password as string
user.send_keys(userMsg)
password.send_keys(passMsg)

#LOGIN: Send Content
chrome_browser.find_element(By.XPATH,'//button[@type="submit"]'). click()

#OPEN FILE TO WRITE
file = open("C:/Users/{}/VscodeFiles/python/linksImaster/out/linksOut.txt".format(getuser()), "a")
file.write('ENLACES FORMACIÓN MINTIC\n')

#CARD
deckCards=WebDriverWait(chrome_browser,10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="card-deck dashboard-card-deck "]')))
cards=deckCards.find_elements(By.XPATH,'//div[@class="card dashboard-card"]')
c=len(cards)
print('Se encontraron {} asignaturas...'.format(c))
for i in range(0,c):
    deckCards=WebDriverWait(chrome_browser,10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="card-deck dashboard-card-deck "]')))
    course=chrome_browser.find_elements(By.XPATH,'//span[@class="multiline"]')[i]
    file.write('Curso: {}\n'.format(course.text))
    course.click()

    #MEETINGS
    nav=WebDriverWait(chrome_browser,10).until(EC.presence_of_element_located((By.XPATH, '//ul[@class="nav nav-tabs mb-3"]'))) #Doesn't find the element
    items=nav.find_element(By.XPATH,'//li[@class="nav-item"]')
    item=items.find_element(By.XPATH,'//a[@title="Sesiones"] | //a[@title="Sesiones Sincrónicas"] | //a[@title="Sesiones Sincrónicas "]')
    item.click()
    
    #VIDEO
    videosList=WebDriverWait(chrome_browser,20).until(EC.presence_of_element_located((By.XPATH, '//div[@class="studyContent__item__column"]')))
    videoList=chrome_browser.find_elements(By.XPATH,'//div[@class="studyContent__item__column"]')
    v=len(videoList)
    print('Se encontraron {} clases de la asignatura {}'.format(v,i+1))
    for j in range(0,v):
        print('Obteniendo clase {} de la asignatura {}'.format(j+1,i+1))
        videosList=WebDriverWait(chrome_browser,10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="studyContent__item__column"]')))
        video=chrome_browser.find_elements(By.XPATH,'//span[@class="studyContent__item__title"]')[j]
        file.write('\t{}\n'.format(video.text))
        video.click()               
        
        #LINK
        time.sleep(2)
        chrome_browser.switch_to.frame("agilessonBackdrop__iframe")
        player=WebDriverWait(chrome_browser,10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="player"]')))        
        link=chrome_browser.find_element(By.XPATH,'//a[@class="ytp-title-link yt-uix-sessionlink"]')
        file.write('\t\t{}\n'.format(link.get_attribute('href')))
    
        #UP LEVEL
        chrome_browser.switch_to.parent_frame()
        buttonClose=chrome_browser.find_element(By.XPATH,'//button[@class="agilessonBackdrop__close"]').click()
        chrome_browser.switch_to.default_content()

    #UP LEVEL
    file.write('\n')
    chrome_browser.get('https://imaster.academy/')

file.close()
