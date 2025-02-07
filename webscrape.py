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
    url = "https://courses.illinois.edu/schedule/2025/spring/" + subject
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    pattern = re.compile(r'schedule/2025/spring/' + subject + '/[^/]+')
    other_links = soup.find_all('a', href=pattern)
    for s in other_links:
      currenturl =str(s).split()[1]
      currenturl = currenturl.split('/')[5]
      course_number = currenturl[0:len(currenturl)-2]
      url = "https://courses.illinois.edu/schedule/2025/spring/" + subject + "/" + course_number
      driver.get(url)
      classes = subject + " " + course_number
      infos = driver.find_elements(By.XPATH, "//*[@id=\"section-dt\"]/tbody/tr")
      name = driver.find_element(By.XPATH, "//*[@id=\"app-course-info\"]/div[1]")
      coursename = name.text.splitlines()[0]
      for element in infos:
        column_list = element.text.splitlines()         
        lecture, time, days, location, instructor = None, None, None, None, None
        for line in column_list:
          if ((len(column_list) >=3)) :
            if (column_list[2] == "Lecture"):
                lecture = "Lecture"
            if (column_list[2] == "Lecture-Discussion"):
                lecture = "Lecture-Discussion"
            if (("AM" in line) | ("PM" in line)):
                time = line
            if (line in combinations):
              days = line
            if (len(column_list) > 6):
              location = column_list[6]
            else:
              location = "TBD"  
            if len(column_list) > 7:
              instructor = column_list[7] 
              if len(column_list) > 8:
                 instructor = instructor + ", " + column_list[8]  
            else:
               instructor = "TBD"
            if all([lecture, time, days, location, instructor]):
              data = {"CourseName": coursename, "Classes": classes, "Type": lecture, "Time": time, "Days": days, "Location": location, "Instructor": instructor}
              df.append(data)
              break   
  df = pd.DataFrame(df)
  driver.quit()
  return df
  
            
url = "https://courses.illinois.edu/schedule/2025/spring"
r = requests.get(url)


soup = BeautifulSoup(r.text, "html.parser")

pattern = re.compile(r'schedule/2025/spring/[^/]+')  # Match any character after 'spring/' except '/'
subjects = soup.find_all('a', href=pattern)
df2 = parser(subjects)
print(df2)
df2.to_excel("lastone.xlsx",
             sheet_name='Sheet_name_1', index = False)


