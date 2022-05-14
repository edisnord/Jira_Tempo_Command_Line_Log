import log
from datetime import datetime

logLink = "https://api.tempo.io/core/3/worklogs"
userID = ""
dateTo = None
numberOfErrors = 0
name = input("Input your Jira display name and surname: \n")
logDate = input(
    "Input a day in which you've logged something on Tempo(YYYY-MM-DD)(necessary to find your user ID through the worklog): \n")

lines = log.readData()

for configShift in range(int(len(lines) / 5)):
    log.startLog(name, logDate, lines, configShift)

if log.numberOfErrors > 0:
    logtxt = open("log" + datetime.now().strftime("%d-%m-%Y") + ".txt", "a")
    logtxt.write("\n\nVery sorry for the inconvenience, the bug will be fixed soon :)\n\n")
    logtxt.close()