#!/usr/bin/python3
# FBTools by Ashish Chaudhary [http://github.com/yankee101]

import selenium.webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pickle
import re
import os

def cookieDumper(driver):
   pickle.dump(driver.get_cookies() , open("cookies.pkl","wb"))
  

def cookieInjector(driver):

   if os.path.isfile("cookies.pkl") == True:
      cookies = pickle.load(open("cookies.pkl", "rb"))
      for cookie in cookies:
         driver.add_cookie(cookie)

def login(driver):
   print("Provide your credentials for login.")
   print("Credentials are not stored and required only once...")
   email = input("Email/Username/Phone : ")
   password = input("Password : ")
   
   print("Attempting Login...")
   
   driver.get("http://0.facebook.com")
   driver.find_element_by_name("email").send_keys(email)
   driver.find_element_by_name("pass").send_keys(password + Keys.RETURN)

   dummy = 0

   try:
      if driver.find_element_by_name("xc_message").is_displayed() == True:
         print("Successfully logged in. Dumping Cookies...")
         cookieDumper(driver)
         print("Dumped Cookies")
         print("xxxxxxx")
         print("Wait...")
         print("xxxxxxx")
         notInList(driver)
   except NoSuchElementException:
         dummy += 1

   if dummy == 1:
      print("Unable to login, try again later.")
   

def loginChecker():
   if os.path.isfile("cookies.pkl") == True:
      return True
   else:
      return False
    

def friendWriter(friendList):
   if os.path.isfile("friendlist.pkl") == True:
      file = open("friendList.pkl",'wb')
   else:
      print("Generating Friend List for the first time.")
      file = open("friendList.pkl",'wb')
   
   pickle.dump(friendList,file)


def friendComparator(newList):

   print("Finding who unfriended you! (or you unfriended them)")
   kickingFriends = []

   print(len(newList))
   
   if os.path.isfile("friendList.pkl") == True:
      oldFile = pickle.load(open("friendList.pkl", "rb"))

   for line in oldFile:
      if line.rstrip() not in newList:
         kickingFriends.append(line)
   else:
      print("Failed to find the Old Friend List")
      print("Writing new Friend List")

   friendWriter(newList)

   return kickingFriends

def notInList(driver):
   comparison = friendComparator(friendList(driver))
   if comparison == []:
      print("")
      print("xxxxxxx")
      print("No new Un-friends")
   else:
      print("These prople are no more in your friend list: ")
      print("")
      print("xxxxxxx")
      for kickingFriend in comparison:
         print(kickingFriend)

def friendList(driver):

   holder = []
   
   driver.get("http://m.facebook.com")

   cookieInjector(driver)
   
   n = 0
   dummy = 0
   
   print("Fetching Friend List...")

   while n <= 500:
      try:
         driver.get("https://m.facebook.com/friends/center/friends/?ppk={}".format(n))
         a = 1
         while a<= 10:
            element = driver.find_element_by_xpath('//*[@id="friends_center_main"]/div[2]/div[{}]/table/tbody/tr/td[2]/a'.format(a))
            print (element.text)
            holder.append(element.text)
            driver.save_screenshot('out.png')
            a += 1
         n += 1
      except NoSuchElementException:
         try:
            elem = driver.find_element_by_xpath('//*[@id="friends_center_main"]/div[2]/div[1]/table/tbody/tr/td[2]/a')
            n += 1
         except:
            break

   print("")
   
   return holder

 
def main():

   dcap = dict(DesiredCapabilities.PHANTOMJS)
   dcap["phantomjs.page.settings.userAgent"] = (
       "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0"
   )
   
   serviceArgs = ['--load-images=no',]
   
   driver=selenium.webdriver.PhantomJS(desired_capabilities=dcap,service_args=serviceArgs)

   if loginChecker() == True:
      print("Attempting Login...")
      notInList(driver)
   else:
      login(driver)
      
   freezer = input("xxxxxxx\n") #screen freeze

if __name__ == "__main__":main()
