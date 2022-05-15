# Tempo command line time logging tool

This app's intent is to make logging time on Tempo's annoying UI easier using their API. 
The program works by inserting your API Key(can be created from the settings inside Tempo) into a 
text file called data.txt in the same directory with the script in the format:

API Key:$API_KEY <br />
Issue:$ISSUE_CODE <br />
Date:$DATE (Optionally another date to create a range) <br />
Start time:$TIME <br />
Hours:$HOURS <br />
Billable Hours:$BILLABLE_HOURS <br />

Do not change the order of the lines as that is how data is read from this file
, the text before the : character can be changed though, but you must never remove the : character or add any space 
between the : and the data you've added to the config, so it should be:

CUSTOM NAME:VALUE YOU'RE UPLOADING

You can also write comments and have spaces in the config.
The script also asks for your display name and a day when you have logged somethign in Tempo, because the 
API does not have a feature which tells you what user created the API key, so I had to take the uglier path to fixing the issue.

You can also chain multiple issues to be logged by adding 5 more lines describing the issues, again in the same order
as the template but this time excluding your API key, as it should always only be in the first line of the configuration

The program supports 2 execution modes, console mode and file mode which can be selected using a parameter when you run
main.py. Console mode supports the upload of only a single issue log(of course ranges are supported in dates)
Here's an example:
```bash
#for console mode
python main.py -c
#for file mode
python main.py -f
#either way you need to have an API key in the first line of data.txt
````