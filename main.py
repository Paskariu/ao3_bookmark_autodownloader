import AO3
import os
import re
import urllib
from bs4 import BeautifulSoup
import time

username="paskariu"
directory="bookmarks"
formats=["PDF","EPUB",]
formatIndex=1
timeoutSeconds=20

def main():
  menu()
  if not os.path.exists(directory):
    os.makedirs(directory)
  getBookmarkedWorks()

def menu():
  print("Please enter your username:")
  username=input()
  print("Please select the downloadformat:")
  for i in range(0,len(formats)):
    print("["+str(i+1)+"]"+formats[i])
  formatIndex=int(input())-1
  print("The directoryname will be 'bookmarks'.")
  print("Works will now be downloaded. This could take a while.")

def getBookmarkedWorks():
  for i in range(1,AO3.User(username).bookmarks+1):
    baseUrl="https://archiveofourown.org/bookmarks/search?utf8=%E2%9C%93&bookmark_search%5Bbookmarkable_query%5D=&bookmark_search%5Bother_tag_names%5D=&bookmark_search%5Bbookmarkable_type%5D=&bookmark_search%5Blanguage_id%5D=&bookmark_search%5Bbookmarkable_date%5D=&bookmark_search%5Bbookmark_query%5D=&bookmark_search%5Bother_bookmark_tag_names%5D=&bookmark_search%5Bbookmarker%5D="+username+"&bookmark_search%5Bbookmark_notes%5D=&bookmark_search%5Brec%5D=0&bookmark_search%5Bwith_notes%5D=0&bookmark_search%5Bdate%5D=&bookmark_search%5Bsort_column%5D=created_at&commit=Search+Bookmarks&page="+str(i)+""
    soup = BeautifulSoup(urllib.request.urlopen(baseUrl),"html.parser")
    for temp in soup.find_all(class_="heading"):
      for line in temp.findChildren(href=re.compile("/works/.")):
        tempWork=AO3.Work((str(line).split('"')[1].split("/")[2]))
        print("Downloading: " + tempWork.title)
        downloadWork(tempWork)
    print("Sleep for " + str(timeoutSeconds) + " seconds to prevent networktimeout")
    time.sleep(timeoutSeconds)

def downloadWork(work):
  filename = validateFilename(work.title) + "." + formats[formatIndex].lower()
  with open(os.path.join(directory,filename), "wb") as file:
    file.write(work.download(formats[formatIndex]))

def validateFilename(name):
  return re.sub('[<>?"/\\|*?]','',name)

if __name__ == "__main__":
  main()