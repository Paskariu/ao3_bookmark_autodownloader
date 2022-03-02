from getpass import getuser
import AO3
import os
import re
import urllib
from bs4 import BeautifulSoup
import time

directory="bookmarks"
formats=["AZW3","PDF","MOBI","EPUB","HTML"]
formatIndex=0
timeoutSeconds=240
countDownloads=0

def main():
  username = getUsername()
  print("Please select the downloadformat:")
  for i in range(0,len(formats)):
    print("["+str(i+1)+"]"+formats[i])
  global formatIndex
  formatIndex=int(input())-1
  print("The directoryname will be 'bookmarks'.")
  if not os.path.exists(directory):
    os.makedirs(directory)
  print("Do you want to download private bookmarks as well? (Requires login) (y/n)")
  if input().lower() == "y":
    print("Please enter your password:")
    password = input()
    getBookmarkedWorksLoggedIn(username,password)
  else:
    getBookmarkedWorksAsGuest(username)
  print("Downloads finished. This application will now stop.")

def getBookmarkedWorksAsGuest(username):
  print("Works will now be downloaded. This could take a while.")
  for i in range(1,AO3.User(username).bookmarks+1):
    baseUrl="https://archiveofourown.org/bookmarks/search?utf8=%E2%9C%93&bookmark_search%5Bbookmarkable_query%5D=&bookmark_search%5Bother_tag_names%5D=&bookmark_search%5Bbookmarkable_type%5D=&bookmark_search%5Blanguage_id%5D=&bookmark_search%5Bbookmarkable_date%5D=&bookmark_search%5Bbookmark_query%5D=&bookmark_search%5Bother_bookmark_tag_names%5D=&bookmark_search%5Bbookmarker%5D="+username+"&bookmark_search%5Bbookmark_notes%5D=&bookmark_search%5Brec%5D=0&bookmark_search%5Bwith_notes%5D=0&bookmark_search%5Bdate%5D=&bookmark_search%5Bsort_column%5D=created_at&commit=Search+Bookmarks&page="+str(i)+""
    parseTheSoupAndGetTheWorks(baseUrl)

def getBookmarkedWorksLoggedIn(username,password):
  print("Works will now be downloaded. This could take a while.")
  session = AO3.Session(username,password)
  for i in range(1,session.bookmarks+1):
    baseUrl="https://archiveofourown.org/bookmarks/search?utf8=%E2%9C%93&bookmark_search%5Bbookmarkable_query%5D=&bookmark_search%5Bother_tag_names%5D=&bookmark_search%5Bbookmarkable_type%5D=&bookmark_search%5Blanguage_id%5D=&bookmark_search%5Bbookmarkable_date%5D=&bookmark_search%5Bbookmark_query%5D=&bookmark_search%5Bother_bookmark_tag_names%5D=&bookmark_search%5Bbookmarker%5D="+username+"&bookmark_search%5Bbookmark_notes%5D=&bookmark_search%5Brec%5D=0&bookmark_search%5Bwith_notes%5D=0&bookmark_search%5Bdate%5D=&bookmark_search%5Bsort_column%5D=created_at&commit=Search+Bookmarks&page="+str(i)+""
    parseTheSoupAndGetTheWorks(baseUrl)

def parseTheSoupAndGetTheWorks(baseUrl):
  soup = BeautifulSoup(urllib.request.urlopen(baseUrl),"html.parser")
  for temp in soup.find_all(class_="heading"):
    for line in temp.findChildren(href=re.compile("/series/.")):
      tempSeries=AO3.Series(getIdFromSoupLine(line))
      for tempwork in tempSeries.work_list:
        tempwork.reload()
        print("Downloading: " + tempwork.title)
        downloadWork(tempwork)
    for line in temp.findChildren(href=re.compile("/works/.")):
      tempWork=AO3.Work(getIdFromSoupLine(line))
      print("Downloading: " + tempWork.title)
      downloadWork(tempWork)

def downloadWork(work):
  filename = validateFilename(work.title) + "." + formats[formatIndex].lower()
  with open(os.path.join(directory,filename), "wb") as file:
    file.write(work.download(formats[formatIndex]))
  global countDownloads
  countDownloads = countDownloads + 1
  timeout()

def timeout():
  if countDownloads%100==0:
    print("Sleep for " + str(timeoutSeconds) + " seconds to prevent networktimeout. Please remain patient.")
    time.sleep(timeoutSeconds)

def getIdFromSoupLine(line):
  return str(line).split('"')[1].split("/")[2]

def validateFilename(name):
  return re.sub('[<>?"/\\|*?]','',name)

def getUsername():
  print("Please enter your username:")
  return input()


if __name__ == "__main__":
  main()