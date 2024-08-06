import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from openpyxl.workbook import Workbook
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import itertools

# Define the days
week = ['M', 'T', 'W', 'R', 'F']

# Generate all possible non-empty combinations of the days
combinations = []
for r in range(1, len(week) + 1):
    combinations += [''.join(c) for c in itertools.combinations(week, r)]


df2 = []


def parser(matching_links):
  headless = Options()
  headless.add_argument('-headless')
  driver = webdriver.Edge(options= headless)
  df = []

  for s in matching_links:
    currenturl =str(s).split()[1]
    currenturl=currenturl.split('/')[4]
    subject = currenturl[0:len(currenturl)-2]
    url = "https://courses.illinois.edu/schedule/2024/fall/" + subject
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    pattern = re.compile(r'schedule/2024/fall/' + subject + '/[^/]+')
    other_links = soup.find_all('a', href=pattern)
    for s in other_links:
      currenturl =str(s).split()[1]
      currenturl = currenturl.split('/')[5]
      course_number = currenturl[0:len(currenturl)-2]
      url = "https://courses.illinois.edu/schedule/2024/fall/" + subject + "/" + course_number
      driver.get(url)
      classes = subject + " " + course_number
      infos = driver.find_elements(By.XPATH, "//*[@id=\"section-dt\"]/tbody/tr")
      for element in infos:
        column_list = element.text.splitlines()         
        lecture, time, days, location = None, None, None, None
        for line in column_list:
          if ((len(column_list) >=3)) :
            if (column_list[2] == "Lecture"):
                lecture = "Lecture"
            if (("AM" in line) | ("PM" in line)):
                time = line
            if (line in combinations):
              days = line
            if (len(column_list) > 6):
              location = column_list[6]
            else:
              location = "TBD"            
            if all([lecture, time, days, location]):
              data = {"Classes": classes, "Type": lecture, "Time": time, "Days": days, "Location": location}
              df.append(data)
              break   
  df = pd.DataFrame(df)
  driver.quit()
  return df
  
            
        #print(infos.text) 
      
      
      
     
     # r = requests.get(url)
    #  soup = BeautifulSoup(r.text, "html.parser")
     # table = soup.find(id = "section-dt")
      #tables = pd.read_html(url) 
      
                
     # th = table.find_all("td", class_ = "app-meeting")
      #for t in th:
       # print(t.text)
    #final_link = table.find("td").renderContents().strip()
    #for s in final_link:
    #    print(str(s))
  #index+= 1





url = "https://courses.illinois.edu/schedule/2024/fall"
r = requests.get(url)


soup = BeautifulSoup(r.text, "html.parser")


pattern = re.compile(r'schedule/2024/fall/[^/]+')  # Match any character after 'spring/' except '/'
subjects = soup.find_all('a', href=pattern)

df2 = parser(subjects)
print(df2)
df2.to_excel("course_explorer.xlsx",
             sheet_name='Sheet_name_1', index = False)
# Extract the 'href' attribute value

