import threading

import requests
import json
from datetime import datetime
from datetime import timedelta

logLink = "https://api.tempo.io/core/3/worklogs"
userID = ""
dateTo = None

def log(task, hrs, billableHrs, date, time, userID):
    global json
    json = json.dumps({
        "issueKey": task,
        "timeSpentSeconds": hrs,
        "billableSeconds": billableHrs,
        "startDate": date.strftime("%Y-%m-%d"),
        "startTime": time,
        "authorAccountId": userID,
        "attributes": [
            {
                "key": "_WorklogValue_",
                "value": "60.0"
            },
            {
                "key": "_RevenueRate_",
                "value": "60.0"
            },
            {
                "key": "_Category_",
                "value": "A"
            },
            {
                "key": "_Location1_",
                "value": "Smart-working"
            }
        ]
    })

    requests.post(url=logLink,
                  headers=data,
                  data=json)




name = input("Your Jira display name and surname: \n")
logDate = input("A day in which you've logged something on Tempo(YYYY-MM-DD): \n")

with open('data.txt') as f:
    lines = f.readlines()
    token = lines[0].replace('\n', '')
    task = lines[1].replace('\n', '')
    if len(lines) >= 3:
        nonProcessedDate = lines[2].replace('\n', '')
    if len(lines) >= 4:
        time = lines[3].replace('\n', '')
    if len(lines) >= 5:
        hrs = str(int(float(lines[4]) * 3600))
    if len(lines) >= 6:
        billableHrs = str(int(float(lines[4]) * 3600))

if nonProcessedDate.count('-') > 2:
    date = datetime.strptime(nonProcessedDate[0:10], "%Y-%m-%d")
    dateTo = datetime.strptime(nonProcessedDate[11:22], "%Y-%m-%d")
else:
    date = datetime.strptime(nonProcessedDate, "%Y-%m-%d")

dateTime = datetime.strptime(logDate, "%Y-%m-%d") + timedelta(days=1)

data = {"Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "User-Agent": "PostmanRuntime/7.29.0",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"}

accIDLink = logLink + "?from=" + logDate + "&to=" + dateTime.strftime("%Y-%m-%d") + "&limit=1000"
accIDReq = requests.get(url=accIDLink,
                        headers=data
                        )

issuesJson: dict = accIDReq.json()
results: list = issuesJson.get("results")
for a in results:
    if a.get("author").get("displayName") == name:
        userID: str = a.get("author").get("accountId")
        break

if userID == "":
    print("No issue found on given date for user, exiting...")
    exit(100)

if dateTo is not None:
    for a in range((dateTo - date).days):
        threading.Thread.start()