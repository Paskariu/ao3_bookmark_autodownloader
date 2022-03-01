import AO3
import re

def main():
  for work in getBookmarkedWorks(askForUsername()):
    downloadWork(work)

def askForUsername():
  print("Please enter your username:")
  return input()

def getBookmarkedWorks(username):
  works=[]
  soup=AO3.User(username)._soup_bookmarks
  for temp in soup.find_all(class_="heading"):
    for line in temp.findChildren(href=re.compile("/works/.")):
      works.append(AO3.Work((str(line).split('"')[1].split("/")[2])))
  return(works)

def downloadWork(work):
  with open(f"{work.title}.pdf", "wb") as file:
    file.write(work.download("PDF"))

if __name__ == "__main__":
  main()