import requests
from bs4 import BeautifulSoup

url = 'https://www.apindustries.gov.in/SPS/UserAccount/LocationMap.aspx'
response = requests.get(url)
print(response) #checking if it worked ; 200- Okay

soup = BeautifulSoup(response.text, 'html.parser') #parsing
mydiv = soup.find("div", attrs={"class": "container-fluid"})  #finding the parent div tag
scripts = mydiv.findAll('script')[1] #getting the script tag
# scripts

scripts_Str = scripts.string.strip()
scripts_Str = scripts_Str.replace('\r\n','')
scripts_Str=scripts_Str[:-1]+" "+scripts_Str[-1]
scripts_Str[-20:]

import re
# import json

pattern = 'var markers = (.*?) ;'
p = re.match(pattern, scripts_Str)
p.groups()
# p.string
d = p.groups()[0]
d[:1000]
# data = json.loads(p.groups()[0])

dataform = str(p.groups()[0]).strip("'<>() ").replace('\'', '\"')
# dataform[:10000]
dataform=dataform.split("}    ,")   #splitting companies by },
# print(len(dataform)) - 36271
dataform=[i.split("            {            ")[1].strip() for i in dataform]  #cleaning companies by also removing { by making into a list
# print(len(dataform)) - 36271
dataform[:5]

x1 = """<table><tr style="height:30px;"><td style="width:180px;">"""
x2 = """</td><td style="width:20px;">:</td><td><b>"+"""
x3 = """+"</b></td></tr><tr style="height:30px;"><td>"""
x4 = """</td><td>:</td><td><b>"+"""
x5 = """+"</b></td></tr></table><b>"""
dataform=[i.replace(x1," ").replace(x2," ").replace(x3, " ").replace(x4, " ").replace(x5," ") for i in dataform]  #removing the tags in description to clean it
# dataform[:5]

dataform1 = [[j.strip() for j in i.split(",")]for i in dataform]  #splitting a company by type
len(dataform1[0])

import pandas as pd
df = pd.DataFrame(columns=['Industry Name','Latitude','Longitude','Category', 'District Name','Sector Name','Activity Name','Pollution Index Category','Total Workers'])
for company in dataform1:
#   print(company)
  IN = company[0][10:len(company[0])-1]
  LT = company[1][8:len(company[1])-1]
  LN = company[2][8:len(company[2])-1]
  CT = company[-1][12:len(company[-1])-5]
  des = list(filter(("").__ne__,company[4].split("\"")[3:-2]))
  print(des)
  DN = des[3]
  if len(des)== 4:
      des.append('NA')
      des.append('NA')
  SN = des[5]
  if len(company)>6:
      a = list(filter(("").__ne__,company[5].split("\"")[0:1]))
      b = list(filter(("").__ne__,company[5].split("\"")[2:3]))
      if len(b) == 0:
          b.append('NA')
      c = list(filter(("").__ne__,company[5].split("\"")[3:-2]))
      if len(c) < 2:
          c.append('NA')
          c.append('NA')
    #   print(c)
      AN = a[0]
      PI = b[0]
      TW = c[1]
  else:
    AN = des[7]
    PI = des[9]
    if len(des) == 11:
        des.append('NA')
    TW = des[11]
  df = df.append({'Industry Name' : IN, 'Latitude' : LT, 'Longitude' : LN,'District Name' :DN,'Sector Name':SN,'Activity Name':AN,'Pollution Index Category':PI,'Category':CT,'Total Workers':TW},  
                ignore_index = True)
df['Total Workers'].unique()

df

df.shape

df.to_csv('AP_Industries_location.csv')

