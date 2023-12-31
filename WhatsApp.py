#!/usr/bin/python3

import SharedMethods
from Person import *
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep



webdriverPath = "/home/mr124/Documents/geckodriver"
profilePath =  "/home/mr124/Project/SocialMediaInvestigationFramework/WhatsAppProfile"

logger = SharedMethods.logSetup.log("whatsApp","log.txt")

class XPath():
    def __init__(self):
        self.newChatXpath = '//*[@id="app"]/div/div/div[4]/header/div[2]/div/span/div[4]/div/span'
        self.searchXpath = '//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/div[1]/div[2]/div[2]/div/div[1]/p'
        self.smallImageXpath = '//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/div[2]/div/div/div/div[2]/div/div/div[1]/div/div/img'
        self.aboutXpath = '//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/div[2]/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/span'
        self.contactDivXpath = '/html/body/div[1]/div/div/div[5]/div/header/div[2]'
        self.imageDivXpath = '/html/body/div[1]/div/div/div[6]/span/div/span/div/div/section/div[1]'
        self.imageIfCoverXpath = '/html/body/div[1]/div/div/div[6]/span/div/span/div/div/section/div[1]/div[2]/div/div/img'
        self.imageIfNoCoverXpath = '/html/body/div[1]/div/div/div[6]/span/div/span/div/div/section/div[1]/div[1]/div/img'
        self.whatsAppUrl = "https://web.whatsapp.com"


