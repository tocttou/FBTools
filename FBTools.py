#!/usr/bin/python3
# FBTools by Ashish Chaudhary [http://github.com/yankee101]

import selenium.webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
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

def login():
   print("Provide your credentials for login.")
   print("Credentials are not stored and required only once...")
   email = input("Email/Username/Phone : ")
   password = input("Password : ")

   driver=selenium.webdriver.PhantomJS()
   
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
         notInList()
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

def notInList():
   comparison = friendComparator(friendList())
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

def friendList():

   holder = []
   driver=selenium.webdriver.PhantomJS()
   
   driver.get("http://0.facebook.com")

   cookieInjector(driver)
   
   dummy = 0

   print("Fetching Friend List",end='')

   for n in range(0,500):
      try:
         driver.get("https://0.facebook.com/friends/center/friends/?ppk={}".format(n))
         elements = driver.find_elements_by_class_name('bu')
         print(".",end='')
         for element in elements:
            if re.search("Report a Problem",element.text):
               dummy += 1
            if dummy == 0:
               holder.append(element.text)
         try:
            if driver.find_element_by_id('u_0_0').is_displayed() == False:
               break
         except:
            break
      except:
         print("Unable to get the Friend List.")

   print("")
   
   return holder

 
def main():

   if loginChecker() == True:
      print("Attempting Login...")
      notInList()
   else:
      login()
      
   freezer = input("xxxxxxx\n") #screen freeze

if __name__ == "__main__":main()

