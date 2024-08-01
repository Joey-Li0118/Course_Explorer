import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def parser(matching_links):
  for s in matching_links:
    currenturl =str(s).split()[1]
    currenturl=currenturl.split('/')[4]
    subject = currenturl[0:len(currenturl)-2]
    url = "https://courses.illinois.edu/schedule/2024/spring/" + subject
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    pattern = re.compile(r'schedule/2024/spring/' + subject + '/[^/]+')
    other_links = soup.find_all('a', href=pattern)
    for s in other_links:
      currenturl =str(s).split()[1]
      currenturl = currenturl.split('/')[5]
      course_number = currenturl[0:len(currenturl)-2]
      url = "https://courses.illinois.edu/schedule/2024/spring/" + subject + "/" + course_number
      r = requests.get(url)
      soup = BeautifulSoup(r.text, "html.parser")
      table = soup.find(id = "section-dt")
      info = table.find(div = "app-meeting" )
      print(info)
    #final_link = table.find("td").renderContents().strip()
    #for s in final_link:
    #    print(str(s))
  #index+= 1





url = "https://courses.illinois.edu/schedule/2024/spring"
r = requests.get(url)


soup = BeautifulSoup(r.text, "html.parser")


pattern = re.compile(r'schedule/2024/spring/[^/]+')  # Match any character after 'spring/' except '/'
subjects = soup.find_all('a', href=pattern)

parser(subjects)
# Extract the 'href' attribute value

