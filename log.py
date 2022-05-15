numberOfErrors = 0
logLink = "https://api.tempo.io/core/3/worklogs"
token = ""

def logtotempo(task, hrs, billableHrs, date, time, userID, data):
    global numberOfErrors
    global logLink
    import json
    import requests

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
        logError(json, request, data)



def logError(json, request, data):
    global numberOfErrors
    from datetime import datetime
    import re
    print("Logging to log" + datetime.now().strftime("%d/%m/%Y") + ".txt, please send the log to the "
                                                                            "developer of the script")
    logtxt = open("log" + datetime.now().strftime("%d-%m-%Y") + ".txt", "a")
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


def readData():
    import re
    global token
    lines = [x for x in open("data.txt").readlines() if x[0:1] != "#" and x[0:1] != "\n"]
    token = re.sub(r'^.*?:', '', lines[0].replace('\n', ''))
    lines.pop(0)
    return lines

def logThruFile(name, logDate, lines, configShift):
    import re
    import json
    import threading
    import time
    import requests
    from datetime import datetime
    from datetime import timedelta

    logLink = "https://api.tempo.io/core/3/worklogs"
    userID = ""
    dateTo = None
    global numberOfErrors
    global token

    configShift = configShift * 5
    task = re.sub(r'^.*?:', '', lines[0 + configShift].replace('\n', ''))
    nonProcessedDate = re.sub(r'^.*?:', '', lines[1 + configShift].replace('\n', ''))
    timeR = re.sub(r'^.*?:', '', lines[2 + configShift].replace('\n', ''))
    if re.compile("^[0-9]{2}-[0-9]{2}-[0-9]{2}$").match(timeR) is None:
        print("Wrong time format, exiting...")
        exit(100)
    hrs = str(int(float(re.sub(r'^.*?:', '', lines[3 + configShift]).replace("\n", '')) * 3600))
    billableHrs = str(int(float(re.sub(r'^.*?:', '', lines[4 + configShift]).replace("\n", '')) * 3600))

    if nonProcessedDate.count('-') > 2:
        date = datetime.strptime(nonProcessedDate[0:10], "%Y-%m-%d")
        dateTo = datetime.strptime(nonProcessedDate[11:22], "%Y-%m-%d")
    else:
        date = datetime.strptime(nonProcessedDate, "%Y-%m-%d")
    try:
        dateTime = datetime.strptime(logDate, "%Y-%m-%d") + timedelta(days=1)
    except Exception:
        print("Inserted wrong date format in console input, exiting...")
        exit(100)

    data = {"Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "User-Agent": "PostmanRuntime/7.29.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"}

    accIDLink = logLink + "?from=" + logDate + "&to=" + dateTime.strftime("%Y-%m-%d") + "&limit=1000"
    try:
        accIDReq = requests.get(url=accIDLink,
                                headers=data
                                )
    except Exception:
        print(
            "You seem to have issues connecting to the internet, please fix any connectivity issues before running this script")
        exit(500)

    if accIDReq.status_code != 200:
        print("Wrong API key in data.txt, check if you key is expired/wrong")
        exit(401)

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
            threads.append(threading.Thread(target=logtotempo,
                                            args=(task, hrs, billableHrs, date + timedelta(days=a), timeR, userID, data)))
        for a in range(len(threads)):
            threads[a].start()
        for a in range(len(threads)):
            threads[a].join()
    else:
        logtotempo(task, hrs, billableHrs, date, timeR, userID, data)

def logThruConsole(name, logDate, lines):
    import re
    import json
    import threading
    import time
    import requests
    from datetime import datetime
    from datetime import timedelta

    logLink = "https://api.tempo.io/core/3/worklogs"
    userID = ""
    dateTo = None
    global numberOfErrors
    global token

    task = input("Insert an issue code:")
    print("(You can also insert a date range just like in data.txt)")
    nonProcessedDate = input("Enter a work date(leave empty for today's date)(Format YYYY-MM-DD):")
    timeR = input("Work start time(Format HH-MM-SS):")
    if re.compile("^[0-9]{2}-[0-9]{2}-[0-9]{2}$").match(timeR) is None:
        print("Wrong time format, exiting...")
        exit(100)
    try:
        hrs = str(int(float(input("How many hours did you work?")) * 3600))
        billableHrs = str(int(float(input("How many of these hours were billable?")) * 3600))
    except ValueError:
        print("Wrong hour format, exiting")
        exit(200)
    if int(hrs) > 24 * 3600 or int(billableHrs) > 24 * 3600:
        print("Wrong hour format, exiting")
        exit(200)

    if nonProcessedDate.count('-') > 2:
        date = datetime.strptime(nonProcessedDate[0:10], "%Y-%m-%d")
        dateTo = datetime.strptime(nonProcessedDate[11:22], "%Y-%m-%d")
    elif nonProcessedDate == "":
        date = datetime.now()
    else:
        date = datetime.strptime(nonProcessedDate, "%Y-%m-%d")

    try:
        dateTime = datetime.strptime(logDate, "%Y-%m-%d") + timedelta(days=1)
    except Exception:
        print("Inserted wrong date format in console input, exiting...")
        exit(100)

    data = {"Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "User-Agent": "PostmanRuntime/7.29.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"}

    accIDLink = logLink + "?from=" + logDate + "&to=" + dateTime.strftime("%Y-%m-%d") + "&limit=1000"
    try:
        accIDReq = requests.get(url=accIDLink,
                                headers=data
                                )
    except Exception:
        print(
            "You seem to have issues connecting to the internet, please fix any connectivity issues before running this script")
        exit(500)

    if accIDReq.status_code != 200:
        print("Wrong API key in data.txt, check if you key is expired/wrong")
        exit(401)

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
            threads.append(threading.Thread(target=logtotempo,
                                            args=(
                                            task, hrs, billableHrs, date + timedelta(days=a), timeR, userID, data)))
        for a in range(len(threads)):
            threads[a].start()
        for a in range(len(threads)):
            threads[a].join()
    else:
        logtotempo(task, hrs, billableHrs, date, timeR, userID, data)
