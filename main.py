import _thread
import re
import threading
import time
import requests
import json
from datetime import datetime
from datetime import timedelta

logLink = "https://api.tempo.io/core/3/worklogs"
userID = ""
dateTo = None
numberOfErrors = 0


def log(task, hrs, billableHrs, date, time, userID):
    import json
    global numberOfErrors
    json = json.dumps({
        "issueKey": task,
        "timeSpentSeconds": hrs,
        "billableSeconds": billableHrs,
        "startDate": date.strftime("%Y-%m-%d"),
        "startTime": time,
        "authorAccountId": userID,
        "attributes": [
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

    request = requests.post(url=logLink,
                            headers=data,
                            data=json)

    if request.status_code == 200:
        print("Logged date: " + date.strftime("%Y-%m-%d"))
    else:
        numberOfErrors += 1
        print("Error logging date " + date.strftime("%Y-%m-%d"))
        logError(json, request)


def logError(json, request):
    global numberOfErrors
    print("Logging to log.txt, please send the log to the developer of the script")
    logtxt = open("log.txt", "a")
    if numberOfErrors < 2:
        logtxt.write("Error date and time: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
        logtxt.write("Error code: " + str(request.status_code))
    else:
        logtxt.write("\n\nError number:" + str(numberOfErrors))
    logtxt.write("\nThe HTTP header for the request: \n")
    logtxt.write(re.sub(r'Authorization.*Content-Type', "Authorization\': \'Bearer HIDDEN', 'Content-Type", str(data)))
    logtxt.write("\nThe JSON data for the request \n")
    logtxt.write(str(json))
    logtxt.close()


name = input("Input your Jira display name and surname: \n")
logDate = input(
    "Input a day in which you've logged something on Tempo(YYYY-MM-DD)(necessary to find your user ID through the worklog): \n")

with open('data.txt') as f:
    lines = f.readlines()
    configShift = 0
    while configShift >= 0:
        if lines[configShift][0:1] == "#" or lines[configShift][0:1] == "\n":
            configShift += 1
        else:
            break

    token = re.sub(r'^.*?:', '', lines[0 + configShift].replace('\n', ''))
    task = re.sub(r'^.*?:', '', lines[1 + configShift].replace('\n', ''))
    nonProcessedDate = re.sub(r'^.*?:', '', lines[2 + configShift].replace('\n', ''))
    timeR = re.sub(r'^.*?:', '', lines[3 + configShift].replace('\n', ''))
    hrs = str(int(float(re.sub(r'^.*?:', '', lines[4 + configShift]).replace("\n", '')) * 3600))
    billableHrs = str(int(float(re.sub(r'^.*?:', '', lines[5 + configShift]).replace("\n", '')) * 3600))

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
    threads: list = []
    for a in range((dateTo - date).days + 1):
        threads.append(threading.Thread(target=log,
                                        args=(task, hrs, billableHrs, date + timedelta(days=a), timeR, userID)))
    for a in range(len(threads)):
        threads[a].start()
    for a in range(len(threads)):
        threads[a].join()

if numberOfErrors > 0:
    logtxt = open("log.txt", "a")
    logtxt.write("\n\nVery sorry for the inconvenience, the bug will be fixed soon :)\n\n")
    logtxt.close()
