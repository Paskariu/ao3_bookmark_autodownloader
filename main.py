import AO3
import os
import re
import inspect

def main():
  downloadWorks(getBookmarkedWorks(askForUsername()))

def askForUsername():
  print("Please enter your username:")
  return input()

def getBookmarkedWorks(username):
  print("Works will now be downloaded. This could take a while.")
  works=[]
  soup=AO3.User(username)._soup_bookmarks
  for temp in soup.find_all(class_="heading"):
    for line in temp.findChildren(href=re.compile("/works/.")):
      works.append(AO3.Work((str(line).split('"')[1].split("/")[2])))
  return(works)

def getBookmarkedWorksBySearch(username):
  for a in AO3.Search(Bookmarker=username):
    print(a.title)

def downloadWorks(works):
  directory="bookmarks"
  if not os.path.exists(directory):
    os.makedirs(directory)
  for work in works:
    filename = work.title + ".pdf"
    with open(os.path.join(directory,filename), "wb") as file:
      file.write(work.download("PDF"))

if __name__ == "__main__":
  main()