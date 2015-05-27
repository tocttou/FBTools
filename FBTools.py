#!/usr/bin/python3
# FBTools by Ashish Chaudhary [http://github.com/yankee101]

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from pyfiglet import Figlet
import selenium.webdriver
import pickle
import sys
import re
import os

class FBLogin:

   def __init__(self):
      dcap = dict(DesiredCapabilities.PHANTOMJS)
      dcap["phantomjs.page.settings.userAgent"] = (
          "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0"
      )    
      serviceArgs = ['--load-images=no',]      
      self.driver=selenium.webdriver.PhantomJS(desired_capabilities=dcap,service_args=serviceArgs)
      

   def cookieDumper(self):
      pickle.dump(self.driver.get_cookies() , open("cookies.pkl","wb"))
     

   def cookieInjector(self):
      if os.path.isfile("cookies.pkl") == True:
         cookies = pickle.load(open("cookies.pkl", "rb"))
         self.driver.get("http://m.facebook.com")
         for cookie in cookies:
            self.driver.add_cookie(cookie)
         self.driver.get("http://m.facebook.com/settings")

   def login(self):
      print("Provide your credentials for login.")
      print("Credentials are not stored and required only once...")
      email = input("Email/Username/Phone : ")
      password = input("Password : ")
      
      print("Attempting Login...")
      
      self.driver.get("http://m.facebook.com/settings")
      self.driver.find_element_by_name("email").send_keys(email)
      self.driver.find_element_by_name("pass").send_keys(password + Keys.RETURN)

      dummy = 0

      try:
         if self.driver.find_element_by_xpath('//*[@id="header"]/form/table/tbody/tr/td[2]/input').is_displayed() == True:
            print("Successfully logged in. Dumping Cookies...")
            self.cookieDumper()
            print("Dumped Cookies")
            print("xxxxxxx")
            print("Wait...")
            print("xxxxxxx")
            self.notInList()
      except NoSuchElementException:
            dummy += 1

      if dummy == 1:
         print("xxxxxxx")
         print("Unable to login, try again later.")
      

   def loginChecker(self):
      if os.path.isfile("cookies.pkl") == True:
         return True
      else:
         return False

   def greeting(self):
      try:
         if self.driver.find_element_by_xpath('//*[@id="viewport"]/div[3]/div/table/tbody/tr/td[2]/a[3]').is_displayed() == True:
            name = self.driver.find_element_by_xpath('//*[@id="viewport"]/div[3]/div/table/tbody/tr/td[2]/a[3]')
            f = Figlet(font='slant')
            print(f.renderText(re.search('\((.*?)\)',name.text).group(1)))
      except NoSuchElementException:
            pass

   def friendWriter(self,friendList):
      if os.path.isfile("friendList.pkl") == True:
         file = open("friendList.pkl",'wb')
      else:
         print("Generating Friend List for the first time.")
         file = open("friendList.pkl",'wb')      
      pickle.dump(friendList,file)


   def friendComparator(self,newList):
      print("Finding who unfriended you! (or you unfriended them)")
      kickingFriends = []
     
      if os.path.isfile("friendList.pkl") == True:
         oldFile = pickle.load(open("friendList.pkl", "rb"))
         for line in oldFile:
            if line.rstrip() not in newList:
               kickingFriends.append(line)
      else:
         print("Failed to find the Old Friend List")
         print("Writing new Friend List")

      self.friendWriter(newList)

      return kickingFriends

   def notInList(self):
      comparison = self.friendComparator(self.friendList())
      if comparison == []:
         print("")
         print("xxxxxxx")
         print("No new Un-friends")
      else:
         print("These prople are no more in your friend list: ")
         print("CAUTION : If they haven't unfriended you, they may have deactivated their account temporarily. Or they may have blocked you.")
         print("")
         print("xxxxxxx")
         for kickingFriend in comparison:
            print(kickingFriend)

   def friendList(self):
      holder = []    
      n = 0
      dummy = 0
      
      print("Fetching Friend List",end='')

      while n <= 500:
         print(".",end='')
         sys.stdout.flush()
         try:
            self.driver.get("https://m.facebook.com/friends/center/friends/?ppk={}".format(n))
            a = 1
            while a<= 10:
               element = self.driver.find_element_by_xpath('//*[@id="friends_center_main"]/div[2]/div[{}]/table/tbody/tr/td[2]/a'.format(a))
               holder.append(element.text)
               a += 1
            n += 1
         except NoSuchElementException:
            try:
               elem = self.driver.find_element_by_xpath('//*[@id="friends_center_main"]/div[2]/div[1]/table/tbody/tr/td[2]/a')
               n += 1
            except:
               break

      print("")
      
      return holder

 
def main():

   test = FBLogin()
   f = Figlet(font='slant')
   print(f.renderText('FBTools\n------'))
   
   if test.loginChecker() == True:
      print("Attempting Login...")
      test.cookieInjector()
      test.greeting()
      test.notInList()
   else:
      test.login()
      
   freezer = input("xxxxxxx\n") #screen freeze

if __name__ == "__main__":main()