class WhatsApp(Person,XPath):
    def __init__(self, phoneNumber=None, name=None):
        self.logger = logger
        self.webdriverPath = webdriverPath
        self.profilePath = profilePath
        self.Xpath = XPath()
        self.Person = Person(name=name,phoneNumber=phoneNumber)

    def saveCookie(self, cookieFileName ,cookies):
        if cookies:
            with open(cookieFileName,"w") as cookieFile:
                json.dump(cookies, cookieFile, indent=4)
            self.logger.info("done writeing what's app cookie")
            return True
        else:
            self.logger.error("erro in saving the cookie")

    def LoadCookeFile(self, cookieFileName):
        if SharedMethods.BaseClass.checkIfFileExist(cookieFileName):
            with open(cookieFileName, 'r') as cookiesFile:
                cookies = json.load(cookiesFile)
                self.logger.info(f"done loading cookefile {cookieFileName}")
                return cookies
        else:
            self.logger.error("can't load cooke file")
            return False

        
    def setupWhatsAppProfile(self):
        driver = SharedMethods.BaseClass.CreatWebDriver(self.webdriverPath, self.profilePath)
        driver.get(self.Xpath.whatsAppUrl)
        self.logger.info("Link Your Device")
        SaveCookie = input("Done Linking Save the cookie?: Y/n ")
        if SaveCookie.lower() == "y" or SaveCookie.lower == 'yes':
            cookies = driver.get_cookies()
            while not cookies:
                input("retry Getting cookies: ?")
                cookies = driver.get_cookies()
            driver.quit()
    
    def LoadCookies(self):
        # not ready yet
        driver = SharedMethods.BaseClass.CreatWebDriver(self.webdriverPath)
        WhatsAppCookies = self.LoadCookeFile("WhatsAppCookies.json")
        if WhatsAppCookies:
            for cookie in WhatsAppCookies:
                driver.add_cookie(cookie)
            else:
                self.logger.info("done adding the cookies")
        return driver

    def creatWhatssAppDriver(self, HeadLess=None):
        driver = SharedMethods.BaseClass.CreatWebDriver(self.webdriverPath, self.profilePath, HeadLess=HeadLess)
        driver.get(self.Xpath.whatsAppUrl)
        self.logger.info("now opened whatsApp")
        self.driver = driver
        return True
        
    def checkIfWhatsAppLoaded(self):
        try:
            element = WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.CLASS_NAME, "_3WByx")))
            if element:
                self.logger.info("whatsApp page loaded")
                return True
        except TimeoutException as e:
            self.logger.error("Time out on loading whatsApp")


    def findElementByXpath(self, xpath):
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            if element:
                return element
            else:
                return False
        except:
            self.logger.error("can't find element")

    def findElementByClass(self, ClassName):
        try:
            element = driver.find_element(By.CLASS_NAME, ClassName)
            if element:
                return element
            else:
                return False
        except:
            self.logger.error("can't find element")
    
    def sendKeys(self, word=None):
        actions = ActionChains(self.driver)
        actions.send_keys(word)
        actions.perform()

    def OpenContactViaUrl(self):
        try:
            print("hello")
            print(f'{self.Xpath.whatsAppUrl}/send?phone={self.Person.phoneNumber}')
            self.driver.get(f'{self.Xpath.whatsAppUrl}/send?phone={self.Person.phoneNumber}')
            return True
        except:
            self.logger.error("can't find contact")
            return False
    
    def searchContact(self):
        try:
            newChatElement = self.findElementByXpath(self.Xpath.newChatXpath)
            newChatElement.click()
            searchElement = self.findElementByXpath(self.Xpath.searchXpath)
            searchElement.click()
            self.sendKeys(word=self.Person.phoneNumber)
            self.logger.info("done searching for contact ")
            sleep(3)
            return True
        except:
            self.logger.error("can't find contact")
            return False

    def OpenContact(self):
        try:
            smallImageElement = self.findElementByXpath(self.Xpath.smallImageXpath)
            smallImageElement.click()
            self.logger.info("Done opening the contact chat")
            return True
        except:
            self.logger.error("error in opening the contact chat")


    def OpenContactInfo(self):
        try:
            contactDiv = self.findElementByXpath(self.Xpath.contactDivXpath)
            contactDiv.click()
            self.logger.info("done opeing the about")
            return True
        except:
            self.logger.error("can't open the contact Info")
    
    def getUrlFromimg(self, element):
        try:
            if element.tag_name == 'img':
                return element.get_attribute('src')
        except:
            self.logger.error("can't find url from the element")
            return False
        

    def getSmallImageUrl(self):
        # set the value of the small image url MUSTH RUN AFTER OPEN CONTACT
        try:
            smallImageElement = self.findElementByXpath(self.Xpath.smallImageXpath)
            smallImageUrl = self.getUrlFromimg(element=smallImageElement)
            self.smallImageUrl = smallImageUrl
            self.logger.info("Done finding small image url")
            return True
        except:
            self.logger.error("can't find the small image")
            return False
    
    def getAbout(self):
        try:
            aboutElemnet = self.findElementByXpath(self.Xpath.aboutXpath)
            if aboutElemnet:
                self.about = aboutElemnet.text
                self.logger.info("done finding about")
                return True
            else:
                self.logger.error("can't find about element")
        except:
            self.logger.error("can't get about ")
        
    def findImageLink(self):
        try:
            imageElement = self.findElementByXpath(self.Xpath.imageDivXpath)
            imgs = imageElement.find_elements(by='xpath', value='.//img')
            if imgs:
                imageUrl = self.getUrlFromimg(imgs[0])
                self.imageUrl = imageUrl
                self.logger.info("done finding the image url")
                return True
            else:
                self.logger.error("can't find img url")
        except:
            self.logger.error("can't find the big image url")
            return False

    def getAlluserInfo(self):
        if self.name and self.phoneNumber:
            x.checkIfWhatsAppLoaded()
            x.searchContact()
            x.getAbout()
            x.getSmallImageUrl()
            x.OpenContact()
            x.OpenContactInfo()
            x.findImageLink()
        else:
            self.logger.error("can't find user name or phoneNumber")

    def downloadUesrImage(self):
        if self.imageUrl and self.Person.name :
            BigImage = SharedMethods.Image(ImageURL=self.imageUrl, ImageName=f'big{self.Person.name}')
            BigImage.DownloadImage()
    
    def checkIfUserChangedPic(self):
        current

    def createUserFoldar(self):
        pass # username foldar then whats twiiter etc - whatss > images: about:
            
    def sendMessage(self):
        pass

    def GetUserProfilePicLink(self):
        pass

    def DownloadUserProfilePic(self):
        pass

    def CheckIfUserChagedProfilePic(self):
        pass





if __name__ == "__main__":
    print("hello")
    x = WhatsApp(name="mano",phoneNumber="+20 10 1964 9231")
    x.creatWhatssAppDriver()
    x.getAlluserInfo()
    x.downloadUesrImage()
    i = input("quite: ")
    x.driver.quit()
    