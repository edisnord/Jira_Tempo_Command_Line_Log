import log
import sys, getopt
from datetime import datetime

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hfc", ["help", "file", "console"])
    except getopt.GetoptError:
        print("main.py --help or -h for all available arguments")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print("main.py arguments: \n"
                  "     -h or --help : help\n"
                  "     -c or --console : console mode\n"
                  "     -f or --file : file mode\n")
            sys.exit()

    if len(opts) == 0:
        print("main.py --help or -h for all available arguments")
        sys.exit(0)

    logLink = "https://api.tempo.io/core/3/worklogs"
    userID = ""
    dateTo = None
    numberOfErrors = 0
    name = input("Input your Jira display name and surname: \n")
    logDate = input(
        "Input a day in which you've logged something on Tempo(YYYY-MM-DD)(necessary to find your user ID through the worklog): \n")

    lines = log.readData()

    for opt, arg in opts:
        if opt in ("-f", "--file"):
            for configShift in range(int(len(lines) / 5)):
                log.logThruFile(name, logDate, lines, configShift)

        elif opt in ("-c", "--console"):
                log.logThruConsole(name, logDate, lines)

    if log.numberOfErrors > 0:
        logtxt = open("log" + datetime.now().strftime("%d-%m-%Y") + ".txt", "a")
        logtxt.write("\n\nVery sorry for the inconvenience, the bug will be fixed soon :)\n\n")
        logtxt.close()

if __name__ == "__main__":
   main(sys.argv[1:])
