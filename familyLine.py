# -*- coding: utf-8 -*-
import re
import os
import datetime
import requests
import lxml
from  bs4 import BeautifulSoup

headers = {"User-Agent":"Mozilla/5.0"}

horse = "オルフェーヴル"
send  = False
sendmessage  = "今週の{}産駒".format(horse) + "\n"
sendmessage2 = ""

url = "https://keiba.yahoo.co.jp"
    
html = requests.get(url, headers=headers)
soup = BeautifulSoup(html.text, "lxml")

days = soup.find_all("td", class_="txC topRaceInfoDay")
for day in days:
    dayInfo = day.find("a").get("href").split("list/")[1].split("/")[0]
    
    dayInfoURL = "https://keiba.yahoo.co.jp/race/list/{}/".format(dayInfo)
    html2 = requests.get(dayInfoURL, headers=headers)
    soup2 = BeautifulSoup(html2.text, "lxml")

    nrace = soup2.find_all("p", class_= "scheRNo")

    for i in range(1, len(nrace)+1):
        race = str(i).zfill(2)
        raceInfo = dayInfo + race
        raceCard = "https://keiba.yahoo.co.jp/race/denma/{}/".format(raceInfo)
        html3 = requests.get(raceCard, headers=headers)
        soup3 = BeautifulSoup(html3.text, "lxml")

        raceName   = soup3.find("h1", class_="fntB").text
        raceNum    = soup3.find(id="raceNo").text
        raceCourse = soup3.find(id="racePlaceNaviC").text
        raceDay    = soup3.find(id="raceTitDay").text.split("|")[0].split("（")[1].split("）")[0] + "曜日"

        rows  = soup3.find("table", class_= "denmaLs mgnBL").find_all("tr")
        rows.pop(0)

        message   = "-----\n" + raceDay + " " + raceCourse + raceNum + " " + raceName + "\n"
        raceSend  = False
        for column in rows:
            parents = column.find_all("td")[5].text
            if horse in parents:
                raceSend  = True
                send      = True
                horseName = column.find_all("td")[2].find("a").find("strong").text
                frame     = column.find_all("td")[0].find("span").text
                number    = column.find_all("td")[1].find("strong").text
                message   += frame + "枠" + number + "番 " + horseName + "\n"

        if raceSend:
            if len(sendmessage) < 950:
                sendmessage += message
            else:
                sendmessage2 += message

if send:
    notifyUrl  = "https://notify-api.line.me/api/notify"
    token      = "Nm5SHHp6sln1zKiN9VNOJHs0387yoAK5CFyOpawnSwW"
    apiHeaders = {"Authorization" : "Bearer "+ token}
    payload    = {"message" :sendmessage}
    r          = requests.post(notifyUrl ,headers = apiHeaders ,params=payload)

    payload    = {"message" :sendmessage2}
    r          = requests.post(notifyUrl ,headers = apiHeaders ,params=payload)
